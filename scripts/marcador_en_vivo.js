/**
 * Marcador en vivo — caché primero (24 nov 2026, port del jefe).
 *
 * Port de la implementación del Empleado 2 (rama empleado-2, commit
 * 8648af3, preview-semana-5-vivo-ui.html) a la página real. El módulo
 * lee primero el caché del workflow (data/vivo.json, contrato del
 * Empleado 1) y usa el fetch directo a ESPN como respaldo.
 *
 * Los 4 estados y sus textos exactos son los de la propuesta aprobada
 * del Empleado 2 (revisión del jefe, 24 nov 2026):
 *   - caché fresco:  "Minuto 35' · Actualizado hace 3 min"
 *   - caché viejo:   "Minuto 23' · Último dato conocido hace 12 min,
 *                     ESPN no responde, reintentando…"
 *   - sin caché + directo: "En vivo, actualizado hace menos de 1 min"
 *   - todo fallando: "Sin marcador en vivo por ahora. ESPN no responde
 *                     y aún no hay datos guardados. Se reintenta solo
 *                     cada minuto."
 * Ningún estado muestra errores crudos ("ESPN 400",
 * "Failed to get events endpoint"): el error del fetch queda interno.
 *
 * Adaptaciones del port (no son de la copia de E2):
 *   - La copia de E2 solo cubría el Galatasaray–Aston Villa y leía el
 *     caché con los campos de su objeto demo (goles_local, minuto
 *     numérico). Aquí se lee el contrato REAL de data/vivo.json del
 *     Empleado 1: home/away, marcador_local/marcador_visita,
 *     minuto como texto ("88'"), estado pre/in/post, actualizado_en
 *     por partido. La búsqueda es por IDs de equipo (home_id/away_id
 *     de PARTIDOS_VIVO) con respaldo por nombre normalizado.
 *   - El fetch directo usa el scoreboard + fallback de dos hosts del
 *     módulo actual (site.api / site.web.api) con el cuerpo del error
 *     en el mensaje (PR #23), y busca el evento por IDs, no por nombre.
 *   - El partido se identifica por estado: 'pre' muestra
 *     "El partido aún no empieza." y 'post' muestra el resultado
 *     final; la copia de E2 no distinguía estados.
 *   - La antigüedad se calcula desde el timestamp (actualizado_en o
 *     el momento del fetch directo), no por incremento: el cambio a
 *     "caché viejo" al cruzar ~10 min es automático y exacto.
 *   - Si el directo deja de responder después de un éxito, el dato
 *     se degrada al texto de "caché viejo" con su antigüedad real en
 *     vez de seguir diciendo "menos de 1 min".
 *
 * Interfaz (igual que el módulo actual, index.html no cambia):
 *   MarcadorEnVivo.init([PARTIDOS_VIVO[key]], vivoEl)
 *   MarcadorEnVivo.stop()
 * La página lleva este archivo incrustado en index.html (bloque
 * <script> con MarcadorEnVivo + PARTIDOS_VIVO): al portar hay que
 * volver a incrustar esta versión en index.html. No se toca el HTML
 * del modal: el módulo escribe dentro de #vivoLine, que ya tiene el
 * estilo #vivoLine .partido.
 *
 * Sin API key: https://site.api.espn.com/apis/site/v2/sports/soccer
 */

