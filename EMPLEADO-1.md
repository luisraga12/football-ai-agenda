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

---

## 19 nov 2026 — Recibido: corrección del BTTS

Leí la corrección del jefe y tienes razón: el BTTS lo calculé sobre la tabla truncada de 0–7 goles sin renormalizar, por eso salía bajo (Real Madrid–Alavés 16.8% en vez de 21.1%). Para la próxima semana lo calculo con la distribución completa, igual que el +2.5. Gracias por verificar los datos, qué bueno que el resto salió exacto.

---

## 19 nov 2026 — Propuesta: automatizar mi parte (datos y Poisson)

Leí la meta de automatización total del jefe. Mi parte (bajar los últimos 5 partidos de ESPN y calcular la tabla Poisson) ya está semi-automatizada: tengo scripts que hacen la recolección de ESPN, el cálculo Poisson y la escritura de la tabla. Propongo que esos scripts se suban al repo y se corran solos con GitHub Actions (Semana 7), para que la tabla se genere sin hacerlo a mano cada semana. Antes de eso hay que aplicarles la corrección del BTTS (distribución completa) y validar que los 16 partidos de la semana existan en ESPN antes de calcular. Los scripts los tiene Luis; si el jefe quiere, los paso para revisarlos.


---

## 20 nov 2026 — Entregado: automatización de datos y Poisson (Semana 1)

**Qué se automatizó:** los tres pasos de mi trabajo ya corren solos con un solo comando (`python3 scripts/run_semana.py --config scripts/config/semana-actual.json`), sin tocar la interfaz:
1. `scripts/recolectar_datos.py` — descarga de ESPN los 16 partidos de la semana y los últimos 5 partidos de liga de los 32 equipos, y los promedios de cada liga. Antes de calcular, **valida que los 16 partidos existan en ESPN** (por ID de equipo); si falta uno, falla y no se calcula nada.
2. `scripts/calcular_poisson.py` — ataque, defensa, xG y probabilidades 1X2, +2.5 y BTTS, con el BTTS ya corregido a la **distribución completa** (rejilla 0–20 goles, `scripts/poisson_core.py`).
3. `scripts/generar_tabla.py` — escribe `data/semana-N/tabla-poisson-semana-N.md` con la tabla de partidos, la tabla por equipo, los promedios de liga y las fuentes.
Además, `.github/workflows/actualizar-poisson.yml` corre todo solo: diario a las 13:00 UTC y cada hora viernes, sábado y domingo (días de partido), y hace commit de `data/` si algo cambió. Solo usa `GITHUB_TOKEN`; no hay claves: ESPN es API pública.

**Dónde quedó (rama `semana-2`, para tu revisión):** `scripts/` (los 5 scripts + README + `config/semana-1.json`, `semana-2.json` y `semana-actual.json`), `.github/workflows/actualizar-poisson.yml`, `data/semana-1/tabla-poisson-semana-1.md` y `data/semana-2/tabla-poisson-semana-2.md` (corregida, ver abajo). No toqué `index.html`.

**Prueba con datos reales de ESPN (hoy, 20 nov):**
- Semana 1: 16/16 partidos verificados en ESPN (Premier, LaLiga, Bundesliga, Serie A y Liga MX, 20–22 nov), 32 equipos con 5 partidos cada uno. La tabla reproducida coincide EXACTA con los valores que aprobaste para la Semana 1: Real Madrid P(1) 83.8%, Newcastle P(1) 3.8% de local, Sevilla–Betis +2.5 91.0%.
- Semana 2 (re-corrida con el BTTS corregido): los 16 BTTS coinciden con tus valores corregidos (desviación máxima 0.07 puntos, redondeo). El 1X2 apenas cambia (máx. 0.6 puntos).

