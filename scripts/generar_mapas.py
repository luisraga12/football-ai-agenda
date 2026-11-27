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
    lastFive, h2h, standings, lineup, estadio, sources}} — la misma
    forma del DETAIL embebido. Identidad y espn_event_id salen de
    ev.json y verified_events.json; lastFive sale de
    raw/teams_last5.json (los mismos 5 que usa el modelo) con la
    competicion resuelta desde los schedule_*.json del raw. Estadio
    y alineacion oficial (Semana 10, orden del jefe 26 nov 2026)
    salen del summary de ESPN por evento: gameInfo.venue y
    rosters[].roster filtrado por starter. Del MISMO summary salen
    tambien la tabla (standings.groups) y el historial directo
    (seasonseries, "Last 5 Matchups"). Para la Liguilla MX el
    summary no trae tabla (fase final sin tabla): se usa la tabla
    regular final (Apertura 2026) del summary de un partido de la
    ultima jornada regular (9 nov 2026).

Reglas (nada inventado, orden del jefe):
  1. Lo que no tiene fuente queda en null y la pagina lo muestra
     como pendiente. h2h y standings SI tienen fuente: el summary
     de ESPN por evento (tabla en standings.groups, historial en
     seasonseries). El endpoint /standings de ESPN no responde
     (404), no se usa. Si alguna fuente falla, el campo queda en
     null y se avisa, nunca se inventa.
  2. Las 28 entradas que ya existen embebidas en partido.html se
     PRESERVAN tal cual (con su h2h, sus standings y sus ultimos 5
     con copas, que el generador no puede reproducir desde
     teams_last5, que es solo de liga) y se marcan con
     fuente_detalle 'embebido'. Las nuevas llevan 'generado'. Asi
     el cambio no quita nada de lo que la pagina ya muestra. A la
     entrada preservada SOLO se le añaden estadio y lineup
     (Semana 10, decision del jefe 26 nov 2026), sin tocar ninguno
     de sus campos existentes.
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
import time
import unicodedata
import urllib.request
from datetime import date, datetime, timezone

# Modulo hermano (scripts/): los scripts siempre se corren como
# `python3 scripts/*.py` desde la raiz del repo, asi que resuelve.
from http_resiliente import descargar_json

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


ESPN_BASES = [
    "https://site.api.espn.com/apis/site/v2/sports/soccer",
    "https://site.web.api.espn.com/apis/site/v2/sports/soccer",
]


def fetch_summary(liga, event_id):
    """Summary ESPN por evento, con respaldo de host; None si fallan
    ambos (mismo patron que calcular_alineacion_probable.py).
    Cada intento de host reintenta errores transitorios
    (ver http_resiliente.py)."""
    for base in ESPN_BASES:
        try:
            return descargar_json(
                f"{base}/{liga}/summary?event={event_id}", timeout=20)
        except Exception:
            continue
    return None


def cargar_summary_cache(dirs, liga, event_id):
    """Summary guardado en raw/ por calcular_alineacion_probable.py
    (summary_{liga}_{event_id}.json); None si no hay ninguno."""
    for d in dirs:
        p = os.path.join(d, "raw", f"summary_{liga}_{event_id}.json")
        if not os.path.isfile(p):
            continue
        try:
            return cargar_json(p)
        except (OSError, ValueError):
            continue
    return None


