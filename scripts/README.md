# Automatización: datos ESPN + modelo Poisson

Scripts del Empleado 1 (datos y modelo Poisson) para generar la tabla de
probabilidades de cada semana **sin hacerlo a mano** y sin tocar la
interfaz (`index.html` no se toca en este trabajo).

## Qué hace

1. **`recolectar_datos.py`** — descarga de la API pública de ESPN (sin
   clave):
   - los scoreboards de cada liga y fecha, y **valida que los partidos
     de la semana existan en ESPN** (por ID de equipo). Si falta uno, el
     script falla y no se calcula nada: no se inventa ningún dato.
   - el schedule de cada equipo: sus últimos 5 partidos de liga o
     competición completados hasta el cutoff de la configuración (en
     competiciones europeas solo hay 4 jornadas jugadas: se usan los 4
     disponibles, con promedios por partido).
   - los promedios de cada liga o competición desde los scoreboards de
     las últimas ~3 jornadas completadas antes del cutoff (el endpoint
     de standings de ESPN devuelve 404; en competiciones UEFA el
     calendario no trae fechas, así que las jornadas se sacan de los
     schedules ya descargados).
2. **`calcular_poisson.py`** — ataque, defensa, goles esperados (xG) y
   probabilidades 1X2, +2.5 y BTTS con la **distribución Poisson
   completa** (rejilla 0–20 goles, ver `poisson_core.py`).
3. **`generar_tabla.py`** — escribe `data/semana-N/tabla-poisson-semana-N.md`
   con la tabla de partidos, la tabla por equipo, los promedios de liga,
   las fuentes y los datos no verificados.
4. **`recolectar_momios.py`** — descarga del scoreboard de ESPN los
   momios por partido (proveedor preferente DraftKings: 1X2 moneyline,
   total y spread; si no hay DraftKings, se usa el único proveedor
   disponible, p. ej. Bet 365, solo para ese partido y etiquetado).
   Valida que los partidos existan por ID de equipo antes de
   calcular; si un partido no tiene momio, queda "pendiente", no se
   inventa ninguna cuota. Escribe `data/semana-N/raw/momios.json`.
   Si un partido trae total/spread pero no moneyline, el 1X2 queda sin
   EV (blindaje, jefe 22 nov 2026) en vez de romper el cálculo.
5. **`calcular_ev.py`** — EV = probabilidad × momio decimal − 1 por
   mercado. El P(over) se calcula para LA línea publicada (2.5 o 3.5)
   desde los xG con la distribución completa (`p_over` en
   `poisson_core.py`); el spread usa `p_spread_cover`. Semáforo por
   mejor pick: verde EV ≥ +5%, amarillo 0–+5%, rojo < 0%. Escribe
   `data/semana-N/raw/ev_result.json`, `data/semana-N/ev.json` y
   `data/semana-N/tabla-momios-semana-N.md`. Desde el 23 nov el
   `ev.json` incluye `mercados` (EV por mercado) y el decimal y la
   probabilidad del mejor pick, para que `integrar_pagina.py` no tenga
   que leer `raw/ev_result.json`.
   `data/semana-N/tabla-momios-semana-N.md`.
6. **`integrar_pagina.py`** — fragmento de integración revisado
   (lunes 23 nov 2026, orden del jefe): inyecta el bloque COMPLETO de
   momios por tarjeta (decimales + EV por mercado: 1X2, total con su
   línea, spread) entre un par de marcadores POR TARJETA
   `<!-- MOMIOS-INICIO:<slug> -->` / `<!-- MOMIOS-FIN:<slug> -->`,
   donde `<slug>` es `local-vs-visita` en minúsculas sin acentos
   (p. ej. `werder-bremen-vs-borussia-monchengladbach`). Trae su CSS
   (`--css-out`), que reusa las variables y clases de la página
   (`.odds`, `.derived-h`, `.dcell`, `.add-btn`). Por defecto es
   dry-run; si a un partido le falta su par de marcadores, falla sin
   tocar nada. Lee `data/semana-N/ev.json` (con `mercados`, ver punto
   5). No se usa en `index.html` hasta que el jefe ponga los
   marcadores; la prueba se hace en una copia con marcadores.
   También escribe el fragmento y el CSS sueltos con
   `--fragment-out` / `--css-out` para que el jefe los pegue.
7. **`run_semana.py`** — corre los pasos (0–6) en orden y valida
   el resultado (partidos verificados, 5 partidos por equipo — 4 en
   competiciones europeas, donde solo se han jugado 4 jornadas —, 1X2
   suma 100%, cada partido con momio tiene EV y semáforo, ningún
   partido pendiente tiene EV inventado). Si algo falla, no se publica
   nada. Antes de regenerar los momios guarda el ev.json vigente en
   `data/semana-N/ev-ayer.json` (solo la primera corrida del día) y
   después del EV corre el paso 6.
