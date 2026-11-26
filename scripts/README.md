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
   que leer `raw/ev_result.json`. Desde el 24 nov `mercados` también
   trae `btts` con su probabilidad Poisson completa (p_btts y
   p_no_btts) en TODOS los partidos, con momio o sin él; sin momio ni
   EV porque ESPN/DraftKings no trae ese momio en esta fuente.
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
   EV inventado). Escribe `data/semana-N/movimientos.json`, que
   `integrar_pagina.py` lee para poner la flecha por tarjeta en el
   fragmento (la página en vivo aún no lo lee sola; eso es Semana 7).
   El "ayer" es `data/semana-N/ev-ayer.json` (lo guarda `run_semana.py`, ver punto
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
   Liga MX) y completar la jornada (orden del jefe, 24 nov 2026,
   JEFE.md 4531da0): en cada corrida consulta los scoreboards de las
   ligas del alcance (mex.1, eng.1, esp.1, ger.1, ita.1, uefa.champions,
   uefa.europa; Conference League sin acceso en ESPN con los slugs
   probados) para la semana corriente (lun–dom) y compara con el
   CONFIG: todo partido de ESPN para las fechas y ligas del propio
   config que no esté en el config se agrega, y el pipeline completo
   corre para él. Un partido ya terminado en ESPN (estado 'post') no
   se agrega: la jornada que se completa es la que falta por jugarse
   (los 5 de Champions del mar 24 nov 2026 ya jugados no entran).
   La línea base guardada en
   `raw/descubrimiento_vistos.json` se sigue actualizando como registro
   de lo visto, pero ya no decide nada (antes solo cazaba partidos
   publicados después de la línea base; la primera corrida solo la
   establecía y no agregaba nada). Nunca inventa partidos ni momios.
   Es el paso 0 de `run_semana.py`. **Solo se agregan partidos cuya
   fecha está en las fechas del propio config y cuya liga está en las
   ligas del propio config**: así un partido de entre semana no entra
   al config de fin de semana ni al revés (las fechas 24–26 y 27–29
   no se solapan) y el mismo partido no aparece en los dos configs; una
   liga que no esté en las ligas del config no se descubre. **Flag
   `completar_jornada` (orden del jefe, 25 nov 2026, JEFE.md 437b004):
   con `completar_jornada: false` en el config, el descubrimiento NO
   agrega nada a ese config (se queda curado en los partidos que
   tiene); la línea base se sigue actualizando como registro y el log
   dice cuántos se habrían agregado. Sin la clave (o en true), se
   completa la jornada como siempre. El fin de semana
   (`semana-actual.json`, 20 partidos) lleva el flag en false: la
   corrida de las 07:00 no debe completarlo solo a 40.** **El cambio
   al config debe commitearse** (`git add data/ scripts/config/` en el
   workflow): lección de la Liguilla, 24 nov 2026 — la corrida c892956
   descubrió los 8 cuartos de final y los puso en el ev.json, pero el
   workflow solo commiteaba `data/` y el cambio al config se perdió; la
   línea base ya los traía, así que en la siguiente corrida no se
   re-agregaron y el pipeline los sacó del ev.json.
10. **`calcular_tendencias.py` + `run_tendencias.py`** — tendencias por
   mercado (orden del jefe, 23 nov 2026, segunda de las 6 propuestas).
   Por partido, la racha de cada equipo en sus últimos 5 partidos de
   liga (4 en competiciones europeas: entre semana), la misma ventana
   que el Poisson, sacada de `raw/teams_last5.json`:
   1X2 (G/E/P), total contra la línea publicada del partido (si el
   partido sigue pendiente sin línea, referencia 2.5, marcada en el
   JSON), BTTS sí/no como conteo de resultados (NO son momios: ESPN
   no da momios de BTTS), y spread aplicando la línea publicada del
   partido a los últimos 5 del equipo (sin distinguir si en esos
   partidos fue local o visita; si no hay línea de spread, no hay
   tendencia de spread). Escribe `data/semana-N/tendencias.json`
   con una `linea_tarjeta` por partido; `integrar_pagina.py` con
   `--tendencias data/semana-N/tendencias.json` la añade a cada
   tarjeta del fragmento (CSS `.momios-tend`), también a las
   pendientes, porque las tendencias no necesitan momios. Es el paso
   7 de `run_semana.py`. Uso: `python3 scripts/run_tendencias.py`
   (las 3 semanas) o `python3 scripts/run_tendencias.py --semanas
   semana-2`.

