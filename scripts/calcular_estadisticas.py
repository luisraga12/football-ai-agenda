"""Estadisticas del partido desde el resumen de ESPN (Football AI Agenda).

Orden del jefe (JEFE.md 437b004 + da79093, Semana 9): publicar
data/<config>/estadisticas.json con las estadisticas de los partidos
TERMINADOS, tomadas del resumen de ESPN (endpoint summary), en el
formato que espera partido.html (comentario ~linea 1274).

Lo que trae el resumen de ESPN (boxscore.teams[].statistics, verificado
25 nov 2026 en summaries de Champions y Liga MX):
  possessionPct, totalShots, shotsOnTarget, wonCorners, foulsCommitted,
  offsides, yellowCards, redCards, accuratePasses, saves (+ otros que
  NO se publican: totalPasses, passPct, shotPct, blockedShots,
  effectiveTackles, totalTackles, interceptions, despejes...).

Mapeo a las claves de partido.html (STATS_ORDEN):
  posesion <- possessionPct (%); tiros <- totalShots;
  tiros_a_puerta <- shotsOnTarget; corners <- wonCorners;
  faltas <- foulsCommitted; fueras_de_juego <- offsides;
  tarjetas_amarillas <- yellowCards; tarjetas_rojas <- redCards;
  pases_precisos <- accuratePasses; paradas <- saves.
  "duelos_ganados" NO se publica: el resumen de ESPN no trae duelos
  (verificado en summaries de Champions y de Liga MX: no hay ninguna
  clave de duelos); inventarlo violaria la regla 5 del jefe. La pagina
  muestra solo las claves presentes; la seccion queda con 10
  estadisticas.

Solo partidos terminados (ESPN: estado 'post' en el scoreboard del
dia). Un partido terminado sin resumen, o sin boxscore, queda FUERA
del archivo (la pagina muestra "Estadisticas pendientes", sin ceros
inventados). Los resumenes crudos se guardan en
data/<config>/raw/summary_<liga>_<id>.json como cache auditable
(raw/ SÍ se sube: el workflow lo incluye en el commit con `git add data/`).

Uso:
    python3 scripts/calcular_estadisticas.py --config scripts/config/semana-2-entresemana.json
    python3 scripts/calcular_estadisticas.py --config scripts/config/semana-actual.json
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

CST = ZoneInfo("America/Mexico_City")
BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"

# (clave partido.html, etiqueta, clave ESPN, unidad)
MAPEO = [
    ("posesion", "Posesión", "possessionPct", "%"),
    ("tiros", "Tiros", "totalShots", ""),
    ("tiros_a_puerta", "Tiros a puerta", "shotsOnTarget", ""),
    ("corners", "Córners", "wonCorners", ""),
    ("faltas", "Faltas", "foulsCommitted", ""),
    ("fueras_de_juego", "Fueras de juego", "offsides", ""),
    ("tarjetas_amarillas", "Tarjetas amarillas", "yellowCards", ""),
    ("tarjetas_rojas", "Tarjetas rojas", "redCards", ""),
    ("pases_precisos", "Pases precisos", "accuratePasses", ""),
    ("paradas", "Paradas", "saves", ""),
]


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def norm(s):
    """Igual que norm() de partido.html: minusculas, sin acentos,
    lo que no es a-z0-9 pasa a '-', sin guiones en los extremos."""
    s = unicodedata.normalize('NFD', (s or '').lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def a_numero(v):
    """displayValue de ESPN es texto ('10', '33.3'); a numero."""
    if isinstance(v, (int, float)):
        return v
    try:
        f = float(str(v).replace(',', '.'))
    except (TypeError, ValueError):
        return None
    return int(f) if f == int(f) else round(f, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True, help='JSON de la semana')
    ap.add_argument('--out', default=None,
                    help='carpeta de salida (por defecto data/semana-N)')
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    semana = cfg['semana']
    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')
    os.makedirs(rawdir, exist_ok=True)

    # ---- 1. Scoreboards frescos: estado actual de cada partido ----
    eventos = {}
    for lg in cfg['ligas']:
        for d in cfg['fechas']:
            dstr = d.replace('-', '')
            try:
                data = fetch(f"{BASE}/{lg}/scoreboard?dates={dstr}")
            except Exception as ex:
                print(f"  !! no se pudo {lg} {dstr}: {ex}")
                continue
            for e in data.get('events', []):
                comp = e['competitions'][0]
                home = next(c for c in comp['competitors']
                            if c['homeAway'] == 'home')
                away = next(c for c in comp['competitors']
                            if c['homeAway'] == 'away')
                dt = datetime.fromisoformat(
                    e['date'].replace('Z', '+00:00')).astimezone(CST)
                key = (str(home['team']['id']), str(away['team']['id']),
                       dt.strftime('%Y-%m-%d'))
                eventos[key] = {
                    'id': e['id'], 'liga': lg,
                    'estado': e.get('status', {}).get('type', {}).get('state'),
                    'home': home['team']['displayName'],
                    'away': away['team']['displayName']}
            time.sleep(0.2)

    # ---- 2. Solo terminados: resumen ESPN -> estadisticas ----
    partidos_out = []
    terminados = sin_resumen = 0
    for p in cfg['partidos']:
        key = (str(p['home_id']), str(p['away_id']), p['fecha'])
        ev = eventos.get(key)
        if not ev:
            print(f"  ?? sin evento en ESPN: {p['fecha']} {p['home']} "
                  f"vs {p['away']} (no se publica nada).")
            continue
        if ev['estado'] != 'post':
            continue
        terminados += 1
        sumpath = os.path.join(rawdir,
                               f"summary_{ev['liga']}_{ev['id']}.json")
        try:
            summary = fetch(f"{BASE}/{ev['liga']}/summary"
                            f"?event={ev['id']}")
        except Exception as ex:
            print(f"  !! sin resumen ESPN: {p['home']} vs {p['away']}: "
                  f"{ex}")
            sin_resumen += 1
            continue
        with open(sumpath, 'w') as f:
            json.dump(summary, f)
        box = (summary.get('boxscore') or {}).get('teams') or []
        stats = {}
        for t in box:
            lado = 'local' if t.get('homeAway') == 'home' else 'visita'
            stats[lado] = {s.get('name'): a_numero(s.get('displayValue'))
                           for s in t.get('statistics', [])}
        if 'local' not in stats or 'visita' not in stats:
            print(f"  !! resumen sin boxscore: {p['home']} vs "
                  f"{p['away']} (no se publica).")
            sin_resumen += 1
            continue
        lista = []
        for clave, etiqueta, espn, unidad in MAPEO:
            vl = stats['local'].get(espn)
            vv = stats['visita'].get(espn)
            if vl is None or vv is None:
                print(f"  !! {p['home']} vs {p['away']}: ESPN no trae "
                      f"{espn} (se omite {clave}).")
                continue
            lista.append({'clave': clave, 'etiqueta': etiqueta,
                          'local': vl, 'visita': vv, 'unidad': unidad})
        partidos_out.append({
            'local': p['home'], 'visita': p['away'],
            'slug': norm(p['home']) + '-vs-' + norm(p['away']),
            'estado': 'post', 'estadisticas': lista})
        print(f"OK   {p['fecha']} {p['home']} vs {p['away']}: "
              f"{len(lista)} estadisticas.")
        time.sleep(0.2)

    out = {
        'config': f"semana-{semana}",
        'fecha_calculo': datetime.now(CST).strftime('%Y-%m-%d'),
        'partidos': partidos_out,
    }
    with open(os.path.join(outdir, 'estadisticas.json'), 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"\n{len(partidos_out)} partido(s) terminado(s) con "
          f"estadisticas ({terminados} terminados en ESPN, "
          f"{sin_resumen} sin resumen/boxscore). "
          "duelos_ganados no se publica: ESPN no lo trae.")
    print("OK -", os.path.join(outdir, 'estadisticas.json'))


if __name__ == '__main__':
    main()
