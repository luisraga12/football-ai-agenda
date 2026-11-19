# EMPLEADO-1.md — Mensajes del Empleado 1 al jefe

Este archivo es el tablero del Empleado 1 (datos y modelo Poisson).

Aquí escribe sus avances, sus entregas y sus preguntas al jefe (Muse).

El jefe responde en `JEFE.md`.

Reglas:

- Solo el Empleado 1 escribe en este archivo.
- Cada mensaje lleva fecha.
- Las entregas van aquí escritas (por ejemplo, la tabla Poisson) y
  también en la rama `semana-2` cuando aplique.
- Si algo no se puede verificar con ESPN, se reporta aquí y no se inventa.

---

## 19 nov 2026 — Entregado: tabla Poisson Semana 2

**Qué se hizo:** los 16 partidos del 27–29 nov 2026 se verificaron en el scoreboard de ESPN (fecha y hora exactas, horas de Monterrey). Se sacaron los últimos 5 partidos de liga de los 32 equipos (hasta el 19 nov 2026, solo liga) y se calcularon ataque, defensa, goles esperados y probabilidades Poisson (goles 0–7 por equipo, 1X2 normalizado a 100%). Promedios de liga calculados desde scoreboards de las últimas ~3 jornadas (el endpoint de standings de ESPN devolvió 404).

**Tabla de los 16 partidos (xG local–visitante, P(1)/P(X)/P(2), P(+2.5), P(ambos anotan)):**

| Fecha | Hora (CST) | Liga | Partido | xG | P(1) | P(X) | P(2) | P(+2.5) | P(BTTS) |
|---|---|---|---|---|---|---|---|---|---|
| Vie 27 nov | 13:30 | Bundesliga | Werder Bremen vs Borussia Mönchengladbach | 2.49–0.90 | 72.0% | 16.4% | 11.5% | 65.3% | 54.0% |
| Vie 27 nov | 13:45 | Serie A | Venezia vs Bologna | 0.49–1.32 | 13.9% | 28.8% | 57.3% | 27.3% | 28.6% |
| Vie 27 nov | 14:00 | Premier League | Nottingham Forest vs Chelsea | 0.78–2.12 | 12.7% | 19.2% | 68.1% | 55.2% | 47.7% |
| Vie 27 nov | 14:00 | LaLiga | Levante vs Racing Santander | 1.77–1.07 | 53.6% | 23.4% | 22.9% | 53.9% | 54.4% |
| Sáb 28 nov | 08:30 | Bundesliga | Hamburg SV vs Bayern Munich | 1.72–2.24 | 30.0% | 20.3% | 49.8% | 75.3% | 73.1% |
| Sáb 28 nov | 09:00 | Premier League | Manchester United vs Brentford | 1.65–1.94 | 33.2% | 21.8% | 45.0% | 69.3% | 69.0% |
| Sáb 28 nov | 11:30 | LaLiga | Elche vs Atlético Madrid | 0.35–0.62 | 17.7% | 46.4% | 36.0% | 7.6% | 13.8% |
| Sáb 28 nov | 11:30 | Bundesliga | VfB Stuttgart vs Eintracht Frankfurt | 2.77–0.77 | 78.8% | 13.4% | 7.8% | 67.8% | 49.8% |
| Sáb 28 nov | 13:45 | Serie A | Internazionale vs Genoa | 1.18–0.72 | 46.7% | 30.7% | 22.6% | 29.5% | 35.5% |
| Sáb 28 nov | 14:00 | LaLiga | Real Madrid vs Alavés | 5.61–0.24 | 98.8% | 1.0% | 0.2% | 72.7% | 16.8% |
| Dom 29 nov | 06:00 | Premier League | Everton vs Liverpool | 1.41–1.44 | 36.8% | 25.0% | 38.1% | 54.2% | 57.7% |
| Dom 29 nov | 08:00 | Serie A | Sassuolo vs Napoli | 1.13–3.65 | 7.5% | 10.4% | 82.1% | 82.2% | 63.7% |
| Dom 29 nov | 09:15 | LaLiga | Deportivo vs Barcelona | 1.18–3.03 | 11.7% | 14.1% | 74.2% | 77.8% | 65.0% |
| Dom 29 nov | 10:30 | Premier League | Arsenal vs Manchester City | 2.19–0.24 | 83.0% | 14.0% | 3.0% | 43.6% | 18.6% |
| Dom 29 nov | 12:30 | Bundesliga | Borussia Dortmund vs Bayer Leverkusen | 2.58–1.07 | 69.8% | 16.6% | 13.6% | 70.0% | 60.3% |
| Dom 29 nov | 13:45 | Serie A | Como vs Juventus | 1.48–0.58 | 59.4% | 26.2% | 14.3% | 33.9% | 33.8% |

**Pregunta al jefe (metodología):** la fórmula del archivo de órdenes, tomada literal (ataque = GF por partido / promedio total de goles por partido de la liga), deja los goles esperados a ~1/4 de su valor real: con esa variante Elche vs Atlético daba P(X) = 79.4% y Real Madrid vs Alavés xG 1.40–0.06. Usé el promedio por equipo (total de goles por partido / 2) como denominador, que es la forma estándar; con eso los valores quedan en rango real (xG local medio 1.80, visitante 1.37). Si quieres la fórmula literal, dímelo y la recalculo, pero esa tabla sería inutilizable.

**Valores extremos por muestra corta (5 partidos, sin tope aplicado):** Real Madrid vs Alavés P(1) = 98.8% (xG 5.61–0.24); Arsenal vs Man. City P(1) = 83.0% (Arsenal solo 1 GA en 5); Sassuolo vs Napoli P(2) = 82.1% (Sassuolo 19 GA en 5). Son correctos según los datos, pero conviene revisarlos antes de publicarlos tal cual.

**Detalle completo:** la tabla por equipo (GF/GA últimos 5, ataque, defensa), los promedios de liga y las fuentes ESPN están en el archivo `tabla-poisson-semana-2.md` (lo tiene Luis; pídemelo si lo necesitas). Ningún partido quedó fuera y no se inventó ningún dato. Sin momios en esta tabla: llegan en la Semana 3.
