"""Historial de aciertos del modelo (rutina fija de cada lunes).

Compara lo que el modelo Poisson pronosticó en la tabla de la semana
con los resultados reales (scoreboards de ESPN guardados en raw/) y
escribe el historial de esa semana.

Definiciones (las mismas que la revisión de la Semana 1 que el jefe
ya verificó; NO se esconden los fallos):
  - Favorito 1X2: el 1/X/2 con mayor P en la tabla. Acierto si el
    resultado real coincide. Se cuentan los 16 partidos con
    resultado; el 6/16 de la Semana 1 se publica tal cual.
  - Más 2.5: solo cuando el modelo daba P(+2.5) > 50%. Acierto si
    hubo 3+ goles. Menos 2.5: cuando P(+2.5) <= 50%; acierto si hubo
    2- goles. (La revisión original solo contaba el lado Más; aquí
    se cuentan los dos lados para no esconder nada.)
  - BTTS: cuando P(ambos anotan) > 50%, acierto si los dos
    marcaron. No-BTTS: cuando <= 50%; acierto si al menos uno no
    marcó. (Son conteos de resultados, NO momios: ESPN no da momios
    de BTTS.)
  - Empate: se cuentan aparte cuántos partidos terminaron en X y
    en cuántos el favorito del modelo era X. En la Semana 1 hubo
    7 empates de 16 y el modelo no puso el empate como favorito en
    ninguno: es el punto débil que hay que decir, no esconder.

Resultados reales: de los scoreboard_*.json en raw/ (solo partidos
con status completed). Si un partido no trae resultado final en el
raw (p. ej. Guadalajara-Cruz Azul, que en el raw iba 1-0 al
descanso sin terminar), se usa el archivo de resultados
verificados (ver --verificados): cada entrada lleva su fuente y
fecha de verificación, y queda registrada por partido en
`fuente_resultado`. Nada se inventa: sin raw ni verificado, el
partido queda "sin resultado" y no entra en los denominadores.

Fecha de cálculo: SIEMPRE en hora de México (America/Mexico_City).
La VM va en UTC y en Tendencias la fecha salió un día adelante; el
jefe ya lo señaló. No repetir ese error.

Salida:
  - data/semana-N/historial.json: resumen + detalle por partido.
  - data/semana-N/historial.html: sección "Cómo le fue al modelo"
    lista para la página (la coloca el jefe; no toca index.html).

Uso:
    python3 scripts/calcular_historial.py \\
        --tabla data/semana-1/tabla-poisson-semana-1.md \\
        --raw-dir data/semana-1/raw \\
        --verificados data/semana-1/resultados_verificados.json \\
        --salida data/semana-1/historial.json \\
        --html data/semana-1/historial.html \\
        --semana semana-1
"""

import argparse
import json
import os
import re
from zoneinfo import ZoneInfo

DIAS = ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")


def fecha_mexico():
    """Fecha de hoy en México (America/Mexico_City), no la de la VM (UTC)."""
    from datetime import datetime
    return datetime.now(ZoneInfo("America/Mexico_City")).date().isoformat()


def leer_tabla(path):
    """Filas de la tabla (a) del .md: fecha, liga, equipos, P1/PX/P2,
    P(+2.5) y P(BTTS)."""
    filas = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.startswith("|"):
            continue
        c = [x.strip() for x in line.split("|")]
        if len(c) < 13 or not any(c[1].startswith(d) for d in DIAS):
            continue
        filas.append({
            "fecha": c[1], "liga": c[3], "home": c[4], "away": c[5],
            "p1": float(c[8].rstrip("%")),
            "px": float(c[9].rstrip("%")),
            "p2": float(c[10].rstrip("%")),
            "p_over": float(c[11].rstrip("%")),
            "p_btts": float(c[12].rstrip("%")),
        })
    return filas


def leer_resultados(raw_dir):
    """Resultados reales de los scoreboards guardados (solo completed).

    Devuelve {(local, visitante): (goles_local, goles_visita)} con los
    nombres tal como los trae ESPN.
    """
    res = {}
    for fn in sorted(os.listdir(raw_dir)):
        if not fn.startswith("scoreboard_"):
            continue
        sb = json.load(open(os.path.join(raw_dir, fn), encoding="utf-8"))
        for e in sb.get("events", []):
            comp = e["competitions"][0]
            if not comp.get("status", {}).get("type", {}).get("completed"):
                continue
            h = next(x for x in comp["competitors"]
                     if x["homeAway"] == "home")
            a = next(x for x in comp["competitors"]
                     if x["homeAway"] == "away")
            res[(h["team"]["displayName"], a["team"]["displayName"])] = (
                int(float(h["score"])), int(float(a["score"])))
    return res


