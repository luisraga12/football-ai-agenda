"""Orquestador de la automatizacion semanal (Football AI Agenda).

Corre los tres pasos en orden y valida el resultado:
  1. recolectar_datos.py  (descarga ESPN + valida los 16 partidos)
  2. calcular_poisson.py   (Poisson con distribucion completa)
  3. generar_tabla.py      (escribe la tabla .md)

Validaciones al final (no se publica nada si fallan):
  - los 16 partidos existen en ESPN (lo garantiza el paso 1: si falta
    uno, el paso 1 falla y este script no sigue)
  - cada equipo tiene 5 partidos en su ultimo-5
  - el 1X2 suma 100% (+-0.05) en los 16 partidos
  - no hay valores nulos en la tabla

Uso:
    python3 scripts/run_semana.py --config scripts/config/semana-actual.json
"""

import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd):
    print(f"$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(f"ERROR: el paso fallo con codigo {r.returncode}. "
              "No se genera ni se publica nada.")
        sys.exit(r.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True,
                    help='config de la semana, p. ej. scripts/config/semana-actual.json')
    args = ap.parse_args()

    cfg = json.load(open(os.path.join(ROOT, args.config)))
    semana = cfg['semana']
    outdir = f"data/semana-{semana}"

    run([sys.executable, 'scripts/recolectar_datos.py',
         '--config', args.config, '--out', outdir])
    run([sys.executable, 'scripts/calcular_poisson.py',
         '--config', args.config, '--out', outdir])
    run([sys.executable, 'scripts/generar_tabla.py',
         '--config', args.config, '--out', outdir])

    # ---- validaciones finales ----
    rawdir = os.path.join(ROOT, outdir, 'raw')
    teams = json.load(open(os.path.join(rawdir, 'teams_last5.json')))
    res = json.load(open(os.path.join(rawdir, 'poisson_result.json')))
    problemas = []
    for name, t in teams.items():
        if t['n'] != 5:
            problemas.append(f"{name}: ultimo-5 con {t['n']} partidos, no 5")
    for r in res['matches']:
        s = r['p1'] + r['px'] + r['p2']
        if abs(s - 100) > 0.05:
            problemas.append(f"{r['home']} vs {r['away']}: 1X2 suma {s:.2f}")
        for k in ('p1', 'px', 'p2', 'over25', 'btts', 'xgh', 'xga'):
            if r[k] is None:
                problemas.append(f"{r['home']} vs {r['away']}: {k} nulo")
    if problemas:
        print("VALIDACION FALLIDA:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)
    print(f"\nOK — Semana {semana} completa y validada: "
          f"{len(res['matches'])} partidos, {len(teams)} equipos, "
          f"tabla en {outdir}/tabla-poisson-semana-{semana}.md")


if __name__ == '__main__':
    main()
