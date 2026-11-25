# Tabla de probabilidades Poisson — Semana 2 entre semana (Football AI Agenda)

**Partidos:** 2026-11-24 al 2026-11-26, horas de Monterrey (CST). **Fuente de datos:** ESPN, API pública sin clave.
**Método:** modelo Poisson con goles esperados (xG) por equipo, distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.
**Fecha de cálculo:** 2026-11-22. Últimos 4 partidos por equipo: partidos de liga completados hasta el 2026-11-22.

## (a) Tabla de los 35 partidos

| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mar 24 nov | 11:45 | Champions League | Galatasaray | Aston Villa | 1.59 | 2.99 | 18.1% | 15.9% | 66.0% | 83.5% | 75.6% |
| Mar 24 nov | 14:00 | Champions League | Arsenal | Borussia Dortmund | 1.33 | 0.58 | 55.0% | 28.7% | 16.3% | 29.8% | 32.4% |
| Mar 24 nov | 14:00 | Champions League | Manchester City | Napoli | 4.38 | 1.16 | 88.4% | 6.9% | 4.7% | 91.4% | 67.8% |
| Mar 24 nov | 14:00 | Champions League | Real Madrid | PSV Eindhoven | 1.72 | 0.58 | 65.2% | 22.8% | 12.0% | 40.5% | 36.2% |
| Mié 25 nov | 11:45 | Champions League | Sabah FK | Barcelona | 0.80 | 3.87 | 3.6% | 7.0% | 89.4% | 84.5% | 53.7% |
| Mié 25 nov | 11:45 | Champions League | Slavia Prague | Villarreal | 2.32 | 1.99 | 46.3% | 19.7% | 34.1% | 80.4% | 77.9% |
| Mié 25 nov | 14:00 | Champions League | Club Brugge | Liverpool | 3.65 | 2.71 | 56.6% | 15.2% | 28.2% | 95.2% | 90.9% |
| Mié 25 nov | 14:00 | Champions League | Internazionale | VfB Stuttgart | 1.06 | 1.16 | 33.0% | 28.9% | 38.1% | 38.3% | 44.9% |
| Mié 25 nov | 14:00 | Champions League | Lille | Bayern Munich | 0.66 | 3.32 | 4.2% | 8.9% | 87.0% | 75.9% | 46.7% |
| Mié 25 nov | 14:00 | Champions League | Paris Saint-Germain | AS Roma | 5.30 | 1.38 | 91.6% | 4.9% | 3.5% | 96.3% | 74.6% |
| Mié 25 nov | 14:00 | Champions League | Sporting CP | Manchester United | 2.12 | 0.89 | 65.8% | 19.6% | 14.6% | 57.8% | 51.7% |
| Mié 25 nov | 14:00 | Champions League | Atlético Madrid | Viking FK | 1.33 | 1.24 | 38.6% | 26.5% | 34.8% | 47.4% | 52.3% |
| Mié 25 nov | 14:00 | Champions League | Shakhtar Donetsk | Fenerbahce | 1.46 | 0.66 | 56.3% | 26.7% | 17.0% | 35.6% | 37.2% |
| Mié 25 nov | 19:00 | Liga MX | Toluca | Atlas | 3.89 | 2.05 | 70.9% | 12.8% | 16.3% | 93.5% | 85.4% |
| Mié 25 nov | 21:10 | Liga MX | Monterrey | América | 1.38 | 1.28 | 39.5% | 26.0% | 34.5% | 49.7% | 54.1% |
| Jue 26 nov | 11:45 | Europa League | Celta Vigo | AFC Bournemouth | 0.32 | 2.88 | 2.4% | 8.8% | 88.8% | 62.1% | 26.1% |
| Jue 26 nov | 11:45 | Europa League | Dinamo Zagreb | Bayer Leverkusen | 0.20 | 1.40 | 5.2% | 26.4% | 68.5% | 21.6% | 13.8% |
| Jue 26 nov | 11:45 | Europa League | Olympiacos | AC Milan | 1.13 | 0.17 | 61.7% | 32.7% | 5.7% | 14.5% | 10.9% |
| Jue 26 nov | 11:45 | Europa League | Besiktas | Hapoel Be'er | 3.56 | 0.35 | 93.2% | 5.4% | 1.4% | 74.9% | 28.6% |
| Jue 26 nov | 11:45 | Europa League | Marseille | Levski Sofia | 0.24 | 1.05 | 8.5% | 35.0% | 56.5% | 14.1% | 14.0% |
| Jue 26 nov | 11:45 | Europa League | RB Salzburg | Ararat-Armenia | 1.70 | 1.40 | 44.8% | 23.6% | 31.6% | 59.8% | 61.5% |
| Jue 26 nov | 11:45 | Europa League | Union St.-Gilloise | Lech Poznan | 4.86 | 0.17 | 98.5% | 1.3% | 0.2% | 87.8% | 15.9% |
| Jue 26 nov | 11:45 | Europa League | Viktoria Plzen | Benfica | 0.36 | 3.97 | 1.1% | 4.0% | 94.9% | 80.7% | 30.0% |
| Jue 26 nov | 14:00 | Europa League | Crystal Palace | Real Sociedad | 1.46 | 2.36 | 23.1% | 19.4% | 57.6% | 73.3% | 69.4% |
| Jue 26 nov | 14:00 | Europa League | Ferencvaros | NK Celje | 4.01 | 0.65 | 92.0% | 5.6% | 2.4% | 84.4% | 47.2% |
| Jue 26 nov | 14:00 | Europa League | Juventus | Omonia Nicosia | 3.12 | 1.05 | 78.1% | 12.6% | 9.3% | 78.5% | 62.0% |
| Jue 26 nov | 14:00 | Europa League | Lyon | Lillestrom | 2.43 | 0.61 | 77.6% | 15.0% | 7.4% | 58.6% | 41.7% |
| Jue 26 nov | 14:00 | Europa League | NEC Nijmegen | Stade Rennais | 0.97 | 1.57 | 23.4% | 25.3% | 51.3% | 46.7% | 49.2% |
| Jue 26 nov | 14:00 | Europa League | OFI Crete | Anderlecht | 0.61 | 1.05 | 21.0% | 33.4% | 45.6% | 23.1% | 29.5% |
| Jue 26 nov | 14:00 | Europa League | Sparta Prague | AZ Alkmaar | 0.97 | 1.83 | 19.7% | 22.7% | 57.6% | 53.1% | 52.2% |
| Jue 26 nov | 14:00 | Europa League | Sunderland | Jagiellonia Bialystok | 1.13 | 0.70 | 46.0% | 31.4% | 22.6% | 27.8% | 34.1% |
| Jue 26 nov | 14:00 | Europa League | Torreense | Celtic | 3.12 | 2.36 | 54.2% | 16.7% | 29.2% | 91.0% | 86.5% |
| Jue 26 nov | 14:00 | Europa League | TSG Hoffenheim | SK Sturm Graz | 1.46 | 0.79 | 53.1% | 26.7% | 20.2% | 38.9% | 41.7% |
| Jue 26 nov | 19:00 | Liga MX | Pachuca | Guadalajara | 1.04 | 0.85 | 39.1% | 31.7% | 29.2% | 29.4% | 37.0% |
| Jue 26 nov | 21:10 | Liga MX | León | Cruz Azul | 1.21 | 1.33 | 33.8% | 26.7% | 39.5% | 46.7% | 51.7% |

