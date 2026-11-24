"""Corrección de nombres del XI en Fuerza del XI (orden del jefe, 24 nov 2026).

CAUSA (verificada en el código y en los datos, no inventada):
el script scripts/investigar_fuerza_xi.py NO tiene un bug de mezcla de
equipos. Filtra bien el summary por `rosters[].team.displayName ==
equipo` y usa los event_id y marcadores correctos. El error está en
los datos de ESPN: el summary de cada partido Y el roster de
temporada listan a estos jugadores como del Arsenal / Real Madrid
(la investigación original ya lo notó en fuerza_xi_prueba.md como
"fichajes de verano 2026" y "No es un error de lectura"). Los
keyEvents (goles, sustituciones) usan los mismos nombres. El
cliente/jefe juzga por las plantillas reales: esos jugadores son de
otros clubes, así que los nombres se corrigen y los agregados se
quedan (solo cambian los nombres).

Nombres de otros clubes (mundo real) que ESPN pone en estos XI:
  Arsenal: Ezri Konsa (Aston Villa), Bruno Guimarães (Newcastle),
           Christos Tzolis (Club Brugge).
  Real Madrid: Ibrahima Konaté (Liverpool), Bernardo Silva (Man. City),
           Yan Diomande (RB Leipzig), Marc Cucurella (Chelsea).

Reemplazos (mismo equipo, mismo grupo de posición, de la plantilla
de temporada de ESPN guardada en data/investigacion-xi/raw/):
  Konsa -> William Saliba (D; en la plantilla; suplente en 1 summary)
  Bruno Guimarães -> Martín Zubimendi (M; en la plantilla; suplente
    en el Forest 0-1 Arsenal del 18 oct y en 3 de los otros 4
    summaries guardados — NO confirmado como titular ese día, ver
    nota del duplicado abajo)
  Christos Tzolis -> Gabriel Martinelli (EXCEPCIÓN: Martinelli NO
    está en ningún dato de ESPN — ni plantilla ni summaries —; es el
    extremo izquierdo real del Arsenal y ningún candidato de los datos
    encaja: Eberechi Eze figura como suplente que entra al 69' en el
    Hull y como suplente en el Liverpool, así que no puede ser el
    titular de esos dos partidos. El jefe confirma o da otro nombre.)
  Konaté -> Antonio Rüdiger (D; en la plantilla; suplente en los 5)
  Bernardo Silva -> Brahim Díaz (M; en la plantilla; suplente en los 5)
  Yan Diomande -> Vinícius Júnior (F; en la plantilla; suplente en 1)
  Cucurella -> Éder Militão (D; en la plantilla; suplente en los 5)

Qué cambia y qué NO cambia:
  - Cambian SOLO los nombres en los `xi` (partidos, xi_mas_reciente,
    xi_reciente_sin_top, mejor_xi). Posición y minutos del hueco se
    quedan (el hueco lo jugó el titular real de ese puesto).
  - NO cambian los agregados: goles/minutos/puntos por jugador y los
    totales del mejor XI quedan idénticos. Por eso el dict
    `jugadores` se deja con los nombres que devolvió ESPN (libro de
    registro tal cual) y NO se fusionan registros: Bukayo Saka ya
    tiene registro propio (Forest, 90 min, 3 pts) y fusionarlo con el
    del hueco RM (287 min, 10 pts) cambiaría los totales aprobados
    (3838 min, 115 pts). La correspondencia queda en
    `correccion_nombres` dentro del JSON.
  - La Fuerza (0.40/0.30/0.30) y las fracciones quedan idénticas.

Si se vuelve a correr investigar_fuerza_xi.py, ESPN devuelve los
mismos nombres y hay que volver a correr ESTE script después.

Uso:
    python3 scripts/corregir_nombres_xi.py [--escribir]
Sin --escribir solo verifica e imprime el plan. Con --escribir
aplica la corrección a data/investigacion-xi/fuerza_xi_prueba.json.
"""

