"""Descarga los momios de ESPN para una semana (Football AI Agenda).

Lee la configuracion de la semana (scripts/config/semana-N.json) y:
  1. Descarga los scoreboards de cada liga y fecha, y VALIDA que los 16
     partidos de la configuracion existan en ESPN (por ID de equipo).
     Si falta alguno, el script FALLA y no se calcula nada: no se inventa
     ningun dato (misma regla que recolectar_datos.py).
  2. Por partido, saca los momios del bloque `odds` del evento:
     proveedor preferente DraftKings; si no hay DraftKings, se usa el
     unico proveedor disponible (p. ej. Bet 365) SOLO para ese partido
     y se etiqueta. Si no hay ningun momio, el partido queda "pendiente",
     NO se inventa ninguna cuota.
  3. Escribe data/semana-N/raw/momios.json (para calcular_ev.py) y
     guarda los scoreboards crudos en data/semana-N/raw/odds_*.json.
  4. Segunda fuente (Bzzoiro, BSD, plan gratis): despues del bucle
     ESPN, recolectar_bsd() agrega por partido la clave 'bsd' con
     btts, asian_handicap y total_corners (consenso, proveedor
     "BSD-consensus"). Si un partido no tiene momio BSD, queda
     registrado en 'sin_momio', nunca se inventa una cuota. Sin
     credencial BSD (secreto BSD_TOKEN en Actions o conector
     custom.bzzoiro en local), la segunda fuente se salta con aviso
     y la parte ESPN sigue igual.

Estructura de momios en ESPN (verificada en vivo, 22 nov 2026):
  - DraftKings: moneyline.home/away/draw.close.odds (americano, texto
    "+115"/"-160"), total.over/under.close.{line,odds} (linea "o3.5"),
    pointSpread.home/away.close.{line,odds}. Campo `overUnder` = linea.
  - Bet 365: homeTeamOdds/awayTeamOdds/drawOdds con `value` decimal
    directo (8.50/6.00/1.25), SIN total ni spread.

Todo desde la API publica de ESPN, sin clave ni credenciales.

Uso:
    python3 scripts/recolectar_momios.py --config scripts/config/semana-2.json
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=-6))
BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def americano_a_decimal(valor):
    """Convierte un momio americano (int o texto '+115'/'-160') a decimal."""
    if valor is None:
        return None
    if isinstance(valor, str):
        valor = int(valor)
    if valor > 0:
        return 1 + valor / 100.0
    if valor < 0:
        return 1 + 100.0 / abs(valor)
    return None


def _close(bloque):
    """Toma el momio 'close' si existe, si no el 'open'."""
    if not isinstance(bloque, dict):
        return {}
    return bloque.get('close') or bloque.get('open') or {}


def extraer_momios(odds_list):
    """Extrae 1X2, total y spread de la lista `odds` de un evento.

    Devuelve (proveedor, momios) o (None, None) si no hay momios.
    """
    if not odds_list:
        return None, None
    odds_list = [o for o in odds_list if isinstance(o, dict)]
    if not odds_list:
        return None, None
    elegido = None
    for o in odds_list:
        nombre = (o.get('provider') or {}).get('name', '')
        if nombre == 'DraftKings':
            elegido = o
            break
    if elegido is None:
        elegido = odds_list[0]  # unico proveedor disponible: etiquetarlo
    proveedor = (elegido.get('provider') or {}).get('name', 'desconocido')

    momios = {'proveedor': proveedor, 'moneyline': None, 'total': None,
              'spread': None}
    ml = elegido.get('moneyline') or {}
    # DraftKings: moneyline.home/away/draw.close.odds (americano)
    if ml:
        h = _close(ml.get('home')).get('odds')
        a = _close(ml.get('away')).get('odds')
        d = _close(ml.get('draw')).get('odds')
        if h is not None and a is not None and d is not None:
            momios['moneyline'] = {
                'home': americano_a_decimal(h),
                'draw': americano_a_decimal(d),
                'away': americano_a_decimal(a)}
    # Bet 365: homeTeamOdds/awayTeamOdds/drawOdds con `value` decimal
    if momios['moneyline'] is None:
        h = elegido.get('homeTeamOdds') or {}
        a = elegido.get('awayTeamOdds') or {}
        d = elegido.get('drawOdds') or {}
        if h.get('value') is not None and a.get('value') is not None \
                and d.get('value') is not None:
            momios['moneyline'] = {
                'home': float(h['value']),
                'draw': float(d['value']),
                'away': float(a['value'])}
    # Total (solo DraftKings lo trae en este formato)
    total = elegido.get('total') or {}
    if total:
        over = _close(total.get('over'))
        under = _close(total.get('under'))
        linea = elegido.get('overUnder')
        if linea is None and over.get('line'):
            linea = float(str(over['line']).lstrip('oO'))
        if linea is not None and over.get('odds') and under.get('odds'):
            momios['total'] = {
                'linea': float(linea),
                'over': americano_a_decimal(over['odds']),
                'under': americano_a_decimal(under['odds'])}
    # Spread (solo DraftKings lo trae en este formato)
    ps = elegido.get('pointSpread') or {}
    if ps:
        home = _close(ps.get('home'))
        away = _close(ps.get('away'))
        if home.get('line') is not None and away.get('line') is not None \
                and home.get('odds') and away.get('odds'):
            momios['spread'] = {
                'home_linea': float(home['line']),
                'home': americano_a_decimal(home['odds']),
                'away_linea': float(away['line']),
                'away': americano_a_decimal(away['odds'])}
    if momios['moneyline'] is None and momios['total'] is None \
            and momios['spread'] is None:
        return None, None
    return proveedor, momios


def extraer_estado_marcador(comp):
    """Saca estado y marcador de un evento de ESPN (mismo patron que
    generar_vivo.py extraer_partido): competitions[0].status.type.state
    y competitors[].score. Devuelve (estado, marcador); marcador es
    {'local': int, 'visita': int} solo cuando ESPN trae ambos goles,
    si no None. Un partido terminado sin momio sigue siendo 'post'
    con su marcador real: el estado no depende de los momios."""
    if not isinstance(comp, dict):
        return 'pre', None
    estado = ((comp.get('status') or {}).get('type') or {}).get('state',
                                                               'pre')
    local = visita = None
    for c in comp.get('competitors') or []:
        try:
            gol = None if c.get('score') is None else int(float(c['score']))
        except (TypeError, ValueError):
            gol = None
        if c.get('homeAway') == 'home':
            local = gol
        elif c.get('homeAway') == 'away':
            visita = gol
    # ESPN trae "0" en el score de los partidos aun no jugados: un
    # 0-0 de un partido 'pre' NO es un marcador real. Solo se publica
    # marcador cuando el partido esta terminado ('post') o en curso
    # ('in'); un 'pre' queda siempre sin marcador.
    marcador = None
    if estado in ('post', 'in') and local is not None \
            and visita is not None:
        marcador = {'local': local, 'visita': visita}
    return estado, marcador


# ----------------------------------------------------------------------
# Segunda fuente de momios: Bzzoiro Sports Data (BSD), plan gratis.
# Verificado con datos reales (26 nov 2026, semana 2, 55 partidos):
# - IDs BSD confirmados por pais + temporada vigente: eng.1=1, esp.1=3,
#   ger.1=5, ita.1=4, mex.1=19 (Apertura), UCL=7, UEL=8.
#   (OJO: Serie A NO es 9, Bundesliga NO es 96, UCL NO es 29: esos son
#   Brasil, Austria y CAF. La lista de /leagues/ tiene 110 ligas.)
# - Eventos: 55/55 partidos tienen evento BSD (ventana de fechas ampliada
#   +-1 dia: los partidos de 29 nov por la noche caen en 30 nov UTC).
# - Cobertura de momios (sobre los 55 partidos): btts 53/55,
#   asian_handicap 35/55 (BSD aun no publica AH del fin de semana),
#   total_corners 51/55.
# - Estrategia: 7 llamadas de eventos + 21 de momios (liga+mercado,
#   updated_after = hoy - 7 dias, paginacion completa). Sin updated_after
#   la liga trae miles de filas historicas; con el, ~50-700 por llamada.
# - Autenticacion: en GitHub Actions usa el secreto BSD_TOKEN (token
#   PELADO; el codigo agrega "Token "). En local (VM de Muse) usa el
#   conector custom.bzzoiro (el valor guardado YA trae "Token ", no se
#   agrega otro prefijo). Si no hay ni secreto ni conector, BSD se salta
#   con aviso y el resto del script sigue (la fuente ESPN no depende de
#   BSD). El token NUNCA se imprime ni se guarda en archivos.
# ----------------------------------------------------------------------

BSD_BASE = "https://sports.bzzoiro.com/api/v2"
BSD_LEAGUE_IDS = {"eng.1": 1, "esp.1": 3, "ger.1": 5, "ita.1": 4,
                  "mex.1": 19, "uefa.champions": 7, "uefa.europa": 8}
BSD_MARKETS = ["btts", "asian_handicap", "total_corners"]
BSD_DIAS_COBERTURA = 7  # updated_after = hoy - 7 dias

# Normalizacion de nombres de equipo (ESPN vs BSD traen variantes).
_TRANSlit = {"ø": "o", "đ": "d", "ł": "l", "ß": "ss", "æ": "ae",
             "þ": "th", "ð": "d", "ı": "i", "ŋ": "n"}
_GENERICOS = {"fc", "cf", "sc", "sv", "afc", "fk", "nk", "sk", "cd", "pfc",
              "kks", "rsc", "losc", "tsg", "vfb", "gnk", "ac", "as", "ud",
              "club", "de", "a", "real", "olympique",
              "cfc", "1", "04", "07", "05", "fsv", "kv"}
_ALIAS = {"munchen": "munich", "hamburger": "hamburg",
          "internazionale": "inter", "monchengladbach": "gladbach",
          "mgladbach": "gladbach", "lyonnais": "lyon", "praha": "prague"}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a):
        raise RuntimeError("redirect refused")


def _bsd_headers():
    """Cabecera Authorization para BSD, o None si no hay credencial.

    1) Secreto BSD_TOKEN (GitHub Actions): token pelado, se agrega
       el prefijo "Token ". 2) Conector custom.bzzoiro (local): el
    valor guardado YA trae "Token ", se usa tal cual via surrogate.
    """
    token = os.environ.get("BSD_TOKEN")
    if token:
        return {"Authorization": "Token " + token.strip()}
    try:
        sys.path.insert(
            0, "/opt/muse/skills/custom-connector-setup/bin")
        from dynamic_credentials import add_surrogate_to_request
        req = urllib.request.Request(BSD_BASE + "/")
        add_surrogate_to_request(
            req, "custom.bzzoiro", allowed_hosts=["sports.bzzoiro.com"])
        return dict(req.header_items())
    except Exception as exc:  # sin conector (p. ej. en Actions sin secreto)
        print(f"BSD: sin credencial ({exc}); se salta la segunda fuente.")
        return None


def _bsd_get(path, headers, contador):
    """GET a BSD. Devuelve (status, json|None). Cuenta las llamadas."""
    contador[0] += 1
    url = BSD_BASE + path
    req = urllib.request.Request(url, headers={
        "User-Agent": "football-ai-agenda/1.0", **headers})
    try:
        with urllib.request.build_opener(_NoRedirect()).open(
                req, timeout=60) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        print(f"BSD: {path} -> HTTP {e.code}")
        return e.code, None
    except Exception as e:
        print(f"BSD: {path} -> error {e}")
        return 0, None


def _bsd_get_all(path, headers, contador):
    """GET paginado (sigue `next`). Devuelve la lista de `results`."""
    rows = []
    while path:
        status, data = _bsd_get(path, headers, contador)
        if status != 200 or not isinstance(data, dict):
            break
        rows += data.get("results", []) or []
        nxt = data.get("next")
        path = nxt.replace(BSD_BASE, "") if nxt else None
    return rows


def _bsd_tokens(nombre):
    """Tokens normalizados de un nombre de equipo."""
    n = str(nombre or "")
    for k, v in _TRANSlit.items():
        n = n.replace(k, v)
    n = unicodedata.normalize("NFKD", n)
    n = "".join(c for c in n if not unicodedata.combining(c)).lower()
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    toks = [_ALIAS.get(t, t) for t in n.split() if t]
    kept = [t for t in toks if t not in _GENERICOS]
    return set(kept if kept else toks)


def _bsd_tok_match(a, b):
    if a == b:
        return True
    if len(a) >= 4 and len(b) >= 4 and (a.startswith(b) or b.startswith(a)):
        return True
    return False


def _bsd_match_partido(partido, candidatos):
    """Empareja un partido del config con un evento BSD.

    candidatos: [(bsd_id, home, away)] de la misma liga y fecha CST.
    Exige >=1 token compartido en cada lado y ganador unico por
    puntuacion. Devuelve (bsd_id, metodo) o (None, None).
    """
    th, ta = _bsd_tokens(partido["home"]), _bsd_tokens(partido["away"])
    mejor, mejor_pts, segundo = None, -1, -1
    for eid, h, a in candidatos:
        sh = sum(1 for x in th if any(_bsd_tok_match(x, y)
                                      for y in _bsd_tokens(h)))
        sa = sum(1 for x in ta if any(_bsd_tok_match(x, y)
                                      for y in _bsd_tokens(a)))
        if sh < 1 or sa < 1:
            continue
        pts = sh + sa
        if pts > mejor_pts:
            segundo, mejor, mejor_pts = mejor_pts, eid, pts
        elif pts > segundo:
            segundo = pts
    if mejor is None or mejor_pts <= segundo:
        return None, None
    for eid, h, a in candidatos:
        if eid == mejor and _bsd_tokens(h) == th and _bsd_tokens(a) == ta:
            return mejor, "exacto"
    return mejor, "nombre-variante"


def _bsd_elegir_btts(filas):
    """Filas btts de un evento -> {'yes': x, 'no': y} o None."""
    out = {}
    for r in filas:
        if r.get("bookmaker_slug") != "consensus":
            continue
        if r.get("outcome") == "yes" and r.get("decimal_odds"):
            out["yes"] = float(r["decimal_odds"])
        elif r.get("outcome") == "no" and r.get("decimal_odds"):
            out["no"] = float(r["decimal_odds"])
    return out if out.get("yes") and out.get("no") else None


def _bsd_elegir_ah(filas):
    """Filas asian_handicap -> {'line', 'home', 'away', 'push'} o None.

    Agrupa por linea; elige la linea con mas casas (desempate: la mas
    cercana a 0). Quarter lines (-0.25, -0.75...) y `push` se conservan.
    """
    por_linea = {}
    for r in filas:
        if r.get("bookmaker_slug") != "consensus":
            continue
        linea = r.get("line")
        if linea is None:
            continue
        g = por_linea.setdefault(float(linea), {"home": None, "away": None,
                                                "push": r.get("push"),
                                                "casas": 0})
        if r.get("outcome") == "HOME" and r.get("decimal_odds"):
            g["home"] = float(r["decimal_odds"])
        elif r.get("outcome") == "AWAY" and r.get("decimal_odds"):
            g["away"] = float(r["decimal_odds"])
        g["casas"] = max(g["casas"], int(r.get("bookmaker_count") or 0))
    completas = {l: g for l, g in por_linea.items()
                 if g["home"] and g["away"]}
    if not completas:
        return None
    linea = sorted(completas, key=lambda l: (-completas[l]["casas"],
                                             abs(l)))[0]
    g = completas[linea]
    return {"line": linea, "home": g["home"], "away": g["away"],
            "push": g["push"], "bookmakers": g["casas"]}


def _bsd_elegir_corners(filas):
    """Filas total_corners -> {'line', 'over', 'under'} o None.

    Elige la linea mas cercana a 9.5; desempate: mas casas.
    """
    por_linea = {}
    for r in filas:
        if r.get("bookmaker_slug") != "consensus":
            continue
        linea = r.get("line")
        if linea is None:
            continue
        g = por_linea.setdefault(float(linea), {"over": None, "under": None,
                                                "casas": 0})
        if r.get("outcome") == "over" and r.get("decimal_odds"):
            g["over"] = float(r["decimal_odds"])
        elif r.get("outcome") == "under" and r.get("decimal_odds"):
            g["under"] = float(r["decimal_odds"])
        g["casas"] = max(g["casas"], int(r.get("bookmaker_count") or 0))
    completas = {l: g for l, g in por_linea.items()
                 if g["over"] and g["under"]}
    if not completas:
        return None
    linea = sorted(completas, key=lambda l: (abs(l - 9.5),
                                             -completas[l]["casas"]))[0]
    g = completas[linea]
    return {"line": linea, "over": g["over"], "under": g["under"],
            "bookmakers": g["casas"]}


def recolectar_bsd(resultados, ligas, fechas):
    """Agrega la segunda fuente (BSD) a los partidos de `resultados`.

    No toca la parte ESPN. Por partido agrega la clave 'bsd':
    {'proveedor': 'BSD-consensus', 'bsd_event_id': int,
     'btts': {...}|None, 'asian_handicap': {...}|None,
     'corners': {...}|None, 'sin_momio': [mercados sin fila]}.
    Si un partido no tiene evento BSD o BSD falla, 'bsd' queda None y
    se reporta; nunca se inventa un momio. Devuelve un resumen.
    """
    resumen = {"llamadas_bsd": 0, "partidos": len(resultados),
               "con_evento": 0, "sin_evento": [],
               "con_btts": 0, "con_ah": 0, "con_corners": 0}
    headers = _bsd_headers()
    if headers is None:
        for r in resultados:
            r["bsd"] = None
        return resumen
    contador = [0]
    desde = (datetime.fromisoformat(min(fechas)) - timedelta(days=1)
             ).strftime("%Y-%m-%d")
    hasta = (datetime.fromisoformat(max(fechas)) + timedelta(days=1)
             ).strftime("%Y-%m-%d")
    actualizado = (datetime.now(timezone.utc)
                   - timedelta(days=BSD_DIAS_COBERTURA)
                   ).strftime("%Y-%m-%dT%H:%M:%SZ")

    # 1) Eventos BSD por liga (ventana ampliada +-1 dia por UTC/CST).
    eventos = {}
    for esp_code in ligas:
        lid = BSD_LEAGUE_IDS.get(esp_code)
        if lid is None:
            print(f"BSD: liga {esp_code} sin ID BSD; se salta.")
            continue
        filas = _bsd_get_all(
            f"/events/?league_id={lid}&date_from={desde}"
            f"&date_to={hasta}&limit=100", headers, contador)
        for e in filas:
            dt = datetime.fromisoformat(
                e["event_date"].replace("Z", "+00:00")).astimezone(CST)
            eventos[e["id"]] = {"home": e.get("home_team"),
                                "away": e.get("away_team"),
                                "fecha": dt.strftime("%Y-%m-%d"),
                                "liga": esp_code}
    por_liga_fecha = {}
    for eid, e in eventos.items():
        por_liga_fecha.setdefault((e["liga"], e["fecha"]), []).append(
            (eid, e["home"], e["away"]))

    # 2) Emparejar cada partido del config con su evento BSD.
    bsd_por_partido = {}
    for r in resultados:
        cands = por_liga_fecha.get((r["liga"], r["fecha"]), [])
        eid, metodo = _bsd_match_partido(r, cands)
        if eid:
            bsd_por_partido[id(r)] = eid
            resumen["con_evento"] += 1
        else:
            resumen["sin_evento"].append(
                f"{r['fecha']} {r['home']} vs {r['away']} [{r['liga']}]")

    # 3) Momios por liga+mercado (solo ligas del config).
    filas_por_evento = {}  # (liga, mercado) -> {event_id: [filas]}
    for esp_code in ligas:
        lid = BSD_LEAGUE_IDS.get(esp_code)
        if lid is None:
            continue
        for m in BSD_MARKETS:
            filas = _bsd_get_all(
                f"/odds/?league_id={lid}&market={m}&is_live=false"
                f"&updated_after={actualizado}&limit=100",
                headers, contador)
            por_evento = {}
            for row in filas:
                por_evento.setdefault(row["event_id"], []).append(row)
            filas_por_evento[(esp_code, m)] = por_evento

    # 4) Mapear a la forma de momios.json.
    for r in resultados:
        eid = bsd_por_partido.get(id(r))
        if not eid:
            r["bsd"] = None
            continue
        btts = _bsd_elegir_btts(
            filas_por_evento.get((r["liga"], "btts"), {}).get(eid, []))
        ah = _bsd_elegir_ah(
            filas_por_evento.get((r["liga"], "asian_handicap"), {})
            .get(eid, []))
        cor = _bsd_elegir_corners(
            filas_por_evento.get((r["liga"], "total_corners"), {})
            .get(eid, []))
        sin = [m for m, v in (("btts", btts), ("asian_handicap", ah),
                              ("corners", cor)) if v is None]
        r["bsd"] = {"proveedor": "BSD-consensus", "bsd_event_id": eid,
                    "btts": btts, "asian_handicap": ah, "corners": cor,
                    "sin_momio": sin}
        resumen["con_btts"] += bool(btts)
        resumen["con_ah"] += bool(ah)
        resumen["con_corners"] += bool(cor)
    resumen["llamadas_bsd"] = contador[0]
    return resumen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True, help='JSON de la semana')
    ap.add_argument('--out', default=None,
                    help='carpeta de salida (por defecto data/semana-N)')
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    semana = cfg['semana']
    ligas = cfg['ligas']
    fechas = cfg['fechas']
    partidos = cfg['partidos']

    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')
    os.makedirs(rawdir, exist_ok=True)

    # ---- Scoreboards: validar que los 16 partidos existan en ESPN ----
    found = {}
    for lg in ligas:
        for d in fechas:
            dstr = d.replace('-', '')
            data = fetch(f"{BASE}/{lg}/scoreboard?dates={dstr}")
            with open(os.path.join(rawdir, f"odds_{lg}_{dstr}.json"), 'w') as f:
                json.dump(data, f)
            for e in data.get('events', []):
                comp = e['competitions'][0]
                home = next(c for c in comp['competitors']
                            if c['homeAway'] == 'home')
                away = next(c for c in comp['competitors']
                            if c['homeAway'] == 'away')
                dt = datetime.fromisoformat(
                    e['date'].replace('Z', '+00:00')).astimezone(CST)
                estado_partido, marcador = extraer_estado_marcador(comp)
                found[(str(home['team']['id']), str(away['team']['id']),
                       dt.strftime('%Y-%m-%d'))] = {
                    'league': lg,
                    'date_cst': dt.strftime('%Y-%m-%d %H:%M'),
                    'home': home['team']['displayName'],
                    'home_id': home['team']['id'],
                    'away': away['team']['displayName'],
                    'away_id': away['team']['id'],
                    'odds': comp.get('odds'),
                    'espn_id': e['id'],
                    'estado_partido': estado_partido,
                    'marcador': marcador,
                }
            time.sleep(0.3)

    faltantes = []
    resultados = []
    for p in partidos:
        key = (str(p['home_id']), str(p['away_id']), p['fecha'])
        if key not in found:
            faltantes.append(p)
            print(f"NO ENCONTRADO: {p['fecha']} {p['home']} vs {p['away']} "
                  f"| {ligas[p['liga']]}")
            continue
        v = found[key]
        proveedor, momios = extraer_momios(v['odds'])
        if momios is None:
            final_txt = ''
            if v['estado_partido'] == 'post' and v['marcador']:
                final_txt = (f" | Final {v['marcador']['local']}–"
                             f"{v['marcador']['visita']}")
            print(f"PENDIENTE {v['date_cst']} CST | {v['home']} vs {v['away']} "
                  f"| {ligas[v['league']]} | sin momio en ESPN{final_txt}")
            resultados.append({**p, 'fecha_cst': v['date_cst'],
                               'liga_nombre': ligas[v['league']],
                               'proveedor': None, 'estado': 'pendiente',
                               'momios': None,
                               'estado_partido': v['estado_partido'],
                               'marcador': v['marcador']})
        else:
            ml = momios['moneyline']
            tot = momios['total']
            spr = momios['spread']
            ml_txt = (f"{ml['home']:.2f}/{ml['draw']:.2f}/{ml['away']:.2f}"
                      if ml else 'sin 1X2')
            print(f"OK   {v['date_cst']} CST | {v['home']} vs {v['away']} | "
                  f"{proveedor} | 1X2 {ml_txt} | "
                  f"total {tot['linea'] if tot else '—'} | "
                  f"spread {spr['home_linea'] if spr else '—'}")
            resultados.append({**p, 'fecha_cst': v['date_cst'],
                               'liga_nombre': ligas[v['league']],
                               'proveedor': proveedor, 'estado': 'con_momio',
                               'momios': momios,
                               'estado_partido': v['estado_partido'],
                               'marcador': v['marcador']})
    if faltantes:
        print(f"\nERROR: {len(faltantes)} partido(s) no existen en ESPN. "
              "No se calcula nada para no inventar datos.")
        sys.exit(1)
    n_momio = sum(1 for r in resultados if r['estado'] == 'con_momio')
    n_pend = sum(1 for r in resultados if r['estado'] != 'con_momio'
                 and r.get('estado_partido') != 'post')
    n_post_sin_momio = sum(1 for r in resultados
                           if r['estado'] != 'con_momio'
                           and r.get('estado_partido') == 'post')

    # ---- Segunda fuente (BSD): no toca la parte ESPN ----
    resumen_bsd = recolectar_bsd(resultados, ligas, fechas)
    print(f"\nBSD: {resumen_bsd['con_evento']}/{resumen_bsd['partidos']} "
          f"con evento | btts {resumen_bsd['con_btts']} | "
          f"asian_handicap {resumen_bsd['con_ah']} | "
          f"corners {resumen_bsd['con_corners']} | "
          f"{resumen_bsd['llamadas_bsd']} llamadas")

    with open(os.path.join(rawdir, 'momios.json'), 'w') as f:
        json.dump({'semana': semana,
                   'fecha_consulta': datetime.now(timezone.utc)
                   .strftime('%Y-%m-%d'),
                   'partidos': resultados},
                  f, indent=1, ensure_ascii=False)
    print(f"\nOK - momios en {rawdir}/momios.json: "
          f"{n_momio} con momio, {n_pend} pendientes, "
          f"{n_post_sin_momio} terminados sin momio (sin inventar).")


if __name__ == '__main__':
    main()
