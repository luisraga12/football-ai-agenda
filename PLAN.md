# Plan semanal — Football AI Agenda

Qué se hace cada semana, en el mismo `index.html` del repo. Las semanas
terminadas están marcadas como hechas; el resto está pendiente.

**Meta del cliente:** que esta página quede tan bien que Luis la use en
lugar de 365Scores o OneFootball.

**Meta final: automatización total.** El cliente dejó claro (19 nov 2026)
que la página NO debe ser estática: todo debe estar automatizado — los
partidos, los momios, las probabilidades, las alineaciones y muchas cosas
más. La Semana 7 (GitHub Actions) es solo el primer paso: que la página
se actualice sola cada día. El objetivo final es automatizar todo el
flujo, no solo los partidos. Las actualizaciones manuales de cada semana
son solo el andamio mientras se construye: una vez entregado el
producto, nadie debe volver a meterle mano.

**Comunicación del equipo:** desde el 23 nov 2026 los mensajes del equipo
(`JEFE.md`, `EMPLEADO-1.md`, `EMPLEADO-2.md`) viven en el repo privado
[buzón](https://github.com/luisraga12/buzon), ya no en este repo. La forma
de trabajar está en
[`FORMA-DE-TRABAJAR.md` del buzón](https://github.com/luisraga12/buzon/blob/main/FORMA-DE-TRABAJAR.md).

## ✅ Semana 1 — Hecha (entregada 19 nov 2026, commit `4032d10`)

- 16 partidos reales del fin de semana 20–22 nov 2026, con horas de Monterrey.
- Fuente de partidos: API pública de ESPN, sin clave, con verificación cruzada.
- Filtros por liga y por estado, semáforo de valor, calculadora de EV con
  entrada manual y panel de parlay (vacío: aún no hay picks con momios).
- Sin momios, probabilidades ni estadísticas inventadas en la página.
- README actualizado con las fuentes reales (commit `28f44a5`).
- GitHub Pages activado: la página está en vivo en
  https://luisraga12.github.io/football-ai-agenda/
- Cuenta gratuita de API-Football creada y probada en vivo: el plan gratis
  solo abre las temporadas 2022 a 2024, no sirve para la 2026/27.
- Revisión de la Semana 1 (23 nov 2026, por el Empleado 1, verificada por
  el jefe contra ESPN en vivo): favorito 1X2 6/16, Más 2.5 5/10 cuando el
  modelo daba >50%, BTTS 3/6. Semana con 7 empates de 16; el modelo casi
  no caza el empate (talón del Poisson con solo 5 partidos). El EV del 1X2
  se lee con más cautela que el de totales.
- Momios de ESPN/DraftKings verificados en vivo para la Semana 3.
- Probabilidades Poisson de la Semana 1 añadidas 19 nov 2026 (a petición
  del cliente): 16 partidos del 20–22 nov con 1X2, +2.5 y BTTS, mismo
  método verificado que la Semana 2 y BTTS con distribución completa.

## ✅ Semana 2 — Hecha (entregada 19 nov 2026, adelantada)

- Modelo Poisson de probabilidades por partido (1X2, más de 2.5 goles y
  ambos anotan), calculado por el Empleado 1 con los últimos 5 partidos de
  liga por equipo (ESPN, 19 nov 2026) y revisado por el jefe.
- Probabilidades propias en cada tarjeta, sin momios inventados.
- 16 partidos del fin de semana 27–29 nov 2026, con horas de Monterrey.
  El Empleado 1 cambió Celta–Villarreal por Sassuolo–Napoli (cambio
  aprobado por el jefe).
- La fórmula de las órdenes se corrigió con la variante estándar
  (promedio por equipo como denominador); la fórmula literal dejaba los
  goles esperados a ~1/4 de su valor real.
- El BTTS de la tabla se corrigió en la integración (la tabla del
  Empleado 1 lo traía mal por truncar a 0–7 goles).
- Nota de cautela en la página: una muestra de 5 partidos puede exagerar
  rachas (Real Madrid 98.8%, Arsenal 83.0%, Napoli 82.1%).
- Esta semana el jefe cubrió el trabajo del Empleado 2 (interfaz).
- Publicación en vivo: lunes 23 nov 2026. La página muestra la Semana 1
  (20–22 nov) hasta el domingo 22, para no tapar los partidos de este fin
  de semana; la Semana 2 ya está hecha y solo falta ponerla en vivo.

## ⏳ Semana 3 — Pendiente

- Momios reales de ESPN/DraftKings por partido (1X2, over/under 2.5, handicap).
- Comparar probabilidad propia vs momio: valor esperado (EV) y semáforo
  de valor real (verde/amarillo/rojo).
- Actualizar los partidos con los de esa semana.
- Más mercados de apuestas: hoy la página muestra 6 (1X2, Over/Under,
  ambos anotan, córners, hándicap asiático y marcador exacto). Se agregan:
  **apuesta sin empate (DNB)** — Luis apuesta mucho a este mercado — y
  **doble oportunidad (1X, 12, X2)**. Los dos se derivan del 1X2, no
  necesitan otra fuente. Los momios de ambos anotan, córners y hándicap
  asiático necesitan una fuente extra además de ESPN (The Odds API o
  MoviOdds, por verificar en esta semana).
- **Avance 22 nov 2026 (jefe):** la interfaz de esta semana ya está
  hecha por el Empleado 2 y portada por el jefe a la página real de la
  Semana 2 (16 partidos): DNB y doble oportunidad derivados del 1X2 en
  cada tarjeta (verificados al decimal). El mismo 22 nov el jefe integró
  los momios reales (DraftKings vía ESPN, consultados ese día) + EV en
  las 16 tarjetas: 15 en verde, 1 en rojo (Deportivo–Barcelona, mejor EV
  −0.3%), parlay con botón solo en picks EV+; Hamburg–Bayern con Bet365
  (DraftKings no lo publicó en ESPN). Tabla en
  `data/semana-2/tabla-momios-semana-2.md`, vista previa en
  `preview-semana-2.html`. La Semana 2 sale en vivo el lunes 23 nov ya
  funcional. Al Empleado 1 le toca ahora automatizar momios + EV (órdenes
  en JEFE.md, 22 nov) para que no se haga a mano cada semana. Prueba del
  Empleado 2 (22 nov, rama semana-3): 2 bugs reales — los totales del
  parlay no se reseteaban al vaciarse y los filtros de día no filtraban —
  más los EV recalculados con las probabilidades publicadas (antes
  diferían hasta 0.8 puntos); corregidos por el jefe y verificados con
  0 errores, diferencia máxima 0.05 puntos. Automatización del
  Empleado 1 entregada 22 nov y verificada por el jefe (reproducción
  exacta, byte a byte): recolectar_momios.py + calcular_ev.py,
  workflow actualizado, Poisson Semana 3 (4–6 dic) listo, momios S3
  4/16 (el resto pendiente de DraftKings).
- **Semana 4** — parlay guardado en localStorage + vista «Mis picks
  guardados» (Empleado 2, 22 nov, adelantada): revisado por el jefe y
  portado a la base real de la Semana 2 — la página del lunes ya lo
  trae.
- **Alcance semanal completo** (decidido 22 nov 2026, a petición de
  Luis): la agenda ya no es solo de fin de semana — cubre también entre
  semana (Champions, Europa League, Conference League). Semana 2: entre
  semana mar 24 – jue 26 nov + fin de semana vie 27 – dom 29 nov.
  Incluye los partidos que se publican tarde: la Liga MX entre semana
  se agenda hasta que se acaba la jornada, así que el workflow debe
  detectar esos partidos solo cuando ESPN los publique y agregarlos sin
  que nadie edite el config a mano (descubrimiento automático, orden
  al Empleado 1 del 22 nov).
- **Entre semana** — sección lista en la página (Empleado 2, 22 nov,
  portada por el jefe) en estado pendiente: se llena con los 12
  partidos cuando el Empleado 1 entregue su tabla.
- **Entre semana lleno** (Empleado 1, 22 nov): 12 partidos Champions
  + Europa League con Poisson (últimos 4), momios DraftKings + EV (12
  verdes) y descubrimiento automático de partidos nuevos; integrados
  por el jefe en la página — el lunes sale con entre semana completo.
- **Semana 5** — detalle del partido (últimos 5, H2H, tabla, momios,
  alineación oficial cuando se publique): adelanto entregado por el
  Empleado 2 el lunes 23 nov y verificado por el jefe contra ESPN en
  vivo (últimos 5 y tabla exactos en los partidos revisados); preview
  en `preview-semana-5-detalle.html`. El port a la página real se hace
  en la Semana 5.
- **Semana 7** — fragmento de integración revisado (bloque completo
  por tarjeta + marcadores por partido + CSS): entregado por el
  Empleado 1 el lunes 23 nov, revisado y aprobado por el jefe
  (reproducción byte a byte, idempotente, falla seguro); sus `ev.json`
  traían momios del domingo, el jefe los regeneró con datos frescos
  de main. El workflow ya corre ambos configs (fin de semana + entre
  semana) en cada corrida — arreglo hecho por el jefe el 23 nov. El
  jefe pone los marcadores en la página cuando toque integrarlo.
- **Semana 8** — Fuerza del XI (como 365Scores, pedida por el cliente
  el lunes 23 nov con fotos): puntaje 0–100 por alineación, contra el
  mejor XI de la temporada del mismo equipo: goles aportados, minutos
  jugados y puntos con esos jugadores en cancha. Necesita la Semana 6
  (alineación probable) + estadísticas de jugadores de ESPN (el
  Empleado 1 verifica la fuente y propone la fórmula exacta).
- **Marcador en vivo** — pendiente de decidir tras el prototipo del
  Empleado 1 (23 nov): el scoreboard de ESPN da marcador y minuto; la
  página hoy se actualiza por horario (diario + cada hora en días de
  partido), no en vivo.

## ⏳ Semana 4 — Pendiente

- Parlay builder con picks reales (solo los de valor positivo).
- Guardar los picks elegidos.
- Actualizar los partidos con los de esa semana.

## ✅ Semana 5 — Hecha (adelanto en vivo 23 nov 2026)

- Al tocar un partido, abrir su detalle estilo 365Scores / OneFootball:
  últimos 5 partidos de cada equipo, historial entre ambos (H2H),
  posición en la tabla y momios.
- Alineación oficial cuando ya esté publicada (cerca de la hora del partido).
- Adelanto del Empleado 2 (23 nov, verificado por el jefe contra ESPN en
  vivo y probado en el preview): el detalle quedó en vivo en `index.html`
  la misma noche, junto con el bloque Fuerza del XI (Semana 8) con sus
  fracciones (Goles/Minutos/Puntos contra el mejor XI).

## ⏳ Semana 6 — Pendiente: alineación probable

- Alineación probable por equipo, como en 365Scores: el XI más frecuente
  por posición en los últimos 3–5 partidos jugados, con la formación más usada.
- Si un titular habitual no jugó el último partido por lesión o suspensión,
  se quita del XI probable y se marca la duda (solo si ESPN reporta la baja).
- Se marca siempre como **probable, no oficial**: la oficial llega cerca
  del partido y la reemplaza.

## ⏳ Semana 7 — Pendiente: actualización automática (que la página ya no sea estática)

- La página deja de depender de una actualización manual cada semana:
  se actualiza sola, sin que nadie tenga que hacer nada.
- Cómo: un flujo automático de GitHub Actions en el mismo repo, que corre
  solo cada día (y cada hora en días de partido): descarga los partidos,
  resultados y momios de ESPN, regenera los datos de `index.html` y hace
  commit automático. GitHub Pages publica el cambio solo.
- La clave de API-Football (si algún día se usa) nunca va en ese flujo
  ni en el repo: solo se usa la API de ESPN, que no necesita clave.
- Si ESPN falla un día, la página sigue mostrando los últimos datos
  guardados, no se queda en blanco.

## ⏳ Semana 8 — Pendiente: Fuerza del XI

- Puntaje 0–100 por alineación (oficial cuando esté publicada, probable
  de la Semana 6 cuando no), como en 365Scores: mide qué tan fuerte es
  el XI de hoy contra el mejor XI de la temporada del mismo equipo.
- Tres componentes, cada uno en % contra el mejor XI: goles aportados
  por los jugadores del XI, minutos jugados del XI y puntos obtenidos
  con esos jugadores en cancha.
- Primero se verifica la fuente (estadísticas de jugadores de ESPN) y
  la fórmula exacta; después se programa y se muestra en el detalle
  del partido.

## Reglas del proyecto

- Sin API keys en el repo ni en `index.html`: los datos se consultan en
  privado y se publican ya integrados en la página.
- Cada semana se actualizan los partidos con los de esa semana (a partir
  de la Semana 7, eso lo hace el flujo automático).
- Nunca se hacen apuestas ni se maneja dinero desde la página.
