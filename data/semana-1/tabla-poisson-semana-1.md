# Tabla de probabilidades Poisson — Semana 1 (Football AI Agenda)

**Partidos:** 2026-11-20 al 2026-11-22, horas de Monterrey (CST). **Fuente de datos:** ESPN, API pública sin clave.
**Método:** modelo Poisson con goles esperados (xG) por equipo, distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.
**Fecha de cálculo:** 2026-11-19. Últimos 5 partidos por equipo: partidos de liga completados hasta el 2026-11-19.

## (a) Tabla de los 16 partidos

| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Vie 20 nov | 13:30 | Bundesliga | Bayern Munich | FC Cologne | 2.30 | 0.60 | 76.0% | 16.1% | 7.9% | 55.4% | 40.5% |
| Vie 20 nov | 14:00 | LaLiga | Athletic Club | Espanyol | 1.26 | 0.45 | 56.9% | 30.0% | 13.2% | 24.3% | 25.7% |
| Vie 20 nov | 19:00 | Liga MX | Puebla | Atlético de San Luis | 0.71 | 0.94 | 26.3% | 34.4% | 39.2% | 22.7% | 30.8% |
| Vie 20 nov | 21:00 | Liga MX | FC Juárez | Atlas | 1.51 | 1.87 | 31.4% | 22.3% | 46.2% | 65.7% | 66.0% |
| Vie 20 nov | 21:10 | Liga MX | Tijuana | Atlante | 2.27 | 0.75 | 71.8% | 17.5% | 10.7% | 58.1% | 47.2% |
| Sáb 21 nov | 06:30 | Premier League | Manchester City | Fulham | 1.25 | 1.18 | 38.2% | 27.4% | 34.4% | 43.8% | 49.4% |
| Sáb 21 nov | 11:30 | Premier League | Newcastle United | Arsenal | 0.16 | 1.44 | 3.8% | 25.1% | 71.1% | 21.6% | 11.1% |
| Sáb 21 nov | 11:30 | LaLiga | Sevilla | Real Betis | 2.20 | 3.27 | 24.7% | 15.9% | 59.4% | 91.0% | 85.5% |
| Sáb 21 nov | 14:00 | LaLiga | Real Madrid | Celta Vigo | 2.04 | 0.12 | 83.8% | 14.5% | 1.6% | 36.6% | 9.8% |
| Sáb 21 nov | 16:50 | Liga MX | Pachuca | Toluca | 1.66 | 1.40 | 43.8% | 23.8% | 32.4% | 59.2% | 61.1% |
| Sáb 21 nov | 19:00 | Liga MX | Pumas UNAM | Monterrey | 1.59 | 1.31 | 44.0% | 24.5% | 31.5% | 55.4% | 58.1% |
| Dom 22 nov | 07:00 | LaLiga | Barcelona | Villarreal | 2.00 | 0.71 | 67.6% | 20.0% | 12.3% | 51.0% | 44.1% |
| Dom 22 nov | 10:30 | Premier League | Liverpool | Manchester United | 3.02 | 1.06 | 76.6% | 13.3% | 10.0% | 77.3% | 62.1% |
| Dom 22 nov | 13:45 | Serie A | Atalanta | Internazionale | 1.06 | 2.88 | 11.0% | 14.3% | 74.7% | 75.3% | 61.6% |
| Dom 22 nov | 14:00 | LaLiga | Getafe | Atlético Madrid | 0.47 | 2.29 | 6.1% | 15.2% | 78.7% | 52.1% | 33.7% |
| Dom 22 nov | 17:07 | Liga MX | Guadalajara | Cruz Azul | 1.01 | 1.40 | 27.1% | 26.9% | 46.0% | 43.3% | 47.9% |

Promedios de la tabla: xG local 1.53, xG visitante 1.35; P(1) media 43.1%, P(X) media 21.3%, P(2) media 35.6%.

