"""Descubre partidos nuevos y completa la jornada (Football AI Agenda).

Problema original (jefe, 22 nov 2026, caso Liga MX): el workflow solo
recalcula los partidos que ya estan en el config. Los partidos que
todavia no existen en ESPN cuando se escribe el config — la Liga MX
entre semana, que se agenda hasta que se acaba la jornada — nadie
los detecta.

Cambio del 25 nov 2026 (jefe, JEFE.md 437b004 — fin de semana curado):
el config puede traer `completar_jornada: false`. Con ese flag, el
descubrimiento NO agrega partidos a ese config (se queda curado en
los que tiene), aunque ESPN tenga mas para sus fechas y ligas; la
linea base se sigue actualizando como registro y el log dice
cuantos se habrian agregado. Sin la clave (o en true), el
comportamiento es el de siempre: completar la jornada. El fin de
semana (semana-actual.json, 20 partidos) lleva el flag en false; la
corrida de las 07:00 no debe completarlo solo a 40.

Cambio del 24 nov 2026 (jefe, JEFE.md 4531da0 — automatizar que la
jornada quede completa): el descubrimiento ya NO caza solo los
partidos publicados despues de la linea base. En cada corrida, para
las fechas y ligas del propio config, agrega CUALQUIER partido que
ESPN tenga y no este en el config. Asi la jornada sale completa sin
que nadie tenga que revisar a mano: los de Champions y Europa League
que ya estaban publicados cuando se armo el config (por eso no los
agrego solo) entran solos en la siguiente corrida. La prueba con un
partido publicado tarde sigue valiendo: un partido publicado tarde
aparece en el scoreboard y, al no estar en el config, se agrega
igual — el mecanismo es el mismo, la linea base solo dejo de ser
el filtro.

Lo que hace este script, en cada corrida:
  1. Consulta los scoreboards de ESPN de las ligas del alcance
     (mex.1, eng.1, esp.1, ger.1, ita.1, uefa.champions, uefa.europa y
     Conference League) para la semana corriente (lun-dom de la primera
     fecha del config).
  2. Compara lo visto con el CONFIG: todo partido de ESPN cuya fecha
     este en cfg['fechas'] y cuya liga este en cfg['ligas'] y que NO
     este ya en el config se agrega (con su liga, fecha y IDs de
     equipo). Un partido visto cuya fecha no esta en el config, o
     cuya liga no esta en el config, no se agrega (lo ve el otro
     config si su fecha y su liga si estan en el suyo). **Un partido
     ya terminado (ESPN: estado 'post') tampoco se agrega**: la
     jornada que se completa es la que falta por jugarse; los 5 de
     Champions del mar 24 nov 2026 (Bodo/Glimt–LASK, Como–AEK,
     Feyenoord–Porto, Leipzig–Lens, Slovan Bratislava–Betis) ya se
     jugaron y el jefe ordeno no agregarlos (JEFE.md 3b2fc87) — el
     descubrimiento los habria metido solos en la corrida del 24 nov
     por la noche, y este filtro lo impide.
  3. La linea base guardada en
     data/semana-N/raw/descubrimiento_vistos.json se sigue actualizando
     como registro de lo visto en ESPN, pero YA NO decide nada: la
     primera corrida tambien completa la jornada (no hay corrida que
     solo establezca la base).
  El pipeline completo (Poisson + momios + EV) corre despues para los
  agregados, porque run_semana.py llama a este script como paso 0.

Reglas (orden del jefe):
  - Solo ligas del alcance; partidos de Liguilla/playoffs incluidos
    cuando ESPN los publique.
  - Valida por team ID como siempre; nunca inventa un partido ni un
    momio.
  - Los partidos agregados se escriben en los mismos `data/` + `ev.json`
    que leera la integracion de la pagina (Semana 7).
  - No se guardan los scoreboards completos del descubrimiento (serian
    ~56 JSON por corrida); solo la linea base compacta.
  - El cambio al config DEBE commitearse (el workflow hace
    `git add data/ scripts/config/`): leccion de la Liguilla, 24 nov
    2026 — la corrida c892956 descubrio los 8 cuartos de final y los
    puso en el ev.json, pero el workflow solo commiteaba `data/` y el
    cambio al config se perdio; la baseline ya los traia, asi que en
    la siguiente corrida no se re-agregaron y el pipeline los saco
    del ev.json. Sin el commit del config, el descubrimiento solo
    dura una corrida.
  - Alcance de las adiciones (24 nov 2026): solo fechas y ligas del
    propio config. Una liga que NO este en cfg['ligas'] no se descubre
    (a diferencia de la Liguilla en Semana 7, donde la liga entro al
    config por el descubrimiento); si el jefe quiere que las ligas
    vuelvan a entrar solas, es una decision suya, no de este script.

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
from datetime import datetime, timedelta, timezone

# Modulo hermano (scripts/): los scripts siempre se corren como
# `python3 scripts/*.py` desde la raiz del repo, asi que resuelve.
from http_resiliente import descargar_json

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
    """GET con reintentos (ver http_resiliente.py)."""
    return descargar_json(url)


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
    # Flag del 25 nov 2026 (jefe, JEFE.md 437b004): con
    # completar_jornada: false el config se queda curado y el
    # descubrimiento no agrega nada (la base se sigue actualizando).
    # Sin la clave, o en true, se completa la jornada como siempre.
    completar = cfg.get('completar_jornada', True)
    print(f"Descubrimiento: semana {dias[0]} al {dias[-1]} "
          f"(config {cfg['nombre']}) — completar jornada: "
          f"{'sí' if completar else 'no (config curado)'}")

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
                estado = e.get('status', {}).get('type', {}).get('state')
                key = (str(home['team']['id']), str(away['team']['id']),
                       dt.strftime('%Y-%m-%d'))
                vistos_ahora[key] = {
                    'home': home['team']['displayName'],
                    'home_id': home['team']['id'],
                    'away': away['team']['displayName'],
                    'away_id': away['team']['id'],
                    'fecha': dt.strftime('%Y-%m-%d'),
                    'liga': lg, 'liga_nombre': nombre,
                    'estado': estado}
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

    # ---- 2. Completar la jornada: todo lo de ESPN para las fechas
    # y ligas del config que no este en el config se agrega. La linea
    # base ya no filtra: es solo registro de lo visto (24 nov 2026).
    base_path = os.path.join(rawdir, 'descubrimiento_vistos.json')
    base = json.load(open(base_path)) if os.path.exists(base_path) else {}
    en_config = {(str(p['home_id']), str(p['away_id']), p['fecha'])
                 for p in cfg['partidos']}
    fechas_config = set(cfg['fechas'])
    ligas_config = set(cfg['ligas'])
    nuevos = []
    no_agregados = 0
    fuera_de_alcance = 0
    terminados = 0
    for key, v in vistos_ahora.items():
        if key in en_config:
            continue
        if v.get('estado') == 'post':
            terminados += 1
            continue
        if v['fecha'] in fechas_config and v['liga'] in ligas_config:
            if completar:
                nuevos.append(v)
            else:
                no_agregados += 1
        else:
            fuera_de_alcance += 1
    if terminados:
        print(f"{terminados} partido(s) ya terminado(s) en ESPN "
              "(no se agregan: la jornada que se completa es la que "
              "falta por jugarse).")
    if no_agregados:
        print(f"Config curado (completar_jornada: false): "
              f"{no_agregados} partido(s) visto(s) en ESPN para las "
              "fechas y ligas del config que NO se agregan; el config "
              "se queda como esta.")
    if fuera_de_alcance:
        print(f"{fuera_de_alcance} partido(s) visto(s) en ESPN con "
              "fecha o liga fuera del config (no se agregan; los ve "
              "el otro config si su fecha y su liga estan en el suyo).")

    # ---- 3. Agregar los nuevos al config y actualizar la base ----
    for v in nuevos:
        cfg['partidos'].append({
            'home': v['home'], 'home_id': v['home_id'],
            'away': v['away'], 'away_id': v['away_id'],
            'fecha': v['fecha'], 'liga': v['liga']})
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