def extraer_estadio_lineup(summary, home, away, home_id, away_id):
    """(estadio, lineup) desde un summary ESPN (Semana 10).

    Estadio sale de gameInfo.venue (el venue de nivel superior viene
    vacio en ESPN). La alineacion oficial sale de rosters[].roster
    filtrado por starter — boxscore.teams[].lineup[] viene vacio, no
    se usa (decision del jefe 26 nov 2026) — y se separa por equipo
    (local/visita), como el XI probable. Publicada solo si hay 11
    titulares en cada lado. Fail-soft: sin datos, estadio None y
    alineacion_publicada False.
    """
    estadio = None
    venue = (summary.get("gameInfo") or {}).get("venue") or {}
    if venue.get("fullName"):
        direccion = venue.get("address") or {}
        estadio = {
            "nombre": venue.get("fullName"),
            "ciudad": direccion.get("city"),
            "pais": direccion.get("country"),
        }
    xis = {"local": [], "visita": []}
    n_roster = 0
    for r in summary.get("rosters") or []:
        equipo = r.get("team") or {}
        if str(equipo.get("id")) == str(home_id):
            lado = "local"
        elif str(equipo.get("id")) == str(away_id):
            lado = "visita"
        elif equipo.get("displayName") == home:
            lado = "local"
        elif equipo.get("displayName") == away:
            lado = "visita"
        else:
            continue
        for x in r.get("roster") or []:
            n_roster += 1
            if not x.get("starter"):
                continue
            atleta = x.get("athlete") or {}
            pos = x.get("position") or {}
            xis[lado].append({
                "jugador": atleta.get("displayName"),
                "pos": pos.get("abbreviation") or pos.get("name"),
                "dorsal": x.get("jersey"),
            })
    return estadio, {
        "alineacion_publicada": (len(xis["local"]) == 11
                                 and len(xis["visita"]) == 11),
        "jugadores": xis,
        "jugadores_en_roster": n_roster,
    }


def _fila_tabla(entries, team_id, team_name):
    """Fila de la tabla ESPN (DETAIL.standings) para un equipo, o None.

    entries: summary.standings.groups[0].standings.entries. La fila
    DETAIL lleva los 8 campos del embebido, todos texto: pos (rank),
    pts, pj, g (ganados), e (empatados), p (perdidos), dg
    (pointDifferential, ya con signo) y récord "G-E-P". Se busca por
    id de equipo y, si no hay id, por nombre.
    """
    for e in entries or []:
        if (str(e.get("id")) == str(team_id)
                or e.get("team") == team_name):
            st = {x.get("name"): x.get("displayValue")
                  for x in e.get("stats") or []}
            try:
                g, em, p = st["wins"], st["ties"], st["losses"]
            except KeyError:
                return None
            return {
                "pos": st.get("rank"), "pts": st.get("points"),
                "pj": st.get("gamesPlayed"), "g": g, "e": em, "p": p,
                "dg": st.get("pointDifferential"),
                "récord": f"{g}-{em}-{p}",
            }
    return None


def extraer_standings(summary, home_id, away_id, home, away):
    """(standings, header) desde summary.standings.groups, o (None, None).

    La tabla es la de la competicion del partido, en vivo. Devuelve
    standings solo si estan los dos equipos; si no, None (la pagina
    muestra "pendiente").
    """
    grupos = ((summary or {}).get("standings") or {}).get("groups") or []
    for g in grupos:
        entries = (g.get("standings") or {}).get("entries") or []
        if not entries:
            continue
        casa = _fila_tabla(entries, home_id, home)
        fuera = _fila_tabla(entries, away_id, away)
        if casa and fuera:
            return {"home": casa, "away": fuera}, g.get("header")
    return None, None


def _resumen_serie(summary_en):
    """'BMG leads series 2-1-2' -> 'BMG lidera la serie 2-1-2';
    'Series tied 2-2' -> 'Serie empatada 2-2'. None si no se reconoce
    (el llamador usa una etiqueta neutra, nunca un registro inventado)."""
    if not summary_en:
        return None
    m = re.match(r"^(\w+) leads series ([\d-]+)$", summary_en)
    if m:
        return f"{m.group(1)} lidera la serie {m.group(2)}"
    m = re.match(r"^Series tied ([\d-]+)$", summary_en)
    if m:
        return f"Serie empatada {m.group(1)}"
    return None


def _fecha_corta_h2h(iso):
    """'2026-01-31T14:30:00Z' -> '31 ene 2026' (fecha UTC, igual que
    lastFive en convertir_last5: el repo usa la fecha ISO)."""
    d = date.fromisoformat(iso[:10])
    return f"{d.day} {MESES_ES[d.month - 1]} {d.year}"