**Hallazgo que necesita tu decisión — el +2.5 también estaba truncado:** al pasar a la distribución completa vi que el +2.5 publicado de la Semana 2 también se calculó sobre la tabla de 0–7 goles, no con la distribución completa como se dio por hecho. Los valores correctos son: Real Madrid–Alavés 93.1% (publicado 72.7%), Sassuolo–Napoli 85.5% (82.2%), Deportivo–Barcelona 79.1% (77.8%), Werder 65.7% (65.3%), Forest 55.4% (55.2%), Hamburg 75.6% (75.3%), Man. United 69.5% (69.3%), Stuttgart 68.5% (67.8%), Everton 54.3% (54.2%), Arsenal 43.8% (43.6%), Dortmund 70.6% (70.0%); el resto igual. La tabla corregida ya está en `data/semana-2/tabla-poisson-semana-2.md`. ¿La republicamos con estos +2.5 corregidos, o la dejamos como está?

**Qué falta / necesita revisión del jefe:**
- Revisar los scripts y el workflow en la rama `semana-2`.
- Decidir lo del +2.5 de la Semana 2 (arriba).
- Fusionar a `main`: los workflows programados de GitHub Actions solo corren en la rama por defecto, así que la actualización automática no empieza hasta que se fusione. Mientras tanto el workflow se puede correr a mano (`workflow_dispatch`).
- Nada pendiente de Luis.

**Sin inventar nada:** todo salió de ESPN o calculado; ningún partido quedó fuera y no se usó ninguna clave.

---

## 22 nov 2026 — Entregado: momios + EV automáticos (Semana 3) y Poisson 4–6 dic

Jefe, leí tus órdenes de la Semana 3 del 22 nov en `JEFE.md` y ya está hecho, en la rama `semana-3` (sin tocar `index.html`).

**1. Scripts de momios y EV:** `scripts/recolectar_momios.py` (DraftKings 1X2/total/spread de ESPN, valida los 16 partidos por ID, "pendiente" si no hay momio, Bet 365 solo etiquetado) y `scripts/calcular_ev.py` (EV = p × decimal − 1, P(over) para la línea publicada 2.5 o 3.5 con distribución completa, semáforo verde ≥ +5% / amarillo 0–+5% / rojo < 0%). En `poisson_core.py` añadí `p_over()` y `p_spread_cover()` (rejilla 0–20). Todo corrido de verdad con `python3`, no solo a ojo: `python3 scripts/run_semana.py --config scripts/config/semana-2.json` terminó en `OK — Semana 2 completa y validada (15 verdes, 0 amarillos, 1 rojos, 0 pendientes)`.

**Verificación contra tu tabla manual:** 15 verdes, 1 rojo, como dices. El Poisson de la Semana 2 se reprodujo EXACTO (la tabla `tabla-poisson-semana-2.md` no cambió). Los momios decimales coinciden casi exactos; Venezia se movió un poco en vivo (1X2 3.30/3.15/2.10 en vez de 3.35/3.20/2.05; total 2.00/1.77 en vez de 1.95/1.80) y su EV de Menos 2.5 quedó en +28.6% (tuyo +31.0%). Deportivo–Barcelona sigue en rojo, mejor EV −0.3% (Más 3.5). Hamburg–Bayern solo Bet 365 (8.50/6.00/1.25, sin total ni spread porque Bet 365 no los trae en ese formato; lo soporté aparte en el script).

| Partido | Mejor pick | EV | Semáforo |
|---|---|---|---|
| Werder Bremen vs Gladbach | Local | +21.9% | 🟢 |
| Venezia vs Bologna | Menos 2.5 | +28.6% | 🟢 |
| Nottm Forest vs Chelsea | Visita | +67.0% | 🟢 |
| Levante vs Racing | Menos 3.5 | +11.1% | 🟢 |
| Hamburg vs Bayern (Bet 365) | Local | +154.5% | 🟢 |
| Man Utd vs Brentford | Visita | +53.2% | 🟢 |
| Elche vs Atlético | Empate | +104.1% | 🟢 |
| Stuttgart vs Frankfurt | Local | +33.4% | 🟢 |
| Inter vs Genoa | Visita | +80.6% | 🟢 |
| Real Madrid vs Alavés | Spread local -2.5 | +87.2% | 🟢 |
| Everton vs Liverpool | Local | +27.1% | 🟢 |
| Sassuolo vs Napoli | Más 3.5 | +61.5% | 🟢 |
| Deportivo vs Barcelona | Más 3.5 | −0.3% | 🔴 |
| Arsenal vs Man City | Local | +62.2% | 🟢 |
| Dortmund vs Leverkusen | Local | +43.4% | 🟢 |
| Como vs Juventus | Menos 2.5 | +29.0% | 🟢 |

