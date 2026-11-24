"""Corre calcular_movimientos.py para las semanas con datos.

El "ayer" sale de una de estas dos fuentes (en este orden):
  1. --ayer-commit <commit>: saca el ev.json de ese commit con
     `git show` (para probar con el historial, p. ej. comparar el
     refresco del lunes con el ev.json del domingo).
  2. Sin --ayer-commit: usa data/semana-N/ev-ayer.json, que
     `run_semana.py` guarda antes de regenerar el ev.json de hoy
     (primera corrida del dia; ver scripts/README.md).

Uso:
    python3 scripts/run_movimientos.py --ayer-commit 5ad1a85
    python3 scripts/run_movimientos.py --semanas semana-2-entresemana
    python3 scripts/run_movimientos.py
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEMANAS = ['semana-2', 'semana-3', 'semana-2-entresemana']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--semanas', nargs='+', default=SEMANAS,
                    help='p. ej. semana-2 semana-3 semana-2-entresemana')
    ap.add_argument('--ayer-commit', default=None,
                    help='commit del que sale el ev.json de ayer')
    ap.add_argument('--fecha-hoy', default=None)
    ap.add_argument('--fecha-ayer', default=None)
    args = ap.parse_args()

    for semana in args.semanas:
        outdir = os.path.join(ROOT, 'data', semana)
        hoy = os.path.join(outdir, 'ev.json')
        salida = os.path.join(outdir, 'movimientos.json')
        if not os.path.exists(hoy):
            print(f"AVISO: {semana} sin ev.json, se salta.")
            continue
        if args.ayer_commit:
            with tempfile.NamedTemporaryFile(
                    'w', suffix='.json', delete=False) as tmp:
                ayer_path = tmp.name
            r = subprocess.run(
                ['git', 'show',
                 f"{args.ayer_commit}:data/{semana}/ev.json"],
                cwd=ROOT, capture_output=True, text=True)
            if r.returncode != 0:
                print(f"ERROR: no hay ev.json de {semana} en "
                      f"{args.ayer_commit}: {r.stderr.strip()}")
                os.unlink(ayer_path)
                sys.exit(1)
            with open(ayer_path, 'w') as f:
                f.write(r.stdout)
        else:
            ayer_path = os.path.join(outdir, 'ev-ayer.json')
            if not os.path.exists(ayer_path):
                print(f"AVISO: {semana} sin ev-ayer.json (ni "
                      "--ayer-commit), se salta.")
                continue
        cmd = [sys.executable, 'scripts/calcular_movimientos.py',
               '--hoy', hoy, '--ayer', ayer_path, '--salida', salida]
        if args.fecha_hoy:
            cmd += ['--fecha-hoy', args.fecha_hoy]
        if args.fecha_ayer:
            cmd += ['--fecha-ayer', args.fecha_ayer]
        r = subprocess.run(cmd, cwd=ROOT)
        if args.ayer_commit:
            os.unlink(ayer_path)
        if r.returncode != 0:
            sys.exit(r.returncode)


if __name__ == '__main__':
    main()
