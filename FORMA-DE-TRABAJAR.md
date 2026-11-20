# Forma de trabajar — Football AI Agenda (y futuros proyectos)

Definida por el cliente, Luis, el 19 nov 2026. Vale para este proyecto y
para los que vienen. El jefe (Muse) la aplica y decide los detalles.

## 1. Sacarle el mayor jugo a cada semana, según el límite

El cliente tiene un límite semanal en Muse. El jefe organiza el trabajo
de cada semana para aprovechar ese límite de manera inteligente: el
trabajo se planea por semana, en paquetes con entregas concretas, y no
se gasta el límite en revisiones innecesarias ni en vueltas sin
resultado. Si algo se puede resolver en un solo paso, se resuelve en
un solo paso.

## 2. Comunicación por GitHub

La comunicación del equipo es por el repo:

- `JEFE.md` — solo el jefe escribe: órdenes, revisiones y correcciones.
- `EMPLEADO-1.md` — solo el Empleado 1 escribe: avances, entregas,
  preguntas.
- `EMPLEADO-2.md` — solo el Empleado 2 escribe: avances, entregas,
  preguntas.
- `PLAN.md` — el plan semanal y las metas del cliente.
- Este archivo — la forma de trabajar.

Los empleados leen `JEFE.md` antes de empezar a trabajar y después de
cada entrega. El cliente solo pasa los avisos entre el jefe y los
empleados; el equipo se comunica entre sí por estos archivos.

Los planes se comunican por el archivo `.md` que le toca a cada quien,
no en archivos de órdenes aparte: el jefe pone las órdenes y los planes
en `JEFE.md`, y cada empleado pone sus avances, entregas y preguntas en
su propio archivo. Así no hacen falta archivos sueltos de órdenes.

## 3. Avisos por commit, no revisión cada horas

Para no gastar el límite, nadie está revisando el repo cada rato. La
regla es: cuando alguien haga un commit o escriba un mensaje en su
archivo, se avisa y el jefe o el empleado que toque revisa. La
notificación automática (que les avise solos cuando alguien suba algo)
es parte del proyecto futuro tipo WhatsApp que el cliente quiere hacer
después de este proyecto.

## 4. Permisos en GitHub

- El jefe tiene permiso total del GitHub: puede subir cosas al repo
  sin pedirle permiso al cliente.
- Los empleados, si necesitan subir algo al repo, lo suben; o bien
  trabajan cada uno en su rama (por ejemplo `semana-2`) y suben ahí sin
  pedir permiso. El jefe revisa y decide qué pasa a `main`.
- El jefe decide. Si algo no está claro, lo resuelve el jefe y solo
  sube al cliente lo que necesite de él.

## 5. El cliente recibe resultados

El cliente es el cliente, no es del equipo. Recibe el producto
funcionando cada semana y pide las mejoras de cómo quiere su página.
Solo se le molesta cuando se necesita algo suyo (su correo, una clave,
un permiso) o para entregarle.
