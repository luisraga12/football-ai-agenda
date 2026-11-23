"""Ejemplos reales para las propuestas del jefe (23 nov 2026).

  1. Tendencias por mercado: con data/semana-2/raw/teams_last5.json
     (últimos 5 de cada equipo, ya descargados) se calcula por equipo
     "ambos marcaron X/5" y "más de 2.5 goles X/5", y por partido la
     racha combinada.
  2. Historial de aciertos del modelo: Semana 1 (20-22 nov, ya jugada).
     Favorito 1X2 de tabla-poisson-semana-1.md contra el resultado real
     de los scoreboards guardados en data/semana-1/raw/. También +2.5
     y BTTS cuando el modelo daba >50%.
  3. Movimientos de momios: ev.json de la Semana 2 del domingo 22 nov
     (rama semana-3, antes del refresco) contra el regenerado del
     lunes 23 nov en main (09:52 + workflow 10:39). Mismo con entre
     semana. Qué cambió: mejor pick, EV y líneas.

Uso: python3 scripts/investigar_propuestas.py
Guarda: data/investigacion-xi/propuestas_ejemplos.json
"""

import json
import os
import re

BASE = "."


def tendencias():
    t = json.load(open("data/semana-2/raw/teams_last5.json"))
    out = {}
    for team, d in t.items():
        ms = d["matches"]
        btts = sum(1 for m in ms if m["gf"] > 0 and m["ga"] > 0)
        over = sum(1 for m in ms if m["gf"] + m["ga"] > 2.5)
        out[team] = {"btts": f"{btts}/5", "mas25": f"{over}/5",
                     "goles_favor": d["gf"], "goles_contra": d["ga"]}
    return out


def semana1_aciertos():
    md = open("data/semana-1/tabla-poisson-semana-1.md").read()
    filas = []
    for line in md.splitlines():
        if not line.startswith("| Vie") and not line.startswith("| Sáb") \
                and not line.startswith("| Dom"):
            continue
        c = [x.strip() for x in line.split("|")]
        # | Fecha | Hora | Liga | Local | Visitante | xGl | xGv | P1 | PX | P2 | P+2.5 | BTTS |
        filas.append({"fecha": c[1], "liga": c[3], "home": c[4], "away": c[5],
                      "p1": float(c[8].rstrip('%')),
                      "px": float(c[9].rstrip('%')),
                      "p2": float(c[10].rstrip('%')),
                      "p_over": float(c[11].rstrip('%')),
                      "p_btts": float(c[12].rstrip('%'))})
    # resultados reales de los scoreboards guardados
    res = {}
    for fn in sorted(os.listdir("data/semana-1/raw")):
        if not fn.startswith("scoreboard_"):
            continue
        sb = json.load(open(f"data/semana-1/raw/{fn}"))
        for e in sb.get("events", []):
            comp = e["competitions"][0]
            if not comp.get("status", {}).get("type", {}).get("completed"):
                continue
            h = next(x for x in comp["competitors"] if x["homeAway"] == "home")
            a = next(x for x in comp["competitors"] if x["homeAway"] == "away")
            res[(h["team"]["displayName"], a["team"]["displayName"])] = (
                int(float(h["score"])), int(float(a["score"])))
    ok1x2 = ok_over = ok_btts = n_over = n_btts = 0
    detalle = []
    for f in filas:
        # el nombre en la tabla puede diferir levemente del de ESPN
        key = None
        for k in res:
            if k[0].startswith(f["home"][:6]) and k[1].startswith(f["away"][:6]):
                key = k
                break
        if key is None:
            detalle.append({**f, "resultado": "sin resultado en raw"})
            continue
        gh, ga = res[key]
        real = "1" if gh > ga else ("X" if gh == ga else "2")
        fav = max(("1", f["p1"]), ("X", f["px"]), ("2", f["p2"]),
                  key=lambda kv: kv[1])[0]
        over_real = gh + ga > 2.5
        btts_real = gh > 0 and ga > 0
        ac1 = fav == real
        ok1x2 += ac1
        over_txt = btts_txt = None
        if f["p_over"] > 50:
            n_over += 1
            ok_over += (over_real == (f["p_over"] > 50))
            over_txt = f"modelo Más 2.5 ({f['p_over']}%) -> {'acierto' if over_real else 'fallo'}"
        if f["p_btts"] > 50:
            n_btts += 1
            ok_btts += (btts_real == (f["p_btts"] > 50))
            btts_txt = f"modelo BTTS ({f['p_btts']}%) -> {'acierto' if btts_real else 'fallo'}"
        detalle.append({**f, "resultado": f"{gh}-{ga} ({real})",
                        "favorito": fav, "acierto_1x2": ac1,
                        "over": over_txt, "btts": btts_txt})
    return {"n": len(filas), "aciertos_1x2": ok1x2,
            "aciertos_mas25": f"{ok_over}/{n_over}",
            "aciertos_btts": f"{ok_btts}/{n_btts}", "detalle": detalle}