Promedios de la tabla: xG local 1.91, xG visitante 1.50; P(1) media 46.0%, P(X) media 19.3%, P(2) media 34.7%.

## (b) Tabla de cálculo por equipo (últimos 4 partidos de liga)

GF = goles a favor, GA = goles en contra en los últimos 4. Ataque = (GF/4) / prom. por equipo de la liga; defensa = (GA/4) / prom. por equipo de la liga.

| Liga | Equipo | GF (4) | GA (4) | GF/partido | GA/partido | Ataque | Defensa | Últimos 4 (fecha, H/A, rival, marcador desde el equipo) |
|---|---|---|---|---|---|---|---|---|
| Liga MX | América | 6 | 8 | 1.20 | 1.60 | 0.832 | 1.109 | 11-22 A vs Tigres UANL 0-1; 11-08 A vs Pumas UNAM 2-2; 11-01 H vs Toluca 2-2; 10-29 H vs Tijuana 1-1; 10-26 H vs Pachuca 1-2 |
| Liga MX | Atlas | 11 | 15 | 2.20 | 3.00 | 1.525 | 2.080 | 11-21 A vs FC Juárez 3-3; 11-07 H vs Pachuca 1-4; 10-31 A vs Atlético de San Luis 1-0; 10-25 H vs Puebla 4-3; 10-22 H vs América 2-5 |
| Liga MX | Cruz Azul | 10 | 6 | 2.00 | 1.20 | 1.387 | 0.832 | 11-22 A vs Guadalajara 0-1; 11-08 A vs Tigres UANL 3-2; 11-02 H vs León 2-1; 10-26 A vs Querétaro 3-1; 10-22 A vs Pachuca 2-1 |
| Liga MX | Guadalajara | 8 | 3 | 1.60 | 0.60 | 1.109 | 0.416 | 11-22 H vs Cruz Azul 1-0; 11-09 A vs León 1-1; 11-01 H vs Atlante 4-2; 10-25 A vs Monterrey 1-0; 10-21 H vs Necaxa 1-0 |
| Liga MX | León | 7 | 5 | 1.40 | 1.00 | 0.971 | 0.693 | 11-21 A vs Santos 2-1; 11-09 H vs Guadalajara 1-1; 11-02 A vs Cruz Azul 1-2; 10-24 H vs Toluca 1-1; 10-21 A vs Tigres UANL 2-0 |
| Liga MX | Monterrey | 6 | 8 | 1.20 | 1.60 | 0.832 | 1.109 | 11-22 A vs Pumas UNAM 2-0; 11-14 A vs Querétaro 1-0; 11-08 A vs Toluca 0-4; 11-01 H vs Tijuana 3-3; 10-25 H vs Guadalajara 0-1 |
| Liga MX | Pachuca | 12 | 4 | 2.40 | 0.80 | 1.664 | 0.555 | 11-21 H vs Toluca 2-0; 11-07 A vs Atlas 4-1; 10-31 H vs Tigres UANL 3-0; 10-26 A vs América 2-1; 10-22 H vs Cruz Azul 1-2 |
| Liga MX | Toluca | 9 | 7 | 1.80 | 1.40 | 1.248 | 0.971 | 11-21 A vs Pachuca 0-2; 11-08 H vs Monterrey 4-0; 11-01 A vs América 2-2; 10-24 A vs León 1-1; 10-22 H vs Tijuana 2-2 |
| Champions League | AS Roma | 10 | 8 | 2.50 | 2.00 | 1.216 | 0.973 | 11-03 A vs Manchester United 2-3; 10-20 H vs Slovan Bratislava 4-0; 10-14 H vs Real Madrid 3-4; 09-10 A vs Fenerbahce 1-1 |
| Champions League | Arsenal | 8 | 3 | 2.00 | 0.75 | 0.973 | 0.365 | 11-04 A vs Slavia Prague 2-1; 10-21 A vs Bayern Munich 2-2; 10-13 H vs Lille 3-0; 09-09 A vs Napoli 1-0 |
| Champions League | Aston Villa | 12 | 6 | 3.00 | 1.50 | 1.459 | 0.730 | 11-03 A vs Barcelona 0-3; 10-21 H vs Viking FK 3-1; 10-14 H vs Fenerbahce 6-0; 09-08 A vs Club Brugge 3-2 |
| Champions League | Atlético Madrid | 4 | 5 | 1.00 | 1.25 | 0.486 | 0.608 | 11-03 H vs Bayern Munich 0-2; 10-20 A vs VfB Stuttgart 1-1; 10-13 H vs Manchester United 2-0; 09-09 A vs Liverpool 1-2 |
| Champions League | Barcelona | 14 | 6 | 3.50 | 1.50 | 1.703 | 0.730 | 11-03 H vs Aston Villa 3-0; 10-20 A vs Paris Saint-Germain 2-4; 10-13 A vs Galatasaray 4-1; 09-09 H vs Feyenoord Rotterdam 5-1 |
| Champions League | Bayern Munich | 12 | 5 | 3.00 | 1.25 | 1.459 | 0.608 | 11-03 A vs Atlético Madrid 2-0; 10-21 H vs Arsenal 2-2; 10-13 A vs Viking FK 3-3; 09-10 H vs Bodo/Glimt 5-0 |
| Champions League | Borussia Dortmund | 7 | 5 | 1.75 | 1.25 | 0.851 | 0.608 | 11-04 H vs Real Betis 2-1; 10-20 A vs Sabah FK 2-1; 10-14 A vs Bodo/Glimt 0-1; 09-08 H vs Villarreal 3-2 |
| Champions League | Club Brugge | 11 | 7 | 2.75 | 1.75 | 1.338 | 0.851 | 11-04 A vs PSV Eindhoven 2-1; 10-21 H vs Lens 3-0; 10-13 A vs Internazionale 4-3; 09-08 H vs Aston Villa 2-3 |
| Champions League | Fenerbahce | 6 | 11 | 1.50 | 2.75 | 0.730 | 1.338 | 11-04 H vs Liverpool 3-2; 10-20 H vs Slavia Prague 2-2; 10-14 A vs Aston Villa 0-6; 09-10 H vs AS Roma 1-1 |
| Champions League | Galatasaray | 8 | 9 | 2.00 | 2.25 | 0.973 | 1.095 | 11-03 H vs VfB Stuttgart 2-0; 10-21 A vs Lille 4-2; 10-13 H vs Barcelona 1-4; 09-09 A vs Sporting CP 1-3 |
| Champions League | Internazionale | 8 | 6 | 2.00 | 1.50 | 0.973 | 0.730 | 11-03 A vs Feyenoord Rotterdam 3-0; 10-21 H vs Shakhtar Donetsk 1-0; 10-13 H vs Club Brugge 3-4; 09-08 A vs Real Madrid 1-2 |
| Champions League | Lille | 4 | 10 | 1.00 | 2.50 | 0.486 | 1.216 | 11-03 A vs Bodo/Glimt 0-0; 10-21 H vs Galatasaray 2-4; 10-13 A vs Arsenal 0-3; 09-08 H vs Real Betis 2-3 |
| Champions League | Liverpool | 14 | 10 | 3.50 | 2.50 | 1.703 | 1.216 | 11-04 A vs Fenerbahce 2-3; 10-20 H vs Villarreal 4-3; 10-14 A vs LASK Linz 6-3; 09-09 H vs Atlético Madrid 2-1 |
| Champions League | Manchester City | 12 | 7 | 3.00 | 1.75 | 1.459 | 0.851 | 11-04 A vs RB Leipzig 3-2; 10-20 H vs AEK Athens 5-1; 10-14 H vs Paris Saint-Germain 2-4; 09-08 A vs FC Porto 2-0 |
| Champions League | Manchester United | 8 | 8 | 2.00 | 2.00 | 0.973 | 0.973 | 11-03 H vs AS Roma 3-2; 10-21 A vs Como 1-4; 10-13 A vs Atlético Madrid 0-2; 09-10 H vs Sabah FK 4-0 |
| Champions League | Napoli | 6 | 11 | 1.50 | 2.75 | 0.730 | 1.338 | 11-04 A vs FC Porto 1-4; 10-20 H vs Bodo/Glimt 4-3; 10-13 A vs Villarreal 1-3; 09-09 H vs Arsenal 0-1 |
| Champions League | PSV Eindhoven | 3 | 4 | 0.75 | 1.00 | 0.365 | 0.486 | 11-04 H vs Club Brugge 1-2; 10-20 A vs FC Porto 1-0; 10-13 A vs RB Leipzig 0-1; 09-10 H vs Shakhtar Donetsk 1-1 |
| Champions League | Paris Saint-Germain | 20 | 5 | 5.00 | 1.25 | 2.432 | 0.608 | 11-03 A vs Villarreal 6-0; 10-20 H vs Barcelona 4-2; 10-14 A vs Manchester City 4-2; 09-09 H vs Slovan Bratislava 6-1 |
| Champions League | Real Madrid | 13 | 7 | 3.25 | 1.75 | 1.581 | 0.851 | 11-04 A vs AEK Athens 3-2; 10-21 H vs RB Leipzig 4-1; 10-14 A vs AS Roma 4-3; 09-08 H vs Internazionale 2-1 |
| Champions League | Sabah FK | 4 | 10 | 1.00 | 2.50 | 0.486 | 1.216 | 11-04 A vs Viking FK 1-4; 10-20 H vs Borussia Dortmund 1-2; 10-13 H vs Slavia Prague 2-0; 09-10 A vs Manchester United 0-4 |
| Champions League | Shakhtar Donetsk | 4 | 4 | 1.00 | 1.00 | 0.486 | 0.486 | 11-03 H vs Sporting CP 0-1; 10-21 A vs Internazionale 0-1; 10-14 H vs AEK Athens 3-1; 09-10 A vs PSV Eindhoven 1-1 |
| Champions League | Slavia Prague | 5 | 9 | 1.25 | 2.25 | 0.608 | 1.095 | 11-04 H vs Arsenal 1-2; 10-20 A vs Fenerbahce 2-2; 10-13 A vs Sabah FK 0-2; 09-10 H vs Lens 2-3 |
| Champions League | Sporting CP | 8 | 4 | 2.00 | 1.00 | 0.973 | 0.486 | 11-03 A vs Shakhtar Donetsk 1-0; 10-21 H vs LASK Linz 2-3; 10-13 A vs Lens 2-0; 09-09 H vs Galatasaray 3-1 |
| Champions League | VfB Stuttgart | 7 | 4 | 1.75 | 1.00 | 0.851 | 0.486 | 11-03 A vs Galatasaray 0-2; 10-20 H vs Atlético Madrid 1-1; 10-14 A vs Slovan Bratislava 3-0; 09-09 H vs Viking FK 3-1 |
| Champions League | Viking FK | 9 | 10 | 2.25 | 2.50 | 1.095 | 1.216 | 11-04 H vs Sabah FK 4-1; 10-21 A vs Aston Villa 1-3; 10-13 H vs Bayern Munich 3-3; 09-09 A vs VfB Stuttgart 1-3 |
| Champions League | Villarreal | 8 | 14 | 2.00 | 3.50 | 0.973 | 1.703 | 11-03 H vs Paris Saint-Germain 0-6; 10-20 A vs Liverpool 3-4; 10-13 H vs Napoli 3-1; 09-08 A vs Borussia Dortmund 2-3 |
| Europa League | AC Milan | 4 | 7 | 1.00 | 1.75 | 0.673 | 1.178 | 11-05 H vs Ferencvaros 0-2; 10-22 A vs AFC Bournemouth 0-3; 10-15 A vs RB Salzburg 4-0; 09-16 H vs Benfica 0-2 |
| Europa League | AFC Bournemouth | 11 | 2 | 2.75 | 0.50 | 1.850 | 0.336 | 11-05 A vs Sparta Prague 3-1; 10-22 H vs AC Milan 3-0; 10-15 H vs SK Sturm Graz 3-0; 09-17 A vs Real Sociedad 2-1 |
| Europa League | AZ Alkmaar | 7 | 4 | 1.75 | 1.00 | 1.178 | 0.673 | 11-05 H vs Juventus 1-2; 10-22 A vs Ararat-Armenia 4-0; 10-15 H vs Hapoel Be'er 2-1; 09-16 A vs Sunderland 0-1 |
| Europa League | Anderlecht | 6 | 3 | 1.50 | 0.75 | 1.009 | 0.505 | 11-05 H vs RB Salzburg 2-0; 10-22 A vs Jagiellonia Bialystok 3-0; 10-15 A vs Dinamo Zagreb 0-1; 09-16 H vs Lyon 1-2 |
| Europa League | Ararat-Armenia | 4 | 14 | 1.00 | 3.50 | 0.673 | 2.355 | 11-05 A vs Torreense 2-3; 10-22 H vs AZ Alkmaar 0-4; 10-15 A vs Jagiellonia Bialystok 1-3; 09-16 H vs Sparta Prague 1-4 |
| Europa League | Bayer Leverkusen | 8 | 1 | 2.00 | 0.25 | 1.346 | 0.168 | 11-05 H vs Marseille 0-1; 10-22 A vs OFI Crete 2-0; 10-15 A vs Lech Poznan 4-0; 09-16 H vs NK Celje 2-0 |
| Europa League | Benfica | 13 | 3 | 3.25 | 0.75 | 2.187 | 0.505 | 11-05 H vs Lech Poznan 3-1; 10-22 A vs Omonia Nicosia 4-1; 10-15 H vs Celtic 4-1; 09-16 A vs AC Milan 2-0 |
| Europa League | Besiktas | 11 | 8 | 2.75 | 2.00 | 1.850 | 1.346 | 11-05 A vs Celtic 2-3; 10-22 H vs Crystal Palace 2-2; 10-15 A vs TSG Hoffenheim 3-2; 09-17 H vs Marseille 4-1 |
| Europa League | Celta Vigo | 4 | 6 | 1.00 | 1.50 | 0.673 | 1.009 | 11-05 H vs Union St.-Gilloise 1-2; 10-22 A vs Celtic 2-1; 10-15 H vs Juventus 1-2; 09-16 A vs Omonia Nicosia 0-1 |
| Europa League | Celtic | 6 | 11 | 1.50 | 2.75 | 1.009 | 1.850 | 11-05 H vs Besiktas 3-2; 10-22 H vs Celta Vigo 1-2; 10-15 A vs Benfica 1-4; 09-17 H vs Ferencvaros 1-3 |
| Europa League | Crystal Palace | 9 | 6 | 2.25 | 1.50 | 1.514 | 1.009 | 11-05 H vs TSG Hoffenheim 1-1; 10-22 A vs Besiktas 2-2; 10-15 A vs Lyon 2-3; 09-17 H vs Lech Poznan 4-0 |
| Europa League | Dinamo Zagreb | 5 | 4 | 1.25 | 1.00 | 0.841 | 0.673 | 11-05 A vs Sunderland 2-0; 10-22 H vs NEC Nijmegen 2-4; 10-15 H vs Anderlecht 1-0; 09-16 A vs Hapoel Be'er 0-0 |
| Europa League | Ferencvaros | 11 | 3 | 2.75 | 0.75 | 1.850 | 0.505 | 11-05 A vs AC Milan 2-0; 10-22 H vs Torreense 4-1; 10-15 H vs Viktoria Plzen 2-1; 09-17 A vs Celtic 3-1 |
| Europa League | Hapoel Be'er | 1 | 8 | 0.25 | 2.00 | 0.168 | 1.346 | 11-05 H vs OFI Crete 0-2; 10-22 A vs Union St.-Gilloise 0-4; 10-15 A vs AZ Alkmaar 1-2; 09-16 H vs Dinamo Zagreb 0-0 |
| Europa League | Jagiellonia Bialystok | 4 | 7 | 1.00 | 1.75 | 0.673 | 1.178 | 11-05 A vs Levski Sofia 0-1; 10-22 H vs Anderlecht 0-3; 10-15 H vs Ararat-Armenia 3-1; 09-16 A vs Olympiacos 1-2 |
| Europa League | Juventus | 11 | 4 | 2.75 | 1.00 | 1.850 | 0.673 | 11-05 A vs AZ Alkmaar 2-1; 10-22 H vs Stade Rennais 2-2; 10-15 A vs Celta Vigo 2-1; 09-17 H vs NEC Nijmegen 5-0 |
| Europa League | Lech Poznan | 2 | 12 | 0.50 | 3.00 | 0.336 | 2.019 | 11-05 A vs Benfica 1-3; 10-22 H vs Sunderland 1-1; 10-15 H vs Bayer Leverkusen 0-4; 09-17 A vs Crystal Palace 0-4 |
| Europa League | Levski Sofia | 4 | 3 | 1.00 | 0.75 | 0.673 | 0.505 | 11-05 H vs Jagiellonia Bialystok 1-0; 10-22 A vs Viktoria Plzen 2-1; 10-15 A vs NEC Nijmegen 1-1; 09-17 H vs RB Salzburg 0-1 |
| Europa League | Lillestrom | 2 | 10 | 0.50 | 2.50 | 0.336 | 1.682 | 11-05 H vs Viktoria Plzen 0-1; 10-22 H vs Real Sociedad 0-6; 10-15 A vs Sparta Prague 1-1; 09-17 H vs Torreense 1-2 |
| Europa League | Lyon | 6 | 7 | 1.50 | 1.75 | 1.009 | 1.178 | 11-05 A vs Real Sociedad 1-1; 10-22 A vs TSG Hoffenheim 0-3; 10-15 H vs Crystal Palace 3-2; 09-16 A vs Anderlecht 2-1 |
| Europa League | Marseille | 2 | 6 | 0.50 | 1.50 | 0.336 | 1.009 | 11-05 A vs Bayer Leverkusen 1-0; 10-22 A vs SK Sturm Graz 0-1; 10-15 H vs Olympiacos 0-1; 09-17 A vs Besiktas 1-4 |
| Europa League | NEC Nijmegen | 8 | 9 | 2.00 | 2.25 | 1.346 | 1.514 | 11-05 H vs Omonia Nicosia 3-1; 10-22 A vs Dinamo Zagreb 4-2; 10-15 H vs Levski Sofia 1-1; 09-17 A vs Juventus 0-5 |
| Europa League | NK Celje | 5 | 9 | 1.25 | 2.25 | 0.841 | 1.514 | 11-05 A vs SK Sturm Graz 3-2; 10-22 H vs RB Salzburg 2-2; 10-15 H vs Omonia Nicosia 0-3; 09-16 A vs Bayer Leverkusen 0-2 |
| Europa League | OFI Crete | 5 | 4 | 1.25 | 1.00 | 0.841 | 0.673 | 11-05 A vs Hapoel Be'er 2-0; 10-22 H vs Bayer Leverkusen 0-2; 10-15 A vs Stade Rennais 1-2; 09-17 H vs TSG Hoffenheim 2-0 |
| Europa League | Olympiacos | 4 | 1 | 1.00 | 0.25 | 0.673 | 0.168 | 11-04 A vs Stade Rennais 0-0; 10-22 H vs Sparta Prague 1-0; 10-15 A vs Marseille 1-0; 09-16 H vs Jagiellonia Bialystok 2-1 |
| Europa League | Omonia Nicosia | 6 | 7 | 1.50 | 1.75 | 1.009 | 1.178 | 11-05 A vs NEC Nijmegen 1-3; 10-22 H vs Benfica 1-4; 10-15 A vs NK Celje 3-0; 09-16 H vs Celta Vigo 1-0 |
| Europa League | RB Salzburg | 3 | 8 | 0.75 | 2.00 | 0.505 | 1.346 | 11-05 A vs Anderlecht 0-2; 10-22 A vs NK Celje 2-2; 10-15 H vs AC Milan 0-4; 09-17 A vs Levski Sofia 1-0 |
| Europa League | Real Sociedad | 9 | 4 | 2.25 | 1.00 | 1.514 | 0.673 | 11-05 H vs Lyon 1-1; 10-22 A vs Lillestrom 6-0; 10-15 A vs Union St.-Gilloise 1-1; 09-17 H vs AFC Bournemouth 1-2 |
| Europa League | SK Sturm Graz | 3 | 6 | 0.75 | 1.50 | 0.505 | 1.009 | 11-05 H vs NK Celje 2-3; 10-22 H vs Marseille 1-0; 10-15 A vs AFC Bournemouth 0-3; 09-16 H vs Stade Rennais 0-0 |
| Europa League | Sparta Prague | 6 | 6 | 1.50 | 1.50 | 1.009 | 1.009 | 11-05 H vs AFC Bournemouth 1-3; 10-22 A vs Olympiacos 0-1; 10-15 H vs Lillestrom 1-1; 09-16 A vs Ararat-Armenia 4-1 |
| Europa League | Stade Rennais | 4 | 3 | 1.00 | 0.75 | 0.673 | 0.505 | 11-04 H vs Olympiacos 0-0; 10-22 A vs Juventus 2-2; 10-15 H vs OFI Crete 2-1; 09-16 A vs SK Sturm Graz 0-0 |
| Europa League | Sunderland | 4 | 4 | 1.00 | 1.00 | 0.673 | 0.673 | 11-05 H vs Dinamo Zagreb 0-2; 10-22 A vs Lech Poznan 1-1; 10-15 A vs Torreense 2-1; 09-16 H vs AZ Alkmaar 1-0 |
| Europa League | TSG Hoffenheim | 6 | 6 | 1.50 | 1.50 | 1.009 | 1.009 | 11-05 A vs Crystal Palace 1-1; 10-22 H vs Lyon 3-0; 10-15 H vs Besiktas 2-3; 09-17 A vs OFI Crete 0-2 |
| Europa League | Torreense | 7 | 9 | 1.75 | 2.25 | 1.178 | 1.514 | 11-05 H vs Ararat-Armenia 3-2; 10-22 A vs Ferencvaros 1-4; 10-15 H vs Sunderland 1-2; 09-17 A vs Lillestrom 2-1 |
| Europa League | Union St.-Gilloise | 10 | 2 | 2.50 | 0.50 | 1.682 | 0.336 | 11-05 A vs Celta Vigo 2-1; 10-22 H vs Hapoel Be'er 4-0; 10-15 H vs Real Sociedad 1-1; 09-17 A vs Viktoria Plzen 3-0 |
| Europa League | Viktoria Plzen | 3 | 7 | 0.75 | 1.75 | 0.505 | 1.178 | 11-05 A vs Lillestrom 1-0; 10-22 H vs Levski Sofia 1-2; 10-15 A vs Ferencvaros 1-2; 09-17 H vs Union St.-Gilloise 0-3 |

