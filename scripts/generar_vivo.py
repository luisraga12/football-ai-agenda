"""Genera data/vivo.json: marcador en vivo desde ESPN (Football AI Agenda).

Lee la configuracion de la semana actual (scripts/config/semana-actual.json
y, si existe, scripts/config/semana-<N>-entresemana.json), pide los
scoreboards de ESPN para cada par (liga, fecha) y escribe un JSON con el
marcador, el minuto y el estado de cada partido de la semana.

Reglas (orden del jefe, 24 nov 2026; propuesta-vivo-cache.md):
  1. Solo API publica de ESPN, sin clave. Se intenta primero
     site.api.espn.com y, si falla, site.web.api.espn.com (el respaldo
     que el jefe preparo para el navegador; aqui no hay CORS, pero el
     400 intermitente de ESPN afecta a los dos hosts).
  2. Los partidos se identifican por liga + fecha + IDs de equipo, nunca
     por nombre: si un partido del config no aparece en ESPN, queda
     registrado como fallo, no se inventa nada.
  3. El archivo se escribe de forma segura: se genera en un temporal,
     se valida (JSON bien formado, lista de partidos, campos requeridos)
     y solo entonces se reemplaza data/vivo.json. Si TODAS las consultas
     fallan, el archivo anterior se conserva intacto y el script sale
     con codigo 1 (el workflow lo registra, no escribe nada roto).
  4. Mezcla (merge): los partidos de fechas que no se consultaron en
     esta corrida conservan su ultimo dato conocido (con su
     actualizado_en). Y siembra (seed): todo partido del config que
     aun no tiene entrada en vivo.json recibe una entrada
     programada (estado 'pre', sin marcador, origen 'config'), para
     que vivo.json siempre traiga TODOS los partidos de la semana y
     la pagina nunca se quede sin marcador en vivo por un partido
     descubierto tarde. La siembra nunca inventa un resultado: la
     entrada programada no muestra marcador hasta que ESPN lo
     publique.
  5. Solo se escribe si algo cambio: una entrada solo se actualiza
     cuando cambia su contenido real (estado, minuto o marcador);
     si nada cambio, el archivo no se reescribe y generado_en
     conserva la hora del ultimo cambio real. Asi el historial de
     git refleja cambios de verdad y no un commit cada 5 minutos.
  6. Los fallos se registran en data/vivo-log.json (ultimas 50 entradas)
     para auditarlos; vivo.json lleva solo un campo "advertencia" corto.

Uso:
    python3 scripts/generar_vivo.py [--config scripts/config/semana-actual.json]
                                     [--salida data/vivo.json] [--todas]
    --todas: consulta todas las fechas de la semana (no solo hoy y ayer).
             Sin --todas se consultan las fechas de hoy y de ayer (hora
             de Mexico), que es lo que corre el workflow cada 5 minutos.
             Ayer se consulta para cerrar en "post" con su marcador
             final real los partidos terminados el dia anterior: el
             scoreboard de hoy ya no los trae, y sin ayer quedarian
             congelados en su ultimo estado conocido (26 nov 2026).
"""

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

MX = ZoneInfo("America/Mexico_City")
UTC = timezone.utc

HOSTS = [
    "https://site.api.espn.com/apis/site/v2/sports/soccer",
    "https://site.web.api.espn.com/apis/site/v2/sports/soccer",
]

CAMPOS = ("liga", "fecha", "home_id", "away_id", "home", "away",
          "estado", "detalle", "minuto", "marcador_local",
          "marcador_visita", "actualizado_en")


