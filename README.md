# Football AI Agenda — Semana 1

La página (`index.html`) ya no muestra partidos de ejemplo: ahora muestra
**partidos reales verificados el 19 nov 2026**, del fin de semana del **20 al 22 de
noviembre de 2026**, con horas de Monterrey (CST).

## Fuentes de datos

- **football-data.org** — cubre sus 12 ligas (entre ellas Premier League, LaLiga,
  Serie A y Bundesliga).
- **API-Football** — Liga MX y momios (plan gratuito).

## Alcance de la Semana 1

Solo **partidos (fixtures), resultados y tablas**. No hay momios, probabilidades
ni valor esperado inventados en la página.

- **Semana 2:** probabilidades (modelo Poisson).
- **Semana 3:** momios y valor esperado (EV).
- **Semana 4:** parlay y picks guardados.

## Partidos incluidos (16)

### Viernes 20 nov — 5 partidos

- 13:30 — Bayern München vs 1. FC Köln (Bundesliga)
- 14:00 — Athletic Club vs Espanyol (LaLiga)
- 19:00 — Puebla vs Atlético San Luis (Liga MX)
- 21:00 — FC Juárez vs Atlas (Liga MX)
- 21:10 — Tijuana vs Atlante (Liga MX)

### Sábado 21 nov — 6 partidos

- 06:30 — Man City vs Fulham (Premier League)
- 11:30 — Newcastle vs Arsenal (Premier League)
- 11:30 — Sevilla vs Real Betis (LaLiga)
- 14:00 — Real Madrid vs Celta Vigo (LaLiga)
- 16:50 — Pachuca vs Toluca (Liga MX)
- 19:00 — Pumas vs Monterrey (Liga MX)

### Domingo 22 nov — 5 partidos

- 07:00 — Barcelona vs Villarreal (LaLiga)
- 10:30 — Liverpool vs Man Utd (Premier League)
- 13:45 — Atalanta vs Inter (Serie A)
- 14:00 — Getafe vs Atlético Madrid (LaLiga)
- 17:07 — Chivas vs Cruz Azul (Liga MX)

Por liga: Liga MX 6, LaLiga 5, Premier League 3, Serie A 1, Bundesliga 1.

## Tablas (al 18 nov 2026)

- Liga MX Apertura: Cruz Azul líder, 32 pts en 16 partidos, 2 puntos sobre América.
- Brasileirão: Flamengo 1º 76 pts, Palmeiras 2º 73, Cruzeiro 3º 60 (antes de la
  jornada 35).

## Seguridad: sin claves en el repo

**No hay API keys en el repositorio ni en `index.html`.** Las claves nunca deben
hacerse commit: los datos se consultan en privado y se publican ya integrados
(`baked`) en `index.html`, sin tokens ni credenciales.
