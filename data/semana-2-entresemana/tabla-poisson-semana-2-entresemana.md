# Tabla de probabilidades Poisson — Semana 2 entre semana (Football AI Agenda)

**Partidos:** 2026-11-24 al 2026-11-29, horas de Monterrey (CST). **Fuente de datos:** ESPN, API pública sin clave.
**Método:** modelo Poisson con goles esperados (xG) por equipo, distribución completa (0–20 goles), P(1)/P(X)/P(2) suman 100%.
**Fecha de cálculo:** 2026-11-22. Últimos 4 partidos por equipo: partidos de liga completados hasta el 2026-11-22.

## (a) Tabla de los 20 partidos

| Fecha | Hora (CST) | Liga | Local | Visitante | xG local | xG visit. | P(1) | P(X) | P(2) | P(+2.5) | P(ambos anotan) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Mar 24 nov | 11:45 | Champions League | Galatasaray | Aston Villa | 1.59 | 2.99 | 18.1% | 15.9% | 66.0% | 83.5% | 75.6% |
| Mar 24 nov | 14:00 | Champions League | Arsenal | Borussia Dortmund | 1.33 | 0.58 | 55.0% | 28.7% | 16.3% | 29.8% | 32.4% |
| Mar 24 nov | 14:00 | Champions League | Manchester City | Napoli | 4.38 | 1.16 | 88.4% | 6.9% | 4.7% | 91.4% | 67.8% |
| Mar 24 nov | 14:00 | Champions League | Real Madrid | PSV Eindhoven | 1.72 | 0.58 | 65.2% | 22.8% | 12.0% | 40.5% | 36.2% |
| Mié 25 nov | 14:00 | Champions League | Club Brugge | Liverpool | 3.65 | 2.71 | 56.6% | 15.2% | 28.2% | 95.2% | 90.9% |
| Mié 25 nov | 14:00 | Champions League | Internazionale | VfB Stuttgart | 1.06 | 1.16 | 33.0% | 28.9% | 38.1% | 38.3% | 44.9% |
| Mié 25 nov | 14:00 | Champions League | Lille | Bayern Munich | 0.66 | 3.32 | 4.2% | 8.9% | 87.0% | 75.9% | 46.7% |
| Mié 25 nov | 14:00 | Champions League | Paris Saint-Germain | AS Roma | 5.30 | 1.38 | 91.6% | 4.9% | 3.5% | 96.3% | 74.6% |
| Mié 25 nov | 14:00 | Champions League | Sporting CP | Manchester United | 2.12 | 0.89 | 65.8% | 19.6% | 14.6% | 57.8% | 51.7% |
| Mié 25 nov | 19:00 | Liga MX | Toluca | Atlas | 3.89 | 2.05 | 70.9% | 12.8% | 16.3% | 93.5% | 85.4% |
| Mié 25 nov | 21:10 | Liga MX | Monterrey | América | 1.38 | 1.28 | 39.5% | 26.0% | 34.5% | 49.7% | 54.1% |
| Jue 26 nov | 11:45 | Europa League | Celta Vigo | AFC Bournemouth | 0.32 | 2.88 | 2.4% | 8.8% | 88.8% | 62.1% | 26.1% |
| Jue 26 nov | 11:45 | Europa League | Dinamo Zagreb | Bayer Leverkusen | 0.20 | 1.40 | 5.2% | 26.4% | 68.5% | 21.6% | 13.8% |
| Jue 26 nov | 11:45 | Europa League | Olympiacos | AC Milan | 1.13 | 0.17 | 61.7% | 32.7% | 5.7% | 14.5% | 10.9% |
| Jue 26 nov | 19:00 | Liga MX | Pachuca | Guadalajara | 1.04 | 0.85 | 39.1% | 31.7% | 29.2% | 29.4% | 37.0% |
| Jue 26 nov | 21:10 | Liga MX | León | Cruz Azul | 1.21 | 1.33 | 33.8% | 26.7% | 39.5% | 46.7% | 51.7% |
| Sáb 28 nov | 19:00 | Liga MX | Atlas | Toluca | 2.22 | 3.59 | 21.5% | 14.6% | 63.9% | 92.9% | 86.7% |
| Sáb 28 nov | 21:10 | Liga MX | América | Monterrey | 1.38 | 1.28 | 39.5% | 26.0% | 34.5% | 49.7% | 54.1% |
| Dom 29 nov | 19:07 | Liga MX | Guadalajara | Pachuca | 0.92 | 0.96 | 33.0% | 32.0% | 34.9% | 29.1% | 37.2% |
| Dom 29 nov | 21:00 | Liga MX | Cruz Azul | León | 1.44 | 1.12 | 44.5% | 26.2% | 29.3% | 47.2% | 51.4% |

