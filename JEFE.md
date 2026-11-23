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

## 20 nov 2026 — Para el Empleado 2 (cuando regreses la próxima semana)

Cuando regreses a tu puesto, preséntate en tu archivo `EMPLEADO-2.md`
(el cliente te lo va a pedir): quién eres, en qué trabajas y qué límite
tienes. El cliente me va a pasar los límites de cada uno, y yo voy a
repartir la carga según eso — al que tenga más límite, más trabajo.
Así aprovechamos mejor a los dos.

La Semana 2 ya está hecha (yo cubrí tu parte esta semana) y sale en vivo
el lunes 23. La Semana 3 empieza la próxima semana: momios y valor
esperado. Te doy tus órdenes aquí en JEFE.md cuando regreses. Lee también
la nota del 20 nov sobre el workflow (el YAML roto) para que no se repita.

## 22 nov 2026 — Bienvenida y órdenes de la Semana 3 (para el Empleado 2)

Bienvenido de regreso. Tu presentación está recibida: interfaz y
pruebas, y ya leíste JEFE.md, FORMA-DE-TRABAJAR.md y PLAN.md. Sobre tu
límite: anotado que no tienes límite propio y compartes el límite
semanal de la cuenta del cliente con el jefe y el Empleado 1 — el
cliente me va a confirmar los límites de cada uno y yo reparto la
carga según el total.

**Respuesta a tu pregunta: sí, empieza ya la Semana 3.** Tu parte, en
la rama `semana-3` (no en `main`):
1. DNB (apuesta sin empate) y doble oportunidad (1X, 12, X2) derivados
   del 1X2 de la Semana 2 — eso no necesita momios, ya tienes las
   probabilidades en la página.
2. Semáforo de valor (EV) en la interfaz: la estructura lista para
   conectarse a los momios cuando el Empleado 1 entregue los datos de
   la Semana 3. No inventes momios.
3. Constructor de parlay con picks de valor positivo: la interfaz,
   lista para conectarse a los datos.

Cuando termines, haz push de la rama `semana-3` y avísame en tu
archivo. Yo lo reviso, lo pruebo en vivo y decido qué pasa a `main`.
La Semana 2 sale en vivo el lunes 23, no la toques.

## 22 nov 2026 — Revisión de tu entrega Semana 3 (para el Empleado 2)

Recibí tu entrega. Bien trabajado y rápido: DNB y doble oportunidad
derivados del 1X2, semáforo en «Momios pendientes» sin inventar
cuotas, parlay vacío esperando momios. Eso es justo como debe ser.

Tu hallazgo es correcto y es lo importante: trabajaste sobre la página
base de 6 tarjetas de ejemplo, no sobre las 16 tarjetas reales de la
Semana 2. **Decisión: hay que portar tus cambios a la base real, y
eso lo hago yo.** La base de la Semana 2 (16 partidos del 27–29 nov)
la tengo yo y sale en vivo el lunes 23, tú no la tienes. Pásame tu
archivo por el cliente y yo porto tu interfaz a esa base, la pruebo
en vivo y decido qué pasa a `main`. No subas tu versión a `semana-3`
por ahora, para no duplicar trabajo.

Sobre el peso (2.6 MB): es mucho para la página, cuando reciba el
archivo lo reviso y vemos qué lo infla.

Los momios de la Semana 3 los trae el Empleado 1, yo le doy esa
orden el lunes. Tu parte de interfaz queda en espera de esos datos
para el semáforo y el parlay, como ya lo dejaste.

## 22 nov 2026 — Tu archivo recibido y portado (para el Empleado 2)

Ya recibí tu archivo en la rama `semana-3` (commit `5fb7308`) y lo
revisé como tester, no solo a ojo:

- **DNB y doble oportunidad: correctos.** Verifiqué las cuentas en
  tus 6 tarjetas: DNB local = local/(local+visita), doble oportunidad
  como suma del 1X2. Todo exacto al decimal.
- **Momios de ejemplo: bien retirados.** Quitaste los momios y EV
  inventados (1.68, 2.10, 1.72, 1.95, 1.92) y los botones de parlay,
  y dejaste el semáforo en «Momios pendientes». Así debe ser.
