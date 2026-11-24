"""Corre calcular_tendencias.py para las semanas con datos.

Por semana lee data/semana-N/ev.json y
data/semana-N/raw/teams_last5.json (generados por
recolectar_datos.py) y escribe data/semana-N/tendencias.json.

Si una semana no tiene teams_last5.json (p. ej. un checkout sin
raw/), se salta con AVISO y no se rompe nada: las tendencias de
esa semana quedan pendientes hasta que se corra recolectar_datos.py.

Uso:
    python3 scripts/run_tendencias.py
    python3 scripts/run_tendencias.py --semanas semana-2 semana-2-entresemana
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEMANAS = ['semana-2', 'semana-3', 'semana-2-entresemana']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--semanas', nargs='+', default=SEMANAS,
                    help='p. ej. semana-2 semana-3 semana-2-entresemana')
    args = ap.parse_args()

    for semana in args.semanas:
        outdir = os.path.join(ROOT, 'data', semana)
        ev = os.path.join(outdir, 'ev.json')
        teams = os.path.join(outdir, 'raw', 'teams_last5.json')
        salida = os.path.join(outdir, 'tendencias.json')
        if not os.path.exists(ev):
            print('AVISO: ' + semana + ' sin ev.json, se salta.')
            continue
        if not os.path.exists(teams):
            print('AVISO: ' + semana + ' sin raw/teams_last5.json, '
                  'se salta. Corre recolectar_datos.py para esa semana.')
            continue
        r = subprocess.run(
            [sys.executable, 'scripts/calcular_tendencias.py',
             '--ev', ev, '--teams-last5', teams,
             '--salida', salida], cwd=ROOT)
        if r.returncode != 0:
            sys.exit(r.returncode)


if __name__ == '__main__':
    main()
