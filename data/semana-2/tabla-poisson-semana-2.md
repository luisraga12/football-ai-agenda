# Tabla de probabilidades Poisson — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-27 al 2026-11-29, horas de Monterrey (CST). **Fuente de datos:** ESPN, API pública sin clave.
**Método:** modelo Poisson con goles esperados (xG) por equipo, distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.
**Fecha de cálculo:** 2026-11-26. Últimos 5 partidos por equipo: partidos de liga completados hasta el 2026-11-26.

## (a) Tabla de los 40 partidos

| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Vie 27 nov | 13:30 | Bundesliga | Werder Bremen | Borussia Mönchengladbach | 2.78 | 0.54 | 83.7% | 11.5% | 4.9% | 64.5% | 39.3% |
| Vie 27 nov | 13:45 | Serie A | Venezia | Bologna | 0.29 | 2.11 | 4.1% | 15.6% | 80.3% | 43.0% | 22.3% |
| Vie 27 nov | 14:00 | Premier League | Nottingham Forest | Chelsea | 1.09 | 0.72 | 44.0% | 32.0% | 24.0% | 27.0% | 33.9% |
| Vie 27 nov | 14:00 | LaLiga | Levante | Racing Santander | 1.50 | 1.55 | 36.8% | 24.1% | 39.2% | 58.7% | 61.1% |
| Sáb 28 nov | 07:00 | LaLiga | Real Betis | Rayo Vallecano | 1.40 | 1.03 | 45.2% | 26.9% | 27.9% | 43.8% | 48.5% |
| Sáb 28 nov | 08:00 | Serie A | Frosinone | Parma | 3.16 | 1.40 | 72.1% | 14.2% | 13.7% | 83.3% | 72.2% |
| Sáb 28 nov | 08:30 | Bundesliga | Hamburg SV | Bayern Munich | 0.95 | 2.74 | 10.4% | 14.7% | 74.9% | 71.2% | 57.3% |
| Sáb 28 nov | 08:30 | Bundesliga | FC Cologne | SV Elversberg | 1.04 | 0.98 | 36.4% | 30.6% | 33.0% | 32.9% | 40.4% |
| Sáb 28 nov | 08:30 | Bundesliga | Mainz | 1. FC Union Berlin | 1.71 | 0.78 | 59.4% | 23.7% | 16.9% | 45.3% | 44.4% |
| Sáb 28 nov | 08:30 | Bundesliga | SC Paderborn 07 | Schalke 04 | 0.79 | 0.17 | 48.7% | 43.6% | 7.7% | 7.4% | 8.7% |
| Sáb 28 nov | 09:00 | Premier League | Manchester United | Brentford | 0.97 | 2.29 | 14.5% | 18.4% | 67.1% | 63.3% | 55.8% |
| Sáb 28 nov | 09:00 | Premier League | Leeds United | Coventry City | 2.33 | 0.66 | 75.0% | 16.3% | 8.8% | 57.3% | 43.4% |
| Sáb 28 nov | 09:15 | LaLiga | Málaga | Athletic Club | 1.00 | 3.25 | 7.9% | 11.5% | 80.6% | 79.6% | 60.7% |
| Sáb 28 nov | 11:00 | Serie A | Torino | Lazio | 0.73 | 2.68 | 7.7% | 13.7% | 78.6% | 66.3% | 48.3% |
| Sáb 28 nov | 11:30 | LaLiga | Elche | Atlético Madrid | 0.27 | 1.18 | 8.3% | 31.5% | 60.2% | 17.8% | 16.2% |
| Sáb 28 nov | 11:30 | Bundesliga | VfB Stuttgart | Eintracht Frankfurt | 0.88 | 0.91 | 32.8% | 32.9% | 34.3% | 26.9% | 35.1% |
| Sáb 28 nov | 11:30 | Premier League | Ipswich Town | Aston Villa | 1.40 | 1.64 | 32.7% | 24.0% | 43.3% | 58.5% | 60.6% |
| Sáb 28 nov | 13:45 | Serie A | Internazionale | Genoa | 0.97 | 1.36 | 26.6% | 27.5% | 45.9% | 41.1% | 46.0% |
| Sáb 28 nov | 14:00 | LaLiga | Real Madrid | Alavés | 4.65 | 0.66 | 94.8% | 3.7% | 1.5% | 90.0% | 48.1% |
| Sáb 28 nov | 19:00 | Liga MX | Atlas | Toluca | 1.53 | 3.55 | 12.5% | 12.6% | 75.0% | 88.2% | 76.1% |
| Sáb 28 nov | 21:10 | Liga MX | América | Monterrey | 1.19 | 1.18 | 36.3% | 27.8% | 35.8% | 42.4% | 48.3% |
| Dom 29 nov | 05:30 | Serie A | Udinese | Fiorentina | 1.29 | 1.91 | 25.7% | 22.3% | 52.1% | 62.0% | 61.7% |
| Dom 29 nov | 06:00 | Premier League | Everton | Liverpool | 0.47 | 2.03 | 7.4% | 18.1% | 74.5% | 45.4% | 32.3% |
| Dom 29 nov | 07:00 | LaLiga | Valencia | Osasuna | 0.50 | 0.92 | 19.1% | 36.6% | 44.3% | 17.2% | 23.7% |
| Dom 29 nov | 08:00 | Serie A | Sassuolo | Napoli | 0.82 | 3.25 | 5.9% | 10.3% | 83.8% | 77.3% | 53.8% |
| Dom 29 nov | 08:05 | Premier League | Brighton & Hove Albion | Newcastle United | 1.55 | 0.41 | 66.0% | 24.5% | 9.5% | 31.3% | 26.5% |
| Dom 29 nov | 08:05 | Premier League | Crystal Palace | Hull City | 0.58 | 1.54 | 13.9% | 25.4% | 60.7% | 35.5% | 34.6% |
| Dom 29 nov | 08:05 | Premier League | Fulham | AFC Bournemouth | 0.19 | 0.68 | 9.5% | 47.6% | 42.9% | 5.8% | 8.7% |
| Dom 29 nov | 08:05 | Premier League | Sunderland | Tottenham Hotspur | 0.16 | 0.92 | 6.1% | 39.1% | 54.8% | 9.5% | 8.7% |
| Dom 29 nov | 08:30 | Bundesliga | SC Freiburg | RB Leipzig | 1.99 | 2.22 | 35.7% | 20.0% | 44.2% | 79.1% | 76.9% |
| Dom 29 nov | 09:15 | LaLiga | Deportivo | Barcelona | 1.06 | 3.77 | 6.1% | 9.0% | 84.8% | 86.0% | 64.0% |
| Dom 29 nov | 10:30 | Premier League | Arsenal | Manchester City | 2.44 | 0.25 | 86.0% | 11.5% | 2.5% | 50.4% | 19.9% |
| Dom 29 nov | 10:30 | Bundesliga | TSG Hoffenheim | FC Augsburg | 2.88 | 1.09 | 74.1% | 14.5% | 11.4% | 75.6% | 62.5% |
| Dom 29 nov | 11:00 | Serie A | AS Roma | Monza | 5.85 | 1.19 | 95.1% | 3.1% | 1.8% | 97.1% | 69.4% |
| Dom 29 nov | 11:30 | LaLiga | Celta Vigo | Villarreal | 0.50 | 1.33 | 13.9% | 28.6% | 57.5% | 27.7% | 28.9% |
| Dom 29 nov | 12:30 | Bundesliga | Borussia Dortmund | Bayer Leverkusen | 1.71 | 0.65 | 62.9% | 23.3% | 13.8% | 41.9% | 39.2% |
| Dom 29 nov | 13:45 | Serie A | Como | Juventus | 0.94 | 0.64 | 41.0% | 35.1% | 23.9% | 21.0% | 28.7% |
| Dom 29 nov | 14:00 | LaLiga | Real Sociedad | Sevilla | 2.93 | 1.48 | 67.2% | 15.9% | 17.0% | 81.5% | 73.0% |
| Dom 29 nov | 19:07 | Liga MX | Guadalajara | Pachuca | 1.09 | 1.18 | 33.4% | 28.5% | 38.0% | 39.7% | 46.0% |
| Dom 29 nov | 21:00 | Liga MX | Cruz Azul | León | 1.70 | 1.38 | 45.2% | 23.6% | 31.2% | 59.5% | 61.2% |

