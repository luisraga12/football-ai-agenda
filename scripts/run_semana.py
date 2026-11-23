"""Orquestador de la automatizacion semanal (Football AI Agenda).

Corre los cinco pasos en orden y valida el resultado:
  1. recolectar_datos.py  (descarga ESPN + valida los 16 partidos)
  2. calcular_poisson.py   (Poisson con distribucion completa)
  3. generar_tabla.py      (escribe la tabla .md)
  4. recolectar_momios.py  (momios DraftKings/Bet 365 de ESPN)
  5. calcular_ev.py        (EV por mercado, semaforo y mejor pick)

Validaciones al final (no se publica nada si fallan):
  - los 16 partidos existen en ESPN (lo garantiza el paso 1: si falta
    uno, el paso 1 falla y este script no sigue)
  - cada equipo tiene 5 partidos en su ultimo-5
  - el 1X2 suma 100% (+-0.05) en los 16 partidos
  - no hay valores nulos en la tabla
  - cada partido con momio tiene EV y semaforo; ningun partido sin
    momio ("pendiente") tiene EV inventado

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
    run([sys.executable, 'scripts/recolectar_momios.py',
         '--config', args.config, '--out', outdir])
    run([sys.executable, 'scripts/calcular_ev.py',
         '--config', args.config, '--out', outdir])

    # ---- validaciones finales ----
    rawdir = os.path.join(ROOT, outdir, 'raw')
    teams = json.load(open(os.path.join(rawdir, 'teams_last5.json')))
    res = json.load(open(os.path.join(rawdir, 'poisson_result.json')))
    evr = json.load(open(os.path.join(rawdir, 'ev_result.json')))
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
    for f in evr['partidos']:
        if f['estado'] == 'con_momio':
            if f['mejor_ev'] is None or f['semaforo'] is None:
                problemas.append(f"{f['home']} vs {f['away']}: con momio "
                                 "pero sin EV/semaforo")
        else:
            if f['mejor_ev'] is not None or f['semaforo'] is not None:
                problemas.append(f"{f['home']} vs {f['away']}: pendiente "
                                 "pero con EV inventado")
    if problemas:
        print("VALIDACION FALLIDA:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)
    n_verde = sum(1 for f in evr['partidos'] if f['semaforo'] == 'verde')
    n_amar = sum(1 for f in evr['partidos'] if f['semaforo'] == 'amarillo')
    n_rojo = sum(1 for f in evr['partidos'] if f['semaforo'] == 'rojo')
    n_pend = sum(1 for f in evr['partidos'] if f['estado'] != 'con_momio')
    print(f"\nOK — Semana {semana} completa y validada: "
          f"{len(res['matches'])} partidos, {len(teams)} equipos, "
          f"tabla en {outdir}/tabla-poisson-semana-{semana}.md "
          f"({n_verde} verdes, {n_amar} amarillos, {n_rojo} rojos, "
          f"{n_pend} pendientes)")


if __name__ == '__main__':
    main()
