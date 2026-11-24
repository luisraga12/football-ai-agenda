"""Movimientos de momios: hoy vs ayer (Football AI Agenda).

Orden del jefe, lunes 23 nov 2026 (JEFE.md, commit 4ab4b6c): primer
trabajo de las 6 propuestas. Compara el ev.json de HOY con el de AYER
y detecta por partido:

  - cambio de mejor pick (p. ej. PSG-Roma: Mas 3.5 -> Spread local -1.5)
  - cambio de EV del mejor pick, en puntos porcentuales, con flecha
    (sube / baja / sin cambio, umbral 0.1 pp)
  - cambio de linea de total (p. ej. Lille-Bayern: 3.5 -> 2.5)
  - EV de hoy del pick de ayer (para ver si el pick viejo sigue en
    verde aunque ya no sea el mejor)

De donde sale el "ayer":
  - En el uso diario lo pone el flujo automatico: `run_semana.py`
    guarda una copia del ev.json en `ev-ayer.json` ANTES de regenerar
    (solo la primera corrida del dia; las corridas de la misma tarde
    no la pisan), y despues corre este script con ese archivo.
  - A mano: cualquier ev.json anterior, p. ej. sacado del historial
    git (`git show <commit>:data/semana-N/ev.json > /tmp/ev-ayer.json`).
    El script acepta los ev.json VIEJOS (sin 'mercados' ni 'hora'):
    la linea de total se lee de `mercados.total.linea` si existe y si
    no de `momios.total.linea`.

Entrada: dos ev.json (hoy y ayer). Salida: movimientos.json por semana,
con la flecha por partido para que la pagina la lea, y un resumen por
stdout. No toca index.html ni descarga nada de ESPN.

Uso:
    python3 scripts/calcular_movimientos.py \\
        --hoy data/semana-2/ev.json \\
        --ayer data/semana-2/ev-ayer.json \\
        --salida data/semana-2/movimientos.json
    python3 scripts/run_movimientos.py --ayer-commit 5ad1a85
    python3 scripts/run_movimientos.py --semanas semana-2-entresemana
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Umbral para que un cambio de EV pinte flecha: menos de esto es ruido.
UMBRAL_PP = 0.1


def slug(texto):
    """Identificador estable del partido: 'local-vs-visita'."""
    sin_acentos = unicodedata.normalize('NFKD', texto).encode(
        'ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]+', '-', sin_acentos.lower()).strip('-')


def id_partido(p):
    return slug(f"{p['home']}-vs-{p['away']}")


def linea_total(p):
    """Linea de total publicada: 'mercados' (ev.json nuevo) o 'momios'
    (ev.json viejo, sin 'mercados'). None si no hay total."""
    mercados = p.get('mercados') or {}
    tot = mercados.get('total')
    if tot and tot.get('linea') is not None:
        return tot['linea']
    momios = p.get('momios') or {}
    tot = momios.get('total')
    if tot and tot.get('linea') is not None:
        return tot['linea']
    return None


def ev_de_pick(p, pick):
    """EV de un pick ('Local', 'Mas 3.5', 'Spread local -1.5', ...)
    dentro de los mercados de ESTE partido. None si no se puede
    calcular (sin 'mercados', o el mercado no existe)."""
    mercados = p.get('mercados')
    if not mercados or not pick:
        return None
    m1x2 = mercados.get('1X2') or {}
    evs = m1x2.get('ev') or {}
    if pick == 'Local':
        return evs.get('1')
    if pick == 'Empate':
        return evs.get('X')
    if pick == 'Visita':
        return evs.get('2')
    tot = mercados.get('total') or {}
    evs_tot = tot.get('ev') or {}
    if pick.startswith('Más '):
        return evs_tot.get('mas')
    if pick.startswith('Menos '):
        return evs_tot.get('menos')
    spr = mercados.get('spread') or {}
    evs_spr = spr.get('ev') or {}
    if pick.startswith('Spread local '):
        return evs_spr.get('local')
    if pick.startswith('Spread visitante '):
        return evs_spr.get('visitante')
    return None


def flecha(delta_pp):
    if delta_pp is None:
        return None
    if delta_pp > UMBRAL_PP:
        return '↑'
    if delta_pp < -UMBRAL_PP:
        return '↓'
    return '→'


def comparar(hoy, ayer):
    """Devuelve la lista de movimientos, un dict por partido de hoy."""
    por_slug_ayer = {id_partido(p): p for p in ayer['partidos']}
    movimientos = []
    for p in hoy['partidos']:
        ident = id_partido(p)
        m = {'slug': ident, 'home': p['home'], 'away': p['away'],
             'fecha': p.get('fecha'), 'hora': p.get('hora'),
             'proveedor': p.get('proveedor')}
        a = por_slug_ayer.get(ident)
        if a is None:
            m['estado'] = 'nuevo'
            m['mejor_pick_hoy'] = p.get('mejor_pick')
            m['ev_hoy'] = p.get('mejor_ev')
            movimientos.append(m)
            continue
        m['mejor_pick_ayer'] = a.get('mejor_pick')
        m['mejor_pick_hoy'] = p.get('mejor_pick')
        m['ev_ayer'] = a.get('mejor_ev')
        m['ev_hoy'] = p.get('mejor_ev')
        m['linea_ayer'] = linea_total(a)
        m['linea_hoy'] = linea_total(p)
        m['cambio_linea'] = (
            m['linea_ayer'] is not None and m['linea_hoy'] is not None
            and m['linea_ayer'] != m['linea_hoy'])
        if p.get('estado') != 'con_momio':
            m['estado'] = 'sin_momio'
            movimientos.append(m)
            continue
        if a.get('estado') != 'con_momio':
            m['estado'] = 'momio_nuevo'
            movimientos.append(m)
            continue
        m['estado'] = 'con_momio'
        m['cambio_pick'] = m['mejor_pick_ayer'] != m['mejor_pick_hoy']
        if m['ev_ayer'] is not None and m['ev_hoy'] is not None:
            m['delta_ev_pp'] = (m['ev_hoy'] - m['ev_ayer']) * 100
        else:
            m['delta_ev_pp'] = None
        m['flecha'] = flecha(m['delta_ev_pp'])
        # EV de hoy del pick de ayer (si cambio el pick, ver si el
        # viejo sigue en verde aunque ya no sea el mejor).
        if m['cambio_pick']:
            m['ev_pick_ayer_hoy'] = ev_de_pick(p, m['mejor_pick_ayer'])
        movimientos.append(m)
    return movimientos


def fmt_pct(valor):
    return f"{valor * 100:+.1f}%" if valor is not None else "—"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hoy', required=True, help='ev.json de hoy')
    ap.add_argument('--ayer', required=True, help='ev.json de ayer')
    ap.add_argument('--salida', required=True, help='movimientos.json')
    ap.add_argument('--fecha-hoy', default=None,
                    help='fecha de hoy (defecto: hoy)')
    ap.add_argument('--fecha-ayer', default=None,
                    help='fecha de ayer (defecto: ayer)')
    args = ap.parse_args()

    hoy = json.load(open(args.hoy))
    ayer = json.load(open(args.ayer))
    fecha_hoy = args.fecha_hoy or date.today().isoformat()
    fecha_ayer = args.fecha_ayer or (date.today() - timedelta(days=1)).isoformat()
    movimientos = comparar(hoy, ayer)

    salida = {'semana': hoy.get('semana'), 'fecha_hoy': fecha_hoy,
              'fecha_ayer': fecha_ayer,
              'partidos': movimientos}
    with open(args.salida, 'w') as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
        f.write('\n')

    n_cambio_pick = sum(1 for m in movimientos
                        if m.get('cambio_pick'))
    n_linea = sum(1 for m in movimientos if m.get('cambio_linea'))
    n_sube = sum(1 for m in movimientos if m.get('flecha') == '↑')
    n_baja = sum(1 for m in movimientos if m.get('flecha') == '↓')
    print(f"OK - movimientos en {args.salida} "
          f"({len(movimientos)} partidos, {n_cambio_pick} cambios de "
          f"pick, {n_linea} cambios de linea, {n_sube} suben, "
          f"{n_baja} bajan).")
    for m in movimientos:
        if m['estado'] == 'nuevo':
            print(f"  NUEVO {m['home']} vs {m['away']}: "
                  f"{m.get('mejor_pick_hoy')} {fmt_pct(m.get('ev_hoy'))}")
        elif m['estado'] == 'momio_nuevo':
            print(f"  MOMIO NUEVO {m['home']} vs {m['away']}: "
                  f"{m.get('mejor_pick_hoy')} {fmt_pct(m.get('ev_hoy'))}")
        elif m['estado'] == 'sin_momio':
            print(f"  PENDIENTE {m['home']} vs {m['away']}: sin momio")
        else:
            linea = (f" · linea {m['linea_ayer']} -> {m['linea_hoy']}"
                     if m.get('cambio_linea') else "")
            pick = (f" · pick {m['mejor_pick_ayer']} -> "
                    f"{m['mejor_pick_hoy']}"
                    if m.get('cambio_pick') else "")
            viejo = ""
            if m.get('cambio_pick') and m.get('ev_pick_ayer_hoy') is not None:
                viejo = (f" (pick de ayer hoy vale "
                         f"{fmt_pct(m['ev_pick_ayer_hoy'])})")
            print(f"  {m.get('flecha')} {m['home']} vs {m['away']}: "
                  f"{m['mejor_pick_hoy']} "
                  f"{fmt_pct(m.get('ev_ayer'))} -> "
                  f"{fmt_pct(m.get('ev_hoy'))}"
                  f" ({m.get('delta_ev_pp'):+.1f} pp)"
                  f"{pick}{linea}{viejo}")


if __name__ == '__main__':
    main()
