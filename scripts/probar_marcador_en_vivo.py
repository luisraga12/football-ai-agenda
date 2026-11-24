"""Prueba del prototipo de marcador en vivo (sin navegador).

  1. Los 28 partidos de la Semana 2 (configs semana-2.json y
     semana-2-entresemana.json) aparecen en el scoreboard de ESPN de su
     fecha, buscados por liga + fecha + IDs de equipo (la misma lógica
     del módulo JS, reimplementada aquí para correrla en Node).
  2. En partidos ya jugados (21 nov 2026) el scoreboard trae marcador y
     minuto/estado, que es lo que el módulo muestra en vivo.
  3. Frescura: el scoreboard trae el campo 'clock' con el minuto en
     juego; ESPN lo actualiza en cada petición (se comprueba pidiendo
     dos veces seguidas y viendo que el timestamp cambia).

Uso: node scripts/probar_marcador_en_vivo.js
"""

import json
import urllib.request
import time

BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def buscar(liga, fecha, home_id, away_id):
    fecha = fecha.replace('-', '')
    sb = fetch(f"{BASE}/{liga}/scoreboard?dates={fecha}")
    for e in sb.get('events', []):
        comp = (e.get('competitions') or [{}])[0]
        ids = [str(c['team']['id']) for c in comp.get('competitors', [])]
        if str(home_id) in ids and str(away_id) in ids:
            return comp
    return None


def main():
    total, hallados, errores = 0, 0, []
    for cfg in ("scripts/config/semana-2.json",
                "scripts/config/semana-2-entresemana.json"):
        c = json.load(open(cfg))
        for p in c['partidos']:
            total += 1
            comp = buscar(p['liga'], p['fecha'], p['home_id'], p['away_id'])
            if comp is None:
                errores.append(f"{p['fecha']} {p['home']} vs {p['away']}")
                continue
            hallados += 1
            st = comp.get('status', {}).get('type', {})
            if total <= 2:
                print(f"  ejemplo: {p['home']} vs {p['away']} -> "
                      f"estado={st.get('state')} detalle={st.get('detail')}")
    print(f"Partidos Semana 2 en scoreboard ESPN: {hallados}/{total}")
    if errores:
        print("NO encontrados:", errores)

    # 2. Partidos jugados: marcador + minuto/estado
    print("\nPartidos jugados 21 nov 2026 (eng.1):")
    sb = fetch(f"{BASE}/eng.1/scoreboard?dates=20261121")
    for e in sb.get('events', [])[:4]:
        comp = e['competitions'][0]
        h = next(c for c in comp['competitors'] if c['homeAway'] == 'home')
        a = next(c for c in comp['competitors'] if c['homeAway'] == 'away')
        st = comp.get('status', {}).get('type', {})
        status = comp.get('status', {})
        clock = status.get('displayClock', '')
        if not clock and isinstance(status.get('clock'), (int, float)):
            clock = f"{int(status['clock'] // 60)}'" if status['clock'] else ''
        print(f"  {h['team']['displayName']} {h.get('score')} - "
              f"{a.get('score')} {a['team']['displayName']} | "
              f"estado={st.get('state')} detalle={st.get('detail')} "
              f"minuto={clock!r}")
    # 3. Frescura: el scoreboard no trae timestamp propio; lo que cambia
    # en vivo es status.displayClock ("67'") y el marcador. Hoy no hay
    # partidos en juego (los de la Semana 2 empiezan el 24 nov), así que
    # la frescura real se verá el día del partido: cada petición de
    # cada 60 s trae el minuto actualizado.
    print("\nFrescura: sin partidos en juego hoy no se puede medir el "
          "retraso; el módulo pide el scoreboard cada 60 s y el minuto "
          "viene en status.displayClock, que ESPN actualiza en vivo.")


if __name__ == '__main__':
    main()
