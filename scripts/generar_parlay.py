"""Genera data/parlay-del-dia.json: el parlay del dia (E1, 28 nov 2026).

Lee data/resultados.json (paso 12) y toma las 3 mejores piernas del dia
entre las recomendaciones equilibradas, sin repetir partido. Cada pierna:
partido, pick, momio, prob y EV del modelo.

Reglas (orden del jefe, JEFE.md f51ccc0; regla balanceada 28 nov 2026,
ejemplo del jefe: Hamburg/empate):
  - Solo partidos de HOY (America/Mexico_City) en estado 'pre'.
  - Cada pierna es el MEJOR VERDE del partido (el pick verde de mayor EV:
    prob >= 60% y EV >= +5%), publicado en resultados.json. Si faltan
    verdes para 3 piernas, se completa con recomendaciones amarillas
    (30% <= prob < 60% y EV >= +5%). Nunca una roja.
  - Antes el parlay tomaba el maximo EV sin mas y por eso puso al Hamburg
    Local @8.00 (29.9%, rojo): la buena era Hamburg +1.5 @1.775 (70%,
    verde), que cubre ganar, empatar y perder por 1.
  - Si hay menos de 3 con valor, se publican las que haya (1-2);
    si no hay ninguna, piernas vacias con "sin valor hoy".
  - Nunca inventar picks: sin mejor verde ni recomendacion amarilla,
    no hay pierna. Si resultados.json no existe o no se puede leer, NO
    se escribe nada (falla fuerte: el parlay necesita las
    recomendaciones; run_semana.py corre resultados antes que el parlay).
  - El parlay del dia se FIJA por la manana: si el archivo ya existe
    con la fecha de hoy, no se sobrescribe (las corridas horarias del
    fin de semana no lo mutan mientras los partidos se van jugando;
    el acierto/fallo del final del dia se evalua sobre estas piernas).

Uso: python3 scripts/generar_parlay.py [--fecha YYYY-MM-DD]
Salida: data/parlay-del-dia.json
"""

import argparse
import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVS = [
    os.path.join(ROOT, "data", "semana-2", "ev.json"),
    os.path.join(ROOT, "data", "semana-2-entresemana", "ev.json"),
]
RESULTADOS = os.path.join(ROOT, "data", "resultados.json")
SALIDA = os.path.join(ROOT, "data", "parlay-del-dia.json")
UMBRAL_EV = 0.05
MAX_PIERNAS = 3


def slug_de(p):
    home = (p.get("home") or "").strip().lower()
    away = (p.get("away") or "").strip().lower()
    import re
    import unicodedata

    def norm(s):
        s = unicodedata.normalize("NFD", s)
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")
        return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

    return norm(home) + "-vs-" + norm(away)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fecha", default=None,
                    help="fecha YYYY-MM-DD (por defecto: hoy en America/Mexico_City)")
    args = ap.parse_args()
    hoy = args.fecha or datetime.now(ZoneInfo("America/Mexico_City")).date().isoformat()

    if os.path.exists(SALIDA):
        try:
            previo = json.load(open(SALIDA))
            if previo.get("fecha") == hoy and previo.get("piernas"):
                print(f"parlay-del-dia.json ya existe para {hoy} "
                      f"({len(previo['piernas'])} piernas): no se sobrescribe.")
                return
        except (ValueError, OSError):
            pass

    try:
        with open(RESULTADOS, encoding="utf-8") as f:
            res = json.load(f)
    except (ValueError, OSError) as e:
        print(f"ERROR: no se pudo leer {RESULTADOS}: {e}. El parlay "
              "necesita las recomendaciones; no se escribe nada.")
        raise SystemExit(1)

    # La hora no viene en resultados.json: se toma de los ev.json.
    horas = {}
    for ruta in EVS:
        try:
            doc = json.load(open(ruta))
        except (ValueError, OSError):
            continue
        for p in doc.get("partidos") or []:
            horas[(p.get("home"), p.get("away"))] = p.get("hora")

    def pierna_de(p, pick):
        return {
            "slug": slug_de(p),
            "partido": f"{p.get('home')} vs {p.get('away')}",
            "liga": p.get("liga"),
            "hora": horas.get((p.get("home"), p.get("away"))),
            "pick": pick.get("pick"),
            "mercado": pick.get("mercado"),
            "momio": pick.get("momio"),
            "prob": pick.get("prob"),
            "ev": pick.get("ev"),
        }

    verdes = []
    amarillas = []
    vistos = set()
    for p in res.get("partidos") or []:
        if p.get("fecha") != hoy:
            continue
        if p.get("estado") != "pre":
            continue
        slug = slug_de(p)
        if slug in vistos:
            continue
        vistos.add(slug)
        rec = p.get("recomendacion") or {}
        mv = rec.get("mejor_verde")
        if isinstance(mv, dict) and mv.get("momio") is not None \
                and isinstance(mv.get("ev"), (int, float)) \
                and mv["ev"] >= UMBRAL_EV:
            verdes.append(pierna_de(p, mv))
        elif rec.get("color") == "amarillo" and rec.get("cumple_regla") \
                and isinstance(rec.get("ev"), (int, float)) \
                and rec["ev"] >= UMBRAL_EV:
            amarillas.append(pierna_de(p, rec))
    verdes.sort(key=lambda c: -c["ev"])
    amarillas.sort(key=lambda c: -c["ev"])
    piernas = (verdes + amarillas)[:MAX_PIERNAS]

    momio_comb = 1.0
    prob_comb = 1.0
    for pierna in piernas:
        momio_comb *= pierna["momio"]
        prob_comb *= pierna["prob"] / 100.0
    out = {
        "fecha": hoy,
        "generado_en": datetime.now(ZoneInfo("UTC")).isoformat(),
        "piernas": piernas,
        "momio_combinado": round(momio_comb, 2) if piernas else None,
        "prob_combinada": round(prob_comb * 100, 2) if piernas else None,
        "ev_combinado": round(prob_comb * momio_comb - 1, 4) if piernas else None,
        "nota": ("sin valor hoy" if not piernas else
                 f"{len(piernas)} pierna(s) verdes/amarillas "
                 "(regla balanceada)"),
    }
    with open(SALIDA, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for pierna in piernas:
        print(f"  {pierna['ev'] * 100:.1f}% {pierna['partido']} | "
              f"{pierna['pick']} @{pierna['momio']:.2f} "
              f"(prob {pierna['prob']:.1f}%)")
    print(f"OK -> data/parlay-del-dia.json ({hoy}): {len(piernas)} piernas, "
          f"momio combinado {out['momio_combinado']}, "
          f"EV combinado "
          f"{out['ev_combinado'] * 100:.1f}% " if piernas else
          "OK -> data/parlay-del-dia.json: sin valor hoy")


if __name__ == "__main__":
    main()
