# Tabla de momios y valor esperado — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-27 al 2026-11-29, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-28.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2.md) × momio decimal − 1. Probabilidades calibradas (28 nov 2026): se encogen hacia las tasas base reales (α=0.35) antes de calcular el EV; la probabilidad cruda queda en prob_cruda de ev.json. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS: probabilidad Poisson completa (ambos anotan); el EV se calcula solo con momio BSD (llave 'bsd' en momios.json); sin esa llave no lleva EV porque ESPN/DraftKings no trae momio de BTTS en esta fuente.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | P(BTTS) | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 11/27 nov | Werder Bremen vs Borussia Mönchengladbach | 1.69 / 4.00 / 4.20 | -10.5% / +3.8% / -11.5% | 3.5 (2.35 / 1.59) | +3.0% / -10.8% | -0.5 (1.67 / 2.10) | -16.1% / +4.3% | 55.2% | AH visitante +0.5 | +11.4% | 🟢 Verde |
| 11/27 nov | Venezia vs Bologna | 2.95 / 3.05 / 2.40 | -3.9% / -7.5% / -10.9% | 2.5 (2.20 / 1.65) | +4.4% / -13.6% | +0.5 (1.54 / 2.30) | -38.3% / +37.9% | 46.2% | AH visitante -0.5 | +46.2% | 🟢 Verde |
| 11/27 nov | Nottingham Forest vs Chelsea | 2.45 / 3.45 / 2.85 | -21.2% / -7.0% / +16.6% | 2.5 (1.77 / 2.05) | +1.3% / -12.4% | -0.5 (2.25 / 1.56) | -33.6% / +9.6% | 52.9% | Visita | +16.6% | 🟢 Verde |
| 11/27 nov | Levante vs Racing Santander | 2.00 / 3.90 / 3.50 | -7.0% / +10.9% / -12.3% | 3.5 (2.30 / 1.62) | -27.3% / +11.1% | -0.5 (1.91 / 1.80) | -16.2% / +1.0% | 55.3% | Menos 3.5 | +11.1% | 🟢 Verde |
| 11/28 nov | Hamburg SV vs Bayern Munich (Bet 365) | 8.00 / 5.75 / 1.30 | +205.6% / +57.0% / -55.2% | — | — | — | — | 61.9% | Local | +205.6% | 🟢 Verde |
| 11/28 nov | Manchester United vs Brentford | 2.35 / 3.70 / 2.85 | -7.6% / +3.0% / -6.5% | 3.5 (2.35 / 1.59) | +13.2% / -17.7% | -0.5 (2.20 / 1.59) | -19.3% / +0.5% | 60.4% | Más 3.5 | +13.2% | 🟢 Verde |
| 11/28 nov | Elche vs Atlético Madrid | 7.00 / 4.70 / 1.43 | +137.2% / +71.4% / -57.5% | 2.5 (1.65 / 2.25) | -33.3% / +33.7% | +1.5 (1.62 / 2.15) | -7.9% / -6.8% | 41.0% | Local | +137.2% | 🟢 Verde |
| 11/28 nov | VfB Stuttgart vs Eintracht Frankfurt | 1.77 / 4.10 / 3.75 | -2.0% / +2.0% / -25.9% | 3.5 (1.95 / 1.83) | -8.1% / -2.9% | -0.5 (1.71 / 2.00) | -9.6% / -5.5% | 53.8% | Empate | +2.0% | 🟡 Amarillo |
| 11/28 nov | Internazionale vs Genoa | 1.21 / 6.00 / 11.00 | -46.6% / +85.9% / +174.4% | 3.5 (2.05 / 1.74) | -74.4% / +52.4% | -1.5 (1.65 / 2.10) | -46.9% / +42.3% | 48.6% | Visita | +174.4% | 🟢 Verde |
| 11/28 nov | Real Madrid vs Alavés | 1.13 / 9.00 / 17.00 | -29.3% / +84.6% / +190.5% | 3.5 (1.71 / 2.10) | +43.1% / -65.3% | -2.5 (2.00 / 1.71) | +12.6% / -25.1% | 43.6% | Visita | +190.5% | 🟢 Verde |
| 11/29 nov | Everton vs Liverpool | 4.60 / 3.85 / 1.74 | +86.8% / +11.6% / -47.1% | 2.5 (1.61 / 2.35) | -8.6% / +1.3% | +0.5 (2.05 / 1.67) | -4.2% / -11.2% | 56.4% | Local | +86.8% | 🟢 Verde |
| 11/29 nov | Sassuolo vs Napoli | 4.40 / 4.20 / 1.62 | +33.1% / -0.3% / -25.2% | 2.5 (1.57 / 2.35) | +6.6% / -24.4% | +0.5 (2.20 / 1.61) | -31.5% / +10.6% | 59.3% | Local | +33.1% | 🟢 Verde |
| 11/29 nov | Deportivo vs Barcelona | 10.00 / 7.50 / 1.22 | +217.6% / +88.2% / -47.3% | 3.5 (1.62 / 2.30) | -1.5% / -9.5% | +2.5 (1.57 / 2.25) | -25.3% / +18.1% | 59.3% | Local | +217.6% | 🟢 Verde |
| 11/29 nov | Arsenal vs Manchester City | 2.00 / 3.75 / 3.55 | +13.6% / -5.8% / -35.8% | 2.5 (1.65 / 2.25) | -12.4% / +5.2% | -0.5 (1.91 / 1.80) | +3.4% / -17.5% | 42.7% | Local | +13.6% | 🟢 Verde |
| 11/29 nov | Borussia Dortmund vs Bayer Leverkusen | 2.05 / 3.80 / 3.00 | +7.0% / -1.2% / -34.7% | 3.5 (2.15 / 1.69) | +6.4% / -14.6% | -0.5 (2.05 / 1.69) | +1.6% / -14.8% | 57.4% | Local | +7.0% | 🟢 Verde |
| 11/29 nov | Como vs Juventus | 1.95 / 3.45 / 3.65 | -5.3% / +1.5% / -19.5% | 2.5 (1.80 / 1.95) | -10.4% / -1.9% | -0.5 (1.91 / 1.80) | -12.4% / -2.6% | 48.0% | Empate | +1.5% | 🟡 Amarillo |
| 11/28 nov | Atlas vs Toluca | 2.90 / 3.80 / 2.25 | -0.6% / -0.9% / -10.8% | 3.5 (2.15 / 1.67) | +34.7% / -37.7% | +0.5 (1.62 / 2.15) | -39.0% / +34.4% | 61.9% | AH visitante -0.5 | +37.8% | 🟢 Verde |
| 11/28 nov | América vs Monterrey | 2.00 / 3.30 / 3.90 | -5.6% / -11.5% / +1.3% | 2.5 (1.77 / 2.00) | +15.8% / -30.9% | -0.5 (1.91 / 1.77) | -14.9% / -1.9% | 62.4% | Más 2.5 | +15.8% | 🟢 Verde |
| 11/29 nov | Guadalajara vs Pachuca | 1.62 / 3.95 / 4.90 | -32.1% / +19.6% / +36.9% | 2.5 (1.62 / 2.15) | -16.4% / +4.3% | -0.5 (1.59 / 2.15) | -37.8% / +30.8% | 52.0% | Visita | +36.9% | 🟢 Verde |
| 11/29 nov | Cruz Azul vs León | pendiente | — | — | — | — | — | 56.8% | — | — | ⏳ Pendiente |
| 11/28 nov | Leeds United vs Coventry City | 1.47 / 4.60 / 6.50 | -44.1% / +37.3% / +107.9% | 2.5 (1.65 / 2.25) | -13.2% / +6.3% | -1.5 (2.20 / 1.61) | -36.0% / +13.9% | 53.0% | Visita | +107.9% | 🟢 Verde |
| 11/28 nov | Ipswich Town vs Aston Villa | 3.35 / 3.70 / 2.10 | +38.2% / -1.8% / -32.3% | 2.5 (1.61 / 2.35) | +10.8% / -27.1% | +0.5 (1.71 / 2.00) | -23.0% / +10.2% | 66.1% | Local | +38.2% | 🟢 Verde |
| 11/28 nov | Real Betis vs Rayo Vallecano | 1.62 / 4.20 / 5.25 | -16.6% / +10.0% / +18.0% | 2.5 (1.59 / 2.35) | +0.6% / -13.9% | -0.5 (1.57 / 2.25) | -23.4% / +15.4% | 58.7% | AH visitante +0.5 | +21.5% | 🟢 Verde |
| 11/28 nov | Málaga vs Athletic Club | 4.70 / 3.85 / 1.74 | +55.0% / +0.5% / -28.8% | 2.5 (1.80 / 2.00) | +14.2% / -26.9% | +0.5 (2.10 / 1.67) | -23.9% / +6.3% | 58.6% | Local | +55.0% | 🟢 Verde |
| 11/28 nov | FC Cologne vs SV Elversberg | 2.00 / 3.60 / 3.30 | -12.5% / +7.6% / -13.0% | 2.5 (1.62 / 2.30) | -15.3% / +10.1% | -0.5 (1.95 / 1.77) | -19.7% / +4.2% | 52.2% | Menos 2.5 | +10.1% | 🟢 Verde |
| 11/28 nov | Mainz vs 1. FC Union Berlin | 1.45 / 4.50 / 5.75 | -40.4% / +42.4% / +57.6% | 3.5 (2.25 / 1.62) | -75.0% / +44.4% | -1.5 (2.15 / 1.62) | -35.3% / +13.6% | 48.6% | Visita | +57.6% | 🟢 Verde |
| 11/28 nov | SC Paderborn 07 vs Schalke 04 | 2.60 / 3.35 / 2.50 | +24.0% / +7.9% / -49.7% | 2.5 (1.65 / 2.25) | -29.0% / +27.9% | +0.5 (1.50 / 2.40) | -14.5% / +3.1% | 41.4% | Menos 2.5 | +27.9% | 🟢 Verde |
| 11/28 nov | Frosinone vs Parma | 1.40 / 5.00 / 6.00 | -26.7% / +30.7% / +29.0% | 3.5 (1.87 / 1.91) | -16.2% / +5.3% | -1.5 (1.95 / 1.74) | -18.0% / +0.9% | 56.0% | Empate | +30.7% | 🟢 Verde |
| 11/28 nov | Torino vs Lazio | 3.55 / 3.40 / 2.00 | +11.7% / -13.3% / -13.9% | 2.5 (1.77 / 2.05) | +10.5% / -23.1% | +0.5 (1.77 / 1.95) | -39.7% / +28.7% | 56.1% | AH visitante -0.5 | +34.8% | 🟢 Verde |
| 11/29 nov | Brighton & Hove Albion vs Newcastle United | 1.56 / 4.50 / 5.50 | -8.3% / +5.1% / -2.8% | 3.5 (2.35 / 1.61) | -18.3% / +4.7% | -1.5 (2.40 / 1.50) | +19.2% / -24.5% | 43.1% | Spread local -1.5 | +19.2% | 🟢 Verde |
| 11/29 nov | Crystal Palace vs Hull City | 1.91 / 3.75 / 3.85 | -32.7% / +5.0% / +41.6% | 2.5 (1.77 / 2.05) | +2.9% / -14.2% | -0.5 (1.87 / 1.83) | -39.0% / +23.5% | 56.1% | Visita | +41.6% | 🟢 Verde |
| 11/29 nov | Fulham vs AFC Bournemouth | 2.80 / 3.50 / 2.50 | +12.9% / +5.1% / -25.9% | 2.5 (1.80 / 2.00) | -5.5% / -5.0% | +0.5 (1.54 / 2.35) | -26.8% / +23.4% | 52.9% | AH visitante -0.5 | +29.3% | 🟢 Verde |
| 11/29 nov | Sunderland vs Tottenham Hotspur | 4.00 / 3.45 / 1.95 | +17.6% / -3.9% / -16.5% | 2.5 (1.95 / 1.83) | -6.1% / -4.8% | +0.5 (1.83 / 1.83) | -36.9% / +20.3% | 42.1% | AH visitante -0.5 | +31.0% | 🟢 Verde |
| 11/29 nov | Valencia vs Osasuna | 2.15 / 3.20 / 3.60 | -6.7% / -7.5% / -0.4% | 2.5 (2.25 / 1.62) | +27.4% / -29.5% | -0.5 (2.05 / 1.69) | -16.4% / +0.1% | 56.0% | Más 2.5 | +27.4% | 🟢 Verde |
| 11/29 nov | Celta Vigo vs Villarreal | 2.75 / 3.55 / 2.50 | -10.6% / +39.9% / -29.8% | 2.5 (1.77 / 2.05) | -30.8% / +24.8% | +0.5 (1.53 / 2.35) | -25.1% / +19.7% | 39.0% | Empate | +39.9% | 🟢 Verde |
| 11/29 nov | Real Sociedad vs Sevilla | 2.15 / 3.65 / 3.30 | +25.3% / -17.1% / -37.2% | 2.5 (1.77 / 2.05) | +25.6% / -40.5% | -0.5 (2.00 / 1.71) | +11.3% / -23.9% | 62.8% | Más 2.5 | +25.6% | 🟢 Verde |
| 11/29 nov | SC Freiburg vs RB Leipzig | 2.65 / 3.70 / 2.30 | -0.4% / -1.6% / -17.6% | 3.5 (2.20 / 1.67) | +50.2% / -47.1% | +0.5 (1.57 / 2.25) | -35.1% / +32.1% | 64.3% | Más 3.5 | +50.2% | 🟢 Verde |
| 11/29 nov | TSG Hoffenheim vs FC Augsburg | 1.67 / 4.50 / 3.90 | -6.1% / +6.8% / -22.2% | 3.5 (1.77 / 2.00) | +35.1% / -52.8% | -0.5 (1.65 / 2.15) | -11.7% / -0.4% | 61.5% | Más 3.5 | +35.1% | 🟢 Verde |
| 11/29 nov | Udinese vs Fiorentina | 3.00 / 3.40 / 2.20 | -9.3% / -16.3% / -0.7% | 2.5 (1.71 / 2.10) | +7.4% / -21.5% | +0.5 (1.65 / 2.15) | -47.4% / +46.2% | 54.0% | AH visitante -0.5 | +50.8% | 🟢 Verde |
| 11/29 nov | AS Roma vs Monza | 1.18 / 7.00 / 11.00 | -32.9% / +64.7% / +117.0% | 3.5 (1.83 / 1.95) | +43.0% / -57.0% | -2.5 (2.20 / 1.61) | -5.4% / -8.5% | 61.6% | Visita | +117.0% | 🟢 Verde |

**Resumen:** 37 verdes, 2 amarillos, 0 rojos, 1 pendientes, 0 terminados sin momio.

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
