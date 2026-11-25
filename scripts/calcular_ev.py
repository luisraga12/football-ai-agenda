"""Calcula el valor esperado (EV) de una semana (Football AI Agenda).

Lee data/semana-N/raw/poisson_result.json (xG y probabilidades Poisson)
y data/semana-N/raw/momios.json (momios de ESPN, ver
recolectar_momios.py), y escribe:
  - data/semana-N/raw/ev_result.json (detalle por mercado)
  - data/semana-N/ev.json (compacto, para integrar en la pagina)
  - data/semana-N/tabla-momios-semana-N.md (tabla legible)

EV = probabilidad x momio decimal - 1, por mercado.

Reglas (orden del jefe, 22 nov 2026):
  - El P(over) se calcula para LA LINEA PUBLICADA (2.5 o 3.5) desde los
    xG con la distribucion completa (p_over en poisson_core.py). NO se
    usa el P(+2.5) con momios de linea 3.5.
  - El spread usa p_spread_cover (distribucion completa). P(visitante
    cubre) = 1 - P(local cubre).
  - Semaforo por mejor pick: verde EV >= +5%, amarillo 0-5%, rojo < 0%.
  - Mejor pick = el mercado con mayor EV de la tarjeta.
  - Si un partido no tiene momio ("pendiente"), NO se le inventa EV:
    queda pendiente, sin semaforo.
  - BTTS (orden del jefe, 24 nov 2026): probabilidad Poisson completa
    (match_probs en poisson_core.py, grid 0-20) para TODOS los partidos,
    con momio o sin el, en mercados['btts'] con p_btts y p_no_btts.
    ESPN/DraftKings no trae momio de BTTS en esta fuente (verificado en
    los scoreboards crudos: solo moneyline, total y pointSpread), asi
    que momios y EV quedan en None y el BTTS no entra al mejor pick.

Uso:
    python3 scripts/calcular_ev.py --config scripts/config/semana-2.json
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from poisson_core import p_over, p_spread_cover  # noqa: E402


def semaforo(ev):
    if ev is None:
        return None
    if ev >= 0.05:
        return 'verde'
    if ev >= 0.0:
        return 'amarillo'
    return 'rojo'


def ev(prob_pct, decimal):
    if prob_pct is None or decimal is None:
        return None
    return prob_pct / 100.0 * decimal - 1


def fmt_pct(valor):
    if valor is None:
        return '—'
    return f"{valor * 100:+.1f}%"


def fmt_dec(valor):
    if valor is None:
        return '—'
    return f"{valor:.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    semana = cfg['semana']
    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')

    res = json.load(open(os.path.join(rawdir, 'poisson_result.json')))
    momios = json.load(open(os.path.join(rawdir, 'momios.json')))
    xg_por_partido = {(r['home'], r['away']): r for r in res['matches']}
    DIAS = {'2026-11-24': '11/24 nov', '2026-11-25': '11/25 nov',
            '2026-11-26': '11/26 nov', '2026-11-27': '11/27 nov',
            '2026-11-28': '11/28 nov',
            '2026-11-29': '11/29 nov', '2026-12-04': '12/04 dic',
            '2026-12-05': '12/05 dic', '2026-12-06': '12/06 dic'}

    filas = []
    for m in momios['partidos']:
        home, away = m['home'], m['away']
        r = xg_por_partido[(home, away)]
        fila = {'fecha': m['fecha'], 'fecha_txt': DIAS.get(m['fecha'], m['fecha']),
                'hora': m['fecha_cst'][11:], 'liga': m['liga_nombre'],
                'home': home, 'away': away, 'proveedor': m['proveedor'],
                'estado': m['estado'],
                # Estado real del partido en ESPN y marcador final (si lo
                # hay): un partido terminado sin momio sigue siendo
                # 'pendiente' en momios/EV, pero ya no se muestra como
                # si no se hubiera jugado. El marcador viene solo de
                # ESPN (recolectar_momios.py); nunca se inventa.
                'estado_partido': m.get('estado_partido', 'pre'),
                'marcador': m.get('marcador'),
                'mercados': {}, 'mejor_pick': None,
                'mejor_ev': None, 'semaforo': None}
        # BTTS para TODOS los partidos (orden del jefe, 24 nov 2026):
        # la probabilidad ya la calcula el Poisson (r['btts'], distribucion
        # completa); va en mercados aunque el partido este pendiente, para
        # que la pagina la muestre en vez de "pendiente". Sin momio ni EV:
        # ESPN/DraftKings no trae ese momio en esta fuente.
        fila['mercados']['btts'] = {
            'p_btts': r['btts'], 'p_no_btts': 100 - r['btts'],
            'momios': None, 'ev': {'si': None, 'no': None}}
        if m['estado'] != 'con_momio':
            filas.append(fila)
            print(f"PENDIENTE {home} vs {away}: sin momio, sin EV.")
            continue
        mm = m['momios']
        candidatos = []  # (nombre, ev)
        # 1X2 (blindaje, jefe 22 nov: un partido puede traer total/spread
        # pero no moneyline; en ese caso no se calcula 1X2, no se rompe).
        ml = mm['moneyline']
        if ml is not None:
            evs_1x2 = {'1': ev(r['p1'], ml['home']),
                       'X': ev(r['px'], ml['draw']),
                       '2': ev(r['p2'], ml['away'])}
            fila['mercados']['1X2'] = {'momios': ml, 'ev': evs_1x2}
            candidatos += [('Local', evs_1x2['1']), ('Empate', evs_1x2['X']),
                           ('Visita', evs_1x2['2'])]
        else:
            print(f"AVISO {home} vs {away}: trae total/spread pero no "
                  "moneyline; el 1X2 no lleva EV.")
        # Total: P(over) para la linea publicada
        tot = mm['total']
        if tot:
            p_over_linea = p_over(r['xgh'], r['xga'], tot['linea'])
            ev_mas = ev(p_over_linea, tot['over'])
            ev_menos = ev(100 - p_over_linea, tot['under'])
            fila['mercados']['total'] = {
                'linea': tot['linea'], 'momios': tot,
                'p_over': p_over_linea,
                'ev': {'mas': ev_mas, 'menos': ev_menos}}
            linea_txt = ('%.1f' % tot['linea']).rstrip('0').rstrip('.')
            candidatos += [(f"Más {linea_txt}", ev_mas),
                           (f"Menos {linea_txt}", ev_menos)]
        # Spread
        spr = mm['spread']
        if spr:
            p_cubre_local = p_spread_cover(r['xgh'], r['xga'],
                                           spr['home_linea'])
            ev_spr_local = ev(p_cubre_local, spr['home'])
            ev_spr_away = ev(100 - p_cubre_local, spr['away'])
            fila['mercados']['spread'] = {
                'home_linea': spr['home_linea'], 'momios': spr,
                'p_cubre_local': p_cubre_local,
                'ev': {'local': ev_spr_local, 'visitante': ev_spr_away}}
            candidatos += [(f"Spread local {spr['home_linea']:+.1f}",
                            ev_spr_local),
                           (f"Spread visitante {spr['away_linea']:+.1f}",
                            ev_spr_away)]
        if not candidatos:
            # No hay ningun mercado con EV (no deberia pasar: el momio
            # solo es "con_momio" si trae al menos un mercado). Se deja
            # sin mejor pick ni semaforo para que la validacion lo marque,
            # en vez de inventar un EV.
            print(f"AVISO {home} vs {away}: con momio pero sin ningun "
                  "mercado con EV; queda sin semaforo.")
            filas.append(fila)
            continue
        mejor_nombre, mejor_ev = max(candidatos, key=lambda c: c[1])
        fila['mejor_pick'] = mejor_nombre
        fila['mejor_ev'] = mejor_ev
        # Decimal y probabilidad del mejor pick (para el boton de parlay
        # del fragmento: data-odds / data-prob). Se resuelven desde los
        # mercados ya calculados, no se inventan.
        if mejor_nombre == 'Local':
            fila['mejor_decimal'] = ml['home'] if ml is not None else None
            fila['mejor_prob'] = r['p1']
        elif mejor_nombre == 'Empate':
            fila['mejor_decimal'] = ml['draw'] if ml is not None else None
            fila['mejor_prob'] = r['px']
        elif mejor_nombre == 'Visita':
            fila['mejor_decimal'] = ml['away'] if ml is not None else None
            fila['mejor_prob'] = r['p2']
        elif mejor_nombre.startswith('Más '):
            # Aqui tot es el total crudo {linea, over, under}, sin 'momios'.
            fila['mejor_decimal'] = tot['over'] if tot else None
            fila['mejor_prob'] = (fila['mercados']['total']['p_over']
                                  if tot else None)
        elif mejor_nombre.startswith('Menos '):
            fila['mejor_decimal'] = tot['under'] if tot else None
            fila['mejor_prob'] = (100 - fila['mercados']['total']['p_over']
                                  if tot else None)
        elif mejor_nombre.startswith('Spread local '):
            # Aqui spr es el spread crudo {home_linea, home, ...}.
            fila['mejor_decimal'] = spr['home'] if spr else None
            fila['mejor_prob'] = (fila['mercados']['spread']['p_cubre_local']
                                  if spr else None)
        elif mejor_nombre.startswith('Spread visitante '):
            fila['mejor_decimal'] = spr['away'] if spr else None
            fila['mejor_prob'] = (100 - fila['mercados']['spread']
                                  ['p_cubre_local'] if spr else None)
        else:
            fila['mejor_decimal'] = None
            fila['mejor_prob'] = None
        fila['semaforo'] = semaforo(mejor_ev)
        icono = {'verde': '🟢', 'amarillo': '🟡', 'rojo': '🔴'}[fila['semaforo']]
        print(f"{icono} {home} vs {away}: mejor pick {mejor_nombre} "
              f"{mejor_ev * 100:+.1f}% ({fila['semaforo']})")
        filas.append(fila)

    json.dump({'semana': semana, 'partidos': filas},
              open(os.path.join(rawdir, 'ev_result.json'), 'w'),
              indent=1, ensure_ascii=False)
    # ev.json compacto para la pagina (ver integrar_pagina.py). Desde la
    # revision del lunes 23 nov incluye 'mercados' (EV por mercado) y el
    # decimal/probabilidad del mejor pick, para que el fragmento de
    # integracion no tenga que leer raw/ev_result.json.
    compacto = {'semana': semana, 'partidos': [
        {'home': f['home'], 'away': f['away'], 'fecha': f['fecha'],
         'hora': f['hora'], 'liga': f['liga'],
         'proveedor': f['proveedor'], 'estado': f['estado'],
         'estado_partido': f['estado_partido'],
         'marcador': f['marcador'],
         'mejor_pick': f['mejor_pick'], 'mejor_ev': f['mejor_ev'],
         'mejor_decimal': f.get('mejor_decimal'),
         'mejor_prob': f.get('mejor_prob'),
         'semaforo': f['semaforo'], 'mercados': f['mercados'],
         'momios': (momios['partidos'][i]['momios']
                    if filas[i]['estado'] == 'con_momio' else None)}
        for i, f in enumerate(filas)]}
    json.dump(compacto, open(os.path.join(outdir, 'ev.json'), 'w'),
              indent=1, ensure_ascii=False)

    # ---- tabla .md ----
    L = []
    L.append(f"# Tabla de momios y valor esperado — {cfg['nombre']} "
             "(Football AI Agenda)")
    L.append("")
    L.append(f"**Partidos:** {cfg['fechas'][0]} al {cfg['fechas'][-1]}, "
             "horas de Monterrey (CST). **Fuente de momios:** ESPN (API "
             "pública sin clave), DraftKings salvo que se indique otro "
             "proveedor. **Fecha de consulta:** "
             f"{momios['fecha_consulta']}.")
    L.append("")
    L.append("**Método:** EV = probabilidad Poisson "
             f"(tabla-poisson-semana-{semana}.md) × momio decimal − 1. "
             "Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea "
             "del total varía por partido (la publicada por DraftKings: "
             "2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los "
             "xG. BTTS: probabilidad Poisson completa (ambos anotan); no "
             "lleva EV porque ESPN/DraftKings no trae momio de BTTS en "
             "esta fuente.")
    L.append("")
    L.append("| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | "
             "EV Más / Menos | Spread (línea local) | EV Spread local / "
             "visitante | P(BTTS) | Mejor pick | EV | Semáforo |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for f in filas:
        if f['estado'] != 'con_momio':
            btts_p = f['mercados']['btts']['p_btts']
            if f.get('estado_partido') == 'post' and f.get('marcador'):
                marc = f['marcador']
                partido_txt = (f"{f['home']} vs {f['away']} "
                               f"(Final {marc['local']}–{marc['visita']})")
                estado_txt = '🏁 Terminado sin momio'
            else:
                partido_txt = f"{f['home']} vs {f['away']}"
                estado_txt = '⏳ Pendiente'
            L.append(f"| {f['fecha_txt']} | {partido_txt} | "
                     "pendiente | — | — | — | — | — | "
                     f"{btts_p:.1f}% | — | — | {estado_txt} |")
            continue
        m1x2 = f['mercados'].get('1X2')
        if m1x2 is not None:
            ml = m1x2['momios']
            evs = m1x2['ev']
            ml_txt = (f"{fmt_dec(ml['home'])} / {fmt_dec(ml['draw'])} / "
                      f"{fmt_dec(ml['away'])}")
            ml_ev = (f"{fmt_pct(evs['1'])} / {fmt_pct(evs['X'])} / "
                     f"{fmt_pct(evs['2'])}")
        else:
            ml_txt = '—'
            ml_ev = '—'
        tot = f['mercados'].get('total')
        spr = f['mercados'].get('spread')
        prov = f" ({f['proveedor']})" if f['proveedor'] != 'DraftKings' \
            else ''
        tot_txt = (f"{tot['linea']:.1f} ({fmt_dec(tot['momios']['over'])} / "
                   f"{fmt_dec(tot['momios']['under'])})") if tot else '—'
        tot_ev = (f"{fmt_pct(tot['ev']['mas'])} / "
                  f"{fmt_pct(tot['ev']['menos'])}") if tot else '—'
        spr_txt = (f"{spr['home_linea']:+.1f} "
                   f"({fmt_dec(spr['momios']['home'])} / "
                   f"{fmt_dec(spr['momios']['away'])})") if spr else '—'
        spr_ev = (f"{fmt_pct(spr['ev']['local'])} / "
                  f"{fmt_pct(spr['ev']['visitante'])}") if spr else '—'
        icono = {'verde': '🟢 Verde', 'amarillo': '🟡 Amarillo',
                 'rojo': '🔴 Rojo'}[f['semaforo']]
        btts_txt = f"{f['mercados']['btts']['p_btts']:.1f}%"
        L.append(f"| {f['fecha_txt']} | {f['home']} vs {f['away']}{prov} | "
                 f"{ml_txt} | {ml_ev} | {tot_txt} | "
                 f"{tot_ev} | {spr_txt} | {spr_ev} | {btts_txt} | "
                 f"{f['mejor_pick']} | "
                 f"{fmt_pct(f['mejor_ev'])} | {icono} |")
    n_verde = sum(1 for f in filas if f['semaforo'] == 'verde')
    n_amar = sum(1 for f in filas if f['semaforo'] == 'amarillo')
    n_rojo = sum(1 for f in filas if f['semaforo'] == 'rojo')
    n_pend = sum(1 for f in filas if f['estado'] != 'con_momio'
                 and f.get('estado_partido') != 'post')
    n_post_sin_momio = sum(1 for f in filas
                           if f['estado'] != 'con_momio'
                           and f.get('estado_partido') == 'post')
    L.append("")
    L.append(f"**Resumen:** {n_verde} verdes, {n_amar} amarillos, "
             f"{n_rojo} rojos, {n_pend} pendientes, "
             f"{n_post_sin_momio} terminados sin momio.")
    peores = [f for f in filas if f['semaforo'] == 'rojo']
    if peores:
        L.append("Único(s) sin valor: " + ", ".join(
            f"{f['home']}–{f['away']} (mejor EV "
            f"{fmt_pct(f['mejor_ev'])}, {f['mejor_pick']})" for f in peores)
            + ".")
    L.append("")
    L.append("**Advertencia:** el modelo Poisson usa solo los últimos "
             "partidos por equipo y puede exagerar rachas; los EV extremos "
             "reflejan desacuerdo fuerte entre el modelo y el mercado, "
             "no una certeza.")
    L.append("")
    out = os.path.join(outdir, f"tabla-momios-semana-{semana}.md")
    open(out, 'w').write("\n".join(L))
    print(f"\nOK - {n_verde} verdes, {n_amar} amarillos, {n_rojo} rojos, "
          f"{n_pend} pendientes, {n_post_sin_momio} terminados sin momio. "
          f"Escrito {out} y {outdir}/ev.json")


if __name__ == '__main__':
    main()
