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
import sys
import time
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
