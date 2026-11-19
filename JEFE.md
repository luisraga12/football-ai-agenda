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
