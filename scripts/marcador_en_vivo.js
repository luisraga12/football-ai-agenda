/**
 * Marcador en vivo — prototipo (Semana 8, orden del jefe 23 nov 2026).
 *
 * Lee el scoreboard público de ESPN para los 28 partidos de la Semana 2
 * (16 de fin de semana + 12 entre semana) y muestra marcador y minuto,
 * refrescando cada 60 segundos. NO toca index.html: esto es un módulo
 * aparte para probar en una copia (preview-marcador-en-vivo.html).
 *
 * Sin API key: https://site.api.espn.com/apis/site/v2/sports/soccer
 * Los partidos se identifican por liga + fecha + IDs de equipo (como
 * valida recolectar_datos.py), nunca por nombre: no se inventa nada.
 *
 * En el navegador: MarcadorEnVivo.init(PARTIDOS, elemento).
 *   PARTIDOS: [{liga, fecha, home_id, away_id, home, away}]
 *   Cada 60 s vuelve a pedir el scoreboard del día y actualiza solo
 *   marcador, minuto y estado. Si ESPN falla, deja lo último que tenía
 *   y marca "sin actualizar".
 */

const MarcadorEnVivo = (() => {
  const BASE = 'https://site.api.espn.com/apis/site/v2/sports/soccer';
  let timer = null;

  const ALT_BASE = 'https://site.web.api.espn.com/apis/site/v2/sports/soccer';

  async function pedirScoreboard(base, liga, fecha) {
    const r = await fetch(`${base}/${liga}/scoreboard?dates=${fecha}`);
    if (!r.ok) {
      // Diagnóstico 24 nov 2026: el navegador de la nube recibe 400 de ESPN
      // en el fetch (la misma URL carga bien por navegación y por curl).
      // Se incluye el cuerpo del error para saber por qué.
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

  function estadoDe(comp) {
    const st = comp.status || {};
    const tipo = st.type || {};
    // En el scoreboard, st.clock es un número (segundos) y el minuto
    // viene en st.displayClock ("67'"); en el summary, clock es un
    // objeto con displayValue. Se aceptan las dos formas.
    let minuto = st.displayClock || '';
    if (!minuto && st.clock && typeof st.clock === 'object') {
      minuto = st.clock.displayValue || '';
    }
    if (!minuto && typeof st.clock === 'number' && st.clock > 0) {
      minuto = `${Math.floor(st.clock / 60)}'`;
    }
    return {
      estado: tipo.state || 'pre', // pre | in | post
      detalle: tipo.detail || tipo.shortDetail || '',
      minuto,
    };
  }

  function marcadorDe(comp) {
    const out = { scoreHome: null, scoreAway: null };
    for (const c of comp.competitors || []) {
      const v = c.score;
      const n = v === undefined || v === null ? null : Number(v);
      if (c.homeAway === 'home') out.scoreHome = n;
      if (c.homeAway === 'away') out.scoreAway = n;
    }
    return out;
  }

  async function actualizar(partidos, el) {
    const porDia = {};
    for (const p of partidos) {
      (porDia[`${p.liga}|${p.fecha}`] ||= []).push(p);
    }
    const filas = [];
    for (const key of Object.keys(porDia)) {
      const [liga, fecha] = key.split('|');
      try {
        const sb = await scoreboard(liga, fecha);
        const eventos = sb.events || [];
        for (const p of porDia[key]) {
          const ev = eventos.find((e) => {
            const comp = (e.competitions || [])[0];
            if (!comp) return false;
            const ids = (comp.competitors || []).map(
              (c) => String(c.team.id));
            return ids.includes(String(p.home_id))
              && ids.includes(String(p.away_id));
          });
          if (!ev) {
            filas.push({ ...p, falta: true });
            continue;
          }
          const comp = ev.competitions[0];
          filas.push({
            ...p,
            ...marcadorDe(comp),
            ...estadoDe(comp),
            actualizado: new Date().toLocaleTimeString('es-MX'),
          });
        }
      } catch (err) {
        for (const p of porDia[key]) filas.push({ ...p, error: String(err) });
      }
    }
    render(filas, el);
    return filas;
  }

  function textoFila(f) {
    if (f.error) return `${f.home} vs ${f.away} — error: ${f.error}`;
    if (f.falta) return `${f.home} vs ${f.away} — no aparece en ESPN todavía`;
    const m = (f.scoreHome === null || f.scoreAway === null)
      ? 'vs'
      : `${f.scoreHome} - ${f.scoreAway}`;
    const cuando = f.estado === 'in'
      ? (f.minuto || 'en juego')
      : (f.detalle || 'por jugar');
    return `${f.home} ${m} ${f.away} · ${cuando}`;
  }

  function render(filas, el) {
    el.innerHTML = filas.map((f) => {
      const cls = f.error || f.falta ? 'pendiente'
        : f.estado === 'in' ? 'vivo' : 'programado';
      return `<div class="partido ${cls}">${textoFila(f)}</div>`;
    }).join('');
  }

  function init(partidos, el, ms = 60000) {
    stop();
    const correr = () => actualizar(partidos, el);
    correr();
    timer = setInterval(correr, ms);
    return { stop };
  }

  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
  }

  return { init, stop, actualizar, textoFila };
})();

if (typeof module !== 'undefined') module.exports = MarcadorEnVivo;