def extraer_h2h(summary):
    """DETAIL.h2h desde summary.seasonseries (head-to-head), o None.

    Formato identico al embebido (verificado contra
    werder-bremen-vs-borussia-monchengladbach: resumen, etiqueta y
    los 5 partidos coinciden con el summary de ESPN): resumen
    traducido del summary de ESPN, etiqueta = shortSummary
    ("Last 5 Matchups"), partidos del mas reciente al mas antiguo.
    """
    for serie in (summary or {}).get("seasonseries") or []:
        if serie.get("type") != "head-to-head":
            continue
        resumen = _resumen_serie(serie.get("summary"))
        partidos = []
        for ev in serie.get("events") or []:
            comps = ev.get("competitors") or []
            casa = next((c for c in comps
                         if c.get("homeAway") == "home"), None)
            fuera = next((c for c in comps
                          if c.get("homeAway") == "away"), None)
            if not casa or not fuera:
                continue
            partidos.append({
                "fecha": _fecha_corta_h2h(ev.get("date") or ""),
                "local": (casa.get("team") or {}).get("displayName"),
                "visitante": (fuera.get("team") or {}).get("displayName"),
                "goles_local": str(casa.get("score")),
                "goles_visitante": str(fuera.get("score")),
            })
        if not partidos:
            return None
        return {
            "resumen": resumen or "Historial directo",
            "etiqueta": serie.get("shortSummary") or "Last 5 Matchups",
            "partidos": partidos,
        }
    return None


_TABLA_MX_REGULAR = None  # cache por corrida: (entries, header) o False