La tabla completa (con 1X2, total, spread y EV por mercado) está en `data/semana-2/tabla-momios-semana-2.md`, regenerada por el script (ahora incluye las columnas de spread).

**Pregunta — el mejor pick puede ser spread:** en Real Madrid–Alavés mi mejor pick es el Spread local −2.5 (+87.2%), no el Más 3.5 (+53.0%): tu tabla no traía spread y la orden pedía incluirlo. Con xG 5.61–0.24 el P(local gana por 3+) es ~89%, así que el spread gana. El Más 3.5 sigue en +53.0%, igual que el tuyo. ¿El mejor pick puede ser spread, o solo 1X2/total? No lo cambio hasta que me digas.

**2. Automatización:** `run_semana.py` ya corre los 5 pasos (datos, Poisson, tabla, momios, EV) con validación (cada partido con momio tiene EV y semáforo; ningún partido pendiente tiene EV inventado), y el workflow quedó actualizado (nombre nuevo "Actualizar datos, Poisson, momios y EV", YAML validado con parser). Solo usa `GITHUB_TOKEN`, sin secretos. Los pasos no cambiaron en el workflow porque ya llama a `run_semana.py`.

**3. Mecanismo para la página (propuesta, no tocado):** `scripts/integrar_pagina.py` genera `data/semana-N/ev.json` e inyecta un fragmento entre `<!-- MOMIOS-INICIO -->` / `<!-- MOMIOS-FIN -->`; si el HTML no tiene los marcadores, falla sin tocar nada (probado: con el `index.html` real falla como debe, intacto en git; con una copia con marcadores inyecta bien con `--apply`). Por defecto es dry-run. Dime si pones los marcadores tú una vez, o si prefieres que la página lea `ev.json` con `fetch()` (Semana 7, cambia la arquitectura actual de datos integrados). No toco `index.html` hasta que me lo digas.

**4. Semana 3 (4–6 dic):** Poisson calculado y validado (16/16, 32 equipos con 5 partidos cada uno, cutoff 22 nov). **Sin Liga MX:** revisé los scoreboards de ESPN del 4, 5 y 6 dic y `mex.1` no tiene ningún partido esos días, por eso va solo con las 4 ligas europeas, 4 partidos por liga. Tabla en `data/semana-3/tabla-poisson-semana-3.md`, config en `scripts/config/semana-3.json`.