def buscar_resultado(home, away, res, verificados):
    """(goles_local, goles_visita, fuente) o (None, None, None).

    Primero el raw; si no hay resultado final ahí, el archivo de
    resultados verificados (con su fuente). Si no hay ninguno, el
    partido queda sin resultado (no se inventa).
    """
    for (h, a), (gh, ga) in res.items():
        if h == home and a == away:
            return gh, ga, "raw"
    for (h, a), (gh, ga) in res.items():
        if h.startswith(home[:6]) and a.startswith(away[:6]):
            return gh, ga, "raw"
    for v in verificados:
        if v["home"] == home and v["away"] == away:
            return (v["goles_local"], v["goles_visita"],
                    "verificado: " + v["fuente"])
    return None, None, None


def evaluar(filas, res, verificados):
    detalle = []
    r = {"n": len(filas), "con_resultado": 0, "sin_resultado": 0,
         "aciertos_1x2": 0, "ok_mas25": 0, "n_mas25": 0,
         "ok_menos25": 0, "n_menos25": 0,
         "ok_btts": 0, "n_btts": 0, "ok_no_btts": 0, "n_no_btts": 0,
         "empates_reales": 0, "favoritos_empate": 0,
         "por_liga": {}}
    for f in filas:
        gh, ga, fuente = buscar_resultado(f["home"], f["away"],
                                          res, verificados)
        fav = max(("1", f["p1"]), ("X", f["px"]), ("2", f["p2"]),
                  key=lambda kv: kv[1])[0]
        d = {**f, "favorito": fav, "fuente_resultado": fuente}
        liga = r["por_liga"].setdefault(
            f["liga"], {"n": 0, "aciertos_1x2": 0})
        liga["n"] += 1
        if gh is None:
            r["sin_resultado"] += 1
            d["resultado"] = "sin resultado"
            d["acierto_1x2"] = None
            detalle.append(d)
            continue
        r["con_resultado"] += 1
        real = "1" if gh > ga else ("X" if gh == ga else "2")
        d["resultado"] = f"{gh}-{ga} ({real})"
        d["acierto_1x2"] = fav == real
        r["aciertos_1x2"] += d["acierto_1x2"]
        liga["aciertos_1x2"] += d["acierto_1x2"]
        if real == "X":
            r["empates_reales"] += 1
        if fav == "X":
            r["favoritos_empate"] += 1
        total = gh + ga
        if f["p_over"] > 50:
            r["n_mas25"] += 1
            ok = total > 2.5
            r["ok_mas25"] += ok
            d["mas25"] = ("acierto" if ok else "fallo")
        else:
            r["n_menos25"] += 1
            ok = total <= 2
            r["ok_menos25"] += ok
            d["menos25"] = ("acierto" if ok else "fallo")
        if f["p_btts"] > 50:
            r["n_btts"] += 1
            ok = gh > 0 and ga > 0
            r["ok_btts"] += ok
            d["btts"] = ("acierto" if ok else "fallo")
        else:
            r["n_no_btts"] += 1
            ok = not (gh > 0 and ga > 0)
            r["ok_no_btts"] += ok
            d["no_btts"] = ("acierto" if ok else "fallo")
        detalle.append(d)
    n = r["con_resultado"]
    r["pct_1x2"] = round(100 * r["aciertos_1x2"] / n, 1) if n else 0
    return r, detalle


