"""Integra momios + EV en la pagina (Football AI Agenda) — REVISION LUNES 23 nov 2026.

Responde a la orden del jefe del 22 nov (JEFE.md, origin/main commit
7e2661a): el fragmento anterior solo traia semaforo + mejor pick por
partido y no calzaba con la pagina. Esta version trae:

  (a) Bloque COMPLETO de momios por tarjeta: decimales + EV por mercado
      (1X2, total con su linea publicada, spread), con el semaforo y el
      mejor pick, y el boton de parlay solo cuando el mejor pick es EV+
      (como la pagina: 15 botones en la Semana 2, el rojo sin boton).
  (b) Marcadores POR TARJETA: un par MOMIOS-INICIO/FIN por partido, con
      el identificador del partido (slug). El jefe pone los marcadores
      en la pagina; este script no toca index.html por su cuenta.
  (c) CSS que combina con la pagina: reusa las variables :root y las
      clases .odds / .derived-h / .dcell / .add-btn que ya trae la
      pagina, y solo anade .momios-grid (7 celdas: 3 de 1X2 + 2 de total
      + 2 de spread) y los colores de EV.

Entrada: data/semana-N/ev.json REGENERADO con calcular_ev.py (desde el
23 nov incluye 'mercados' con el EV por mercado y el decimal/prob. del
mejor pick). Si el ev.json no trae 'mercados', el script falla y pide
regenerarlo; no calcula EV a ojo ni inventa momios.

Reglas de seguridad:
  - Por defecto es DRY-RUN: solo imprime el resumen, no escribe nada.
  - Solo escribe con --apply --html COPIA --out COPIA.
  - Si a un partido le falta su par de marcadores, FALLA SIN TOCAR NADA
    (valida todos antes de escribir).
  - Los partidos "pendiente" se muestran como "Momios pendientes", sin
    EV inventado; si un partido trae 1X2 pero no total/spread (p. ej.
    Hamburg-Bayern, solo Bet365), esas celdas se omiten y se anota.
  - Nunca toca index.html: la prueba se hace en una COPIA con
    marcadores (ver fragmento de prueba en EMPLEADO-1.md).

Uso:
    python3 scripts/integrar_pagina.py --ev data/semana-2/ev.json --html copia.html
    python3 scripts/integrar_pagina.py --ev data/semana-2/ev.json --html copia.html --out copia.html --apply
    python3 scripts/integrar_pagina.py --ev data/semana-2/ev.json --fragment-out data/semana-2/fragmento-momios.html --css-out data/semana-2/fragmento-momios.css
    python3 scripts/integrar_pagina.py --ev data/semana-2/ev.json --movimientos data/semana-2/movimientos.json --fragment-out data/semana-2/fragmento-momios.html
      (con --movimientos anade la flecha ↑↓ por tarjeta: cambio de EV
      en pp vs ayer, cambio de mejor pick y cambio de linea de total)
"""

import argparse
import html
import json
import re
import sys
import unicodedata


def slug(texto):
    """Identificador estable del partido: 'werder-bremen-vs-borussia-monchengladbach'."""
    sin_acentos = unicodedata.normalize('NFKD', texto).encode(
        'ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]+', '-', sin_acentos.lower()).strip('-')


def id_partido(p):
    return slug(f"{p['home']}-vs-{p['away']}")


def fmt_dec(valor):
    return f"{valor:.2f}" if valor is not None else "—"


def fmt_ev(valor):
    if valor is None:
        return "—"
    return f"{valor * 100:+.1f}%"


def clase_ev(valor):
    """Color del EV con los mismos umbrales del semaforo."""
    if valor is None:
        return ""
    if valor >= 0.05:
        return "ev-pos"
    if valor >= 0.0:
        return "ev-mid"
    return "ev-neg"


def fmt_linea(valor):
    return ('%.1f' % valor).rstrip('0').rstrip('.')


def celda(etiqueta, decimal, ev):
    return (
        f'<div class="dcell"><span>{html.escape(etiqueta)} '
        f'{fmt_dec(decimal)}</span>'
        f'<b class="num {clase_ev(ev)}">{fmt_ev(ev)}</b></div>')


def linea_mov(m):
    """Linea de movimiento de UNA tarjeta (flecha ↑↓ por tarjeta,
    orden del jefe 23 nov 2026): cambio de EV en pp vs ayer, cambio
    de mejor pick y cambio de linea de total. None si no hay
    movimiento que mostrar (sin momio, o sin datos de ayer)."""
    if not m or m.get('estado') in (None, 'sin_momio'):
        return None
    if m['estado'] == 'nuevo':
        return 'Nuevo partido hoy'
    if m['estado'] == 'momio_nuevo':
        return 'Nuevo momio hoy'
    flecha = m.get('flecha')
    delta = m.get('delta_ev_pp')
    if flecha == '↑':
        texto = f"↑ +{delta:.1f} pp vs ayer"
    elif flecha == '↓':
        texto = f"↓ {delta:.1f} pp vs ayer"
    else:
        texto = "→ sin cambio vs ayer"
    if m.get('cambio_pick'):
        texto += (f" · cambio de pick: {m['mejor_pick_ayer']} → "
                  f"{m['mejor_pick_hoy']}")
        if m.get('ev_pick_ayer_hoy') is not None:
            texto += (f" (el pick de ayer hoy vale "
                      f"{fmt_ev(m['ev_pick_ayer_hoy'])})")
    if m.get('cambio_linea'):
        texto += (f" · línea total {fmt_linea(m['linea_ayer'])} → "
                  f"{fmt_linea(m['linea_hoy'])}")
    return texto


