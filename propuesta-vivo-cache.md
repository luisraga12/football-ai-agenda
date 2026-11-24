# Propuesta: marcador en vivo con caché (Empleado 1 — datos/workflow)

**Fecha:** 24 nov 2026. **Orden:** JEFE.md, commit e0016b3 (24 nov 13:12 CST).
**Leí primero la propuesta del jefe** (caché primero, fetch directo como
respaldo) y esta es la mía: estoy de acuerdo en lo central, con 4 mejoras y
1 reto con evidencia. Nada de aquí es solo "estoy de acuerdo": todo trae
números y algo probado corriendo.

## 1. El problema, con los números de hoy

El módulo pide el marcador a ESPN directamente desde el navegador de cada
visitante. ESPN es una API no oficial, sin llave, sin SLA y sin aviso de
cambios. Hoy 24 nov falló de forma intermitente con
`{"code":400,"message":"Failed to get events endpoint."}`:

- 12:33 y 12:36: el modal del Galatasaray da 400 en el navegador de la nube.
- 12:39: el 400 es GENERAL en ese navegador (también Arsenal–City, eng.1).
- 12:47: el cuerpo del error es de ESPN mismo; la misma URL da 200 por curl
  y en el navegador real de Luis.
- 12:51: una página de prueba pide las 4 URLs (site.api y site.web.api,
  Champions y Premier) y las 4 dan 200; 12:53 el modal vuelve a dar 400.
- 12:55: el módulo da 400 en AMBOS hosts; 12:56 curl/node dan 200 al mismo URL.

Conclusión del jefe, que comparto: el fallo es intermitente del lado de
ESPN, no un bloqueo fijo ni un error del código. Cualquier arreglo solo en
el navegador (reintento, otro host) sigue dependiendo de que ESPN esté
arriba justo en el segundo en que el usuario abre el detalle. Eso no es a
prueba de futuro.

## 2. Diseño propuesto: caché primero, fetch directo como respaldo

### 2.1 Qué se pide y cuándo

Un workflow nuevo, `.github/workflows/actualizar-vivo.yml`, separado del
workflow de Poisson (otra cadencia, otro propósito; el diario no se toca).
Cada corrida pide los scoreboards de ESPN **solo para hoy** (hora de México)
y solo para los pares (liga, fecha) que trae la configuración de la semana
actual (`scripts/config/semana-actual.json` + `semana-<N>-entresemana.json`
si existe). Semana 2: 6 ligas, 16 pares (liga, fecha), 28 partidos.

El cron corre cada 5 minutos **solo en ventanas de partido** (horas UTC;
en noviembre México es UTC-6). El mínimo del cron de GitHub Actions es
5 minutos, así que no se puede pedir más frecuente por este camino.

| Ventana (cron, UTC) | Días | En hora de México | Cubre |
|---|---|---|---|
| `*/5 17-23 * * 2,3,4` | mar–jue | 11:00–17:55 | Entre semana (11:45 y 14:00) |
| `*/5 12-23 * * 5,6,0` | vie–dom | 06:00–17:55 | Fin de semana (ligas europeas) |
| `*/5 0-4 * * 6,0` | sáb–dom | vie/sáb 18:00–22:55 | Extensión nocturna Liga MX |

La tercera ventana existe para semanas con Liga MX (viernes noche); en
semanas sin Liga MX el script sale temprano sin escribir nada (ver 2.4).

**Validación del cron (parser `croniter`, 24 nov 13:30 CST = 19:30 UTC):**
próximos disparos `mar 24 nov 19:35, 19:40, 19:45 UTC`; `vie 27 nov 12:00,
12:05, 12:10 UTC`; `sáb 28 nov 00:00, 00:05, 00:10 UTC`. Las 3 expresiones
son sintaxis válida. Conteo en la semana 24–30 nov: 252 + 432 + 120 =
**804 corridas/semana en el peor caso** (todas las ventanas).

### 2.2 Formato de `data/vivo.json`

Un solo archivo, siempre completo con los 28 partidos de la semana (merge,
ver 2.4). Cada entrada lleva su propia hora de actualización, y el archivo
lleva la hora de generación para que la página calcule la antigüedad.

```json
{
  "version": 1,
  "generado_en": "2026-11-24T19:29:05Z",
  "generado_en_mx": "2026-11-24T13:29:05-06:00",
  "semana": 2,
  "fuente": "ESPN scoreboard (site.api.espn.com, respaldo site.web.api.espn.com)",
  "partidos": [
    {
      "liga": "uefa.champions", "fecha": "2026-11-24",
      "home_id": 432, "away_id": 362,
      "home": "Galatasaray", "away": "Aston Villa",
      "estado": "in", "detalle": "88'", "minuto": "88'",
      "marcador_local": 1, "marcador_visita": 0,
      "actualizado_en": "2026-11-24T19:29:05Z"
    }
  ],
  "advertencia": null
}
```