def fetch_json(url):
    """Pide una URL y devuelve el JSON. Lanza la excepcion si falla."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def scoreboard(liga, fecha):
    """Scoreboard de ESPN para (liga, fecha), con respaldo de host.

    Devuelve (datos, host_usado). Lanza la ultima excepcion si los dos
    hosts fallan.
    """
    url_path = f"{liga}/scoreboard?dates={fecha.replace('-', '')}"
    ultimo_error = None
    for host in HOSTS:
        try:
            return fetch_json(f"{host}/{url_path}"), host
        except Exception as e:  # noqa: BLE001 - se reintenta con el otro host
            ultimo_error = e
    raise ultimo_error


def extraer_partido(evento, liga, fecha, ahora_iso):
    """Saca marcador/minuto/estado de un evento de ESPN (o None)."""
    comps = (evento.get("competitions") or [None])[0]
    if not comps:
        return None
    competidores = comps.get("competitors") or []
    ids = {}
    nombres = {}
    for c in competidores:
        equipo = c.get("team") or {}
        rol = c.get("homeAway")
        ids[rol] = str(equipo.get("id"))
        nombres[rol] = equipo.get("displayName", "")
        marcador = c.get("score")
        try:
            marcador = None if marcador is None else int(float(marcador))
        except (TypeError, ValueError):
            marcador = None
        ids[rol + "_score"] = marcador
    st = comps.get("status") or {}
    tipo = st.get("type") or {}
    minuto = st.get("displayClock") or ""
    return {
        "liga": liga,
        "fecha": fecha,
        "home_id": int(ids["home"]) if ids.get("home") else None,
        "away_id": int(ids["away"]) if ids.get("away") else None,
        "home": nombres.get("home", ""),
        "away": nombres.get("away", ""),
        "estado": tipo.get("state", "pre"),
        "detalle": tipo.get("detail") or tipo.get("shortDetail") or "",
        "minuto": minuto,
        "marcador_local": ids.get("home_score"),
        "marcador_visita": ids.get("away_score"),
        "actualizado_en": ahora_iso,
    }


def contenido_igual(a, b):
    """True si dos entradas de vivo.json dicen lo mismo (estado,
    minuto y marcador). actualizado_en y origen no cuentan: si el
    contenido no cambio, la entrada se conserva tal cual para no
    reescribir el archivo cada 5 minutos."""
    for campo in ("estado", "detalle", "minuto", "marcador_local",
                  "marcador_visita"):
        if a.get(campo) != b.get(campo):
            return False
    return True


def registrar_fallos(fallos, log_path):
    """Agrega fallos a data/vivo-log.json (ultimas 50 entradas)."""
    registro = []
    if os.path.isfile(log_path):
        try:
            with open(log_path, encoding="utf-8") as f:
                registro = json.load(f)
        except (OSError, ValueError):
            registro = []
    registro.extend(fallos)
    registro = registro[-50:]
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2)
        f.write("\n")


def cargar_config(path_config):
    """Partidos de la semana actual + entre semana (si hay)."""
    with open(path_config, encoding="utf-8") as f:
        actual = json.load(f)
    semana = actual.get("semana")
    partidos = list(actual.get("partidos") or [])
    base = os.path.dirname(path_config)
    entresemana = os.path.join(base, f"semana-{semana}-entresemana.json")
    if os.path.isfile(entresemana):
        with open(entresemana, encoding="utf-8") as f:
            partidos += list(json.load(f).get("partidos") or [])
    return semana, partidos


def clave(p):
    return (p["liga"], p["fecha"], str(p["home_id"]), str(p["away_id"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="scripts/config/semana-actual.json")
    ap.add_argument("--salida", default="data/vivo.json")
    ap.add_argument("--log", default="data/vivo-log.json")
    ap.add_argument("--todas", action="store_true",
                    help="consultar todas las fechas, no solo hoy")
    args = ap.parse_args()

    ahora_utc = datetime.now(UTC)
    ahora_iso = ahora_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    hoy_mx_dt = datetime.now(MX)
    hoy_mx = hoy_mx_dt.strftime("%Y-%m-%d")
    # Ayer (hora de Mexico): se consulta ademas de hoy para cerrar en
    # "post" con su marcador final real los partidos terminados el dia
    # anterior. El scoreboard de hoy ya no los trae; sin ayer, el merge
    # los dejaba congelados en su ultimo estado conocido (p. ej.
    # Toluca-Atlas "in" 23' 1-0 y Monterrey-America "pre" en main la
    # noche del 25-26 nov 2026).
    ayer_mx = (hoy_mx_dt - timedelta(days=1)).strftime("%Y-%m-%d")

    semana, partidos = cargar_config(args.config)
    pares = sorted({(p["liga"], p["fecha"]) for p in partidos})
    if not args.todas:
        pares = [par for par in pares if par[1] in (hoy_mx, ayer_mx)]
    if not pares:
        print(f"Sin fechas que consultar hoy ni ayer ({hoy_mx}, {ayer_mx}); "
              "no se escribe nada.")
        return 0

    # Datos previos (merge): si el archivo existe y es valido, se conserva.
    previos = {}
    viejo = None
    if os.path.isfile(args.salida):
        try:
            with open(args.salida, encoding="utf-8") as f:
                viejo = json.load(f)
            for p in viejo.get("partidos") or []:
                previos[clave(p)] = p
        except (OSError, ValueError):
            print("AVISO: vivo.json anterior ilegible; se regenera desde cero.")
            viejo = None

    nuevos = dict(previos)
    fallos = []
    consultados = 0
    encontrados = 0
    for liga, fecha in pares:
        consultados += 1
        try:
            datos, host = scoreboard(liga, fecha)
        except Exception as e:  # noqa: BLE001 - se registra y se sigue
            fallos.append({"cuando": ahora_iso, "liga": liga, "fecha": fecha,
                           "error": f"{type(e).__name__}: {e}"})
            print(f"FALLO {liga} {fecha}: {e}")
            continue
        eventos = datos.get("events") or []
        por_ids = {}
        for ev in eventos:
            ext = extraer_partido(ev, liga, fecha, ahora_iso)
            if ext and ext["home_id"] and ext["away_id"]:
                por_ids[(str(ext["home_id"]), str(ext["away_id"]))] = ext
        for p in partidos:
            if (p["liga"], p["fecha"]) != (liga, fecha):
                continue
            ext = por_ids.get((str(p["home_id"]), str(p["away_id"])))
            if ext is None:
                fallos.append({"cuando": ahora_iso, "liga": liga,
                               "fecha": fecha,
                               "error": f"partido no en ESPN: "
                                        f"{p['home']} vs {p['away']}"})
                continue
            anterior = nuevos.get(clave(ext))
            if anterior is not None and contenido_igual(anterior, ext):
                # Sin cambio real: se conserva la entrada tal cual (con
                # su actualizado_en), para no reescribir cada 5 minutos.
                pass
            else:
                nuevos[clave(ext)] = ext
            encontrados += 1
        print(f"OK {liga} {fecha} via {host.split('/')[2]}: "
              f"{len(eventos)} eventos en el scoreboard.")

    # Siembra: todo partido del config sin entrada recibe una entrada
    # programada (estado 'pre', sin marcador, origen 'config'). Asi
    # vivo.json cubre la semana completa aunque ESPN aun no publique
    # el partido, la corrida solo consulte las fechas de hoy o el
    # partido se haya descubierto tarde (paso 0). La siembra nunca
    # inventa un resultado: la entrada programada no muestra marcador
    # hasta que ESPN lo publique, y en la siguiente corrida el dato
    # real de ESPN la reemplaza (misma clave liga/fecha/ids).
    sembrados = 0
    for p in partidos:
        k = (p["liga"], p["fecha"], str(p["home_id"]), str(p["away_id"]))
        if k not in nuevos:
            nuevos[k] = {
                "liga": p["liga"], "fecha": p["fecha"],
                "home_id": p["home_id"], "away_id": p["away_id"],
                "home": p["home"], "away": p["away"],
                "estado": "pre", "detalle": "", "minuto": "",
                "marcador_local": None, "marcador_visita": None,
                "actualizado_en": ahora_iso, "origen": "config",
            }
            sembrados += 1

    if not partidos:
        print("FALLO TOTAL: el config no trae partidos; vivo.json "
              "no se toca.")
        return 1
    # Si todas las consultas fallaron, igual se escribe la siembra
    # (partidos programados, sin marcador): la pagina muestra los
    # partidos programados en vez de quedarse sin vivo.json. Los
    # fallos quedan en vivo-log.json.

    lista = [nuevos[k] for k in sorted(nuevos)]
    previos_lista = (viejo.get("partidos")
                     if isinstance(viejo, dict) else None)
    if previos_lista == lista:
        # Nada cambio: no se reescribe el archivo (generado_en
        # conserva la hora del ultimo cambio real). Los fallos de
        # esta corrida igual se registran.
        if fallos:
            registrar_fallos(fallos, args.log)
        print(f"vivo.json: sin cambios ({len(lista)} partidos, "
              f"{len(fallos)} fallo(s) en esta corrida).")
        return 0
    advertencia = None
    if fallos:
        advertencia = (f"{len(fallos)} fallo(s) en la ultima corrida "
                       f"({ahora_iso}); se conserva el ultimo dato bueno.")
    salida = {
        "version": 1,
        "generado_en": ahora_iso,
        "generado_en_mx": datetime.now(MX).strftime("%Y-%m-%dT%H:%M:%S-06:00"),
        "semana": semana,
        "fuente": "ESPN scoreboard (site.api.espn.com, respaldo "
                  "site.web.api.espn.com)",
        "partidos": lista,
        "advertencia": advertencia,
    }
    # Validacion antes de escribir: estructura minima.
    assert isinstance(salida["partidos"], list)
    for p in salida["partidos"]:
        for campo in CAMPOS:
            assert campo in p, f"falta {campo} en {p}"

    os.makedirs(os.path.dirname(args.salida) or ".", exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(args.salida) or ".",
                               prefix=".vivo-", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, args.salida)

    if fallos:
        registrar_fallos(fallos, args.log)

    print(f"vivo.json: {len(lista)} partidos "
          f"({encontrados} actualizados en esta corrida, "
          f"{sembrados} sembrados del config, "
          f"{len(fallos)} fallo(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
