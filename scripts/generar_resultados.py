#!/usr/bin/env python3
"""Genera data/resultados.json: recomendación pre-partido + acertó/falló
y Marcador (pre-partido vs en vivo) para las nuevas funcionalidades
(orden Luis 28 nov 00:19, JEFE.md f51ccc0 + caee893).

Lee los dos ev.json (semana-2 y entresemana) + vivo.json + el log en vivo
(data/live-log/*.jsonl, si existe). NO inventa nada:
- REGLA DE RECOMENDACIÓN (Luis, 28 nov 11:16, corregida 11:21): el pick
  con MÁS PROBABILIDAD entre los que tienen VALOR (EV ≥ +5%), buscando
  en TODOS los mercados (1X2, Más/Menos X.5, Spread, BTTS). Color del
  semáforo (Luis 11:20, 11:35, 11:37-11:39, calibre final): VERDE =
  poco (o muy poco) riesgo y buena ganancia (prob ≥ 60% y EV ≥ +5%);
  AMARILLO = un 50/50 (30% ≤ prob < 60% y EV ≥ +5%); ROJO = los dos
  extremos: mucho riesgo pero mucha ganancia (prob < 30%, aunque tenga
  el EV más alto) o muy poco riesgo aparente y poca ganancia (EV < +5%,
  como el favorito a momio bajo con EV negativo). Si ningún pick llega
  a EV +5%, la recomendación NO desaparece: es el pick de mayor EV
  disponible en ROJO marcado "No cumple la regla", y Luis decide si
  apuesta. El mejor valor (EV+ máximo) queda como señal aparte, con
  su color por riesgo/ganancia. ALTERNATIVA AMARILLA (Luis 11:33,
  corregida 11:35): además se publica el pick arriesgado que vale la
  pena por lo que se gana: mayor EV entre los de EV ≥ +5% y 30% ≤ prob
  < 60%, distinto de la recomendación y con EV ≥ +50% (el premio debe
  justificar el riesgo). En el Inter–Genoa la amarilla es el EMPATE
  (30.7% @5.5, EV +68.8%), no la Visita @9.0 (22.6%: rojo); la doble
  oportunidad a favor del Genoa sería otra amarilla, pero hoy no hay
  momio para ella en los datos (pendiente: ver si BSD la trae).
- Sin resultado final publicado el acierto es null ("Pendiente").
- Sin snapshots en el log en vivo, la columna en vivo es "sin datos".

La predicción en vivo se deriva del ÚLTIMO snapshot del partido con el
mismo cálculo que partido.html (liveInvertirXG + liveCalc, gamma 0.25,
0.301 goles/TDA). Usa las probabilidades PUBLICADAS para invertir el xG
(no las ajustadas por XI oficial; la diferencia está topada por el ±12
del cap de Fuerza). Si no hay snapshot, no hay predicción en vivo.
"""

import json
import math
import os
import re
import sys
import unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MX = ZoneInfo("America/Mexico_City")

CONFIGS = [
    ("semana-2", "data/semana-2/ev.json"),
    ("entresemana", "data/semana-2-entresemana/ev.json"),
]

# --- live math: port fiel de partido.html (livePois/liveP1x2/
# liveInvertirXG/liveCalc). Solo TDA predice goles (corr 0.632);
# la posesión NO se usa en ningún ajuste. ---
_FACT = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800,
         39916800, 479001600]
_GAMMA = 0.25
_GOL_TDA = 0.301


