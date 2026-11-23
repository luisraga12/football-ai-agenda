# Tabla de momios y valor esperado — Semana 2 (Football AI Agenda)

**Partidos:** 2026-11-27 al 2026-11-29, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo Hamburg–Bayern (Bet365, DraftKings no publicó ese partido en ESPN). **Fecha de consulta:** 2026-11-22. **Corrección 22 nov:** los EV se calculan con las probabilidades publicadas en la tabla Poisson (las que muestra la página), no con el recálculo desde xG.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-2.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (2.5 o 3.5, la publicada por DraftKings); el P(over) se calculó para esa línea desde los xG. BTTS no tiene momio en esta fuente, por eso no lleva EV.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|
| 11/27 nov | Bremen vs Gladbach | 1.69 / 4.10 / 3.85 | +22.0% / -32.8% / -55.7% | 3.5 (2.15 / 1.65) | -5.6% / -7.7% | Local | +22.0% | 🟢 Verde |
| 11/27 nov | Venezia vs Bologna | 3.35 / 3.20 / 2.05 | -53.4% / -7.8% / +17.5% | 2.5 (1.95 / 1.80) | -46.7% / +30.9% | Menos 2.5 | +30.9% | 🟢 Verde |
| 11/27 nov | Nottm Forest vs Chelsea | 2.75 / 3.50 / 2.45 | -65.1% / -32.8% / +66.8% | 2.5 (1.71 / 2.10) | -5.0% / -6.3% | Visita | +66.8% | 🟢 Verde |
| 11/27 nov | Levante vs Racing | 2.05 / 3.85 / 3.15 | +10.1% / -9.9% / -27.9% | 3.5 (2.25 / 1.62) | -28.7% / +11.0% | Menos 3.5 | +11.0% | 🟢 Verde |
| 11/28 nov | Hamburg vs Bayern | 8.50 / 6.00 / 1.25 | +154.2% / +21.2% / -37.8% | — (sin total) | — / — | Local | +154.2% | 🟢 Verde |
| 11/28 nov | Man Utd vs Brentford | 2.00 / 3.75 / 3.40 | -33.6% / -18.2% / +53.3% | 3.5 (2.35 / 1.56) | +13.5% / -19.6% | Visita | +53.3% | 🟢 Verde |
| 11/28 nov | Elche vs Atlético | 5.25 / 4.40 / 1.56 | -7.1% / +104.2% / -44.0% | 3.5 (2.35 / 1.57) | -96.0% / +54.5% | Empate | +104.2% | 🟢 Verde |
| 11/28 nov | Stuttgart vs Frankfurt | 1.69 / 4.40 / 3.70 | +33.5% / -41.5% / -71.5% | 3.5 (1.69 / 2.10) | -20.2% / +10.9% | Local | +33.5% | 🟢 Verde |
| 11/28 nov | Inter Milan vs Genoa | 1.29 / 5.00 / 8.00 | -39.6% / +53.5% / +80.8% | 2.5 (1.57 / 2.30) | -53.6% / +62.2% | Visita | +80.8% | 🟢 Verde |
| 11/28 nov | Real Madrid vs Alavés | 1.15 / 8.50 / 14.00 | +14.2% / -93.2% / -98.6% | 3.5 (1.83 / 1.91) | +53.1% / -68.5% | Más 3.5 | +53.1% | 🟢 Verde |
| 11/29 nov | Everton vs Liverpool | 3.45 / 3.60 / 2.05 | +27.0% / -10.0% / -21.7% | 2.5 (1.69 / 2.15) | -8.2% / -1.7% | Local | +27.0% | 🟢 Verde |
| 11/29 nov | Sassuolo vs Napoli | 4.30 / 4.10 / 1.62 | -68.6% / -59.0% / +34.4% | 3.5 (2.30 / 1.57) | +61.7% / -53.3% | Más 3.5 | +61.7% | 🟢 Verde |
| 11/29 nov | Deportivo vs Barcelona | 8.50 / 7.00 / 1.25 | -1.4% / -2.7% / -6.8% | 3.5 (1.65 / 2.20) | -0.3% / -13.3% | Más 3.5 | -0.3% | 🔴 Rojo |
| 11/29 nov | Arsenal vs Man City | 1.95 / 3.75 / 3.60 | +62.2% / -47.5% / -89.2% | 2.5 (1.71 / 2.10) | -24.9% / +18.0% | Local | +62.2% | 🟢 Verde |
| 11/29 nov | Dortmund vs Leverkusen | 2.05 / 3.80 / 2.95 | +43.5% / -37.3% / -60.2% | 3.5 (2.15 / 1.65) | +6.4% / -16.9% | Local | +43.5% | 🟢 Verde |
| 11/29 nov | Como vs Juventus | 2.05 / 3.40 / 3.20 | +21.8% / -10.9% / -54.2% | 2.5 (1.80 / 1.95) | -39.0% / +29.0% | Menos 2.5 | +29.0% | 🟢 Verde |

**Resumen:** 15 verdes, 0 amarillos, 1 rojos. Único sin valor: Deportivo–Barcelona (mejor EV −0.3%, Más 3.5).

**Advertencia:** el modelo Poisson usa solo los últimos 5 partidos por equipo y puede exagerar rachas; los EV extremos (p. ej. Hamburg local +154.2% con Bet365, Elche empate +104.2%) reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
