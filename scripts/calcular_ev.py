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
  Con momio BSD (llave 'bsd' en momios.json con btts {yes, no} decimales,
  consenso BSD), los momios y el EV si se llenan: ev.si = p_btts x momio_si - 1
  y ev.no = p_no_btts x momio_no - 1; sin esa llave, quedan en None.
  Hándicap asiático BSD (E1, 28 nov 2026; ejemplo del jefe: Hamburg/empate):
  con la llave 'bsd' en momios.json con asian_handicap {line, home, away}
  (consenso BSD), se publica mercados['asian_handicap'] con la probabilidad
  de cubrir (p_spread_cover, la línea es del local; las líneas son .5, sin
  push) y el EV por lado; el AH sí entra al mejor pick.
  Calibración (E1, 28 nov 2026; diseño en
  ~/workspace/e1-calibracion/CALIBRACION-2026-11-28.md): el modelo Poisson
  es muy sobreconfiado — en 61 partidos terminados (semana 1 + 2) dice
  78.9% de probabilidad media en su recomendación y acierta 37.8%; Brier
  1X2 0.783. Las probabilidades se encogen hacia las tasas base reales
  (ALFA_CAL = 0.35 de modelo + 0.65 de tasa base) antes de calcular el EV:
  1X2 hacia (42.6, 31.1, 26.2), Más 2.5 hacia 58.3%, BTTS hacia 55.7%,
  spread local hacia 38.6% y AH local hacia 36.4%. El total solo se calibra
  con línea 2.5 (la base medida); otras líneas quedan crudas. La
  probabilidad cruda se guarda en prob_cruda para diagnóstico y reajuste.
  Brier con calibración (validación cruzada entre semanas): 1X2 0.657,
  binarios 0.24-0.27. Reajustar ALFA y las bases cada semana con los
  partidos nuevos; no fijarlas para siempre.

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


# ---- Calibración (E1, 28 nov 2026) ----
# El modelo Poisson es sobreconfiado: encoger cada probabilidad hacia su
# tasa base real antes de calcular el EV. ALFA_CAL = peso del modelo.
ALFA_CAL = 0.35
BASE_1X2 = (42.6, 31.1, 26.2)  # local, empate, visita (61 partidos)
BASE_OVER25 = 58.3
BASE_BTTS = 55.7
BASE_SPREAD = 38.6  # cubre el local, promedio global de líneas (n=44)
BASE_AH = 36.4  # cubre el local, promedio global de líneas (n=44)


def cal(prob_pct, base_pct):
    """Encoge una probabilidad (%) hacia su tasa base (%)."""
    if prob_pct is None:
        return None
    return ALFA_CAL * prob_pct + (1 - ALFA_CAL) * base_pct


