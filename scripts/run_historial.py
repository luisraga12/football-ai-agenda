"""Corre calcular_historial.py para las semanas jugadas.

Por semana lee data/semana-N/tabla-poisson-semana-N.md y los
scoreboards en data/semana-N/raw/, y escribe
data/semana-N/historial.json + data/semana-N/historial.html.

Es la rutina fija de cada lunes (orden del jefe, tercera tanda): se
corre a mano el lunes, cuando la semana ya se jugó y los resultados
están finales. NO va en el flujo diario de run_semana.py: ahí los
partidos aún no se juegan y el historial saldría vacío o parcial.

Si una semana no tiene tabla o raw, se salta con AVISO. Si ningún
partido trae resultado todavía, el JSON queda con con_resultado 0 y
estado sin resultados (no se inventa nada).

Uso:
    python3 scripts/run_historial.py
    python3 scripts/run_historial.py --semanas semana-1 semana-2
"""

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEMANAS = ["semana-1"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--semanas", nargs="+", default=SEMANAS,
                    help="p. ej. semana-1 semana-2")
    args = ap.parse_args()

    for semana in args.semanas:
        outdir = os.path.join(ROOT, "data", semana)
        tabla = os.path.join(outdir, f"tabla-poisson-{semana}.md")
        rawdir = os.path.join(outdir, "raw")
        verif = os.path.join(outdir, "resultados_verificados.json")
        salida = os.path.join(outdir, "historial.json")
        html = os.path.join(outdir, "historial.html")
        if not os.path.exists(tabla):
            print(f"AVISO: {semana} sin {tabla}, se salta.")
            continue
        if not os.path.isdir(rawdir):
            print(f"AVISO: {semana} sin raw/, se salta.")
            continue
        cmd = [sys.executable, "scripts/calcular_historial.py",
               "--tabla", tabla, "--raw-dir", rawdir,
               "--salida", salida, "--html", html,
               "--semana", semana]
        if os.path.exists(verif):
            cmd += ["--verificados", verif]
        r = subprocess.run(cmd, cwd=ROOT)
        if r.returncode != 0:
            sys.exit(r.returncode)


if __name__ == "__main__":
    main()
