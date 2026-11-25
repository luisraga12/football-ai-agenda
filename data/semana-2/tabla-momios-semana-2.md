# Tabla de momios y valor esperado — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-27 al 2026-11-29, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-25.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS: probabilidad Poisson completa (ambos anotan); no lleva EV porque ESPN/DraftKings no trae momio de BTTS en esta fuente.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | P(BTTS) | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 11/27 nov | Werder Bremen vs Borussia Mönchengladbach | 1.69 / 4.20 / 4.00 | +21.9% / -31.3% / -54.0% | 3.5 (2.20 / 1.65) | -3.6% / -7.6% | -0.5 (1.67 / 2.05) | +20.3% / -42.9% | 54.2% | Local | +21.9% | 🟢 Verde |
| 11/27 nov | Venezia vs Bologna | 3.30 / 3.25 / 2.15 | -54.2% / -6.4% / +23.3% | 2.5 (2.00 / 1.80) | -45.4% / +30.8% | +0.5 (1.67 / 2.05) | -28.9% / +17.5% | 28.6% | Menos 2.5 | +30.8% | 🟢 Verde |
| 11/27 nov | Nottingham Forest vs Chelsea | 2.55 / 3.40 / 2.80 | -67.7% / -34.8% / +90.8% | 2.5 (1.74 / 2.05) | -3.6% / -8.6% | -0.5 (2.40 / 1.51) | -69.6% / +32.1% | 47.8% | Visita | +90.8% | 🟢 Verde |
| 11/27 nov | Levante vs Racing Santander | 2.10 / 3.90 / 3.20 | +12.7% / -8.6% / -26.7% | 3.5 (2.15 / 1.69) | -32.0% / +15.6% | -0.5 (1.95 / 1.74) | +4.8% / -19.3% | 54.5% | Menos 3.5 | +15.6% | 🟢 Verde |
| 11/28 nov | Hamburg SV vs Bayern Munich (Bet 365) | 9.50 / 6.25 / 1.25 | +184.4% / +26.3% / -37.7% | — | — | — | — | 73.4% | Local | +184.4% | 🟢 Verde |
| 11/28 nov | Manchester United vs Brentford | 2.10 / 3.75 / 3.25 | -30.3% / -18.4% / +46.5% | 3.5 (2.40 / 1.57) | +15.6% / -18.5% | -0.5 (2.00 / 1.71) | -33.6% / +14.6% | 69.1% | Visita | +46.5% | 🟢 Verde |
| 11/28 nov | Elche vs Atlético Madrid | 6.00 / 4.70 / 1.50 | +5.9% / +118.0% / -46.1% | 3.5 (2.40 / 1.57) | -95.8% / +54.4% | +1.5 (1.61 / 2.20) | +44.9% / -78.5% | 13.8% | Empate | +118.0% | 🟢 Verde |
| 11/28 nov | VfB Stuttgart vs Eintracht Frankfurt | 1.71 / 4.40 / 3.65 | +35.4% / -41.5% / -71.8% | 3.5 (1.69 / 2.15) | -20.5% / +13.8% | -0.5 (1.69 / 2.05) | +33.4% / -56.9% | 50.2% | Local | +35.4% | 🟢 Verde |
| 11/28 nov | Internazionale vs Genoa | 1.30 / 5.25 / 8.00 | -39.1% / +61.1% / +80.6% | 3.5 (2.35 / 1.57) | -70.7% / +37.6% | -1.5 (1.87 / 1.83) | -61.7% / +45.8% | 35.5% | Visita | +80.6% | 🟢 Verde |
| 11/28 nov | Real Madrid vs Alavés | 1.13 / 9.50 / 17.00 | +12.2% / -92.2% / -97.6% | 3.5 (1.83 / 1.95) | +53.0% / -67.7% | -2.5 (2.00 / 1.74) | +78.3% / -81.1% | 21.1% | Spread local -2.5 | +78.3% | 🟢 Verde |
| 11/29 nov | Everton vs Liverpool | 4.10 / 3.60 / 1.87 | +51.0% / -9.9% / -28.7% | 2.5 (1.67 / 2.15) | -9.6% / -1.6% | +0.5 (1.91 / 1.77) | +18.1% / -32.5% | 57.7% | Local | +51.0% | 🟢 Verde |
| 11/29 nov | Sassuolo vs Napoli | 4.30 / 4.10 / 1.62 | -68.7% / -58.9% / +34.4% | 2.5 (1.56 / 2.35) | +33.0% / -66.0% | +0.5 (2.15 / 1.59) | -62.8% / +31.4% | 65.9% | Visita | +34.4% | 🟢 Verde |
| 11/29 nov | Deportivo vs Barcelona | 9.00 / 7.00 / 1.24 | +4.0% / -2.8% / -7.9% | 3.5 (1.65 / 2.20) | -0.3% / -13.4% | +1.5 (2.15 / 1.59) | -4.4% / -11.8% | 65.8% | Local | +4.0% | 🟡 Amarillo |
| 11/29 nov | Arsenal vs Manchester City | 1.95 / 3.75 / 3.55 | +62.2% / -47.6% / -89.5% | 2.5 (1.71 / 2.05) | -24.9% / +15.2% | -0.5 (1.87 / 1.77) | +55.3% / -70.0% | 18.6% | Local | +62.2% | 🟢 Verde |
| 11/29 nov | Borussia Dortmund vs Bayer Leverkusen | 2.10 / 3.70 / 2.90 | +46.9% / -38.9% / -60.8% | 3.5 (2.15 / 1.65) | +6.4% / -16.9% | -0.5 (2.00 / 1.69) | +39.9% / -49.3% | 60.6% | Local | +46.9% | 🟢 Verde |
| 11/29 nov | Como vs Juventus | 2.00 / 3.40 / 3.30 | +18.9% / -10.8% / -52.7% | 2.5 (1.77 / 1.95) | -40.0% / +29.0% | -0.5 (1.95 / 1.71) | +16.0% / -30.5% | 33.8% | Menos 2.5 | +29.0% | 🟢 Verde |
| 11/28 nov | Atlas vs Toluca | pendiente | — | — | — | — | — | 73.3% | — | — | ⏳ Pendiente |
| 11/28 nov | América vs Monterrey | pendiente | — | — | — | — | — | 74.7% | — | — | ⏳ Pendiente |
| 11/29 nov | Guadalajara vs Pachuca | pendiente | — | — | — | — | — | 45.1% | — | — | ⏳ Pendiente |
| 11/29 nov | Cruz Azul vs León | pendiente | — | — | — | — | — | 58.7% | — | — | ⏳ Pendiente |

**Resumen:** 15 verdes, 1 amarillos, 0 rojos, 4 pendientes.

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