Promedios de la tabla: xG local 1.85, xG visitante 1.58; P(1) media 43.4%, P(X) media 20.8%, P(2) media 35.8%.

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
| Champions League | Bayern Munich | 12 | 5 | 3.00 | 1.25 | 1.459 | 0.608 | 11-03 A vs Atlético Madrid 2-0; 10-21 H vs Arsenal 2-2; 10-13 A vs Viking FK 3-3; 09-10 H vs Bodo/Glimt 5-0 |
| Champions League | Borussia Dortmund | 7 | 5 | 1.75 | 1.25 | 0.851 | 0.608 | 11-04 H vs Real Betis 2-1; 10-20 A vs Sabah FK 2-1; 10-14 A vs Bodo/Glimt 0-1; 09-08 H vs Villarreal 3-2 |
| Champions League | Club Brugge | 11 | 7 | 2.75 | 1.75 | 1.338 | 0.851 | 11-04 A vs PSV Eindhoven 2-1; 10-21 H vs Lens 3-0; 10-13 A vs Internazionale 4-3; 09-08 H vs Aston Villa 2-3 |
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
| Champions League | Sporting CP | 8 | 4 | 2.00 | 1.00 | 0.973 | 0.486 | 11-03 A vs Shakhtar Donetsk 1-0; 10-21 H vs LASK Linz 2-3; 10-13 A vs Lens 2-0; 09-09 H vs Galatasaray 3-1 |
| Champions League | VfB Stuttgart | 7 | 4 | 1.75 | 1.00 | 0.851 | 0.486 | 11-03 A vs Galatasaray 0-2; 10-20 H vs Atlético Madrid 1-1; 10-14 A vs Slovan Bratislava 3-0; 09-09 H vs Viking FK 3-1 |
| Europa League | AC Milan | 4 | 7 | 1.00 | 1.75 | 0.673 | 1.178 | 11-05 H vs Ferencvaros 0-2; 10-22 A vs AFC Bournemouth 0-3; 10-15 A vs RB Salzburg 4-0; 09-16 H vs Benfica 0-2 |
| Europa League | AFC Bournemouth | 11 | 2 | 2.75 | 0.50 | 1.850 | 0.336 | 11-05 A vs Sparta Prague 3-1; 10-22 H vs AC Milan 3-0; 10-15 H vs SK Sturm Graz 3-0; 09-17 A vs Real Sociedad 2-1 |
| Europa League | Bayer Leverkusen | 8 | 1 | 2.00 | 0.25 | 1.346 | 0.168 | 11-05 H vs Marseille 0-1; 10-22 A vs OFI Crete 2-0; 10-15 A vs Lech Poznan 4-0; 09-16 H vs NK Celje 2-0 |
| Europa League | Celta Vigo | 4 | 6 | 1.00 | 1.50 | 0.673 | 1.009 | 11-05 H vs Union St.-Gilloise 1-2; 10-22 A vs Celtic 2-1; 10-15 H vs Juventus 1-2; 09-16 A vs Omonia Nicosia 0-1 |
| Europa League | Dinamo Zagreb | 5 | 4 | 1.25 | 1.00 | 0.841 | 0.673 | 11-05 A vs Sunderland 2-0; 10-22 H vs NEC Nijmegen 2-4; 10-15 H vs Anderlecht 1-0; 09-16 A vs Hapoel Be'er 0-0 |
| Europa League | Olympiacos | 4 | 1 | 1.00 | 0.25 | 0.673 | 0.168 | 11-04 A vs Stade Rennais 0-0; 10-22 H vs Sparta Prague 1-0; 10-15 A vs Marseille 1-0; 09-16 H vs Jagiellonia Bialystok 2-1 |

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

- Scoreboard por liga y día, 2026-11-24 al 2026-11-29: `site.api.espn.com/apis/site/v2/sports/soccer/{{liga}}/scoreboard?dates={{AAAAMMDD}}` — los {n_partidos} partidos aparecen como STATUS_SCHEDULED con la fecha y hora exactas de la configuración (horas convertidas de UTC a CST, UTC-6).
- Schedule por equipo (últimos partidos completados): `site.api.espn.com/apis/site/v2/sports/soccer/{liga}/teams/{id}/schedule` — 32 equipos, 4 partidos completados cada uno, todos de liga, hasta el cutoff.
- Scoreboards de jornadas pasadas para promedios de liga: 9 fechas por liga (ver tabla c).
- Los archivos JSON crudos de todas estas consultas están en `raw/` dentro de esta misma carpeta.

## (e) Datos no verificados y partidos excluidos

- **Ningún partido quedó fuera:** los 20 partidos de la lista se verificaron en el scoreboard de ESPN con fecha, hora y equipos exactos antes de calcular.
- **Valores extremos por muestra corta (4 partidos, sin tope aplicado):** son correctos según los datos, pero una muestra de 4 partidos exagera rachas; conviene leer los favoritos más extremos con cautela.
- **Últimos 4 = solo liga:** el schedule de ESPN por liga devuelve partidos de esa liga; no se mezclaron otras competiciones.
- **Sin momios ni cuotas en esta tabla:** solo probabilidades propias (Poisson). Los momios y el EV están en la tabla de momios de la misma semana.
