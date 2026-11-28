# Tabla de momios y valor esperado — Semana 2 entre semana (Football AI Agenda)

**Partidos:** 2026-11-24 al 2026-11-26, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-28.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2-entresemana.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS: probabilidad Poisson completa (ambos anotan); el EV se calcula solo con momio BSD (llave 'bsd' en momios.json); sin esa llave no lleva EV porque ESPN/DraftKings no trae momio de BTTS en esta fuente.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | P(BTTS) | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 11/24 nov | Galatasaray vs Aston Villa | 2.85 / 4.00 / 2.25 | -48.3% / -36.5% / +48.5% | 3.5 (1.95 / 1.87) | +31.0% / -38.5% | +0.5 (1.62 / 2.15) | -44.7% / +41.9% | 75.6% | Visita | +48.5% | 🟢 Verde |
| 11/24 nov | Arsenal vs Borussia Dortmund | 1.42 / 4.90 / 7.50 | -22.1% / +40.6% / +22.3% | 2.5 (1.61 / 2.35) | -52.1% / +64.9% | -1.5 (2.05 / 1.67) | -45.3% / +22.2% | 32.4% | Menos 2.5 | +64.9% | 🟢 Verde |
| 11/24 nov | Manchester City vs Napoli | 1.29 / 6.50 / 9.00 | +13.6% / -54.9% / -57.8% | 3.5 (1.80 / 2.00) | +44.4% / -60.5% | -1.5 (1.67 / 2.05) | +27.5% / -51.8% | 67.8% | Más 3.5 | +44.4% | 🟢 Verde |
| 11/24 nov | Real Madrid vs PSV Eindhoven | 1.17 / 9.00 / 12.00 | -23.9% / +105.0% / +44.4% | 4.5 (2.00 / 1.80) | -83.1% / +64.8% | -2.5 (1.91 / 1.77) | -66.8% / +46.2% | 36.2% | Empate | +105.0% | 🟢 Verde |
| 11/25 nov | Club Brugge vs Liverpool | 4.50 / 4.70 / 1.62 | +154.8% / -28.7% / -54.2% | 3.5 (1.74 / 2.05) | +52.8% / -75.0% | +0.5 (2.25 / 1.59) | +61.5% / -55.2% | 90.9% | Local | +154.8% | 🟢 Verde |
| 11/25 nov | Internazionale vs VfB Stuttgart | 1.42 / 5.50 / 6.00 | -53.2% / +59.0% / +128.5% | 3.5 (1.65 / 2.25) | -69.5% / +83.3% | -1.5 (1.91 / 1.80) | -75.5% / +56.9% | 44.9% | Visita | +128.5% | 🟢 Verde |
| 11/25 nov | Lille vs Bayern Munich | 5.25 / 4.20 / 1.61 | -78.1% / -62.8% / +39.7% | 2.5 (1.77 / 2.05) | +34.4% / -50.7% | +0.5 (2.30 / 1.56) | -70.0% / +35.3% | 46.7% | AH visitante -0.5 | +41.5% | 🟢 Verde |
| 11/25 nov | Paris Saint-Germain vs AS Roma | 1.44 / 5.00 / 6.50 | +32.3% / -75.3% / -77.3% | 3.5 (1.80 / 2.00) | +62.1% / -80.1% | -1.5 (2.05 / 1.69) | +69.8% / -71.0% | 74.6% | AH local -1.5 | +82.3% | 🟢 Verde |
| 11/25 nov | Sporting CP vs Manchester United | 2.55 / 3.75 / 2.60 | +67.8% / -26.4% / -62.1% | 3.5 (2.25 / 1.62) | -20.3% / +4.9% | -0.5 (2.40 / 1.51) | +57.9% / -48.2% | 51.7% | Local | +67.8% | 🟢 Verde |
| 11/26 nov | Celta Vigo vs AFC Bournemouth | 3.85 / 3.55 / 2.00 | -90.9% / -68.6% / +77.6% | 2.5 (2.00 / 1.80) | +24.2% / -31.7% | +0.5 (1.80 / 1.91) | -79.9% / +69.6% | 26.1% | Visita | +77.6% | 🟢 Verde |
| 11/26 nov | Dinamo Zagreb vs Bayer Leverkusen | 5.00 / 4.40 / 1.62 | -74.1% / +15.9% / +11.3% | 3.5 (2.25 / 1.65) | -82.3% / +51.6% | +0.5 (2.25 / 1.56) | -29.0% / +6.5% | 13.8% | Menos 3.5 | +51.6% | 🟢 Verde |
| 11/26 nov | Olympiacos vs AC Milan | 2.85 / 3.30 / 2.55 | +75.8% / +7.8% / -85.6% | 2.5 (2.15 / 1.69) | -68.9% / +44.5% | +0.5 (1.51 / 2.40) | +42.7% / -86.4% | 10.9% | Local | +75.8% | 🟢 Verde |
| 11/25 nov | Toluca vs Atlas | 1.44 / 4.80 / 6.00 | +2.4% / -38.4% / -2.2% | 2.5 (1.56 / 2.35) | +45.5% / -84.8% | -1.5 (2.10 / 1.65) | +15.2% / -25.7% | 85.4% | Más 2.5 | +45.5% | 🟢 Verde |
| 11/25 nov | Monterrey vs América | 2.25 / 3.30 / 3.15 | -11.2% / -14.2% / +8.8% | 2.5 (1.87 / 1.87) | -7.1% / -6.0% | -0.5 (2.15 / 1.62) | -15.1% / -1.6% | 54.1% | Visita | +8.8% | 🟢 Verde |
| 11/26 nov | Pachuca vs Guadalajara | 2.95 / 3.20 / 2.45 | +15.4% / +1.5% / -28.6% | 2.5 (1.95 / 1.80) | -42.7% / +27.1% | +0.5 (1.54 / 2.35) | +9.1% / -31.5% | 37.0% | Menos 2.5 | +27.1% | 🟢 Verde |
| 11/26 nov | León vs Cruz Azul | 3.20 / 3.60 / 2.15 | +8.2% / -4.0% / -15.1% | 2.5 (1.71 / 2.05) | -19.9% / +9.3% | +0.5 (1.69 / 2.05) | +2.2% / -19.0% | 51.7% | Menos 2.5 | +9.3% | 🟢 Verde |
| 11/25 nov | Sabah FK vs Barcelona | 23.00 / 14.00 / 1.07 | -17.1% / -2.2% / -4.2% | 4.5 (1.91 / 1.87) | -4.6% / -6.4% | +3.5 (1.59 / 2.20) | -4.8% / -11.8% | 53.7% | Empate | -2.2% | 🔴 Rojo |
| 11/25 nov | Slavia Prague vs Villarreal | 3.15 / 3.90 / 2.10 | +45.7% / -23.3% / -28.4% | 3.5 (2.30 / 1.62) | +43.8% / -39.1% | +0.5 (1.71 / 2.00) | +13.0% / -31.8% | 77.9% | Local | +45.7% | 🟢 Verde |
| 11/25 nov | Atlético Madrid vs Viking FK | 1.11 / 10.50 / 20.00 | -57.1% / +178.7% / +596.6% | 3.5 (1.67 / 2.20) | -57.1% / +63.3% | -2.5 (1.80 / 1.91) | -88.8% / +79.1% | 52.3% | Visita | +596.6% | 🟢 Verde |
| 11/25 nov | Shakhtar Donetsk vs Fenerbahce | 2.95 / 3.55 / 2.35 | +66.2% / -5.2% / -60.2% | 2.5 (1.80 / 2.00) | -35.8% / +28.7% | +0.5 (1.59 / 2.20) | +31.9% / -62.7% | 37.2% | Local | +66.2% | 🟢 Verde |
| 11/26 nov | Besiktas vs Hapoel Be'er | 1.40 / 5.25 / 7.00 | +30.5% / -71.8% / -90.0% | 3.5 (2.10 / 1.74) | +15.3% / -21.5% | -1.5 (2.00 / 1.71) | +61.2% / -66.8% | 28.6% | Spread local -1.5 | +61.2% | 🟢 Verde |
| 11/26 nov | Marseille vs Levski Sofia | 1.39 / 5.00 / 8.00 | -88.1% / +74.9% / +351.9% | 2.5 (1.77 / 2.05) | -75.1% / +76.2% | -1.5 (2.05 / 1.69) | -98.0% / +67.3% | 14.0% | Visita | +351.9% | 🟢 Verde |
| 11/26 nov | RB Salzburg vs Ararat-Armenia | 1.18 / 8.00 / 13.00 | -47.1% / +88.6% / +311.3% | 3.5 (1.71 / 2.10) | -35.8% / +31.4% | -2.5 (2.20 / 1.61) | -77.9% / +44.5% | 61.5% | Visita | +311.3% | 🟢 Verde |
| 11/26 nov | Union St.-Gilloise vs Lech Poznan | 1.34 / 5.50 / 8.50 | +31.9% / -92.7% / -98.4% | 3.5 (2.30 / 1.61) | +70.1% / -58.2% | -1.5 (1.83 / 1.87) | +71.9% / -88.3% | 15.9% | AH local -1.5 | +83.6% | 🟢 Verde |
| 11/26 nov | Viktoria Plzen vs Benfica | 5.50 / 4.50 / 1.56 | -94.1% / -81.9% / +47.6% | 2.5 (1.59 / 2.35) | +28.2% / -54.6% | +0.5 (2.35 / 1.53) | -88.1% / +44.9% | 30.0% | AH visitante -1.5 | +94.6% | 🟢 Verde |
| 11/26 nov | Crystal Palace vs Real Sociedad | 1.95 / 4.00 / 3.50 | -55.0% / -22.4% / +101.5% | 3.5 (2.25 / 1.65) | +19.1% / -22.6% | -0.5 (1.87 / 1.83) | -56.9% / +41.1% | 69.4% | Visita | +101.5% | 🟢 Verde |
| 11/26 nov | Ferencvaros vs NK Celje | 1.38 / 5.25 / 7.50 | +26.7% / -70.6% / -81.9% | 3.5 (2.25 / 1.65) | +54.0% / -48.1% | -1.5 (1.95 / 1.77) | +57.2% / -65.5% | 47.2% | AH local -1.5 | +60.1% | 🟢 Verde |
| 11/26 nov | Juventus vs Omonia Nicosia | 1.20 / 7.00 / 14.00 | -6.2% / -11.7% / +29.6% | 2.5 (1.56 / 2.45) | +22.1% / -47.3% | -1.5 (1.59 / 2.20) | -5.2% / -11.3% | 62.0% | Visita | +29.6% | 🟢 Verde |
| 11/26 nov | Lyon vs Lillestrom | 1.25 / 6.50 / 11.00 | -3.0% / -2.6% / -18.3% | 3.5 (2.25 / 1.65) | -18.6% / +5.0% | -1.5 (1.69 / 2.05) | -7.2% / -7.6% | 41.7% | Menos 3.5 | +5.0% | 🟢 Verde |
| 11/26 nov | NEC Nijmegen vs Stade Rennais | 3.00 / 3.90 / 2.20 | -29.8% / -1.3% / +12.9% | 3.5 (2.20 / 1.67) | -44.7% / +24.8% | +0.5 (1.67 / 2.05) | -18.8% / +5.2% | 49.2% | Menos 3.5 | +24.8% | 🟢 Verde |
| 11/26 nov | OFI Crete vs Anderlecht | 4.50 / 3.80 / 1.77 | -5.4% / +26.8% / -19.3% | 2.5 (1.80 / 2.00) | -58.5% / +53.8% | +0.5 (2.00 / 1.71) | +8.8% / -21.8% | 29.5% | Menos 2.5 | +53.8% | 🟢 Verde |
| 11/26 nov | Sparta Prague vs AZ Alkmaar | 2.60 / 3.60 / 2.60 | -48.7% / -18.3% / +49.7% | 2.5 (1.74 / 2.10) | -7.5% / -1.6% | -0.5 (2.45 / 1.49) | -51.7% / +19.4% | 52.2% | Visita | +49.7% | 🟢 Verde |
| 11/26 nov | Sunderland vs Jagiellonia Bialystok | 1.27 / 5.75 / 11.00 | -41.6% / +80.7% / +148.4% | 2.5 (1.65 / 2.25) | -54.3% / +62.5% | -1.5 (1.74 / 1.95) | -65.8% / +56.9% | 34.1% | Visita | +148.4% | 🟢 Verde |
| 11/26 nov | Torreense vs Celtic | 4.50 / 4.40 / 1.69 | +143.7% / -26.6% / -50.7% | 3.5 (2.15 / 1.71) | +71.0% / -64.9% | +0.5 (2.15 / 1.62) | +52.3% / -52.6% | 86.5% | Local | +143.7% | 🟢 Verde |
| 11/26 nov | TSG Hoffenheim vs SK Sturm Graz | 1.29 / 6.50 / 9.00 | -31.8% / +73.7% / +81.9% | 3.5 (1.80 / 2.00) | -66.0% / +62.2% | -1.5 (1.69 / 2.05) | -54.6% / +49.9% | 41.7% | Visita | +81.9% | 🟢 Verde |

**Resumen:** 34 verdes, 0 amarillos, 1 rojos, 0 pendientes, 0 terminados sin momio.
Único(s) sin valor: Sabah FK–Barcelona (mejor EV -2.2%, Empate).

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
