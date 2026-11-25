# Tabla de probabilidades Poisson — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-25 al 2026-11-29, horas de Monterrey (CST). **Fuente de datos:** ESPN, API pública sin clave.
**Método:** modelo Poisson con goles esperados (xG) por equipo, distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.
**Fecha de cálculo:** 2026-11-19. Últimos 5 partidos por equipo: partidos de liga completados hasta el 2026-11-19.

## (a) Tabla de los 24 partidos

| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mié 25 nov | 19:00 | Liga MX | Toluca | Atlas | 3.03 | 1.40 | 70.2% | 15.0% | 14.9% | 81.8% | 71.8% |
| Mié 25 nov | 21:10 | Liga MX | Monterrey | América | 1.82 | 2.31 | 30.7% | 19.8% | 49.5% | 78.0% | 75.5% |
| Jue 26 nov | 19:00 | Liga MX | Pachuca | Guadalajara | 1.11 | 1.12 | 35.3% | 28.9% | 35.9% | 38.6% | 45.2% |
| Jue 26 nov | 21:10 | Liga MX | León | Cruz Azul | 1.01 | 3.16 | 8.6% | 12.1% | 79.3% | 78.5% | 60.8% |
| Vie 27 nov | 13:30 | Bundesliga | Werder Bremen | Borussia Mönchengladbach | 2.49 | 0.90 | 72.2% | 16.4% | 11.5% | 65.7% | 54.2% |
| Vie 27 nov | 13:45 | Serie A | Venezia | Bologna | 0.49 | 1.32 | 13.9% | 28.8% | 57.3% | 27.3% | 28.6% |
| Vie 27 nov | 14:00 | Premier League | Nottingham Forest | Chelsea | 0.78 | 2.12 | 12.7% | 19.2% | 68.1% | 55.4% | 47.8% |
| Vie 27 nov | 14:00 | LaLiga | Levante | Racing Santander | 1.77 | 1.07 | 53.7% | 23.4% | 22.9% | 53.9% | 54.5% |
| Sáb 28 nov | 08:30 | Bundesliga | Hamburg SV | Bayern Munich | 1.72 | 2.24 | 29.9% | 20.2% | 49.8% | 75.6% | 73.4% |
| Sáb 28 nov | 09:00 | Premier League | Manchester United | Brentford | 1.65 | 1.94 | 33.2% | 21.8% | 45.1% | 69.5% | 69.1% |
| Sáb 28 nov | 11:30 | LaLiga | Elche | Atlético Madrid | 0.35 | 0.62 | 17.7% | 46.4% | 36.0% | 7.6% | 13.8% |
| Sáb 28 nov | 11:30 | Bundesliga | VfB Stuttgart | Eintracht Frankfurt | 2.77 | 0.77 | 79.0% | 13.3% | 7.7% | 68.5% | 50.2% |
| Sáb 28 nov | 13:45 | Serie A | Internazionale | Genoa | 1.18 | 0.72 | 46.7% | 30.7% | 22.6% | 29.5% | 35.5% |
| Sáb 28 nov | 14:00 | LaLiga | Real Madrid | Alavés | 5.61 | 0.24 | 99.0% | 0.8% | 0.1% | 93.1% | 21.1% |
| Sáb 28 nov | 19:00 | Liga MX | Atlas | Toluca | 1.51 | 2.81 | 18.8% | 16.7% | 64.5% | 80.5% | 73.3% |
| Sáb 28 nov | 21:10 | Liga MX | América | Monterrey | 2.50 | 1.68 | 55.6% | 18.9% | 25.5% | 78.7% | 74.7% |
| Dom 29 nov | 06:00 | Premier League | Everton | Liverpool | 1.41 | 1.44 | 36.8% | 25.0% | 38.2% | 54.3% | 57.7% |
| Dom 29 nov | 08:00 | Serie A | Sassuolo | Napoli | 1.13 | 3.65 | 7.3% | 10.0% | 82.7% | 85.5% | 65.9% |
| Dom 29 nov | 09:15 | LaLiga | Deportivo | Barcelona | 1.18 | 3.03 | 11.6% | 13.9% | 74.6% | 79.1% | 65.8% |
| Dom 29 nov | 10:30 | Premier League | Arsenal | Manchester City | 2.19 | 0.24 | 83.1% | 14.0% | 3.0% | 43.8% | 18.6% |
| Dom 29 nov | 12:30 | Bundesliga | Borussia Dortmund | Bayer Leverkusen | 2.58 | 1.07 | 70.0% | 16.5% | 13.5% | 70.6% | 60.6% |
| Dom 29 nov | 13:45 | Serie A | Como | Juventus | 1.48 | 0.58 | 59.4% | 26.2% | 14.3% | 33.9% | 33.8% |
| Dom 29 nov | 19:07 | Liga MX | Guadalajara | Pachuca | 1.21 | 1.03 | 40.2% | 28.7% | 31.1% | 38.8% | 45.1% |
| Dom 29 nov | 21:00 | Liga MX | Cruz Azul | León | 3.41 | 0.94 | 83.4% | 10.2% | 6.4% | 80.8% | 58.7% |

