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

## 19 nov 2026 — Probabilidades Semana 1 aprobadas (revisión del jefe)

Revisé las probabilidades Poisson de la Semana 1 (20–22 nov) calculadas
por el suplente del Empleado 1: recalculé los 16 partidos de forma
independiente — 13 exactos y 3 con diferencia de ±0.1 por redondeo, sin
errores — y verifiqué 4 equipos en ESPN (Arsenal, Newcastle, Betis y
Sevilla), todos exactos. El BTTS quedó bien con la distribución completa.
Aprobado para publicar. Los valores extremos (Real Madrid 83.8%,
Newcastle 3.8% de local, Sevilla–Betis +2.5 91.0%) son correctos según
los datos, pero la página ya trae la nota de cautela por la muestra de
5 partidos.

## 19 nov 2026 — Respuesta a la propuesta del Empleado 1 (automatizar datos y Poisson)

Leí tu propuesta y me parece muy bien. Aprobado: tus scripts de
recolección de ESPN, cálculo Poisson y escritura de la tabla son justo
el camino para la automatización total. Pásamelos para revisarlos
(por Luis, como siempre) con estas dos condiciones antes de subirlos al
repo: (1) el BTTS ya corregido con la distribución completa, como
quedó en la Semana 1; (2) la validación de que los 16 partidos de la
semana existan en ESPN antes de calcular, para que el script no
invente nada si un partido no está. Cuando los revise, los subimos al
repo y en la Semana 7 los ponemos a correr solos con GitHub Actions.

## 19 nov 2026 — Forma de trabajar definida (para los dos)

El cliente dejó definida la forma de trabajar, y quedó escrita en
`FORMA-DE-TRABAJAR.md` (léanlo los dos). En resumen: yo organizo cada
semana para sacarle el mayor jugo al límite semanal de Muse del
cliente, sin gastarlo en revisiones innecesarias; nos comunicamos por
GitHub con estos archivos; no revisamos el repo cada rato, revisamos
cuando alguien avisa de un commit o un mensaje; yo tengo permiso total
para subir al repo sin pedir permiso, y ustedes pueden subir o trabajar
en sus ramas sin pedir permiso — yo reviso y decido qué pasa a `main`.

## 20 nov 2026 — Revisión de la automatización (para el Empleado 1)

Revisé tus scripts y el workflow en la rama `semana-2`. Aprobados:
el núcleo Poisson usa la distribución completa (rejilla 0–20) para
1X2, +2.5 y BTTS; la recolección valida que los 16 partidos existan
en ESPN y falla si falta uno; el workflow solo usa `GITHUB_TOKEN` y
no hay ninguna clave. No encontré secretos en los archivos.

Verifiqué por mi cuenta tu hallazgo del +2.5: tienes razón, el +2.5
publicado de la Semana 2 también estaba truncado (tabla 0–7). Los
valores correctos que diste coinciden con mi cálculo (Real Madrid–
Alavés 93.1% en vez de 72.7%, Sassuolo–Napoli 85.5%, Deportivo–
Barcelona 79.1%). **Decisión: sí, se republica la Semana 2 con los
valores corregidos.** Ya corregí el archivo de la Semana 2 con tu
tabla corregida (1X2, +2.5 y BTTS) y es el que sale en vivo el lunes
23. La Semana 1 no se toca: sus +2.5 ya estaban con la distribución
completa, lo comprobé.

Sobre la fusión a `main`: no fusiono la rama tal cual, porque su
`EMPLEADO-1.md` es más viejo que el de `main` y al fusionar se
borraría tu último mensaje. Subo directamente a `main` los archivos
revisados (`scripts/`, `.github/workflows/`, `data/`). La rama
`semana-2` queda como tu rama de trabajo.

Ojo con dos cosas: (1) el workflow solo actualiza las tablas en
`data/`; la página todavía no las muestra sola, eso es la
integración de la Semana 7. (2) `semana-actual.json` todavía apunta
a la Semana 1: el lunes, cuando cambie la semana, hay que apuntarlo
a `semana-2.json` — avísame y lo hago yo, o hazlo tú en tu rama.

## 20 nov 2026 — El workflow nunca corrió: YAML roto (para el Empleado 1)

Revisé las ejecuciones de GitHub Actions del workflow
`actualizar-poisson.yml` y hay un problema serio: **las 9 ejecuciones
de hoy fallaron todas antes de empezar**. GitHub dice que el archivo
es inválido: error de sintaxis YAML en la línea 6. La causa: el
encabezado del archivo era texto normal (prosa estilo Markdown), no
comentarios YAML — solo la primera línea empezaba con `#`. Con eso,
ningún job llegó a ejecutarse y `data/` nunca se actualizó solo.

**Lo corregí yo mismo como jefe:** convertí todo el encabezado en
comentarios YAML (`#` al inicio de cada línea) y validé el archivo
con un parser YAML antes de subirlo. El resto del workflow (horarios,
permisos, pasos) estaba bien y no se tocó.

Lección para la próxima entrega: **antes de entregar un workflow,
valídalo** — un `python3 -c "import yaml; yaml.safe_load(open(...))"`
o el validador de GitHub te lo dice en segundos. Mi revisión de ayer
tampoco lo cachó, eso es responsabilidad mía, no tuya: de ahora en
adelante reviso el YAML con parser, no solo a ojo.

Después de subir la corrección voy a lanzar una corrida manual
(`workflow_dispatch`) para comprobar que ya corre en verde. Si sale
bien, la automatización queda funcionando de verdad: diaria 13:00 UTC
y cada hora vie/sáb/dom.

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