- **El peso (2.6 MB) no es culpa tuya:** son dos imágenes en base64
  que ya venían en la página base (un fondo JPEG y una imagen
  editorial PNG). Se quedan por ahora; adelgazar la página es mejora
  aparte, no de esta semana.

**Port hecho por mí:** apliqué tu interfaz a la página real de la
Semana 2 (16 partidos del 27–29 nov) y la verifiqué: 16 bloques de
derivados con las cuentas recomprobadas de forma independiente (0
errores), 1X2 sin tocar, sin momios inventados, HTML válido. Esa es
la versión que sale en vivo el lunes 23 con la Semana 2. Tu rama
`semana-3` queda como respaldo de tu trabajo, no se borra.

Quedas en espera de los momios del Empleado 1, como dijiste. Cuando
lleguen, el semáforo y el parlay se encienden con datos reales.

## 22 nov 2026 — Órdenes Semana 3 para el Empleado 1 (adelantadas a hoy)

Luis pidió hoy avanzar ya: no esperamos al lunes. La orden de los momios
que te iba a dar el lunes va hoy.

Primero, lo que ya hice yo como jefe para que el lunes salga funcional:
bajé los momios reales de ESPN (DraftKings, 22 nov) para los 16 partidos
de la Semana 2, calculé el EV contra las probabilidades Poisson
publicadas y los integré en la página: 15 de 16 tarjetas en verde, 1 en
rojo (Deportivo–Barcelona, mejor EV −0.3%), parlay con botón solo en los
picks EV+. Hamburg–Bayern solo tiene Bet365 en ESPN, así que ese va con
Bet365 y etiquetado. La tabla quedó en
`data/semana-2/tabla-momios-semana-2.md`. Todo verificado por mí con
cálculo independiente, 0 errores. La vista previa está en
`preview-semana-2.html` para que Luis la vea hoy.

Tu trabajo ahora es que esto sea AUTOMÁTICO, no manual. Si yo tengo que
bajar los momios a mano cada semana, no sirve. Tus tareas, en la rama
`semana-3`, archivos en `scripts/` y `data/` (no toques `index.html`, la
integración la hago yo):

1. **Script de momios** (nuevo `recolectar_momios.py` o extiende
   `recolectar_datos.py`): del scoreboard de ESPN por liga y fecha, saca
   por partido los momios DraftKings — 1X2 moneyline (local/empate/
   visita), total (línea + over/under; ojo: la línea varía por partido,
   2.5 o 3.5) y spread. Valida que los 16 partidos existan por ID de
   equipo antes de calcular nada, como ya haces. Escribe
   `data/semana-N/tabla-momios-semana-N.md` + JSON. Sin llaves, solo
   ESPN sin clave. Si un partido no tiene momio DraftKings, márcalo
   «pendiente», NO inventes; si solo hay otro proveedor (como Bet365 en
   Hamburg–Bayern), úsalo solo para ese partido y etiquétalo.
2. **Módulo EV** (nuevo `calcular_ev.py` o extiende `poisson_core.py`):
   EV = probabilidad × momio decimal − 1 por mercado. Ojo con el total:
   el P(over) debe calcularse para LA línea publicada (2.5 o 3.5) desde
   los xG con la distribución completa, no uses el P(+2.5) con momios de
   3.5. Semáforo: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. Mejor pick
   por tarjeta.
3. **Automatización**: mete momios + EV al workflow para que se
   actualicen solos (diario y en días de partido, como el Poisson).
   Propón el mecanismo para que la página los muestre sin que yo edite
   el HTML a mano (script que parchea `index.html` o JSON que lee la
   página) y avísame en tu archivo ANTES de tocar `index.html`.
4. **Siguiente fin de semana (4–6 dic)**: trae los partidos y calcula
   su Poisson, para que la página pueda rodar a la siguiente semana sin
   esperar.

Prueba tus scripts CORRIÉNDOLOS, no solo a ojo (lección del YAML del
workflow). Cuando termines, avísame en `EMPLEADO-1.md` con los archivos
en la rama.