## (c) Promedios de liga usados y cómo se calcularon

Los promedios se calcularon desde los scoreboards de las últimas ~3 jornadas completadas antes del cutoff (partidos con STATUS_FULL_TIME). El endpoint de posiciones (standings) de ESPN devuelve 404, por eso se usan scoreboards.

| Liga | Jornadas usadas (fechas) | Partidos | Goles local | Goles visitante | Prom. goles/partido | Prom. local | Prom. visitante | Prom. por equipo |
|---|---|---|---|---|---|---|---|---|
| Liga MX | 20261030, 20261031, 20261101, 20261106, 20261107, 20261108, 20261114, 20261120, 20261121 | 26 | 39 | 36 | 2.885 | 1.500 | 1.385 | 1.442 |
| Champions League | 20261013, 20261014, 20261020, 20261021, 20261103, 20261104 | 54 | 121 | 101 | 4.111 | 2.241 | 1.870 | 2.056 |
| Europa League | 20260916, 20260917, 20261015, 20261022, 20261104, 20261105 | 72 | 103 | 111 | 2.972 | 1.431 | 1.542 | 1.486 |

**Fórmulas aplicadas:**

- Prom. por equipo = prom. goles/partido / 2 (cada partido reparte sus goles entre dos equipos).
- Ataque = (GF/4) / prom. por equipo; defensa = (GA/4) / prom. por equipo.
- xG local = prom. local de la liga × ataque local × defensa visitante; xG visitante = prom. visitante de la liga × ataque visitante × defensa local.
- Poisson: P(k;λ) = e^-λ × λ^k / k!, k = 0..20 por equipo (distribución completa; la cola fuera de la rejilla es < 1e-6). P(1), P(X) y P(2) suman 100% sin renormalizar; el BTTS y el +2.5 también se calculan con la distribución completa.

