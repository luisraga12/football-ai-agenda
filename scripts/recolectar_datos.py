"""Descarga los datos de ESPN para una semana (Football AI Agenda).

Lee la configuracion de la semana (scripts/config/semana-N.json) y:
  1. Descarga los scoreboards de cada liga y fecha, y VALIDA que los 16
     partidos de la configuracion existan en ESPN (por ID de equipo).
     Si falta alguno, el script FALLA y no se calcula nada: no se inventa
     ningun dato (condicion 2 del jefe, 19 nov 2026).
  2. Descarga el schedule de cada equipo y toma sus ultimos 5 partidos de
     liga completados hasta el cutoff de la configuracion.
  3. Calcula los promedios de cada liga desde los scoreboards de las
     ultimas ~3 jornadas completadas antes del cutoff.

Todo desde la API publica de ESPN, sin clave ni credenciales.
Los JSON crudos quedan en data/semana-N/raw/ para poder auditarlos.

Uso:
    python3 scripts/recolectar_datos.py --config scripts/config/semana-1.json
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
    ligas = cfg['ligas']
    fechas = cfg['fechas']
    partidos = cfg['partidos']
    cutoff = datetime.fromisoformat(cfg['cutoff'].replace('Z', '+00:00'))

    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')
    os.makedirs(rawdir, exist_ok=True)

    # ---- 1. Scoreboards: validar que los 16 partidos existan en ESPN ----
    found = {}
    for lg in ligas:
        for d in fechas:
            dstr = d.replace('-', '')
            data = fetch(f"{BASE}/{lg}/scoreboard?dates={dstr}")
            with open(os.path.join(rawdir, f"scoreboard_{lg}_{dstr}.json"), 'w') as f:
                json.dump(data, f)
            for e in data.get('events', []):
                comp = e['competitions'][0]
                home = next(c for c in comp['competitors'] if c['homeAway'] == 'home')
                away = next(c for c in comp['competitors'] if c['homeAway'] == 'away')
                dt = datetime.fromisoformat(e['date'].replace('Z', '+00:00')).astimezone(CST)
                found[(str(home['team']['id']), str(away['team']['id']), dt.strftime('%Y-%m-%d'))] = {
                    'league': lg,
                    'date_cst': dt.strftime('%Y-%m-%d %H:%M'),
                    'home': home['team']['displayName'],
                    'home_id': home['team']['id'],
                    'away': away['team']['displayName'],
                    'away_id': away['team']['id'],
                    'status': comp.get('status', {}).get('type', {}).get('name'),
                    'espn_id': e['id'],
                }
            time.sleep(0.3)

    faltantes = []
    verificados = []
    for p in partidos:
        key = (str(p['home_id']), str(p['away_id']), p['fecha'])
        if key in found:
            verificados.append({**p, **found[key]})
            v = found[key]
            print(f"OK   {v['date_cst']} CST | {v['home']} vs {v['away']} | "
                  f"{ligas[v['league']]} | {v['status']}")
        else:
            faltantes.append(p)
            print(f"NO ENCONTRADO: {p['fecha']} {p['home']} vs {p['away']} "
                  f"| {ligas[p['liga']]}")
    if faltantes:
        print(f"\nERROR: {len(faltantes)} partido(s) no existen en ESPN. "
              "No se calcula nada para no inventar datos.")
        sys.exit(1)
    with open(os.path.join(rawdir, 'verified_events.json'), 'w') as f:
        json.dump(verificados, f, indent=1, ensure_ascii=False)
    print(f"\n16/16 partidos verificados en ESPN.")

    # ---- 2. Ultimos 5 partidos de liga por equipo ----
    equipos = {}
    for p in partidos:
        for lado in ('home', 'away'):
            equipos[p[f'{lado}_id']] = (p['liga'], p[lado])

    teams_last5 = {}
    for tid, (lg, name) in sorted(equipos.items(), key=lambda kv: kv[1][1]):
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
    with open(os.path.join(rawdir, 'teams_last5.json'), 'w') as f:
        json.dump(teams_last5, f, indent=1, ensure_ascii=False)

    # ---- 3. Promedios de liga desde scoreboards de jornadas pasadas ----
    league_avgs = {}
    cutoff_date = cfg['cutoff'][:10]
    for lg in ligas:
        cal = json.load(open(os.path.join(
            rawdir, f"scoreboard_{lg}_{fechas[0].replace('-', '')}.json"))
        )['leagues'][0]['calendar']
        past = sorted([c for c in cal if c[:10] < cutoff_date])
        use_dates = past[-9:]  # ultimas ~3 jornadas
        tot_m = tot_h = tot_a = 0
        per_date = []
        for c in use_dates:
            dstr = c[:10].replace('-', '')
            try:
                d = fetch(f"{BASE}/{lg}/scoreboard?dates={dstr}")
            except Exception as ex:
                print(f"  !! no se pudo {lg} {dstr}: {ex}")
                continue
            with open(os.path.join(rawdir, f"avg_{lg}_{dstr}.json"), 'w') as f:
                json.dump(d, f)
            m = h = a = 0
            for e in d.get('events', []):
                comp = e['competitions'][0]
                if comp.get('status', {}).get('type', {}).get('name') != 'STATUS_FULL_TIME':
                    continue
                sc = score_of(comp)
                if sc.get('home') is None or sc.get('away') is None:
                    continue
                m += 1
                h += sc['home']
                a += sc['away']
            per_date.append((dstr, m, h, a))
            tot_m += m
            tot_h += h
            tot_a += a
            time.sleep(0.3)
        league_avgs[lg] = {
            'dates': [p[0] for p in per_date], 'matches': tot_m,
            'home_goals': tot_h, 'away_goals': tot_a,
            'avg_total': (tot_h + tot_a) / tot_m if tot_m else None,
            'avg_home': tot_h / tot_m if tot_m else None,
            'avg_away': tot_a / tot_m if tot_m else None}
        print(f"{ligas[lg]}: fechas {league_avgs[lg]['dates']} | partidos={tot_m} "
              f"GH={tot_h:.0f} GA={tot_a:.0f} | prom total="
              f"{league_avgs[lg]['avg_total']:.3f} local="
              f"{league_avgs[lg]['avg_home']:.3f} visitante="
              f"{league_avgs[lg]['avg_away']:.3f}")
    with open(os.path.join(rawdir, 'league_avgs.json'), 'w') as f:
        json.dump(league_avgs, f, indent=1, ensure_ascii=False)
    print("OK - datos en", outdir)


if __name__ == '__main__':
    main()