| Fecha | Partido | xG | P(1) / P(X) / P(2) | P(+2.5) | P(BTTS) |
|---|---|---|---|---|---|
| Vie 4 dic 13:30 | Bayern vs Paderborn | 3.40–0.71 | 87.0 / 8.7 / 4.3% | 77.8% | 49.1% |
| Vie 4 dic 13:45 | Bologna vs Roma | 2.42–2.47 | 39.8 / 18.6 / 41.7% | 86.6% | 83.4% |
| Sáb 5 dic 06:30 | Chelsea vs Liverpool | 0.56–2.18 | 8.1 / 17.1 / 74.8% | 51.5% | 37.9% |
| Sáb 5 dic 08:30 | Leverkusen vs Gladbach | 2.43–1.06 | 67.5 / 17.7 / 14.9% | 67.8% | 59.7% |
| Sáb 5 dic 11:30 | Villarreal vs Real Sociedad | 1.77–1.83 | 37.9 / 21.9 / 40.2% | 69.7% | 69.7% |
| Sáb 5 dic 13:45 | Napoli vs Lecce | 3.22–0.52 | 88.4 / 8.4 / 3.2% | 72.0% | 38.9% |
| Sáb 5 dic 14:00 | Brentford vs Man City | 2.01–1.19 | 56.4 / 21.5 / 22.1% | 61.9% | 60.2% |
| Sáb 5 dic 14:00 | Barcelona vs Celta | 3.77–0.80 | 88.6 / 7.5 / 3.9% | 83.4% | 53.7% |
| Sáb 5 dic 11:30 | Frankfurt vs Werder | 1.06–1.04 | 35.6 / 29.9 / 34.4% | 35.1% | 42.3% |
| Dom 6 dic 14:00 | Atlético vs Betis | 2.07–0.47 | 75.2 / 17.6 / 7.1% | 46.5% | 32.5% |
| Dom 6 dic 08:30 | Schalke vs Dortmund | 0.09–0.71 | 4.4 / 47.9 / 47.7% | 4.7% | 4.4% |
| Dom 6 dic 08:00 | Newcastle vs Sunderland | 0.93–0.28 | 50.9 / 38.1 / 11.0% | 12.3% | 14.9% |
| Dom 6 dic 10:30 | Tottenham vs Arsenal | 0.67–0.40 | 36.9 / 44.2 / 18.9% | 9.3% | 15.9% |
| Dom 6 dic 11:00 | Juventus vs Udinese | 2.75–0.40 | 86.2 / 10.4 / 3.4% | 60.8% | 30.6% |
| Dom 6 dic 09:15 | Athletic vs Real Madrid | 0.89–2.79 | 9.2 / 13.9 / 76.9% | 71.1% | 55.2% |
| Dom 6 dic 13:45 | Milan vs Parma | 3.46–1.04 | 82.3 / 10.5 / 7.3% | 82.7% | 62.6% |

Valores extremos (muestra de 5, sin tope): Schalke xG local 0.09 (solo 1 GF en 5) y Dortmund 47.7% de visita con empate 47.9% — el modelo casi no ve goles en ese partido; Tottenham–Arsenal también sale bajo en goles (xG 0.67–0.40) porque el Tottenham solo encajó 2 en 5. Son correctos según los datos, pero conviene la nota de cautela en la página, como en la Semana 2.

Momios Semana 3 (hoy, 22 nov): solo 4 con momio, los de Serie A con Bet 365 (Bologna Local +51.1% 🟢, Napoli Local +17.8% 🟢, Juventus Local +19.0% 🟢, Milan Local +4.5% 🟡, primer amarillo del proyecto); los otros 12 pendientes porque DraftKings aún no los publica — el workflow diario los llenará solo cuando aparezcan en ESPN. Detalle cosmético: en la tabla de la Semana 3, Frankfurt–Werder (sáb 11:30) sale después de los partidos de las 14:00 porque la config se ordenó por fecha, no por hora.

**Pendiente de ti, jefe:** (a) ¿el mejor pick puede ser spread? (b) mecanismo de integración: marcadores `MOMIOS-INICIO`/`FIN` o `fetch()` de `ev.json`. (c) ¿Cuándo apunto `semana-actual.json` a la Semana 2? Sigue apuntando a la Semana 1, no lo toqué; tú decides.

**Sin inventar nada:** todo salió de ESPN o calculado; ningún partido quedó fuera, ningún momio inventado (12 pendientes en la Semana 3) y no se usó ninguna clave.

---

## 22 nov 2026 — Entregado: datos entre semana 24–26 nov (Champions + Europa League)

Jefe, leí tus órdenes entre semana y el añadido del descubrimiento automático en `JEFE.md`, y ya está hecho, en la rama `semana-3` (sin tocar `index.html` ni `semana-actual.json`).

**0. Sincronización:** la rama local estaba en `e1418ce` con mi trabajo anterior sin confirmar; lo comparé byte a byte con el remoto y era idéntico a lo subido, así que hice reset a `origin/semana-3` (`67c4825`) y fusioné `main` (`1d6a2ea`, tus órdenes entre semana + descubrimiento). Hubo un conflicto en `EMPLEADO-2.md` (tu versión de main traía la sección "Archivo pasado al jefe" y la rama las dos secciones nuevas del Empleado 2): conservé las tres secciones en orden cronológico, no se perdió ningún mensaje.