def lectura(r):
    """Lectura honesta del historial, generada desde los números."""
    out = []
    if r["con_resultado"] == 0:
        out.append("Sin resultados todavía: la semana no se ha jugado.")
        return out
    out.append(
        f"Favorito 1X2: {r['aciertos_1x2']}/{r['con_resultado']} "
        f"({r['pct_1x2']}%). "
        + ("Bajo: el 1X2 es el mercado más flojo del modelo; su EV "
           "debe leerse con más cautela que el de totales."
           if r["pct_1x2"] < 50 else
           "Por encima de la mitad: el favorito 1X2 aguantó."))
    out.append(
        f"Empates: {r['empates_reales']} de {r['con_resultado']} "
        f"partidos terminaron en X y el modelo puso el empate como "
        f"favorito en {r['favoritos_empate']}. "
        + ("El modelo casi no caza el empate: nunca lo pone de "
           "favorito y los empates lo tumban."
           if r["empates_reales"] > 0 and r["favoritos_empate"] == 0
           else ""))
    out.append(
        f"Totales: Más 2.5 {r['ok_mas25']}/{r['n_mas25']} cuando el "
        f"modelo daba >50%; Menos 2.5 {r['ok_menos25']}/{r['n_menos25']} "
        f"cuando daba <=50%. BTTS {r['ok_btts']}/{r['n_btts']} y "
        f"No-BTTS {r['ok_no_btts']}/{r['n_no_btts']}.")
    return [x for x in out if x]


def fragmento_html(semana, fecha_calculo, r, detalle):
    """Sección 'Cómo le fue al modelo' lista para la página."""
    def pct(ok, n):
        return f"{ok}/{n}" if n else "—"
    filas = "\n".join(
        f"<tr><td>{d['fecha']}</td><td>{d['liga']}</td>"
        f"<td>{d['home']} vs {d['away']}</td>"
        f"<td>{d['resultado']}</td>"
        f"<td>{'✓' if d.get('acierto_1x2') else ('✗' if d.get('acierto_1x2') is False else '—')}</td>"
        f"<td>{d.get('mas25') or d.get('menos25') or '—'}</td>"
        f"<td>{d.get('btts') or d.get('no_btts') or '—'}</td></tr>"
        for d in detalle)
    return f"""<!-- HISTORIAL-INICIO:{semana} -->
<section class="historial">
<h2>Cómo le fue al modelo — {semana}</h2>
<p>Favorito 1X2: <strong>{r['aciertos_1x2']}/{r['con_resultado']} ({r['pct_1x2']}%)</strong>
· Más 2.5: {pct(r['ok_mas25'], r['n_mas25'])}
· Menos 2.5: {pct(r['ok_menos25'], r['n_menos25'])}
· BTTS: {pct(r['ok_btts'], r['n_btts'])}
· No-BTTS: {pct(r['ok_no_btts'], r['n_no_btts'])}
· Empates: {r['empates_reales']} de {r['con_resultado']}</p>
<p class="historial-fecha">Revisión del lunes, fecha de cálculo {fecha_calculo} (México).</p>
<table class="historial-tabla">
<tr><th>Fecha</th><th>Liga</th><th>Partido</th><th>Resultado</th><th>1X2</th><th>Total</th><th>BTTS</th></tr>
{filas}
</table>
</section>
<!-- HISTORIAL-FIN:{semana} -->
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tabla", required=True)
    ap.add_argument("--raw-dir", required=True)
    ap.add_argument("--verificados", default=None,
                    help="JSON con resultados verificados a mano "
                         "(partidos sin resultado final en el raw)")
    ap.add_argument("--salida", required=True)
    ap.add_argument("--html", default=None)
    ap.add_argument("--semana", required=True)
    ap.add_argument("--fecha", default=None,
                    help="fecha de cálculo (por defecto hoy en México)")
    args = ap.parse_args()

    filas = leer_tabla(args.tabla)
    res = leer_resultados(args.raw_dir)
    verificados = []
    if args.verificados and os.path.exists(args.verificados):
        verificados = json.load(open(args.verificados, encoding="utf-8"))
    r, detalle = evaluar(filas, res, verificados)
    fecha_calculo = args.fecha or fecha_mexico()
    salida = {
        "semana": args.semana,
        "fecha_calculo": fecha_calculo,
        "resumen": r,
        "lectura": lectura(r),
        "detalle": detalle,
    }
    json.dump(salida, open(args.salida, "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    print(f"{args.semana}: 1X2 {r['aciertos_1x2']}/{r['con_resultado']} "
          f"({r['pct_1x2']}%), Más 2.5 {r['ok_mas25']}/{r['n_mas25']}, "
          f"BTTS {r['ok_btts']}/{r['n_btts']}, "
          f"sin resultado: {r['sin_resultado']} -> {args.salida}")
    if args.html:
        open(args.html, "w", encoding="utf-8").write(
            fragmento_html(args.semana, fecha_calculo, r, detalle))
        print(f"Fragmento -> {args.html}")


if __name__ == "__main__":
    main()
