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


def p_over(xg_home, xg_away, linea):
    """P(total de goles > linea) con la distribucion Poisson completa.

    La linea es la PUBLICADA por el proveedor de momios (2.5 o 3.5).
    No usar el P(+2.5) de match_probs() con momios de linea 3.5:
    para linea 3.5 hay que recalcular con esta funcion.
    """
    ph = [pois(k, xg_home) for k in range(K_MAX + 1)]
    pa = [pois(k, xg_away) for k in range(K_MAX + 1)]
    p = 0.0
    for i in range(K_MAX + 1):
        for j in range(K_MAX + 1):
            if i + j > linea:
                p += ph[i] * pa[j]
    return p * 100


def p_spread_cover(xg_home, xg_away, linea_local):
    """P(el local cubre el spread) con la distribucion Poisson completa.

    linea_local es la linea del spread del LOCAL (p. ej. -2.5: el local
    cubre si gana por mas de 2.5 goles; +0.5: cubre si no pierde por
    mas de 0 goles, es decir, si gana o empata). En general el local
    cubre si (goles local - goles visitante) > -linea_local.
    P(visitante cubre) = 1 - P(local cubre) (las lineas son .5, sin push).
    """
    ph = [pois(k, xg_home) for k in range(K_MAX + 1)]
    pa = [pois(k, xg_away) for k in range(K_MAX + 1)]
    p = 0.0
    for i in range(K_MAX + 1):
        for j in range(K_MAX + 1):
            if i - j > -linea_local:
                p += ph[i] * pa[j]
    return p * 100


def expected_goals(avg_home, avg_away, ataque_home, defensa_away,
                   ataque_away, defensa_home):
    """xG local y visitante con la metodologia aprobada por el jefe.

    xG local = prom. local de la liga x ataque local x defensa visitante
    xG visitante = prom. visitante de la liga x ataque visitante x defensa local
    """
    return (avg_home * ataque_home * defensa_away,
            avg_away * ataque_away * defensa_home)


def attack_defense(gf, ga, avg_por_equipo, n=5):
    """Ataque y defensa desde los ultimos n partidos de la competicion.

    Denominador = promedio de goles POR EQUIPO de la competicion (prom.
    total / 2). Usar el promedio total como denominador dejaria los xG
    a ~1/4 de su valor real (metodologia aprobada por el jefe, 19 nov
    2026). n es el numero de partidos usados (5 en ligas domesticas;
    4 en competiciones europeas, donde solo se han jugado 4 jornadas).
    """
    return (gf / n) / avg_por_equipo, (ga / n) / avg_por_equipo
