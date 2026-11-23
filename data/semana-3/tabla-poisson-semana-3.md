# Tabla de probabilidades Poisson — Semana 3 (Football AI Agenda)

**Partidos:** 2026-12-04 al 2026-12-06, horas de Monterrey (CST). **Fuente de datos:** ESPN, API pública sin clave.
**Método:** modelo Poisson con goles esperados (xG) por equipo, distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.
**Fecha de cálculo:** 2026-11-22. Últimos 5 partidos por equipo: partidos de liga completados hasta el 2026-11-22.

## (a) Tabla de los 16 partidos

| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Vie 4 dic | 13:30 | Bundesliga | Bayern Munich | SC Paderborn 07 | 3.40 | 0.71 | 87.0% | 8.7% | 4.3% | 77.8% | 49.1% |
| Vie 4 dic | 13:45 | Serie A | Bologna | AS Roma | 2.42 | 2.47 | 39.8% | 18.6% | 41.7% | 86.6% | 83.4% |
| Sáb 5 dic | 06:30 | Premier League | Chelsea | Liverpool | 0.56 | 2.18 | 8.1% | 17.1% | 74.8% | 51.5% | 37.9% |
| Sáb 5 dic | 08:30 | Bundesliga | Bayer Leverkusen | Borussia Mönchengladbach | 2.43 | 1.06 | 67.5% | 17.7% | 14.9% | 67.8% | 59.7% |
| Sáb 5 dic | 11:30 | LaLiga | Villarreal | Real Sociedad | 1.77 | 1.83 | 37.9% | 21.9% | 40.2% | 69.7% | 69.7% |
| Sáb 5 dic | 11:30 | Bundesliga | Eintracht Frankfurt | Werder Bremen | 1.06 | 1.04 | 35.6% | 29.9% | 34.4% | 35.1% | 42.3% |
| Sáb 5 dic | 13:45 | Serie A | Napoli | Lecce | 3.22 | 0.52 | 88.4% | 8.4% | 3.2% | 72.0% | 38.9% |
| Sáb 5 dic | 14:00 | Premier League | Brentford | Manchester City | 2.01 | 1.19 | 56.4% | 21.5% | 22.1% | 61.9% | 60.2% |
| Sáb 5 dic | 14:00 | LaLiga | Barcelona | Celta Vigo | 3.77 | 0.80 | 88.6% | 7.5% | 3.9% | 83.4% | 53.7% |
| Dom 6 dic | 08:00 | Premier League | Newcastle United | Sunderland | 0.93 | 0.28 | 50.9% | 38.1% | 11.0% | 12.3% | 14.9% |
| Dom 6 dic | 08:30 | Bundesliga | Schalke 04 | Borussia Dortmund | 0.09 | 0.71 | 4.4% | 47.9% | 47.7% | 4.7% | 4.4% |
| Dom 6 dic | 09:15 | LaLiga | Athletic Club | Real Madrid | 0.89 | 2.79 | 9.2% | 13.9% | 76.9% | 71.1% | 55.2% |
| Dom 6 dic | 10:30 | Premier League | Tottenham Hotspur | Arsenal | 0.67 | 0.40 | 36.9% | 44.2% | 18.9% | 9.3% | 15.9% |
| Dom 6 dic | 11:00 | Serie A | Juventus | Udinese | 2.75 | 0.40 | 86.2% | 10.4% | 3.4% | 60.8% | 30.6% |
| Dom 6 dic | 13:45 | Serie A | AC Milan | Parma | 3.46 | 1.04 | 82.3% | 10.5% | 7.3% | 82.7% | 62.6% |
| Dom 6 dic | 14:00 | LaLiga | Atlético Madrid | Real Betis | 2.07 | 0.47 | 75.2% | 17.6% | 7.1% | 46.5% | 32.5% |

Promedios de la tabla: xG local 1.97, xG visitante 1.12; P(1) media 53.4%, P(X) media 20.9%, P(2) media 25.7%.

