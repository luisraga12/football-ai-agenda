# Investigación Fuerza del XI — prueba con datos reales (23 nov 2026)

## Qué endpoint da qué (ESPN, API pública, sin clave)

| Dato | Endpoint | ¿Lo da? |
|---|---|---|
| Plantilla del equipo | `GET /{liga}/teams/{id}/roster` | Sí: 31 jugadores Arsenal, 36 Real Madrid, temp. 2026-27. Por jugador: posición, dorsal, edad. |
| Goles y asistencias de temporada por jugador | Mismo roster: `athlete.statistics.splits.categories` (offensive: `totalGoals`, `goalAssists`, `totalShots`, `shotsOnTarget`; general: `appearances`, `subIns`) | Sí. Ej.: Mbappé 13 goles + 3 asist. en 13 partidos; Saka 3 + 0 en 7; Rice 0 + 5 en 11. |
| Minutos jugados de temporada por jugador | — | **NO. Ningún endpoint de ESPN da `minutesPlayed`**: ni el roster ni el summary por partido lo traen (inventario completo de nombres de stats verificado). |
| Minutos por partido (estimados) | `GET /{liga}/summary?event={id}` → `keyEvents` tipo `Substitution` (minuto + quién entra por quién) | Sí, exactos salvo el descuento: titular no sustituido = 90'; titular sustituido al M = M; suplente que entra al M = 90−M. Ej.: Saka salió al 68' vs Coventry (68 min); Madueke entró al 68' (22 min). |
| Titulares + resultado por partido | `GET /{liga}/summary?event={id}` → `rosters[]` (`starter: true/false`, `formationPlace`) + `header.competitions[0]` (marcador, `completed`) | Sí. También `boxscore.teams[].statistics` (posesión, tiros, etc.) pero `boxscore.players` viene vacío: no hay stats por jugador ahí. |
| Puntos con el jugador en cancha | Derivado: 3/1/0 por partido para cada titular del summary | Sí, calculado. Ej.: Arsenal 13 pts en sus últimos 5 (4V 1E); Real Madrid 15 pts (5V). |
| Alineación probable (antes del partido) | — | **NO.** ESPN solo publica el XI cuando sale (~1 h antes). La Semana 6 (alineación probable) tendrá que estimarla o esperar al XI oficial. |

Verificación de cordura: los XI de los summaries incluyen fichajes de verano 2026 (Konsa, Guimarães y Tzolis en el Arsenal; Konaté, Bernardo Silva, Diomande y Trent en el Real Madrid) y coinciden con el roster actual de cada equipo. No es un error de lectura.

## Fórmula exacta propuesta

Ventana: últimos 5 de liga por equipo (igual que el Poisson del proyecto).
La versión de temporada completa usa los mismos pasos con todos los
partidos de liga de la temporada.

**Mejor XI de la temporada (del equipo, en la ventana):** 1 portero + 4
defensas + 4 medios + 2 delanteros con MÁS MINUTOS jugados en la
ventana, por grupo de posición. (Alternativa, si el jefe la prefiere:
los 11 con más G+A de temporada; la de minutos es la que propongo
porque es la más estable y no depende de un partido con muchos goles.)

Para un XI cualquiera, cada componente en % contra el mejor XI:
- **A (goles):** Σ(goles+asistencias en la ventana del XI) / Σ(del mejor XI) × 100
- **B (minutos):** Σ(minutos del XI) / Σ(del mejor XI) × 100
- **C (puntos):** Σ(puntos con el jugador en cancha del XI) / Σ(del mejor XI) × 100

**Fuerza = 0.40·A + 0.30·B + 0.30·C** (0–100, cada componente topado en 100).
Pesos propuestos: el gol pesa más porque es lo que más mueve el
resultado; minutos y puntos pesan igual. El jefe decide los pesos.

## Números reales de prueba (últimos 5 de liga hasta 21 nov 2026)

| Equipo | XI del 21 nov | A | B | C | Fuerza |
|---|---|---|---|---|---|
| Arsenal (Newcastle 2–2 Arsenal) | Raya, Gabriel, Konsa, Calafiori, Timber, Ødegaard, Rice, Guimarães, Havertz, Eze, Madueke | 100 | 100 | 100 | **100.0** |
| Arsenal sin Ødegaard (suplente: Ben White) | mismo XI menos Ødegaard | 90.0 | 95.7 | 97.4 | **93.9** |
| Real Madrid (Madrid 2–1 Celta) | Courtois, Huijsen, Konaté, Camavinga, Carreras, Trent, Bellingham, Bernardo Silva, Diomande, Güler, Mbappé | 89.5 | 83.5 | 85.7 | **86.5** |
| Real Madrid sin Mbappé (suplente: Cucurella) | mismo XI menos Mbappé | 52.6 | 81.5 | 83.7 | **70.6** |

Lectura: el Arsenal salió con el XI completo (100). El Madrid rotó
(Camavinga, Carreras, Trent en vez de los habituales) y quedó en 86.5.
Sin Mbappé el Madrid cae a 70.6 porque Mbappé lleva 7 G+A en la
ventana de 19 del equipo: el componente A se desploma a 52.6. Eso es
justo lo que el puntaje tiene que avisar antes de apostar.

Mejor XI por minutos (ventana): Arsenal G+A 10, 3 838 min, 115 pts;
Real Madrid G+A 19, 4 247 min, 147 pts. Detalle por jugador en
`fuerza_xi_prueba.json`.

## Qué falta para programarlo

1. Decisión del jefe: pesos (0.40/0.30/0.30 propuestos) y definición
   de mejor XI (por minutos, propuesta; o por G+A).
2. Ventana: últimos 5 (hecho) o temporada completa (mismo loop con
   todos los partidos: ~11 por equipo hoy, crece cada semana).
3. Fuente del XI del día: oficial de ESPN cuando se publique (~1 h
   antes) o probable de la Semana 6; hay que decidirlo antes de
   programar la Semana 8.
4. Trabajo estimado: 1 día (script `fuerza_xi.py` en el pipeline +
   tarjeta en el detalle del partido). Los datos ya existen: roster +
   summary, sin endpoint nuevo.