def bloque(p, mov=None):
    """Bloque completo de momios de UNA tarjeta."""
    ident = id_partido(p)
    titulo = f"{p['home']} vs {p['away']}"
    if p['estado'] != 'con_momio':
        prov = p.get('proveedor')
        prov_txt = (f"{html.escape(prov)} aún no publica"
                    if prov else "aún no publicados")
        return (
            f'<div class="odds momios" data-partido="{ident}" '
            f'aria-label="Momios de {html.escape(titulo)}">'
            f'<div class="derived-h"><span>Momios pendientes</span>'
            f'<span>{prov_txt}</span>'
            f'</div><p class="momios-pendiente">Momios pendientes — '
            f'sin EV inventado.</p></div>')
    mercados = p.get('mercados')
    if not mercados:
        raise ValueError(
            f"{titulo}: el ev.json no trae 'mercados' (EV por mercado). "
            "Regenera con python3 scripts/calcular_ev.py --config "
            "scripts/config/semana-N.json y vuelve a intentar.")
    celdas = []
    notas = []
    m1x2 = mercados.get('1X2')
    if m1x2:
        ml, evs = m1x2['momios'], m1x2['ev']
        celdas.append(celda('Local', ml['home'], evs['1']))
        celdas.append(celda('Empate', ml['draw'], evs['X']))
        celdas.append(celda('Visita', ml['away'], evs['2']))
    else:
        notas.append('1X2 no publicado para este partido.')
    tot = mercados.get('total')
    if tot:
        linea = fmt_linea(tot['linea'])
        celdas.append(celda(f"Más {linea}", tot['momios']['over'],
                            tot['ev']['mas']))
        celdas.append(celda(f"Menos {linea}", tot['momios']['under'],
                            tot['ev']['menos']))
    else:
        notas.append('Total no publicado para este partido.')
    spr = mercados.get('spread')
    if spr:
        celdas.append(celda(f"Spread local {spr['home_linea']:+.1f}",
                            spr['momios']['home'], spr['ev']['local']))
        celdas.append(celda(
            f"Spread visita {spr['momios']['away_linea']:+.1f}",
            spr['momios']['away'], spr['ev']['visitante']))
    else:
        notas.append('Spread no publicado para este partido.')
    sem = p['semaforo']
    sem_txt = {'verde': 'Verde', 'amarillo': 'Amarillo',
               'rojo': 'Rojo'}[sem]
    mejor_txt = (f"{sem_txt} · {p['mejor_pick']} "
                 f"{fmt_ev(p['mejor_ev'])}")
    partes = [
        f'<div class="odds momios" data-partido="{ident}" '
        f'aria-label="Momios reales y valor esperado">',
        f'<div class="derived-h"><span>Momios '
        f'{html.escape(p["proveedor"])}</span>'
        f'<span>Semáforo: {mejor_txt} · EV = prob. × momio − 1</span></div>',
        '<div class="momios-grid">' + ''.join(celdas) + '</div>',
    ]
    mov_txt = linea_mov(mov)
    if mov_txt:
        partes.append(
            f'<p class="momios-mov">{html.escape(mov_txt)}</p>')
    for nota in notas:
        partes.append(f'<p class="momios-nota">{html.escape(nota)} '
                      f'({html.escape(p["proveedor"])}).</p>')
    if sem == 'verde' and p.get('mejor_decimal') is not None:
        partes.append(
            '<div class="odds-add"><button class="add-btn" type="button" '
            f'data-pick="{html.escape(titulo)} · '
            f'{html.escape(p["mejor_pick"])}" '
            f'data-odds="{p["mejor_decimal"]:.2f}" '
            f'data-prob="{p["mejor_prob"]:.1f}">'
            'Sumar al parlay</button></div>')
    partes.append('</div>')
    return ''.join(partes)


CSS = """/* Fragmento momios — Empleado 1, lunes 23 nov 2026.
   Reusa las variables :root y las clases .odds / .derived-h / .dcell /
   .add-btn de la pagina; solo anade lo que falta para el spread
   (7 celdas: 3 de 1X2 + 2 de total + 2 de spread) y los colores de EV.
   Pegar junto al resto del CSS de la pagina. */
.momios-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}
@media (max-width:900px){.momios-grid{grid-template-columns:repeat(4,1fr)}}
@media (max-width:560px){.momios-grid{grid-template-columns:repeat(3,1fr)}}
.momios .ev-pos{color:var(--accent-strong)}
.momios .ev-mid{color:var(--amber)}
.momios .ev-neg{color:var(--live)}
.momios-pendiente{margin:10px 0 0;font-size:.86rem;font-weight:700;color:var(--amber)}
.momios-nota{margin-top:10px;font-size:.78rem;font-weight:700;color:var(--muted)}
.momios-mov{margin:10px 0 0;font-size:.82rem;font-weight:700;color:var(--muted)}
"""


