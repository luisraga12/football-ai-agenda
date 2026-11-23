"""Descubre partidos nuevos publicados tarde en ESPN (Football AI Agenda).

Problema (jefe, 22 nov 2026, caso Liga MX): el workflow solo recalcula
los partidos que ya estan en el config. Los partidos que todavia no
existen en ESPN cuando se escribe el config — la Liga MX entre semana,
que se agenda hasta que se acaba la jornada — nadie los detecta.

Lo que hace este script, en cada corrida:
  1. Consulta los scoreboards de ESPN de las ligas del alcance
     (mex.1, eng.1, esp.1, ger.1, ita.1, uefa.champions, uefa.europa y
     Conference League) para la semana corriente (lun-dom de la primera
     fecha del config).
  2. Compara con una linea base guardada en
     data/semana-N/raw/descubrimiento_vistos.json (partidos ya vistos en
     corridas anteriores). La PRIMERA corrida solo establece la linea
     base y NO agrega nada: asi una config curada (p. ej. los 12 de
     entre semana, elegidos de 36) no se llena de partidos que ya
     existian y simplemente no se eligieron.
  3. Si en una corrida posterior aparece un partido que NO estaba en la
     linea base ni en el config, lo agrega al config (con su liga, fecha
     y IDs de equipo) y deja constancia en el log. El pipeline completo
     (Poisson + momios + EV) corre despues para el, porque
     run_semana.py llama a este script como paso 0.

Reglas (orden del jefe):
  - Solo ligas del alcance; partidos de Liguilla/playoffs incluidos
    cuando ESPN los publique.
  - Valida por team ID como siempre; nunca inventa un partido ni un
    momio.
  - Los partidos agregados se escriben en los mismos `data/` + `ev.json`
    que leera la integracion de la pagina (Semana 7).
  - No se guardan los scoreboards completos del descubrimiento (serian
    ~56 JSON por corrida); solo la linea base compacta.

Conference League: en ESPN no responde con ninguno de los slugs
probados (uefa.europa-conference, uefa.conference-league,
uefa.conference, uefa.uecl, uefa.conf, uefa.europa_conf,
uefa.europa-conference-league: todos HTTP 400, 22 nov 2026). Se sigue
intentando en cada corrida por si ESPN la publica; si no responde, se
registra en el log y se sigue con las demas ligas.

Uso:
    python3 scripts/descubrir_partidos.py --config scripts/config/semana-actual.json
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone

CST = timezone(timedelta(hours=-6))
BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"

# Ligas del alcance de la agenda (orden del jefe, 22 nov 2026).
ALCANCE = {
    'mex.1': 'Liga MX',
    'eng.1': 'Premier League',
    'esp.1': 'LaLiga',
    'ger.1': 'Bundesliga',
    'ita.1': 'Serie A',
    'uefa.champions': 'Champions League',
    'uefa.europa': 'Europa League',
}
# Slugs probados para la Conference League (ninguno responde en ESPN
# a 22 nov 2026; se reintentan por si ESPN la publica despues).
CONFERENCE_SLUGS = [
    'uefa.europa-conference', 'uefa.conference-league', 'uefa.conference',
    'uefa.uecl', 'uefa.conf', 'uefa.europa_conf',
    'uefa.europa-conference-league',
]


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def lunes_de(fecha_iso):
    d = datetime.fromisoformat(fecha_iso).date()
    return d - timedelta(days=d.weekday())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True,
                    help='JSON de la semana')
    ap.add_argument('--out', default=None,
                    help='carpeta de salida (por defecto data/semana-N)')
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    semana = cfg['semana']
    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')
    os.makedirs(rawdir, exist_ok=True)

    lunes = lunes_de(cfg['fechas'][0])
    dias = [(lunes + timedelta(days=i)).isoformat() for i in range(7)]
    print(f"Descubrimiento: semana {dias[0]} al {dias[-1]} "
          f"(config {cfg['nombre']})")

    # ---- 1. Scoreboards de la semana, ligas del alcance ----
    vistos_ahora = {}
    for lg, nombre in ALCANCE.items():
        for d in dias:
            dstr = d.replace('-', '')
            try:
                data = fetch(f"{BASE}/{lg}/scoreboard?dates={dstr}")
            except Exception as ex:
                print(f"  !! no se pudo {lg} {dstr}: {ex}")
                continue
            for e in data.get('events', []):
                comp = e['competitions'][0]
                home = next(c for c in comp['competitors']
                            if c['homeAway'] == 'home')
                away = next(c for c in comp['competitors']
                            if c['homeAway'] == 'away')
                dt = datetime.fromisoformat(
                    e['date'].replace('Z', '+00:00')).astimezone(CST)
                key = (str(home['team']['id']), str(away['team']['id']),
                       dt.strftime('%Y-%m-%d'))
                vistos_ahora[key] = {
                    'home': home['team']['displayName'],
                    'home_id': home['team']['id'],
                    'away': away['team']['displayName'],
                    'away_id': away['team']['id'],
                    'fecha': dt.strftime('%Y-%m-%d'),
                    'liga': lg, 'liga_nombre': nombre}
            time.sleep(0.2)
    # Conference League: se intenta, pero ESPN no la trae (ver docstring).
    conf_ok = False
    for slug in CONFERENCE_SLUGS:
        try:
            data = fetch(f"{BASE}/{slug}/scoreboard?dates="
                         f"{dias[0].replace('-', '')}")
            conf_ok = True
            print(f"  Conference League responde con el slug {slug} "
                  "(antes no respondia).")
            break
        except Exception:
            continue
    if not conf_ok:
        print("  Conference League: ESPN no la trae con ningun slug "
              "probado; se sigue sin ella.")

    # ---- 2. Linea base: primera corrida solo registra, no agrega ----
    base_path = os.path.join(rawdir, 'descubrimiento_vistos.json')
    if not os.path.exists(base_path):
        with open(base_path, 'w') as f:
            json.dump({f"{k[0]}|{k[1]}|{k[2]}": v
                       for k, v in vistos_ahora.items()},
                      f, indent=1, ensure_ascii=False)
        print(f"Linea base establecida: {len(vistos_ahora)} partidos "
              "vistos en ESPN esta semana. 0 agregados al config "
              "(primera corrida: no se agregan partidos que ya existian "
              "y simplemente no estaban curados).")
        return

    base = json.load(open(base_path))
    en_config = {(str(p['home_id']), str(p['away_id']), p['fecha'])
                 for p in cfg['partidos']}
    nuevos = []
    for key, v in vistos_ahora.items():
        kstr = f"{key[0]}|{key[1]}|{key[2]}"
        if kstr not in base and key not in en_config:
            nuevos.append(v)

    # ---- 3. Agregar los nuevos al config y actualizar la base ----
    for v in nuevos:
        cfg['partidos'].append({
            'home': v['home'], 'home_id': v['home_id'],
            'away': v['away'], 'away_id': v['away_id'],
            'fecha': v['fecha'], 'liga': v['liga']})
        if v['fecha'] not in cfg['fechas']:
            cfg['fechas'] = sorted(cfg['fechas'] + [v['fecha']])
        if v['liga'] not in cfg['ligas']:
            cfg['ligas'][v['liga']] = v['liga_nombre']
        print(f"NUEVO PARTIDO DETECTADO: {v['fecha']} {v['home']} vs "
              f"{v['away']} | {v['liga_nombre']} — agregado al config.")
    if nuevos:
        with open(args.config, 'w') as f:
            json.dump(cfg, f, indent=1, ensure_ascii=False)
        print(f"{len(nuevos)} partido(s) nuevo(s) agregados al config; "
              "el pipeline completo correra para ellos.")
    else:
        print("Sin partidos nuevos: 0 agregados al config.")
    base.update({f"{k[0]}|{k[1]}|{k[2]}": v
                 for k, v in vistos_ahora.items()})
    with open(base_path, 'w') as f:
        json.dump(base, f, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
