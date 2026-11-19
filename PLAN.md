# Plan semanal — Football AI Agenda

Qué se hace cada semana, en el mismo `index.html` del repo. Las semanas
terminadas están marcadas como hechas; el resto está pendiente.

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
- Momios de ESPN/DraftKings verificados en vivo para la Semana 3.

## ⏳ Semana 2 — Pendiente (lun 23 nov 2026)

- Modelo Poisson de probabilidades por partido (1X2 y goles).
- Probabilidades propias en cada tarjeta, sin momios inventados.
- Actualizar los partidos con los de esa semana.

## ⏳ Semana 3 — Pendiente

- Momios reales de ESPN/DraftKings por partido (1X2, over/under 2.5, handicap).
- Comparar probabilidad propia vs momio: valor esperado (EV) y semáforo
  de valor real (verde/amarillo/rojo).
- Actualizar los partidos con los de esa semana.

## ⏳ Semana 4 — Pendiente

- Parlay builder con picks reales (solo los de valor positivo).
- Guardar los picks elegidos.
- Actualizar los partidos con los de esa semana.

## ⏳ Semana 5 — Pendiente: detalle del partido

- Al tocar un partido, abrir su detalle estilo 365Scores / OneFootball:
  últimos 5 partidos de cada equipo, historial entre ambos (H2H),
  posición en la tabla y momios.
- Alineación oficial cuando ya esté publicada (cerca de la hora del partido).

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

## Reglas del proyecto

- Sin API keys en el repo ni en `index.html`: los datos se consultan en
  privado y se publican ya integrados en la página.
- Cada semana se actualizan los partidos con los de esa semana (a partir
  de la Semana 7, eso lo hace el flujo automático).
- Nunca se hacen apuestas ni se maneja dinero desde la página.
