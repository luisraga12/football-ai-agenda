# Tabla de momios y valor esperado — Semana 3 (Football AI Agenda)

**Partidos:** 2026-12-04 al 2026-12-06, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-23.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-3.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (la publicada por DraftKings: 2.5, 3.5 o 4.5); el P(over) se calculó para esa línea desde los xG. BTTS no tiene momio en esta fuente, por eso no lleva EV.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 12/04 dic | Bayern Munich vs SC Paderborn 07 | 1.03 / 13.00 / 17.00 | -10.1% / +13.4% / -26.6% | 4.5 (1.83 / 1.87) | -28.0% / +13.5% | -3.5 (1.95 / 1.67) | -36.6% / +12.5% | Menos 4.5 | +13.5% | 🟢 Verde |
| 12/04 dic | Bologna vs AS Roma (Bet 365) | 3.80 / 3.60 / 1.85 | +51.1% / -33.2% / -22.9% | — | — | — | — | Local | +51.1% | 🟢 Verde |
| 12/05 dic | Chelsea vs Liverpool | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Bayer Leverkusen vs Borussia Mönchengladbach | 1.26 / 5.75 / 7.50 | -15.3% / +1.7% / +11.5% | 3.5 (1.71 / 2.00) | -20.8% / +7.6% | -1.5 (1.67 / 2.00) | -24.3% / +9.2% | Visita | +11.5% | 🟢 Verde |
| 12/05 dic | Villarreal vs Real Sociedad | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Napoli vs Lecce (Bet 365) | 1.33 / 4.50 / 8.50 | +17.8% / -62.3% / -72.4% | — | — | — | — | Local | +17.8% | 🟢 Verde |
| 12/05 dic | Brentford vs Manchester City | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Barcelona vs Celta Vigo | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Eintracht Frankfurt vs Werder Bremen | 2.00 / 3.75 / 2.95 | -28.7% / +12.2% / +1.6% | 3.5 (2.00 / 1.74) | -67.6% / +45.9% | -0.5 (1.95 / 1.69) | -30.4% / +8.7% | Menos 3.5 | +45.9% | 🟢 Verde |
| 12/06 dic | Atlético Madrid vs Real Betis | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Schalke 04 vs Borussia Dortmund | 4.10 / 3.75 / 1.69 | -81.9% / +79.6% / -19.4% | 2.5 (1.57 / 2.25) | -92.6% / +114.3% | +0.5 (2.00 / 1.65) | +4.6% / -21.5% | Menos 2.5 | +114.3% | 🟢 Verde |
| 12/06 dic | Newcastle United vs Sunderland | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Tottenham Hotspur vs Arsenal | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Juventus vs Udinese (Bet 365) | 1.36 / 4.75 / 8.50 | +17.6% / -50.4% / -71.4% | — | — | — | — | Local | +17.6% | 🟢 Verde |
| 12/06 dic | Athletic Club vs Real Madrid | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | AC Milan vs Parma (Bet 365) | 1.22 / 5.75 / 10.00 | +0.5% / -39.6% / -27.5% | — | — | — | — | Local | +0.5% | 🟡 Amarillo |

**Resumen:** 7 verdes, 1 amarillos, 0 rojos, 8 pendientes.

**Advertencia:** el modelo Poisson usa solo los últimos partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
