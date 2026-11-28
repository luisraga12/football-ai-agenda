"""Fuerza del XI oficial por partido (Empleado 1, 27 nov 2026).

Lee data/mapas.json (XI oficial publicado por ESPN + alineacion_publicada)
y los dos alineacion-probable.json (F_prob + ventana por equipo), y
publica data/fuerza_xi.json con F_of/F_prob por partido.

Por partido y lado:
  - F_of: Fuerza del XI OFICIAL (los 11 nombres oficiales casados con
    per_player por normalizacion: minusculas, sin acentos), con la
    misma formula aprobada (0.40*Goles + 0.30*Minutos + 0.30*Puntos,
    componentes vs el mejor XI de la misma ventana).
  - F_of_efectiva: F_of topada a F_prob +/- 12 puntos (tope obligatorio
    T1: sin tope el sesgo de medicion ~17 pts infla el EV y empeora el
    Brier; con tope mejora a 0.8066 con k=1.0, n=35, indicio).
  - r = F_of_efectiva / F_prob (k=1.0 piloto): el JS aplica r^k para
    el recalculado del EV en el detalle. NUNCA se publica el ratio
    crudo F_of/F_prob.

per_player (goles/minutos/puntos por jugador) se reconstruye SOLO del
cache data/semana-<N>/raw y data/semana-<N>-entresemana/raw ya
commiteado (los summaries que uso calcular_alineacion_probable.py):
cero llamadas nuevas a ESPN.

Fail-soft por lado, nunca inventado: sin alineacion oficial, sin
F_prob, XI incompleto, sin ventana en cache, o <8/11 casados ->
f_of/f_of_efectiva/r en null + motivo.

Auditoria: replica la F_prob con los nombres pre-MAPEO y avisa si
difiere >0.15 de la guardada (se publica siempre la guardada).

Uso: python3 scripts/calcular_fuerza_oficial.py [--mapas ...]
       [--salida ...]. Se corre DESPUES de generar_mapas.py.
"""

import argparse
import glob
import json
import os
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone

# Modulo hermano (scripts/): los scripts siempre se corren como
# `python3 scripts/*.py` desde la raiz del repo, asi que resuelve.
import calcular_alineacion_probable as cap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPE_PUNTOS = 12
K_PILOTO = 1.0
MIN_CASADOS = 8
MIN_SUMMARIES = 3
UMBRAL_AUDITORIA = 0.15

# Letras que NFD no descompone y que rompen el casado de nombres.
_EXTRA = str.maketrans({
    "ı": "i", "ł": "l", "đ": "d", "ø": "o", "ß": "ss",
    "æ": "ae", "œ": "oe", "þ": "th", "ð": "d",
})


def norm_nombre(s):
    """Clave canonica de un nombre: minusculas, sin acentos ni
    puntuacion ni espacios (para casar el XI oficial con per_player)."""
    if not s:
        return ""
    t = unicodedata.normalize("NFD", str(s))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.lower().translate(_EXTRA)
    return "".join(c for c in t if c.isalnum())


def norm_clave(fecha, liga, local, visita):
    return (str(fecha), str(liga), norm_nombre(local), norm_nombre(visita))


def construir_per_player(raw_dirs, liga, ventana, equipo, tid):
    """Reconstruye per_player de un equipo desde el cache raw/.

    ventana: [{event_id, ...}] del alineacion-probable.json.
    Devuelve (per_player, n_summaries, fallos). Cero llamadas a ESPN.
    """
    # Indice nombre de archivo -> ruta (se construye una vez por
    # llamada; los raw/ son pequenos).
    archivos = {}
    for d in raw_dirs:
        for path in glob.glob(os.path.join(d, "summary_*.json")):
            archivos.setdefault(os.path.basename(path), path)
    per_player = {}
    n_summaries = 0
    fallos = []
    for m in ventana or []:
        event_id = str(m.get("event_id", ""))
        path = archivos.get(f"summary_{liga}_{event_id}.json")
        if not path:
            fallos.append(event_id)
            continue
        try:
            with open(path, encoding="utf-8") as f:
                s = json.load(f)
        except (OSError, ValueError):
            fallos.append(event_id)
            continue
        xi, jugados = cap.xi_del_partido(s, equipo, tid)
        if xi is None or len(xi) != 11:
            fallos.append(event_id)
            continue
        n_summaries += 1
        for jg in jugados or []:
            dd = per_player.setdefault(jg["jugador"], {
                "posiciones": Counter(), "titularidades": 0,
                "minutos": 0, "puntos": 0, "goles": 0, "asist": 0})
            dd["posiciones"][jg["pos"]] += 1
            dd["minutos"] += jg["minutos"]
            dd["puntos"] += jg["puntos"]
            dd["goles"] += jg["goles"]
            dd["asist"] += jg["asist"]
        for x in xi:
            per_player[x["jugador"]]["titularidades"] += 1
    for dd in per_player.values():
        dd["pos"] = dd["posiciones"].most_common(1)[0][0]
    return per_player, n_summaries, fallos