def movimientos(archivo_dom, archivo_lun, etiqueta):
    dom = json.load(open(archivo_dom))["partidos"]
    lun = json.load(open(archivo_lun))["partidos"]
    dl = {(p["home"], p["away"]): p for p in dom}
    cambios = []
    for p in lun:
        d = dl.get((p["home"], p["away"]))
        if d is None:
            continue
        ev_d, ev_l = d["mejor_ev"] * 100, p["mejor_ev"] * 100
        linea_d = (d.get("mercados", {}).get("total") or {}).get("linea")
        linea_l = (p.get("mercados", {}).get("total") or {}).get("linea")
        if d["mejor_pick"] != p["mejor_pick"] or abs(ev_d - ev_l) > 0.5 \
                or linea_d != linea_l:
            cambios.append({
                "partido": f"{p['home']} vs {p['away']}",
                "pick_domingo": f"{d['mejor_pick']} {ev_d:+.1f}%",
                "pick_lunes": f"{p['mejor_pick']} {ev_l:+.1f}%",
                "linea_total_domingo": linea_d,
                "linea_total_lunes": linea_l,
            })
    return {"etiqueta": etiqueta, "partidos_con_cambio": len(cambios),
            "de": len(lun), "cambios": cambios}


def main():
    out = {}
    out["tendencias"] = tendencias()
    print("== Tendencias (últimos 5, Semana 2, ejemplos) ==")
    for team in ("Real Madrid", "Arsenal", "Bayern Munich", "Barcelona",
                 "Liverpool", "Napoli", "Inter", "Sassuolo"):
        if team in out["tendencias"]:
            print(f"   {team}: BTTS {out['tendencias'][team]['btts']}, "
                  f"Más 2.5 {out['tendencias'][team]['mas25']}")
    out["semana1"] = semana1_aciertos()
    s1 = out["semana1"]
    print(f"\n== Semana 1: favorito 1X2 {s1['aciertos_1x2']}/{s1['n']}, "
          f"Más 2.5 {s1['aciertos_mas25']}, BTTS {s1['aciertos_btts']}")
    for d in s1["detalle"]:
        print(f"   {d['fecha']} {d['home']} vs {d['away']}: "
              f"{d.get('resultado')} fav {d.get('favorito')} "
              f"{'ACIERTO' if d.get('acierto_1x2') else 'fallo'}"
              f"{' | ' + d['over'] if d.get('over') else ''}"
              f"{' | ' + d['btts'] if d.get('btts') else ''}")
    import subprocess
    subprocess.run(["git", "show", "semana-3:data/semana-2/ev.json"],
                   stdout=open("/tmp/ev_s2_domingo.json", "w"))
    subprocess.run(["git", "show", "semana-3:data/semana-2-entresemana/ev.json"],
                   stdout=open("/tmp/ev_se_domingo.json", "w"))
    out["movimientos_s2"] = movimientos(
        "/tmp/ev_s2_domingo.json", "data/semana-2/ev.json", "Semana 2")
    out["movimientos_entresemana"] = movimientos(
        "/tmp/ev_se_domingo.json", "data/semana-2-entresemana/ev.json",
        "Entre semana")
    for k in ("movimientos_s2", "movimientos_entresemana"):
        m = out[k]
        print(f"\n== Movimientos {m['etiqueta']}: {m['partidos_con_cambio']}"
              f" de {m['de']} partidos cambiaron pick/EV/línea")
        for c in m["cambios"]:
            print(f"   {c['partido']}: {c['pick_domingo']} -> "
                  f"{c['pick_lunes']} | línea total "
                  f"{c['linea_total_domingo']} -> {c['linea_total_lunes']}")
    json.dump(out, open("data/investigacion-xi/propuestas_ejemplos.json",
                        "w"), indent=1, ensure_ascii=False)
    print("\nOK -> data/investigacion-xi/propuestas_ejemplos.json")


if __name__ == "__main__":
    main()
