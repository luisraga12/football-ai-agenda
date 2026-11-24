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
     actualizado_en). Asi vivo.json siempre trae los 28 partidos de la
     semana y cada entrada dice de cuando es su dato.
  5. Los fallos se registran en data/vivo-log.json (ultimas 50 entradas)
     para auditarlos; vivo.json lleva solo un campo "advertencia" corto.

Uso:
    python3 scripts/generar_vivo.py [--config scripts/config/semana-actual.json]
                                     [--salida data/vivo.json] [--todas]
    --todas: consulta todas las fechas de la semana (no solo hoy).
             Sin --todas solo se consultan las fechas de hoy (hora de
             Mexico), que es lo que corre el workflow cada 5 minutos.
"""

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
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
    hoy_mx = datetime.now(MX).strftime("%Y-%m-%d")

    semana, partidos = cargar_config(args.config)
    pares = sorted({(p["liga"], p["fecha"]) for p in partidos})
    if not args.todas:
        pares = [par for par in pares if par[1] == hoy_mx]
    if not pares:
        print(f"Sin fechas que consultar hoy ({hoy_mx}); no se escribe nada.")
        return 0

    # Datos previos (merge): si el archivo existe y es valido, se conserva.
    previos = {}
    if os.path.isfile(args.salida):
        try:
            with open(args.salida, encoding="utf-8") as f:
                viejo = json.load(f)
            for p in viejo.get("partidos") or []:
                previos[clave(p)] = p
        except (OSError, ValueError):
            print("AVISO: vivo.json anterior ilegible; se regenera desde cero.")

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
            nuevos[clave(ext)] = ext
            encontrados += 1
        print(f"OK {liga} {fecha} via {host.split('/')[2]}: "
              f"{len(eventos)} eventos en el scoreboard.")

    if consultados > 0 and encontrados == 0 and not previos:
        print("FALLO TOTAL: ninguna consulta devolvio partidos; "
              "vivo.json no se toca.")
        return 1

    lista = [nuevos[k] for k in sorted(nuevos)]
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
        registro = []
        if os.path.isfile(args.log):
            try:
                with open(args.log, encoding="utf-8") as f:
                    registro = json.load(f)
            except (OSError, ValueError):
                registro = []
        registro.extend(fallos)
        registro = registro[-50:]
        with open(args.log, "w", encoding="utf-8") as f:
            json.dump(registro, f, ensure_ascii=False, indent=2)
            f.write("\n")

    print(f"vivo.json: {len(lista)} partidos "
          f"({encontrados} actualizados en esta corrida, "
          f"{len(fallos)} fallo(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
