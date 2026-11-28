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
  7. calcular_tendencias.py (racha por mercado de los ultimos 5
     partidos por equipo, o 4 en competiciones europeas; escribe
     tendencias.json. Si falta raw/teams_last5.json, se avisa y se
     sigue sin tendencias para esa semana.)
  8. calcular_alineacion_probable.py (XI probable + Fuerza por
     partido, Semana 6; escribe alineacion-probable.json. Es parte
     del pipeline completo desde la Semana 7: un partido descubierto
     en el paso 0 tambien lleva su XI probable con Fuerza, no solo
     Poisson y EV.)
  9. calcular_estadisticas.py (estadisticas del partido terminado
     desde el resumen de ESPN, Semana 9; escribe estadisticas.json.
     Solo partidos con estado 'post'; sin resumen o sin boxscore no
     se publica nada para ese partido, nunca ceros inventados.
     "duelos_ganados" no se publica: el resumen de ESPN no lo trae.)

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
  - cada partido terminado sin momio (estado 'post' en ESPN) lleva
    su marcador real; si falta, la validacion falla

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
    # Paso 7: tendencias por mercado (racha de los ultimos 5 por
    # equipo). run_tendencias.py avisa y sigue si falta el
    # teams_last5.json de la semana.
    run([sys.executable, 'scripts/run_tendencias.py',
         '--semanas', f'semana-{semana}'])
    # Paso 8: alineacion probable + Fuerza (Semana 6). Un partido
    # descubierto en el paso 0 tambien lleva su XI probable con
    # Fuerza; el script marca pendiente al equipo sin datos, no
    # inventa nada.
    run([sys.executable, 'scripts/calcular_alineacion_probable.py',
         '--config', args.config,
         '--out', os.path.join(outdir, 'alineacion-probable.json')])
    # Paso 9: estadisticas del partido terminado (Semana 9). Solo los
    # partidos con estado 'post' en ESPN llevan estadisticas; el resto
    # queda "pendiente" en la pagina hasta que se juegue.
    run([sys.executable, 'scripts/calcular_estadisticas.py',
         '--config', args.config,
         '--out', outdir])
    # Paso 10: mapas en vivo + detalle (cobertura 28 -> 55, 25 nov
    # 2026). Regenera data/mapas.json (PARTIDOS_VIVO y DETAIL) desde
    # los datos, para que un partido descubierto en el paso 0 tenga
    # marcador en vivo y detalle sin que nadie edite el HTML a mano.
    # Lee los dos configs (fin de semana + entre semana) y el DETAIL
    # embebido en partido.html, que preserva para las 28 claves que
    # ya existen (h2h, standings y ultimos 5 con copas).
    run([sys.executable, 'scripts/generar_mapas.py',
         '--config', args.config])
    # Paso 11: Fuerza del XI oficial (27 nov 2026). Despues de
    # generar_mapas.py: lee el XI oficial publicado por ESPN en
    # mapas.json y publica data/fuerza_xi.json (F_of, F_of_efectiva
    # topada a F_prob +/- 12 y r para el recalculo del EV en el
    # detalle). Sin alineacion oficial, el lado queda en null con
    # motivo; el detalle muestra la Fuerza probable como hoy.
    run([sys.executable, 'scripts/calcular_fuerza_oficial.py'])
    # Paso 12: parlay del dia (28 nov 2026). Despues del EV: toma los
    # 3 mejores picks verdes (EV >= +5%) del dia y publica
    # data/parlay-del-dia.json. Si el archivo ya existe con la fecha
    # de hoy, no se sobrescribe (el parlay se fija por la manana).
    run([sys.executable, 'scripts/generar_parlay.py'])
    # Paso 13: resultados + Marcador (28 nov 2026). Despues del EV y
    # del parlay: lee los dos ev.json + vivo.json + el log en vivo y
    # publica data/resultados.json (recomendacion pre-partido por
    # partido, acertó/falló contra el marcador final real, y resumen
    # pre-partido vs en vivo). Sin EV positivo no hay recomendacion;
    # sin resultado final el acierto es Pendiente; sin snapshots en
    # data/live-log la columna en vivo es "sin datos", nunca inventada.

    run([sys.executable, 'scripts/generar_resultados.py'])

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
            # Un partido terminado sin momio debe llevar su marcador
            # real de ESPN; si no lo lleva, la correccion no funciono.
            if f.get('estado_partido') == 'post' and not f.get('marcador'):
                problemas.append(f"{f['home']} vs {f['away']}: terminado "
                                 "(post) sin momio pero sin marcador")
            if f.get('estado_partido') not in (None, 'pre', 'in', 'post'):
                problemas.append(f"{f['home']} vs {f['away']}: "
                                 "estado_partido desconocido: "
                                 f"{f.get('estado_partido')}")
    if problemas:
        print("VALIDACION FALLIDA:")
        for p in problemas:
            print(" -", p)
        sys.exit(1)
    n_verde = sum(1 for f in evr['partidos'] if f['semaforo'] == 'verde')
    n_amar = sum(1 for f in evr['partidos'] if f['semaforo'] == 'amarillo')
    n_rojo = sum(1 for f in evr['partidos'] if f['semaforo'] == 'rojo')
    n_pend = sum(1 for f in evr['partidos'] if f['estado'] != 'con_momio'
                 and f.get('estado_partido') != 'post')
    n_post_sin_momio = sum(1 for f in evr['partidos']
                           if f['estado'] != 'con_momio'
                           and f.get('estado_partido') == 'post')
    print(f"\nOK — Semana {semana} completa y validada: "
          f"{len(res['matches'])} partidos, {len(teams)} equipos, "
          f"tabla en {outdir}/tabla-poisson-semana-{semana}.md "
          f"({n_verde} verdes, {n_amar} amarillos, {n_rojo} rojos, "
          f"{n_pend} pendientes, {n_post_sin_momio} terminados sin momio)")


if __name__ == '__main__':
    main()
