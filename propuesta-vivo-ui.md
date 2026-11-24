# Propuesta de UI: marcador en vivo a prueba de futuro (Empleado 2, 24 nov 2026)

## Mi posición frente a la propuesta del jefe

De acuerdo en lo esencial: el workflow de Actions como fuente (caché `data/vivo.json` cada 5 min en ventanas de partido), el fetch directo a ESPN como respaldo, nunca un error crudo como único estado, reintento automático cada 60 s, y el límite honesto (si ESPN cae por horas, el caché se pone viejo y la página lo dice). No cambio la arquitectura; mis cambios son de UI: qué ve el usuario en cada estado, cuándo cambia el texto y de dónde viene el dato.

## Mejoras que propongo (con números)

1. **La antigüedad sube sola y el estado cambia solo.** El jefe dice que la página muestra "actualizado hace X min". Propongo que ese contador suba cada 60 s mientras el modal está abierto, y que al cruzar ~10 min el estado pase solo de "caché fresco" a "caché viejo" (con su texto) y se intente el fetch directo. Sin esto, un usuario que deja el detalle abierto 20 minutos seguiría viendo "hace 3 min".

2. **Fetch directo en segundo plano desde los ~5 min, no solo a los 10.** El caché tiene entre 0 y 5 min cuando se lee (el workflow corre cada 5 min). Si el usuario abre el detalle con un caché de 4 min, con la propuesta del jefe vería un minuto con 4 min de retraso hasta que cumpla 10. Propongo: si el caché tiene más de ~5 min, intentar el fetch directo en segundo plano aunque se siga mostrando el caché; si responde, el dato se afina a ~1 min (el retraso medido de ESPN en vivo es <1 min, estimado ~medio minuto). Si no responde, no pasa nada: se sigue viendo el caché con su antigüedad.

3. **La fuente se ve en el texto.** "Actualizado hace X min" = dato del caché. "En vivo, actualizado hace menos de 1 min" = dato del fetch directo. El usuario entiende por qué el minuto puede saltar de 35' a 38' de una vez: cambió la fuente, no es un error.

4. **La primera carga no bloquea el resto del detalle.** Al abrir, solo la sección del marcador dice "Cargando marcador…" mientras se lee el caché (mismo origen, rápido); el resto del detalle (momios, últimos 5, Radiografía, H2H, tabla, XI) ya está ahí. Al cerrar el modal se paran el refresco de 60 s y el contador de antigüedad.

## Un reto con evidencia

El caché de 5 min puede esconder un gol hasta 5 minutos: un gol al 40' se ve en el caché hasta la siguiente corrida, y el usuario vería "0-0, 38', hace 4 min" sin saber que ya hubo gol. Por eso la antigüedad visible importa más que el número: el usuario debe ver "hace 4 min" y entender que el marcador puede estar desactualizado. Y la ventana del workflow tiene que cubrir todos los partidos de la semana: un partido fuera de ventana no tiene caché y cae al fetch directo, que hoy falló de forma intermitente en los dos hosts a la vez. El diseño lo aguanta (el estado "sin caché" existe), pero la ventana es el punto frágil.

## Los 4 estados del detalle (texto exacto que ve el usuario)

| Estado | Cuándo | Lo que ve el usuario |
|---|---|---|
| Caché fresco | Caché de menos de ~10 min | "Galatasaray 0 – 0 Aston Villa" / "Minuto 35' · Actualizado hace 3 min" |
| Caché viejo | Caché de ~10 min o más, fetch directo sin responder | "Galatasaray 0 – 0 Aston Villa" / "Minuto 23' · Último dato conocido hace 12 min, ESPN no responde, reintentando…" |
| Sin caché + fetch directo | No hay caché y ESPN responde | "Galatasaray 0 – 0 Aston Villa" / "Minuto 35' · En vivo, actualizado hace menos de 1 min" |
| Todo fallando | No hay caché y ESPN no responde | "Sin marcador en vivo por ahora. ESPN no responde y aún no hay datos guardados. Se reintenta solo cada minuto." |

Además: mientras se espera la primera carga, la sección dice "Cargando marcador…". Si el partido aún no empieza: "El partido aún no empieza." Ningún estado muestra "ESPN 400" ni "Failed to get events endpoint": esos errores solo se registran, no se le enseñan al usuario.

## Números que la sostienen

- Workflow cada 5 min (mínimo del cron de Actions); el caché tiene 0–5 min al leerlo.
- Fresco: menos de ~10 min. A partir de ~5 min se intenta el fetch directo en segundo plano (mejora 2).
- Fetch directo: ~1 min cuando ESPN responde. Retraso medido en vivo hoy: <1 min (estimado ~medio minuto). Medición del Empleado 1, 12:04:37–12:08:48: 0-0, minuto 19'→23'. Verificación del jefe, 12:20:52: 0-0, minuto 35'.
- Reintento automático cada 60 s, también cuando todo falla.
- Fallo de hoy: "error: ESPN 400 (uefa.champions 2026-11-24)", intermitente, del lado de ESPN; a veces en los dos hosts a la vez.

## Abrir, cerrar y antigüedad

- Al abrir el detalle: la sección muestra "Cargando marcador…" y luego el estado que toque (caché fresco en el caso normal). El resto del detalle no espera.
- Mientras el modal está abierto: el marcador se refresca cada 60 s y la antigüedad sube cada 60 s ("hace 3 min" → "hace 4 min"…).
- Al cruzar ~10 min de antigüedad: el texto cambia solo a "Último dato conocido hace X min, ESPN no responde, reintentando…" y se intenta el fetch directo.
- Al cerrar el modal: se paran el refresco y el contador. Al volver a abrir, se lee el caché de nuevo (fresco otra vez si el workflow ya corrió).
- Si el fetch directo responde mientras se ve el caché viejo: el dato se actualiza al minuto en vivo y el texto pasa a "En vivo, actualizado hace menos de 1 min".

## Límite honesto

El mismo que declara el jefe: si ESPN cae por horas, el caché se queda viejo y la página lo dice ("Último dato conocido hace X min…"). Ninguna solución gratuita arregla eso. Añado uno: si un partido queda fuera de la ventana del workflow, no hay caché para ese partido y todo depende del fetch directo, que es justo lo que falla de forma intermitente.

## Qué se probó

Copia `preview-semana-5-vivo-ui.html` (base: la copia de la Radiografía con Alavés 3/5): la sección "Marcador en vivo" arriba del detalle, con un selector de vista previa que muestra los 4 estados en el Galatasaray–Aston Villa de hoy (datos reales: 0-0, 35', 12:20:52 CST; 0-0, 23', 12:08:48 CST; las edades son de ejemplo para mostrar cada estado). `node --check` OK; jsdom 33/33: los 4 estados con sus textos exactos, ningún estado muestra un error crudo, el fresco muestra 0-0, 35' y la antigüedad, el contador sube y al llegar a 10 min cambia solo a texto de caché viejo, "Cargando marcador…" al abrir. Regresiones intactas (F1, F2, barra fija, pie, ordenar por EV, filtros, veredicto, Fuerza del XI, Radiografía con Alavés 3/5, parlay). No probado en navegador real ni en móvil (solo jsdom).