## (b) Tabla de cálculo por equipo (últimos 5 partidos de liga)

GF = goles a favor, GA = goles en contra en los últimos 5. Ataque = (GF/5) / prom. por equipo de la liga; defensa = (GA/5) / prom. por equipo de la liga.

| Liga | Equipo | GF (5) | GA (5) | GF/partido | GA/partido | Ataque | Defensa | Últimos 5 (fecha, H/A, rival, marcador desde el equipo) |
|---|---|---|---|---|---|---|---|---|
| Premier League | Arsenal | 7 | 1 | 1.40 | 0.20 | 1.200 | 0.171 | 11-07 H vs Hull City 1-0; 11-01 A vs Liverpool 1-0; 10-24 H vs Everton 2-0; 10-18 A vs Nottingham Forest 1-0; 10-10 H vs Leeds United 2-1 |
| Premier League | Fulham | 5 | 4 | 1.00 | 0.80 | 0.857 | 0.686 | 11-07 H vs Newcastle United 1-1; 10-31 A vs Aston Villa 1-1; 10-24 A vs Coventry City 1-0; 10-17 H vs Hull City 1-0; 10-10 A vs Ipswich Town 1-2 |
| Premier League | Liverpool | 7 | 6 | 1.40 | 1.20 | 1.200 | 1.029 | 11-08 A vs Crystal Palace 3-1; 11-01 H vs Arsenal 0-1; 10-25 H vs Brighton & Hove Albion 2-0; 10-17 A vs Brentford 2-1; 10-11 H vs Manchester City 0-3 |
| Premier League | Manchester City | 8 | 8 | 1.60 | 1.60 | 1.371 | 1.371 | 11-07 A vs Nottingham Forest 1-3; 10-31 H vs Brighton & Hove Albion 0-1; 10-24 A vs Aston Villa 1-2; 10-17 H vs Ipswich Town 3-2; 10-11 A vs Liverpool 3-0 |
| Premier League | Manchester United | 6 | 11 | 1.20 | 2.20 | 1.029 | 1.886 | 11-08 H vs Aston Villa 4-4; 10-31 A vs Chelsea 0-2; 10-25 H vs AFC Bournemouth 0-3; 10-18 A vs Leeds United 1-1; 10-10 H vs Tottenham Hotspur 1-1 |
| Premier League | Newcastle United | 4 | 7 | 0.80 | 1.40 | 0.686 | 1.200 | 11-07 A vs Fulham 1-1; 11-02 H vs Everton 0-1; 10-25 A vs Crystal Palace 2-0; 10-17 H vs Aston Villa 0-1; 10-12 A vs Coventry City 1-4 |
| LaLiga | Athletic Club | 8 | 5 | 1.60 | 1.00 | 1.379 | 0.862 | 11-07 A vs Osasuna 1-1; 11-01 H vs Real Sociedad 2-1; 10-25 H vs Getafe 4-0; 10-21 A vs Levante 1-3; 10-17 A vs Valencia 0-0 |
| LaLiga | Atlético Madrid | 7 | 3 | 1.40 | 0.60 | 1.207 | 0.517 | 11-08 H vs Barcelona 1-2; 10-31 A vs Levante 2-0; 10-24 H vs Deportivo 1-0; 10-17 A vs Espanyol 1-0; 10-10 A vs Alavés 2-1 |
| LaLiga | Barcelona | 17 | 6 | 3.40 | 1.20 | 2.931 | 1.034 | 11-08 A vs Atlético Madrid 2-1; 10-31 H vs Alavés 6-1; 10-25 H vs Real Madrid 1-2; 10-17 A vs Real Betis 5-2; 10-10 H vs Getafe 3-0 |
| LaLiga | Celta Vigo | 2 | 4 | 0.40 | 0.80 | 0.345 | 0.690 | 11-08 H vs Levante 0-0; 10-31 A vs Rayo Vallecano 0-3; 10-25 H vs Real Betis 0-0; 10-18 H vs Alavés 2-1; 10-11 A vs Elche 0-0 |
| LaLiga | Espanyol | 3 | 4 | 0.60 | 0.80 | 0.517 | 0.690 | 11-07 H vs Deportivo 0-0; 10-30 A vs Villarreal 1-0; 10-24 A vs Racing Santander 1-2; 10-17 H vs Atlético Madrid 0-1; 10-09 A vs Málaga 1-1 |
| LaLiga | Getafe | 4 | 11 | 0.80 | 2.20 | 0.690 | 1.897 | 11-08 A vs Villarreal 0-2; 11-01 H vs Sevilla 3-1; 10-25 A vs Athletic Club 0-4; 10-19 H vs Rayo Vallecano 1-1; 10-10 A vs Barcelona 0-3 |
| LaLiga | Real Betis | 11 | 8 | 2.20 | 1.60 | 1.897 | 1.379 | 11-08 A vs Elche 2-0; 10-31 H vs Málaga 2-1; 10-25 A vs Celta Vigo 0-0; 10-17 H vs Barcelona 2-5; 10-11 H vs Osasuna 5-2 |
| LaLiga | Real Madrid | 13 | 2 | 2.60 | 0.40 | 2.241 | 0.345 | 11-07 A vs Valencia 3-0; 11-01 A vs Racing Santander 3-0; 10-25 A vs Barcelona 2-1; 10-18 H vs Sevilla 4-1; 10-10 H vs Villarreal 1-0 |
| LaLiga | Sevilla | 7 | 10 | 1.40 | 2.00 | 1.207 | 1.724 | 11-06 H vs Alavés 0-0; 11-01 A vs Getafe 1-3; 10-26 H vs Osasuna 2-0; 10-18 A vs Real Madrid 1-4; 10-12 A vs Levante 3-3 |
| LaLiga | Villarreal | 4 | 3 | 0.80 | 0.60 | 0.690 | 0.517 | 11-08 H vs Getafe 2-0; 10-30 H vs Espanyol 0-1; 10-24 A vs Valencia 2-1; 10-17 H vs Elche 0-0; 10-10 A vs Real Madrid 0-1 |
| Bundesliga | Bayern Munich | 15 | 7 | 3.00 | 1.40 | 1.952 | 0.911 | 11-07 A vs Mainz 2-1; 10-31 H vs Borussia Dortmund 2-2; 10-25 A vs SC Freiburg 3-1; 10-17 H vs RB Leipzig 6-1; 10-10 A vs FC Augsburg 2-2 |
| Bundesliga | FC Cologne | 4 | 5 | 0.80 | 1.00 | 0.520 | 0.651 | 11-08 H vs Bayer Leverkusen 1-2; 11-01 A vs 1. FC Union Berlin 1-1; 10-24 H vs Schalke 04 0-0; 10-16 A vs Eintracht Frankfurt 0-1; 10-11 H vs Borussia Mönchengladbach 2-1 |
| Serie A | Atalanta | 9 | 12 | 1.80 | 2.40 | 1.069 | 1.426 | 11-08 A vs Monza 1-0; 11-02 H vs Parma 0-3; 10-29 A vs Fiorentina 2-2; 10-25 H vs Frosinone 4-4; 10-18 A vs AC Milan 2-3 |
| Serie A | Internazionale | 10 | 5 | 2.00 | 1.00 | 1.188 | 0.594 | 11-08 H vs Como 2-0; 10-31 A vs AC Milan 1-3; 10-28 A vs Venezia 2-0; 10-25 H vs Fiorentina 2-1; 10-17 A vs Bologna 3-1 |
| Liga MX | Atlante | 4 | 9 | 0.80 | 1.80 | 0.486 | 1.094 | 11-07 H vs Santos 0-2; 11-01 A vs Guadalajara 2-4; 10-24 H vs Atlético de San Luis 0-1; 10-21 A vs FC Juárez 1-0; 10-17 H vs Pumas UNAM 1-2 |
| Liga MX | Atlas | 10 | 12 | 2.00 | 2.40 | 1.215 | 1.458 | 11-07 H vs Pachuca 1-4; 10-31 A vs Atlético de San Luis 1-0; 10-25 H vs Puebla 4-3; 10-22 H vs América 2-5; 10-17 A vs Necaxa 2-0 |
| Liga MX | Atlético de San Luis | 4 | 4 | 0.80 | 0.80 | 0.486 | 0.486 | 11-07 H vs FC Juárez 0-1; 10-31 H vs Atlas 0-1; 10-24 A vs Atlante 1-0; 10-21 H vs Querétaro 2-1; 10-18 A vs Toluca 1-1 |
| Liga MX | Cruz Azul | 15 | 5 | 3.00 | 1.00 | 1.823 | 0.608 | 11-08 A vs Tigres UANL 3-2; 11-02 H vs León 2-1; 10-26 A vs Querétaro 3-1; 10-22 A vs Pachuca 2-1; 10-18 H vs FC Juárez 5-0 |
| Liga MX | FC Juárez | 5 | 8 | 1.00 | 1.60 | 0.608 | 0.972 | 11-07 A vs Atlético de San Luis 1-0; 10-31 H vs Querétaro 3-1; 10-24 A vs Necaxa 1-1; 10-21 H vs Atlante 0-1; 10-18 A vs Cruz Azul 0-5 |
| Liga MX | Guadalajara | 8 | 4 | 1.60 | 0.80 | 0.972 | 0.486 | 11-09 A vs León 1-1; 11-01 H vs Atlante 4-2; 10-25 A vs Monterrey 1-0; 10-21 H vs Necaxa 1-0; 10-17 H vs Tigres UANL 1-1 |
| Liga MX | Monterrey | 8 | 9 | 1.60 | 1.80 | 0.972 | 1.094 | 11-14 A vs Querétaro 1-0; 11-08 A vs Toluca 0-4; 11-01 H vs Tijuana 3-3; 10-25 H vs Guadalajara 0-1; 10-22 A vs Puebla 4-1 |
| Liga MX | Pachuca | 11 | 6 | 2.20 | 1.20 | 1.337 | 0.729 | 11-07 A vs Atlas 4-1; 10-31 H vs Tigres UANL 3-0; 10-26 A vs América 2-1; 10-22 H vs Cruz Azul 1-2; 10-19 A vs Monterrey 1-2 |
| Liga MX | Puebla | 7 | 10 | 1.40 | 2.00 | 0.851 | 1.215 | 11-09 A vs Querétaro 2-0; 10-31 H vs Pumas UNAM 1-2; 10-25 A vs Atlas 3-4; 10-22 H vs Monterrey 1-4; 10-17 A vs Tijuana 0-0 |
| Liga MX | Pumas UNAM | 7 | 7 | 1.40 | 1.40 | 0.851 | 0.851 | 11-08 H vs América 2-2; 10-31 A vs Puebla 2-1; 10-25 H vs Tigres UANL 1-1; 10-22 A vs Santos 0-2; 10-17 A vs Atlante 2-1 |
| Liga MX | Tijuana | 10 | 8 | 2.00 | 1.60 | 1.215 | 0.972 | 11-07 A vs Necaxa 0-1; 11-01 A vs Monterrey 3-3; 10-29 A vs América 1-1; 10-26 H vs Santos 4-1; 10-22 A vs Toluca 2-2 |
| Liga MX | Toluca | 10 | 6 | 2.00 | 1.20 | 1.215 | 0.729 | 11-08 H vs Monterrey 4-0; 11-01 A vs América 2-2; 10-24 A vs León 1-1; 10-22 H vs Tijuana 2-2; 10-18 H vs Atlético de San Luis 1-1 |

