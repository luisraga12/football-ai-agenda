"""Genera data/mapas.json: PARTIDOS_VIVO + DETAIL desde los datos
(Football AI Agenda).

Antes, los dos mapas vivian escritos a mano dentro de index.html
(PARTIDOS_VIVO, 28 entradas) y partido.html (DETAIL, 28 claves):
se hicieron el 23-24 nov 2026 y nada los regeneraba cuando
descubrir_partidos.py (paso 0 de run_semana.py) agregaba partidos
nuevos. Resultado: la cobertura en vivo y el detalle se congelaron
en 28 de 55 partidos (faltaban los 8 de Liguilla, 4 de Champions
del 25 nov y 15 de Europa League del 26 nov).

Este script genera los dos mapas desde los datos del repo, en cada
corrida del pipeline (paso 10 de run_semana.py), para que sigan
solos a los partidos descubiertos:
  - partidos_vivo: {slug: {liga, fecha, home_id, away_id, home,
    away}} — la misma forma del PARTIDOS_VIVO embebido. Sale del
    config de la semana (fin de semana + entre semana).
  - detalle: {slug: {home, away, league, day, time, espn_event_id,
    lastFive, h2h, standings, lineup, sources}} — la misma forma
    del DETAIL embebido. Identidad y espn_event_id salen de ev.json
    y verified_events.json; lastFive sale de raw/teams_last5.json
    (los mismos 5 que usa el modelo) con la competicion resuelta
    desde los schedule_*.json del raw.

Reglas (nada inventado, orden del jefe):
  1. Lo que no tiene fuente en el repo queda en null y la pagina lo
     muestra como pendiente: h2h y standings no tienen fuente en el
     repo (el endpoint de posiciones de ESPN no responde), asi que
     van en null en las entradas nuevas.
  2. Las 28 entradas que ya existen embebidas en partido.html se
     PRESERVAN tal cual (con su h2h, sus standings y sus ultimos 5
     con copas, que el generador no puede reproducir desde
     teams_last5, que es solo de liga) y se marcan con
     fuente_detalle 'embebido'. Las nuevas llevan 'generado'. Asi
     el cambio no quita nada de lo que la pagina ya muestra.
  3. El slug es exactamente el de la pagina (norm() en JS):
     minusculas, sin acentos, [^a-z0-9]+ -> '-', sin guiones en
     los extremos; clave = norm(local) + '-vs-' + norm(visita).
  4. Si un partido del config no esta en ev.json o no tiene
     verified_events, se avisa y se sigue con time/espn_event_id
     en null; el script solo falla si el config no cuadra (otro
     numero de partidos en partidos_vivo que en el config).

Uso:
    python3 scripts/generar_mapas.py [--config scripts/config/semana-actual.json]
                                     [--salida data/mapas.json]
                                     [--partido partido.html]
"""

import argparse
import glob
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MESES_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago",
            "sep", "oct", "nov", "dic"]
MESES_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"]
DIAS_ES = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]

# Nombre corto de la competicion (como lo muestra DETAIL) desde el
# displayName de temporada de ESPN ("2026-27 English Premier
# League" -> "English Premier League"). "Liga BBVA MX" es el
# nombre oficial de ESPN para la liga que la pagina llama "Liga MX".
COMPETICION_CORTO = {"Liga BBVA MX": "Liga MX"}


def corto_competicion(nombre):
    nombre = re.sub(r"^\d{4}-\d{2} ", "", nombre or "")
    return COMPETICION_CORTO.get(nombre, nombre)
LIGA_DISPLAY = {
    "eng.1": "Premier League",
    "esp.1": "LaLiga",
    "ger.1": "Bundesliga",
    "ita.1": "Serie A",
    "mex.1": "Liga MX",
    "uefa.champions": "Champions League",
    "uefa.europa": "Europa League",
}


def norm(s):
    """Replica norm() de index.html/partido.html."""
    s = (s or "").lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def slug(home, away):
    return norm(home) + "-vs-" + norm(away)


def cargar_configs(path_config):
    """Partidos de la semana: config dado + su entre semana (si hay),
    igual que generar_vivo.py. Devuelve (semana, partidos)."""
    with open(path_config, encoding="utf-8") as f:
        actual = json.load(f)
    semana = str(actual.get("semana"))
    partidos = list(actual.get("partidos") or [])
    base = os.path.dirname(path_config)
    if semana.endswith("-entresemana"):
        numero = semana.split("-")[0]
        otro = os.path.join(base, "semana-actual.json")
        if os.path.isfile(otro):
            with open(otro, encoding="utf-8") as f:
                partidos += list(json.load(f).get("partidos") or [])
    else:
        entresemana = os.path.join(base, f"semana-{semana}-entresemana.json")
        if os.path.isfile(entresemana):
            with open(entresemana, encoding="utf-8") as f:
                partidos += list(json.load(f).get("partidos") or [])
    return semana, partidos


