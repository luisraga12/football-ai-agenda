"""Calcula las tendencias por mercado de una semana (Football AI Agenda).

Por cada partido del ev.json de la semana, calcula la racha de cada
equipo en cada mercado usando sus ultimos partidos de la misma
competicion (los de data/semana-N/raw/teams_last5.json, generados por
recolectar_datos.py; la misma ventana que el Poisson).

Definicion exacta de cada tendencia (documentada tambien en
scripts/README.md, punto 9):
  - Ventana: ultimos 5 partidos de liga por equipo (Semana 2 y 3);
    ultimos 4 partidos de la competicion en entre semana (solo hubo
    4 jornadas UEFA antes del corte). El `n` de cada equipo queda
    en el JSON; si un equipo tiene menos partidos, se cuenta con
    los que tiene y se dice.
  - 1X2: G/E/P de los ultimos n (victoria si gf > ga, empate si
    gf == ga, derrota si gf < ga).
  - Total: contra la LINEA PUBLICADA del partido
    (ev.json, mercados.total.linea). Mas = total de goles > linea;
    Menos = total < linea; Empuje = total == linea (se cuenta
    aparte, no suma a Mas ni a Menos). Si el partido sigue
    pendiente sin linea publicada, linea de referencia 2.5
    (queda marcado en el JSON como linea_referencia).
  - BTTS: si = el equipo marco y encajo en el partido
    (gf > 0 y ga > 0); no en caso contrario. OJO: es un conteo de
    resultados, NO son momios: ESPN no da momios de BTTS y aqui no
    se usa ninguno.
  - Spread: se aplica la LINEA DE SPREAD PUBLICADA del partido
    (mercados.spread.momios.home_linea / away_linea) a los ultimos
    n del equipo: cubre si (gf - ga) + linea > 0, empuje si == 0,
    no cubre si < 0. LIMITACION: la linea se aplica a los ultimos
    n sin distinguir si en esos partidos el equipo fue local o
    visita. Si el partido no trae linea de spread, no hay tendencia
    de spread (no se inventa).

Salida: data/semana-N/tendencias.json con un `linea_tarjeta` por
partido (una linea por tarjeta) y el detalle por equipo. Si un
equipo no esta en teams_last5.json, queda como "sin_datos" (sin
inventar numeros).

Uso:
    python3 scripts/calcular_tendencias.py --ev data/semana-2/ev.json \\
        --teams-last5 data/semana-2/raw/teams_last5.json \\
        --salida data/semana-2/tendencias.json
    python3 scripts/run_tendencias.py   (las 3 semanas con datos)
"""

import argparse
import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slug(nombre):
    return (nombre.lower().replace(' ', '-').replace('á', 'a')
            .replace('é', 'e').replace('í', 'i').replace('ó', 'o')
            .replace('ö', 'o').replace('ü', 'u').replace('ä', 'a')
            .replace('ú', 'u'))


def fmt_linea(valor):
    return ('%.1f' % valor).rstrip('0').rstrip('.')


def tendencia_equipo(matches, linea_total, linea_spread):
    """Racha de UN equipo en sus ultimos n partidos.

    matches: lista de {gf, ga} (la de teams_last5.json).
    linea_total: linea publicada del partido (o 2.5 de referencia).
    linea_spread: linea de spread publicada para ESTE equipo, o None.
    """
    n = len(matches)
    g = e = p = 0
    mas = menos = empuje = 0
    btts_si = btts_no = 0
    cubre = no_cubre = empuje_sp = 0
    for m in matches:
        gf, ga = float(m['gf']), float(m['ga'])
        if gf > ga:
            g += 1
        elif gf == ga:
            e += 1
        else:
            p += 1
        total = gf + ga
        if total > linea_total:
            mas += 1
        elif total < linea_total:
            menos += 1
        else:
            empuje += 1
        if gf > 0 and ga > 0:
            btts_si += 1
        else:
            btts_no += 1
        if linea_spread is not None:
            margen = (gf - ga) + linea_spread
            if margen > 0:
                cubre += 1
            elif margen < 0:
                no_cubre += 1
            else:
                empuje_sp += 1
    return {
        'n': n, 'g': g, 'e': e, 'p': p,
        'mas': mas, 'menos': menos, 'empuje': empuje,
        'btts_si': btts_si, 'btts_no': btts_no,
        'spread_linea': linea_spread,
        'cubre': cubre, 'no_cubre': no_cubre,
        'empuje_spread': empuje_sp,
    }


