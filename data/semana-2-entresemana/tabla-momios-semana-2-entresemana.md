# Tabla de momios y valor esperado — Semana 2 entre semana (Football AI Agenda)

**Partidos:** 2026-11-24 al 2026-11-26, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-23.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2-entresemana.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS no tiene momio en esta fuente, por eso no lleva EV.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 11/24 nov | Galatasaray vs Aston Villa | 2.85 / 4.00 / 2.25 | -48.3% / -36.5% / +48.5% | 3.5 (1.95 / 1.87) | +31.0% / -38.5% | +0.5 (1.62 / 2.15) | -44.7% / +41.9% | Visita | +48.5% | 🟢 Verde |
| 11/24 nov | Arsenal vs Borussia Dortmund | 1.42 / 4.90 / 7.50 | -22.1% / +40.6% / +22.3% | 2.5 (1.61 / 2.35) | -52.1% / +64.9% | -1.5 (2.05 / 1.67) | -45.3% / +22.2% | Menos 2.5 | +64.9% | 🟢 Verde |
| 11/24 nov | Manchester City vs Napoli | 1.29 / 6.50 / 9.00 | +13.6% / -54.9% / -57.8% | 3.5 (1.80 / 2.00) | +44.4% / -60.5% | -1.5 (1.67 / 2.05) | +27.5% / -51.8% | Más 3.5 | +44.4% | 🟢 Verde |
| 11/24 nov | Real Madrid vs PSV Eindhoven | 1.17 / 9.00 / 12.00 | -23.5% / +105.0% / +44.4% | 4.5 (2.00 / 1.80) | -83.1% / +64.8% | -2.5 (1.95 / 1.77) | -66.1% / +46.2% | Empate | +105.0% | 🟢 Verde |
| 11/25 nov | Club Brugge vs Liverpool | 4.40 / 4.70 / 1.65 | +149.1% / -28.7% / -53.6% | 3.5 (1.77 / 2.05) | +55.3% / -75.0% | +0.5 (2.20 / 1.59) | +58.0% / -55.2% | Local | +149.1% | 🟢 Verde |
| 11/25 nov | Internazionale vs VfB Stuttgart | 1.43 / 5.50 / 6.00 | -52.9% / +59.0% / +128.5% | 3.5 (1.62 / 2.30) | -69.9% / +87.4% | -1.5 (1.91 / 1.80) | -75.5% / +56.9% | Visita | +128.5% | 🟢 Verde |
| 11/25 nov | Lille vs Bayern Munich | 5.00 / 4.50 / 1.61 | -79.1% / -60.2% / +39.7% | 2.5 (1.57 / 2.40) | +19.3% / -42.2% | +0.5 (2.30 / 1.56) | -70.0% / +35.3% | Visita | +39.7% | 🟢 Verde |
| 11/25 nov | Paris Saint-Germain vs AS Roma | 1.43 / 5.00 / 6.50 | +30.5% / -75.3% / -77.3% | 3.5 (1.87 / 1.91) | +68.3% / -81.0% | -1.5 (2.05 / 1.69) | +69.8% / -71.0% | Spread local -1.5 | +69.8% | 🟢 Verde |
| 11/25 nov | Sporting CP vs Manchester United | 2.40 / 3.75 / 2.70 | +57.9% / -26.4% / -60.6% | 3.5 (2.35 / 1.61) | -16.8% / +3.7% | -0.5 (2.30 / 1.56) | +51.3% / -46.8% | Local | +57.9% | 🟢 Verde |
| 11/26 nov | Celta Vigo vs AFC Bournemouth | 3.80 / 3.65 / 1.95 | -91.1% / -67.8% / +73.4% | 2.5 (1.87 / 1.91) | +16.1% / -27.6% | +0.5 (1.80 / 1.91) | -79.9% / +69.6% | Visita | +73.4% | 🟢 Verde |
| 11/26 nov | Dinamo Zagreb vs Bayer Leverkusen | 4.40 / 4.30 / 1.71 | -77.2% / +13.3% / +17.4% | 3.5 (2.20 / 1.69) | -82.7% / +55.7% | +0.5 (2.15 / 1.65) | -32.2% / +12.6% | Menos 3.5 | +55.7% | 🟢 Verde |
| 11/26 nov | Olympiacos vs AC Milan | 2.75 / 3.45 / 2.55 | +69.6% / +12.7% / -85.6% | 2.5 (1.83 / 1.95) | -73.5% / +67.0% | +0.5 (1.51 / 2.35) | +42.7% / -86.7% | Local | +69.6% | 🟢 Verde |

**Resumen:** 12 verdes, 0 amarillos, 0 rojos, 0 pendientes.

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
