"""Orquestador de la automatizacion semanal (Football AI Agenda).

Corre los pasos en orden y valida el resultado:
  0. descubrir_partidos.py (partidos nuevos publicados tarde en ESPN:
     primera corrida solo establece la linea base; en corridas
     posteriores agrega al config los partidos que aparecen nuevos)
  1. recolectar_datos.py  (descarga ESPN + valida los partidos)
  2. calcular_poisson.py   (Poisson con distribucion completa)
  3. generar_tabla.py      (escribe la tabla .md)
  4. recolectar_momios.py  (momios DraftKings/Bet 365 de ESPN)
  5. calcular_ev.py        (EV por mercado, semaforo y mejor pick)
  6. calcular_movimientos.py (hoy vs ayer: cambio de mejor pick, de EV
     en pp con flecha, y de linea de total; escribe movimientos.json.
     Antes del paso 4 se guarda el ev.json vigente en ev-ayer.json,
     solo en la primera corrida del dia, para que el "ayer" sea el
     ultimo ev.json del dia anterior y no el de hace una hora.)

Validaciones al final (no se publica nada si fallan):
  - los partidos existen en ESPN (lo garantiza el paso 1: si falta
    uno, el paso 1 falla y este script no sigue)
  - cada equipo tiene 5 partidos en su ultimo-5 (4 en competiciones
    europeas, donde solo se han jugado 4 jornadas: se acepta n>=4 y se
    avisa; menos de 4 es error)
  - el 1X2 suma 100% (+-0.05) en los partidos
  - no hay valores nulos en la tabla
  - cada partido con momio tiene EV y semaforo; ningun partido sin
    momio ("pendiente") tiene EV inventado

Uso:
    python3 scripts/run_semana.py --config scripts/config/semana-actual.json
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fecha_snapshot(outdir):
    """Fecha del snapshot guardado en ev-ayer.json. Se lee del archivo
    ev-ayer-fecha.txt que se escribe junto al snapshot (parche del
    jefe, 23 nov 2026): en CI el checkout pone mtime de hoy a todos
    los archivos, asi que decidir por mtime congelaria el "ayer" en
    el primer dia. Sin archivo de fecha (primer uso local), la mtime."""
    fecha_path = os.path.join(ROOT, outdir, 'ev-ayer-fecha.txt')
    if os.path.exists(fecha_path):
        try:
            with open(fecha_path) as f:
                return date.fromisoformat(f.read().strip())
        except ValueError:
            pass
    ayer = os.path.join(ROOT, outdir, 'ev-ayer.json')
    if os.path.exists(ayer):
        return date.fromtimestamp(os.path.getmtime(ayer))
    return None


def guardar_ayer(outdir):
    """Guarda el ev.json vigente como ev-ayer.json, solo en la primera
    corrida del dia. Las corridas de la misma tarde (p. ej. cada hora
    en dias de partido) no lo pisan: el "ayer" sigue siendo el ultimo
    ev.json del dia anterior, no el de hace una hora."""
    ev = os.path.join(ROOT, outdir, 'ev.json')
    ayer = os.path.join(ROOT, outdir, 'ev-ayer.json')
    if not os.path.exists(ev):
        return None
    hoy = date.today()
    fecha_ayer = fecha_snapshot(outdir)
    if fecha_ayer is not None and fecha_ayer >= hoy:
        print(f"{ayer} ya es de hoy ({fecha_ayer}); no se pisa.")
        return ayer
    shutil.copy2(ev, ayer)
    with open(os.path.join(ROOT, outdir, 'ev-ayer-fecha.txt'), 'w') as f:
        f.write(hoy.isoformat() + "\n")
    print(f"Snapshot de ayer guardado en {ayer} (ev.json anterior).")
    return ayer


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

    run([sys.executable, 'scripts/descubrir_partidos.py',
         '--config', args.config, '--out', outdir])
    # El descubrimiento pudo agregar partidos al config: los pasos
    # siguientes leen el config de disco, asi que lo ven actualizado.
    run([sys.executable, 'scripts/recolectar_datos.py',
         '--config', args.config, '--out', outdir])
    run([sys.executable, 'scripts/calcular_poisson.py',
         '--config', args.config, '--out', outdir])
    run([sys.executable, 'scripts/generar_tabla.py',
         '--config', args.config, '--out', outdir])
    # Snapshot del ev.json vigente ANTES de regenerarlo: es el "ayer"
    # de los movimientos (primera corrida del dia; ver guardar_ayer).
    ayer_path = guardar_ayer(outdir)
    run([sys.executable, 'scripts/recolectar_momios.py',
         '--config', args.config, '--out', outdir])
    run([sys.executable, 'scripts/calcular_ev.py',
         '--config', args.config, '--out', outdir])
    if ayer_path:
        fecha_ayer = fecha_snapshot(outdir).isoformat()
        run([sys.executable, 'scripts/calcular_movimientos.py',
             '--hoy', os.path.join(outdir, 'ev.json'),
             '--ayer', ayer_path,
             '--salida', os.path.join(outdir, 'movimientos.json'),
             '--fecha-hoy', date.today().isoformat(),
             '--fecha-ayer', fecha_ayer])
    else:
        print("Sin ev.json anterior: primera corrida, no hay "
              "movimientos vs ayer.")

    # ---- validaciones finales ----
    rawdir = os.path.join(ROOT, outdir, 'raw')
    teams = json.load(open(os.path.join(rawdir, 'teams_last5.json')))
    res = json.load(open(os.path.join(rawdir, 'poisson_result.json')))
    evr = json.load(open(os.path.join(rawdir, 'ev_result.json')))
    problemas = []
    for name, t in teams.items():
        if t['n'] < 4:
            problemas.append(f"{name}: ultimo-5 con {t['n']} partidos, "
                             "menos de 4")
        elif t['n'] < 5:
            print(f"AVISO: {name}: ultimo-5 con {t['n']} partidos "
                  "(competicion con solo 4 jornadas jugadas; se usan "
                  "promedios por partido).")
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