**1. Los 12 partidos elegidos (de 36, Champions 9+9 y Europa League 18):**

| Fecha | Hora (CST) | Partido |
|---|---|---|
| Mar 24 nov | 11:45 | Galatasaray vs Aston Villa |
| Mar 24 nov | 14:00 | Arsenal vs Borussia Dortmund |
| Mar 24 nov | 14:00 | Manchester City vs Napoli |
| Mar 24 nov | 14:00 | Real Madrid vs PSV Eindhoven |
| Mié 25 nov | 14:00 | Club Brugge vs Liverpool |
| Mié 25 nov | 14:00 | Internazionale vs VfB Stuttgart |
| Mié 25 nov | 14:00 | Lille vs Bayern Munich |
| Mié 25 nov | 14:00 | Paris Saint-Germain vs AS Roma |
| Mié 25 nov | 14:00 | Sporting CP vs Manchester United |
| Jue 26 nov | 11:45 | Celta Vigo vs AFC Bournemouth |
| Jue 26 nov | 11:45 | Dinamo Zagreb vs Bayer Leverkusen |
| Jue 26 nov | 11:45 | Olympiacos vs AC Milan |

**Por qué estos 12:** equipos grandes que Luis sigue (Arsenal, Real Madrid, Man City, Liverpool, Bayern, PSG, Inter, Man Utd, Milan, Juventus era el 13º) y partidos parejos. Dejé fuera los más desparejos (Sabah–Barcelona, Juventus–Omonia) y los de equipos chicos (Bodo/Glimt–LASK, Slovan–Betis, Como–AEK, Slavia–Villarreal, Atlético–Viking, Shakhtar–Fenerbahce, Besiktas, Marseille, Salzburg, Union SG, Plzen–Benfica, Ferencvaros, Lyon, NEC–Rennes, OFI–Anderlecht, Sparta–AZ, Sunderland–Jagiellonia, Torreense–Celtic, Hoffenheim–Sturm, Feyenoord–Porto, Leipzig–Lens).

**2. Método — un cambio obligado que te reporto:** en Champions y Europa League solo se han jugado **4 jornadas** antes del cutoff (22 nov), así que no hay últimos 5: usé los **últimos 4** de cada equipo, con promedios por partido (GF/4, GA/4) en vez de GF/5. Los promedios son de LA COMPETICIÓN, como ordenaste: Champions 4.11 goles/partido (54 partidos, últimas 3 jornadas: 13-14 oct, 20-21 oct, 3-4 nov) y Europa League 2.97 (72 partidos, 16-17 sep, 15 oct, 22 oct, 4-5 nov). Tuve que arreglar `recolectar_datos.py`: el calendario de ESPN para competiciones UEFA no trae fechas sino fases (dicts), así que las jornadas pasadas ahora se sacan de los schedules ya descargados. La validación acepta n>=4 (avisa) y falla si n<4. Todo corrido de verdad con `python3 scripts/run_semana.py`: `OK — Semana 2-entresemana completa y validada: 12 partidos, 24 equipos (12 verdes, 0 amarillos, 0 rojos, 0 pendientes)`.

**Tabla Poisson (xG, 1X2, +2.5, BTTS):**

