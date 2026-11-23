"""Calcula la tabla Poisson de una semana (Football AI Agenda).

Lee data/semana-N/raw/teams_last5.json y league_avgs.json (generados por
recolectar_datos.py) y la configuracion de la semana, y escribe
data/semana-N/raw/poisson_result.json con ataque/defensa por equipo,
xG y probabilidades 1X2, +2.5 y BTTS de cada partido.

Metodologia (aprobada por el jefe, 19 nov 2026):
  - Ataque = (GF/5) / prom. por equipo de la liga; defensa igual con GA.
    Prom. por equipo = prom. total de goles por partido / 2.
  - xG local = prom. local x ataque local x defensa visitante (y viceversa).
  - Probabilidades con la distribucion Poisson COMPLETA (rejilla 0..20,
    ver poisson_core.py). El 1X2 suma 100% sin renormalizar.

Uso:
    python3 scripts/calcular_poisson.py --config scripts/config/semana-1.json
"""

import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poisson_core import attack_defense, expected_goals, match_probs  # noqa: E402

DIAS = {'2026-11-20': 'Vie 20 nov', '2026-11-21': 'Sáb 21 nov',
        '2026-11-22': 'Dom 22 nov', '2026-11-27': 'Vie 27 nov',
        '2026-11-28': 'Sáb 28 nov', '2026-11-29': 'Dom 29 nov',
        '2026-12-04': 'Vie 4 dic', '2026-12-05': 'Sáb 5 dic',
        '2026-12-06': 'Dom 6 dic'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    semana = cfg['semana']
    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')

    teams = json.load(open(os.path.join(rawdir, 'teams_last5.json')))
    avgs = json.load(open(os.path.join(rawdir, 'league_avgs.json')))
    verificados = json.load(open(os.path.join(rawdir, 'verified_events.json')))
    hora_por_partido = {(v['home'], v['away']): v['date_cst'][11:]
                        for v in verificados}

    for lg in avgs:
        avgs[lg]['avg_por_equipo'] = avgs[lg]['avg_total'] / 2

    calc = {}
    for name, t in teams.items():
        lg = t['league']
        den = avgs[lg]['avg_por_equipo']
        ataque, defensa = attack_defense(t['gf'], t['ga'], den)
        calc[name] = {'league': lg, 'gf': t['gf'], 'ga': t['ga'],
                      'gf_pj': t['gf'] / 5, 'ga_pj': t['ga'] / 5,
                      'ataque': ataque, 'defensa': defensa,
                      'matches': t['matches']}

    rows = []
    for p in cfg['partidos']:
        lg = p['liga']
        ah, av = avgs[lg]['avg_home'], avgs[lg]['avg_away']
        xgh, xga = expected_goals(ah, av, calc[p['home']]['ataque'],
                                  calc[p['away']]['defensa'],
                                  calc[p['away']]['ataque'],
                                  calc[p['home']]['defensa'])
        pr = match_probs(xgh, xga)
        s = p1 = pr['p1'] + pr['px'] + pr['p2']
        assert abs(s - 100) < 0.05, f"1X2 no suma 100% en {p['home']}: {s}"
        rows.append({'fecha': DIAS.get(p['fecha'], p['fecha']),
                     'hora': hora_por_partido[(p['home'], p['away'])],
                     'liga': cfg['ligas'][lg], 'home': p['home'],
                     'away': p['away'], 'xgh': xgh, 'xga': xga, **pr})

    json.dump({'teams': calc, 'matches': rows, 'avgs': avgs},
              open(os.path.join(rawdir, 'poisson_result.json'), 'w'),
              indent=1, ensure_ascii=False)

    print(f"=== TABLA POISSON — {cfg['nombre']} (distribucion completa) ===")
    for r in rows:
        print(f"{r['fecha']} {r['hora']} {r['liga'][:4]:4s} {r['home']:26s} vs "
              f"{r['away']:26s} xG {r['xgh']:.2f}-{r['xga']:.2f} | "
              f"1:{r['p1']:5.1f}% X:{r['px']:5.1f}% 2:{r['p2']:5.1f}% | "
              f"+2.5:{r['over25']:5.1f}% BTTS:{r['btts']:5.1f}%")
    print()
    print("xG local medio:", round(statistics.mean(r['xgh'] for r in rows), 2),
          "| xG visitante medio:", round(statistics.mean(r['xga'] for r in rows), 2))
    print("P(1) media:", round(statistics.mean(r['p1'] for r in rows), 1),
          "| P(X) media:", round(statistics.mean(r['px'] for r in rows), 1),
          "| P(2) media:", round(statistics.mean(r['p2'] for r in rows), 1))


if __name__ == '__main__':
    main()
