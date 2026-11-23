"""Integra momios + EV en la pagina (Football AI Agenda) — PROPUESTA.

Mecanismo propuesto al jefe (22 nov 2026, sin tocar index.html por
cuenta propia): el workflow genera `data/semana-N/ev.json` y este
script inyecta un fragmento HTML con los momios, el EV y el semaforo
entre los marcadores `<!-- MOMIOS-INICIO -->` y `<!-- MOMIOS-FIN -->`
de la pagina.

Reglas de seguridad del script:
  - Por defecto es DRY-RUN: solo imprime lo que haria, no escribe nada.
  - Solo escribe con `--apply --html ARCHIVO --out ARCHIVO`.
  - Si el HTML no tiene los dos marcadores, FALLA SIN TOCAR NADA.
  - Nunca inventa momios: solo usa lo que trae ev.json; los partidos
    "pendiente" se muestran como "Momios pendientes".

Alternativa (Semana 7, para decidir con el jefe): que `index.html`
lea `data/semana-N/ev.json` con `fetch()` en el navegador. Eso cambia
la arquitectura actual (hoy la pagina lleva los datos integrados, no
lee JSON), asi que queda como opcion, no se implementa aqui.

Uso:
    python3 scripts/integrar_pagina.py --ev data/semana-2/ev.json --html index.html
    python3 scripts/integrar_pagina.py --ev data/semana-2/ev.json --html index.html --out index.html --apply
"""

import argparse
import json
import sys

INICIO = "<!-- MOMIOS-INICIO -->"
FIN = "<!-- MOMIOS-FIN -->"


def fragmento(ev):
    """Genera el fragmento HTML con momios + EV de una semana."""
    partes = []
    for p in ev['partidos']:
        if p['estado'] != 'con_momio':
            partes.append(
                f'<div class="momios" data-partido="{p["home"]} vs {p["away"]}">'
                f'<span class="momios-estado">Momios pendientes</span></div>')
            continue
        color = {'verde': 'verde', 'amarillo': 'amarillo',
                 'rojo': 'rojo'}[p['semaforo']]
        partes.append(
            f'<div class="momios" data-partido="{p["home"]} vs {p["away"]}">'
            f'<span class="semaforo semaforo-{color}">{p["semaforo"]}</span> '
            f'<span class="mejor-pick">{p["mejor_pick"]}</span> '
            f'<span class="mejor-ev">{p["mejor_ev"] * 100:+.1f}% EV</span>'
            f'</div>')
    return "\n".join(partes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ev', required=True, help='data/semana-N/ev.json')
    ap.add_argument('--html', required=True, help='HTML a parchear')
    ap.add_argument('--out', default=None, help='HTML de salida')
    ap.add_argument('--apply', action='store_true',
                    help='escribir de verdad (sin esto es dry-run)')
    args = ap.parse_args()

    ev = json.load(open(args.ev))
    html = open(args.html).read()
    if INICIO not in html or FIN not in html:
        print(f"ERROR: {args.html} no tiene los marcadores "
              f"{INICIO} / {FIN}. No se toco nada.")
        sys.exit(1)
    frag = fragmento(ev)
    antes = html.split(INICIO)[0]
    despues = html.split(FIN, 1)[1]
    nuevo = antes + INICIO + "\n" + frag + "\n" + FIN + despues
    if not args.apply:
        print("DRY-RUN: no se escribio nada. Fragmento que se inyectaria:")
        print(frag[:2000])
        print(f"\nUsa --apply --out {args.html} para escribir de verdad.")
        return
    salida = args.out or args.html
    open(salida, 'w').write(nuevo)
    print(f"OK - fragmento inyectado en {salida} "
          f"({len(ev['partidos'])} partidos).")


if __name__ == '__main__':
    main()
