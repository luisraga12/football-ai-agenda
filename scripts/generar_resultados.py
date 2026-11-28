#!/usr/bin/env python3
"""Genera data/resultados.json: recomendación pre-partido + acertó/falló
y Marcador (pre-partido vs en vivo) para las nuevas funcionalidades
(orden Luis 28 nov 00:19, JEFE.md f51ccc0 + caee893).

Lee los dos ev.json (semana-2 y entresemana) + vivo.json + el log en vivo
(data/live-log/*.jsonl, si existe). NO inventa nada:
- Sin momios o sin EV positivo no hay recomendación ("Sin recomendación").
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
    m = re.match(r"^Spread\s+(local|visita)\s+([+-]?\d+[.,]\d+)$", pick or "")
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

            pick = p.get("mejor_pick")
            ev_pick = p.get("mejor_ev")
            # Recomendación solo si el pick tiene valor (EV > 0).
            if pick and ev_pick is not None and ev_pick > 0:
                recomendacion = {
                    "pick": pick,
                    "momio": p.get("mejor_decimal"),
                    "prob": p.get("mejor_prob"),
                    "ev": ev_pick,
                    "semaforo": p.get("semaforo"),
                }
            else:
                recomendacion = None

            acierto = None
            if recomendacion is not None and final:
                acierto = _evaluar_pick(pick, gl, ga)

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
        "nota": ("La columna en vivo usa el último snapshot del log "
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
