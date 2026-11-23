# Forma de trabajar — Football AI Agenda (y futuros proyectos)

Definida por el cliente, Luis, el 19 nov 2026. Vale para este proyecto y para los que vienen. El jefe (Muse) la aplica y decide los detalles. Actualizada el 23 nov 2026 con las reglas de trabajo ordenado y el cambio de la comunicación al buzón.

## 1. Sacarle el mayor jugo a cada semana, según el límite

El cliente tiene un límite semanal en Muse. El jefe organiza el trabajo de cada semana para aprovechar ese límite de manera inteligente: el trabajo se planea por semana, en paquetes con entregas concretas, y no se gasta el límite en revisiones innecesarias ni en vueltas sin resultado. Si algo se puede resolver en un solo paso, se resuelve en un solo paso.

## 2. Comunicación del equipo: en el buzón

La comunicación del equipo vive en el repo privado **buzón** (https://github.com/luisraga12/buzón). Ya NO va en `football-ai-agenda`.

- `JEFE.md` — solo el jefe escribe: órdenes, revisiones y correcciones.
- `EMPLEADO-1.md` — solo el Empleado 1 escribe: avances, entregas, preguntas.
- `EMPLEADO-2.md` — solo el Empleado 2 escribe: avances, entregas, preguntas.
- `PLAN.md` — el plan semanal y las metas del cliente (vive en `football-ai-agenda`).
- Este archivo — la forma de trabajar (vive en `football-ai-agenda`).

Los empleados leen `JEFE.md` antes de empezar a trabajar y después de cada entrega. Los planes se comunican por el archivo `.md` que le toca a cada quien, no en archivos de órdenes aparte: el jefe pone las órdenes y los planes en `JEFE.md`, y cada empleado pone sus avances, entregas y preguntas en su propio archivo.

## 3. Avisos por commit, no revisión cada rato

Para no gastar el límite, nadie está revisando el repo cada rato. La regla es: cuando alguien haga un commit o escriba un mensaje en su archivo, se avisa y el jefe o el empleado que toque revisa. La notificación automática (que les avise solos cuando alguien suba algo) es parte del proyecto futuro tipo WhatsApp que el cliente quiere hacer después de este proyecto.

## 4. GitHub ordenado

- Una rama por tarea, con nombre claro (`semana-3`, `detalle-partido`; no `prueba`, `final2`, `copia`).
- Cambios por PR con revisión del jefe; nada directo a `main`.
- Se trabaja SIEMPRE sobre la base real (`main` o la rama de la tarea). Nada de reconstruir copias de la página o del proyecto: lo que se entrega es la base con el cambio aplicado, y el jefe lo verifica tarjeta por tarjeta / archivo por archivo.
- Commits descriptivos (qué se hizo y por qué), en español como el resto del repo.
- Al fusionar una rama, se borra. Ramas viejas sin borrar no se acumulan.
- En la raíz solo van los archivos necesarios: `README.md`, `PLAN.md`, `FORMA-DE-TRABAJAR.md`, `index.html` y las carpetas del proyecto (`scripts/`, `data/`, `.github/`). Nada de `.md` sueltos de mensajes ni previews viejos: los previews temporales se borran al publicarse.
- Cada semana terminada se marca como hecha en `PLAN.md`.
- El jefe es también el tester: nada se sube a `main` sin correrlo, validarlo (con parser donde aplique, no solo a ojo) y verificarlo en vivo.

## 5. Permisos en GitHub

- El jefe tiene permiso total del GitHub: puede subir cosas al repo sin pedirle permiso al cliente.
- Los empleados, si necesitan subir algo al repo, lo suben; o bien trabajan cada uno en su rama y suben ahí sin pedir permiso. El jefe revisa y decide qué pasa a `main`.
- El jefe decide. Si algo no está claro, lo resuelve el jefe y solo sube al cliente lo que necesite de él.

## 6. Laravel y código ordenado (seguridad y mantenimiento)

- Autenticación con lo que trae Laravel (o Sanctum para API); contraseñas siempre con hash, nunca en claro.
- Validar TODO lo que entra (Form Requests / validación en controlador): nada de confiar en lo que manda el cliente.
- Protección contra inyección SQL usando Eloquent / query builder con parámetros; nunca concatenar datos del usuario en SQL crudo.
- CSRF activo en formularios web; XSS controlado con Blade (escape por defecto, nada de `{!! !!}` con datos del usuario).
- Permisos con policies y middleware (quién puede hacer qué, en el servidor, no solo escondiendo botones).
- Base de datos con migraciones (nada de crear tablas a mano en el servidor), llaves foráneas, transacciones donde una operación toca varias tablas, y respaldos periódicos.

## 7. Base de datos de verdad, no JSON

- Un archivo JSON sirve para una demo estática o para datos de prueba que casi no cambian. No es una base de datos.
- En cuanto hay usuarios, registros, búsquedas o dos personas escribiendo a la vez, va MySQL o PostgreSQL (SQLite solo para desarrollo local o prototipos de un usuario), con migraciones y relaciones.
- El JSON queda solo para lo que es: configuración, semillas de datos o intercambio entre sistemas, nunca como única fuente de verdad de una app con escrituras.

## 8. Otros stacks

Laravel es el stack principal de Luis, pero la regla es la misma en cualquier tecnología: framework con su forma ordenada de hacer las cosas (Symfony, Django, FastAPI, NestJS, etc.), base de datos real, migraciones, validación, autenticación y pruebas antes de entregar. Si un proyecto pide otro stack, se hace en ese stack, con estas mismas reglas.

## 9. El cliente recibe resultados

El cliente es el cliente, no es del equipo. Recibe el producto funcionando cada semana y pide las mejoras de cómo quiere su página. Solo se le molesta cuando se necesita algo suyo (su correo, una clave, un permiso) o para entregarle.