const MarcadorEnVivo = (() => {
  const BASE = 'https://site.api.espn.com/apis/site/v2/sports/soccer';
  const ALT_BASE = 'https://site.web.api.espn.com/apis/site/v2/sports/soccer';
  const CACHE_URL = 'data/vivo.json';
  const CACHE_TIMEOUT_MS = 3000;
  const DIRECTO_TIMEOUT_MS = 5000;
  const VIEJO_MIN = 10;   // a partir de aquí el caché es "viejo"
  const DIRECTO_MIN = 5;  // a partir de aquí se intenta el directo en segundo plano

  let timer = null;
  let elActual = null;
  let partido = null;      // {liga, fecha, home_id, away_id, home, away}
  let estado = null;       // {fuente:'cache'|'directo', hs, as, min, ts, estadoPartido:'in'}
  let terminal = null;     // {tipo:'pre'} | {tipo:'post', hs, as} | null
  let listo = false;       // primera actualización completada
  let abierto = false;
  let directoEnCurso = false;

  function normNombre(s) {
    return (s || '').toLowerCase().normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  }

  function escHtml(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;')
      .replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function tsDe(v) {
    if (typeof v === 'number' && isFinite(v)) {
      return v < 100000000000 ? v * 1000 : v;
    }
    if (typeof v === 'string' && v) {
      const t = Date.parse(v);
      return isNaN(t) ? null : t;
    }
    return null;
  }

  function numDe() {
    for (let i = 0; i < arguments.length; i++) {
      const v = arguments[i];
      if (typeof v === 'number' && isFinite(v)) return v;
      if (typeof v === 'string' && v !== '' && isFinite(Number(v))) return Number(v);
    }
    return null;
  }

  // "88'" -> 88; 88 -> 88; "Full Time" / "" -> null.
  function minutoDe(v) {
    if (typeof v === 'number' && isFinite(v)) return Math.floor(v);
    if (typeof v === 'string' && v) {
      const n = parseInt(v, 10);
      return isNaN(n) ? null : n;
    }
    return null;
  }

  function edadMin(ts) {
    if (!ts) return 0;
    return Math.max(0, Math.floor((Date.now() - ts) / 60000));
  }

  function fetchJSON(url, timeoutMs) {
    const f = (typeof fetch !== 'undefined') ? fetch : null;
    if (!f) return Promise.resolve(null);
    let ctrl = null;
    let timerAbort = null;
    try {
      if (typeof AbortController !== 'undefined') {
        ctrl = new AbortController();
        timerAbort = setTimeout(() => { try { ctrl.abort(); } catch (e) { /* sin abort */ } }, timeoutMs);
      }
    } catch (e) { ctrl = null; }
    let p;
    try {
      p = ctrl ? f(url, { signal: ctrl.signal }) : f(url);
    } catch (e) {
      if (timerAbort) clearTimeout(timerAbort);
      return Promise.resolve(null);
    }
    return Promise.resolve(p).then((res) => {
      if (timerAbort) clearTimeout(timerAbort);
      if (!res || (typeof res.ok !== 'undefined' && !res.ok)) return null;
      try {
        return Promise.resolve(res.json()).catch(() => null);
      } catch (e) { return null; }
    }).catch(() => {
      if (timerAbort) clearTimeout(timerAbort);
      return null;
    });
  }

  // Contrato REAL de data/vivo.json (Empleado 1): partidos con home/away,
  // home_id/away_id, marcador_local/marcador_visita, minuto como texto
  // ("88'"), estado pre/in/post y actualizado_en por partido. Se aceptan
  // también los campos del demo de E2 (goles_local, minuto numérico) por
  // compatibilidad, pero el archivo real manda.
  function buscarEnCache(json, p) {
    if (!json || typeof json !== 'object') return null;
    let lista = null;
    if (Array.isArray(json)) lista = json;
    else if (Array.isArray(json.partidos)) lista = json.partidos;
    else if (Array.isArray(json.matches)) lista = json.matches;
    else if (Array.isArray(json.partidos_vivo)) lista = json.partidos_vivo;
    if (!lista) return null;
    const topTs = tsDe(json.actualizado_en) || tsDe(json.updated_at)
      || tsDe(json.generado_en) || tsDe(json.generated_at);
    const h = normNombre(p.home);
    const a = normNombre(p.away);
    for (const q of lista) {
      if (!q || typeof q !== 'object') continue;
      const porId = p.home_id != null && p.away_id != null
        && q.home_id != null && q.away_id != null
        && String(q.home_id) === String(p.home_id)
        && String(q.away_id) === String(p.away_id);
      const loc = q.home || q.local || q.equipo_local;
      const vis = q.away || q.visitante || q.equipo_visitante;
      const porNombre = loc && vis
        && normNombre(String(loc)) === h && normNombre(String(vis)) === a;
      if (!porId && !porNombre) continue;
      const estadoPartido = q.estado || q.state || 'in';
      const hs = numDe(q.marcador_local, q.goles_local, q.homeScore, q.goles_casa);
      const as = numDe(q.marcador_visita, q.goles_visitante, q.awayScore, q.goles_fuera);
      const min = minutoDe(q.minuto != null ? q.minuto : q.minute);
      const ts = tsDe(q.actualizado_en) || tsDe(q.updated_at) || tsDe(q.actualizado)
        || topTs || tsDe(q.generado_en) || tsDe(json.generado_en);
      if (estadoPartido === 'pre' || estadoPartido === 'post') {
        return { fuente: 'cache', hs, as, min, ts, estadoPartido };
      }
      if (hs === null || as === null || min === null || !ts) return null;
      return { fuente: 'cache', hs, as, min, ts, estadoPartido: 'in' };
    }
    return null;
  }

  function leerCache(p) {
    return fetchJSON(CACHE_URL, CACHE_TIMEOUT_MS).then((json) => {
      if (!json) return null;
      return buscarEnCache(json, p);
    });
  }

  async function pedirScoreboard(base, liga, fecha) {
    const r = await fetch(`${base}/${liga}/scoreboard?dates=${fecha}`);
    if (!r.ok) {
      // Diagnóstico 24 nov 2026: el navegador de la nube recibe 400 de ESPN
      // en el fetch (la misma URL carga bien por navegación y por curl).
      // Se incluye el cuerpo del error para saber por qué. El mensaje
      // queda interno: nunca se muestra en la página.
      let cuerpo = '';
      try { cuerpo = (await r.text()).slice(0, 200); } catch (e) { /* sin cuerpo */ }
      throw new Error(`ESPN ${r.status} (${liga} ${fecha}) ${cuerpo}`);
    }
    return r.json();
  }

  async function scoreboard(liga, fecha) {
    // Respaldo 24 nov 2026: site.api.espn.com devolvió 400 intermitente
    // ("Failed to get events endpoint") en el navegador; si falla, se
    // reintenta una vez contra site.web.api.espn.com (mismos datos).
    try {
      return await pedirScoreboard(BASE, liga, fecha);
    } catch (err1) {
      try {
        return await pedirScoreboard(ALT_BASE, liga, fecha);
      } catch (err2) {
        throw new Error(String(err1.message || err1) + ' | respaldo: ' + String(err2.message || err2));
      }
    }
  }

  function buscarDirecto(p) {
    return scoreboard(p.liga, p.fecha).then((sb) => {
      if (!sb || typeof sb !== 'object' || !Array.isArray(sb.events)) return null;
      for (const ev of sb.events) {
        if (!ev || typeof ev !== 'object') continue;
        const comp = (Array.isArray(ev.competitions) && ev.competitions[0]) || null;
        if (!comp) continue;
        const ids = (comp.competitors || []).map((c) => String(c.team.id));
        if (!ids.includes(String(p.home_id)) || !ids.includes(String(p.away_id))) continue;
        const st = comp.status || {};
        const tipo = st.type || {};
        const estadoPartido = tipo.state || 'pre';
        if (estadoPartido === 'pre') return { estadoPartido: 'pre' };
        let hs = null;
        let as = null;
        for (const c of comp.competitors || []) {
          if (!c || !c.team) continue;
          const sc = (c.score === undefined || c.score === null) ? null : Number(c.score);
          if (sc === null || isNaN(sc)) continue;
          if (c.homeAway === 'home') hs = sc;
          else if (c.homeAway === 'away') as = sc;
        }
        if (hs === null || as === null) continue;
        const min = minutoDe(st.displayClock || '');
        return {
          estadoPartido: estadoPartido === 'post' ? 'post' : 'in',
          hs, as,
          min: estadoPartido === 'post' ? null : min,
        };
      }
      return null;
    }).catch(() => null);
  }

  function intentarDirecto() {
    if (directoEnCurso || !abierto || !partido) return;
    directoEnCurso = true;
    buscarDirecto(partido).then((res) => {
      directoEnCurso = false;
      if (!abierto) return;
      listo = true;
      if (!res) {
        // ESPN no responde: se sigue mostrando lo último que había.
        render();
        return;
      }
      if (res.estadoPartido === 'pre') {
        terminal = { tipo: 'pre' };
        estado = null;
        render();
        return;
      }
      if (res.estadoPartido === 'post') {
        terminal = { tipo: 'post', hs: res.hs, as: res.as };
        estado = null;
        render();
        return;
      }
      terminal = null;
      estado = {
        fuente: 'directo', hs: res.hs, as: res.as,
        min: res.min, ts: Date.now(), estadoPartido: 'in',
      };
      render();
    });
  }

  async function actualizar() {
    if (!abierto || !partido) return estado;
    // El directo es lo más fresco: mientras responda, se reintenta cada tick.
    if (estado && estado.fuente === 'directo') {
      intentarDirecto();
      return estado;
    }
    let cache = null;
    try {
      cache = await leerCache(partido);
    } catch (e) { cache = null; }
    if (!abierto) return estado;
    if (cache) {
      if (cache.estadoPartido === 'pre') {
        terminal = { tipo: 'pre' };
        estado = null;
        listo = true;
        render();
        return estado;
      }
      if (cache.estadoPartido === 'post') {
        terminal = { tipo: 'post', hs: cache.hs, as: cache.as };
        estado = null;
        listo = true;
        render();
        return estado;
      }
      terminal = null;
      estado = cache;
      listo = true;
      render();
      if (edadMin(cache.ts) >= DIRECTO_MIN) intentarDirecto();
      return estado;
    }
    // Sin entrada en el caché.
    if (estado && estado.fuente === 'cache') {
      // La lectura del caché falló: se sigue mostrando el último dato
      // con su antigüedad real.
      render();
      if (edadMin(estado.ts) >= DIRECTO_MIN) intentarDirecto();
      return estado;
    }
    intentarDirecto();
    return estado;
  }

  function tick() {
    if (!abierto) return;
    actualizar();
  }

  // Textos exactos de la propuesta aprobada (E2). La antigüedad se
  // calcula desde el timestamp, así el cambio a "viejo" es automático.
  function textoEstado(e, t, home, away) {
    if (t && t.tipo === 'pre') {
      return '<div class="partido pendiente">El partido aún no empieza.</div>';
    }
    if (t && t.tipo === 'post') {
      const sc = escHtml(home) + ' ' + t.hs + ' – ' + t.as + ' ' + escHtml(away);
      return '<div class="partido"><b>' + sc + '</b><br>Final</div>';
    }
    if (!e) {
      return '<div class="partido pendiente">Sin marcador en vivo por ahora. ESPN no responde y aún no hay datos guardados. Se reintenta solo cada minuto.</div>';
    }
    const sc = escHtml(home) + ' ' + e.hs + ' – ' + e.as + ' ' + escHtml(away);
    const age = edadMin(e.ts);
    if (e.fuente === 'directo') {
      if (age < 1) {
        return '<div class="partido vivo"><b>' + sc + '</b><br>Minuto ' + e.min + "' · En vivo, actualizado hace menos de 1 min</div>";
      }
      // El directo dejó de responder tras el último éxito: el dato se
      // degrada al texto de "viejo" con su antigüedad real, en vez de
      // seguir diciendo "menos de 1 min".
      return '<div class="partido vivo"><b>' + sc + '</b><br>Minuto ' + e.min + "' · Último dato conocido hace " + age + ' min, ESPN no responde, reintentando…</div>';
    }
    if (age >= VIEJO_MIN) {
      return '<div class="partido vivo"><b>' + sc + '</b><br>Minuto ' + e.min + "' · Último dato conocido hace " + age + ' min, ESPN no responde, reintentando…</div>';
    }
    return '<div class="partido vivo"><b>' + sc + '</b><br>Minuto ' + e.min + "' · Actualizado hace " + age + ' min</div>';
  }

  function render() {
    if (!abierto || !elActual || !partido) return;
    if (!listo) {
      elActual.innerHTML = '<div class="partido pendiente">Cargando marcador…</div>';
      return;
    }
    elActual.innerHTML = textoEstado(estado, terminal, partido.home, partido.away);
  }

  function init(partidos, el, ms = 60000) {
    stop();
    if (!partidos || !partidos.length || !el) return { stop };
    partido = partidos[0];
    elActual = el;
    estado = null;
    terminal = null;
    listo = false;
    abierto = true;
    directoEnCurso = false;
    render();
    timer = setInterval(tick, ms);
    actualizar();
    return { stop };
  }

  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
    abierto = false;
    elActual = null;
    directoEnCurso = false;
  }

  return {
    init, stop, actualizar,
    _test: { buscarEnCache, textoEstado, edadMin, minutoDe, normNombre },
  };
})();

if (typeof module !== 'undefined') module.exports = MarcadorEnVivo;