Ejemplo real arriba: Galatasaray 1–0 Aston Villa, min 88', generado hoy a
las 13:29 CST (el partido empezó 11:45; 88' + descanso cuadra con la hora).
`estado` es `pre | in | post` (el de ESPN), `detalle` es el texto de ESPN
("88'", "Descanso", "Finalizado") y `minuto` es `displayClock`. Los
partidos se identifican por liga + fecha + IDs de equipo, nunca por nombre,
igual que `recolectar_datos.py` y `marcador_en_vivo.js`.

**Cómo sabe la página la antigüedad:** lee `generado_en` (y por partido
`actualizado_en`), calcula `ahora − generado_en` y muestra
"actualizado hace X min". Regla: si el caché tiene menos de ~10 min, se
muestra tal cual; si tiene más de ~10 min o no existe, el módulo intenta el
fetch directo a ESPN (comportamiento actual + respaldo de dos hosts);
si eso también falla, mensaje corto y honesto, nunca un error crudo como
único estado. Reintento automático cada 60 s mientras el detalle esté
abierto. Este es el contrato que usa la propuesta de UI del Empleado 2.

### 2.3 Qué pasa cuando ESPN falla una corrida

- Se intenta `site.api.espn.com` y, si falla, `site.web.api.espn.com`
  (el respaldo que el jefe preparó para el navegador; en el workflow no
  hay CORS, pero el 400 de hoy afectó a los dos hosts).
- Si una liga/fecha falla, sus partidos conservan el último dato bueno
  (merge) y el fallo queda registrado con hora, liga, fecha y error.
- Si TODAS las consultas fallan, **no se toca `data/vivo.json`**: el
  script sale con código 1, el workflow lo registra y el archivo anterior
  sigue sirviendo. Nunca se escribe un archivo vacío o roto.
- El archivo se genera en un temporal, se valida (JSON bien formado,
  lista de partidos, todos los campos requeridos) y solo entonces se
  reemplaza (`os.replace`, atómico).
- Los fallos se acumulan en `data/vivo-log.json` (últimas 50 entradas)
  para auditarlos; `vivo.json` lleva solo `advertencia` (texto corto o
  `null`) para que la página pueda mostrarla sin leer otro archivo.
- El workflow hace commit **solo si algo cambió** (`git diff --cached`),
  igual que el workflow de Poisson: no hay commits vacíos cada 5 minutos.

### 2.4 La compuerta es doble (mejora 4)

1. **Ventanas del cron** (2.1): fuera de ellas no hay corridas.
2. **El script no escribe los días sin partidos:** si hoy no hay ningún
   par (liga, fecha) en la configuración (por ejemplo, un lunes), sale
   con código 0 sin tocar nada. No se necesita una lista de fechas en el
   workflow: la ventana se deriva de la configuración de la semana, así
   que al cambiar de semana no hay que editar el cron.

### 2.5 Estimación de minutos de Actions (con números)

- Peor caso: 804 corridas/semana (2.1). Cada corrida es checkout (~15–30 s)
  + setup-python (~20–40 s) + script (1–4 consultas ESPN, ~10–30 s) +
  commit/push solo si cambió (~10 s): **~1 minuto por corrida**.
- **~800 min/semana, ~3,480 min/mes.** Las ventanas ahorran 60% frente
  a un cron `*/5` 24/7 (2,016 corridas/semana, ~2,000 min/semana).
- **Costo: $0.** El repo es público y GitHub Actions es ilimitado y
  gratuito para repositorios públicos. Los minutos se declaran como uso,
  no como gasto. Si el repo fuera privado, el plan gratuito trae
  2,000 min/mes y estos ~3,480 min/mes lo rebasarían: en ese caso habría
  que recortar ventanas (por ejemplo, quitar la extensión nocturna:
  −120 corridas/semana, −15%).
- Los workflows programados **solo corren en `main`**: este workflow
  empieza a correr cuando se fusione a `main`, igual que el de Poisson.

### 2.6 Qué NO arregla esta propuesta (límite honesto, de acuerdo con el jefe)

Si ESPN cae por horas, el caché se queda viejo y la página lo dice
("último dato conocido hace X min, ESPN no responde, reintentando").
Ninguna solución gratuita arregla eso. La única sería una segunda fuente
en vivo, y las gratuitas no sirven: football-data.org pide token (el
cliente no lo ha dado), API-Football gratis no abre la temporada 2026/27
y TheSportsDB no tiene en vivo en la llave gratuita. Largo plazo, cuando
el cliente despliegue su EC2: el mismo diseño, con un backend pequeño en
su servidor pidiendo a ESPN cada 30–60 s; el diseño no cambia, solo el
que pide los datos se mueve del workflow al servidor.

**Compromiso que se declara:** el caché del workflow es cada 5 min (el
mínimo del cron de Actions), no cada 60 s. Se cambia frescura de 60 s por
confiabilidad; el fetch directo cubre la diferencia cuando ESPN responde.

## 3. Mejoras sobre la propuesta del jefe

1. **Merge, no reconstrucción:** `vivo.json` siempre trae los 28 partidos
   de la semana, no solo los de hoy. Cada entrada conserva su
   `actualizado_en`; los partidos de otros días no se pierden entre
   corridas y los finalizados quedan con su marcador final.
2. **Respaldo de dos hosts también en el workflow**, no solo en el
   navegador: el script intenta site.api y luego site.web.api en cada
   consulta.
3. **Validación + escritura atómica + log de fallos separado:**
   temporal → validar → reemplazar; `data/vivo-log.json` con las últimas
   50 fallas; `advertencia` corta dentro de `vivo.json`.
4. **Compuerta doble** (2.4): ventanas del cron + salida temprana los
   días sin partidos. El cron no lleva fechas fijas: la ventana se deriva
   de la configuración de la semana.

## 4. Reto a la propuesta del jefe (con evidencia)

**El cron de 5 min es "best-effort", no 5 min garantizados.** GitHub
documenta que las corridas programadas pueden retrasarse minutos cuando la
plataforma va cargada, y el retraso no se puede medir desde el repo. Por
eso la frescura real no es "cada 5 min" sino "hasta 5 min + retraso de
GitHub". El diseño ya lo absorbe: la página no confía en el horario, confía
en `generado_en`/`actualizado_en` y muestra la edad real; el umbral de
10 min para el fetch directo existe justo para ese hueco. No lo medí en
este repo (no hay corridas programadas de este workflow todavía), así que
lo dejo como límite declarado, no como número.

## 5. Pruebas hechas (hoy, con datos reales)

- `python3 scripts/generar_vivo.py --todas` (13:29 CST): **28/28 partidos,
  0 fallos**, 16 pares (liga, fecha) consultados, todo por site.api.
  Ejemplo real en `data/vivo.json`: Galatasaray 1–0 Aston Villa, 88'.
- `python3 scripts/generar_vivo.py` (modo workflow, solo hoy, 13:29 CST):
  4 partidos actualizados (los de hoy), **28 conservados: el merge
  funciona**, 0 fallos.
- Workflow `.github/workflows/actualizar-vivo.yml`: `yaml.safe_load` OK;
  los 3 crons validados con `croniter` (próximos disparos y conteo
  semanal 252 + 432 + 120 = 804, ver 2.1 y 2.5).
- `python3 -m py_compile scripts/generar_vivo.py` OK.
  `node --check scripts/marcador_en_vivo.js` OK (el módulo no se tocó).
- **Límite honesto de la prueba:** el 400 intermitente NO apareció en
  mis corridas (todo dio 200 por site.api entre 13:29 y 13:30 CST), así
  que el respaldo de dos hosts está implementado pero **no se ejerció
  hoy**: queda como código, no como prueba. La primera corrida real del
  workflow en `main` es la que lo pondrá a prueba contra el 400.

## 6. Archivos de esta entrega

- `propuesta-vivo-cache.md` (este archivo, en la raíz de la rama).
- `scripts/generar_vivo.py` (nuevo): genera `data/vivo.json` desde ESPN.
- `.github/workflows/actualizar-vivo.yml` (nuevo): cron cada 5 min en
  ventanas de partido + `workflow_dispatch` para probar.
- `data/vivo.json` (nuevo): ejemplo real generado hoy (28 partidos).
- `scripts/README.md`: punto nuevo documentando el script y el workflow.

No se tocó `index.html`, `semana-actual.json` ni el workflow de Poisson.
El workflow nuevo solo corre cuando se fusione a `main` (regla de Actions).

## 7. Preguntas al jefe

1. ¿El workflow nuevo va en su propio PR o junto con la Semana 6?
2. ¿`data/vivo.json` se commitea en `main` como ejemplo (como va aquí) o
   se deja que solo Actions lo genere? Yo lo dejo commiteado para que la
   página tenga algo que leer desde el primer día.
3. ¿La extensión nocturna de Liga MX (sáb/dom 00:00–04:55 UTC) se queda,
   o la recorto para ahorrar 120 corridas/semana?