| Fecha | Partido | xG | P(1) / P(X) / P(2) | P(+2.5) | P(BTTS) |
|---|---|---|---|---|---|
| Mar 24 nov 11:45 | Galatasaray vs Aston Villa | 1.59–2.99 | 18.1 / 15.9 / 66.0% | 83.5% | 75.6% |
| Mar 24 nov 14:00 | Arsenal vs Borussia Dortmund | 1.33–0.58 | 55.0 / 28.7 / 16.3% | 29.8% | 32.4% |
| Mar 24 nov 14:00 | Manchester City vs Napoli | 4.38–1.16 | 88.4 / 6.9 / 4.7% | 91.4% | 67.8% |
| Mar 24 nov 14:00 | Real Madrid vs PSV Eindhoven | 1.72–0.58 | 65.2 / 22.8 / 12.0% | 40.5% | 36.2% |
| Mié 25 nov 14:00 | Club Brugge vs Liverpool | 3.65–2.71 | 56.6 / 15.2 / 28.2% | 95.2% | 90.9% |
| Mié 25 nov 14:00 | Internazionale vs VfB Stuttgart | 1.06–1.16 | 33.0 / 28.9 / 38.1% | 38.3% | 44.9% |
| Mié 25 nov 14:00 | Lille vs Bayern Munich | 0.66–3.32 | 4.2 / 8.9 / 87.0% | 75.9% | 46.7% |
| Mié 25 nov 14:00 | Paris Saint-Germain vs AS Roma | 5.30–1.38 | 91.6 / 4.9 / 3.5% | 96.3% | 74.6% |
| Mié 25 nov 14:00 | Sporting CP vs Manchester United | 2.12–0.89 | 65.8 / 19.6 / 14.6% | 57.8% | 51.7% |
| Jue 26 nov 11:45 | Celta Vigo vs AFC Bournemouth | 0.32–2.88 | 2.4 / 8.8 / 88.8% | 62.1% | 26.1% |
| Jue 26 nov 11:45 | Dinamo Zagreb vs Bayer Leverkusen | 0.20–1.40 | 5.2 / 26.4 / 68.5% | 21.6% | 13.8% |
| Jue 26 nov 11:45 | Olympiacos vs AC Milan | 1.13–0.17 | 61.7 / 32.7 / 5.7% | 14.5% | 10.9% |

**Valores extremos (muestra de 4, sin tope):** PSG xG 5.30 (20 GF en 4), Man City 4.38, Club Brugge–Liverpool xG 3.65–2.71 con P(+2.5) 95.2%, y por el otro lado Celta 0.32 y Dinamo Zagreb 0.20. Son correctos según los datos, pero con solo 4 partidos la muestra exagera más que con 5: conviene la nota de cautela en la página, como en la Semana 2.

**3. Momios + EV (DraftKings, los 12 con momio, 0 pendientes):** 12 verdes, 0 amarillos, 0 rojos. Verifiqué el EV 1X2 local de los 12 a mano y el 1X2 suma 100% en los 12.

| Partido | Mejor pick | EV |
|---|---|---|
| Galatasaray vs Aston Villa | Visita | +55.1% 🟢 |
| Arsenal vs Borussia Dortmund | Menos 2.5 | +57.9% 🟢 |
| Manchester City vs Napoli | Más 3.5 | +53.2% 🟢 |
| Real Madrid vs PSV Eindhoven | Empate | +93.6% 🟢 |
| Club Brugge vs Liverpool | Local | +149.1% 🟢 |
| Internazionale vs VfB Stuttgart | Visita | +128.5% 🟢 |
| Lille vs Bayern Munich | Visita | +39.7% 🟢 |
| Paris Saint-Germain vs AS Roma | Más 3.5 | +65.1% 🟢 |
| Sporting CP vs Manchester United | Local | +64.5% 🟢 |
| Celta Vigo vs AFC Bournemouth | Visita | +73.4% 🟢 |
| Dinamo Zagreb vs Bayer Leverkusen | Menos 3.5 | +53.6% 🟢 |
| Olympiacos vs AC Milan | Menos 2.5 | +67.0% 🟢 |

Los EV tan altos (Brugge +149.1%, Inter–Stuttgart visita +128.5%) salen de que el modelo con 4 partidos discrepa fuerte del mercado: el mercado da a Liverpool favorito (1.65) y a Stuttgart casi parejo, mientras el modelo ve a Brugge con xG 3.65 y a Stuttgart con P(2) 38.1%. No es certeza, es desacuerdo modelo–mercado con muestra corta. Ojo: Real Madrid–PSV trae línea de total 4.5 (no 2.5/3.5); el P(over) se calculó para 4.5 con la distribución completa, como ordenaste.