Promedios de la tabla: xG local 1.85, xG visitante 1.52; P(1) media 44.5%, P(X) media 19.9%, P(2) media 35.6%.

## (b) Tabla de cálculo por equipo (últimos 5 partidos de liga)

GF = goles a favor, GA = goles en contra en los últimos 5. Ataque = (GF/5) / prom. por equipo de la liga; defensa = (GA/5) / prom. por equipo de la liga.

| Liga | Equipo | GF (5) | GA (5) | GF/partido | GA/partido | Ataque | Defensa | Últimos 5 (fecha, H/A, rival, marcador desde el equipo) |
|---|---|---|---|---|---|---|---|---|
| Premier League | Arsenal | 7 | 1 | 1.40 | 0.20 | 1.200 | 0.171 | 11-07 H vs Hull City 1-0; 11-01 A vs Liverpool 1-0; 10-24 H vs Everton 2-0; 10-18 A vs Nottingham Forest 1-0; 10-10 H vs Leeds United 2-1 |
| Premier League | Brentford | 6 | 7 | 1.20 | 1.40 | 1.029 | 1.200 | 11-08 A vs Brighton & Hove Albion 0-2; 10-31 H vs Nottingham Forest 2-0; 10-25 A vs Hull City 1-1; 10-17 H vs Liverpool 1-2; 10-10 A vs Aston Villa 2-2 |
| Premier League | Chelsea | 9 | 4 | 1.80 | 0.80 | 1.543 | 0.686 | 11-08 A vs Sunderland 0-1; 10-31 H vs Manchester United 2-0; 10-24 H vs Tottenham Hotspur 0-2; 10-17 A vs Everton 2-0; 10-10 H vs AFC Bournemouth 5-1 |
| Premier League | Everton | 6 | 7 | 1.20 | 1.40 | 1.029 | 1.200 | 11-06 H vs Coventry City 3-1; 11-02 A vs Newcastle United 1-0; 10-24 A vs Arsenal 0-2; 10-17 H vs Chelsea 0-2; 10-11 A vs Hull City 2-2 |
| Premier League | Liverpool | 7 | 6 | 1.40 | 1.20 | 1.200 | 1.029 | 11-08 A vs Crystal Palace 3-1; 11-01 H vs Arsenal 0-1; 10-25 H vs Brighton & Hove Albion 2-0; 10-17 A vs Brentford 2-1; 10-11 H vs Manchester City 0-3 |
| Premier League | Manchester City | 8 | 8 | 1.60 | 1.60 | 1.371 | 1.371 | 11-07 A vs Nottingham Forest 1-3; 10-31 H vs Brighton & Hove Albion 0-1; 10-24 A vs Aston Villa 1-2; 10-17 H vs Ipswich Town 3-2; 10-11 A vs Liverpool 3-0 |
| Premier League | Manchester United | 6 | 11 | 1.20 | 2.20 | 1.029 | 1.886 | 11-08 H vs Aston Villa 4-4; 10-31 A vs Chelsea 0-2; 10-25 H vs AFC Bournemouth 0-3; 10-18 A vs Leeds United 1-1; 10-10 H vs Tottenham Hotspur 1-1 |
| Premier League | Nottingham Forest | 5 | 8 | 1.00 | 1.60 | 0.857 | 1.371 | 11-07 H vs Manchester City 3-1; 10-31 A vs Brentford 0-2; 10-23 A vs Ipswich Town 1-1; 10-18 H vs Arsenal 0-1; 10-11 A vs Crystal Palace 1-3 |
| LaLiga | Alavés | 4 | 11 | 0.80 | 2.20 | 0.690 | 1.897 | 11-06 A vs Sevilla 0-0; 10-31 A vs Barcelona 1-6; 10-23 H vs Málaga 1-1; 10-18 A vs Celta Vigo 1-2; 10-10 H vs Atlético Madrid 1-2 |
| LaLiga | Atlético Madrid | 7 | 3 | 1.40 | 0.60 | 1.207 | 0.517 | 11-08 H vs Barcelona 1-2; 10-31 A vs Levante 2-0; 10-24 H vs Deportivo 1-0; 10-17 A vs Espanyol 1-0; 10-10 A vs Alavés 2-1 |
| LaLiga | Barcelona | 17 | 6 | 3.40 | 1.20 | 2.931 | 1.034 | 11-08 A vs Atlético Madrid 2-1; 10-31 H vs Alavés 6-1; 10-25 H vs Real Madrid 1-2; 10-17 A vs Real Betis 5-2; 10-10 H vs Getafe 3-0 |
| LaLiga | Deportivo | 5 | 6 | 1.00 | 1.20 | 0.862 | 1.034 | 11-07 A vs Espanyol 0-0; 11-02 H vs Osasuna 2-1; 10-24 A vs Atlético Madrid 0-1; 10-16 H vs Levante 1-1; 10-11 A vs Real Sociedad 2-3 |
| LaLiga | Elche | 3 | 3 | 0.60 | 0.60 | 0.517 | 0.517 | 11-08 H vs Real Betis 0-2; 11-01 H vs Valencia 0-1; 10-24 A vs Rayo Vallecano 3-0; 10-17 A vs Villarreal 0-0; 10-11 H vs Celta Vigo 0-0 |
| LaLiga | Levante | 5 | 6 | 1.00 | 1.20 | 0.862 | 1.034 | 11-08 A vs Celta Vigo 0-0; 10-31 H vs Atlético Madrid 0-2; 10-25 A vs Real Sociedad 1-2; 10-21 H vs Athletic Club 3-1; 10-16 A vs Deportivo 1-1 |
| LaLiga | Racing Santander | 6 | 9 | 1.20 | 1.80 | 1.034 | 1.552 | 11-07 A vs Málaga 2-1; 11-01 H vs Real Madrid 0-3; 10-24 H vs Espanyol 2-1; 10-18 A vs Osasuna 0-2; 10-11 H vs Valencia 2-2 |
| LaLiga | Real Madrid | 13 | 2 | 2.60 | 0.40 | 2.241 | 0.345 | 11-07 A vs Valencia 3-0; 11-01 A vs Racing Santander 3-0; 10-25 A vs Barcelona 2-1; 10-18 H vs Sevilla 4-1; 10-10 H vs Villarreal 1-0 |
| Bundesliga | Bayer Leverkusen | 10 | 12 | 2.00 | 2.40 | 1.301 | 1.561 | 11-08 A vs FC Cologne 2-1; 10-31 H vs VfB Stuttgart 2-4; 10-25 A vs TSG Hoffenheim 0-3; 10-18 H vs SC Freiburg 2-1; 10-10 A vs Mainz 4-3 |
| Bundesliga | Bayern Munich | 15 | 7 | 3.00 | 1.40 | 1.952 | 0.911 | 11-07 A vs Mainz 2-1; 10-31 H vs Borussia Dortmund 2-2; 10-25 A vs SC Freiburg 3-1; 10-17 H vs RB Leipzig 6-1; 10-10 A vs FC Augsburg 2-2 |
| Bundesliga | Borussia Dortmund | 7 | 5 | 1.40 | 1.00 | 0.911 | 0.651 | 11-07 H vs SV Elversberg 2-1; 10-31 A vs Bayern Munich 2-2; 10-24 H vs Eintracht Frankfurt 1-0; 10-17 A vs 1. FC Union Berlin 0-0; 10-09 H vs Werder Bremen 2-2 |
| Bundesliga | Borussia Mönchengladbach | 6 | 9 | 1.20 | 1.80 | 0.781 | 1.171 | 11-06 A vs Hamburg SV 1-3; 10-31 H vs SC Paderborn 07 0-0; 10-23 A vs VfB Stuttgart 3-2; 10-18 H vs TSG Hoffenheim 1-2; 10-11 A vs FC Cologne 1-2 |
| Bundesliga | Eintracht Frankfurt | 6 | 10 | 1.20 | 2.00 | 0.781 | 1.301 | 11-07 A vs SC Paderborn 07 2-2; 11-01 H vs Hamburg SV 3-1; 10-24 A vs Borussia Dortmund 0-1; 10-16 H vs FC Cologne 1-0; 10-10 A vs RB Leipzig 0-6 |
| Bundesliga | Hamburg SV | 8 | 7 | 1.60 | 1.40 | 1.041 | 0.911 | 11-06 H vs Borussia Mönchengladbach 3-1; 11-01 A vs Eintracht Frankfurt 1-3; 10-24 A vs SC Paderborn 07 0-1; 10-17 H vs VfB Stuttgart 1-0; 10-10 A vs TSG Hoffenheim 3-2 |
| Bundesliga | VfB Stuttgart | 9 | 6 | 1.80 | 1.20 | 1.171 | 0.781 | 11-07 H vs Werder Bremen 1-0; 10-31 A vs Bayer Leverkusen 4-2; 10-23 H vs Borussia Mönchengladbach 2-3; 10-17 A vs Hamburg SV 0-1; 10-10 A vs SC Paderborn 07 2-0 |
| Bundesliga | Werder Bremen | 9 | 7 | 1.80 | 1.40 | 1.171 | 0.911 | 11-07 A vs VfB Stuttgart 0-1; 10-31 H vs TSG Hoffenheim 2-0; 10-24 A vs Mainz 3-2; 10-17 H vs SC Paderborn 07 2-2; 10-09 A vs Borussia Dortmund 2-2 |
| Serie A | Bologna | 11 | 7 | 2.20 | 1.40 | 1.307 | 0.832 | 11-07 A vs Parma 2-1; 10-31 H vs Monza 2-1; 10-28 A vs AC Milan 4-2; 10-24 A vs Cagliari 2-0; 10-17 H vs Internazionale 1-3 |
| Serie A | Como | 9 | 4 | 1.80 | 0.80 | 1.069 | 0.475 | 11-08 A vs Internazionale 0-2; 11-01 H vs Venezia 1-0; 10-27 A vs Torino 3-1; 10-24 H vs Sassuolo 2-0; 10-18 A vs Fiorentina 3-1 |
| Serie A | Genoa | 6 | 5 | 1.20 | 1.00 | 0.713 | 0.594 | 11-08 H vs AC Milan 1-2; 11-01 A vs Lecce 2-1; 10-28 H vs Juventus 2-0; 10-25 H vs Venezia 1-0; 10-17 A vs AS Roma 0-2 |
| Serie A | Internazionale | 10 | 5 | 2.00 | 1.00 | 1.188 | 0.594 | 11-08 H vs Como 2-0; 10-31 A vs AC Milan 1-3; 10-28 A vs Venezia 2-0; 10-25 H vs Fiorentina 2-1; 10-17 A vs Bologna 3-1 |
| Serie A | Juventus | 6 | 7 | 1.20 | 1.40 | 0.713 | 0.832 | 11-08 A vs Fiorentina 2-2; 11-01 H vs Napoli 2-0; 10-28 A vs Genoa 0-2; 10-25 A vs Lecce 2-0; 10-18 H vs Lazio 0-3 |
| Serie A | Napoli | 8 | 8 | 1.60 | 1.60 | 0.950 | 0.950 | 11-08 H vs Lazio 1-1; 11-01 A vs Juventus 0-2; 10-28 A vs Monza 4-1; 10-24 H vs AS Roma 3-3; 10-17 A vs Venezia 0-1 |
| Serie A | Sassuolo | 6 | 19 | 1.20 | 3.80 | 0.713 | 2.257 | 11-07 A vs AS Roma 0-3; 11-02 H vs Fiorentina 2-4; 10-27 H vs Lazio 2-6; 10-24 A vs Como 0-2; 10-16 A vs Frosinone 2-4 |
| Serie A | Venezia | 3 | 5 | 0.60 | 1.00 | 0.356 | 0.594 | 11-06 H vs Udinese 2-1; 11-01 A vs Como 0-1; 10-28 H vs Internazionale 0-2; 10-25 A vs Genoa 0-1; 10-17 H vs Napoli 1-0 |
| Liga MX | América | 11 | 9 | 2.20 | 1.80 | 1.337 | 1.094 | 11-08 A vs Pumas UNAM 2-2; 11-01 H vs Toluca 2-2; 10-29 H vs Tijuana 1-1; 10-26 H vs Pachuca 1-2; 10-22 A vs Atlas 5-2 |
| Liga MX | Atlas | 10 | 12 | 2.00 | 2.40 | 1.215 | 1.458 | 11-07 H vs Pachuca 1-4; 10-31 A vs Atlético de San Luis 1-0; 10-25 H vs Puebla 4-3; 10-22 H vs América 2-5; 10-17 A vs Necaxa 2-0 |
| Liga MX | Cruz Azul | 15 | 5 | 3.00 | 1.00 | 1.823 | 0.608 | 11-08 A vs Tigres UANL 3-2; 11-02 H vs León 2-1; 10-26 A vs Querétaro 3-1; 10-22 A vs Pachuca 2-1; 10-18 H vs FC Juárez 5-0 |
| Liga MX | Guadalajara | 8 | 4 | 1.60 | 0.80 | 0.972 | 0.486 | 11-09 A vs León 1-1; 11-01 H vs Atlante 4-2; 10-25 A vs Monterrey 1-0; 10-21 H vs Necaxa 1-0; 10-17 H vs Tigres UANL 1-1 |
| Liga MX | León | 8 | 9 | 1.60 | 1.80 | 0.972 | 1.094 | 11-09 H vs Guadalajara 1-1; 11-02 A vs Cruz Azul 1-2; 10-24 H vs Toluca 1-1; 10-21 A vs Tigres UANL 2-0; 10-18 H vs América 3-5 |
| Liga MX | Monterrey | 8 | 9 | 1.60 | 1.80 | 0.972 | 1.094 | 11-14 A vs Querétaro 1-0; 11-08 A vs Toluca 0-4; 11-01 H vs Tijuana 3-3; 10-25 H vs Guadalajara 0-1; 10-22 A vs Puebla 4-1 |
| Liga MX | Pachuca | 11 | 6 | 2.20 | 1.20 | 1.337 | 0.729 | 11-07 A vs Atlas 4-1; 10-31 H vs Tigres UANL 3-0; 10-26 A vs América 2-1; 10-22 H vs Cruz Azul 1-2; 10-19 A vs Monterrey 1-2 |
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