## (b) Tabla de cálculo por equipo (últimos 5 partidos de liga)

GF = goles a favor, GA = goles en contra en los últimos 5. Ataque = (GF/5) / prom. por equipo de la liga; defensa = (GA/5) / prom. por equipo de la liga.

| Liga | Equipo | GF (5) | GA (5) | GF/partido | GA/partido | Ataque | Defensa | Últimos 5 (fecha, H/A, rival, marcador desde el equipo) |
|---|---|---|---|---|---|---|---|---|
| Premier League | Arsenal | 7 | 2 | 1.40 | 0.40 | 1.145 | 0.327 | 11-21 A vs Newcastle United 2-2; 11-07 H vs Hull City 1-0; 11-01 A vs Liverpool 1-0; 10-24 H vs Everton 2-0; 10-18 A vs Nottingham Forest 1-0 |
| Premier League | Brentford | 6 | 7 | 1.20 | 1.40 | 0.982 | 1.145 | 11-08 A vs Brighton & Hove Albion 0-2; 10-31 H vs Nottingham Forest 2-0; 10-25 A vs Hull City 1-1; 10-17 H vs Liverpool 1-2; 10-10 A vs Aston Villa 2-2 |
| Premier League | Chelsea | 5 | 7 | 1.00 | 1.40 | 0.818 | 1.145 | 11-21 H vs Leeds United 1-4; 11-08 A vs Sunderland 0-1; 10-31 H vs Manchester United 2-0; 10-24 H vs Tottenham Hotspur 0-2; 10-17 A vs Everton 2-0 |
| Premier League | Liverpool | 11 | 3 | 2.20 | 0.60 | 1.800 | 0.491 | 11-22 H vs Manchester United 4-0; 11-08 A vs Crystal Palace 3-1; 11-01 H vs Arsenal 0-1; 10-25 H vs Brighton & Hove Albion 2-0; 10-17 A vs Brentford 2-1 |
| Premier League | Manchester City | 6 | 9 | 1.20 | 1.80 | 0.982 | 1.473 | 11-21 H vs Fulham 1-1; 11-07 A vs Nottingham Forest 1-3; 10-31 H vs Brighton & Hove Albion 0-1; 10-24 A vs Aston Villa 1-2; 10-17 H vs Ipswich Town 3-2 |
| Premier League | Newcastle United | 5 | 5 | 1.00 | 1.00 | 0.818 | 0.818 | 11-21 H vs Arsenal 2-2; 11-07 A vs Fulham 1-1; 11-02 H vs Everton 0-1; 10-25 A vs Crystal Palace 2-0; 10-17 H vs Aston Villa 0-1 |
| Premier League | Sunderland | 2 | 5 | 0.40 | 1.00 | 0.327 | 0.818 | 11-21 A vs Aston Villa 0-0; 11-08 H vs Chelsea 1-0; 10-31 A vs Coventry City 1-3; 10-25 H vs Leeds United 0-0; 10-18 A vs AFC Bournemouth 0-2 |
| Premier League | Tottenham Hotspur | 9 | 2 | 1.80 | 0.40 | 1.473 | 0.327 | 11-21 H vs Ipswich Town 2-0; 11-07 A vs Leeds United 0-1; 10-31 H vs Crystal Palace 2-0; 10-24 A vs Chelsea 2-0; 10-19 H vs Coventry City 3-1 |
| LaLiga | Athletic Club | 8 | 6 | 1.60 | 1.20 | 1.404 | 1.053 | 11-20 H vs Espanyol 0-1; 11-07 A vs Osasuna 1-1; 11-01 H vs Real Sociedad 2-1; 10-25 H vs Getafe 4-0; 10-21 A vs Levante 1-3 |
| LaLiga | Atlético Madrid | 8 | 2 | 1.60 | 0.40 | 1.404 | 0.351 | 11-22 A vs Getafe 3-0; 11-08 H vs Barcelona 1-2; 10-31 A vs Levante 2-0; 10-24 H vs Deportivo 1-0; 10-17 A vs Espanyol 1-0 |
| LaLiga | Barcelona | 17 | 8 | 3.40 | 1.60 | 2.982 | 1.404 | 11-22 H vs Villarreal 3-2; 11-08 A vs Atlético Madrid 2-1; 10-31 H vs Alavés 6-1; 10-25 H vs Real Madrid 1-2; 10-17 A vs Real Betis 5-2 |
| LaLiga | Celta Vigo | 3 | 6 | 0.60 | 1.20 | 0.526 | 1.053 | 11-21 A vs Real Madrid 1-2; 11-08 H vs Levante 0-0; 10-31 A vs Rayo Vallecano 0-3; 10-25 H vs Real Betis 0-0; 10-18 H vs Alavés 2-1 |
| LaLiga | Real Betis | 7 | 7 | 1.40 | 1.40 | 1.228 | 1.228 | 11-21 A vs Sevilla 1-1; 11-08 A vs Elche 2-0; 10-31 H vs Málaga 2-1; 10-25 A vs Celta Vigo 0-0; 10-17 H vs Barcelona 2-5 |
| LaLiga | Real Madrid | 14 | 3 | 2.80 | 0.60 | 2.456 | 0.526 | 11-21 H vs Celta Vigo 2-1; 11-07 A vs Valencia 3-0; 11-01 A vs Racing Santander 3-0; 10-25 A vs Barcelona 2-1; 10-18 H vs Sevilla 4-1 |
| LaLiga | Real Sociedad | 11 | 8 | 2.20 | 1.60 | 1.930 | 1.404 | 11-22 A vs Racing Santander 2-3; 11-08 H vs Rayo Vallecano 1-0; 11-01 A vs Athletic Club 1-2; 10-25 H vs Levante 2-1; 10-18 A vs Málaga 5-2 |
| LaLiga | Villarreal | 6 | 5 | 1.20 | 1.00 | 1.053 | 0.877 | 11-22 A vs Barcelona 2-3; 11-08 H vs Getafe 2-0; 10-30 H vs Espanyol 0-1; 10-24 A vs Valencia 2-1; 10-17 H vs Elche 0-0 |
| Bundesliga | Bayer Leverkusen | 10 | 9 | 2.00 | 1.80 | 1.350 | 1.215 | 11-21 H vs SC Paderborn 07 4-0; 11-08 A vs FC Cologne 2-1; 10-31 H vs VfB Stuttgart 2-4; 10-25 A vs TSG Hoffenheim 0-3; 10-18 H vs SC Freiburg 2-1 |
| Bundesliga | Bayern Munich | 14 | 6 | 2.80 | 1.20 | 1.890 | 0.810 | 11-20 H vs FC Cologne 1-1; 11-07 A vs Mainz 2-1; 10-31 H vs Borussia Dortmund 2-2; 10-25 A vs SC Freiburg 3-1; 10-17 H vs RB Leipzig 6-1 |
| Bundesliga | Borussia Dortmund | 6 | 3 | 1.20 | 0.60 | 0.810 | 0.405 | 11-21 A vs Borussia Mönchengladbach 1-0; 11-07 H vs SV Elversberg 2-1; 10-31 A vs Bayern Munich 2-2; 10-24 H vs Eintracht Frankfurt 1-0; 10-17 A vs 1. FC Union Berlin 0-0 |
| Bundesliga | Borussia Mönchengladbach | 5 | 8 | 1.00 | 1.60 | 0.675 | 1.080 | 11-21 H vs Borussia Dortmund 0-1; 11-06 A vs Hamburg SV 1-3; 10-31 H vs SC Paderborn 07 0-0; 10-23 A vs VfB Stuttgart 3-2; 10-18 H vs TSG Hoffenheim 1-2 |
| Bundesliga | Eintracht Frankfurt | 7 | 4 | 1.40 | 0.80 | 0.945 | 0.540 | 11-21 H vs TSG Hoffenheim 1-0; 11-07 A vs SC Paderborn 07 2-2; 11-01 H vs Hamburg SV 3-1; 10-24 A vs Borussia Dortmund 0-1; 10-16 H vs FC Cologne 1-0 |
| Bundesliga | SC Paderborn 07 | 5 | 8 | 1.00 | 1.60 | 0.675 | 1.080 | 11-21 A vs Bayer Leverkusen 0-4; 11-07 H vs Eintracht Frankfurt 2-2; 10-31 A vs Borussia Mönchengladbach 0-0; 10-24 H vs Hamburg SV 1-0; 10-17 A vs Werder Bremen 2-2 |
| Bundesliga | Schalke 04 | 1 | 5 | 0.20 | 1.00 | 0.135 | 0.675 | 11-21 H vs VfB Stuttgart 0-0; 11-08 A vs TSG Hoffenheim 1-2; 10-31 H vs RB Leipzig 0-2; 10-24 A vs FC Cologne 0-0; 10-17 H vs Mainz 0-1 |
| Bundesliga | Werder Bremen | 11 | 5 | 2.20 | 1.00 | 1.485 | 0.675 | 11-22 H vs Hamburg SV 4-0; 11-07 A vs VfB Stuttgart 0-1; 10-31 H vs TSG Hoffenheim 2-0; 10-24 A vs Mainz 3-2; 10-17 H vs SC Paderborn 07 2-2 |
| Serie A | AC Milan | 14 | 7 | 2.80 | 1.40 | 1.827 | 0.914 | 11-22 H vs Frosinone 5-1; 11-08 A vs Genoa 2-1; 10-31 H vs Internazionale 3-1; 10-28 H vs Bologna 2-4; 10-25 A vs Udinese 2-0 |
| Serie A | AS Roma | 20 | 8 | 4.00 | 1.60 | 2.611 | 1.044 | 11-21 A vs Parma 5-1; 11-07 H vs Sassuolo 3-0; 10-31 A vs Udinese 5-2; 10-27 H vs Cagliari 4-2; 10-24 A vs Napoli 3-3 |
| Serie A | Bologna | 11 | 5 | 2.20 | 1.00 | 1.436 | 0.653 | 11-22 H vs Udinese 1-1; 11-07 A vs Parma 2-1; 10-31 H vs Monza 2-1; 10-28 A vs AC Milan 4-2; 10-24 A vs Cagliari 2-0 |
| Serie A | Juventus | 10 | 4 | 2.00 | 0.80 | 1.305 | 0.522 | 11-22 H vs Venezia 4-0; 11-08 A vs Fiorentina 2-2; 11-01 H vs Napoli 2-0; 10-28 A vs Genoa 0-2; 10-25 A vs Lecce 2-0 |
| Serie A | Lecce | 3 | 13 | 0.60 | 2.60 | 0.392 | 1.697 | 11-21 A vs Lazio 0-3; 11-07 A vs Torino 1-1; 11-01 H vs Genoa 1-2; 10-29 A vs Frosinone 1-5; 10-25 H vs Juventus 0-2 |
| Serie A | Napoli | 9 | 7 | 1.80 | 1.40 | 1.175 | 0.914 | 11-21 H vs Torino 1-0; 11-08 H vs Lazio 1-1; 11-01 A vs Juventus 0-2; 10-28 A vs Monza 4-1; 10-24 H vs AS Roma 3-3 |
| Serie A | Parma | 6 | 9 | 1.20 | 1.80 | 0.783 | 1.175 | 11-21 H vs AS Roma 1-5; 11-07 H vs Bologna 1-2; 11-02 A vs Atalanta 3-0; 10-28 H vs Udinese 0-0; 10-24 A vs Lazio 1-2 |
| Serie A | Udinese | 4 | 10 | 0.80 | 2.00 | 0.522 | 1.305 | 11-22 A vs Bologna 1-1; 11-06 A vs Venezia 1-2; 10-31 H vs AS Roma 2-5; 10-28 A vs Parma 0-0; 10-25 H vs AC Milan 0-2 |