11. **`calcular_historial.py` + `run_historial.py`** — historial de
    aciertos del modelo (orden del jefe, 23 nov 2026, tercera de las
    6 propuestas; rutina fija de cada lunes). Compara lo que el
    modelo pronosticó en `data/semana-N/tabla-poisson-semana-N.md`
    con los resultados reales de los scoreboards en
    `data/semana-N/raw/` (solo partidos con status completed) y
    escribe `data/semana-N/historial.json` +
    `data/semana-N/historial.html` (sección "Cómo le fue al modelo",
    con marcadores `HISTORIAL-INICIO/FIN:<semana>`; la coloca el
    jefe, no toca index.html). Definiciones: favorito 1X2 (el 1/X/2
    con mayor P; se publica el número tal cual, sin esconderlo:
    Semana 1, 6/16); Más 2.5 solo cuando P(+2.5) > 50% y Menos 2.5
    cuando <= 50%; BTTS / No-BTTS como conteos de resultados (NO
    momios). Si un partido no trae resultado final en el raw, se
    usa `data/semana-N/resultados_verificados.json` (cada entrada
    con su fuente y fecha de verificación; queda registrada por
    partido en `fuente_resultado`); sin raw ni verificado, el
    partido queda "sin resultado" y no entra en los denominadores.
    **Se corre a mano el lunes, cuando la semana ya se jugó: NO va
    en el flujo diario de `run_semana.py`** (ahí los partidos aún
    no se juegan). Cada lunes se corre `python3
    scripts/run_historial.py --semanas semana-N` con la semana
    recién jugada y el historial crece con sus resultados. Uso:
    `python3 scripts/run_historial.py` (por defecto solo semana-1).

12. **`generar_vivo.py`** — marcador en vivo con caché (propuesta del
    jefe en JEFE.md, commit e0016b3, 24 nov 2026; diseño detallado en
    `propuesta-vivo-cache.md`). Lee la semana actual + entre semana,
    pide los scoreboards de ESPN de hoy (site.api, con respaldo
    site.web.api) y escribe `data/vivo.json` con marcador, minuto y
    estado de los 28 partidos de la semana. Mezcla con el último dato
    conocido (cada entrada con su `actualizado_en`); si TODAS las
    consultas fallan, no toca el archivo anterior y sale con código 1;
    los fallos quedan en `data/vivo-log.json` (últimas 50). Lo corre el
    workflow `.github/workflows/actualizar-vivo.yml` cada 5 min solo en
    ventanas de partido (ver el archivo: 3 crons en UTC + la estimación
    de minutos de Actions). Uso: `python3 scripts/generar_vivo.py`
    (solo hoy) o `--todas` (toda la semana, para probar).

13. **`calcular_alineacion_probable.py`** — prototipo Semana 6
    (alineación probable, orden del jefe, 24 nov 2026). Para cada
    partido de la semana estima el XI más frecuente por posición de
    los últimos partidos + la formación más usada, siempre marcado
    como PROBABLE (ESPN no publica XI probable). Ventana: últimos 5
    de liga doméstica (fin de semana) o últimos 4 de la competición
    UEFA (entre semana), antes de la fecha del partido — misma
    ventana que el Poisson. Fuentes: schedule del equipo y summary
    por evento de ESPN (site.api, respaldo site.web.api); los
    summaries se guardan en `data/<semana>/raw/summary_*.json`
    (raw/ no se sube). El XI se elige por titularidades (desempate:
    minutos estimados de sustituciones, luego titularidad más
    reciente); la formación es la (D-M-F) más frecuente en la
    ventana. Aplica el MAPEO conocido de nombres de otros clubes
    (Arsenal / Real Madrid, ver `corregir_nombres_xi.py`) y deja en
    `revisiones` a cualquier titular que no esté en la plantilla de
    temporada. Si un equipo no tiene datos, queda pendiente, no se
    inventa nada. Uso:
    `python3 scripts/calcular_alineacion_probable.py --config scripts/config/semana-2.json --out data/semana-2/alineacion-probable.json`
    (y lo mismo con `semana-2-entresemana.json`). Cada XI trae
    `fuerza` (corrección del jefe, 24 nov 2026): valor 0–100 y los 3
    componentes con fracciones (goles+asistencias / minutos /
    puntos, cada uno vs el mejor XI 1-4-4-2 por minutos de la misma
    ventana), pesos 0.40/0.30/0.30, cada componente topado en 100;
    calculada con los nombres ESPN antes del MAPEO. Puntos: 3/1/0
    del partido para todo jugador que jugó (titular o suplente con
    minutos > 0). Es el paso 8 de `run_semana.py` desde la Semana 7
    (un partido descubierto en el paso 0 también lleva su XI
    probable con Fuerza). Verificación de nombres (24 nov 2026): los ~50
    nombres señalados por el jefe se verificaron uno por uno contra
    los fichajes del verano 2026 y los datos — los 60 son jugadores
    reales del equipo asignado, así que no se añadió ningún
    reemplazo al MAPEO (detalle con fuentes en EMPLEADO-1.md).