Promedios de la tabla: xG local 1.48, xG visitante 1.46; P(1) media 37.6%, P(X) media 22.3%, P(2) media 40.1%.

## (b) Tabla de cálculo por equipo (últimos 5 partidos de liga)

GF = goles a favor, GA = goles en contra en los últimos 5. Ataque = (GF/5) / prom. por equipo de la liga; defensa = (GA/5) / prom. por equipo de la liga.

| Liga | Equipo | GF (5) | GA (5) | GF/partido | GA/partido | Ataque | Defensa | Últimos 5 (fecha, H/A, rival, marcador desde el equipo) |
|---|---|---|---|---|---|---|---|---|
| Premier League | AFC Bournemouth | 11 | 1 | 2.20 | 0.20 | 1.630 | 0.148 | 11-21 H vs Nottingham Forest 2-0; 11-08 A vs Ipswich Town 2-1; 10-31 H vs Leeds United 2-0; 10-25 A vs Manchester United 3-0; 10-18 H vs Sunderland 2-0 |
| Premier League | Arsenal | 7 | 2 | 1.40 | 0.40 | 1.037 | 0.296 | 11-21 A vs Newcastle United 2-2; 11-07 H vs Hull City 1-0; 11-01 A vs Liverpool 1-0; 10-24 H vs Everton 2-0; 10-18 A vs Nottingham Forest 1-0 |
| Premier League | Aston Villa | 8 | 6 | 1.60 | 1.20 | 1.185 | 0.889 | 11-21 H vs Sunderland 0-0; 11-08 A vs Manchester United 4-4; 10-31 H vs Fulham 1-1; 10-24 H vs Manchester City 2-1; 10-17 A vs Newcastle United 1-0 |
| Premier League | Brentford | 8 | 5 | 1.60 | 1.00 | 1.185 | 0.741 | 11-23 H vs Everton 4-0; 11-08 A vs Brighton & Hove Albion 0-2; 10-31 H vs Nottingham Forest 2-0; 10-25 A vs Hull City 1-1; 10-17 H vs Liverpool 1-2 |
| Premier League | Brighton & Hove Albion | 8 | 4 | 1.60 | 0.80 | 1.185 | 0.593 | 11-22 A vs Hull City 0-2; 11-08 H vs Brentford 2-0; 10-31 A vs Manchester City 1-0; 10-25 A vs Liverpool 0-2; 10-18 H vs Crystal Palace 5-0 |
| Premier League | Chelsea | 5 | 7 | 1.00 | 1.40 | 0.741 | 1.037 | 11-21 H vs Leeds United 1-4; 11-08 A vs Sunderland 0-1; 10-31 H vs Manchester United 2-0; 10-24 H vs Tottenham Hotspur 0-2; 10-17 A vs Everton 2-0 |
| Premier League | Coventry City | 8 | 10 | 1.60 | 2.00 | 1.185 | 1.481 | 11-21 H vs Crystal Palace 3-2; 11-06 A vs Everton 1-3; 10-31 H vs Sunderland 3-1; 10-24 H vs Fulham 0-1; 10-19 A vs Tottenham Hotspur 1-3 |
| Premier League | Crystal Palace | 3 | 15 | 0.60 | 3.00 | 0.444 | 2.222 | 11-21 A vs Coventry City 2-3; 11-08 H vs Liverpool 1-3; 10-31 A vs Tottenham Hotspur 0-2; 10-25 H vs Newcastle United 0-2; 10-18 A vs Brighton & Hove Albion 0-5 |
| Premier League | Everton | 4 | 9 | 0.80 | 1.80 | 0.593 | 1.333 | 11-23 A vs Brentford 0-4; 11-06 H vs Coventry City 3-1; 11-02 A vs Newcastle United 1-0; 10-24 A vs Arsenal 0-2; 10-17 H vs Chelsea 0-2 |
| Premier League | Fulham | 5 | 3 | 1.00 | 0.60 | 0.741 | 0.444 | 11-21 A vs Manchester City 1-1; 11-07 H vs Newcastle United 1-1; 10-31 A vs Aston Villa 1-1; 10-24 A vs Coventry City 1-0; 10-17 H vs Hull City 1-0 |
| Premier League | Hull City | 5 | 5 | 1.00 | 1.00 | 0.741 | 0.741 | 11-22 H vs Brighton & Hove Albion 2-0; 11-07 A vs Arsenal 0-1; 10-31 H vs Ipswich Town 2-2; 10-25 H vs Brentford 1-1; 10-17 A vs Fulham 0-1 |
| Premier League | Ipswich Town | 6 | 10 | 1.20 | 2.00 | 0.889 | 1.481 | 11-21 A vs Tottenham Hotspur 0-2; 11-08 H vs AFC Bournemouth 1-2; 10-31 A vs Hull City 2-2; 10-23 H vs Nottingham Forest 1-1; 10-17 A vs Manchester City 2-3 |
| Premier League | Leeds United | 6 | 4 | 1.20 | 0.80 | 0.889 | 0.593 | 11-21 A vs Chelsea 4-1; 11-07 H vs Tottenham Hotspur 1-0; 10-31 A vs AFC Bournemouth 0-2; 10-25 A vs Sunderland 0-0; 10-18 H vs Manchester United 1-1 |
| Premier League | Liverpool | 11 | 3 | 2.20 | 0.60 | 1.630 | 0.444 | 11-22 H vs Manchester United 4-0; 11-08 A vs Crystal Palace 3-1; 11-01 H vs Arsenal 0-1; 10-25 H vs Brighton & Hove Albion 2-0; 10-17 A vs Brentford 2-1 |
| Premier League | Manchester City | 6 | 9 | 1.20 | 1.80 | 0.889 | 1.333 | 11-21 H vs Fulham 1-1; 11-07 A vs Nottingham Forest 1-3; 10-31 H vs Brighton & Hove Albion 0-1; 10-24 A vs Aston Villa 1-2; 10-17 H vs Ipswich Town 3-2 |
| Premier League | Manchester United | 5 | 14 | 1.00 | 2.80 | 0.741 | 2.074 | 11-22 A vs Liverpool 0-4; 11-08 H vs Aston Villa 4-4; 10-31 A vs Chelsea 0-2; 10-25 H vs AFC Bournemouth 0-3; 10-18 A vs Leeds United 1-1 |
| Premier League | Newcastle United | 5 | 5 | 1.00 | 1.00 | 0.741 | 0.741 | 11-21 H vs Arsenal 2-2; 11-07 A vs Fulham 1-1; 11-02 H vs Everton 0-1; 10-25 A vs Crystal Palace 2-0; 10-17 H vs Aston Villa 0-1 |
| Premier League | Nottingham Forest | 4 | 7 | 0.80 | 1.40 | 0.593 | 1.037 | 11-21 A vs AFC Bournemouth 0-2; 11-07 H vs Manchester City 3-1; 10-31 A vs Brentford 0-2; 10-23 A vs Ipswich Town 1-1; 10-18 H vs Arsenal 0-1 |
| Premier League | Sunderland | 2 | 5 | 0.40 | 1.00 | 0.296 | 0.741 | 11-21 A vs Aston Villa 0-0; 11-08 H vs Chelsea 1-0; 10-31 A vs Coventry City 1-3; 10-25 H vs Leeds United 0-0; 10-18 A vs AFC Bournemouth 0-2 |
| Premier League | Tottenham Hotspur | 9 | 2 | 1.80 | 0.40 | 1.333 | 0.296 | 11-21 H vs Ipswich Town 2-0; 11-07 A vs Leeds United 0-1; 10-31 H vs Crystal Palace 2-0; 10-24 A vs Chelsea 2-0; 10-19 H vs Coventry City 3-1 |
| LaLiga | Alavés | 6 | 10 | 1.20 | 2.00 | 1.053 | 1.754 | 11-21 H vs Deportivo 3-1; 11-06 A vs Sevilla 0-0; 10-31 A vs Barcelona 1-6; 10-23 H vs Málaga 1-1; 10-18 A vs Celta Vigo 1-2 |
| LaLiga | Athletic Club | 8 | 6 | 1.60 | 1.20 | 1.404 | 1.053 | 11-20 H vs Espanyol 0-1; 11-07 A vs Osasuna 1-1; 11-01 H vs Real Sociedad 2-1; 10-25 H vs Getafe 4-0; 10-21 A vs Levante 1-3 |
| LaLiga | Atlético Madrid | 8 | 2 | 1.60 | 0.40 | 1.404 | 0.351 | 11-22 A vs Getafe 3-0; 11-08 H vs Barcelona 1-2; 10-31 A vs Levante 2-0; 10-24 H vs Deportivo 1-0; 10-17 A vs Espanyol 1-0 |
| LaLiga | Barcelona | 17 | 8 | 3.40 | 1.60 | 2.982 | 1.404 | 11-22 H vs Villarreal 3-2; 11-08 A vs Atlético Madrid 2-1; 10-31 H vs Alavés 6-1; 10-25 H vs Real Madrid 1-2; 10-17 A vs Real Betis 5-2 |
| LaLiga | Celta Vigo | 3 | 6 | 0.60 | 1.20 | 0.526 | 1.053 | 11-21 A vs Real Madrid 1-2; 11-08 H vs Levante 0-0; 10-31 A vs Rayo Vallecano 0-3; 10-25 H vs Real Betis 0-0; 10-18 H vs Alavés 2-1 |
| LaLiga | Deportivo | 4 | 6 | 0.80 | 1.20 | 0.702 | 1.053 | 11-21 A vs Alavés 1-3; 11-07 A vs Espanyol 0-0; 11-02 H vs Osasuna 2-1; 10-24 A vs Atlético Madrid 0-1; 10-16 H vs Levante 1-1 |
| LaLiga | Elche | 4 | 4 | 0.80 | 0.80 | 0.702 | 0.702 | 11-23 A vs Levante 1-1; 11-08 H vs Real Betis 0-2; 11-01 H vs Valencia 0-1; 10-24 A vs Rayo Vallecano 3-0; 10-17 A vs Villarreal 0-0 |
| LaLiga | Levante | 5 | 6 | 1.00 | 1.20 | 0.877 | 1.053 | 11-23 H vs Elche 1-1; 11-08 A vs Celta Vigo 0-0; 10-31 H vs Atlético Madrid 0-2; 10-25 A vs Real Sociedad 1-2; 10-21 H vs Athletic Club 3-1 |
| LaLiga | Málaga | 5 | 11 | 1.00 | 2.20 | 0.877 | 1.930 | 11-22 A vs Osasuna 0-1; 11-07 H vs Racing Santander 1-2; 10-31 A vs Real Betis 1-2; 10-23 A vs Alavés 1-1; 10-18 H vs Real Sociedad 2-5 |
| LaLiga | Osasuna | 5 | 5 | 1.00 | 1.00 | 0.877 | 0.877 | 11-22 H vs Málaga 1-0; 11-07 H vs Athletic Club 1-1; 11-02 A vs Deportivo 1-2; 10-26 A vs Sevilla 0-2; 10-18 H vs Racing Santander 2-0 |
| LaLiga | Racing Santander | 7 | 9 | 1.40 | 1.80 | 1.228 | 1.579 | 11-22 H vs Real Sociedad 3-2; 11-07 A vs Málaga 2-1; 11-01 H vs Real Madrid 0-3; 10-24 H vs Espanyol 2-1; 10-18 A vs Osasuna 0-2 |
| LaLiga | Rayo Vallecano | 4 | 6 | 0.80 | 1.20 | 0.702 | 1.053 | 11-21 H vs Valencia 0-1; 11-08 A vs Real Sociedad 0-1; 10-31 H vs Celta Vigo 3-0; 10-24 H vs Elche 0-3; 10-19 A vs Getafe 1-1 |
| LaLiga | Real Betis | 7 | 7 | 1.40 | 1.40 | 1.228 | 1.228 | 11-21 A vs Sevilla 1-1; 11-08 A vs Elche 2-0; 10-31 H vs Málaga 2-1; 10-25 A vs Celta Vigo 0-0; 10-17 H vs Barcelona 2-5 |
| LaLiga | Real Madrid | 14 | 3 | 2.80 | 0.60 | 2.456 | 0.526 | 11-21 H vs Celta Vigo 2-1; 11-07 A vs Valencia 3-0; 11-01 A vs Racing Santander 3-0; 10-25 A vs Barcelona 2-1; 10-18 H vs Sevilla 4-1 |
| LaLiga | Real Sociedad | 11 | 8 | 2.20 | 1.60 | 1.930 | 1.404 | 11-22 A vs Racing Santander 2-3; 11-08 H vs Rayo Vallecano 1-0; 11-01 A vs Athletic Club 1-2; 10-25 H vs Levante 2-1; 10-18 A vs Málaga 5-2 |
| LaLiga | Sevilla | 5 | 8 | 1.00 | 1.60 | 0.877 | 1.404 | 11-21 H vs Real Betis 1-1; 11-06 H vs Alavés 0-0; 11-01 A vs Getafe 1-3; 10-26 H vs Osasuna 2-0; 10-18 A vs Real Madrid 1-4 |
| LaLiga | Valencia | 3 | 5 | 0.60 | 1.00 | 0.526 | 0.877 | 11-21 A vs Rayo Vallecano 1-0; 11-07 H vs Real Madrid 0-3; 11-01 A vs Elche 1-0; 10-24 H vs Villarreal 1-2; 10-17 H vs Athletic Club 0-0 |
| LaLiga | Villarreal | 6 | 5 | 1.20 | 1.00 | 1.053 | 0.877 | 11-22 A vs Barcelona 2-3; 11-08 H vs Getafe 2-0; 10-30 H vs Espanyol 0-1; 10-24 A vs Valencia 2-1; 10-17 H vs Elche 0-0 |
| Bundesliga | 1. FC Union Berlin | 3 | 9 | 0.60 | 1.80 | 0.400 | 1.200 | 11-21 H vs RB Leipzig 1-5; 11-08 A vs SC Freiburg 0-2; 11-01 H vs FC Cologne 1-1; 10-24 A vs FC Augsburg 1-1; 10-17 H vs Borussia Dortmund 0-0 |
| Bundesliga | Bayer Leverkusen | 10 | 9 | 2.00 | 1.80 | 1.333 | 1.200 | 11-21 H vs SC Paderborn 07 4-0; 11-08 A vs FC Cologne 2-1; 10-31 H vs VfB Stuttgart 2-4; 10-25 A vs TSG Hoffenheim 0-3; 10-18 H vs SC Freiburg 2-1 |
| Bundesliga | Bayern Munich | 14 | 6 | 2.80 | 1.20 | 1.867 | 0.800 | 11-20 H vs FC Cologne 1-1; 11-07 A vs Mainz 2-1; 10-31 H vs Borussia Dortmund 2-2; 10-25 A vs SC Freiburg 3-1; 10-17 H vs RB Leipzig 6-1 |
| Bundesliga | Borussia Dortmund | 6 | 3 | 1.20 | 0.60 | 0.800 | 0.400 | 11-21 A vs Borussia Mönchengladbach 1-0; 11-07 H vs SV Elversberg 2-1; 10-31 A vs Bayern Munich 2-2; 10-24 H vs Eintracht Frankfurt 1-0; 10-17 A vs 1. FC Union Berlin 0-0 |
| Bundesliga | Borussia Mönchengladbach | 5 | 8 | 1.00 | 1.60 | 0.667 | 1.067 | 11-21 H vs Borussia Dortmund 0-1; 11-06 A vs Hamburg SV 1-3; 10-31 H vs SC Paderborn 07 0-0; 10-23 A vs VfB Stuttgart 3-2; 10-18 H vs TSG Hoffenheim 1-2 |
| Bundesliga | Eintracht Frankfurt | 7 | 4 | 1.40 | 0.80 | 0.933 | 0.533 | 11-21 H vs TSG Hoffenheim 1-0; 11-07 A vs SC Paderborn 07 2-2; 11-01 H vs Hamburg SV 3-1; 10-24 A vs Borussia Dortmund 0-1; 10-16 H vs FC Cologne 1-0 |
| Bundesliga | FC Augsburg | 10 | 13 | 2.00 | 2.60 | 1.333 | 1.733 | 11-22 H vs Mainz 3-1; 11-07 A vs RB Leipzig 2-5; 10-31 H vs SC Freiburg 1-2; 10-24 H vs 1. FC Union Berlin 1-1; 10-17 A vs SV Elversberg 3-4 |
| Bundesliga | FC Cologne | 3 | 5 | 0.60 | 1.00 | 0.400 | 0.667 | 11-20 A vs Bayern Munich 1-1; 11-08 H vs Bayer Leverkusen 1-2; 11-01 A vs 1. FC Union Berlin 1-1; 10-24 H vs Schalke 04 0-0; 10-16 A vs Eintracht Frankfurt 0-1 |
| Bundesliga | Hamburg SV | 5 | 9 | 1.00 | 1.80 | 0.667 | 1.200 | 11-22 A vs Werder Bremen 0-4; 11-06 H vs Borussia Mönchengladbach 3-1; 11-01 A vs Eintracht Frankfurt 1-3; 10-24 A vs SC Paderborn 07 0-1; 10-17 H vs VfB Stuttgart 1-0 |
| Bundesliga | Mainz | 6 | 12 | 1.20 | 2.40 | 0.800 | 1.600 | 11-22 A vs FC Augsburg 1-3; 11-07 H vs Bayern Munich 1-2; 10-30 A vs SV Elversberg 1-4; 10-24 H vs Werder Bremen 2-3; 10-17 A vs Schalke 04 1-0 |
| Bundesliga | RB Leipzig | 17 | 9 | 3.40 | 1.80 | 2.267 | 1.200 | 11-21 A vs 1. FC Union Berlin 5-1; 11-07 H vs FC Augsburg 5-2; 10-31 A vs Schalke 04 2-0; 10-24 H vs SV Elversberg 4-0; 10-17 A vs Bayern Munich 1-6 |
| Bundesliga | SC Freiburg | 7 | 6 | 1.40 | 1.20 | 0.933 | 0.800 | 11-21 A vs SV Elversberg 1-0; 11-08 H vs 1. FC Union Berlin 2-0; 10-31 A vs FC Augsburg 2-1; 10-25 H vs Bayern Munich 1-3; 10-18 A vs Bayer Leverkusen 1-2 |
| Bundesliga | SC Paderborn 07 | 5 | 8 | 1.00 | 1.60 | 0.667 | 1.067 | 11-21 A vs Bayer Leverkusen 0-4; 11-07 H vs Eintracht Frankfurt 2-2; 10-31 A vs Borussia Mönchengladbach 0-0; 10-24 H vs Hamburg SV 1-0; 10-17 A vs Werder Bremen 2-2 |
| Bundesliga | SV Elversberg | 9 | 11 | 1.80 | 2.20 | 1.200 | 1.467 | 11-21 H vs SC Freiburg 0-1; 11-07 A vs Borussia Dortmund 1-2; 10-30 H vs Mainz 4-1; 10-24 A vs RB Leipzig 0-4; 10-17 H vs FC Augsburg 4-3 |
| Bundesliga | Schalke 04 | 1 | 5 | 0.20 | 1.00 | 0.133 | 0.667 | 11-21 H vs VfB Stuttgart 0-0; 11-08 A vs TSG Hoffenheim 1-2; 10-31 H vs RB Leipzig 0-2; 10-24 A vs FC Cologne 0-0; 10-17 H vs Mainz 0-1 |
| Bundesliga | TSG Hoffenheim | 7 | 5 | 1.40 | 1.00 | 0.933 | 0.667 | 11-21 A vs Eintracht Frankfurt 0-1; 11-08 H vs Schalke 04 2-1; 10-31 A vs Werder Bremen 0-2; 10-25 H vs Bayer Leverkusen 3-0; 10-18 A vs Borussia Mönchengladbach 2-1 |
| Bundesliga | VfB Stuttgart | 7 | 6 | 1.40 | 1.20 | 0.933 | 0.800 | 11-21 A vs Schalke 04 0-0; 11-07 H vs Werder Bremen 1-0; 10-31 A vs Bayer Leverkusen 4-2; 10-23 H vs Borussia Mönchengladbach 2-3; 10-17 A vs Hamburg SV 0-1 |
| Bundesliga | Werder Bremen | 11 | 5 | 2.20 | 1.00 | 1.467 | 0.667 | 11-22 H vs Hamburg SV 4-0; 11-07 A vs VfB Stuttgart 0-1; 10-31 H vs TSG Hoffenheim 2-0; 10-24 A vs Mainz 3-2; 10-17 H vs SC Paderborn 07 2-2 |
| Serie A | AS Roma | 20 | 8 | 4.00 | 1.60 | 2.526 | 1.011 | 11-21 A vs Parma 5-1; 11-07 H vs Sassuolo 3-0; 10-31 A vs Udinese 5-2; 10-27 H vs Cagliari 4-2; 10-24 A vs Napoli 3-3 |
| Serie A | Bologna | 11 | 5 | 2.20 | 1.00 | 1.389 | 0.632 | 11-22 H vs Udinese 1-1; 11-07 A vs Parma 2-1; 10-31 H vs Monza 2-1; 10-28 A vs AC Milan 4-2; 10-24 A vs Cagliari 2-0 |
| Serie A | Como | 8 | 3 | 1.60 | 0.60 | 1.011 | 0.379 | 11-21 H vs Cagliari 2-0; 11-08 A vs Internazionale 0-2; 11-01 H vs Venezia 1-0; 10-27 A vs Torino 3-1; 10-24 H vs Sassuolo 2-0 |
| Serie A | Fiorentina | 9 | 11 | 1.80 | 2.20 | 1.137 | 1.389 | 11-23 A vs Monza 0-3; 11-08 H vs Juventus 2-2; 11-02 A vs Sassuolo 4-2; 10-29 H vs Atalanta 2-2; 10-25 A vs Internazionale 1-2 |
| Serie A | Frosinone | 12 | 11 | 2.40 | 2.20 | 1.516 | 1.389 | 11-22 A vs AC Milan 1-5; 11-07 A vs Cagliari 0-1; 11-01 H vs Torino 2-0; 10-29 H vs Lecce 5-1; 10-25 A vs Atalanta 4-4 |
| Serie A | Genoa | 8 | 3 | 1.60 | 0.60 | 1.011 | 0.379 | 11-22 A vs Sassuolo 2-0; 11-08 H vs AC Milan 1-2; 11-01 A vs Lecce 2-1; 10-28 H vs Juventus 2-0; 10-25 H vs Venezia 1-0 |
| Serie A | Internazionale | 11 | 8 | 2.20 | 1.60 | 1.389 | 1.011 | 11-22 A vs Atalanta 4-4; 11-08 H vs Como 2-0; 10-31 A vs AC Milan 1-3; 10-28 A vs Venezia 2-0; 10-25 H vs Fiorentina 2-1 |
| Serie A | Juventus | 10 | 4 | 2.00 | 0.80 | 1.263 | 0.505 | 11-22 H vs Venezia 4-0; 11-08 A vs Fiorentina 2-2; 11-01 H vs Napoli 2-0; 10-28 A vs Genoa 0-2; 10-25 A vs Lecce 2-0 |
| Serie A | Lazio | 14 | 5 | 2.80 | 1.00 | 1.768 | 0.632 | 11-21 H vs Lecce 3-0; 11-08 A vs Napoli 1-1; 11-01 H vs Cagliari 2-1; 10-27 A vs Sassuolo 6-2; 10-24 H vs Parma 2-1 |
| Serie A | Monza | 7 | 10 | 1.40 | 2.00 | 0.884 | 1.263 | 11-23 H vs Fiorentina 3-0; 11-08 H vs Atalanta 0-1; 10-31 A vs Bologna 1-2; 10-28 H vs Napoli 1-4; 10-23 A vs Torino 2-3 |
| Serie A | Napoli | 9 | 7 | 1.80 | 1.40 | 1.137 | 0.884 | 11-21 H vs Torino 1-0; 11-08 H vs Lazio 1-1; 11-01 A vs Juventus 0-2; 10-28 A vs Monza 4-1; 10-24 H vs AS Roma 3-3 |
| Serie A | Parma | 6 | 9 | 1.20 | 1.80 | 0.758 | 1.137 | 11-21 H vs AS Roma 1-5; 11-07 H vs Bologna 1-2; 11-02 A vs Atalanta 3-0; 10-28 H vs Udinese 0-0; 10-24 A vs Lazio 1-2 |
| Serie A | Sassuolo | 4 | 17 | 0.80 | 3.40 | 0.505 | 2.147 | 11-22 H vs Genoa 0-2; 11-07 A vs AS Roma 0-3; 11-02 H vs Fiorentina 2-4; 10-27 H vs Lazio 2-6; 10-24 A vs Como 0-2 |
| Serie A | Torino | 5 | 9 | 1.00 | 1.80 | 0.632 | 1.137 | 11-21 A vs Napoli 0-1; 11-07 H vs Lecce 1-1; 11-01 A vs Frosinone 0-2; 10-27 H vs Como 1-3; 10-23 H vs Monza 3-2 |
| Serie A | Udinese | 4 | 10 | 0.80 | 2.00 | 0.505 | 1.263 | 11-22 A vs Bologna 1-1; 11-06 A vs Venezia 1-2; 10-31 H vs AS Roma 2-5; 10-28 A vs Parma 0-0; 10-25 H vs AC Milan 0-2 |
| Serie A | Venezia | 2 | 9 | 0.40 | 1.80 | 0.253 | 1.137 | 11-22 A vs Juventus 0-4; 11-06 H vs Udinese 2-1; 11-01 A vs Como 0-1; 10-28 H vs Internazionale 0-2; 10-25 A vs Genoa 0-1 |
| Liga MX | América | 5 | 6 | 1.00 | 1.20 | 0.836 | 1.004 | 11-26 A vs Monterrey 0-0; 11-22 A vs Tigres UANL 0-1; 11-08 A vs Pumas UNAM 2-2; 11-01 H vs Toluca 2-2; 10-29 H vs Tijuana 1-1 |
| Liga MX | Atlas | 9 | 12 | 1.80 | 2.40 | 1.505 | 2.007 | 11-26 A vs Toluca 0-2; 11-21 A vs FC Juárez 3-3; 11-07 H vs Pachuca 1-4; 10-31 A vs Atlético de San Luis 1-0; 10-25 H vs Puebla 4-3 |
| Liga MX | Cruz Azul | 10 | 6 | 2.00 | 1.20 | 1.673 | 1.004 | 11-22 A vs Guadalajara 0-1; 11-08 A vs Tigres UANL 3-2; 11-02 H vs León 2-1; 10-26 A vs Querétaro 3-1; 10-22 A vs Pachuca 2-1 |
| Liga MX | Guadalajara | 8 | 3 | 1.60 | 0.60 | 1.338 | 0.502 | 11-22 H vs Cruz Azul 1-0; 11-09 A vs León 1-1; 11-01 H vs Atlante 4-2; 10-25 A vs Monterrey 1-0; 10-21 H vs Necaxa 1-0 |
| Liga MX | León | 7 | 5 | 1.40 | 1.00 | 1.171 | 0.836 | 11-21 A vs Santos 2-1; 11-09 H vs Guadalajara 1-1; 11-02 A vs Cruz Azul 1-2; 10-24 H vs Toluca 1-1; 10-21 A vs Tigres UANL 2-0 |
| Liga MX | Monterrey | 6 | 7 | 1.20 | 1.40 | 1.004 | 1.171 | 11-26 H vs América 0-0; 11-22 A vs Pumas UNAM 2-0; 11-14 A vs Querétaro 1-0; 11-08 A vs Toluca 0-4; 11-01 H vs Tijuana 3-3 |
| Liga MX | Pachuca | 12 | 4 | 2.40 | 0.80 | 2.007 | 0.669 | 11-21 H vs Toluca 2-0; 11-07 A vs Atlas 4-1; 10-31 H vs Tigres UANL 3-0; 10-26 A vs América 2-1; 10-22 H vs Cruz Azul 1-2 |
| Liga MX | Toluca | 9 | 5 | 1.80 | 1.00 | 1.505 | 0.836 | 11-26 H vs Atlas 2-0; 11-21 A vs Pachuca 0-2; 11-08 H vs Monterrey 4-0; 11-01 A vs América 2-2; 10-24 A vs León 1-1 |

