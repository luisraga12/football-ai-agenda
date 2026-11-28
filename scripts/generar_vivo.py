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

  7. En juego: cada partido con estado "in" pide su summary de ESPN
     (mismo respaldo de host que el scoreboard) y publica rojas,
     stats (posesion/tiros/TDA/corners) y cambios en vivo.json. Si el
     summary falla, se conservan las ultimas conocidas y el fallo
     queda en vivo-log.json; la corrida no falla. Un partido
     terminado conserva sus ultimas stats (las finales).
  8. Log de snapshots: cada cambio de un partido en juego con stats
     anade una linea JSONL a data/live-log/YYYY-MM-DD.jsonl (fecha de
     Mexico), para calibrar el modelo en vivo; nunca se reescribe.

Uso:
    python3 scripts/generar_vivo.py [--config scripts/config/semana-actual.json]
                                     [--salida data/vivo.json] [--todas]
                                     [--live-log-dir data/live-log]
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
import re
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# Modulo hermano (scripts/): los scripts siempre se corren como
# `python3 scripts/*.py` desde la raiz del repo, asi que resuelve.
from http_resiliente import descargar_json

MX = ZoneInfo("America/Mexico_City")
UTC = timezone.utc

HOSTS = [
    "https://site.api.espn.com/apis/site/v2/sports/soccer",
    "https://site.web.api.espn.com/apis/site/v2/sports/soccer",
]

CAMPOS = ("liga", "fecha", "home_id", "away_id", "home", "away",
          "estado", "detalle", "minuto", "marcador_local",
          "marcador_visita", "actualizado_en", "evento_id")

TIPOS_ROJA = ("Red Card", "Second Yellow Card")


def fetch_json(url):
    """Pide una URL y devuelve el JSON. Lanza la excepcion si falla.
    Con reintentos (ver http_resiliente.py): un error transitorio
    ya no tumba el vivo de un partido."""
    return descargar_json(url)


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


def summary(liga, event_id):
    """Summary de ESPN para un evento, con respaldo de host.

    Devuelve el JSON. Lanza la ultima excepcion si los dos hosts
    fallan. Usa el mismo mecanismo resiliente que scoreboard()
    (http_resiliente.py): un error transitorio no tumba la corrida.
    """
    url_path = f"{liga}/summary?event={event_id}"
    ultimo_error = None
    for host in HOSTS:
        try:
            return fetch_json(f"{host}/{url_path}")
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
        "evento_id": evento.get("id"),
    }


def _num_stat(stats, nombre):
    """Valor numerico de una estadistica del boxscore (o None).

    ESPN trae "value" en null y el numero en "displayValue" como
    texto; se acepta value si es numero y si no se parsea
    displayValue. Nunca se inventa un 0.
    """
    for s in stats or []:
        if s.get("name") != nombre:
            continue
        v = s.get("value")
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return v
        dv = s.get("displayValue")
        if dv is None:
            return None
        try:
            return int(str(dv))
        except (TypeError, ValueError):
            pass
        try:
            return float(str(dv))
        except (TypeError, ValueError):
            return None
    return None


def extraer_rojas_stats(summary, home_id, away_id):
    """(rojas, stats, cambios, minuto) de un summary ESPN.

    - rojas: keyEvents "Red Card"/"Second Yellow Card": equipo por
      team.id ("H"/"A"), minuto de clock.displayValue, jugador del
      primer participant.
    - stats: boxscore.teams[].statistics por team.id (no por orden):
      possessionPct, totalShots, shotsOnTarget, wonCorners. Valores
      numericos (value, respaldo displayValue); None si falta un
      dato, nunca 0 inventado.
    - cambios: keyEvents "Substitution" -> {local: [minutos],
      visita: [minutos]} (solo minuto y equipo; no se registra quien
      entra/sale porque el orden de participants no esta documentado).
    - minuto: displayClock del summary ("" si no lo trae, p. ej. un
      partido terminado: el llamador usa el minuto del scoreboard
      como respaldo).
    """
    rojas = []
    cambios = {"local": [], "visita": []}
    for k in summary.get("keyEvents") or []:
        tipo = (k.get("type") or {}).get("text", "")
        team_id = str((k.get("team") or {}).get("id", ""))
        if team_id == str(home_id):
            lado = "local"
        elif team_id == str(away_id):
            lado = "visita"
        else:
            lado = None
        reloj = (k.get("clock") or {}).get("displayValue", "") or ""
        m = re.search(r"(\d+)", reloj)
        minuto_ev = (m.group(1) + "'") if m else ""
        if tipo in TIPOS_ROJA:
            parts = k.get("participants") or []
            jugador = ""
            if parts:
                jugador = ((parts[0].get("athlete") or {})
                           .get("displayName") or "")
            rojas.append({"equipo": "H" if lado == "local" else "A",
                          "minuto": minuto_ev, "jugador": jugador})
        elif tipo == "Substitution" and lado is not None and m:
            try:
                cambios[lado].append(int(m.group(1)))
            except ValueError:
                pass
    status = ((summary.get("header") or {}).get("competitions") or [{}])[0]
    minuto_sum = ((status.get("status") or {}).get("displayClock")) or ""
    stats = None
    vals = {}
    for t in ((summary.get("boxscore") or {}).get("teams") or []):
        tid = str((t.get("team") or {}).get("id", ""))
        if tid == str(home_id):
            suf = "h"
        elif tid == str(away_id):
            suf = "a"
        else:
            continue
        st = t.get("statistics") or []
        vals[suf] = {
            "pos": _num_stat(st, "possessionPct"),
            "tiros": _num_stat(st, "totalShots"),
            "tda": _num_stat(st, "shotsOnTarget"),
            "corn": _num_stat(st, "wonCorners"),
        }
    if vals:
        stats = {"min": minuto_sum,
                 "pos_h": vals.get("h", {}).get("pos"),
                 "pos_a": vals.get("a", {}).get("pos"),
                 "tiros_h": vals.get("h", {}).get("tiros"),
                 "tiros_a": vals.get("a", {}).get("tiros"),
                 "tda_h": vals.get("h", {}).get("tda"),
                 "tda_a": vals.get("a", {}).get("tda"),
                 "corn_h": vals.get("h", {}).get("corn"),
                 "corn_a": vals.get("a", {}).get("corn")}
    return rojas, stats, cambios, minuto_sum


