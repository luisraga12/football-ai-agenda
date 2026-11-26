"""Prototipo Semana 6: alineación probable (orden del jefe, 24 nov 2026).

Para cada partido de la semana, estima el XI más frecuente por
posición de los últimos partidos + la formación más usada, siempre
marcado como PROBABLE: ESPN no publica XI probable, solo el oficial
~1 h antes, así que la estimación es el trabajo.

Ventana (definición del prototipo, a validar por el jefe):
  - Equipos de fin de semana: últimos 5 partidos de su liga doméstica
    antes de la fecha del partido (misma ventana que el Poisson).
  - Equipos entre semana (Champions/Europa): últimos 4 partidos de
    esa competición antes de la fecha del partido (solo había 4
    jornadas antes del corte; misma ventana que el Poisson).
  Pregunta al jefe: ¿para los equipos UEFA la ventana debe ser su
  liga doméstica en vez de la competición UEFA?

Fuentes (API pública de ESPN, sin clave):
  - Schedule del equipo: .../soccer/{liga}/teams/{id}/schedule
    (eventos con state=post, fecha < fecha del partido).
  - Summary por evento: .../soccer/{liga}/summary?event={id}
    (rosters con titulares + posición; keyEvents Substitution para
    estimar minutos). Respaldo: site.web.api.espn.com si site.api
    falla. Si un equipo no tiene datos, queda "pendiente", no se
    inventa nada.

Formación: la (defensas, medios, delanteros) más frecuente en la
ventana; desempate: la del partido más reciente. El XI probable toma,
por grupo de posición, a los jugadores con más titularidades en la
ventana (desempate: más minutos estimados, luego titularidad más
reciente). Sin duplicados.

Nombres: ESPN lista en los XI a jugadores de otros clubes (ver
scripts/corregir_nombres_xi.py). Se aplica el mismo MAPEO conocido
(Arsenal / Real Madrid) y cualquier titular del XI probable que NO
esté en la plantilla de temporada del equipo queda en "revisiones"
para que el jefe lo confirme; no se inventa un reemplazo.

Verificación de nombres (24 nov 2026, corrección (a) del jefe):
los ~50 nombres señalados por el jefe fueron verificados uno por uno
contra los fichajes del verano 2026 y contra los datos: los 60 son
jugadores reales del equipo al que ESPN los asigna (fichajes 2026),
así que NO se añadió ningún reemplazo al MAPEO — se mantiene solo
el MAPEO aprobado de Arsenal / Real Madrid (corrección Fuerza del
XI, cerrada). El detalle con fuentes está en EMPLEADO-1.md.

Fuerza (corrección (b) del jefe, misma fórmula aprobada de Fuerza
del XI): cada XI probable trae "fuerza" con valor 0-100 y los 3
componentes con fracciones (goles+asistencias / minutos / puntos),
pesos 0.40/0.30/0.30, cada componente topado en 100. Cada componente
se mide contra el mejor XI posible EN ESE componente con la MISMA
formación del XI probable (corrección 25 nov 2026: antes los 3 se
medían contra un solo mejor XI 1-4-4-2 por minutos y el XI probable
podía superarlo en bruto — 88 casos en la Semana 2, p. ej. Atlas 65
puntos vs mejor 63). El denominador es así el máximo alcanzable y
cada componente es un % verdadero ≤ 100. Se calcula con los nombres
ESPN ANTES del MAPEO (las estadísticas pertenecen al hueco del XI).
Puntos: 3/1/0 del partido para todo jugador que jugó (titular o
suplente con minutos > 0); en la investigación original solo se
contaban los titulares, pero aquí XI probable y mejor XI usan la
misma tabla, así que las fracciones son comparables y la definición
del PLAN ("puntos con esos jugadores en cancha") se cumple mejor.

Uso:
    python3 scripts/calcular_alineacion_probable.py \
        --config scripts/config/semana-2.json \
        --out data/semana-2/alineacion-probable.json
    python3 scripts/calcular_alineacion_probable.py \
        --config scripts/config/semana-2-entresemana.json \
        --out data/semana-2-entresemana/alineacion-probable.json
Los summaries se guardan en data/<semana>/raw/summary_*.json (raw/
no se sube al repo, regla del jefe). fecha_calculo en hora de México.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo

BASES = [
    "https://site.api.espn.com/apis/site/v2/sports/soccer",
    "https://site.web.api.espn.com/apis/site/v2/sports/soccer",
]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MX = ZoneInfo("America/Mexico_City")

# Ventana por tipo de competición (misma que el Poisson).
VENTANA = {"liga": 5, "uefa": 4}

# Mapeo conocido de nombres de otros clubes (ver
# scripts/corregir_nombres_xi.py). Solo Arsenal / Real Madrid.
MAPEO = {
    "Arsenal": {
        "Ezri Konsa": "William Saliba",
        "Bruno Guimarães": "Martín Zubimendi",
        "Christos Tzolis": "Gabriel Martinelli",
    },
    "Real Madrid": {
        "Ibrahima Konaté": "Antonio Rüdiger",
        "Bernardo Silva": "Brahim Díaz",
        "Yan Diomande": "Vinícius Júnior",
        "Marc Cucurella": "Éder Militão",
    },
}


def fetch_json(url):
    """GET con respaldo de dos hosts ESPN; None si ambos fallan."""
    last_err = None
    for base in BASES:
        u = url.replace(BASES[0], base) if url.startswith(BASES[0]) else url
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001 - reintento con el otro host
            last_err = e
    print(f"  AVISO: no se pudo bajar {url} ({last_err})", file=sys.stderr)
    return None


def parse_substitutions(summary):
    """{nombre: minuto_entrada} y {nombre: minuto_salida}."""
    entra, sale = {}, {}
    for k in summary.get("keyEvents", []):
        if k.get("type", {}).get("text") != "Substitution":
            continue
        clock = k.get("clock", {}).get("displayValue", "")
        m = re.search(r"(\d+)", clock or "")
        if not m:
            continue
        minuto = int(m.group(1))
        text = k.get("text", "")
        mm = re.search(r"\.\s*(.+?)\s+replaces\s+(.+?)\.", text)
        if mm:
            entra[mm.group(1).strip()] = minuto
            sale[mm.group(2).strip()] = minuto
    return entra, sale


def minutes_for_player(starter, name, entra, sale):
    if starter:
        return sale.get(name, 90)
    return 90 - entra[name] if name in entra else 0


def norm_pos(summary_pos, roster_pos):
    """Normaliza la posición a G/D/M/F (misma lógica que
    investigar_fuerza_xi.py)."""
    name = (summary_pos or {}).get("name", "")
    abbr = (summary_pos or {}).get("abbreviation", "") or roster_pos or ""
    if "Goalkeeper" in name or abbr == "G":
        return "G"
    if "Defender" in name or abbr.startswith(("D", "CD", "LB", "RB", "WB")):
        return "D"
    if "Midfielder" in name or abbr.startswith(("M", "CM", "DM", "AM", "LM", "RM")):
        return "M"
    if ("Forward" in name or "Striker" in name or "Winger" in name
            or abbr.startswith(("F", "ST", "CF", "LW", "RW"))):
        return "F"
    return roster_pos if roster_pos in ("G", "D", "M", "F") else "?"


def ventana_partidos(liga, tid, fecha_partido, n):
    """Últimos n partidos con state=post antes de fecha_partido.

    Devuelve [(event_id, fecha, rival, local_o_visita)] o None si el
    schedule no se pudo bajar.
    """
    sched = fetch_json(f"{BASES[0]}/{liga}/teams/{tid}/schedule")
    if not sched:
        return None
    out = []
    for e in sched.get("events", []):
        comp = (e.get("competitions") or [{}])[0]
        if comp.get("status", {}).get("type", {}).get("state") != "post":
            continue
        fecha = (e.get("date") or "")[:10]
        if fecha >= fecha_partido:
            continue
        rivales = [c["team"]["displayName"]
                   for c in comp.get("competitors", [])]
        out.append({"event_id": e.get("id"), "fecha": fecha,
                    "rivales": rivales})
    out.sort(key=lambda m: m["fecha"], reverse=True)
    return out[:n]


def team_result_by_id(summary, tid):
    """(goles_favor, goles_contra, puntos 3/1/0) del equipo por id."""
    comp = summary["header"]["competitions"][0]
    me = next(c for c in comp["competitors"]
              if str(c["team"].get("id")) == str(tid))
    other = next(c for c in comp["competitors"]
                 if str(c["team"].get("id")) != str(tid))
    gf = int(float(me["score"]))
    ga = int(float(other["score"]))
    return gf, ga, 3 if gf > ga else (1 if gf == ga else 0)


def xi_del_partido(summary, equipo, tid=None):
    """XI titular del equipo en un summary + stats de los que jugaron.

    Devuelve (xi, jugados): xi = [{jugador, pos, minutos}] (11
    titulares); jugados = [{jugador, pos, minutos, goles, asist,
    puntos}] para todo el que jugó (titular o suplente con minutos
    > 0). goles/asist salen de x['stats'] del summary (totalGoals /
    goalAssists); puntos 3/1/0 del resultado del partido.
    """
    ros = None
    for r in summary.get("rosters", []):
        if tid is not None and str(r["team"].get("id")) == str(tid):
            ros = r
            break
    if ros is None:
        ros = next((r for r in summary.get("rosters", [])
                    if r["team"]["displayName"] == equipo), None)
    if not ros:
        return None, None
    entra, sale = parse_substitutions(summary)
    try:
        _gf, _ga, pts = team_result_by_id(summary, tid)
    except (KeyError, StopIteration, ValueError):
        pts = 0
    xi, jugados = [], []
    for x in ros["roster"]:
        name = x["athlete"]["displayName"]
        starter = bool(x.get("starter"))
        mins = minutes_for_player(starter, name, entra, sale)
        if starter:
            pos = norm_pos(x.get("position"), None)
            xi.append({"jugador": name, "pos": pos, "minutos": mins})
        if mins <= 0:
            continue
        mstats = {s["name"]: s.get("value", 0)
                  for s in x.get("stats", [])}
        jugados.append({
            "jugador": name,
            "pos": norm_pos(x.get("position"), None),
            "minutos": mins,
            "goles": mstats.get("totalGoals", 0),
            "asist": mstats.get("goalAssists", 0),
            "puntos": pts,
        })
    return xi, jugados


def mejor_xi_por_componente(per_player, grupos, clave):
    """Mejor XI posible con la formación dada (grupos {"G","D","M","F"})
    maximizando el componente que da `clave` (función jugador->valor).

    Toma por grupo a los de mayor valor en ese componente; si un grupo
    no tiene suficientes candidatos, completa con los de mayor valor
    sin importar el grupo (misma regla de respaldo que la
    investigación Fuerza del XI aprobada).
    """
    mejor = []
    for g, n in grupos.items():
        cands = sorted(
            ((nm, d) for nm, d in per_player.items() if d["pos"] == g),
            key=lambda kv: clave(kv[1]), reverse=True)[:n]
        mejor += [nm for nm, _d in cands]
    if len(mejor) < 11:
        resto = sorted(
            ((nm, d) for nm, d in per_player.items() if nm not in mejor),
            key=lambda kv: clave(kv[1]), reverse=True)
        mejor += [nm for nm, _d in resto[:11 - len(mejor)]]
    return mejor[:11]


def calcular_fuerza(nombres_probable, per_player):
    """Fuerza del XI probable vs mejor XI (fórmula aprobada 0.40/0.30/
    0.30, componentes topados en 100). Devuelve el dict 'fuerza' con
    valor + 3 componentes + valores brutos y totales del mejor XI
    para mostrar las fracciones (p. ej. 3965/3838).

    Corrección 25 nov 2026 (denominador Atlas 65/63): antes los 3
    componentes se medían contra UN solo mejor XI 1-4-4-2 elegido por
    minutos, y el XI probable (elegido por titularidades, con su
    propia formación) podía superarlo en bruto en cualquier
    componente — 88 casos en la Semana 2 (Atlas 65 puntos vs mejor
    63). Ahora cada componente se mide contra el mejor XI posible
    en ESE componente con la MISMA formación del XI probable: el
    denominador es el máximo alcanzable, así que cada componente es
    un % verdadero ≤ 100 (el tope en 100 queda como red de
    seguridad). El XI probable siempre es candidato de su propia
    formación, así que el denominador nunca es menor que su valor.
    """
    def componentes(nombres):
        ga = sum(per_player.get(n, {}).get("goles", 0)
                 + per_player.get(n, {}).get("asist", 0)
                 for n in nombres)
        mins = sum(per_player.get(n, {}).get("minutos", 0)
                   for n in nombres)
        pts = sum(per_player.get(n, {}).get("puntos", 0)
                  for n in nombres)
        return ga, mins, pts

    # Formación del XI probable (conteo por grupo de sus posiciones).
    grupos = {"G": 0, "D": 0, "M": 0, "F": 0}
    for n in nombres_probable:
        pos = per_player.get(n, {}).get("pos")
        if pos in grupos:
            grupos[pos] += 1
    b_ga = componentes(mejor_xi_por_componente(
        per_player, grupos,
        lambda d: d.get("goles", 0) + d.get("asist", 0)))[0]
    b_min = componentes(mejor_xi_por_componente(
        per_player, grupos, lambda d: d.get("minutos", 0)))[1]
    b_pts = componentes(mejor_xi_por_componente(
        per_player, grupos, lambda d: d.get("puntos", 0)))[2]
    ga, mins, pts = componentes(nombres_probable)
    A = min(100, 100 * ga / b_ga) if b_ga else 0
    B = min(100, 100 * mins / b_min) if b_min else 0
    C = min(100, 100 * pts / b_pts) if b_pts else 0
    return {
        "valor": round(0.40 * A + 0.30 * B + 0.30 * C, 1),
        "A_goles": round(A, 1),
        "B_minutos": round(B, 1),
        "C_puntos": round(C, 1),
        "goles_asist": ga, "minutos": mins, "puntos": pts,
        "mejor": {"goles_asist": b_ga, "minutos": b_min,
                  "puntos": b_pts},
    }


def calcular_xi_probable(ventana_xis):
    """ventana_xis: [xi (lista de 11) por partido, más reciente primero].

    Devuelve (formacion "D-M-F", jugadores [11], detalle_por_jugador).
    """
    # Formación más frecuente en la ventana.
    formas = Counter()
    for xi in ventana_xis:
        c = Counter(x["pos"] for x in xi)
        formas[(c.get("D", 0), c.get("M", 0), c.get("F", 0))] += 1
    # Desempate: la del partido más reciente.
    forma_reciente = None
    if ventana_xis:
        c = Counter(x["pos"] for x in ventana_xis[0])
        forma_reciente = (c.get("D", 0), c.get("M", 0), c.get("F", 0))
    forma = formas.most_common(1)[0][0] if formas else forma_reciente
    if formas and forma_reciente and formas[forma] == formas[forma_reciente]:
        forma = forma_reciente
    d_n, m_n, f_n = forma or (4, 4, 2)
    formacion = f"{d_n}-{m_n}-{f_n}"

    # Agregado por jugador: titularidades, minutos, última fecha, pos.
    jug = {}
    for i, xi in enumerate(ventana_xis):
        for x in xi:
            dd = jug.setdefault(x["jugador"], {
                "posiciones": Counter(), "titularidades": 0,
                "minutos": 0, "ultima": i})
            dd["posiciones"][x["pos"]] += 1
            dd["titularidades"] += 1
            dd["minutos"] += x["minutos"]
            dd["ultima"] = min(dd["ultima"], i)
    for dd in jug.values():
        dd["pos"] = dd["posiciones"].most_common(1)[0][0]

    def clave(nm):
        dd = jug[nm]
        return (-dd["titularidades"], -dd["minutos"], dd["ultima"])

    elegidos = []
    for grupo, n in (("G", 1), ("D", d_n), ("M", m_n), ("F", f_n)):
        cands = sorted((nm for nm, dd in jug.items() if dd["pos"] == grupo),
                       key=clave)
        elegidos += cands[:n]
    if len(elegidos) < 11:
        resto = sorted((nm for nm in jug if nm not in elegidos), key=clave)
        elegidos += resto[:11 - len(elegidos)]
    jugadores = [{"jugador": nm, "pos": jug[nm]["pos"],
                  "titularidades": jug[nm]["titularidades"],
                  "minutos": jug[nm]["minutos"]}
                 for nm in elegidos[:11]]
    return formacion, jugadores, jug


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    cfg = json.load(open(args.config))
    out_dir = os.path.dirname(args.out)
    raw_dir = os.path.join(out_dir, "raw")
    os.makedirs(raw_dir, exist_ok=True)
    fecha_calculo = datetime.now(MX).strftime("%Y-%m-%d")

    partidos_out = []
    equipos_vistos = {}
    for p in cfg["partidos"]:
        liga = p["liga"]
        n = VENTANA["uefa"] if liga.startswith("uefa.") else VENTANA["liga"]
        lado = {}
        for rol, nombre, tid in (("local", p["home"], p["home_id"]),
                                 ("visita", p["away"], p["away_id"])):
            clave_eq = (liga, tid)
            if clave_eq in equipos_vistos:
                lado[rol] = equipos_vistos[clave_eq]
                continue
            print(f"== {nombre} ({liga}) — ventana últimos {n} antes de "
                  f"{p['fecha']}")
            ventana = ventana_partidos(liga, tid, p["fecha"], n)
            if ventana is None:
                lado[rol] = {"equipo": nombre, "liga": liga,
                             "pendiente": "no se pudo bajar el schedule de ESPN",
                             "probable": None}
                equipos_vistos[clave_eq] = lado[rol]
                continue
            if not ventana:
                lado[rol] = {"equipo": nombre, "liga": liga,
                             "pendiente": "sin partidos previos en la ventana",
                             "probable": None}
                equipos_vistos[clave_eq] = lado[rol]
                continue
            xis, ventana_out, fallos = [], [], []
            per_player = {}
            for m in ventana:
                path = os.path.join(raw_dir, f"summary_{liga}_{m['event_id']}.json")
                if os.path.exists(path):
                    s = json.load(open(path))
                else:
                    s = fetch_json(f"{BASES[0]}/{liga}/summary?event={m['event_id']}")
                    if s:
                        json.dump(s, open(path, "w"))
                    time.sleep(0.2)
                if not s:
                    fallos.append(m["event_id"])
                    continue
                xi, jugados = xi_del_partido(s, nombre, tid)
                if xi is None or len(xi) != 11:
                    fallos.append(m["event_id"])
                    continue
                xis.append(xi)
                ventana_out.append({
                    "fecha": m["fecha"], "event_id": m["event_id"],
                    "rivales": m["rivales"],
                    "formacion": (lambda c: f"{c.get('D',0)}-{c.get('M',0)}-{c.get('F',0)}")(
                        Counter(x["pos"] for x in xi)),
                })
                for jg in jugados or []:
                    dd = per_player.setdefault(jg["jugador"], {
                        "posiciones": Counter(), "titularidades": 0,
                        "minutos": 0, "puntos": 0, "goles": 0,
                        "asist": 0})
                    dd["posiciones"][jg["pos"]] += 1
                    dd["minutos"] += jg["minutos"]
                    dd["puntos"] += jg["puntos"]
                    dd["goles"] += jg["goles"]
                    dd["asist"] += jg["asist"]
                for x in xi:
                    per_player[x["jugador"]]["titularidades"] += 1
            for dd in per_player.values():
                dd["pos"] = dd["posiciones"].most_common(1)[0][0]
            if len(xis) < 3:
                lado[rol] = {"equipo": nombre, "liga": liga,
                             "ventana": ventana_out,
                             "pendiente": f"solo {len(xis)} XI en la ventana "
                                          f"(mínimo 3); fallos: {fallos}",
                             "probable": None}
                equipos_vistos[clave_eq] = lado[rol]
                continue
            formacion, jugadores, _jug = calcular_xi_probable(xis)
            # Fuerza con los nombres ESPN, ANTES del MAPEO (las
            # estadísticas pertenecen al hueco del XI).
            fuerza = calcular_fuerza(
                [j["jugador"] for j in jugadores], per_player)
            # Corrección de nombres conocidos + revisión contra plantilla.
            mapa = MAPEO.get(nombre, {})
            roster = fetch_json(f"{BASES[0]}/{liga}/teams/{tid}/roster")
            plantilla = ({a["displayName"] for a in roster["athletes"]}
                         if roster else set())
            revisiones = []
            for j in jugadores:
                espn = j["jugador"]
                j["jugador"] = mapa.get(espn, espn)
                if espn in mapa:
                    j["corregido_de"] = espn
                if plantilla and espn not in plantilla and espn not in mapa:
                    revisiones.append(
                        f"{espn} ({j['pos']}): ESPN lo pone en el XI pero "
                        "no está en la plantilla de temporada del equipo; "
                        "nombre por confirmar, no se inventa reemplazo.")
            lado[rol] = {"equipo": nombre, "liga": liga,
                         "ventana_partidos": len(xis),
                         "ventana": ventana_out,
                         "formacion": formacion,
                         "jugadores": jugadores,
                         "fuerza": fuerza,
                         "revisiones": revisiones,
                         "fallos_summary": fallos,
                         "probable": True}
            equipos_vistos[clave_eq] = lado[rol]
            print(f"   {nombre}: formación {formacion}, "
                  f"{len(jugadores)} jugadores, fuerza "
                  f"{fuerza['valor']}, revisiones {len(revisiones)}")
        partidos_out.append({
            "fecha": p["fecha"], "liga": liga,
            "local": p["home"], "visita": p["away"],
            "local_xi": lado["local"], "visita_xi": lado["visita"],
        })

    resultado = {
        "semana": cfg.get("nombre"),
        "config": os.path.basename(args.config),
        "fecha_calculo": fecha_calculo,
        "metodo": ("XI más frecuente por posición de los últimos partidos "
                   "+ formación más usada; siempre PROBABLE (ESPN no "
                   "publica XI probable). Ventana: últimos 5 de liga "
                   "doméstica (fin de semana) o últimos 4 de la "
                   "competición UEFA (entre semana), antes de la fecha "
                   "del partido. Fuerza por XI: 0.40·goles+asistencias + "
                   "0.30·minutos + 0.30·puntos, cada componente en % vs "
                   "el mejor XI posible en ese componente con la misma "
                   "formación del XI probable (corrección 25 nov 2026: "
                   "antes era un solo mejor XI 1-4-4-2 por minutos y el "
                   "XI podía superarlo, p. ej. Atlas 65/63), "
                   "con fracciones; calculada con nombres ESPN antes del "
                   "MAPEO."),
        "verificacion_nombres": ("Los ~50 nombres señalados por el jefe "
                   "el 24 nov 2026 fueron verificados uno por uno: los 60 "
                   "son jugadores reales del equipo asignado (fichajes "
                   "del verano 2026, con fuentes en EMPLEADO-1.md). No "
                   "se añadió ningún reemplazo al MAPEO."),
        "partidos": partidos_out,
    }
    json.dump(resultado, open(args.out, "w"), indent=1, ensure_ascii=False)
    n_ok = sum(1 for pt in partidos_out
               for x in (pt["local_xi"], pt["visita_xi"]) if x.get("probable"))
    n_tot = len(partidos_out) * 2
    print(f"OK -> {args.out} ({n_ok}/{n_tot} XI probables, "
          f"{len(partidos_out)} partidos)")


if __name__ == "__main__":
    main()