def texto_equipo(nombre, t):
    """Texto de la racha de UN equipo para la linea de la tarjeta."""
    if t is None:
        return f"{nombre}: sin datos"
    n = t['n']
    partes = [f"{nombre} {t['g']}G-{t['e']}E-{t['p']}P"]
    linea = t.get('linea_total')
    partes.append(f"Más {fmt_linea(linea)} {t['mas']}/{n}")
    partes.append(f"Menos {fmt_linea(linea)} {t['menos']}/{n}")
    if t['empuje']:
        partes[-1] += f" ({t['empuje']} empuje)"
    partes.append(f"BTTS {t['btts_si']}/{n}")
    if t.get('spread_linea') is not None:
        sl = t['spread_linea']
        signo = '+' if sl > 0 else ''
        partes.append(f"Cubre {signo}{fmt_linea(sl)} {t['cubre']}/{n}")
        if t['empuje_spread']:
            partes[-1] += f" ({t['empuje_spread']} empuje)"
    return ' · '.join(partes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ev', required=True,
                    help='ev.json de la semana')
    ap.add_argument('--teams-last5', required=True,
                    help='raw/teams_last5.json de la semana')
    ap.add_argument('--salida', required=True,
                    help='tendencias.json a escribir')
    ap.add_argument('--fecha', default=None,
                    help='fecha de calculo (por defecto hoy)')
    args = ap.parse_args()

    ev = json.load(open(args.ev))
    teams = json.load(open(args.teams_last5))
    semana = ev.get('semana', os.path.basename(
        os.path.dirname(args.ev)))
    partidos = ev['partidos']
    # Ventana: la misma del Poisson (n de cada equipo; entre semana
    # son 4 jornadas UEFA, las ligas 5 partidos).
    ventana_n = sorted({v['n'] for v in teams.values()}) if teams else []
    ventana = (f"últimos {ventana_n[0]} partidos de la competición"
               if len(ventana_n) == 1
               else f"últimos partidos de la competición {ventana_n}")

    out_partidos = []
    sin_datos = 0
    for p in partidos:
        mercados = p.get('mercados') or {}
        total = mercados.get('total') or {}
        linea_total = total.get('linea')
        linea_referencia = False
        if linea_total is None:
            # Partido pendiente sin linea publicada: referencia 2.5.
            linea_total = 2.5
            linea_referencia = True
        spread = mercados.get('spread') or {}
        momios_sp = spread.get('momios') or {}
        linea_local = momios_sp.get('home_linea')
        linea_visita = momios_sp.get('away_linea')

        entrada = {
            'slug': slug(f"{p['home']}-vs-{p['away']}"),
            'home': p['home'], 'away': p['away'],
            'fecha': p.get('fecha'), 'hora': p.get('hora'),
            'liga': p.get('liga'), 'estado': p.get('estado'),
            'linea_total': linea_total,
            'linea_referencia': linea_referencia,
        }
        for lado, nombre, linea_sp in (
                ('local', p['home'], linea_local),
                ('visita', p['away'], linea_visita)):
            equipo = teams.get(nombre)
            if equipo is None:
                entrada[lado] = None
                sin_datos += 1
                continue
            t = tendencia_equipo(equipo['matches'], linea_total,
                                 linea_sp)
            t['linea_total'] = linea_total
            entrada[lado] = t
        entrada['linea_tarjeta'] = (
            'Tendencias: '
            + texto_equipo(p['home'], entrada['local'])
            + ' — '
            + texto_equipo(p['away'], entrada['visita']))
        out_partidos.append(entrada)

    out = {
        'semana': semana,
        'ventana': ventana,
        'fecha_calculo': args.fecha or date.today().isoformat(),
        'partidos': out_partidos,
    }
    with open(args.salida, 'w') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"OK - tendencias de {semana}: {len(out_partidos)} partidos, "
          f"ventana {ventana}, {sin_datos} equipo(s) sin datos, "
          f"escrito en {args.salida}")


if __name__ == '__main__':
    main()
