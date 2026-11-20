"""Modelo Poisson para Football AI Agenda.

CORRECCION OBLIGATORIA (jefe, 19 nov 2026): el BTTS (ambos anotan) y el
+2.5 se calculan con la DISTRIBUCION COMPLETA, no sobre la tabla truncada
de 0-7 goles. El error anterior daba Real Madrid-Alaves 16.8% en vez de
21.1% correcto, y el +2.5 de ese mismo partido 72.7% en vez de 93.1%.

Por eso aqui se usa una rejilla de 0..20 goles por equipo: con los xG
maximos que maneja el proyecto (lambda ~5.6) la cola de 8+ goles es del
20% y NO se puede descartar; con 0..20 la masa que queda fuera es
< 1e-6 y el 1X2 suma 100% sin necesidad de renormalizar.
"""

import math

K_MAX = 20  # goles por equipo; cola fuera de la rejilla < 1e-6 para lambda <= 6


def pois(k, lam):
    """P(X = k) para X ~ Poisson(lam)."""
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def match_probs(xg_home, xg_away):
    """Probabilidades 1X2, +2.5 y BTTS con la distribucion Poisson completa.

    Devuelve porcentajes (0-100). El 1X2 suma 100% (sin renormalizar:
    la rejilla 0..20 ya cubre practicamente toda la masa).
    """
    ph = [pois(k, xg_home) for k in range(K_MAX + 1)]
    pa = [pois(k, xg_away) for k in range(K_MAX + 1)]
    p1 = px = p2 = over25 = btts = 0.0
    for i in range(K_MAX + 1):
        for j in range(K_MAX + 1):
            p = ph[i] * pa[j]
            if i > j:
                p1 += p
            elif i == j:
                px += p
            else:
                p2 += p
            if i + j > 2.5:
                over25 += p
            if i >= 1 and j >= 1:
                btts += p
    return {
        'p1': p1 * 100,
        'px': px * 100,
        'p2': p2 * 100,
        'over25': over25 * 100,
        'btts': btts * 100,
    }


def expected_goals(avg_home, avg_away, ataque_home, defensa_away,
                   ataque_away, defensa_home):
    """xG local y visitante con la metodologia aprobada por el jefe.

    xG local = prom. local de la liga x ataque local x defensa visitante
    xG visitante = prom. visitante de la liga x ataque visitante x defensa local
    """
    return (avg_home * ataque_home * defensa_away,
            avg_away * ataque_away * defensa_home)


def attack_defense(gf5, ga5, avg_por_equipo):
    """Ataque y defensa desde los ultimos 5 partidos de liga.

    Denominador = promedio de goles POR EQUIPO de la liga (prom. total / 2).
    Usar el promedio total como denominador dejaria los xG a ~1/4 de su
    valor real (metodologia aprobada por el jefe, 19 nov 2026).
    """
    return (gf5 / 5) / avg_por_equipo, (ga5 / 5) / avg_por_equipo