def cal_1x2(p1, px, p2):
    """Encoge el triplete 1X2 hacia BASE_1X2 y renormaliza a 100."""
    q = [cal(p1, BASE_1X2[0]), cal(px, BASE_1X2[1]), cal(p2, BASE_1X2[2])]
    s = sum(q)
    return [x / s * 100 for x in q]


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
        # Probabilidades CALIBRADAS (ver docstring): se usan en todos los
        # mercados y en el EV; la cruda queda en prob_cruda para diagnóstico.
        p1c, pxc, p2c = cal_1x2(r['p1'], r['px'], r['p2'])
        bttsc = cal(r['btts'], BASE_BTTS)
        over25c = cal(r['over25'], BASE_OVER25)
        fila = {'fecha': m['fecha'], 'fecha_txt': DIAS.get(m['fecha'], m['fecha']),
                'hora': m['fecha_cst'][11:], 'liga': m['liga_nombre'],
                'home': home, 'away': away, 'proveedor': m['proveedor'],
                'estado': m['estado'],
                'prob_cruda': {'1': r['p1'], 'X': r['px'], '2': r['p2'],
                               'over25': r['over25'], 'btts': r['btts']},
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
        # ESPN/DraftKings no trae ese momio en esta fuente (salvo momio BSD: ver bloque siguiente).
        fila['mercados']['btts'] = {
            'p_btts': bttsc, 'p_no_btts': 100 - bttsc,
            'momios': None, 'ev': {'si': None, 'no': None}}
        # BTTS con momio BSD (octava ronda, lado E1): si momios.json
        # trae la llave 'bsd' con btts {yes, no} decimales (consenso
        # BSD, scripts/recolectar_momios.py), se llenan los momios y
        # el EV con la formula del jefe: ev.si = p_btts x momio_si - 1
        # y ev.no = p_no_btts x momio_no - 1 (reusa ev(), que ya hace
        # prob_pct / 100 * decimal - 1). Sin llave bsd, sin btts en
        # ella, o sin los dos decimales, momios y EV quedan en None:
        # nada inventado. El BTTS sigue sin entrar al mejor pick.
        bsd = m.get('bsd') if isinstance(m, dict) else None
        btts_bsd = bsd.get('btts') if isinstance(bsd, dict) else None
        if isinstance(btts_bsd, dict):
            momio_si = btts_bsd.get('yes')
            momio_no = btts_bsd.get('no')
            if momio_si is not None and momio_no is not None:
                fila['mercados']['btts']['momios'] = {
                    'si': float(momio_si), 'no': float(momio_no)}
                fila['mercados']['btts']['ev'] = {
                    'si': ev(bttsc, float(momio_si)),
                    'no': ev(100 - bttsc, float(momio_no))}
        # Hándicap asiático con momio BSD (E1, 28 nov 2026; ejemplo del
        # jefe: Hamburg/empate, local +1.5 cubre ganar, empatar y perder
        # por 1): si momios.json trae la llave 'bsd' con asian_handicap
        # {line, home, away} (consenso BSD, scripts/recolectar_momios.py),
        # se publica en mercados con la probabilidad de cubrir
        # (p_spread_cover: la línea es del local; las líneas son .5, sin
        # push) y el EV por lado. Sin llave bsd, sin asian_handicap, sin
        # los dos momios, o con línea no .5, no se publica nada: nada
        # inventado. El AH sí entra al mejor pick (ver bloque con_momio).
        ah_bsd = bsd.get('asian_handicap') if isinstance(bsd, dict) else None
        if isinstance(ah_bsd, dict):
            linea_ah = ah_bsd.get('line')
            momio_ah_local = ah_bsd.get('home')
            momio_ah_visitante = ah_bsd.get('away')
            es_media = (isinstance(linea_ah, (int, float))
                        and abs(linea_ah * 2 - round(linea_ah * 2)) < 1e-9
                        and round(linea_ah * 2) % 2 != 0)
            if (es_media and momio_ah_local is not None
                    and momio_ah_visitante is not None):
                p_cubre_ah = cal(p_spread_cover(r['xgh'], r['xga'], linea_ah),
                                 BASE_AH)
                fila['mercados']['asian_handicap'] = {
                    'linea': linea_ah,
                    'momios': {'local': float(momio_ah_local),
                               'visitante': float(momio_ah_visitante)},
                    'p_cubre_local': p_cubre_ah,
                    'ev': {'local': ev(p_cubre_ah, float(momio_ah_local)),
                           'visitante': ev(100 - p_cubre_ah,
                                           float(momio_ah_visitante))}}
            else:
                print(f"AVISO {home} vs {away}: AH BSD sin línea .5 o sin "
                      "momios; no se publica.")
        if m['estado'] != 'con_momio':
            # 1X2 y total del MODELO solo para los partidos sin momio
            # (orden del jefe, 25 nov 2026; mismo precedente que
            # BTTS): las probabilidades ya las calcula el Poisson
            # (r['p1'/'px'/'p2'] y r['over25'] para la linea 2.5) y
            # van en mercados aunque no haya momio, para que la
            # pagina muestre las probabilidades del modelo en vez
            # de "1X2: pendiente" / "Total: pendiente". Sin momio
            # ni EV: no hay con que calcularlos y no se inventan.
            # Un partido terminado sin momio sigue sin EV ni
            # semaforo; solo deja de verse como si no se hubiera
            # jugado. (Solo aqui: con momio, los mercados 1X2/total
            # los escribe el bloque de abajo con momios y EV, y la
            # tabla .md supone momios dict; no se toca ese camino.)
            fila['mercados']['1X2'] = {
                'prob': {'1': p1c, 'X': pxc, '2': p2c},
                'momios': None, 'ev': None}
            fila['mercados']['total'] = {
                'linea': 2.5, 'p_over': over25c,
                'momios': None, 'ev': None}
            filas.append(fila)
            print(f"PENDIENTE {home} vs {away}: sin momio, sin EV.")
            continue
        mm = m['momios']
        candidatos = []  # (nombre, ev)
        # 1X2 (blindaje, jefe 22 nov: un partido puede traer total/spread
        # pero no moneyline; en ese caso no se calcula 1X2, no se rompe).
        ml = mm['moneyline']
        if ml is not None:
            evs_1x2 = {'1': ev(p1c, ml['home']),
                       'X': ev(pxc, ml['draw']),
                       '2': ev(p2c, ml['away'])}
            fila['mercados']['1X2'] = {'momios': ml, 'ev': evs_1x2}
            candidatos += [('Local', evs_1x2['1']), ('Empate', evs_1x2['X']),
                           ('Visita', evs_1x2['2'])]
        else:
            print(f"AVISO {home} vs {away}: trae total/spread pero no "
                  "moneyline; el 1X2 no lleva EV.")
        # Total: P(over) para la linea publicada
        tot = mm['total']
        if tot:
            # Calibración solo con línea 2.5 (la base medida, 58.3%);
            # otras líneas quedan crudas (sin base medida para ellas).
            p_over_raw = p_over(r['xgh'], r['xga'], tot['linea'])
            p_over_linea = (cal(p_over_raw, BASE_OVER25)
                            if tot['linea'] == 2.5 else p_over_raw)
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
            p_cubre_local = cal(p_spread_cover(r['xgh'], r['xga'],
                                              spr['home_linea']),
                                BASE_SPREAD)
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
        # Hándicap asiático BSD: el pick "Hamburg/empate" (local +1.5)
        # cubre ganar, empatar y perder por 1. Entra a candidatos con
        # los mismos nombres que _candidatos/_evaluar_pick esperan
        # (generar_resultados.py).
        ah = fila['mercados'].get('asian_handicap')
        if isinstance(ah, dict) and isinstance(ah.get('ev'), dict):
            la = ah.get('linea')
            pc_ah = ah.get('p_cubre_local')
            if la is not None and pc_ah is not None:
                candidatos += [(f"AH local {la:+.1f}",
                                ah['ev']['local']),
                               (f"AH visitante {-la:+.1f}",
                                ah['ev']['visitante'])]
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
            fila['mejor_prob'] = p1c
        elif mejor_nombre == 'Empate':
            fila['mejor_decimal'] = ml['draw'] if ml is not None else None
            fila['mejor_prob'] = pxc
        elif mejor_nombre == 'Visita':
            fila['mejor_decimal'] = ml['away'] if ml is not None else None
            fila['mejor_prob'] = p2c
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
        elif mejor_nombre.startswith('AH local '):
            fila['mejor_decimal'] = (fila['mercados']['asian_handicap']
                                     ['momios']['local'])
            fila['mejor_prob'] = (fila['mercados']['asian_handicap']
                                  ['p_cubre_local'])
        elif mejor_nombre.startswith('AH visitante '):
            fila['mejor_decimal'] = (fila['mercados']['asian_handicap']
                                     ['momios']['visitante'])
            fila['mejor_prob'] = (100 - fila['mercados']['asian_handicap']
                                  ['p_cubre_local'])
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
         'prob_cruda': f.get('prob_cruda'),
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
             "Probabilidades calibradas (28 nov 2026): se encogen hacia las "
             "tasas base reales (α=0.35) antes de calcular el EV; la "
             "probabilidad cruda queda en prob_cruda de ev.json. "
             "Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea "
             "del total varía por partido (la publicada por DraftKings: "
             "2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los "
             "xG. BTTS: probabilidad Poisson completa (ambos anotan); el EV se "
             "calcula solo con momio BSD (llave 'bsd' en momios.json); sin esa "
             "llave no lleva EV porque ESPN/DraftKings no trae momio de BTTS en esta fuente.")
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
