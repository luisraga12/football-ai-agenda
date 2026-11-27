# Tabla de probabilidades Poisson — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-27 al 2026-11-29, horas de Monterrey (CST). **Fuente de datos:** ESPN, API pública sin clave.
**Método:** modelo Poisson con goles esperados (xG) por equipo, distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.
**Fecha de cálculo:** 2026-11-19. Últimos 5 partidos por equipo: partidos de liga completados hasta el 2026-11-19.

## (a) Tabla de los 40 partidos

| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Vie 27 nov | 13:30 | Bundesliga | Werder Bremen | Borussia Mönchengladbach | 2.49 | 0.90 | 72.2% | 16.4% | 11.5% | 65.7% | 54.2% |
| Vie 27 nov | 13:45 | Serie A | Venezia | Bologna | 0.49 | 1.32 | 13.9% | 28.8% | 57.3% | 27.3% | 28.6% |
| Vie 27 nov | 14:00 | Premier League | Nottingham Forest | Chelsea | 0.78 | 2.12 | 12.7% | 19.2% | 68.1% | 55.4% | 47.8% |
| Vie 27 nov | 14:00 | LaLiga | Levante | Racing Santander | 1.77 | 1.07 | 53.7% | 23.4% | 22.9% | 53.9% | 54.5% |
| Sáb 28 nov | 07:00 | LaLiga | Real Betis | Rayo Vallecano | 2.59 | 1.19 | 67.5% | 17.0% | 15.5% | 72.8% | 64.3% |
| Sáb 28 nov | 08:00 | Serie A | Frosinone | Parma | 2.47 | 0.96 | 70.4% | 16.9% | 12.7% | 66.6% | 56.5% |
| Sáb 28 nov | 08:30 | Bundesliga | Hamburg SV | Bayern Munich | 1.72 | 2.24 | 29.9% | 20.2% | 49.8% | 75.6% | 73.4% |
| Sáb 28 nov | 08:30 | Bundesliga | FC Cologne | SV Elversberg | 1.35 | 0.96 | 45.8% | 27.6% | 26.6% | 40.7% | 45.7% |
| Sáb 28 nov | 08:30 | Bundesliga | Mainz | 1. FC Union Berlin | 0.98 | 0.83 | 37.8% | 32.6% | 29.6% | 27.3% | 35.3% |
| Sáb 28 nov | 08:30 | Bundesliga | SC Paderborn 07 | Schalke 04 | 1.08 | 0.26 | 57.0% | 34.2% | 8.8% | 15.0% | 14.9% |
| Sáb 28 nov | 09:00 | Premier League | Manchester United | Brentford | 1.65 | 1.94 | 33.2% | 21.8% | 45.1% | 69.5% | 69.1% |
| Sáb 28 nov | 09:00 | Premier League | Leeds United | Coventry City | 1.06 | 1.32 | 29.8% | 27.5% | 42.7% | 42.5% | 47.9% |
| Sáb 28 nov | 09:15 | LaLiga | Málaga | Athletic Club | 1.18 | 2.62 | 15.0% | 16.8% | 68.2% | 73.0% | 64.1% |
| Sáb 28 nov | 11:00 | Serie A | Torino | Lazio | 0.94 | 2.69 | 10.7% | 15.0% | 74.3% | 70.2% | 56.8% |
| Sáb 28 nov | 11:30 | LaLiga | Elche | Atlético Madrid | 0.35 | 0.62 | 17.7% | 46.4% | 36.0% | 7.6% | 13.8% |
| Sáb 28 nov | 11:30 | Bundesliga | VfB Stuttgart | Eintracht Frankfurt | 2.77 | 0.77 | 79.0% | 13.3% | 7.7% | 68.5% | 50.2% |
| Sáb 28 nov | 11:30 | Premier League | Ipswich Town | Aston Villa | 2.51 | 2.64 | 38.6% | 18.0% | 43.3% | 88.8% | 85.3% |
| Sáb 28 nov | 13:45 | Serie A | Internazionale | Genoa | 1.18 | 0.72 | 46.7% | 30.7% | 22.6% | 29.5% | 35.5% |
| Sáb 28 nov | 14:00 | LaLiga | Real Madrid | Alavés | 5.61 | 0.24 | 99.0% | 0.8% | 0.1% | 93.1% | 21.1% |
| Sáb 28 nov | 19:00 | Liga MX | Atlas | Toluca | 1.51 | 2.81 | 18.8% | 16.7% | 64.5% | 80.5% | 73.3% |
| Sáb 28 nov | 21:10 | Liga MX | América | Monterrey | 2.50 | 1.68 | 55.6% | 18.9% | 25.5% | 78.7% | 74.7% |
| Dom 29 nov | 05:30 | Serie A | Udinese | Fiorentina | 0.78 | 2.88 | 7.2% | 12.5% | 80.3% | 70.7% | 51.0% |
| Dom 29 nov | 06:00 | Premier League | Everton | Liverpool | 1.41 | 1.44 | 36.8% | 25.0% | 38.2% | 54.3% | 57.7% |
| Dom 29 nov | 07:00 | LaLiga | Valencia | Osasuna | 1.57 | 1.25 | 44.8% | 24.8% | 30.4% | 53.5% | 56.5% |
| Dom 29 nov | 08:00 | Serie A | Sassuolo | Napoli | 1.13 | 3.65 | 7.3% | 10.0% | 82.7% | 85.5% | 65.9% |
| Dom 29 nov | 08:05 | Premier League | Brighton & Hove Albion | Newcastle United | 2.74 | 0.24 | 89.2% | 8.9% | 1.8% | 57.2% | 19.6% |
| Dom 29 nov | 08:05 | Premier League | Crystal Palace | Hull City | 1.10 | 1.91 | 21.5% | 22.2% | 56.3% | 57.8% | 56.8% |
| Dom 29 nov | 08:05 | Premier League | Fulham | AFC Bournemouth | 1.18 | 1.18 | 36.0% | 28.0% | 36.0% | 41.7% | 47.8% |
| Dom 29 nov | 08:05 | Premier League | Sunderland | Tottenham Hotspur | 0.24 | 1.65 | 4.8% | 21.7% | 73.4% | 29.1% | 16.9% |
| Dom 29 nov | 08:30 | Bundesliga | SC Freiburg | RB Leipzig | 1.97 | 2.69 | 28.2% | 18.2% | 53.7% | 84.3% | 80.1% |
| Dom 29 nov | 09:15 | LaLiga | Deportivo | Barcelona | 1.18 | 3.03 | 11.6% | 13.9% | 74.6% | 79.1% | 65.8% |
| Dom 29 nov | 10:30 | Premier League | Arsenal | Manchester City | 2.19 | 0.24 | 83.1% | 14.0% | 3.0% | 43.8% | 18.6% |
| Dom 29 nov | 10:30 | Bundesliga | TSG Hoffenheim | FC Augsburg | 3.87 | 1.34 | 81.7% | 10.0% | 8.3% | 89.2% | 72.4% |
| Dom 29 nov | 11:00 | Serie A | AS Roma | Monza | 4.00 | 1.34 | 82.9% | 9.4% | 7.7% | 90.1% | 72.6% |
| Dom 29 nov | 11:30 | LaLiga | Celta Vigo | Villarreal | 0.24 | 0.48 | 13.8% | 54.8% | 31.5% | 3.6% | 7.9% |
| Dom 29 nov | 12:30 | Bundesliga | Borussia Dortmund | Bayer Leverkusen | 2.58 | 1.07 | 70.0% | 16.5% | 13.5% | 70.6% | 60.6% |
| Dom 29 nov | 13:45 | Serie A | Como | Juventus | 1.48 | 0.58 | 59.4% | 26.2% | 14.3% | 33.9% | 33.8% |
| Dom 29 nov | 14:00 | LaLiga | Real Sociedad | Sevilla | 4.71 | 1.46 | 87.3% | 7.1% | 5.6% | 94.5% | 76.0% |
| Dom 29 nov | 19:07 | Liga MX | Guadalajara | Pachuca | 1.21 | 1.03 | 40.2% | 28.7% | 31.1% | 38.8% | 45.1% |
| Dom 29 nov | 21:00 | Liga MX | Cruz Azul | León | 3.41 | 0.94 | 83.4% | 10.2% | 6.4% | 80.8% | 58.7% |