- Scoreboard por liga y día, 2026-11-25 al 2026-11-29: `site.api.espn.com/apis/site/v2/sports/soccer/{{liga}}/scoreboard?dates={{AAAAMMDD}}` — los {n_partidos} partidos aparecen como STATUS_SCHEDULED con la fecha y hora exactas de la configuración (horas convertidas de UTC a CST, UTC-6).
- Schedule por equipo (últimos partidos completados): `site.api.espn.com/apis/site/v2/sports/soccer/{liga}/teams/{id}/schedule` — 40 equipos, 5 partidos completados cada uno, todos de liga, hasta el cutoff.
- Scoreboards de jornadas pasadas para promedios de liga: 9 fechas por liga (ver tabla c).
- Los archivos JSON crudos de todas estas consultas están en `raw/` dentro de esta misma carpeta.

## (e) Datos no verificados y partidos excluidos

- **Ningún partido quedó fuera:** los 24 partidos de la lista se verificaron en el scoreboard de ESPN con fecha, hora y equipos exactos antes de calcular.
- **Valores extremos por muestra corta (5 partidos, sin tope aplicado):** son correctos según los datos, pero una muestra de 5 partidos exagera rachas; conviene leer los favoritos más extremos con cautela.
- **Últimos 5 = solo liga:** el schedule de ESPN por liga devuelve partidos de esa liga; no se mezclaron otras competiciones.
- **Sin momios ni cuotas en esta tabla:** solo probabilidades propias (Poisson). Los momios y el EV están en la tabla de momios de la misma semana.