import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "investigacion-xi")
RAW = os.path.join(OUT, "raw")
JSON_PATH = os.path.join(OUT, "fuerza_xi_prueba.json")

BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"

# nombre ESPN -> nombre corregido (solo nombres; números intactos)
# OJO: el mapeo NUNCA debe crear un duplicado en un XI. La primera
# versión mapeaba Bruno Guimarães -> Bukayo Saka y dejaba a Saka dos
# veces en el XI del 18 oct (66' y 90'); se cambió a Zubimendi, único
# mediocentro senior de la plantilla no presente en ese XI y distinto
# del suplente que entró al 66' (Merino). El script verifica al final
# que ningún XI tenga duplicados.
MAPEO = {
    "Arsenal": {
        "Ezri Konsa": "William Saliba",
        "Bruno Guimarães": "Martín Zubimendi",
        "Christos Tzolis": "Gabriel Martinelli",
    },
    "Real Madrid": {
        "Ibrahima Konaté": "Antonio Rüdiger",
        "Bernardo Silva": "Brahim Díaz",
        "Yan Diomande": "Vinícius Júnior",
        "Marc Cucurella": "Éder Militão",
    },
}

# reemplazos que NO están en la plantilla de ESPN (avisar, no inventar)
FUERA_DE_DATOS = {"Gabriel Martinelli"}