def casar_oficial(nombres_oficiales, per_player):
    """Casa los 11 nombres oficiales con per_player por normalizacion.

    Devuelve (casados, sin_casar): casados son las claves canonicas de
    per_player (las que entiende calcular_fuerza); sin_casar son los
    nombres oficiales sin pareja. Si dos claves de per_player
    normalizan igual (mismo jugador con dos grafias), se queda la de
    mas minutos.
    """
    indice = {}
    for nombre, dd in per_player.items():
        clave = norm_nombre(nombre)
        if not clave:
            continue
        actual = indice.get(clave)
        if actual is None or dd.get("minutos", 0) > per_player[actual].get("minutos", 0):
            indice[clave] = nombre
    casados, sin_casar = [], []
    for nombre in nombres_oficiales:
        canon = indice.get(norm_nombre(nombre))
        if canon is None:
            sin_casar.append(nombre)
        else:
            casados.append(canon)
    return casados, sin_casar


def lado_nulo(f_prob, motivo):
    return {"f_prob": f_prob, "f_of": None, "f_of_efectiva": None,
            "r": None, "casados": 0, "sin_casar": [],
            "tope_aplicado": False, "motivo": motivo,
            "f_of_detalle": None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mapas", default="data/mapas.json")
    ap.add_argument("--salida", default="data/fuerza_xi.json")
    args = ap.parse_args()

    mapas = json.load(open(os.path.join(ROOT, args.mapas), encoding="utf-8"))
    # mapas.json guarda la semana de la ULTIMA regeneracion, que puede
    # ser la de entre semana ("2-entresemana"); los archivos de la
    # semana cuelgan del numero base ("2").
    semana = str(mapas.get("semana", "2")).split("-")[0]
    partidos_vivo = mapas.get("partidos_vivo") or {}
    detalle = mapas.get("detalle") or {}

    # Alineacion probable: los dos archivos (fin de semana + entre semana).
    prob_por_partido = {}
    for ruta in (f"data/semana-{semana}/alineacion-probable.json",
                 f"data/semana-{semana}-entresemana/alineacion-probable.json"):
        path = os.path.join(ROOT, ruta)
        if not os.path.isfile(path):
            print(f"AVISO: no existe {ruta}")
            continue
        doc = json.load(open(path, encoding="utf-8"))
        for p in doc.get("partidos") or []:
            clave = norm_clave(p.get("fecha"), p.get("liga"),
                               p.get("local"), p.get("visita"))
            prob_por_partido[clave] = p

    raw_dirs = [os.path.join(ROOT, f"data/semana-{semana}/raw"),
                os.path.join(ROOT, f"data/semana-{semana}-entresemana/raw")]
    cache_per_player = {}

    def per_player_de(liga, tid, xi_ap, equipo):
        """per_player del equipo (cache por liga+tid) o (None, motivo)."""
        clave_cache = (liga, str(tid))
        if clave_cache in cache_per_player:
            return cache_per_player[clave_cache]
        ventana = (xi_ap or {}).get("ventana") or []
        if not ventana:
            res = (None, "sin ventana en cache")
            cache_per_player[clave_cache] = res
            return res
        pp, n_sum, fallos = construir_per_player(
            raw_dirs, liga, ventana, equipo, tid)
        if n_sum < MIN_SUMMARIES:
            res = (None, f"ventana incompleta en cache "
                         f"({n_sum} summaries, minimo {MIN_SUMMARIES})")
            cache_per_player[clave_cache] = res
            return res
        if fallos:
            print(f"  AVISO {equipo} ({liga}): {len(fallos)} summaries "
                  f"de la ventana no estan en cache: {fallos}")
        res = (pp, None)
        cache_per_player[clave_cache] = res
        return res

    partidos_out = {}
    n_of = 0
    n_topados = 0
    avisos_auditoria = 0
    for slug in sorted(partidos_vivo):
        pv = partidos_vivo[slug]
        liga = pv.get("liga")
        fecha = pv.get("fecha")
        home = pv.get("home")
        away = pv.get("away")
        det = detalle.get(slug) or {}
        lineup = det.get("lineup") or {}
        publicada = bool(lineup.get("alineacion_publicada"))
        jugadores_of = (lineup.get("jugadores") or {})

        ap = prob_por_partido.get(norm_clave(fecha, liga, home, away))
        entrada = {"liga": liga, "fecha": fecha, "home": home,
                   "away": away, "alineacion_publicada": publicada}
        for rol, xi_clave, tid, nombre in (
                ("local", "local_xi", pv.get("home_id"), home),
                ("visita", "visita_xi", pv.get("away_id"), away)):
            xi_ap = (ap or {}).get(xi_clave) if ap else None
            f_prob = None
            if xi_ap and xi_ap.get("probable"):
                fuerza = xi_ap.get("fuerza") or {}
                if isinstance(fuerza.get("valor"), (int, float)):
                    f_prob = float(fuerza["valor"])
            if f_prob is None:
                entrada[rol] = lado_nulo(None, "sin Fuerza probable publicada")
                continue
            pp, motivo_pp = per_player_de(liga, tid, xi_ap, nombre)
            if pp is None:
                entrada[rol] = lado_nulo(f_prob, motivo_pp)
                continue
            # Auditoria: replicar la F_prob con los nombres pre-MAPEO.
            pre_nombres = [(j.get("corregido_de") or j.get("jugador"))
                           for j in (xi_ap.get("jugadores") or [])]
            replica = cap.calcular_fuerza(pre_nombres, pp)["valor"]
            if abs(replica - f_prob) > UMBRAL_AUDITORIA:
                avisos_auditoria += 1
                print(f"  AVISO auditoria {nombre} ({slug}): F_prob "
                      f"replicada {replica} vs guardada {f_prob}")
            if not publicada:
                entrada[rol] = lado_nulo(f_prob, "sin alineación oficial publicada")
                continue
            oficiales = [(j.get("jugador") or "")
                         for j in (jugadores_of.get(rol) or [])]
            if len(oficiales) != 11:
                entrada[rol] = lado_nulo(
                    f_prob, "alineación oficial incompleta "
                            f"({len(oficiales)}/11 jugadores)")
                continue
            casados, sin_casar = casar_oficial(oficiales, pp)
            if len(casados) < MIN_CASADOS:
                entrada[rol] = lado_nulo(
                    f_prob, f"solo {len(casados)}/11 jugadores casados "
                           "con la ventana")
                continue
            detalle_f = cap.calcular_fuerza(casados, pp)
            f_of = float(detalle_f["valor"])
            f_ef = min(max(f_of, f_prob - TOPE_PUNTOS),
                       f_prob + TOPE_PUNTOS)
            f_ef = round(f_ef, 1)
            r = round(f_ef / f_prob, 3) if f_prob > 0 else None
            entrada[rol] = {
                "f_prob": f_prob, "f_of": f_of,
                "f_of_efectiva": f_ef, "r": r,
                "casados": len(casados), "sin_casar": sin_casar,
                "tope_aplicado": f_ef != f_of, "motivo": None,
                "f_of_detalle": detalle_f,
            }
            n_of += 1
            if f_ef != f_of:
                n_topados += 1
        partidos_out[slug] = entrada

    salida = {
        "version": 1,
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "semana": semana,
        "k": K_PILOTO,
        "tope_puntos": TOPE_PUNTOS,
        "partidos": partidos_out,
    }
    os.makedirs(os.path.dirname(os.path.join(ROOT, args.salida)) or ".",
                exist_ok=True)
    with open(os.path.join(ROOT, args.salida), "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"OK -> {args.salida} ({len(partidos_out)} partidos, "
          f"{n_of} lados con F_of, {n_topados} con tope aplicado, "
          f"{avisos_auditoria} avisos de auditoria)")


if __name__ == "__main__":
    main()