def cargar_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def leer_detalle_embebido(path_partido):
    """DETAIL embebido en partido.html (base para preservar lo hecho
    a mano: h2h, standings y ultimos 5 con copas). {} si no se puede
    leer: no se rompe por eso."""
    try:
        with open(path_partido, encoding="utf-8") as f:
            texto = f.read()
    except OSError as e:
        print(f"AVISO: no se pudo leer {path_partido}: {e}")
        return {}
    m = re.search(r"var DETAIL = (\{.*?\});\nvar XI_PROBABLE", texto, re.S)
    if not m:
        print("AVISO: no se encontro var DETAIL en partido.html")
        return {}
    try:
        return json.loads(m.group(1))
    except ValueError as e:
        print(f"AVISO: DETAIL embebido ilegible: {e}")
        return {}


def fecha_corta(iso):
    """'2026-11-22' -> '22 nov 2026' (formato de DETAIL.lastFive)."""
    d = date.fromisoformat(iso[:10])
    return f"{d.day} {MESES_ES[d.month - 1]} {d.year}"


def convertir_last5(info):
    """teams_last5.json (un equipo) -> lista DETAIL.lastFive.
    La competicion se resuelve fuera, aqui va None si no se conoce;
    el llamador la rellena desde los schedules."""
    juegos = []
    for m in info.get("matches") or []:
        gf = float(m.get("gf") or 0)
        ga = float(m.get("ga") or 0)
        local = bool(m.get("home"))
        if local:
            gl, gv = int(gf), int(ga)
        else:
            gl, gv = int(ga), int(gf)
        res = "V" if gf > ga else ("E" if gf == ga else "D")
        juegos.append({
            "fecha": fecha_corta(m["date"]),
            "fecha_iso": m["date"][:10],
            "rival": m["opp"],
            "local": local,
            "goles_local": str(gl),
            "goles_visitante": str(gv),
            "resultado": res,
            # Penaltis: teams_last5 no dice si hubo tanda; se deja
            # en falso y se documenta, nunca se inventa un 'true'.
            "penaltis": False,
            "competicion": None,
        })
    return juegos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="scripts/config/semana-actual.json")
    ap.add_argument("--salida", default="data/mapas.json")
    ap.add_argument("--partido", default="partido.html")
    args = ap.parse_args()

    semana, partidos = cargar_configs(args.config)
    numero = str(semana).split("-")[0]
    # Directorios de datos de la semana: fin de semana + entre semana.
    dirs = [f"data/semana-{numero}"]
    entresemana_dir = f"data/semana-{numero}-entresemana"
    if os.path.isdir(entresemana_dir):
        dirs.append(entresemana_dir)

    ev_por_partido = {}
    for d in dirs:
        p = os.path.join(d, "ev.json")
        if not os.path.isfile(p):
            continue
        for m in cargar_json(p).get("partidos") or []:
            ev_por_partido[(m["home"], m["away"])] = m

    verificados = {}
    for d in dirs:
        p = os.path.join(d, "raw", "verified_events.json")
        if not os.path.isfile(p):
            continue
        for v in cargar_json(p):
            verificados[(str(v.get("home_id")), str(v.get("away_id")))] = v

    last5 = {}
    for d in dirs:
        p = os.path.join(d, "raw", "teams_last5.json")
        if not os.path.isfile(p):
            continue
        last5.update(cargar_json(p))

    # Indice de competicion desde los schedules del raw:
    # (team_id, fecha, rival) -> nombre corto de la competicion.
    competicion = {}
    for d in dirs:
        for f in glob.glob(os.path.join(d, "raw", "schedule_*.json")):
            try:
                sched = cargar_json(f)
            except (OSError, ValueError):
                continue
            tid = str((sched.get("team") or {}).get("id"))
            for ev in sched.get("events") or []:
                comps = (ev.get("competitions") or [None])[0] or {}
                fecha = (ev.get("date") or "")[:10]
                nombre = corto_competicion(
                    (ev.get("season") or {}).get("displayName"))
                for c in comps.get("competitors") or []:
                    t = c.get("team") or {}
                    competicion[(tid, fecha, t.get("displayName"))] = nombre

    embebido = leer_detalle_embebido(args.partido)

    partidos_vivo = {}
    detalle = {}
    avisos = []
    for p in partidos:
        home, away = p["home"], p["away"]
        key = slug(home, away)
        partidos_vivo[key] = {
            "liga": p["liga"], "fecha": p["fecha"],
            "home_id": p["home_id"], "away_id": p["away_id"],
            "home": home, "away": away,
        }
        if key in embebido:
            # Se preserva tal cual lo hecho a mano (h2h, standings,
            # ultimos 5 con copas); solo se marca la fuente.
            entrada = dict(embebido[key])
            entrada["fuente_detalle"] = "embebido"
            detalle[key] = entrada
            continue
        evm = ev_por_partido.get((home, away))
        liga_display = (evm or {}).get("liga") or LIGA_DISPLAY.get(p["liga"], p["liga"])
        hora = (evm or {}).get("hora")
        fecha = date.fromisoformat(p["fecha"])
        ver = verificados.get((str(p["home_id"]), str(p["away_id"])))
        if evm is None:
            avisos.append(f"{home} vs {away}: sin ev.json (liga/hora)")
        if ver is None:
            avisos.append(f"{home} vs {away}: sin verified_events "
                          "(espn_event_id en null)")
        # Ultimos 5 desde teams_last5 (los mismos del modelo).
        lf = {"home": [], "away": []}
        for lado, equipo in (("home", home), ("away", away)):
            info = last5.get(equipo)
            if info is None:
                avisos.append(f"{home} vs {away}: {equipo} sin "
                              "teams_last5 (ultimos 5 vacios)")
                continue
            juegos = convertir_last5(info)
            tid = str(info.get("id"))
            for j in juegos:
                comp = competicion.get((tid, j["fecha_iso"], j["rival"]))
                if comp:
                    j["competicion"] = comp
                else:
                    # No se inventa la competicion: se usa la liga
                    # del equipo y se avisa (en la practica no pasa:
                    # 488/488 resolvieron en la prueba del 25 nov).
                    j["competicion"] = LIGA_DISPLAY.get(
                        info.get("league"), info.get("league"))
                    avisos.append(f"{home} vs {away}: competicion de "
                                  f"{equipo} vs {j['rival']} "
                                  f"({j['fecha_iso']}) sin schedule")
            for j in juegos:
                del j["fecha_iso"]
            lf[lado] = juegos
        detalle[key] = {
            "home": home, "away": away, "league": liga_display,
            "day": DIAS_ES[fecha.weekday()],
            "time": (f"{MESES_EN[fecha.month - 1]} {fecha.day} · {hora}"
                     if hora else None),
            "espn_event_id": (ver or {}).get("espn_id"),
            "lastFive": lf,
            "h2h": None,
            "standings": None,
            "lineup": {"alineacion_publicada": False,
                       "jugadores_en_roster": 0},
            "sources": {"standings_header": liga_display + " Standings"},
            "fuente_detalle": "generado",
        }

    # Validacion: los mapas deben cubrir el config completo.
    problemas = []
    if len(partidos_vivo) != len(partidos):
        problemas.append(f"partidos_vivo trae {len(partidos_vivo)} y el "
                         f"config {len(partidos)}")
    if len(detalle) != len(partidos):
        problemas.append(f"detalle trae {len(detalle)} y el config "
                         f"{len(partidos)}")
    for key, e in detalle.items():
        for campo in ("home", "away", "league", "day", "time"):
            if not e.get(campo):
                problemas.append(f"{key}: sin {campo}")
    if problemas:
        print("VALIDACION FALLIDA:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)

    n_nuevos = sum(1 for e in detalle.values()
                   if e.get("fuente_detalle") == "generado")
    n_preservados = len(detalle) - n_nuevos
    salida = {
        "version": 1,
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "semana": semana,
        "fuente": ("config + ev.json + verified_events.json + "
                   "teams_last5.json + schedule_*.json + DETAIL "
                   "embebido en partido.html (preservado)"),
        "partidos_vivo": partidos_vivo,
        "detalle": detalle,
        "resumen": {
            "partidos": len(partidos),
            "partidos_vivo": len(partidos_vivo),
            "detalle": len(detalle),
            "detalle_generado": n_nuevos,
            "detalle_preservado_embebido": n_preservados,
            "avisos": avisos,
        },
    }
    os.makedirs(os.path.dirname(args.salida) or ".", exist_ok=True)
    with open(args.salida, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
        f.write("\n")
    for a in avisos:
        print(f"AVISO: {a}")
    print(f"mapas.json: {len(partidos_vivo)} partidos_vivo, "
          f"{len(detalle)} detalle ({n_nuevos} generados, "
          f"{n_preservados} preservados del embebido), "
          f"{len(avisos)} aviso(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
