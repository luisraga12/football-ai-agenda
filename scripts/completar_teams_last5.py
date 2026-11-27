"""Completa raw/teams_last5.json con los equipos que faltan
(Football AI Agenda).

Orden del jefe (JEFE.md da79093, Semana 9): completar el
raw/teams_last5.json de entre semana con los 19 partidos nuevos
(Radiografia 36 -> 55; ultimos 5/H2H/tabla de los 27 nuevos tambien
dependen de esa consulta).

Reutiliza la logica exacta de recolectar_datos.py paso 2 (mismo cutoff
del config, mismos filtros: STATUS_FULL_TIME, fecha <= cutoff, sin
marcador se salta; ultimos 5 por fecha desc): solo calcula los equipos
del config que NO estan ya en el archivo, y los agrega sin tocar los
existentes. Guarda tambien raw/schedule_<liga>_<id>.json por equipo
nuevo, igual que recolectar_datos.py.

Uso:
    python3 scripts/completar_teams_last5.py --config scripts/config/semana-2-entresemana.json
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime

# Modulo hermano (scripts/): los scripts siempre se corren como
# `python3 scripts/*.py` desde la raiz del repo, asi que resuelve.
from http_resiliente import descargar_json

BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"


def fetch(url):
    """GET con reintentos (ver http_resiliente.py)."""
    return descargar_json(url)


def score_of(comp):
    out = {}
    for c in comp['competitors']:
        s = c.get('score')
        val = None
        if isinstance(s, dict):
            val = s.get('value')
        elif isinstance(s, (int, float)):
            val = s
        elif isinstance(s, str):
            try:
                val = float(s)
            except ValueError:
                val = None
        out[c['homeAway']] = val
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True, help='JSON de la semana')
    ap.add_argument('--out', default=None,
                    help='carpeta de salida (por defecto data/semana-N)')
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    semana = cfg['semana']
    cutoff = datetime.fromisoformat(cfg['cutoff'].replace('Z', '+00:00'))

    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')
    os.makedirs(rawdir, exist_ok=True)

    t5_path = os.path.join(rawdir, 'teams_last5.json')
    teams_last5 = json.load(open(t5_path)) if os.path.exists(t5_path) else {}

    equipos = {}
    for p in cfg['partidos']:
        for lado in ('home', 'away'):
            equipos[p[lado]] = (p['liga'], p[f'{lado}_id'])

    faltantes = {n: v for n, v in equipos.items() if n not in teams_last5}
    print(f"Equipos en config: {len(equipos)}; en teams_last5: "
          f"{len(teams_last5)}; faltan: {len(faltantes)}.")
    if not faltantes:
        print("Nada que completar.")
        return

    for name, (lg, tid) in sorted(faltantes.items(), key=lambda kv: kv[0]):
        d = fetch(f"{BASE}/{lg}/teams/{tid}/schedule")
        with open(os.path.join(rawdir, f"schedule_{lg}_{tid}.json"), 'w') as f:
            json.dump(d, f)
        completed = []
        for e in d.get('events', []):
            comp = e['competitions'][0]
            st = comp.get('status', {}).get('type', {}).get('name')
            dt = datetime.fromisoformat(e['date'].replace('Z', '+00:00'))
            if st == 'STATUS_FULL_TIME' and dt <= cutoff:
                sc = score_of(comp)
                if sc.get('home') is None or sc.get('away') is None:
                    continue
                home = next(c for c in comp['competitors'] if c['homeAway'] == 'home')
                away = next(c for c in comp['competitors'] if c['homeAway'] == 'away')
                is_home = str(home['team']['id']) == str(tid)
                gf = sc['home'] if is_home else sc['away']
                ga = sc['away'] if is_home else sc['home']
                completed.append({
                    'date': e['date'],
                    'opp': away['team']['displayName'] if is_home else home['team']['displayName'],
                    'home': is_home, 'gf': gf, 'ga': ga})
        completed.sort(key=lambda x: x['date'], reverse=True)
        last5 = completed[:5]
        teams_last5[name] = {'league': lg, 'id': tid, 'matches': last5,
                             'gf': sum(m['gf'] for m in last5),
                             'ga': sum(m['ga'] for m in last5),
                             'n': len(last5)}
        if len(last5) < 5:
            print(f"AVISO: {name} solo tiene {len(last5)} partidos "
                  "completados antes del cutoff (se esperaban 5).")
        print(f"{name:28s} n={len(last5)} GF={teams_last5[name]['gf']:.0f} "
              f"GA={teams_last5[name]['ga']:.0f}")
        time.sleep(0.3)

    with open(t5_path, 'w') as f:
        json.dump(teams_last5, f, indent=1, ensure_ascii=False)
    print(f"OK - {t5_path}: {len(teams_last5)} equipos "
          f"({len(faltantes)} agregados, 0 tocados de los existentes).")


if __name__ == '__main__':
    main()
