"""Descargas HTTP con reintentos para el Football AI Agenda.

Motivo (27 nov 2026): la corrida #30 de "Actualizar datos, Poisson,
momios y EV" fallo por un error TRANSITORIO de red al bajar datos de
ESPN — `urllib.error.URLError: [SSL: CERTIFICATE_VERIFY_FAILED]`
precedido por `ssl.SSLCertVerificationError: [SSL: TLSV1_ALERT_INTERNAL_ERROR]`
en scripts/recolectar_datos.py (linea 131, schedule de un equipo).
El paso fallo con exit 1 y no se publico nada; la corrida manual #31
despues si funciono. Un solo intento por URL no aguanta un error
pasajero: este modulo reintenta solo los errores transitorios.

Reglas:
  - TRANSITORIOS (se reintentan): errores de red/SSL/timeout
    (URLError, SSLError, ConnectionError, TimeoutError,
    http.client.RemoteDisconnected) y HTTP 429 o 5xx. El error de la
    corrida #30 es URLError envolviendo un SSLError: transitorio.
  - PERMANENTES (NO se reintentan, fallan a la primera): HTTP 404,
    400, 401, 403 y datos malformados (JSONDecodeError). Reintentarlos
    no los arregla y solo quema tiempo y cuota.
  - Espera creciente (backoff exponencial) con un poco de jitter:
    2s, 4s, 8s entre intentos (max ~14s por URL que falla).
    Por defecto 4 intentos en total.

Uso en los scripts del pipeline (se importa igual en todos):
    from http_resiliente import descargar_json
    datos = descargar_json(url)  # lanza la ultima excepcion si agota

Para los call sites que ya son fail-soft (devuelven None si falla,
p. ej. generar_mapas.py / calcular_alineacion_probable.py):
    from http_resiliente import descargar_json_o_none
    datos = descargar_json_o_none(url)  # None si agota o es permanente
"""

import json
import random
import ssl
import sys
import time
import urllib.error
import urllib.request
from http.client import RemoteDisconnected

INTENTOS = 4            # intentos totales por URL (1 + 3 reintentos)
ESPERA_BASE = 2.0       # segundos antes del 1er reintento; luego x2
TIMEOUT_DEF = 30        # segundos por intento (igual que antes)
UA = "Mozilla/5.0"


def es_transitorio(exc):
    """True si el error es pasajero y vale la pena reintentar.

    HTTPError es subclase de URLError: se revisa primero, porque un
    404 no es transitorio aunque sea un URLError.
    """
    if isinstance(exc, urllib.error.HTTPError):
        return exc.code == 429 or 500 <= exc.code < 600
    if isinstance(exc, urllib.error.URLError):
        return True
    if isinstance(exc, (ssl.SSLError, ConnectionError, TimeoutError,
                        RemoteDisconnected)):
        return True
    return False


def _abrir(url, timeout, headers, opener):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
    if opener is not None:
        with opener.open(req, timeout=timeout) as r:
            return json.load(r)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def descargar_json(url, timeout=TIMEOUT_DEF, intentos=INTENTOS,
                   espera_base=ESPERA_BASE, headers=None, opener=None):
    """GET con reintentos solo para errores transitorios.

    Devuelve el JSON. Si el error es permanente, lanza a la primera.
    Si agota los intentos, lanza la ultima excepcion (el llamador
    decide: el pipeline falla como antes, o el call site fail-soft
    devuelve None).
    """
    ultimo = None
    for intento in range(1, intentos + 1):
        try:
            return _abrir(url, timeout, headers, opener)
        except Exception as exc:  # noqa: BLE001 - se clasifica abajo
            ultimo = exc
            if not es_transitorio(exc):
                raise
            if intento == intentos:
                break
            espera = espera_base * (2 ** (intento - 1)) + random.uniform(0, 0.5)
            print(f"  REINTENTO {intento}/{intentos} {url} "
                  f"({exc}); esperando {espera:.1f}s",
                  file=sys.stderr)
            time.sleep(espera)
    raise ultimo


def descargar_json_o_none(url, timeout=TIMEOUT_DEF, intentos=INTENTOS,
                          espera_base=ESPERA_BASE, headers=None,
                          opener=None):
    """Como descargar_json, pero devuelve None si falla (fail-soft)."""
    try:
        return descargar_json(url, timeout=timeout, intentos=intentos,
                              espera_base=espera_base, headers=headers,
                              opener=opener)
    except Exception as exc:  # noqa: BLE001 - fail-soft deliberado
        print(f"  AVISO: no se pudo bajar {url} ({exc})", file=sys.stderr)
        return None