8. **`calcular_movimientos.py` + `run_movimientos.py`** — movimientos
   de momios, hoy vs ayer (orden del jefe, 23 nov 2026, primera de las
   6 propuestas). Por partido detecta: cambio de mejor pick, cambio de
   EV del mejor pick en puntos porcentuales con flecha ↑ (sube más de
   0.1 pp) / ↓ (baja más de 0.1 pp) / → (sin cambio), cambio de línea
   de total, y el EV de hoy del pick de ayer. También marca partidos
   nuevos, momios publicados hoy y partidos que siguen pendientes (sin
   EV inventado). Escribe `data/semana-N/movimientos.json`, que la
   página lee para la flecha por tarjeta. El "ayer" es
   `data/semana-N/ev-ayer.json` (lo guarda `run_semana.py`, ver punto
   7); a mano se puede usar cualquier ev.json anterior, p. ej. del
   historial git (`git show <commit>:data/semana-N/ev.json`), y el
   script acepta los ev.json viejos sin `mercados` (la línea se lee
   entonces de `momios.total.linea`). `integrar_pagina.py` con
   `--movimientos data/semana-N/movimientos.json` añade la línea
   `↑↓ ... vs ayer` a cada tarjeta del fragmento (CSS `.momios-mov`).
   Uso: `python3 scripts/run_movimientos.py` (las 3 semanas) o
   `python3 scripts/run_movimientos.py --ayer-commit <commit>` (prueba
   contra el historial).
9. **`descubrir_partidos.py`** — descubrimiento automático de partidos
   nuevos publicados tarde en ESPN (orden del jefe, 22 nov 2026, caso
   Liga MX): en cada corrida consulta los scoreboards de las ligas del
   alcance (mex.1, eng.1, esp.1, ger.1, ita.1, uefa.champions,
   uefa.europa; Conference League sin acceso en ESPN con los slugs
   probados) para la semana corriente (lun–dom) y compara con una línea
   base guardada en `raw/descubrimiento_vistos.json`. La primera
   corrida solo establece la línea base y no agrega nada (así una
   config curada no se llena de partidos que ya existían); en corridas
   posteriores, un partido que aparece nuevo se agrega al config y el
   pipeline completo corre para él. Nunca inventa partidos ni momios.
   Es el paso 0 de `run_semana.py`.

## Corrección obligatoria aplicada (jefe, 19 nov 2026)

El BTTS (ambos anotan) y el +2.5 se calculan con la distribución
completa, no sobre la tabla truncada de 0–7 goles. El error anterior
daba Real Madrid–Alavés 16.8% en vez de 21.1% correcto (BTTS), y el
+2.5 de ese mismo partido salía 72.7% en vez de 93.1%: con xG 5.61 la
cola de 8+ goles es del 20% y no se puede descartar. Verificado: con
los datos de la Semana 2, los 16 BTTS calculados aquí coinciden con los
valores corregidos del jefe (diferencia máxima 0.07 puntos, redondeo).

## Uso manual

```bash
# Semana actual (la que apunta scripts/config/semana-actual.json)
python3 scripts/run_semana.py --config scripts/config/semana-actual.json

# Una semana concreta
python3 scripts/run_semana.py --config scripts/config/semana-1.json
```

Los pasos también se pueden correr por separado:

```bash
python3 scripts/recolectar_datos.py --config scripts/config/semana-1.json
python3 scripts/calcular_poisson.py --config scripts/config/semana-1.json
python3 scripts/generar_tabla.py   --config scripts/config/semana-1.json
```

Salidas en `data/semana-N/`: `tabla-poisson-semana-N.md`,
`tabla-momios-semana-N.md`, `ev.json` y `raw/` con los JSON crudos de
ESPN (`scoreboard_*`, `odds_*`, `schedule_*`), `teams_last5.json`,
`league_avgs.json`, `verified_events.json`, `poisson_result.json`,
`momios.json` y `ev_result.json`.

## Cambiar de semana

1. Copiar la configuración de la semana nueva sobre
   `scripts/config/semana-actual.json` (o crear `semana-N.json` con sus
   partidos: fecha, liga, equipos y sus IDs de ESPN).
2. Correr `run_semana.py`. Los IDs de equipo se sacan del scoreboard de
   ESPN de la fecha del partido; no se adivinan. Para entre semana hay
   una config aparte (`semana-2-entresemana.json`, 12 partidos de
   Champions y Europa League, 24–26 nov) que no es la semana actual del
   workflow.

## GitHub Actions (Semana 7)

`.github/workflows/actualizar-poisson.yml` corre `run_semana.py` con la
semana actual:

- diario a las 13:00 UTC (07:00 CST),
- cada hora viernes, sábado y domingo (días de partido),
- manual (`workflow_dispatch`).

Si los datos cambiaron, hace commit de `data/` en la rama. Solo usa
`GITHUB_TOKEN`; no hay secretos ni claves: ESPN es API pública.

**Nota:** los workflows programados solo corren en la rama por defecto
(`main`). Este workflow se entrega en la rama `semana-3` para revisión
del jefe; empieza a correr solo cuando se fusione a `main`.

## Metodología (aprobada por el jefe, 19 nov 2026)

- Prom. por equipo = prom. total de goles por partido / 2.
- Ataque = (GF/n) / prom. por equipo; defensa = (GA/n) / prom. por equipo
  (n = partidos usados: 5 en ligas, 4 en competiciones europeas).
- xG local = prom. local × ataque local × defensa visitante;
  xG visitante = prom. visitante × ataque visitante × defensa local.
- Poisson P(k;λ) = e^-λ × λ^k / k!, k = 0..20 por equipo.