def marcadores(ident):
    return (f"<!-- MOMIOS-INICIO:{ident} -->",
            f"<!-- MOMIOS-FIN:{ident} -->")


def inyectar(html_texto, bloques):
    """Reemplaza cada par de marcadores por su bloque. Valida todos
    antes de escribir nada; si falta uno, falla sin tocar nada."""
    faltantes = [ident for ident in bloques
                 if marcadores(ident)[0] not in html_texto
                 or marcadores(ident)[1] not in html_texto]
    if faltantes:
        raise ValueError(
            "Faltan marcadores por tarjeta en el HTML: " +
            ", ".join(faltantes) +
            ". El jefe pone los marcadores; no se toco nada.")
    nuevo = html_texto
    for ident, frag in bloques.items():
        ini, fin = marcadores(ident)
        antes, resto = nuevo.split(ini, 1)
        _, despues = resto.split(fin, 1)
        nuevo = antes + ini + "\n" + frag + "\n" + fin + despues
    return nuevo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ev', required=True, help='data/semana-N/ev.json')
    ap.add_argument('--html', default=None, help='Copia HTML con marcadores')
    ap.add_argument('--out', default=None, help='HTML de salida')
    ap.add_argument('--apply', action='store_true',
                    help='escribir de verdad (sin esto es dry-run)')
    ap.add_argument('--fragment-out', default=None,
                    help='escribir el fragmento (todos los bloques) a un archivo')
    ap.add_argument('--css-out', default=None,
                    help='escribir el CSS del fragmento a un archivo')
    ap.add_argument('--movimientos', default=None,
                    help='movimientos.json de calcular_movimientos.py: '
                         'anade la flecha ↑↓ por tarjeta')
    args = ap.parse_args()

    ev = json.load(open(args.ev))
    movs = {}
    if args.movimientos:
        mov_data = json.load(open(args.movimientos))
        movs = {m['slug']: m for m in mov_data['partidos']}
        print(f"Movimientos leidos de {args.movimientos} "
              f"({len(movs)} partidos, "
              f"{mov_data.get('fecha_ayer')} -> "
              f"{mov_data.get('fecha_hoy')}).")
    bloques = {}
    for p in ev['partidos']:
        bloques[id_partido(p)] = bloque(p, movs.get(id_partido(p)))
    if args.fragment_out:
        open(args.fragment_out, 'w').write("\n\n".join(
            f"<!-- MOMIOS-INICIO:{k} -->\n{v}\n<!-- MOMIOS-FIN:{k} -->"
            for k, v in bloques.items()) + "\n")
        print(f"OK - fragmento escrito en {args.fragment_out} "
              f"({len(bloques)} partidos).")
    if args.css_out:
        open(args.css_out, 'w').write(CSS)
        print(f"OK - CSS escrito en {args.css_out}.")
    if not args.html:
        if not args.fragment_out and not args.css_out:
            print("DRY-RUN: no se escribio nada.")
            print(f"Partidos: {len(bloques)} "
                  f"({sum(1 for p in ev['partidos'] if p['estado'] == 'con_momio')} "
                  "con momio). Ejemplo (primer partido):")
            print(list(bloques.values())[0])
            print("\nCSS:\n" + CSS)
        return
    html_texto = open(args.html).read()
    # Compatibilidad: si el HTML trae los marcadores globales viejos,
    # se inyectan todos los bloques ahi (un solo bloque por tarjeta
    # sigue valiendo, solo cambia donde van).
    if ('<!-- MOMIOS-INICIO -->' in html_texto
            and '<!-- MOMIOS-FIN -->' in html_texto
            and not any(marcadores(k)[0] in html_texto
                        for k in bloques)):
        frag = "\n\n".join(bloques.values())
        antes = html_texto.split('<!-- MOMIOS-INICIO -->')[0]
        despues = html_texto.split('<!-- MOMIOS-FIN -->', 1)[1]
        nuevo = (antes + '<!-- MOMIOS-INICIO -->\n' + frag +
                 '\n<!-- MOMIOS-FIN -->' + despues)
    else:
        try:
            nuevo = inyectar(html_texto, bloques)
        except ValueError as e:
            print(f"ERROR: {e}")
            sys.exit(1)
    if not args.apply:
        print("DRY-RUN: no se escribio nada. "
              f"{len(bloques)} bloques listos para inyectar.")
        print("Ejemplo (primer partido):")
        print(list(bloques.values())[0])
        print(f"\nUsa --apply --out {args.html} para escribir de verdad.")
        return
    salida = args.out or args.html
    open(salida, 'w').write(nuevo)
    print(f"OK - fragmento inyectado en {salida} "
          f"({len(bloques)} partidos, marcadores por tarjeta).")


if __name__ == '__main__':
    main()
