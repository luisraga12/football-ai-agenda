"""Investigación Fuerza del XI (Semana 8, orden del jefe 23 nov 2026).

Prueba de concepto con datos reales de ESPN (API pública, sin clave):
  1. Últimos 5 partidos de liga de Arsenal (eng.1) y Real Madrid (esp.1),
     ya guardados en data/investigacion-xi/raw/ultimos_partidos.json.
  2. Por partido, el summary de ESPN da:
     - rosters[]: titulares (starter=true) + suplentes, con posición.
     - keyEvents Substitution: minuto y quién entra por quién.
     - resultado: puntos (3/1/0) para cada titular.
  3. El roster de temporada da por jugador: totalGoals, goalAssists,
     appearances, subIns (NO da minutos: se estiman del summary).
  4. Minutos estimados por partido: titular no sustituido = 90;
     titular sustituido al minuto M = M; suplente que entra al M = 90-M.

Fórmula propuesta (a validar por el jefe):
  Mejor XI de la temporada (ventana: últimos 5 de liga, como el Poisson
  del proyecto): 1 portero + 4 defensas + 4 medios + 2 delanteros con
  MÁS MINUTOS jugados en la ventana, por grupo de posición.
  Para un XI cualquiera:
    A = Σ(goles+asistencias de temporada del XI) / Σ(goles+asistencias
        del mejor XI) * 100
    B = Σ(minutos del XI en la ventana) / Σ(minutos del mejor XI) * 100
    C = Σ(puntos con el jugador en cancha) / Σ(puntos del mejor XI) * 100
  Fuerza = 0.40*A + 0.30*B + 0.30*C   (0-100)

Uso:
    python3 scripts/investigar_fuerza_xi.py
Guarda:
    data/investigacion-xi/fuerza_xi_prueba.json
    data/investigacion-xi/fuerza_xi_prueba.md
"""

import json
import os
import re
import urllib.request

BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"
OUT = "data/investigacion-xi"
RAW = os.path.join(OUT, "raw")


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def parse_substitutions(summary):
    """Devuelve {nombre_jugador: minuto_entrada} y {nombre: minuto_salida}."""
    entra, sale = {}, {}
    for k in summary.get('keyEvents', []):
        if k.get('type', {}).get('text') != 'Substitution':
            continue
        clock = k.get('clock', {}).get('displayValue', '')
        m = re.search(r"(\d+)", clock or '')
        if not m:
            continue
        minuto = int(m.group(1))
        text = k.get('text', '')
        # "Substitution, Arsenal. Noni Madueke replaces Bukayo Saka."
        mm = re.search(r"\.\s*(.+?)\s+replaces\s+(.+?)\.", text)
        if mm:
            entra[mm.group(1).strip()] = minuto
            sale[mm.group(2).strip()] = minuto
    return entra, sale


def minutes_for_player(starter, name, entra, sale):
    if starter:
        return sale.get(name, 90)
    return 90 - entra[name] if name in entra else 0


def norm_pos(summary_pos, roster_pos):
    """Normaliza la posición a G/D/M/F desde el summary o el roster."""
    name = (summary_pos or {}).get('name', '')
    abbr = (summary_pos or {}).get('abbreviation', '') or roster_pos or ''
    if 'Goalkeeper' in name or abbr == 'G':
        return 'G'
    if 'Defender' in name or abbr.startswith(('D', 'CD', 'LB', 'RB', 'WB')):
        return 'D'
    if 'Midfielder' in name or abbr.startswith(('M', 'CM', 'DM', 'AM', 'LM', 'RM')):
        return 'M'
    if 'Forward' in name or 'Striker' in name or 'Winger' in name \
            or abbr.startswith(('F', 'ST', 'CF', 'LW', 'RW')):
        return 'F'
    return roster_pos if roster_pos in ('G', 'D', 'M', 'F') else '?'


