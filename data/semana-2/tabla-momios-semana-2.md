# Tabla de momios y valor esperado — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-27 al 2026-11-29, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-28.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS: probabilidad Poisson completa (ambos anotan); el EV se calcula solo con momio BSD (llave 'bsd' en momios.json); sin esa llave no lleva EV porque ESPN/DraftKings no trae momio de BTTS en esta fuente.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | P(BTTS) | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 11/27 nov | Werder Bremen vs Borussia Mönchengladbach | 1.69 / 4.00 / 4.20 | +21.9% / -34.6% / -51.8% | 3.5 (2.35 / 1.59) | +3.0% / -10.8% | -0.5 (1.67 / 2.10) | +20.3% / -41.5% | 54.2% | Local | +21.9% | 🟢 Verde |
| 11/27 nov | Venezia vs Bologna | 2.95 / 3.05 / 2.40 | -59.1% / -12.2% / +37.6% | 2.5 (2.20 / 1.65) | -39.9% / +19.6% | +0.5 (1.54 / 2.30) | -34.3% / +31.9% | 28.6% | Visita | +37.6% | 🟢 Verde |
| 11/27 nov | Nottingham Forest vs Chelsea | 2.45 / 3.45 / 2.85 | -69.0% / -33.8% / +94.2% | 2.5 (1.77 / 2.05) | -2.0% / -8.6% | -0.5 (2.25 / 1.56) | -71.5% / +35.9% | 47.8% | Visita | +94.2% | 🟢 Verde |
| 11/27 nov | Levante vs Racing Santander | 2.00 / 3.90 / 3.50 | +7.3% / -8.6% / -19.8% | 3.5 (2.30 / 1.62) | -27.3% / +11.1% | -0.5 (1.91 / 1.80) | +2.5% / -16.6% | 54.5% | Menos 3.5 | +11.1% | 🟢 Verde |
| 11/28 nov | Hamburg SV vs Bayern Munich (Bet 365) | 8.00 / 5.75 / 1.30 | +139.5% / +16.2% / -35.2% | — | — | — | — | 73.4% | Local | +139.5% | 🟢 Verde |
| 11/28 nov | Manchester United vs Brentford | 2.35 / 3.70 / 2.85 | -22.0% / -19.5% / +28.4% | 3.5 (2.35 / 1.59) | +13.2% / -17.7% | -0.5 (2.20 / 1.59) | -27.0% / +6.1% | 69.1% | Visita | +28.4% | 🟢 Verde |
| 11/28 nov | Elche vs Atlético Madrid | 6.00 / 4.60 / 1.50 | +5.9% / +113.4% / -46.1% | 2.5 (1.65 / 2.25) | -87.5% / +107.9% | +1.5 (1.56 / 2.30) | +40.3% / -77.5% | 13.8% | Empate | +113.4% | 🟢 Verde |
| 11/28 nov | VfB Stuttgart vs Eintracht Frankfurt | 1.77 / 4.40 / 3.55 | +39.7% / -41.5% / -72.6% | 3.5 (1.71 / 2.10) | -19.3% / +11.2% | -0.5 (1.74 / 2.00) | +37.5% / -57.9% | 50.2% | Local | +39.7% | 🟢 Verde |
| 11/28 nov | Internazionale vs Genoa | 1.27 / 5.50 / 9.00 | -40.6% / +68.8% / +103.1% | 3.5 (2.20 / 1.67) | -72.6% / +45.9% | -1.5 (1.74 / 1.95) | -64.4% / +55.3% | 35.5% | Visita | +103.1% | 🟢 Verde |
| 11/28 nov | Real Madrid vs Alavés | 1.14 / 9.00 / 17.00 | +13.2% / -92.6% / -97.6% | 3.5 (1.80 / 2.00) | +50.3% / -67.0% | -2.5 (2.10 / 1.67) | +87.2% / -81.9% | 21.1% | Spread local -2.5 | +87.2% | 🟢 Verde |
| 11/29 nov | Everton vs Liverpool | 4.60 / 3.85 / 1.74 | +69.4% / -3.7% / -33.6% | 2.5 (1.67 / 2.25) | -9.6% / +2.9% | +0.5 (2.05 / 1.69) | +26.8% / -35.5% | 57.7% | Local | +69.4% | 🟢 Verde |
| 11/29 nov | Sassuolo vs Napoli | 4.40 / 4.20 / 1.62 | -68.0% / -57.9% / +34.4% | 2.5 (1.57 / 2.35) | +34.4% / -66.0% | +0.5 (2.15 / 1.61) | -62.8% / +32.8% | 65.9% | Más 2.5 | +34.4% | 🟢 Verde |
| 11/29 nov | Deportivo vs Barcelona | 10.00 / 7.50 / 1.22 | +15.6% / +4.1% / -8.9% | 3.5 (1.65 / 2.25) | -0.3% / -11.4% | +2.5 (1.57 / 2.25) | +0.7% / -19.1% | 65.8% | Local | +15.6% | 🟢 Verde |
| 11/29 nov | Arsenal vs Manchester City | 2.05 / 3.65 / 3.55 | +70.3% / -49.0% / -89.5% | 2.5 (1.77 / 2.05) | -22.5% / +15.2% | -0.5 (1.95 / 1.77) | +62.2% / -70.0% | 18.6% | Local | +70.3% | 🟢 Verde |
| 11/29 nov | Borussia Dortmund vs Bayer Leverkusen | 2.05 / 3.80 / 3.00 | +43.4% / -37.3% / -59.4% | 3.5 (2.15 / 1.69) | +6.4% / -14.6% | -0.5 (2.00 / 1.71) | +39.9% / -48.5% | 60.6% | Local | +43.4% | 🟢 Verde |
| 11/29 nov | Como vs Juventus | 1.95 / 3.45 / 3.65 | +16.0% / -9.5% / -47.7% | 2.5 (1.80 / 1.95) | -39.0% / +29.0% | -0.5 (1.91 / 1.80) | +13.5% / -27.0% | 33.8% | Menos 2.5 | +29.0% | 🟢 Verde |
| 11/28 nov | Atlas vs Toluca | 2.90 / 3.80 / 2.25 | -45.6% / -36.5% / +45.2% | 3.5 (2.15 / 1.65) | +34.7% / -38.5% | +0.5 (1.62 / 2.15) | -42.3% / +38.7% | 73.3% | Visita | +45.2% | 🟢 Verde |
| 11/28 nov | América vs Monterrey | 2.10 / 3.20 / 3.70 | +16.9% / -39.7% / -5.6% | 2.5 (1.77 / 1.95) | +39.3% / -58.5% | -0.5 (2.05 / 1.69) | +14.1% / -25.1% | 74.7% | Más 2.5 | +39.3% | 🟢 Verde |
| 11/29 nov | Guadalajara vs Pachuca | 1.62 / 3.95 / 4.90 | -34.7% / +13.2% / +52.5% | 2.5 (1.62 / 2.15) | -37.0% / +31.6% | -0.5 (1.59 / 2.15) | -36.1% / +28.5% | 45.1% | Visita | +52.5% | 🟢 Verde |
| 11/29 nov | Cruz Azul vs León | pendiente | — | — | — | — | — | 58.7% | — | — | ⏳ Pendiente |
| 11/28 nov | Leeds United vs Coventry City | 1.47 / 4.60 / 6.50 | -56.3% / +26.5% / +177.4% | 2.5 (1.65 / 2.25) | -30.1% / +29.3% | -1.5 (2.20 / 1.61) | -74.9% / +42.3% | 47.9% | Visita | +177.4% | 🟢 Verde |
| 11/28 nov | Ipswich Town vs Aston Villa | 3.40 / 3.75 / 2.05 | +31.4% / -32.4% / -11.2% | 2.5 (1.59 / 2.40) | +41.0% / -73.0% | +0.5 (1.74 / 1.95) | -1.4% / -15.4% | 85.3% | Más 2.5 | +41.0% | 🟢 Verde |
| 11/28 nov | Real Betis vs Rayo Vallecano | 1.62 / 4.20 / 5.25 | +9.7% / -28.6% / -18.6% | 2.5 (1.59 / 2.35) | +15.6% / -36.0% | -0.5 (1.57 / 2.25) | +6.1% / -26.9% | 64.3% | Más 2.5 | +15.6% | 🟢 Verde |
| 11/28 nov | Málaga vs Athletic Club | 4.70 / 3.85 / 1.74 | -29.3% / -35.5% / +18.7% | 2.5 (1.80 / 2.00) | +31.4% / -46.0% | +0.5 (2.10 / 1.67) | -33.2% / +13.7% | 64.1% | Más 2.5 | +31.4% | 🟢 Verde |
| 11/28 nov | FC Cologne vs SV Elversberg | 2.00 / 3.60 / 3.30 | -8.4% / -0.7% / -12.2% | 2.5 (1.62 / 2.30) | -33.9% / +36.4% | -0.5 (1.95 / 1.77) | -10.6% / -4.1% | 45.7% | Menos 2.5 | +36.4% | 🟢 Verde |
| 11/28 nov | Mainz vs 1. FC Union Berlin | 1.45 / 4.50 / 5.75 | -45.0% / +46.6% / +70.1% | 3.5 (2.25 / 1.62) | -75.0% / +44.4% | -1.5 (2.15 / 1.62) | -69.2% / +39.2% | 35.3% | Visita | +70.1% | 🟢 Verde |
| 11/28 nov | SC Paderborn 07 vs Schalke 04 | 2.60 / 3.35 / 2.50 | +48.3% / +14.6% / -78.1% | 2.5 (1.65 / 2.25) | -75.3% / +91.2% | +0.5 (1.50 / 2.40) | +36.9% / -79.0% | 14.9% | Menos 2.5 | +91.2% | 🟢 Verde |
| 11/28 nov | Frosinone vs Parma | 1.40 / 5.00 / 6.00 | -1.4% / -15.7% / -23.7% | 3.5 (1.87 / 1.91) | -16.2% / +5.3% | -1.5 (1.95 / 1.74) | -5.6% / -10.1% | 56.5% | Menos 3.5 | +5.3% | 🟢 Verde |
| 11/28 nov | Torino vs Lazio | 3.35 / 3.25 / 2.10 | -64.2% / -51.2% / +56.0% | 2.5 (1.87 / 1.91) | +31.3% / -43.2% | +0.5 (1.69 / 2.05) | -56.6% / +52.3% | 56.8% | Visita | +56.0% | 🟢 Verde |
| 11/29 nov | Brighton & Hove Albion vs Newcastle United | 1.56 / 4.50 / 5.50 | +38.8% / -59.8% / -90.0% | 3.5 (2.35 / 1.61) | -18.3% / +4.7% | -1.5 (2.40 / 1.50) | +68.7% / -55.4% | 19.6% | Spread local -1.5 | +68.7% | 🟢 Verde |
| 11/29 nov | Crystal Palace vs Hull City | 1.91 / 3.75 / 3.85 | -58.9% / -16.9% / +116.8% | 2.5 (1.77 / 2.05) | +2.3% / -13.6% | -0.5 (1.87 / 1.83) | -59.8% / +43.9% | 56.8% | Visita | +116.8% | 🟢 Verde |
| 11/29 nov | Fulham vs AFC Bournemouth | 2.80 / 3.50 / 2.50 | +0.8% / -2.0% / -10.0% | 2.5 (1.80 / 2.00) | -24.9% / +16.5% | +0.5 (1.54 / 2.35) | -1.4% / -15.4% | 47.8% | Menos 2.5 | +16.5% | 🟢 Verde |
| 11/29 nov | Sunderland vs Tottenham Hotspur | 4.00 / 3.45 / 1.95 | -80.6% / -25.0% / +43.3% | 2.5 (1.95 / 1.83) | -43.2% / +30.0% | +0.5 (1.83 / 1.87) | -51.3% / +37.3% | 16.9% | Visita | +43.3% | 🟢 Verde |
| 11/29 nov | Valencia vs Osasuna | 2.15 / 3.20 / 3.60 | -3.6% / -20.6% / +9.3% | 2.5 (2.25 / 1.62) | +20.3% / -24.4% | -0.5 (2.05 / 1.69) | -8.1% / -6.8% | 56.5% | Más 2.5 | +20.3% | 🟢 Verde |
| 11/29 nov | Celta Vigo vs Villarreal | 2.75 / 3.55 / 2.50 | -62.2% / +94.4% / -21.3% | 2.5 (1.77 / 2.05) | -93.7% / +97.7% | +0.5 (1.53 / 2.35) | +4.6% / -26.0% | 7.9% | Menos 2.5 | +97.7% | 🟢 Verde |
| 11/29 nov | Real Sociedad vs Sevilla | 2.15 / 3.70 / 3.20 | +87.6% / -73.8% / -81.9% | 2.5 (1.80 / 2.05) | +70.1% / -88.7% | -0.5 (2.05 / 1.69) | +78.9% / -78.5% | 76.0% | Local | +87.6% | 🟢 Verde |
| 11/29 nov | SC Freiburg vs RB Leipzig | 2.65 / 3.70 / 2.30 | -25.3% / -32.8% / +23.4% | 3.5 (2.15 / 1.67) | +46.8% / -47.1% | +0.5 (1.59 / 2.20) | -26.4% / +18.1% | 80.1% | Más 3.5 | +46.8% | 🟢 Verde |
| 11/29 nov | TSG Hoffenheim vs FC Augsburg | 1.67 / 4.50 / 3.90 | +36.1% / -54.9% / -67.6% | 3.5 (1.77 / 2.00) | +35.1% / -52.8% | -0.5 (1.65 / 2.15) | +34.4% / -60.6% | 72.4% | Local | +36.1% | 🟢 Verde |
| 11/29 nov | Udinese vs Fiorentina | 3.00 / 3.40 / 2.20 | -78.3% / -57.5% / +76.6% | 2.5 (1.69 / 2.10) | +19.5% / -38.5% | +0.5 (1.65 / 2.15) | -67.5% / +72.6% | 51.0% | Visita | +76.6% | 🟢 Verde |
| 11/29 nov | AS Roma vs Monza | 1.18 / 7.00 / 11.00 | -2.0% / -34.0% / -15.7% | 3.5 (1.80 / 1.95) | +40.4% / -57.0% | -2.5 (2.20 / 1.59) | +12.6% / -22.5% | 72.6% | Más 3.5 | +40.4% | 🟢 Verde |

**Resumen:** 39 verdes, 0 amarillos, 0 rojos, 1 pendientes, 0 terminados sin momio.

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
