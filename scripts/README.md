# Automatización: datos ESPN + modelo Poisson

Scripts del Empleado 1 (datos y modelo Poisson) para generar la tabla de
probabilidades de cada semana **sin hacerlo a mano** y sin tocar la
interfaz (`index.html` no se toca en este trabajo).

## Qué hace

1. **`recolectar_datos.py`** — descarga de la API pública de ESPN (sin
   clave):
   - los scoreboards de cada liga y fecha, y **valida que los 16 partidos
     de la semana existan en ESPN** (por ID de equipo). Si falta uno, el
     script falla y no se calcula nada: no se inventa ningún dato.
   - el schedule de cada equipo: sus últimos 5 partidos de liga
     completados hasta el cutoff de la configuración.
   - los promedios de cada liga desde los scoreboards de las últimas ~3
     jornadas completadas antes del cutoff (el endpoint de standings de
     ESPN devuelve 404).
2. **`calcular_poisson.py`** — ataque, defensa, goles esperados (xG) y
   probabilidades 1X2, +2.5 y BTTS con la **distribución Poisson
   completa** (rejilla 0–20 goles, ver `poisson_core.py`).
3. **`generar_tabla.py`** — escribe `data/semana-N/tabla-poisson-semana-N.md`
   con la tabla de partidos, la tabla por equipo, los promedios de liga,
   las fuentes y los datos no verificados.
4. **`run_semana.py`** — corre los tres pasos en orden y valida el
   resultado (16 partidos verificados, 5 partidos por equipo, 1X2 suma
   100%). Si algo falla, no se publica nada.

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

Salidas en `data/semana-N/`: `tabla-poisson-semana-N.md` y
`raw/` con los JSON crudos de ESPN (`scoreboard_*`, `schedule_*`),
`teams_last5.json`, `league_avgs.json`, `verified_events.json` y
`poisson_result.json`.

## Cambiar de semana

1. Copiar la configuración de la semana nueva sobre
   `scripts/config/semana-actual.json` (o crear `semana-N.json` con sus
   16 partidos: fecha, liga, equipos y sus IDs de ESPN).
2. Correr `run_semana.py`. Los IDs de equipo se sacan del scoreboard de
   ESPN de la fecha del partido; no se adivinan.

## GitHub Actions (Semana 7)

`.github/workflows/actualizar-poisson.yml` corre `run_semana.py` con la
semana actual:

- diario a las 13:00 UTC (07:00 CST),
- cada hora viernes, sábado y domingo (días de partido),
- manual (`workflow_dispatch`).

Si los datos cambiaron, hace commit de `data/` en la rama. Solo usa
`GITHUB_TOKEN`; no hay secretos ni claves: ESPN es API pública.

**Nota:** los workflows programados solo corren en la rama por defecto
(`main`). Este workflow se entrega en la rama `semana-2` para revisión
del jefe; empieza a correr solo cuando se fusione a `main`.

## Metodología (aprobada por el jefe, 19 nov 2026)

- Prom. por equipo = prom. total de goles por partido / 2.
- Ataque = (GF/5) / prom. por equipo; defensa = (GA/5) / prom. por equipo.
- xG local = prom. local × ataque local × defensa visitante;
  xG visitante = prom. visitante × ataque visitante × defensa local.
- Poisson P(k;λ) = e^-λ × λ^k / k!, k = 0..20 por equipo.