def team_result(summary, team_name):
    comp = summary['header']['competitions'][0]
    me = next(c for c in comp['competitors']
              if c['team']['displayName'] == team_name)
    other = next(c for c in comp['competitors']
                 if c['team']['displayName'] != team_name)
    gf = int(float(me['score']))
    ga = int(float(other['score']))
    pts = 3 if gf > ga else (1 if gf == ga else 0)
    return gf, ga, pts


def main():
    ultimos = json.load(open(os.path.join(RAW, "ultimos_partidos.json")))
    resultado = {}
    for team, liga, tid in (("Arsenal", "eng.1", 359),
                            ("Real Madrid", "esp.1", 86)):
        partidos = sorted(ultimos[team], key=lambda m: m['date'],
                          reverse=True)[:5]
        # --- stats de temporada por jugador (roster) ---
        roster = fetch(f"{BASE}/{liga}/teams/{tid}/roster")
        season = {}
        for a in roster['athletes']:
            cats = {}
            sp = (a.get('statistics') or {}).get('splits') or {}
            for c in sp.get('categories', []):
                for s in c.get('stats', []):
                    cats[s['name']] = s.get('value', 0)
            pos = (a.get('position') or {}).get('abbreviation', '?')
            season[a['displayName']] = {
                'pos': pos,
                'goles': cats.get('totalGoals', 0),
                'asistencias': cats.get('goalAssists', 0),
                'apariciones': cats.get('appearances', 0),
                'suplencias': cats.get('subIns', 0),
            }
        # --- últimos 5: titulares, minutos, puntos ---
        per_player = {}
        partidos_out = []
        for m in partidos:
            s = fetch(f"{BASE}/{liga}/summary?event={m['event_id']}")
            json.dump(s, open(os.path.join(
                RAW, f"summary_{liga}_{m['event_id']}.json"), "w"))
            ros = next(r for r in s['rosters']
                       if r['team']['displayName'] == team)
            entra, sale = parse_substitutions(s)
            gf, ga, pts = team_result(s, team)
            xi = []
            for x in ros['roster']:
                name = x['athlete']['displayName']
                if not x.get('starter'):
                    continue
                mins = minutes_for_player(True, name, entra, sale)
                pos = norm_pos(x.get('position'),
                               season.get(name, {}).get('pos', '?'))
                xi.append({'jugador': name, 'pos': pos, 'minutos': mins})
                mstats = {s['name']: s.get('value', 0)
                          for s in x.get('stats', [])}
                d = per_player.setdefault(name, {
                    'pos': pos, 'titularidades': 0, 'minutos': 0,
                    'puntos': 0,
                    'goles_ventana': 0, 'asist_ventana': 0,
                    'goles_temp': season.get(name, {}).get('goles', 0),
                    'asist_temp': season.get(name, {}).get('asistencias', 0),
                })
                d['titularidades'] += 1
                d['minutos'] += mins
                d['puntos'] += pts
                d['goles_ventana'] += mstats.get('totalGoals', 0)
                d['asist_ventana'] += mstats.get('goalAssists', 0)
            partidos_out.append({
                'fecha': m['date'][:10], 'partido': f"{m['home']} {m['score_home']}-{m['score_away']} {m['away']}",
                'puntos': pts, 'xi': xi,
            })
        # --- mejor XI por minutos, por grupo (1-4-4-2) ---
        grupos = {'G': 1, 'D': 4, 'M': 4, 'F': 2}
        mejor_xi = []
        for g, n in grupos.items():
            cands = sorted(
                ((nm, d) for nm, d in per_player.items() if d['pos'] == g),
                key=lambda kv: kv[1]['minutos'], reverse=True)[:n]
            mejor_xi += [{'jugador': nm, **d} for nm, d in cands]
        # Si falta alguien en un grupo (p.ej. pocos defensas), completar
        # con los de más minutos sin importar el grupo.
        if len(mejor_xi) < 11:
            resto = sorted(
                ((nm, d) for nm, d in per_player.items()
                 if nm not in {x['jugador'] for x in mejor_xi}),
                key=lambda kv: kv[1]['minutos'], reverse=True)
            for nm, d in resto[:11 - len(mejor_xi)]:
                mejor_xi.append({'jugador': nm, **d})

        def componentes(xi_nombres):
            # A usa goles+asistencias EN LA VENTANA (del summary por
            # partido), para que los 3 componentes midan lo mismo.
            ga = sum(per_player.get(n, {}).get('goles_ventana', 0)
                     + per_player.get(n, {}).get('asist_ventana', 0)
                     for n in xi_nombres)
            mins = sum(per_player.get(n, {}).get('minutos', 0)
                       for n in xi_nombres)
            pts = sum(per_player.get(n, {}).get('puntos', 0)
                      for n in xi_nombres)
            return ga, mins, pts

        best_n = [x['jugador'] for x in mejor_xi]
        b_ga, b_min, b_pts = componentes(best_n)

        def fuerza(xi_nombres):
            ga, mins, pts = componentes(xi_nombres)
            # Cada componente se topa en 100: el XI no puede ser más
            # fuerte que el mejor XI (si lo supera en bruto, es 100).
            A = min(100, 100 * ga / b_ga) if b_ga else 0
            B = min(100, 100 * mins / b_min) if b_min else 0
            C = min(100, 100 * pts / b_pts) if b_pts else 0
            return {'A_goles': round(A, 1), 'B_minutos': round(B, 1),
                    'C_puntos': round(C, 1),
                    'fuerza': round(0.40 * A + 0.30 * B + 0.30 * C, 1),
                    'goles_asist': ga, 'minutos': mins, 'puntos': pts}

        xi_reciente = [x['jugador'] for x in partidos_out[0]['xi']]
        # XI reciente sin el máximo goleador de la VENTANA del equipo
        top = max(per_player.items(),
                  key=lambda kv: kv[1]['goles_ventana']
                  + kv[1]['asist_ventana'])
        xi_sin_top = [n for n in xi_reciente if n != top[0]]
        # completar a 11 con el siguiente con más minutos fuera del XI
        # (sin volver a meter al jugador que acabamos de quitar)
        supl = sorted(
            ((nm, d) for nm, d in per_player.items()
             if nm not in xi_sin_top and nm != top[0]),
            key=lambda kv: kv[1]['minutos'], reverse=True)
        if supl:
            xi_sin_top.append(supl[0][0])

        resultado[team] = {
            'liga': liga,
            'ventana': 'últimos 5 de liga hasta 21 nov 2026',
            'partidos': partidos_out,
            'jugadores': per_player,
            'mejor_xi': mejor_xi,
            'mejor_xi_totales': {'goles_asist': b_ga, 'minutos': b_min,
                                 'puntos': b_pts},
            'xi_mas_reciente': {'fecha': partidos_out[0]['fecha'],
                                'xi': xi_reciente,
                                **fuerza(xi_reciente)},
            'xi_reciente_sin_top': {'sin': top[0],
                                    'xi': xi_sin_top,
                                    **fuerza(xi_sin_top)},
            'top_goles_ventana': {'jugador': top[0],
                                  'goles': top[1]['goles_ventana'],
                                  'asistencias': top[1]['asist_ventana']},
        }
        print(f"== {team}: mejor XI {len(mejor_xi)} jugadores, "
              f"totales G+A={b_ga} min={b_min} pts={b_pts}")
        print(f"   XI reciente ({partidos_out[0]['fecha']}): "
              f"{resultado[team]['xi_mas_reciente']}")
        print(f"   XI sin {top[0]}: "
              f"{resultado[team]['xi_reciente_sin_top']}")

    json.dump(resultado, open(os.path.join(OUT, "fuerza_xi_prueba.json"), "w"),
              indent=1, ensure_ascii=False)
    print("OK -> data/investigacion-xi/fuerza_xi_prueba.json")


if __name__ == '__main__':
    main()
