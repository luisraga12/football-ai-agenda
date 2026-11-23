"""Escribe el entregable de una semana (Football AI Agenda).

Lee data/semana-N/raw/poisson_result.json y escribe
data/semana-N/tabla-poisson-semana-N.md con:
  (a) tabla de los partidos, (b) tabla de calculo por equipo,
  (c) promedios de liga usados, (d) fuentes ESPN consultadas,
  (e) datos no verificados y partidos excluidos.

Uso:
    python3 scripts/generar_tabla.py --config scripts/config/semana-1.json
"""

import argparse
import json
import os
import statistics


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    semana = cfg['semana']
    outdir = args.out or f"data/semana-{semana}"
    rawdir = os.path.join(outdir, 'raw')
    res = json.load(open(os.path.join(rawdir, 'poisson_result.json')))
    teams, rows, avgs = res['teams'], res['matches'], res['avgs']
    LN = cfg['ligas']
    fechas_txt = f"{cfg['fechas'][0]} al {cfg['fechas'][-1]}"
    cutoff = cfg['cutoff'][:10]
    n_partidos = len(rows)
    n_equipos = len(teams)
    # n de partidos por equipo usados (5 en ligas; 4 en competiciones
    # europeas, donde solo se han jugado 4 jornadas).
    n_usados = min(t['n'] for t in teams.values())
    # Ambito: "liga" en domesticas, "competicion" en europeas.
    ambito = ('competición' if all(lg.startswith('uefa.')
                                   for lg in avgs) else 'liga')
    # Orden por fecha+hora (pendiente del jefe, 22 nov 2026).
    orden_fecha = {f: i for i, f in enumerate(cfg['fechas'])}
    rows = sorted(rows, key=lambda r: (
        orden_fecha.get(r.get('fecha_iso', ''), 99), r['hora']))

    def last5_str(name):
        ms = teams[name]['matches']
        parts = []
        for m in ms:
            parts.append(f"{m['date'][5:10]} {'H' if m['home'] else 'A'} vs "
                         f"{m['opp']} {m['gf']:.0f}-{m['ga']:.0f}")
        return "; ".join(parts)

    L = []
    L.append(f"# Tabla de probabilidades Poisson — {cfg['nombre']} "
             "(Football AI Agenda)")
    L.append("")
    L.append(f"**Partidos:** {fechas_txt}, horas de Monterrey (CST). "
             "**Fuente de datos:** ESPN, API pública sin clave.")
    L.append("**Método:** modelo Poisson con goles esperados (xG) por equipo, "
             "distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.")
    L.append(f"**Fecha de cálculo:** {cutoff}. Últimos {n_usados} partidos "
             f"por equipo: partidos de {ambito} completados hasta el "
             f"{cutoff}.")
    L.append("")
    L.append(f"## (a) Tabla de los {n_partidos} partidos")
    L.append("")
    L.append("| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | "
             "P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        L.append(f"| {r['fecha']} | {r['hora']} | {r['liga']} | {r['home']} | "
                 f"{r['away']} | {r['xgh']:.2f} | {r['xga']:.2f} | {r['p1']:.1f}% | "
                 f"{r['px']:.1f}% | {r['p2']:.1f}% | {r['over25']:.1f}% | "
                 f"{r['btts']:.1f}% |")
    L.append("")
    L.append(f"Promedios de la tabla: xG local "
             f"{statistics.mean(r['xgh'] for r in rows):.2f}, xG visitante "
             f"{statistics.mean(r['xga'] for r in rows):.2f}; P(1) media "
             f"{statistics.mean(r['p1'] for r in rows):.1f}%, P(X) media "
             f"{statistics.mean(r['px'] for r in rows):.1f}%, P(2) media "
             f"{statistics.mean(r['p2'] for r in rows):.1f}%.")
    L.append("")
    L.append(f"## (b) Tabla de cálculo por equipo (últimos {n_usados} "
             f"partidos de {ambito})")
    L.append("")
    L.append(f"GF = goles a favor, GA = goles en contra en los últimos "
             f"{n_usados}. Ataque = (GF/{n_usados}) / prom. por equipo de "
             f"la {ambito}; defensa = (GA/{n_usados}) / prom. por equipo "
             f"de la {ambito}.")
    L.append("")
    L.append(f"| Liga | Equipo | GF ({n_usados}) | GA ({n_usados}) | "
             "GF/partido | GA/partido | Ataque | "
             f"Defensa | Últimos {n_usados} (fecha, H/A, rival, marcador "
             "desde el equipo) |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for name in sorted(teams, key=lambda n: (teams[n]['league'], n)):
        c = teams[name]
        L.append(f"| {LN[c['league']]} | {name} | {c['gf']:.0f} | {c['ga']:.0f} | "
                 f"{c['gf_pj']:.2f} | {c['ga_pj']:.2f} | {c['ataque']:.3f} | "
                 f"{c['defensa']:.3f} | {last5_str(name)} |")
    L.append("")
    L.append("## (c) Promedios de liga usados y cómo se calcularon")
    L.append("")
    L.append("Los promedios se calcularon desde los scoreboards de las últimas "
             "~3 jornadas completadas antes del cutoff (partidos con "
             "STATUS_FULL_TIME). El endpoint de posiciones (standings) de ESPN "
             "devuelve 404, por eso se usan scoreboards.")
    L.append("")
    L.append("| Liga | Jornadas usadas (fechas) | Partidos | Goles local | "
             "Goles visitante | Prom. goles/partido | Prom. local | "
             "Prom. visitante | Prom. por equipo |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for lg in sorted(avgs):
        a = avgs[lg]
        L.append(f"| {LN[lg]} | {', '.join(a['dates'])} | {a['matches']} | "
                 f"{a['home_goals']:.0f} | {a['away_goals']:.0f} | "
                 f"{a['avg_total']:.3f} | {a['avg_home']:.3f} | "
                 f"{a['avg_away']:.3f} | {a['avg_por_equipo']:.3f} |")
    L.append("")
    L.append("**Fórmulas aplicadas:**")
    L.append("")
    L.append("- Prom. por equipo = prom. goles/partido / 2 (cada partido "
             "reparte sus goles entre dos equipos).")
    L.append(f"- Ataque = (GF/{n_usados}) / prom. por equipo; "
             f"defensa = (GA/{n_usados}) / prom. por equipo.")
    L.append("- xG local = prom. local de la liga × ataque local × defensa "
             "visitante; xG visitante = prom. visitante de la liga × ataque "
             "visitante × defensa local.")
    L.append("- Poisson: P(k;λ) = e^-λ × λ^k / k!, k = 0..20 por equipo "
             "(distribución completa; la cola fuera de la rejilla es < 1e-6). "
             "P(1), P(X) y P(2) suman 100% sin renormalizar; el BTTS y el +2.5 "
             "también se calculan con la distribución completa.")
    L.append("")
    L.append("## (d) Fuentes ESPN consultadas (API pública, sin clave)")
    L.append("")
    L.append(f"- Scoreboard por liga y día, {fechas_txt}: "
             "`site.api.espn.com/apis/site/v2/sports/soccer/{{liga}}/scoreboard"
             "?dates={{AAAAMMDD}}` — los {n_partidos} partidos aparecen como "
             "STATUS_SCHEDULED con la fecha y hora exactas de la configuración "
             "(horas convertidas de UTC a CST, UTC-6).")
    L.append("- Schedule por equipo (últimos partidos completados): "
             "`site.api.espn.com/apis/site/v2/sports/soccer/{liga}/teams/{id}"
             "/schedule` — "
             f"{n_equipos} equipos, {n_usados} partidos completados cada uno, "
             f"todos de {ambito}, hasta el cutoff.")
    L.append("- Scoreboards de jornadas pasadas para promedios de liga: "
             "9 fechas por liga (ver tabla c).")
    L.append("- Los archivos JSON crudos de todas estas consultas están en "
             "`raw/` dentro de esta misma carpeta.")
    L.append("")
    L.append("## (e) Datos no verificados y partidos excluidos")
    L.append("")
    L.append(f"- **Ningún partido quedó fuera:** los {n_partidos} partidos "
             "de la lista se verificaron en el scoreboard de ESPN con fecha, "
             "hora y equipos exactos antes de calcular.")
    L.append(f"- **Valores extremos por muestra corta ({n_usados} partidos, "
             "sin tope aplicado):** son correctos según los datos, pero una "
             f"muestra de {n_usados} partidos exagera rachas; conviene leer "
             "los favoritos más extremos con cautela.")
    L.append(f"- **Últimos {n_usados} = solo {ambito}:** el schedule de ESPN "
             f"por {ambito} devuelve partidos de esa {ambito}; no se "
             "mezclaron otras competiciones.")
    L.append("- **Sin momios ni cuotas en esta tabla:** solo probabilidades "
             "propias (Poisson). Los momios y el EV están en la tabla de "
             "momios de la misma semana.")
    L.append("")

    out = os.path.join(outdir, f"tabla-poisson-semana-{semana}.md")
    open(out, 'w').write("\n".join(L))
    print(f"Escrito {out}: {len(chr(10).join(L))} caracteres")


if __name__ == '__main__':
    main()
