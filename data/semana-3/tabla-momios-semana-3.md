# Tabla de momios y valor esperado — Semana 3 (Football AI Agenda)

**Partidos:** 2026-12-04 al 2026-12-06, horas de Monterrey (CST). **Fuente de momios:** ESPN (API pública sin clave), DraftKings salvo que se indique otro proveedor. **Fecha de consulta:** 2026-11-23.

**Método:** EV = probabilidad Poisson (tabla-poisson-semana-3.md) × momio decimal − 1. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. La línea del total varía por partido (2.5 o 3.5, la publicada por DraftKings); el P(over) se calculó para esa línea desde los xG. BTTS no tiene momio en esta fuente, por eso no lleva EV.

| Fecha | Partido | 1X2 (decimal) | EV 1 / X / 2 | Total (línea) | EV Más / Menos | Spread (línea local) | EV Spread local / visitante | Mejor pick | EV | Semáforo |
|---|---|---|---|---|---|---|---|---|---|---|
| 12/04 dic | Bayern Munich vs SC Paderborn 07 | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/04 dic | Bologna vs AS Roma (Bet 365) | 3.80 / 3.60 / 1.85 | +51.1% / -33.2% / -22.9% | — | — | — | — | Local | +51.1% | 🟢 Verde |
| 12/05 dic | Chelsea vs Liverpool | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Bayer Leverkusen vs Borussia Mönchengladbach | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Villarreal vs Real Sociedad | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Napoli vs Lecce (Bet 365) | 1.33 / 4.50 / 8.50 | +17.8% / -62.3% / -72.4% | — | — | — | — | Local | +17.8% | 🟢 Verde |
| 12/05 dic | Brentford vs Manchester City | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Barcelona vs Celta Vigo | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/05 dic | Eintracht Frankfurt vs Werder Bremen | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Atlético Madrid vs Real Betis | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Schalke 04 vs Borussia Dortmund | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Newcastle United vs Sunderland | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Tottenham Hotspur vs Arsenal | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | Juventus vs Udinese (Bet 365) | 1.38 / 4.75 / 8.00 | +19.0% / -50.4% / -73.1% | — | — | — | — | Local | +19.0% | 🟢 Verde |
| 12/06 dic | Athletic Club vs Real Madrid | pendiente | — | — | — | — | — | — | — | ⏳ Pendiente |
| 12/06 dic | AC Milan vs Parma (Bet 365) | 1.27 / 5.25 / 9.00 | +4.5% / -44.9% / -34.7% | — | — | — | — | Local | +4.5% | 🟡 Amarillo |

**Resumen:** 3 verdes, 1 amarillos, 0 rojos, 12 pendientes.

**Advertencia:** el modelo Poisson usa solo los últimos 5 partidos por equipo y puede exagerar rachas; los EV extremos reflejan desacuerdo fuerte entre el modelo y el mercado, no una certeza.
