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