def tabla_mx_regular():
    """Tabla regular final (Apertura 2026) para la Liguilla MX.

    Los summaries de Liguilla traen standings.groups vacio (fase
    final sin tabla). La tabla regular final sale del summary de un
    partido de la ultima jornada regular: se busca el primer evento
    terminado en el scoreboard mex.1 del 8 nov 2026 (fecha en hora
    local CST — los eventos salen con fecha UTC 9 nov; el
    scoreboard con dates=20261109 devuelve 0 eventos).
    Cache por corrida; None si falla (la tabla MX queda en null).
    """
    global _TABLA_MX_REGULAR
    if _TABLA_MX_REGULAR is not None:
        return _TABLA_MX_REGULAR or None
    _TABLA_MX_REGULAR = False
    try:
        req = urllib.request.Request(
            f"{ESPN_BASES[0]}/mex.1/scoreboard?dates=20261108",
            headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            sb = json.load(r)
        for ev in sb.get("events") or []:
            if (ev.get("status") or {}).get("type", {}).get("state") != "post":
                continue
            summary = fetch_summary("mex.1", ev["id"])
            if summary is None:
                continue
            grupos = (summary.get("standings") or {}).get("groups") or []
            for g in grupos:
                entries = (g.get("standings") or {}).get("entries") or []
                if entries:
                    _TABLA_MX_REGULAR = (entries, g.get("header"))
                    return _TABLA_MX_REGULAR
    except Exception as exc:
        print(f"AVISO: tabla regular MX no disponible ({exc})")
    return None


def resumen_partido(liga, event_id, home, away, home_id, away_id,
                    dirs, avisos, key):
    """(estadio, lineup, summary) del partido desde el summary ESPN.

    Fetch en vivo por evento; si falla, respaldo con el summary
    guardado en raw/ (si lo hay); si no hay nada, fail-soft (estadio
    None, alineacion_publicada False, summary None). Nunca se inventa
    nada. El summary se devuelve para reutilizarlo (standings, h2h)
    sin volver a llamar a ESPN.
    """
    vacio = (None, {"alineacion_publicada": False,
                    "jugadores": {"local": [], "visita": []},
                    "jugadores_en_roster": 0}, None)
    if not event_id:
        return vacio
    summary = fetch_summary(liga, event_id)
    if summary is None:
        summary = cargar_summary_cache(dirs, liga, event_id)
        if summary is not None:
            avisos.append(f"{key}: summary en vivo fallo, se uso el "
                          "guardado en raw/")
    if summary is None:
        avisos.append(f"{key}: sin summary ESPN (estadio/lineup "
                      "pendientes)")
        return vacio
    time.sleep(0.2)
    estadio, lineup = extraer_estadio_lineup(
        summary, home, away, home_id, away_id)
    return estadio, lineup, summary


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
            # ultimos 5 con copas); solo se marca la fuente y se le
            # AÑADEN estadio y lineup (Semana 10), sin tocar sus
            # campos existentes.
            entrada = dict(embebido[key])
            entrada["fuente_detalle"] = "embebido"
            estadio, lineup, _summary = resumen_partido(
                p["liga"], entrada.get("espn_event_id"), home, away,
                p["home_id"], p["away_id"], dirs, avisos, key)
            # Septima ronda, Tarea 2: a la entrada preservada SOLO se
            # le añaden estadio y lineup (Semana 10) MAS el h2h cuando
            # viene en null (no se toca ningun campo existente: el h2h
            # preservado, los standings y los ultimos 5 con copas se
            # quedan tal cual).
            if not entrada.get("h2h"):
                h2h_pres = extraer_h2h(_summary)
                if h2h_pres is not None:
                    entrada["h2h"] = h2h_pres
                else:
                    avisos.append(f"{home} vs {away}: sin historial "
                                  "directo ESPN (h2h pendiente)")
            entrada["estadio"] = estadio
            entrada["lineup"] = lineup
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
        estadio, lineup, summary = resumen_partido(
            p["liga"], (ver or {}).get("espn_id"), home, away,
            p["home_id"], p["away_id"], dirs, avisos, key)
        standings, header_tabla = extraer_standings(
            summary, p["home_id"], p["away_id"], home, away)
        if standings is None and p["liga"] == "mex.1":
            # Liguilla: el summary no trae tabla; usar la regular final.
            ref = tabla_mx_regular()
            if ref is not None:
                entries_mx, header_mx = ref
                casa = _fila_tabla(entries_mx, p["home_id"], home)
                fuera = _fila_tabla(entries_mx, p["away_id"], away)
                if casa and fuera:
                    standings = {"home": casa, "away": fuera}
                    header_tabla = header_mx
                else:
                    avisos.append(f"{home} vs {away}: equipos sin "
                                  "fila en la tabla regular MX")
            else:
                avisos.append(f"{home} vs {away}: sin tabla regular MX "
                              "(standings pendiente)")
        h2h = extraer_h2h(summary)
        if standings is None:
            avisos.append(f"{home} vs {away}: sin standings ESPN "
                          "(tabla pendiente)")
        if h2h is None:
            avisos.append(f"{home} vs {away}: sin historial directo "
                          "ESPN (h2h pendiente)")
        detalle[key] = {
            "home": home, "away": away, "league": liga_display,
            "day": DIAS_ES[fecha.weekday()],
            "time": (f"{MESES_EN[fecha.month - 1]} {fecha.day} · {hora}"
                     if hora else None),
            "espn_event_id": (ver or {}).get("espn_id"),
            "lastFive": lf,
            "h2h": h2h,
            "standings": standings,
            "lineup": lineup,
            "estadio": estadio,
            "sources": {"standings_header":
                        header_tabla or liga_display + " Standings"},
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
        for campo in ("estadio", "lineup"):
            if campo not in e:
                problemas.append(f"{key}: sin {campo} (Semana 10)")
    if problemas:
        print("VALIDACION FALLIDA:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)

    n_nuevos = sum(1 for e in detalle.values()
                   if e.get("fuente_detalle") == "generado")
    n_preservados = len(detalle) - n_nuevos
    n_estadio = sum(1 for e in detalle.values() if e.get("estadio"))
    n_xi = sum(1 for e in detalle.values()
               if (e.get("lineup") or {}).get("alineacion_publicada"))
    n_standings = sum(1 for e in detalle.values() if e.get("standings"))
    n_h2h = sum(1 for e in detalle.values() if e.get("h2h"))
    salida = {
        "version": 1,
        "generado_en": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "semana": semana,
        "fuente": ("config + ev.json + verified_events.json + "
                   "teams_last5.json + schedule_*.json + DETAIL "
                   "embebido en partido.html (preservado) + summary "
                   "ESPN por evento (estadio + alineacion oficial + "
                   "standings + h2h; tabla regular MX para Liguilla)"),
        "partidos_vivo": partidos_vivo,
        "detalle": detalle,
        "resumen": {
            "partidos": len(partidos),
            "partidos_vivo": len(partidos_vivo),
            "detalle": len(detalle),
            "detalle_generado": n_nuevos,
            "detalle_preservado_embebido": n_preservados,
            "detalle_con_estadio": n_estadio,
            "detalle_con_alineacion_oficial": n_xi,
            "detalle_con_standings": n_standings,
            "detalle_con_h2h": n_h2h,
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
          f"{n_estadio} con estadio, {n_xi} con alineacion oficial, "
          f"{n_standings} con standings, {n_h2h} con h2h, "
          f"{len(avisos)} aviso(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