**4. Conference League — ESPN no la trae:** probé 7 slugs (`uefa.europa-conference`, `uefa.conference-league`, `uefa.conference`, `uefa.uecl`, `uefa.conf`, `uefa.europa_conf`, `uefa.europa-conference-league`): todos HTTP 400, con y sin fecha. Por eso los 12 son solo Champions + Europa League. Si ESPN la publica con otro slug, el descubrimiento la intentará en cada corrida.

**5. Liga MX entre semana — no hay partidos:** revisé `mex.1` 24, 25 y 26 nov (0 eventos) y la línea base del descubrimiento cubre toda la semana 23–29 nov: tampoco hay ningún partido de Liga MX esa semana en ESPN. Por eso no se agregó nada por descubrimiento.

**6. Descubrimiento automático (`scripts/descubrir_partidos.py`, nuevo, paso 0 de `run_semana.py`):** consulta los scoreboards de las ligas del alcance (mex.1, eng.1, esp.1, ger.1, ita.1, uefa.champions, uefa.europa; Conference League se intenta pero no responde) para la semana corriente (lun–dom) y compara con la línea base en `data/semana-N/raw/descubrimiento_vistos.json`. Primera corrida: solo establece la línea base (75 partidos vistos esta semana: Champions 18, Europa League 18, Premier 11, LaLiga 10, Bundesliga 9, Serie A 9, Liga MX 0) y NO agrega nada, para no llenar una config curada con partidos que ya existían. En corridas posteriores, un partido nuevo se agrega al config y el pipeline completo corre para él; queda en el log del workflow. Solo ligas del alcance, Liguilla/playoffs incluidos cuando ESPN los publique, validación por team ID, nunca se inventa nada. No se guardan los ~56 scoreboards del descubrimiento, solo la línea base compacta. El workflow no cambia de horario (la corrida diaria de las 13:00 UTC alcanza) y sigue usando solo `GITHUB_TOKEN`.

**7. Pendientes de tu revisión, hechos:** (a) orden por fecha+hora en `generar_tabla.py` (y en `calcular_poisson.py`: los partidos se calculan ya ordenados) — la tabla entre semana sale Mar 24 11:45, luego 14:00, Mié 25, Jue 26; (b) `calcular_ev.py` blindado: si un partido trae total/spread pero no moneyline, el 1X2 queda sin EV en vez de romper en `ml['home']` (también blindado el print de `recolectar_momios.py`); (c) `raw/` incluido en esta entrega (3.6 MB en `data/semana-2-entresemana/raw/`, con scoreboards, schedules, `teams_last5.json`, `league_avgs.json`, `poisson_result.json`, `momios.json`, `ev_result.json` y `descubrimiento_vistos.json`). Los `raw/` de Semana 2 y Semana 3 también están en local por si los quieres subir.

**8. Pendiente, no hecho:** la vuelta al fragmento de integración (bloque completo de momios por tarjeta, marcadores por tarjeta y su CSS) — queda para la siguiente entrega, como dijiste que tú pones los marcadores cuando esté listo. No toqué `index.html`.

**Archivos en la rama semana-3:** `scripts/config/semana-2-entresemana.json`, `data/semana-2-entresemana/` (tabla-poisson, tabla-momios, `ev.json`, `raw/`), `scripts/descubrir_partidos.py` (nuevo), cambios en `poisson_core.py` (ataque/defensa con n), `calcular_poisson.py` (días 24–26 nov, orden fecha+hora, n), `recolectar_datos.py` (conteos generalizados, promedios UEFA desde schedules), `generar_tabla.py` (orden, conteos, ámbito, n), `calcular_ev.py` (días, blindaje moneyline), `recolectar_momios.py` (blindaje del print), `run_semana.py` (paso 0 descubrimiento, validación n>=4), `scripts/README.md`, `.github/workflows/actualizar-poisson.yml` (solo comentarios: paso 0 y n=4 en europeas; YAML validado con parser).

**Sin inventar nada:** todo salió de ESPN o calculado; ningún partido quedó fuera de los 12 curados (los otros 24 se excluyeron por curaduría, listados arriba) y ningún momio inventado (12/12 con momio DraftKings).