## (d) Fuentes ESPN consultadas (API pública, sin clave)

- Scoreboard por liga y día, 2026-11-24 al 2026-11-26: `site.api.espn.com/apis/site/v2/sports/soccer/{{liga}}/scoreboard?dates={{AAAAMMDD}}` — los {n_partidos} partidos aparecen como STATUS_SCHEDULED con la fecha y hora exactas de la configuración (horas convertidas de UTC a CST, UTC-6).
- Schedule por equipo (últimos partidos completados): `site.api.espn.com/apis/site/v2/sports/soccer/{liga}/teams/{id}/schedule` — 70 equipos, 4 partidos completados cada uno, todos de liga, hasta el cutoff.
- Scoreboards de jornadas pasadas para promedios de liga: 9 fechas por liga (ver tabla c).
- Los archivos JSON crudos de todas estas consultas están en `raw/` dentro de esta misma carpeta.

## (e) Datos no verificados y partidos excluidos

- **Ningún partido quedó fuera:** los 35 partidos de la lista se verificaron en el scoreboard de ESPN con fecha, hora y equipos exactos antes de calcular.
- **Valores extremos por muestra corta (4 partidos, sin tope aplicado):** son correctos según los datos, pero una muestra de 4 partidos exagera rachas; conviene leer los favoritos más extremos con cautela.
- **Últimos 4 = solo liga:** el schedule de ESPN por liga devuelve partidos de esa liga; no se mezclaron otras competiciones.
- **Sin momios ni cuotas en esta tabla:** solo probabilidades propias (Poisson). Los momios y el EV están en la tabla de momios de la misma semana.