Promedios de la tabla: xG local 1.85, xG visitante 1.46; P(1) media 44.9%, P(X) media 20.6%, P(2) media 34.5%.

## (b) Tabla de cálculo por equipo (últimos 5 partidos de liga)

GF = goles a favor, GA = goles en contra en los últimos 5. Ataque = (GF/5) / prom. por equipo de la liga; defensa = (GA/5) / prom. por equipo de la liga.

| Liga | Equipo | GF (5) | GA (5) | GF/partido | GA/partido | Ataque | Defensa | Últimos 5 (fecha, H/A, rival, marcador desde el equipo) |
|---|---|---|---|---|---|---|---|---|
| Premier League | AFC Bournemouth | 10 | 6 | 2.00 | 1.20 | 1.714 | 1.029 | 11-08 A vs Ipswich Town 2-1; 10-31 H vs Leeds United 2-0; 10-25 A vs Manchester United 3-0; 10-18 H vs Sunderland 2-0; 10-10 A vs Chelsea 1-5 |
| Premier League | Arsenal | 7 | 1 | 1.40 | 0.20 | 1.200 | 0.171 | 11-07 H vs Hull City 1-0; 11-01 A vs Liverpool 1-0; 10-24 H vs Everton 2-0; 10-18 A vs Nottingham Forest 1-0; 10-10 H vs Leeds United 2-1 |
| Premier League | Aston Villa | 10 | 8 | 2.00 | 1.60 | 1.714 | 1.371 | 11-08 A vs Manchester United 4-4; 10-31 H vs Fulham 1-1; 10-24 H vs Manchester City 2-1; 10-17 A vs Newcastle United 1-0; 10-10 H vs Brentford 2-2 |
| Premier League | Brentford | 6 | 7 | 1.20 | 1.40 | 1.029 | 1.200 | 11-08 A vs Brighton & Hove Albion 0-2; 10-31 H vs Nottingham Forest 2-0; 10-25 A vs Hull City 1-1; 10-17 H vs Liverpool 1-2; 10-10 A vs Aston Villa 2-2 |
| Premier League | Brighton & Hove Albion | 10 | 2 | 2.00 | 0.40 | 1.714 | 0.343 | 11-08 H vs Brentford 2-0; 10-31 A vs Manchester City 1-0; 10-25 A vs Liverpool 0-2; 10-18 H vs Crystal Palace 5-0; 10-10 A vs Sunderland 2-0 |
| Premier League | Chelsea | 9 | 4 | 1.80 | 0.80 | 1.543 | 0.686 | 11-08 A vs Sunderland 0-1; 10-31 H vs Manchester United 2-0; 10-24 H vs Tottenham Hotspur 0-2; 10-17 A vs Everton 2-0; 10-10 H vs AFC Bournemouth 5-1 |
| Premier League | Coventry City | 9 | 9 | 1.80 | 1.80 | 1.543 | 1.543 | 11-06 A vs Everton 1-3; 10-31 H vs Sunderland 3-1; 10-24 H vs Fulham 0-1; 10-19 A vs Tottenham Hotspur 1-3; 10-12 H vs Newcastle United 4-1 |
| Premier League | Crystal Palace | 4 | 13 | 0.80 | 2.60 | 0.686 | 2.229 | 11-08 H vs Liverpool 1-3; 10-31 A vs Tottenham Hotspur 0-2; 10-25 H vs Newcastle United 0-2; 10-18 A vs Brighton & Hove Albion 0-5; 10-11 H vs Nottingham Forest 3-1 |
| Premier League | Everton | 6 | 7 | 1.20 | 1.40 | 1.029 | 1.200 | 11-06 H vs Coventry City 3-1; 11-02 A vs Newcastle United 1-0; 10-24 A vs Arsenal 0-2; 10-17 H vs Chelsea 0-2; 10-11 A vs Hull City 2-2 |
| Premier League | Fulham | 5 | 4 | 1.00 | 0.80 | 0.857 | 0.686 | 11-07 H vs Newcastle United 1-1; 10-31 A vs Aston Villa 1-1; 10-24 A vs Coventry City 1-0; 10-17 H vs Hull City 1-0; 10-10 A vs Ipswich Town 1-2 |
| Premier League | Hull City | 5 | 7 | 1.00 | 1.40 | 0.857 | 1.200 | 11-07 A vs Arsenal 0-1; 10-31 H vs Ipswich Town 2-2; 10-25 H vs Brentford 1-1; 10-17 A vs Fulham 0-1; 10-11 H vs Everton 2-2 |
| Premier League | Ipswich Town | 8 | 9 | 1.60 | 1.80 | 1.371 | 1.543 | 11-08 H vs AFC Bournemouth 1-2; 10-31 A vs Hull City 2-2; 10-23 H vs Nottingham Forest 1-1; 10-17 A vs Manchester City 2-3; 10-10 H vs Fulham 2-1 |
| Premier League | Leeds United | 3 | 5 | 0.60 | 1.00 | 0.514 | 0.857 | 11-07 H vs Tottenham Hotspur 1-0; 10-31 A vs AFC Bournemouth 0-2; 10-25 A vs Sunderland 0-0; 10-18 H vs Manchester United 1-1; 10-10 A vs Arsenal 1-2 |
| Premier League | Liverpool | 7 | 6 | 1.40 | 1.20 | 1.200 | 1.029 | 11-08 A vs Crystal Palace 3-1; 11-01 H vs Arsenal 0-1; 10-25 H vs Brighton & Hove Albion 2-0; 10-17 A vs Brentford 2-1; 10-11 H vs Manchester City 0-3 |
| Premier League | Manchester City | 8 | 8 | 1.60 | 1.60 | 1.371 | 1.371 | 11-07 A vs Nottingham Forest 1-3; 10-31 H vs Brighton & Hove Albion 0-1; 10-24 A vs Aston Villa 1-2; 10-17 H vs Ipswich Town 3-2; 10-11 A vs Liverpool 3-0 |
| Premier League | Manchester United | 6 | 11 | 1.20 | 2.20 | 1.029 | 1.886 | 11-08 H vs Aston Villa 4-4; 10-31 A vs Chelsea 0-2; 10-25 H vs AFC Bournemouth 0-3; 10-18 A vs Leeds United 1-1; 10-10 H vs Tottenham Hotspur 1-1 |
| Premier League | Newcastle United | 4 | 7 | 0.80 | 1.40 | 0.686 | 1.200 | 11-07 A vs Fulham 1-1; 11-02 H vs Everton 0-1; 10-25 A vs Crystal Palace 2-0; 10-17 H vs Aston Villa 0-1; 10-12 A vs Coventry City 1-4 |
| Premier League | Nottingham Forest | 5 | 8 | 1.00 | 1.60 | 0.857 | 1.371 | 11-07 H vs Manchester City 3-1; 10-31 A vs Brentford 0-2; 10-23 A vs Ipswich Town 1-1; 10-18 H vs Arsenal 0-1; 10-11 A vs Crystal Palace 1-3 |
| Premier League | Sunderland | 2 | 7 | 0.40 | 1.40 | 0.343 | 1.200 | 11-08 H vs Chelsea 1-0; 10-31 A vs Coventry City 1-3; 10-25 H vs Leeds United 0-0; 10-18 A vs AFC Bournemouth 0-2; 10-10 H vs Brighton & Hove Albion 0-2 |
| Premier League | Tottenham Hotspur | 8 | 3 | 1.60 | 0.60 | 1.371 | 0.514 | 11-07 A vs Leeds United 0-1; 10-31 H vs Crystal Palace 2-0; 10-24 A vs Chelsea 2-0; 10-19 H vs Coventry City 3-1; 10-10 A vs Manchester United 1-1 |
| LaLiga | Alavés | 4 | 11 | 0.80 | 2.20 | 0.690 | 1.897 | 11-06 A vs Sevilla 0-0; 10-31 A vs Barcelona 1-6; 10-23 H vs Málaga 1-1; 10-18 A vs Celta Vigo 1-2; 10-10 H vs Atlético Madrid 1-2 |
| LaLiga | Athletic Club | 8 | 5 | 1.60 | 1.00 | 1.379 | 0.862 | 11-07 A vs Osasuna 1-1; 11-01 H vs Real Sociedad 2-1; 10-25 H vs Getafe 4-0; 10-21 A vs Levante 1-3; 10-17 A vs Valencia 0-0 |
| LaLiga | Atlético Madrid | 7 | 3 | 1.40 | 0.60 | 1.207 | 0.517 | 11-08 H vs Barcelona 1-2; 10-31 A vs Levante 2-0; 10-24 H vs Deportivo 1-0; 10-17 A vs Espanyol 1-0; 10-10 A vs Alavés 2-1 |
| LaLiga | Barcelona | 17 | 6 | 3.40 | 1.20 | 2.931 | 1.034 | 11-08 A vs Atlético Madrid 2-1; 10-31 H vs Alavés 6-1; 10-25 H vs Real Madrid 1-2; 10-17 A vs Real Betis 5-2; 10-10 H vs Getafe 3-0 |
| LaLiga | Celta Vigo | 2 | 4 | 0.40 | 0.80 | 0.345 | 0.690 | 11-08 H vs Levante 0-0; 10-31 A vs Rayo Vallecano 0-3; 10-25 H vs Real Betis 0-0; 10-18 H vs Alavés 2-1; 10-11 A vs Elche 0-0 |
| LaLiga | Deportivo | 5 | 6 | 1.00 | 1.20 | 0.862 | 1.034 | 11-07 A vs Espanyol 0-0; 11-02 H vs Osasuna 2-1; 10-24 A vs Atlético Madrid 0-1; 10-16 H vs Levante 1-1; 10-11 A vs Real Sociedad 2-3 |
| LaLiga | Elche | 3 | 3 | 0.60 | 0.60 | 0.517 | 0.517 | 11-08 H vs Real Betis 0-2; 11-01 H vs Valencia 0-1; 10-24 A vs Rayo Vallecano 3-0; 10-17 A vs Villarreal 0-0; 10-11 H vs Celta Vigo 0-0 |
| LaLiga | Levante | 5 | 6 | 1.00 | 1.20 | 0.862 | 1.034 | 11-08 A vs Celta Vigo 0-0; 10-31 H vs Atlético Madrid 0-2; 10-25 A vs Real Sociedad 1-2; 10-21 H vs Athletic Club 3-1; 10-16 A vs Deportivo 1-1 |
| LaLiga | Málaga | 6 | 11 | 1.20 | 2.20 | 1.034 | 1.897 | 11-07 H vs Racing Santander 1-2; 10-31 A vs Real Betis 1-2; 10-23 A vs Alavés 1-1; 10-18 H vs Real Sociedad 2-5; 10-09 H vs Espanyol 1-1 |
| LaLiga | Osasuna | 6 | 10 | 1.20 | 2.00 | 1.034 | 1.724 | 11-07 H vs Athletic Club 1-1; 11-02 A vs Deportivo 1-2; 10-26 A vs Sevilla 0-2; 10-18 H vs Racing Santander 2-0; 10-11 A vs Real Betis 2-5 |
| LaLiga | Racing Santander | 6 | 9 | 1.20 | 1.80 | 1.034 | 1.552 | 11-07 A vs Málaga 2-1; 11-01 H vs Real Madrid 0-3; 10-24 H vs Espanyol 2-1; 10-18 A vs Osasuna 0-2; 10-11 H vs Valencia 2-2 |
| LaLiga | Rayo Vallecano | 5 | 6 | 1.00 | 1.20 | 0.862 | 1.034 | 11-08 A vs Real Sociedad 0-1; 10-31 H vs Celta Vigo 3-0; 10-24 H vs Elche 0-3; 10-19 A vs Getafe 1-1; 09-19 A vs Osasuna 1-1 |
| LaLiga | Real Betis | 11 | 8 | 2.20 | 1.60 | 1.897 | 1.379 | 11-08 A vs Elche 2-0; 10-31 H vs Málaga 2-1; 10-25 A vs Celta Vigo 0-0; 10-17 H vs Barcelona 2-5; 10-11 H vs Osasuna 5-2 |
| LaLiga | Real Madrid | 13 | 2 | 2.60 | 0.40 | 2.241 | 0.345 | 11-07 A vs Valencia 3-0; 11-01 A vs Racing Santander 3-0; 10-25 A vs Barcelona 2-1; 10-18 H vs Sevilla 4-1; 10-10 H vs Villarreal 1-0 |
| LaLiga | Real Sociedad | 12 | 7 | 2.40 | 1.40 | 2.069 | 1.207 | 11-08 H vs Rayo Vallecano 1-0; 11-01 A vs Athletic Club 1-2; 10-25 H vs Levante 2-1; 10-18 A vs Málaga 5-2; 10-11 H vs Deportivo 3-2 |
| LaLiga | Sevilla | 7 | 10 | 1.40 | 2.00 | 1.207 | 1.724 | 11-06 H vs Alavés 0-0; 11-01 A vs Getafe 1-3; 10-26 H vs Osasuna 2-0; 10-18 A vs Real Madrid 1-4; 10-12 A vs Levante 3-3 |
| LaLiga | Valencia | 4 | 7 | 0.80 | 1.40 | 0.690 | 1.207 | 11-07 H vs Real Madrid 0-3; 11-01 A vs Elche 1-0; 10-24 H vs Villarreal 1-2; 10-17 H vs Athletic Club 0-0; 10-11 A vs Racing Santander 2-2 |
| LaLiga | Villarreal | 4 | 3 | 0.80 | 0.60 | 0.690 | 0.517 | 11-08 H vs Getafe 2-0; 10-30 H vs Espanyol 0-1; 10-24 A vs Valencia 2-1; 10-17 H vs Elche 0-0; 10-10 A vs Real Madrid 0-1 |
| Bundesliga | 1. FC Union Berlin | 3 | 4 | 0.60 | 0.80 | 0.390 | 0.520 | 11-08 A vs SC Freiburg 0-2; 11-01 H vs FC Cologne 1-1; 10-24 A vs FC Augsburg 1-1; 10-17 H vs Borussia Dortmund 0-0; 10-10 H vs SV Elversberg 1-0 |
| Bundesliga | Bayer Leverkusen | 10 | 12 | 2.00 | 2.40 | 1.301 | 1.561 | 11-08 A vs FC Cologne 2-1; 10-31 H vs VfB Stuttgart 2-4; 10-25 A vs TSG Hoffenheim 0-3; 10-18 H vs SC Freiburg 2-1; 10-10 A vs Mainz 4-3 |
| Bundesliga | Bayern Munich | 15 | 7 | 3.00 | 1.40 | 1.952 | 0.911 | 11-07 A vs Mainz 2-1; 10-31 H vs Borussia Dortmund 2-2; 10-25 A vs SC Freiburg 3-1; 10-17 H vs RB Leipzig 6-1; 10-10 A vs FC Augsburg 2-2 |
| Bundesliga | Borussia Dortmund | 7 | 5 | 1.40 | 1.00 | 0.911 | 0.651 | 11-07 H vs SV Elversberg 2-1; 10-31 A vs Bayern Munich 2-2; 10-24 H vs Eintracht Frankfurt 1-0; 10-17 A vs 1. FC Union Berlin 0-0; 10-09 H vs Werder Bremen 2-2 |
| Bundesliga | Borussia Mönchengladbach | 6 | 9 | 1.20 | 1.80 | 0.781 | 1.171 | 11-06 A vs Hamburg SV 1-3; 10-31 H vs SC Paderborn 07 0-0; 10-23 A vs VfB Stuttgart 3-2; 10-18 H vs TSG Hoffenheim 1-2; 10-11 A vs FC Cologne 1-2 |
| Bundesliga | Eintracht Frankfurt | 6 | 10 | 1.20 | 2.00 | 0.781 | 1.301 | 11-07 A vs SC Paderborn 07 2-2; 11-01 H vs Hamburg SV 3-1; 10-24 A vs Borussia Dortmund 0-1; 10-16 H vs FC Cologne 1-0; 10-10 A vs RB Leipzig 0-6 |
| Bundesliga | FC Augsburg | 9 | 14 | 1.80 | 2.80 | 1.171 | 1.822 | 11-07 A vs RB Leipzig 2-5; 10-31 H vs SC Freiburg 1-2; 10-24 H vs 1. FC Union Berlin 1-1; 10-17 A vs SV Elversberg 3-4; 10-10 H vs Bayern Munich 2-2 |
| Bundesliga | FC Cologne | 4 | 5 | 0.80 | 1.00 | 0.520 | 0.651 | 11-08 H vs Bayer Leverkusen 1-2; 11-01 A vs 1. FC Union Berlin 1-1; 10-24 H vs Schalke 04 0-0; 10-16 A vs Eintracht Frankfurt 0-1; 10-11 H vs Borussia Mönchengladbach 2-1 |
| Bundesliga | Hamburg SV | 8 | 7 | 1.60 | 1.40 | 1.041 | 0.911 | 11-06 H vs Borussia Mönchengladbach 3-1; 11-01 A vs Eintracht Frankfurt 1-3; 10-24 A vs SC Paderborn 07 0-1; 10-17 H vs VfB Stuttgart 1-0; 10-10 A vs TSG Hoffenheim 3-2 |
| Bundesliga | Mainz | 8 | 13 | 1.60 | 2.60 | 1.041 | 1.692 | 11-07 H vs Bayern Munich 1-2; 10-30 A vs SV Elversberg 1-4; 10-24 H vs Werder Bremen 2-3; 10-17 A vs Schalke 04 1-0; 10-10 H vs Bayer Leverkusen 3-4 |
| Bundesliga | RB Leipzig | 18 | 8 | 3.60 | 1.60 | 2.342 | 1.041 | 11-07 H vs FC Augsburg 5-2; 10-31 A vs Schalke 04 2-0; 10-24 H vs SV Elversberg 4-0; 10-17 A vs Bayern Munich 1-6; 10-10 H vs Eintracht Frankfurt 6-0 |
| Bundesliga | SC Freiburg | 8 | 7 | 1.60 | 1.40 | 1.041 | 0.911 | 11-08 H vs 1. FC Union Berlin 2-0; 10-31 A vs FC Augsburg 2-1; 10-25 H vs Bayern Munich 1-3; 10-18 A vs Bayer Leverkusen 1-2; 10-11 H vs Schalke 04 2-1 |
| Bundesliga | SC Paderborn 07 | 5 | 6 | 1.00 | 1.20 | 0.651 | 0.781 | 11-07 H vs Eintracht Frankfurt 2-2; 10-31 A vs Borussia Mönchengladbach 0-0; 10-24 H vs Hamburg SV 1-0; 10-17 A vs Werder Bremen 2-2; 10-10 H vs VfB Stuttgart 0-2 |
| Bundesliga | SV Elversberg | 9 | 11 | 1.80 | 2.20 | 1.171 | 1.431 | 11-07 A vs Borussia Dortmund 1-2; 10-30 H vs Mainz 4-1; 10-24 A vs RB Leipzig 0-4; 10-17 H vs FC Augsburg 4-3; 10-10 A vs 1. FC Union Berlin 0-1 |
| Bundesliga | Schalke 04 | 2 | 7 | 0.40 | 1.40 | 0.260 | 0.911 | 11-08 A vs TSG Hoffenheim 1-2; 10-31 H vs RB Leipzig 0-2; 10-24 A vs FC Cologne 0-0; 10-17 H vs Mainz 0-1; 10-11 A vs SC Freiburg 1-2 |
| Bundesliga | TSG Hoffenheim | 9 | 7 | 1.80 | 1.40 | 1.171 | 0.911 | 11-08 H vs Schalke 04 2-1; 10-31 A vs Werder Bremen 0-2; 10-25 H vs Bayer Leverkusen 3-0; 10-18 A vs Borussia Mönchengladbach 2-1; 10-10 H vs Hamburg SV 2-3 |
| Bundesliga | VfB Stuttgart | 9 | 6 | 1.80 | 1.20 | 1.171 | 0.781 | 11-07 H vs Werder Bremen 1-0; 10-31 A vs Bayer Leverkusen 4-2; 10-23 H vs Borussia Mönchengladbach 2-3; 10-17 A vs Hamburg SV 0-1; 10-10 A vs SC Paderborn 07 2-0 |
| Bundesliga | Werder Bremen | 9 | 7 | 1.80 | 1.40 | 1.171 | 0.911 | 11-07 A vs VfB Stuttgart 0-1; 10-31 H vs TSG Hoffenheim 2-0; 10-24 A vs Mainz 3-2; 10-17 H vs SC Paderborn 07 2-2; 10-09 A vs Borussia Dortmund 2-2 |
| Serie A | AS Roma | 17 | 7 | 3.40 | 1.40 | 2.020 | 0.832 | 11-07 H vs Sassuolo 3-0; 10-31 A vs Udinese 5-2; 10-27 H vs Cagliari 4-2; 10-24 A vs Napoli 3-3; 10-17 H vs Genoa 2-0 |
| Serie A | Bologna | 11 | 7 | 2.20 | 1.40 | 1.307 | 0.832 | 11-07 A vs Parma 2-1; 10-31 H vs Monza 2-1; 10-28 A vs AC Milan 4-2; 10-24 A vs Cagliari 2-0; 10-17 H vs Internazionale 1-3 |
| Serie A | Como | 9 | 4 | 1.80 | 0.80 | 1.069 | 0.475 | 11-08 A vs Internazionale 0-2; 11-01 H vs Venezia 1-0; 10-27 A vs Torino 3-1; 10-24 H vs Sassuolo 2-0; 10-18 A vs Fiorentina 3-1 |
| Serie A | Fiorentina | 10 | 11 | 2.00 | 2.20 | 1.188 | 1.307 | 11-08 H vs Juventus 2-2; 11-02 A vs Sassuolo 4-2; 10-29 H vs Atalanta 2-2; 10-25 A vs Internazionale 1-2; 10-18 H vs Como 1-3 |
| Serie A | Frosinone | 15 | 8 | 3.00 | 1.60 | 1.782 | 0.950 | 11-07 A vs Cagliari 0-1; 11-01 H vs Torino 2-0; 10-29 H vs Lecce 5-1; 10-25 A vs Atalanta 4-4; 10-16 H vs Sassuolo 4-2 |
| Serie A | Genoa | 6 | 5 | 1.20 | 1.00 | 0.713 | 0.594 | 11-08 H vs AC Milan 1-2; 11-01 A vs Lecce 2-1; 10-28 H vs Juventus 2-0; 10-25 H vs Venezia 1-0; 10-17 A vs AS Roma 0-2 |
| Serie A | Internazionale | 10 | 5 | 2.00 | 1.00 | 1.188 | 0.594 | 11-08 H vs Como 2-0; 10-31 A vs AC Milan 1-3; 10-28 A vs Venezia 2-0; 10-25 H vs Fiorentina 2-1; 10-17 A vs Bologna 3-1 |
| Serie A | Juventus | 6 | 7 | 1.20 | 1.40 | 0.713 | 0.832 | 11-08 A vs Fiorentina 2-2; 11-01 H vs Napoli 2-0; 10-28 A vs Genoa 0-2; 10-25 A vs Lecce 2-0; 10-18 H vs Lazio 0-3 |
| Serie A | Lazio | 14 | 5 | 2.80 | 1.00 | 1.663 | 0.594 | 11-08 A vs Napoli 1-1; 11-01 H vs Cagliari 2-1; 10-27 A vs Sassuolo 6-2; 10-24 H vs Parma 2-1; 10-18 A vs Juventus 3-0 |
| Serie A | Monza | 8 | 10 | 1.60 | 2.00 | 0.950 | 1.188 | 11-08 H vs Atalanta 0-1; 10-31 A vs Bologna 1-2; 10-28 H vs Napoli 1-4; 10-23 A vs Torino 2-3; 10-19 H vs Cagliari 4-0 |
| Serie A | Napoli | 8 | 8 | 1.60 | 1.60 | 0.950 | 0.950 | 11-08 H vs Lazio 1-1; 11-01 A vs Juventus 0-2; 10-28 A vs Monza 4-1; 10-24 H vs AS Roma 3-3; 10-17 A vs Venezia 0-1 |
| Serie A | Parma | 5 | 7 | 1.00 | 1.40 | 0.594 | 0.832 | 11-07 H vs Bologna 1-2; 11-02 A vs Atalanta 3-0; 10-28 H vs Udinese 0-0; 10-24 A vs Lazio 1-2; 10-19 H vs Torino 0-3 |
| Serie A | Sassuolo | 6 | 19 | 1.20 | 3.80 | 0.713 | 2.257 | 11-07 A vs AS Roma 0-3; 11-02 H vs Fiorentina 2-4; 10-27 H vs Lazio 2-6; 10-24 A vs Como 0-2; 10-16 A vs Frosinone 2-4 |
| Serie A | Torino | 8 | 8 | 1.60 | 1.60 | 0.950 | 0.950 | 11-07 H vs Lecce 1-1; 11-01 A vs Frosinone 0-2; 10-27 H vs Como 1-3; 10-23 H vs Monza 3-2; 10-19 A vs Parma 3-0 |
| Serie A | Udinese | 3 | 12 | 0.60 | 2.40 | 0.356 | 1.426 | 11-06 A vs Venezia 1-2; 10-31 H vs AS Roma 2-5; 10-28 A vs Parma 0-0; 10-25 H vs AC Milan 0-2; 10-18 H vs Lecce 0-3 |
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

