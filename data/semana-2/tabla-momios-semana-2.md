# Tabla de momios y valor esperado — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-27 al 2026-11-29, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-27.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS: probabilidad Poisson completa (ambos anotan); el EV se calcula solo con momio BSD (llave 'bsd' en momios.json); sin esa llave no lleva EV porque ESPN/DraftKings no trae momio de BTTS en esta fuente.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | P(BTTS) | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 11/27 nov | Werder Bremen vs Borussia Mönchengladbach | 1.67 / 4.00 / 4.30 | +20.3% / -34.6% / -50.6% | 3.5 (2.30 / 1.59) | +0.8% / -10.8% | -0.5 (1.65 / 2.10) | +18.7% / -41.5% | 54.2% | Local | +20.3% | 🟢 Verde |
| 11/27 nov | Venezia vs Bologna | 2.85 / 3.00 / 2.50 | -60.5% / -13.6% / +43.3% | 2.5 (2.20 / 1.65) | -39.9% / +19.6% | +0.5 (1.50 / 2.40) | -36.0% / +37.6% | 28.6% | Visita | +43.3% | 🟢 Verde |
| 11/27 nov | Nottingham Forest vs Chelsea | 2.45 / 3.45 / 2.85 | -69.0% / -33.8% / +94.2% | 2.5 (1.74 / 2.10) | -3.6% / -6.3% | -0.5 (2.30 / 1.54) | -70.9% / +34.5% | 47.8% | Visita | +94.2% | 🟢 Verde |
| 11/27 nov | Levante vs Racing Santander | 2.00 / 3.95 / 3.40 | +7.3% / -7.5% / -22.1% | 3.5 (2.15 / 1.71) | -32.0% / +17.2% | -0.5 (1.91 / 1.77) | +2.5% / -18.0% | 54.5% | Menos 3.5 | +17.2% | 🟢 Verde |
| 11/28 nov | Hamburg SV vs Bayern Munich (Bet 365) | 8.00 / 7.00 / 1.27 | +139.5% / +41.5% / -36.7% | — | — | — | — | 73.4% | Local | +139.5% | 🟢 Verde |
| 11/28 nov | Manchester United vs Brentford | 2.20 / 3.75 / 3.05 | -27.0% / -18.4% / +37.4% | 2.5 (1.57 / 2.40) | +9.2% / -26.7% | -0.5 (2.10 / 1.67) | -30.3% / +11.4% | 69.1% | Visita | +37.4% | 🟢 Verde |
| 11/28 nov | Elche vs Atlético Madrid | 6.50 / 4.80 / 1.47 | +14.7% / +122.7% / -47.3% | 2.5 (1.61 / 2.35) | -87.8% / +117.1% | +1.5 (1.61 / 2.20) | +44.9% / -78.5% | 13.8% | Empate | +122.7% | 🟢 Verde |
| 11/28 nov | VfB Stuttgart vs Eintracht Frankfurt | 1.80 / 4.30 / 3.35 | +42.1% / -42.8% / -74.1% | 3.5 (1.71 / 2.10) | -19.3% / +11.2% | -0.5 (1.77 / 1.91) | +39.7% / -59.9% | 50.2% | Local | +42.1% | 🟢 Verde |
| 11/28 nov | Internazionale vs Genoa | 1.29 / 5.50 / 8.50 | -39.9% / +68.8% / +91.8% | 3.5 (2.35 / 1.59) | -70.7% / +39.0% | -1.5 (1.80 / 1.91) | -63.1% / +51.8% | 35.5% | Visita | +91.8% | 🟢 Verde |
| 11/28 nov | Real Madrid vs Alavés | 1.12 / 10.00 / 18.00 | +11.4% / -91.8% / -97.5% | 3.5 (1.80 / 2.00) | +50.3% / -67.0% | -2.5 (1.91 / 1.77) | +70.2% / -80.8% | 21.1% | Spread local -2.5 | +70.2% | 🟢 Verde |
| 11/29 nov | Everton vs Liverpool | 4.60 / 3.85 / 1.74 | +69.4% / -3.7% / -33.6% | 2.5 (1.67 / 2.25) | -9.6% / +2.9% | +0.5 (2.05 / 1.69) | +26.8% / -35.5% | 57.7% | Local | +69.4% | 🟢 Verde |
| 11/29 nov | Sassuolo vs Napoli | 4.40 / 4.20 / 1.62 | -68.0% / -57.9% / +34.4% | 2.5 (1.57 / 2.35) | +34.4% / -66.0% | +0.5 (2.15 / 1.61) | -62.8% / +32.8% | 65.9% | Más 2.5 | +34.4% | 🟢 Verde |
| 11/29 nov | Deportivo vs Barcelona | 10.00 / 7.50 / 1.22 | +15.6% / +4.1% / -8.9% | 3.5 (1.65 / 2.25) | -0.3% / -11.4% | +2.5 (1.57 / 2.25) | +0.7% / -19.1% | 65.8% | Local | +15.6% | 🟢 Verde |
| 11/29 nov | Arsenal vs Manchester City | 2.00 / 3.70 / 3.60 | +66.1% / -48.3% / -89.3% | 2.5 (1.77 / 2.05) | -22.5% / +15.2% | -0.5 (1.91 / 1.80) | +58.6% / -69.5% | 18.6% | Local | +66.1% | 🟢 Verde |
| 11/29 nov | Borussia Dortmund vs Bayer Leverkusen | 2.05 / 3.80 / 3.00 | +43.4% / -37.3% / -59.4% | 3.5 (2.15 / 1.69) | +6.4% / -14.6% | -0.5 (2.00 / 1.71) | +39.9% / -48.5% | 60.6% | Local | +43.4% | 🟢 Verde |
| 11/29 nov | Como vs Juventus | 1.95 / 3.45 / 3.65 | +16.0% / -9.5% / -47.7% | 2.5 (1.80 / 2.00) | -39.0% / +32.2% | -0.5 (1.91 / 1.80) | +13.5% / -27.0% | 33.8% | Menos 2.5 | +32.2% | 🟢 Verde |
| 11/28 nov | Atlas vs Toluca | 2.95 / 3.80 / 2.15 | -44.6% / -36.5% / +38.7% | 3.5 (2.10 / 1.67) | +31.5% / -37.7% | +0.5 (1.67 / 2.05) | -40.9% / +32.3% | 73.3% | Visita | +38.7% | 🟢 Verde |
| 11/28 nov | América vs Monterrey | 2.20 / 3.05 / 3.50 | +22.4% / -42.5% / -10.7% | 2.5 (1.77 / 1.91) | +39.3% / -59.4% | -0.5 (2.05 / 1.65) | +14.1% / -27.0% | 74.7% | Más 2.5 | +39.3% | 🟢 Verde |
| 11/29 nov | Guadalajara vs Pachuca | 1.65 / 3.95 / 4.70 | -33.8% / +13.2% / +46.3% | 2.5 (1.61 / 2.20) | -37.7% / +34.7% | -0.5 (1.62 / 2.10) | -34.7% / +25.6% | 45.1% | Visita | +46.3% | 🟢 Verde |
| 11/29 nov | Cruz Azul vs León | pendiente | — | — | — | — | — | 58.7% | — | — | ⏳ Pendiente |

**Resumen:** 19 verdes, 0 amarillos, 0 rojos, 1 pendientes, 0 terminados sin momio.

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