## (c) Promedios de liga usados y cómo se calcularon

Los promedios se calcularon desde los scoreboards de las últimas ~3 jornadas completadas antes del cutoff (partidos con STATUS_FULL_TIME). El endpoint de posiciones (standings) de ESPN devuelve 404, por eso se usan scoreboards.

| Liga | Jornadas usadas (fechas) | Partidos | Goles local | Goles visitante | Prom. goles/partido | Prom. local | Prom. visitante | Prom. por equipo |
|---|---|---|---|---|---|---|---|---|
| Premier League | 20261031, 20261101, 20261102, 20261106, 20261107, 20261108, 20261121, 20261122, 20261123 | 30 | 53 | 28 | 2.700 | 1.767 | 0.933 | 1.350 |
| LaLiga | 20261101, 20261102, 20261106, 20261107, 20261108, 20261120, 20261121, 20261122, 20261123 | 25 | 27 | 30 | 2.280 | 1.080 | 1.200 | 1.140 |
| Bundesliga | 20261030, 20261031, 20261101, 20261106, 20261107, 20261108, 20261120, 20261121, 20261122 | 27 | 48 | 33 | 3.000 | 1.778 | 1.222 | 1.500 |
| Serie A | 20261031, 20261101, 20261102, 20261106, 20261107, 20261108, 20261121, 20261122, 20261123 | 30 | 55 | 40 | 3.167 | 1.833 | 1.333 | 1.583 |
| Liga MX | 20261101, 20261106, 20261107, 20261108, 20261114, 20261120, 20261121, 20261122, 20261125 | 23 | 28 | 27 | 2.391 | 1.217 | 1.174 | 1.196 |

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