- Scoreboard por liga y día, 2026-11-27 al 2026-11-29: `site.api.espn.com/apis/site/v2/sports/soccer/{{liga}}/scoreboard?dates={{AAAAMMDD}}` — los {n_partidos} partidos aparecen como STATUS_SCHEDULED con la fecha y hora exactas de la configuración (horas convertidas de UTC a CST, UTC-6).
- Schedule por equipo (últimos partidos completados): `site.api.espn.com/apis/site/v2/sports/soccer/{liga}/teams/{id}/schedule` — 80 equipos, 5 partidos completados cada uno, todos de liga, hasta el cutoff.
- Scoreboards de jornadas pasadas para promedios de liga: 9 fechas por liga (ver tabla c).
- Los archivos JSON crudos de todas estas consultas están en `raw/` dentro de esta misma carpeta.

## (e) Datos no verificados y partidos excluidos

- **Ningún partido quedó fuera:** los 40 partidos de la lista se verificaron en el scoreboard de ESPN con fecha, hora y equipos exactos antes de calcular.
- **Valores extremos por muestra corta (5 partidos, sin tope aplicado):** son correctos según los datos, pero una muestra de 5 partidos exagera rachas; conviene leer los favoritos más extremos con cautela.
- **Últimos 5 = solo liga:** el schedule de ESPN por liga devuelve partidos de esa liga; no se mezclaron otras competiciones.
- **Sin momios ni cuotas en esta tabla:** solo probabilidades propias (Poisson). Los momios y el EV están en la tabla de momios de la misma semana.