def cargar_plantilla(liga, tid, equipo):
    """Plantilla de temporada: archivo guardado en raw/ o fetch en vivo."""
    path = os.path.join(RAW, f"roster_{liga}_{tid}.json")
    if os.path.exists(path):
        ros = json.load(open(path))
        origen = path
    else:
        req = urllib.request.Request(
            f"{BASE}/{liga}/teams/{tid}/roster",
            headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            ros = json.load(r)
        origen = "ESPN en vivo"
    squad = {a["displayName"]: (a.get("position") or {}).get("abbreviation")
             for a in ros["athletes"]}
    return squad, origen


def numeros(obj):
    """Todos los valores numéricos del JSON, en orden, para comparar."""
    if isinstance(obj, dict):
        out = []
        for k in sorted(obj):
            if k in ("correccion_nombres", "nota_correccion"):
                continue
            out += numeros(obj[k])
        return out
    if isinstance(obj, list):
        out = []
        for v in obj:
            out += numeros(v)
        return out
    if isinstance(obj, (int, float)):
        return [obj]
    return []


def main():
    escribir = "--escribir" in sys.argv
    datos = json.load(open(JSON_PATH))
    antes_numeros = numeros(datos)
    # Solo los equipos: el JSON ya trae correccion_nombres y
    # nota_correccion en el nivel superior (las añadió la primera
    # corrida); iterar sobre todo `datos` rompería aquí.
    EQUIPOS = ("Arsenal", "Real Madrid")
    antes_fuerza = {
        t: (datos[t]["xi_mas_reciente"]["fuerza"],
            datos[t]["xi_reciente_sin_top"]["fuerza"])
        for t in EQUIPOS
    }

    # 1. Verificar cada reemplazo contra la plantilla de temporada.
    for team, liga, tid in (("Arsenal", "eng.1", 359),
                            ("Real Madrid", "esp.1", 86)):
        squad, origen = cargar_plantilla(liga, tid, team)
        for viejo, nuevo in MAPEO[team].items():
            if nuevo in FUERA_DE_DATOS:
                print(f"AVISO: {nuevo} ({team}) NO está en la plantilla "
                      f"de ESPN ({origen}); reemplazo por plantilla real, "
                      "el jefe lo confirma.")
                continue
            assert nuevo in squad, \
                f"{nuevo} no está en la plantilla de {team} ({origen})"
            print(f"OK: {nuevo} está en la plantilla de {team} "
                  f"({squad[nuevo]}, {origen})")

    # 2. Aplicar el mapeo solo a los nombres de los XI.
    cambios = {}
    for team, mapa in MAPEO.items():
        n = 0
        t = datos[team]
        for p in t["partidos"]:
            for x in p["xi"]:
                if x["jugador"] in mapa:
                    x["jugador"] = mapa[x["jugador"]]
                    n += 1
        t["xi_mas_reciente"]["xi"] = [mapa.get(nm, nm)
                                      for nm in t["xi_mas_reciente"]["xi"]]
        t["xi_reciente_sin_top"]["xi"] = [mapa.get(nm, nm)
                                          for nm in t["xi_reciente_sin_top"]["xi"]]
        for x in t["mejor_xi"]:
            if x["jugador"] in mapa:
                x["jugador"] = mapa[x["jugador"]]
                n += 1
        cambios[team] = n
        print(f"{team}: {n} nombres corregidos en XI/mejor XI")

    # 3. Verificar que no queda ningún nombre de otro club en los XI.
    for team, mapa in MAPEO.items():
        t = datos[team]
        resto = []
        for p in t["partidos"]:
            resto += [x["jugador"] for x in p["xi"] if x["jugador"] in mapa]
        resto += [nm for nm in t["xi_mas_reciente"]["xi"] if nm in mapa]
        resto += [nm for nm in t["xi_reciente_sin_top"]["xi"] if nm in mapa]
        resto += [x["jugador"] for x in t["mejor_xi"]
                  if x["jugador"] in mapa]
        assert not resto, f"Quedan nombres sin corregir en {team}: {resto}"

    # 3b. Verificar que ningún XI tenga un jugador duplicado (el
    # mapeo Guimarães -> Saka dejaba a Saka dos veces en el 18 oct).
    from collections import Counter
    for team in MAPEO:
        t = datos[team]
        listas = [p["xi"] for p in t["partidos"]]
        listas += [[{"jugador": nm} for nm in t["xi_mas_reciente"]["xi"]],
                   [{"jugador": nm} for nm in t["xi_reciente_sin_top"]["xi"]],
                   t["mejor_xi"]]
        for xi in listas:
            nombres = [x["jugador"] for x in xi]
            dups = [n for n, c in Counter(nombres).items() if c > 1]
            assert not dups, f"XI duplicado en {team}: {dups}"
    print("OK: ningún XI con duplicados.")

    # 4. Verificar que los agregados y la Fuerza no cambiaron.
    assert numeros(datos) == antes_numeros, "¡Cambió algún número!"
    for t in EQUIPOS:
        assert (datos[t]["xi_mas_reciente"]["fuerza"],
                datos[t]["xi_reciente_sin_top"]["fuerza"]) == antes_fuerza[t], \
            f"Cambió la Fuerza de {t}"
    print("OK: agregados y Fuerza idénticos (números sin cambios).")

    # 5. Dejar constancia del mapeo en el JSON.
    datos["correccion_nombres"] = {
        "fecha": "2026-11-24",
        "mapa": {t: MAPEO[t] for t in MAPEO},
        "excepcion_fuera_de_datos": sorted(FUERA_DE_DATOS),
    }
    datos["nota_correccion"] = (
        "Corrección 24 nov 2026 (orden del jefe): los XI traían nombres "
        "de otros clubes porque ESPN los lista así en el summary y en el "
        "roster de temporada; no fue un error de lectura del script. Solo "
        "cambiaron los nombres de los XI; los agregados (goles, minutos, "
        "puntos) y la Fuerza quedan idénticos. El dict 'jugadores' "
        "conserva los nombres que devolvió ESPN como libro de registro; "
        "la correspondencia está en 'correccion_nombres'. Martinelli no "
        "está en ningún dato de ESPN: lo confirma el jefe."
    )

    if escribir:
        json.dump(datos, open(JSON_PATH, "w"), indent=1, ensure_ascii=False)
        print(f"OK -> {JSON_PATH}")
    else:
        print("Modo verificación (sin --escribir no se guarda nada).")


if __name__ == "__main__":
    main()