## (c) Promedios de liga usados y cómo se calcularon

Los promedios se calcularon desde los scoreboards de las últimas ~3 jornadas completadas antes del cutoff (partidos con STATUS_FULL_TIME). El endpoint de posiciones (standings) de ESPN devuelve 404, por eso se usan scoreboards.

| Liga | Jornadas usadas (fechas) | Partidos | Goles local | Goles visitante | Prom. goles/partido | Prom. local | Prom. visitante | Prom. por equipo |
|---|---|---|---|---|---|---|---|---|
| Premier League | 20261024, 20261025, 20261031, 20261101, 20261102, 20261106, 20261107, 20261108, 20261121 | 36 | 50 | 38 | 2.444 | 1.389 | 1.056 | 1.222 |
| LaLiga | 20261030, 20261031, 20261101, 20261102, 20261106, 20261107, 20261108, 20261120, 20261121 | 25 | 30 | 27 | 2.280 | 1.200 | 1.080 | 1.140 |
| Bundesliga | 20261025, 20261030, 20261031, 20261101, 20261106, 20261107, 20261108, 20261120, 20261121 | 27 | 45 | 35 | 2.963 | 1.667 | 1.296 | 1.481 |
| Serie A | 20261028, 20261029, 20261031, 20261101, 20261102, 20261106, 20261107, 20261108, 20261121 | 31 | 50 | 45 | 3.065 | 1.613 | 1.452 | 1.532 |