14. **`calcular_estadisticas.py`** — estadísticas del partido terminado
    (Semana 9, orden del jefe, 25 nov 2026, JEFE.md 437b004 + da79093).
    Para cada partido con estado 'post' en ESPN descarga el resumen
    (`summary?event=<id>`) y publica `data/<config>/estadisticas.json`
    en el formato que espera `partido.html` (comentario ~línea 1274):
    10 estadísticas (posesión, tiros, tiros a puerta, córners, faltas,
    fueras de juego, tarjetas amarillas, tarjetas rojas, pases
    precisos, paradas). "duelos_ganados" NO se publica: el resumen de
    ESPN no trae duelos (verificado en summaries de Champions y Liga
    MX). Un partido terminado sin resumen o sin boxscore queda fuera
    del archivo; la página muestra "Estadísticas pendientes", sin
    ceros inventados. Es el paso 9 de `run_semana.py`.
15. **`completar_teams_last5.py`** — completa `raw/teams_last5.json`
    con los equipos del config que faltan (Semana 9, orden del jefe,
    25 nov 2026, JEFE.md da79093). Reutiliza la lógica exacta de
    `recolectar_datos.py` paso 2 (mismo cutoff del config, últimos 5
    completados antes del cutoff, 4 en competiciones UEFA) y no toca
    los equipos ya presentes. Guarda también
    `raw/schedule_<liga>_<id>.json` por equipo nuevo. Uso:
    `python3 scripts/completar_teams_last5.py --config scripts/config/semana-2-entresemana.json`.
    (La corrida diaria regenera el archivo completo de todos modos en
    el paso 1; este script es para completarlo sin re-correr todo.)

**Fecha de cálculo en México:** todos los JSON que generan fecha
(`fecha_calculo`, `fecha_hoy`) usan hora de México
(`America/Mexico_City`, `ZoneInfo`), no la de la VM, que va en UTC
y sacaba la fecha un día adelante (el jefe lo señaló en la
revisión de Tendencias, 23 nov). Si un script nuevo genera una
fecha, que use `fecha_mexico()` como en `calcular_historial.py` y
`calcular_tendencias.py`.

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

- diario a las 13:17 UTC (07:17 CST),
- cada hora viernes, sábado y domingo (días de partido),
- manual (`workflow_dispatch`).

Si los datos cambiaron, hace commit de `data/` en la rama. Solo usa
`GITHUB_TOKEN`; no hay secretos ni claves: ESPN es API pública.

**Ojo (Semana 7):** el commit también incluye `scripts/config/`
(`git add data/ scripts/config/`), porque el descubrimiento (paso 0)
modifica el config cuando ESPN publica un partido tarde. Si solo se
commitea `data/`, el cambio al config se pierde en la siguiente
corrida y el partido descubierto desaparece del ev.json (lección de
la Liguilla, 24 nov 2026).

**Nota:** los workflows programados solo corren en la rama por defecto
(`main`).

## Metodología (aprobada por el jefe, 19 nov 2026)

- Prom. por equipo = prom. total de goles por partido / 2.
- Ataque = (GF/n) / prom. por equipo; defensa = (GA/n) / prom. por equipo
  (n = partidos usados: 5 en ligas, 4 en competiciones europeas).
- xG local = prom. local × ataque local × defensa visitante;
  xG visitante = prom. visitante × ataque visitante × defensa local.
- Poisson P(k;λ) = e^-λ × λ^k / k!, k = 0..20 por equipo.
