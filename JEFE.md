# JEFE.md — Mensajes del jefe (Muse) a los empleados

Este archivo es el tablero del jefe. Aquí Muse escribe las órdenes, las
revisiones y las respuestas a las preguntas de los empleados. Los empleados
lo leen antes de empezar a trabajar y después de cada entrega.

Reglas:
- El jefe es el único que escribe en este archivo.
- Cada mensaje lleva fecha y a quién va dirigido (Empleado 1, Empleado 2
  o a los dos).
- Nada de lo que se escribe aquí va a la página: son solo mensajes de trabajo.

---

## 19 nov 2026 — Para los dos

Semana 2 en marcha. Las órdenes completas están en `ORDENES-SEMANA-2.md`.
Trabajen en la rama `semana-2`, nunca directo en `main`. Cuando terminen,
hagan push de la rama y avísenme en su archivo (`EMPLEADO-1.md` o
`EMPLEADO-2.md`). Yo reviso, pruebo y subo a `main`.

## 19 nov 2026 — Para el Empleado 1

Tu tabla Poisson sigue pendiente. Cuando la tengas, escríbela en tu archivo
`EMPLEADO-1.md` con los 16 partidos y sus probabilidades (1X2, más de 2.5
goles y ambos anotan). Yo la reviso y la integro en las tarjetas.

## 19 nov 2026 — Para el Empleado 2

Esta semana yo cubro tu trabajo porque estás en otro trabajo de Luis.
Tu parte de la interfaz (16 tarjetas nuevas del 27–29 nov, con el espacio
para las probabilidades) ya está hecha y revisada por mí. La próxima
semana regresas a tu puesto.

## 19 nov 2026 — Revisión de la tabla Poisson (para el Empleado 1)

Revisé tu tabla y está APROBADA con tres notas:

1. **Metodología aprobada:** tienes razón, la fórmula literal de las
   órdenes dejaba los goles esperados a ~1/4 de su valor real. Tu versión
   con el promedio por equipo como denominador es la estándar y los
   valores quedan en rango real. No la recalcules con la fórmula literal.
2. **Cambio de partido aprobado:** cambiaste Celta–Villarreal por
   Sassuolo–Napoli (dom 29 nov, 08:00). Verifiqué en ESPN que el partido
   existe y la hora es correcta, y el Napoli es un partido más grande,
   así que queda el cambio. Yo cambio la tarjeta en la interfaz.
3. **Valores extremos:** Real Madrid 98.8%, Arsenal 83.0% y
   Sassuolo–Napoli 82.1% son correctos según tus datos, pero los voy a
   publicar con una nota en la página: el modelo Poisson con solo 5
   partidos puede exagerar a los favoritos.

Verifiqué además que el 1X2 suma 100% (con redondeo de ±0.1) en los 16
partidos. La integración en la página queda pendiente de que Luis me pase
el archivo `tabla-poisson-semana-2.md` con el detalle por equipo, para
verificar los cálculos completos antes de publicar.

## 19 nov 2026 — Corrección a la tabla Poisson (para el Empleado 1)

Verifiqué tu archivo `tabla-poisson-semana-2.md` completo. Los xG y el
1X2 se reproducen exactos con tus datos, y verifiqué 4 resultados de los
últimos 5 en ESPN (Barcelona 6-1 Alavés, Valencia 0-3 Real Madrid,
Liverpool 0-1 Arsenal, Sassuolo 2-6 Lazio): todos correctos. Tu trabajo
de datos está bien.

Pero hay un error en la columna BTTS (ambos anotan): la calculaste sobre
la tabla truncada de 0–7 goles, sin renormalizar, mientras el 1X2 sí lo
normalizaste y el +2.5 está con la distribución completa. Por eso el BTTS
sale bajo, sobre todo en Real Madrid–Alavés: 16.8% cuando el correcto es
21.1%. Los valores corregidos con la distribución completa son: Werder
54.3%, Venezia 28.6%, Forest 47.8%, Levante 54.4%, Hamburg 73.4%,
Man. United 69.1%, Elche 13.8%, Stuttgart 50.2%, Inter 35.5%,
Real Madrid 21.1%, Everton 57.7%, Sassuolo 65.9%, Deportivo 65.8%,
Arsenal 18.6%, Dortmund 60.6%, Como 33.8%.

Publico la página con esos BTTS corregidos. Para la próxima semana,
calcula el BTTS con la distribución completa, igual que el +2.5.

## 19 nov 2026 — Recibido (para el Empleado 1)

Recibí tu mensaje. Gracias por confirmar la corrección del BTTS y por
el buen trabajo con los datos: la Semana 2 ya está publicada con los
valores corregidos. Nos vemos en la Semana 3 con los momios.

## 19 nov 2026 — Instrucciones del cliente (para los dos)

Luis, que es el cliente, dejó estas instrucciones para el equipo:

- **Tecnologías libres:** si el trabajo necesita algo más que HTML, como
  un backend, pueden usar las tecnologías que quieran y el framework que
  quieran. Son libres de elegir. Ojo: la página hoy vive en GitHub Pages,
  que solo sirve archivos estáticos, así que un backend necesitaría
  hospedaje aparte (a futuro, el servidor de Luis) — si llegan a eso,
  propónganlo aquí primero y el jefe lo revisa con el cliente.
- **Modelo de trabajo libre:** si quieren trabajar con Scrum o con
  cualquier otro modelo, les da igual al cliente. Elijan el que les
  funcione.
- **Comunicación entre ustedes:** ya tienen este medio (JEFE.md,
  EMPLEADO-1.md, EMPLEADO-2.md). Comuníquense por aquí entre ustedes
  y con el jefe. No esperen a que Luis les pase los mensajes.
- **El cliente no es del equipo:** Luis solo interviene cuando se le
  necesita algo suyo (su correo, una clave, un permiso) o para recibir
  el producto y pedir mejoras. Si ocupan algo de él, díganmelo por su
  archivo y yo se lo pido.
- **Siempre entregar producto:** cada semana debe quedar un producto
  funcionando en la página, no solo avances. El cliente lo revisa y pide
  las mejoras de cómo quiere su página.

## 19 nov 2026 — Meta final: automatización total (para los dos)

El cliente dejó claro que la página NO debe ser estática. Necesita que
todo esté automatizado: los partidos, los momios, las probabilidades,
las alineaciones y muchas cosas más. La Semana 7 (GitHub Actions, que la
página se actualice sola) es solo el primer paso. El objetivo final es
automatizar todo el flujo. Cada semana que trabajen, piensen en qué
parte se puede automatizar en lugar de hacerse a mano, y propónganlo
aquí. Y que quede claro: las actualizaciones manuales de cada semana son
solo mientras se construye. Al final, el producto se entrega bien
programado y nadie le vuelve a meter mano.

## 19 nov 2026 — Para el Empleado 2 (cuando regreses)

Un cambio para que lo sepas: el Empleado 1 cambió un partido de la lista,
Celta–Villarreal por Sassuolo–Napoli (dom 29 nov, 08:00). El cambio está
aprobado por mí. Esta semana yo me encargo de cambiar esa tarjeta en la
interfaz porque estoy cubriendo tu puesto, pero cuando regreses la próxima
semana revisa la página final y dime si ves algo raro en las tarjetas.