## (c) Promedios de liga usados y cómo se calcularon

Los promedios se calcularon desde los scoreboards de las últimas ~3 jornadas completadas antes del cutoff (partidos con STATUS_FULL_TIME). El endpoint de posiciones (standings) de ESPN devuelve 404, por eso se usan scoreboards.

| Liga | Jornadas usadas (fechas) | Partidos | Goles local | Goles visitante | Prom. goles/partido | Prom. local | Prom. visitante | Prom. por equipo |
|---|---|---|---|---|---|---|---|---|
| Premier League | 20261023, 20261024, 20261025, 20261031, 20261101, 20261102, 20261106, 20261107, 20261108 | 30 | 40 | 30 | 2.333 | 1.333 | 1.000 | 1.167 |
| LaLiga | 20261025, 20261026, 20261030, 20261031, 20261101, 20261102, 20261106, 20261107, 20261108 | 25 | 33 | 25 | 2.320 | 1.320 | 1.000 | 1.160 |
| Bundesliga | 20261023, 20261024, 20261025, 20261030, 20261031, 20261101, 20261106, 20261107, 20261108 | 27 | 49 | 34 | 3.074 | 1.815 | 1.259 | 1.537 |
| Serie A | 20261027, 20261028, 20261029, 20261031, 20261101, 20261102, 20261106, 20261107, 20261108 | 30 | 50 | 51 | 3.367 | 1.667 | 1.700 | 1.683 |
| Liga MX | 20261025, 20261028, 20261030, 20261031, 20261101, 20261106, 20261107, 20261108, 20261114 | 24 | 41 | 38 | 3.292 | 1.708 | 1.583 | 1.646 |

