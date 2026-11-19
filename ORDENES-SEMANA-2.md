# Órdenes — Semana 2 (modelo Poisson)

Jefe: Muse. Empleados: los 2 agentes de programación en Muse Code.
Luis (dueño) les pasa estas órdenes. El jefe revisa y prueba lo que entregan
antes de subirlo a `main`.

## Reglas para los dos (obligatorias)

- Trabajar en la rama `semana-2`, nunca directo en `main`. Al terminar,
  hacer push de la rama y avisar al jefe. El jefe hace el merge a `main`.
- No inventar ningún dato: ni resultados, ni momios, ni probabilidades,
  ni goles. Todo sale de ESPN (ver abajo) o se calcula con la fórmula dada.
- No poner API keys, tokens ni credenciales en ningún archivo ni en el repo.
- No cambiar el diseño, los colores ni el CSS de la página: editar solo lo
  necesario en `index.html`, de forma quirúrgica.
- La página sigue siendo estática: los datos van integrados en `index.html`.

## Partidos del fin de semana 27–29 nov 2026 (verificados en ESPN, horas de Monterrey)

Hay 37 partidos en las 5 ligas; la agenda lleva solo 16, como en la Semana 1.
Elegir 16 con este criterio: los más importantes (clásicos, derbis y equipos
de arriba) y repartidos en los 3 días. Anotar en el reporte cuáles se eligieron
y por qué. No hay partidos de Liga MX ese fin de semana en ESPN.

### Viernes 27 nov

- 13:30 — Werder Bremen vs Borussia Mönchengladbach (Bundesliga)
- 13:45 — Venezia vs Bologna (Serie A)
- 14:00 — Nottingham Forest vs Chelsea (Premier League)
- 14:00 — Levante vs Racing Santander (LaLiga)

### Sábado 28 nov

- 07:00 — Real Betis vs Rayo Vallecano (LaLiga)
- 08:00 — Frosinone vs Parma (Serie A)
- 08:30 — FC Cologne vs SV Elversberg (Bundesliga)
- 08:30 — Hamburg SV vs Bayern Munich (Bundesliga)
- 08:30 — Mainz vs 1. FC Union Berlin (Bundesliga)
- 08:30 — SC Paderborn 07 vs Schalke 04 (Bundesliga)
- 09:00 — Leeds United vs Coventry City (Premier League)
- 09:00 — Manchester United vs Brentford (Premier League)
- 09:15 — Málaga vs Athletic Club (LaLiga)
- 11:00 — Torino vs Lazio (Serie A)
- 11:30 — Ipswich Town vs Aston Villa (Premier League)
- 11:30 — Elche vs Atlético Madrid (LaLiga)
- 11:30 — VfB Stuttgart vs Eintracht Frankfurt (Bundesliga)
- 13:45 — Internazionale vs Genoa (Serie A)
- 14:00 — Real Madrid vs Alavés (LaLiga)

### Domingo 29 nov

- 05:30 — Udinese vs Fiorentina (Serie A)
- 06:00 — Everton vs Liverpool (Premier League)
- 07:00 — Valencia vs Osasuna (LaLiga)
- 08:00 — Sassuolo vs Napoli (Serie A)
- 08:05 — Brighton vs Newcastle United (Premier League)
- 08:05 — Crystal Palace vs Hull City (Premier League)
- 08:05 — Fulham vs AFC Bournemouth (Premier League)
- 08:05 — Sunderland vs Tottenham Hotspur (Premier League)
- 08:30 — SC Freiburg vs RB Leipzig (Bundesliga)
- 09:15 — Deportivo vs Barcelona (LaLiga)
- 10:30 — Arsenal vs Manchester City (Premier League)
- 10:30 — TSG Hoffenheim vs FC Augsburg (Bundesliga)
- 11:00 — AS Roma vs Monza (Serie A)
- 11:30 — Celta Vigo vs Villarreal (LaLiga)
- 12:30 — Borussia Dortmund vs Bayer Leverkusen (Bundesliga)
- 13:45 — Como vs Juventus (Serie A)
- 14:00 — Real Sociedad vs Sevilla (LaLiga)

## Empleado 1 — Datos y modelo Poisson

1. Para cada uno de los 16 equipos elegidos, sacar de ESPN (endpoint
   `summary` de cada partido o `schedule` de cada equipo) sus últimos
   5 partidos: goles a favor y en contra.
2. Calcular la fuerza de ataque y de defensa de cada equipo contra el
   promedio de su liga: ataque = goles a favor por partido / promedio de
   goles por partido de la liga; defensa = goles en contra por partido /
   promedio de goles por partido de la liga.
3. Goles esperados: local = promedio de goles de local de la liga x ataque
   local x defensa visitante; visitante = promedio de goles de visitante
   de la liga x ataque visitante x defensa local.
4. Con la distribución de Poisson (goles de 0 a 7 por equipo), calcular por
   partido: probabilidad de victoria local, de empate y de victoria
   visitante, probabilidad de más de 2.5 goles y probabilidad de que ambos
   anoten. Las 3 de 1X2 deben sumar 100%.
5. Entregar una tabla con los 16 partidos y sus probabilidades calculadas,
   para que el jefe la revise antes de ponerla en la página.

## Empleado 2 — Interfaz y pruebas

1. Reemplazar las 16 tarjetas de la Semana 1 por los 16 partidos elegidos
   (fechas 27–29 nov, horas de Monterrey).
2. Mostrar en cada tarjeta las probabilidades del modelo Poisson (1X2 en %,
   y más de 2.5 goles y ambos anotan donde quepan), sin inventar momios:
   los momios llegan en la Semana 3.
3. Actualizar el encabezado de fecha, el contador "Todas 16" y la nota de
   datos verificados a 19 nov 2026 (partidos del 27–29 nov).
4. Probar antes de avisar al jefe: 16 tarjetas correctas, filtros por liga
   y por estado funcionando, probabilidades sumando 100% en cada partido,
   sin la palabra "Ejemplo" y sin claves ni llamadas a ninguna API en la página.

## Criterio de aceptación (lo revisa el jefe)

- 16 partidos reales, horas correctas, probabilidades Poisson con su tabla
  de cálculo, filtros funcionando y cero datos inventados.
- Si algo no se puede verificar con ESPN, se deja fuera y se reporta,
  no se inventa.
