"""Genera data/parlay-del-dia.json: el parlay del dia (E1, 28 nov 2026).

Lee los ev.json publicados (fin de semana + entre semana) y toma los
3 mejores picks verdes (EV >= +5%) del dia, sin repetir partido.
Cada pierna: partido, pick, momio, prob y EV del modelo.

Reglas (orden del jefe, JEFE.md f51ccc0):
  - Solo partidos de HOY (America/Mexico_City) en estado 'pre'.
  - Si hay menos de 3 con valor, se publican las que haya (1-2);
    si no hay ninguna, piernas vacias con "sin valor hoy".
  - Nunca inventar picks: sin mejor_ev publicado, no hay pierna.
  - El parlay del dia se FIJA por la manana: si el archivo ya existe
    con la fecha de hoy, no se sobrescribe (las corridas horarias del
    fin de semana no lo mutan mientras los partidos se van jugando;
    el acerto/fallo del final del dia se evalua sobre estas piernas).

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

    cands = []
    vistos = set()
    for ruta in EVS:
        try:
            doc = json.load(open(ruta))
        except (ValueError, OSError):
            continue
        for p in doc.get("partidos") or []:
            if p.get("fecha") != hoy:
                continue
            if p.get("estado_partido") != "pre":
                continue
            ev = p.get("mejor_ev")
            if not isinstance(ev, (int, float)) or ev < UMBRAL_EV:
                continue
            slug = p.get("slug") or slug_de(p)
            if slug in vistos:
                continue
            vistos.add(slug)
            cands.append({
                "slug": slug,
                "partido": f"{p.get('home')} vs {p.get('away')}",
                "liga": p.get("liga"),
                "hora": p.get("hora"),
                "pick": p.get("mejor_pick"),
                "momio": p.get("mejor_decimal"),
                "prob": p.get("mejor_prob"),
                "ev": ev,
            })
    cands.sort(key=lambda c: -c["ev"])
    piernas = cands[:MAX_PIERNAS]

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
                 f"{len(piernas)} pierna(s) con EV >= +5%"),
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
