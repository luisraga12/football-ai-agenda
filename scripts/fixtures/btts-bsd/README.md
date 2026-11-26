# Fixture BTTS-BSD (octava ronda, Tarea 1)

Fixture ilustrativo para probar el EV de BTTS con momios BSD en
`scripts/calcular_ev.py`. NO son datos reales: los momios BSD
(1.80/2.00 y 2.10/1.75) y los momios de ESPN son inventados para la
prueba. La única probabilidad real es la p_btts de Werder Bremen
(54.2486, de `data/semana-2/ev.json` de la corrida diaria #27).

## Partidos del fixture

1. Werder Bremen - Borussia Mönchengladbach (con_momio, con bsd):
   p_btts 54.2486, btts BSD sí 1.80 / no 2.00.
   Esperado: momios {"si": 1.8, "no": 2.0}; ev.si = -0.0235252;
   ev.no = -0.084972.
2. Venezia - Bologna (pendiente, con bsd): p_btts 60.0,
   btts BSD sí 2.10 / no 1.75. Esperado: momios {"si": 2.1, "no": 1.75};
   ev.si = 0.26; ev.no = -0.30.
3. Nottingham Forest - Chelsea (con_momio, sin bsd): p_btts 50.0.
   Esperado: momios null; ev {"si": null, "no": null}.

## Cómo se corre

Desde la raíz del repo:

    mkdir -p /tmp/btts-bsd/raw
    cp scripts/fixtures/btts-bsd/raw/momios.json /tmp/btts-bsd/raw/momios.json
    cp scripts/fixtures/btts-bsd/raw/poisson_result.json /tmp/btts-bsd/raw/poisson_result.json
    python3 scripts/calcular_ev.py --config scripts/fixtures/btts-bsd/config.json --out /tmp/btts-bsd

Revisar en /tmp/btts-bsd/ev.json los mercados.btts de los tres
partidos y compararlos con los valores esperados de arriba.

Fórmula del jefe: ev.si = p_btts x momio_si - 1;
ev.no = p_no_btts x momio_no - 1 (probabilidades en tanto por uno).