**Fórmulas aplicadas:**

- Prom. por equipo = prom. goles/partido / 2 (cada partido reparte sus goles entre dos equipos).
- Ataque = (GF/5) / prom. por equipo; defensa = (GA/5) / prom. por equipo.
- xG local = prom. local de la liga × ataque local × defensa visitante; xG visitante = prom. visitante de la liga × ataque visitante × defensa local.
- Poisson: P(k;λ) = e^-λ × λ^k / k!, k = 0..20 por equipo (distribución completa; la cola fuera de la rejilla es < 1e-6). P(1), P(X) y P(2) suman 100% sin renormalizar; el BTTS y el +2.5 también se calculan con la distribución completa.

## (d) Fuentes ESPN consultadas (API pública, sin clave)

- Scoreboard por liga y día, 2026-11-20 al 2026-11-22: `site.api.espn.com/apis/site/v2/sports/soccer/{{liga}}/scoreboard?dates={{AAAAMMDD}}` — los 16 partidos aparecen como STATUS_SCHEDULED con la fecha y hora exactas de la configuración (horas convertidas de UTC a CST, UTC-6).
- Schedule por equipo (últimos 5 completados): `site.api.espn.com/apis/site/v2/sports/soccer/{liga}/teams/{id}/schedule` — 32 equipos, 5 partidos completados cada uno, todos de liga, hasta el cutoff.
- Scoreboards de jornadas pasadas para promedios de liga: 9 fechas por liga (ver tabla c).
- Los archivos JSON crudos de todas estas consultas están en `raw/` dentro de esta misma carpeta.

## (e) Datos no verificados y partidos excluidos

- **Ningún partido quedó fuera:** los 16 partidos de la lista se verificaron en el scoreboard de ESPN con fecha, hora y equipos exactos antes de calcular.
- **Valores extremos por muestra corta (5 partidos, sin tope aplicado):** son correctos según los datos, pero una muestra de 5 partidos exagera rachas; conviene leer los favoritos más extremos con cautela.
- **Últimos 5 = solo liga:** el schedule de ESPN por liga devuelve partidos de esa liga; no se mezclaron copas ni Champions.
- **Sin momios ni cuotas en esta tabla:** solo probabilidades propias (Poisson). Los momios llegan en la Semana 3.