def _pois(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(-lam) * (lam ** k) / _FACT[k]


def _p1x2(xg_h, xg_a, gh, ga):
    p1 = px = p2 = 0.0
    for i in range(13):
        for j in range(13):
            p = _pois(i, xg_h) * _pois(j, xg_a)
            th, ta = gh + i, ga + j
            if th > ta:
                p1 += p
            elif th == ta:
                px += p
            else:
                p2 += p
    s = p1 + px + p2
    return {"p1": p1 / s * 100, "px": px / s * 100, "p2": p2 / s * 100}


def _p_over(xg_h, xg_a, gh, ga, linea):
    t = 0.0
    for i in range(13):
        for j in range(13):
            if gh + i + ga + j > linea:
                t += _pois(i, xg_h) * _pois(j, xg_a)
    return t * 100


def _invertir_xg(p1, px, p2):
    def err(lh, la):
        q = _p1x2(lh, la, 0, 0)
        return (q["p1"] - p1) ** 2 + (q["px"] - px) ** 2 + (q["p2"] - p2) ** 2

    best = [1.5, 1.5]
    be = 1e9
    lh = 0.1
    while lh <= 4.6 + 1e-9:
        la = 0.1
        while la <= 4.6 + 1e-9:
            e = err(lh, la)
            if e < be:
                be = e
                best = [lh, la]
            la += 0.1
        lh += 0.1
    st = 0.05
    while st >= 0.005 - 1e-12:
        improved = True
        while improved:
            improved = False
            for dh in (-1, 0, 1):
                for da in (-1, 0, 1):
                    if not dh and not da:
                        continue
                    nh, na = best[0] + dh * st, best[1] + da * st
                    if nh < 0.05 or na < 0.05:
                        continue
                    e2 = err(nh, na)
                    if e2 < be:
                        be = e2
                        best = [nh, na]
                        improved = True
        st /= 2
    return {"lh": best[0], "la": best[1]}


def _live_calc(xg, p_pre, minuto, gh, ga, tda_h, tda_a):
    """Devuelve {p1, px, p2} en vivo. xg = {lh, la} invertido de las
    probabilidades publicadas; p_pre = {p1, px, p2} publicadas."""
    if not xg or not p_pre:
        return None
    rem = max(0.0, (90 - minuto) / 90)
    eff = _GAMMA * _GOL_TDA * ((tda_h or 0) - (tda_a or 0)) * rem
    xg_h = max(0.0, xg["lh"] * rem + eff)
    xg_a = max(0.0, xg["la"] * rem - eff)
    base = _p1x2(xg["lh"], xg["la"], 0, 0)
    now = _p1x2(xg_h, xg_a, gh, ga)

    def rel(nw, bs, pub):
        if not (bs > 0.05):
            return pub
        return pub * (nw / bs)

    p1 = rel(now["p1"], base["p1"], p_pre["p1"])
    px = rel(now["px"], base["px"], p_pre["px"])
    p2 = rel(now["p2"], base["p2"], p_pre["p2"])
    s = p1 + px + p2
    if not (s > 0):
        return None
    return {"p1": p1 / s * 100, "px": px / s * 100, "p2": p2 / s * 100}


def _norm(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _prob_1x2(m):
    """Probabilidades 1X2 publicadas, como derivar1X2 en partido.html:
    prob = (ev + 1) / momio * 100."""
    x = m["1X2"]
    out = {}
    for clave, momio_clave, ev_clave in (("p1", "home", "1"),
                                         ("px", "draw", "X"),
                                         ("p2", "away", "2")):
        momio = x["momios"].get(momio_clave)
        ev = x["ev"].get(ev_clave)
        if momio and ev is not None:
            out[clave] = (ev + 1) / momio * 100
    return out if len(out) == 3 else None


def _linea_txt(linea):
    return ("%.1f" % float(linea)).rstrip("0").rstrip(".")


def _color_por_prob_ev(prob, ev):
    """Color del semáforo por riesgo/ganancia (calibre final de Luis,
    28 nov 11:37-11:39, con el ejemplo Inter–Genoa):
    - VERDE: poco (o muy poco) riesgo y buena ganancia: prob ≥ 60% y
      EV ≥ +5%.
    - AMARILLO: un 50/50 (la zona incierta, donde puede pasar o no):
      30% ≤ prob < 60% y EV ≥ +5%.
    - ROJO: los dos extremos: (a) mucho riesgo pero mucha ganancia
      (prob < 30%, longshot, aunque tenga el EV más alto) o (b) muy
      poco riesgo APARENTE y poca ganancia (EV < +5%, como el favorito
      a momio bajo: se arriesga mucho para ganar poco y el EV es
      negativo; Luis: las de poco riesgo son las de mayor riesgo)."""
    if ev < 0.05:
        return "rojo"
    if prob >= 60:
        return "verde"
    if prob >= 30:
        return "amarillo"
    return "rojo"


def _candidatos(p):
    """Todos los picks de todos los mercados con momio, EV y probabilidad
    del modelo. Nombres idénticos a calcular_ev.py (y a _evaluar_pick):
    1X2 Local/Empate/Visita; Total Más/Menos X.5; Spread local/visitante
    ±X.5; BTTS Sí/No (solo cuando BSD trae sus momios; si no, momios y
    EV son None y el pick no entra); AH local/visitante ±X.5 (solo cuando
    BSD trae su hándicap asiático; líneas .5, sin push). Sin momio no hay
    EV: el pick no entra (nada inventado)."""
    mercados = p.get("mercados") or {}
    picks = []

    def agregar(mercado, nombre, momio, ev, prob):
        if momio is None or ev is None or prob is None:
            return
        try:
            momio = float(momio)
            ev = float(ev)
            prob = float(prob)
        except (TypeError, ValueError):
            return
        picks.append({"mercado": mercado, "pick": nombre,
                      "momio": momio, "ev": ev, "prob": prob})

    x12 = mercados.get("1X2") or {}
    if isinstance(x12.get("momios"), dict) and isinstance(x12.get("ev"), dict):
        for nombre, mk, ek in (("Local", "home", "1"),
                               ("Empate", "draw", "X"),
                               ("Visita", "away", "2")):
            momio = x12["momios"].get(mk)
            evv = x12["ev"].get(ek)
            prob = ((evv + 1) / momio * 100
                    if momio and evv is not None else None)
            agregar("1X2", nombre, momio, evv, prob)
    tot = mercados.get("total") or {}
    if isinstance(tot.get("momios"), dict) and isinstance(tot.get("ev"), dict):
        linea = tot.get("linea")
        p_over = tot.get("p_over")
        if linea is not None and p_over is not None:
            lt = _linea_txt(linea)
            agregar("Total", f"Más {lt}", tot["momios"].get("over"),
                    tot["ev"].get("mas"), p_over)
            agregar("Total", f"Menos {lt}", tot["momios"].get("under"),
                    tot["ev"].get("menos"), 100 - p_over)
    spr = mercados.get("spread") or {}
    if isinstance(spr.get("momios"), dict) and isinstance(spr.get("ev"), dict):
        pc = spr.get("p_cubre_local")
        hl = spr["momios"].get("home_linea")
        al = spr["momios"].get("away_linea")
        if pc is not None and hl is not None and al is not None:
            agregar("Spread", f"Spread local {hl:+.1f}",
                    spr["momios"].get("home"), spr["ev"].get("local"), pc)
            agregar("Spread", f"Spread visitante {al:+.1f}",
                    spr["momios"].get("away"), spr["ev"].get("visitante"),
                    100 - pc)
    btts = mercados.get("btts") or {}
    if isinstance(btts.get("momios"), dict) and isinstance(btts.get("ev"), dict):
        agregar("BTTS", "BTTS Sí", btts["momios"].get("si"),
                btts["ev"].get("si"), btts.get("p_btts"))
        agregar("BTTS", "BTTS No", btts["momios"].get("no"),
                btts["ev"].get("no"), btts.get("p_no_btts"))
    ah = mercados.get("asian_handicap") or {}
    if isinstance(ah.get("momios"), dict) and isinstance(ah.get("ev"), dict):
        la = ah.get("linea")
        pc_ah = ah.get("p_cubre_local")
        if la is not None and pc_ah is not None:
            agregar("AH", f"AH local {la:+.1f}",
                    ah["momios"].get("local"), ah["ev"].get("local"), pc_ah)
            agregar("AH", f"AH visitante {(-la):+.1f}",
                    ah["momios"].get("visitante"),
                    ah["ev"].get("visitante"), 100 - pc_ah)
    return picks


def _evaluar_pick(pick, gl, ga):
    """True si el pick acertó con el marcador final, False si falló,
    None si el formato no se reconoce (nunca se inventa un acierto)."""
    if pick in ("Local", "Visita", "Empate"):
        real = "Local" if gl > ga else ("Visita" if ga > gl else "Empate")
        return pick == real
    m = re.match(r"^(Más|Menos)\s+(\d+[.,]\d+)$", pick or "")
    if m:
        linea = float(m.group(2).replace(",", "."))
        total = gl + ga
        return total > linea if m.group(1) == "Más" else total < linea
    m = re.match(r"^Spread\s+(local|visita|visitante)\s+([+-]?\d+[.,]\d+)$", pick or "")
    if m:
        linea = float(m.group(2).replace(",", "."))
        margen = (gl - ga) if m.group(1) == "local" else (ga - gl)
        return margen + linea > 0
    m = re.match(r"^AH\s+(local|visita|visitante)\s+([+-]?\d+[.,]\d+)$", pick or "")
    if m:
        linea = float(m.group(2).replace(",", "."))
        margen = (gl - ga) if m.group(1) == "local" else (ga - gl)
        return margen + linea > 0
    if pick in ("BTTS Sí", "BTTS No"):
        ambos = gl > 0 and ga > 0
        return ambos if pick == "BTTS Sí" else not ambos
    return None


def _parse_minuto(txt):
    m = re.match(r"^\s*(\d+)", str(txt or ""))
    return int(m.group(1)) if m else None


def _leer_log_vivo(log_dir):
    """Último snapshot por partido (clave: nombres normalizados).
    El log es append-only JSONL por fecha; si no existe, {}."""
    ultimo = {}
    if not os.path.isdir(log_dir):
        return ultimo
    for nombre in sorted(os.listdir(log_dir)):
        if not nombre.endswith(".jsonl"):
            continue
        try:
            with open(os.path.join(log_dir, nombre), encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    try:
                        s = json.loads(linea)
                    except json.JSONDecodeError:
                        continue
                    clave = (_norm(s.get("home")), _norm(s.get("away")))
                    if not all(clave):
                        continue
                    cuando = s.get("cuando", "")
                    if clave not in ultimo or cuando >= ultimo[clave].get("cuando", ""):
                        ultimo[clave] = s
        except OSError:
            continue
    return ultimo


def main():
    vivo_path = os.path.join(ROOT, "data", "vivo.json")
    with open(vivo_path, encoding="utf-8") as f:
        vivo = json.load(f)
    por_nombre = {}
    for p in vivo.get("partidos", []):
        por_nombre[(_norm(p.get("home")), _norm(p.get("away")))] = p

    log = _leer_log_vivo(os.path.join(ROOT, "data", "live-log"))

    partidos = []
    for config, rel in CONFIGS:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            ev = json.load(f)
        for p in ev.get("partidos", []):
            home, away = p.get("home"), p.get("away")
            clave = (_norm(home), _norm(away))
            v = por_nombre.get(clave, {})
            estado = v.get("estado") or p.get("estado_partido") or "pre"
            gl = v.get("marcador_local")
            ga = v.get("marcador_visita")
            if gl is None and isinstance(p.get("marcador"), dict):
                gl = p["marcador"].get("local")
                ga = p["marcador"].get("visita")
            final = estado == "post" and gl is not None and ga is not None

            # REGLA FINAL (Luis 11:16 + 11:20 + 11:21, calibre final
            # 11:37-11:39): la recomendación es el pick con MÁS
            # PROBABILIDAD entre los que tienen VALOR (EV ≥ +5%), en
            # TODOS los mercados. Color por riesgo/ganancia: VERDE poco
            # riesgo y buena ganancia (prob ≥ 60% y EV ≥ +5%); AMARILLO
            # un 50/50 (30% ≤ prob < 60% y EV ≥ +5%); ROJO los dos
            # extremos (prob < 30% o EV < +5%). Si ningún pick llega a
            # +5%, la recomendación NO desaparece: es el pick de mayor
            # EV disponible en ROJO ("No cumple la regla"). El mejor
            # valor (EV+ máximo) queda como señal aparte, con su color.
            picks = _candidatos(p)
            if not picks and p.get("mejor_pick") and p.get("mejor_ev") is not None \
                    and p.get("mejor_decimal") is not None \
                    and p.get("mejor_prob") is not None:
                # Respaldo: ev.json viejo sin mercados (no debería pasar).
                picks = [{"mercado": "1X2", "pick": p["mejor_pick"],
                          "momio": p["mejor_decimal"],
                          "ev": p["mejor_ev"], "prob": p["mejor_prob"]}]
            con_valor = [c for c in picks if c["ev"] >= 0.05]
            mejor_valor = (max(picks, key=lambda c: c["ev"])
                           if picks else None)
            if con_valor:
                elegido = max(con_valor, key=lambda c: c["prob"])
                color = _color_por_prob_ev(elegido["prob"], elegido["ev"])
                cumple = True
            elif picks:
                elegido = max(picks, key=lambda c: c["ev"])
                color = "rojo"
                cumple = False
            else:
                elegido = None
            if elegido is not None:
                # ALTERNATIVA AMARILLA (Luis 11:33, corregida 11:35 y
                # 11:37): el pick arriesgado que vale la pena por lo que
                # se gana: mayor EV entre los de EV ≥ +5% y 30% ≤ prob <
                # 60%, distinto de la recomendación y con EV ≥ +50%.
                alternativa = None
                amarillos = [c for c in picks
                             if c["ev"] >= 0.05
                             and 30 <= c["prob"] < 60]
                if amarillos:
                    alt = max(amarillos, key=lambda c: c["ev"])
                    if alt["pick"] != elegido["pick"] and alt["ev"] >= 0.50:
                        alternativa = {
                            "pick": alt["pick"],
                            "mercado": alt["mercado"],
                            "momio": alt["momio"],
                            "prob": round(alt["prob"], 1),
                            "ev": alt["ev"],
                        }
                # MEJOR VERDE (E1, 28 nov 2026; ejemplo del jefe:
                # Hamburg/empate): de los picks verdes (prob ≥ 60% y
                # EV ≥ +5%), el de mayor EV. Es la pierna que usa el
                # parlay del día: el combinado quiere el mayor EV
                # entre picks equilibrados, no el EV máximo sin más
                # (que era un rojo como el Local @8.00 del Hamburg).
                verdes = [c for c in picks
                          if _color_por_prob_ev(c["prob"], c["ev"]) == "verde"]
                mejor_verde = (max(verdes, key=lambda c: c["ev"])
                               if verdes else None)
                recomendacion = {
                    "pick": elegido["pick"],
                    "mercado": elegido["mercado"],
                    "momio": elegido["momio"],
                    "prob": round(elegido["prob"], 1),
                    "ev": elegido["ev"],
                    "color": color,
                    "semaforo": color,
                    "cumple_regla": cumple,
                    "alternativa_amarilla": alternativa,
                    "mejor_valor": ({
                        "pick": mejor_valor["pick"],
                        "mercado": mejor_valor["mercado"],
                        "momio": mejor_valor["momio"],
                        "prob": round(mejor_valor["prob"], 1),
                        "ev": mejor_valor["ev"],
                        "color": _color_por_prob_ev(mejor_valor["prob"],
                                                     mejor_valor["ev"]),
                    } if mejor_valor is not None else None),
                    "mejor_verde": ({
                        "pick": mejor_verde["pick"],
                        "mercado": mejor_verde["mercado"],
                        "momio": mejor_verde["momio"],
                        "prob": round(mejor_verde["prob"], 1),
                        "ev": mejor_verde["ev"],
                        "color": "verde",
                    } if mejor_verde is not None else None),
                }
            else:
                recomendacion = None

            acierto = None
            if recomendacion is not None and final:
                acierto = _evaluar_pick(recomendacion["pick"], gl, ga)

            # Columna en vivo: último snapshot del log, si existe.
            snap = log.get(clave)
            vivo_info = {"tiene_datos": False, "motivo": "sin snapshots en data/live-log",
                         "ultimo_snapshot": None, "prediccion": None,
                         "acierto": None}
            if snap is not None:
                minuto = _parse_minuto(snap.get("minuto"))
                tda = snap.get("tda") or [None, None]
                marc = snap.get("marcador") or [None, None]
                probs = _prob_1x2(p["mercados"])
                pred = None
                if minuto is not None and marc[0] is not None and probs:
                    xg = _invertir_xg(probs["p1"], probs["px"], probs["p2"])
                    live = _live_calc(xg, probs, minuto, marc[0], marc[1],
                                      tda[0], tda[1])
                    if live:
                        fav = max(live, key=live.get)
                        pred = {
                            "favorito": {"p1": "Local", "px": "Empate",
                                        "p2": "Visita"}[fav],
                            "p1": round(live["p1"], 1),
                            "px": round(live["px"], 1),
                            "p2": round(live["p2"], 1),
                        }
                vivo_info = {
                    "tiene_datos": True,
                    "motivo": None,
                    "ultimo_snapshot": {
                        "cuando": snap.get("cuando"),
                        "minuto": snap.get("minuto"),
                        "marcador": marc,
                        "tda": tda,
                        "rojas": snap.get("rojas", []),
                    },
                    "prediccion": pred,
                    "acierto": None,
                }
                if pred is not None and final:
                    real = ("Local" if gl > ga else
                            "Visita" if ga > gl else "Empate")
                    vivo_info["acierto"] = pred["favorito"] == real

            partidos.append({
                "config": config,
                "fecha": p.get("fecha"),
                "liga": p.get("liga"),
                "home": home,
                "away": away,
                "estado": estado,
                "marcador": ({"local": gl, "visita": ga}
                             if gl is not None and ga is not None else None),
                "recomendacion": recomendacion,
                "acierto": acierto,
                "acierto_texto": ("Acertó" if acierto is True else
                                  "Falló" if acierto is False else
                                  "Sin recomendación"
                                  if recomendacion is None else
                                  "Pendiente"),
                "vivo": vivo_info,
            })

    def resumen(columna):
        con = [p for p in partidos
               if (p["acierto"] if columna == "pre" else p["vivo"]["acierto"])
               is not None]
        ac = sum(1 for p in con
                 if (p["acierto"] if columna == "pre"
                     else p["vivo"]["acierto"]))
        sin_datos = (0 if columna == "pre" else
                     sum(1 for p in partidos
                         if p["estado"] == "post"
                         and not p["vivo"]["tiene_datos"]))
        return {
            "con_resultado": len(con),
            "aciertos": ac,
            "fallos": len(con) - ac,
            "pct_acierto": (round(ac / len(con) * 100, 1)
                            if con else None),
            "sin_datos": sin_datos,
        }

    salida = {
        "fecha_calculo": datetime.now(MX).strftime("%Y-%m-%d"),
        "generado_en_mx": datetime.now(MX).isoformat(timespec="seconds"),
        "nota": ("Recomendación: el pick con más probabilidad entre los "
                 "de EV ≥ +5% en todos los mercados; color por "
                 "riesgo/ganancia: verde (prob ≥ 60% y EV ≥ +5%), "
                 "amarillo (30% ≤ prob < 60% y EV ≥ +5%, un 50/50) o "
                 "rojo (prob < 30% o EV < +5%: mucho riesgo y mucha "
                 "ganancia, o poco riesgo aparente y poca ganancia). "
                 "Alternativa amarilla: mayor EV entre EV ≥ +5% y 30% ≤ "
                 "prob < 60%, distinto de la recomendación y con EV ≥ "
                 "+50%. La columna en vivo usa el último snapshot del log "
                 "(data/live-log); sin snapshots es 'sin datos', nunca "
                 "inventada. La predicción en vivo invierte el xG de las "
                 "probabilidades publicadas (no las ajustadas por XI)."),
        "partidos": partidos,
        "resumen": {
            "pre_partido": resumen("pre"),
            "en_vivo": resumen("vivo"),
        },
    }
    out_path = os.path.join(ROOT, "data", "resultados.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
    r = salida["resumen"]
    print(f"resultados.json: {len(partidos)} partidos | "
          f"pre-partido {r['pre_partido']['aciertos']}/"
          f"{r['pre_partido']['con_resultado']} "
          f"({r['pre_partido']['pct_acierto']}%) | "
          f"en vivo {r['en_vivo']['aciertos']}/"
          f"{r['en_vivo']['con_resultado']} "
          f"({r['en_vivo']['pct_acierto']}%), "
          f"sin datos: {r['en_vivo']['sin_datos']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