**Fórmulas aplicadas:**

- Prom. por equipo = prom. goles/partido / 2 (cada partido reparte sus goles entre dos equipos).
- Ataque = (GF/5) / prom. por equipo; defensa = (GA/5) / prom. por equipo.
- xG local = prom. local de la liga × ataque local × defensa visitante; xG visitante = prom. visitante de la liga × ataque visitante × defensa local.
- Poisson: P(k;λ) = e^-λ × λ^k / k!, k = 0..20 por equipo (distribución completa; la cola fuera de la rejilla es < 1e-6). P(1), P(X) y P(2) suman 100% sin renormalizar; el BTTS y el +2.5 también se calculan con la distribución completa.

## (d) Fuentes ESPN consultadas (API pública, sin clave)

- Scoreboard por liga y día, 2026-12-04 al 2026-12-06: `site.api.espn.com/apis/site/v2/sports/soccer/{{liga}}/scoreboard?dates={{AAAAMMDD}}` — los {n_partidos} partidos aparecen como STATUS_SCHEDULED con la fecha y hora exactas de la configuración (horas convertidas de UTC a CST, UTC-6).
- Schedule por equipo (últimos partidos completados): `site.api.espn.com/apis/site/v2/sports/soccer/{liga}/teams/{id}/schedule` — 32 equipos, 5 partidos completados cada uno, todos de liga, hasta el cutoff.
- Scoreboards de jornadas pasadas para promedios de liga: 9 fechas por liga (ver tabla c).
- Los archivos JSON crudos de todas estas consultas están en `raw/` dentro de esta misma carpeta.

## (e) Datos no verificados y partidos excluidos

- **Ningún partido quedó fuera:** los 16 partidos de la lista se verificaron en el scoreboard de ESPN con fecha, hora y equipos exactos antes de calcular.
- **Valores extremos por muestra corta (5 partidos, sin tope aplicado):** son correctos según los datos, pero una muestra de 5 partidos exagera rachas; conviene leer los favoritos más extremos con cautela.
- **Últimos 5 = solo liga:** el schedule de ESPN por liga devuelve partidos de esa liga; no se mezclaron otras competiciones.
- **Sin momios ni cuotas en esta tabla:** solo probabilidades propias (Poisson). Los momios y el EV están en la tabla de momios de la misma semana.
