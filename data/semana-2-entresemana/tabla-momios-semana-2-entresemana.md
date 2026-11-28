# Tabla de momios y valor esperado — Semana 2 entre semana (Football AI Agenda)

**Partidos:** 2026-11-24 al 2026-11-26, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-28.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2-entresemana.md) × momio decimal − 1. Probabilidades calibradas (28 nov 2026): se encogen hacia las tasas base reales (α=0.35) antes de calcular el EV; la probabilidad cruda queda en prob_cruda de ev.json. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS: probabilidad Poisson completa (ambos anotan); el EV se calcula solo con momio BSD (llave 'bsd' en momios.json); sin esa llave no lleva EV porque ESPN/DraftKings no trae momio de BTTS en esta fuente.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | P(BTTS) | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 11/24 nov | Galatasaray vs Aston Villa | 2.85 / 4.00 / 2.25 | -2.9% / +3.2% / -9.7% | 3.5 (1.95 / 1.87) | +31.0% / -38.5% | +0.5 (1.62 / 2.15) | -39.9% / +35.5% | 62.7% | Spread visitante -0.5 | +35.5% | 🟢 Verde |
| 11/24 nov | Arsenal vs Borussia Dortmund | 1.42 / 4.90 / 7.50 | -33.5% / +48.4% / +70.6% | 2.5 (1.61 / 2.35) | -22.4% / +21.4% | -1.5 (2.05 / 1.67) | -29.4% / +9.3% | 47.5% | Visita | +70.6% | 🟢 Verde |
| 11/24 nov | Manchester City vs Napoli | 1.29 / 6.50 / 9.00 | -24.6% / +47.3% / +68.2% | 3.5 (1.80 / 2.00) | +44.4% / -60.5% | -1.5 (1.67 / 2.05) | -13.6% / -1.3% | 60.0% | Visita | +68.2% | 🟢 Verde |
| 11/24 nov | Real Madrid vs PSV Eindhoven | 1.17 / 9.00 / 12.00 | -41.0% / +153.8% / +155.1% | 4.5 (2.00 / 1.80) | -83.1% / +64.8% | -2.5 (1.91 / 1.77) | -40.5% / +21.8% | 48.9% | Visita | +155.1% | 🟢 Verde |
| 11/25 nov | Club Brugge vs Liverpool | 4.50 / 4.70 / 1.62 | +113.9% / +20.1% / -56.3% | 3.5 (1.74 / 2.05) | +52.8% / -75.0% | +0.5 (2.25 / 1.59) | +13.0% / -20.9% | 68.0% | Local | +113.9% | 🟢 Verde |
| 11/25 nov | Internazionale vs VfB Stuttgart | 1.42 / 5.50 / 6.00 | -44.4% / +66.9% / +82.3% | 3.5 (1.65 / 2.25) | -69.5% / +83.3% | -1.5 (1.91 / 1.80) | -43.5% / +26.8% | 51.9% | Menos 3.5 | +83.3% | 🟢 Verde |
| 11/25 nov | Lille vs Bayern Munich | 5.25 / 4.20 / 1.61 | +53.2% / -2.0% / -23.7% | 2.5 (1.77 / 2.05) | +14.1% / -27.2% | +0.5 (2.30 / 1.56) | -31.8% / +9.4% | 52.6% | Local | +53.2% | 🟢 Verde |
| 11/25 nov | Paris Saint-Germain vs AS Roma | 1.44 / 5.00 / 6.50 | -13.7% / +9.8% / +18.7% | 3.5 (1.80 / 2.00) | +62.1% / -80.1% | -1.5 (2.05 / 1.69) | +10.9% / -22.4% | 62.3% | Más 3.5 | +62.1% | 🟢 Verde |
| 11/25 nov | Sporting CP vs Manchester United | 2.55 / 3.75 / 2.60 | +29.4% / +1.6% / -42.4% | 3.5 (2.25 / 1.62) | -20.3% / +4.9% | -0.5 (2.40 / 1.51) | +15.5% / -21.5% | 54.3% | Local | +29.4% | 🟢 Verde |
| 11/26 nov | Celta Vigo vs AFC Bournemouth | 3.85 / 3.55 / 2.00 | +9.8% / -17.2% / -3.7% | 2.5 (2.00 / 1.80) | +19.2% / -27.3% | +0.5 (1.80 / 1.91) | -47.8% / +35.5% | 45.3% | AH visitante -0.5 | +41.4% | 🟢 Verde |
| 11/26 nov | Dinamo Zagreb vs Bayer Leverkusen | 5.00 / 4.40 / 1.62 | +47.6% / +29.6% / -33.3% | 3.5 (2.25 / 1.65) | -82.3% / +51.6% | +0.5 (2.25 / 1.56) | -18.7% / -0.6% | 41.0% | Menos 3.5 | +51.6% | 🟢 Verde |
| 11/26 nov | Olympiacos vs AC Milan | 2.85 / 3.30 / 2.55 | +40.5% / +4.5% / -51.5% | 2.5 (2.15 / 1.69) | -7.6% / -3.6% | +0.5 (1.51 / 2.40) | -12.1% / +0.5% | 40.0% | Local | +40.5% | 🟢 Verde |
| 11/25 nov | Toluca vs Atlas | 1.44 / 4.80 / 6.00 | -24.1% / +18.7% / +36.5% | 2.5 (1.56 / 2.35) | +9.9% / -31.0% | -1.5 (2.10 / 1.65) | -7.0% / -8.3% | 66.1% | Visita | +36.5% | 🟢 Verde |
| 11/25 nov | Monterrey vs América | 2.25 / 3.30 / 3.15 | -6.6% / -3.2% / -8.2% | 2.5 (1.87 / 1.87) | +3.4% / -16.4% | -0.5 (2.15 / 1.62) | -16.4% / -0.7% | 55.1% | Más 2.5 | +3.4% | 🟡 Amarillo |
| 11/26 nov | Pachuca vs Guadalajara | 2.95 / 3.20 / 2.45 | +22.2% / +0.3% / -33.2% | 2.5 (1.95 / 1.80) | -5.9% / -6.7% | +0.5 (1.54 / 2.35) | -23.1% / +17.8% | 49.2% | Local | +22.2% | 🟢 Verde |
| 11/26 nov | León vs Cruz Azul | 3.20 / 3.60 / 2.15 | +26.6% / +6.5% / -33.6% | 2.5 (1.71 / 2.05) | -7.0% / -6.2% | +0.5 (1.69 / 2.05) | -21.8% / +10.2% | 54.3% | Local | +26.6% | 🟢 Verde |
| 11/25 nov | Sabah FK vs Barcelona | 23.00 / 14.00 / 1.07 | +566.3% / +217.4% / -48.2% | 4.5 (1.91 / 1.87) | -4.6% / -6.4% | +3.5 (1.59 / 2.20) | -26.8% / +18.7% | 55.0% | Local | +566.3% | 🟢 Verde |
| 11/25 nov | Slavia Prague vs Villarreal | 3.15 / 3.90 / 2.10 | +38.3% / +5.7% / -39.1% | 3.5 (2.30 / 1.62) | +43.8% / -39.1% | +0.5 (1.71 / 2.00) | -17.4% / +3.7% | 63.5% | Más 3.5 | +43.8% | 🟢 Verde |
| 11/25 nov | Atlético Madrid vs Viking FK | 1.11 / 10.50 / 20.00 | -54.2% / +210.0% / +484.8% | 3.5 (1.67 / 2.20) | -57.1% / +63.3% | -2.5 (1.80 / 1.91) | -50.9% / +38.9% | 54.5% | Visita | +484.8% | 🟢 Verde |
| 11/25 nov | Shakhtar Donetsk vs Fenerbahce | 2.95 / 3.55 / 2.35 | +40.0% / +5.0% / -46.0% | 2.5 (1.80 / 2.00) | -9.3% / -0.7% | +0.5 (1.59 / 2.20) | -14.0% / +0.9% | 49.2% | Local | +40.0% | 🟢 Verde |
| 11/26 nov | Besiktas vs Hapoel Be'er | 1.40 / 5.25 / 7.00 | -15.5% / +16.1% / +22.8% | 3.5 (2.10 / 1.74) | +15.3% / -21.5% | -1.5 (2.00 / 1.71) | +6.6% / -19.9% | 46.2% | Visita | +22.8% | 🟢 Verde |
| 11/26 nov | Marseille vs Levski Sofia | 1.39 / 5.00 / 8.00 | -57.3% / +62.4% / +194.6% | 2.5 (1.77 / 2.05) | -24.2% / +17.2% | -1.5 (2.05 / 1.69) | -47.9% / +26.0% | 41.1% | Visita | +194.6% | 🟢 Verde |
| 11/26 nov | RB Salzburg vs Ararat-Armenia | 1.18 / 8.00 / 13.00 | -48.7% / +127.9% / +265.6% | 3.5 (1.71 / 2.10) | -35.8% / +31.4% | -2.5 (2.20 / 1.61) | -37.1% / +14.7% | 57.7% | Visita | +265.6% | 🟢 Verde |
| 11/26 nov | Union St.-Gilloise vs Lech Poznan | 1.34 / 5.50 / 8.50 | -16.7% / +13.8% / +45.4% | 3.5 (2.30 / 1.61) | +70.1% / -58.2% | -1.5 (1.83 / 1.87) | +6.2% / -21.3% | 41.8% | Más 3.5 | +70.1% | 🟢 Verde |
| 11/26 nov | Viktoria Plzen vs Benfica | 5.50 / 4.50 / 1.56 | +54.5% / -2.6% / -21.8% | 2.5 (1.59 / 2.35) | +5.0% / -20.4% | +0.5 (2.35 / 1.53) | -36.9% / +11.6% | 46.7% | AH visitante -1.5 | +62.8% | 🟢 Verde |
| 11/26 nov | Crystal Palace vs Real Sociedad | 1.95 / 4.00 / 3.50 | -30.1% / +8.1% / +30.2% | 3.5 (2.25 / 1.65) | +19.1% / -22.6% | -0.5 (1.87 / 1.83) | -38.0% / +22.5% | 60.5% | Visita | +30.2% | 🟢 Verde |
| 11/26 nov | Ferencvaros vs NK Celje | 1.38 / 5.25 / 7.50 | -17.5% / +16.5% / +34.2% | 3.5 (2.25 / 1.65) | +54.0% / -48.1% | -1.5 (1.95 / 1.77) | +4.0% / -17.3% | 52.7% | Más 3.5 | +54.0% | 🟢 Verde |
| 11/26 nov | Juventus vs Omonia Nicosia | 1.20 / 7.00 / 14.00 | -33.9% / +72.5% / +184.0% | 2.5 (1.56 / 2.45) | +1.7% / -15.2% | -1.5 (1.59 / 2.20) | -27.0% / +18.8% | 57.9% | Visita | +184.0% | 🟢 Verde |
| 11/26 nov | Lyon vs Lillestrom | 1.25 / 6.50 / 11.00 | -31.4% / +65.6% / +116.1% | 3.5 (2.25 / 1.65) | -18.6% / +5.0% | -1.5 (1.69 / 2.05) | -25.1% / +14.2% | 50.8% | Visita | +116.1% | 🟢 Verde |
| 11/26 nov | NEC Nijmegen vs Stade Rennais | 3.00 / 3.90 / 2.20 | +7.7% / +13.5% / -23.0% | 3.5 (2.20 / 1.67) | -44.7% / +24.8% | +0.5 (1.67 / 2.05) | -29.8% / +18.6% | 53.4% | Menos 3.5 | +24.8% | 🟢 Verde |
| 11/26 nov | OFI Crete vs Anderlecht | 4.50 / 3.80 / 1.77 | +57.8% / +21.3% / -41.6% | 2.5 (1.80 / 2.00) | -17.3% / +8.1% | +0.5 (2.00 / 1.71) | -11.8% / -4.2% | 46.5% | Local | +57.8% | 🟢 Verde |
| 11/26 nov | Sparta Prague vs AZ Alkmaar | 2.60 / 3.60 / 2.60 | -10.0% / +1.4% / -3.3% | 2.5 (1.74 / 2.10) | -1.7% / -8.6% | -0.5 (2.45 / 1.49) | -21.6% / +1.2% | 54.5% | AH visitante -0.5 | +40.8% | 🟢 Verde |
| 11/26 nov | Sunderland vs Jagiellonia Bialystok | 1.27 / 5.75 / 11.00 | -44.3% / +79.6% / +174.4% | 2.5 (1.65 / 2.25) | -21.7% / +17.9% | -1.5 (1.74 / 1.95) | -44.4% / +32.8% | 48.1% | Visita | +174.4% | 🟢 Verde |
| 11/26 nov | Torreense vs Celtic | 4.50 / 4.40 / 1.69 | +110.0% / +14.7% / -53.9% | 3.5 (2.15 / 1.71) | +71.0% / -64.9% | +0.5 (2.15 / 1.62) | +7.2% / -18.6% | 66.5% | Local | +110.0% | 🟢 Verde |
| 11/26 nov | TSG Hoffenheim vs SK Sturm Graz | 1.29 / 6.50 / 9.00 | -40.5% / +92.3% / +117.1% | 3.5 (1.80 / 2.00) | -66.0% / +62.2% | -1.5 (1.69 / 2.05) | -41.7% / +34.3% | 50.8% | Visita | +117.1% | 🟢 Verde |

**Resumen:** 34 verdes, 1 amarillos, 0 rojos, 0 pendientes, 0 terminados sin momio.

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