def contenido_igual(a, b):
    """True si dos entradas de vivo.json dicen lo mismo (estado,
    minuto, marcador, rojas, stats y cambios). actualizado_en y origen
    no cuentan: si el contenido no cambio, la entrada se conserva tal
    cual para no reescribir el archivo cada 5 minutos."""
    for campo in ("estado", "detalle", "minuto", "marcador_local",
                  "marcador_visita", "rojas", "stats", "cambios"):
        if a.get(campo) != b.get(campo):
            return False
    return True


def registrar_snapshots(snapshots, log_dir, fecha_mx):
    """Anade snapshots de partidos en juego a
    data/live-log/YYYY-MM-DD.jsonl (fecha de Mexico, append-only).

    Solo se llama con snapshots de partidos en juego con stats cuyo
    contenido cambio en esta corrida; si no hay snapshots no se crea
    nada. Cada linea lleva "cuando" (ISO UTC) para que dos snapshots
    iguales sean distinguibles.
    """
    if not snapshots:
        return
    os.makedirs(log_dir, exist_ok=True)
    path = os.path.join(log_dir, f"{fecha_mx}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        for s in snapshots:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")


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
    ap.add_argument("--live-log-dir", default="data/live-log",
                    help="directorio del log de snapshots en vivo "
                         "(JSONL por fecha, Mexico; default data/live-log)")
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
                p.setdefault("evento_id", None)
                previos[clave(p)] = p
        except (OSError, ValueError):
            print("AVISO: vivo.json anterior ilegible; se regenera desde cero.")
            viejo = None

    nuevos = dict(previos)
    fallos = []
    snapshots = []
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
            # Vivo (27 nov 2026): rojas/stats/cambios del summary, solo
            # en juego. Si el summary falla se conservan las ultimas
            # conocidas y el fallo queda en vivo-log.json; la corrida
            # no falla. Un partido terminado conserva sus ultimas
            # stats (las finales).
            if ext["estado"] == "in" and ext.get("evento_id"):
                sumario = None
                try:
                    sumario = summary(liga, ext["evento_id"])
                except Exception as e:  # noqa: BLE001 - fail-soft
                    fallos.append({"cuando": ahora_iso, "liga": liga,
                                   "fecha": fecha,
                                   "error": f"summary no disponible: "
                                            f"{ext['home']} vs {ext['away']}: "
                                            f"{type(e).__name__}: {e}"})
                    print(f"AVISO summary {liga} {ext['evento_id']}: {e}")
                if sumario:
                    rojas, stats, cambios, minuto_sum = extraer_rojas_stats(
                        sumario, ext["home_id"], ext["away_id"])
                    ext["rojas"] = rojas
                    ext["stats"] = stats
                    ext["cambios"] = cambios
                    min_ef = minuto_sum or ext.get("minuto") or ""
                    if stats is not None:
                        stats["min"] = min_ef
                    if min_ef:
                        ext["minuto"] = min_ef
                elif anterior is not None:
                    for campo in ("rojas", "stats", "cambios"):
                        if campo in anterior:
                            ext[campo] = anterior[campo]
            elif anterior is not None:
                # No en juego (o sin evento): conserva sus ultimas
                # rojas/stats (las finales de un terminado).
                for campo in ("rojas", "stats", "cambios"):
                    if campo in anterior:
                        ext[campo] = anterior[campo]
            # Snapshot para el log en vivo: solo si esta en juego,
            # tiene al menos un dato de stats y su informacion cambio
            # en esta corrida.
            st = ext.get("stats")
            tiene_stats = (isinstance(st, dict)
                           and any(v is not None
                                   for k, v in st.items() if k != "min"))
            if ext["estado"] == "in" and tiene_stats:
                if anterior is None or not contenido_igual(anterior, ext):
                    snapshots.append({
                        "cuando": ahora_iso, "evento": ext.get("evento_id"),
                        "liga": liga, "home": ext["home"],
                        "away": ext["away"],
                        "minuto": ext.get("minuto", ""),
                        "marcador": [ext.get("marcador_local"),
                                     ext.get("marcador_visita")],
                        "tiros": [st.get("tiros_h"), st.get("tiros_a")],
                        "tda": [st.get("tda_h"), st.get("tda_a")],
                        "pos": [st.get("pos_h"), st.get("pos_a")],
                        "corners": [st.get("corn_h"), st.get("corn_a")],
                        "rojas": ext.get("rojas", []),
                    })
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
                "evento_id": None,
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
    # Log de snapshots en vivo (append-only, solo si hubo cambios en
    # partidos en juego con stats).
    registrar_snapshots(snapshots, args.live_log_dir, hoy_mx)
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