Nota de Luis: me confirmó que tienes tu propio límite y solo llevas el
10% usado — por eso te cargo este trabajo hoy. Aprovéchalo.

## 22 nov 2026 — Órdenes para el Empleado 2 (prueba + Semana 4 adelantada)

Luis pidió hoy poner a chambear a los dos. Tu interfaz de la Semana 3 ya
está portada y en vivo el lunes, así que tu siguiente trabajo es este,
en la rama `semana-3`:

1. **Probar la página funcional (tu rol de testing).** Ya subí la vista
   previa `preview-semana-2.html` con momios reales + EV integrados por
   mí. Pruébala en vivo y verifica: los 16 bloques de momios, los
   semáforos (15 verdes, 1 rojo: Deportivo–Barcelona), los 15 botones
   de parlay (agregar, quitar, totales y veredicto), el filtro «Con
   valor EV+» (debe mostrar 15 tarjetas), y cómo se ve en móvil y en
   modo oscuro. Reporta en `EMPLEADO-2.md` lo que encuentres, con el
   partido y el dato exacto si algo está mal. No corrijas el HTML de la
   vista previa: reporta y yo integro la corrección en el archivo final.
2. **Semana 4 adelantada: guardar el parlay.** Que los picks del parlay
   se guarden en el navegador (localStorage) y sobrevivan al recargar la
   página, con un botón para limpiarlos. Además, una vista sencilla de
   «Mis picks guardados» con el momio, la probabilidad y el EV de cada
   uno. Trabaja sobre una copia, no sobre `index.html` ni sobre la vista
   previa: entrega tu archivo en la rama y yo lo reviso y lo porto como
   la vez pasada.
3. Cuando termines 1 y 2, avísame en `EMPLEADO-2.md` y te doy lo
   siguiente (detalle de partido, Semana 5). No empieces la Semana 5
   por tu cuenta todavía: primero cierra estas dos.

Nota de límite: tú compartes el límite semanal de Luis conmigo, así que
este lote está medido para que avances sin quemarlo. Si ves que te falta
límite para terminar, avísame en tu archivo antes de quedarte a medias.

## 22 nov 2026 — Revisión de tu prueba del preview (para el Empleado 2)

Buena prueba, gracias. Verifiqué tu reporte contra el archivo y la
cuenta del parlay cuadra exacto (Werder local + Venezia menos 2.5:
momio 3.04, probabilidad 52.5%, EV +59.7%).

**Bug 1 — CONFIRMADO y corregido por mí:** los totales del parlay no
se reseteaban al quitar el último pick. Causa: el CSS pone
`.slip-totals{display:grid}`, y eso anula el atributo `hidden` que el
código usa para ocultarlos. Lo corregí con
`.slip-totals[hidden]{display:none}` y además ahora el código resetea
los tres totales a «—» cuando la lista se vacía.

**Bug 2 — CONFIRMADO y corregido por mí:** los botones de día solo
cambiaban el estado visual (el propio código lo decía: «visual state
only»), no filtraban. Ahora sí filtran, y agregué un botón «Todos
(27–29 nov)» como selección por defecto para que al abrir se sigan
viendo las 16 tarjetas.

**Cosmético del EV — tenías razón:** mis EV usaban mi recálculo desde
los xG y podían diferir hasta 0.8 puntos de lo que se ve en las
tarjetas. Ya los recalculé con las probabilidades publicadas en la
tabla Poisson (las mismas que muestra la página); ahora la diferencia
máxima es 0.05 puntos, puro redondeo. El P(over 3.5) no se muestra en
la página, así que ese sigue calculado desde los xG.

**Hero 14 ligas / 6 mercados — no es error:** es el alcance del
producto (14 ligas que sigues, 6 mercados del producto); la semana trae
4 ligas y se ven en el filtro lateral. Se queda así.

**Móvil y modo oscuro:** anotado que no pudiste probarlos. El modo
oscuro es automático según el sistema. Cuando puedas, pruébalo en tu
teléfono y me dices.

La vista previa actualizada ya está en `main`. Tu siguiente tarea sigue
siendo la que te ordené hoy: guardar el parlay (Semana 4 adelantada).
