/* Tabla UEL unificada (28 nov 2026, Empleado 2, ronda 7:30).
   Los 4 partidos de la Europa League sin tabla (Marseille-Levski, Juventus-Omonia,
   NEC-Rennes, Sunderland-Jagiellonia) toman la tabla unificada 2026-27 (36 equipos,
   5 PJ) del endpoint ESPN apis/v2 (sin «site»), en vivo al abrir la página.
   Solo actúa cuando la página es UEL (window.__detalle.liga === 'uefa.europa')
   y las dos cajas de «Posición en la tabla» dicen «pendiente»; si el endpoint
   falla, la posición queda «pendiente» y no se inventa nada.
   Mismo núcleo que preview-uel-unificada.html (commit 5ca65be).
   Se carga desde partido.html con <script src="tabla-uel.js"></script> antes de </body>. */
(function(){
  'use strict';
  var URL_TABLA_UEL = '/apis/v2/sports/soccer/uefa.europa/standings';
  var HOSTS_UEL = ['https://site.api.espn.com', 'https://site.web.api.espn.com'];
  var ALIAS_UEL = {olm:'marseille', lev:'levskisofia', juv:'juventus', omon:'omonianicosia', nec:'necnijmegen', ren:'staderennais', sun:'sunderland', jag:'jagielloniabialystok'};
  function normUEL(s){ return String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]/g, ''); }
  function escUEL(s){ return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function statUEL(entry, nombre){ var a = (entry && entry.stats) || []; for(var i = 0; i < a.length; i++){ if(a[i] && a[i].name === nombre) return a[i].value; } return null; }
  function buscarEquipoUEL(entries, nombrePagina){
    var n = normUEL(nombrePagina);
    for(var i = 0; i < entries.length; i++){
      var t = entries[i].team || {};
      var cands = [t.location, t.name, t.shortDisplayName, t.displayName, t.abbreviation];
      for(var j = 0; j < cands.length; j++){ if(cands[j] && normUEL(cands[j]) === n) return entries[i]; }
      if(t.abbreviation && ALIAS_UEL[String(t.abbreviation).toLowerCase()] === n) return entries[i];
    }
    return null;
  }
  function stDeUEL(entry){
    var g = statUEL(entry, 'wins'), e = statUEL(entry, 'ties'), p = statUEL(entry, 'losses');
    return {pos:statUEL(entry, 'rank'), pts:statUEL(entry, 'points'), pj:statUEL(entry, 'gamesPlayed'), g:g, e:e, p:p, dg:statUEL(entry, 'pointDifferential'), 'récord':g + '-' + e + '-' + p};
  }
  function cajaPosUEL(nombre, st){
    var dg = (st.dg == null ? '–' : String(st.dg));
    return '<div class="pos-box"><b>' + escUEL(nombre) + '</b>' +
      '<div class="pos-num num">' + escUEL(st.pos) + 'º</div>' +
      '<p>' + escUEL(st.pts) + ' pts · ' + escUEL(st.pj) + ' PJ · ' + escUEL(st['récord']) + ' · DG ' + escUEL(dg) + '</p></div>';
  }
  function notaUEL(texto){
    var pos = document.querySelector('.detail-pos');
    if(!pos) return;
    var nota = document.getElementById('uel-nota');
    if(!nota){
      nota = document.createElement('p');
      nota.id = 'uel-nota';
      nota.className = 'detail-note';
      pos.parentNode.insertBefore(nota, pos.nextSibling);
    }
    nota.textContent = texto;
  }
  function esUEL(det){
    if(det && det.liga === 'uefa.europa') return true;
    try{
      if(det && typeof DETAIL !== 'undefined' && DETAIL[det.slug] && DETAIL[det.slug].league && String(DETAIL[det.slug].league).indexOf('Europa League') !== -1) return true;
    }catch(e){}
    return false;
  }
  function pedirUEL(idx){
    if(idx >= HOSTS_UEL.length) return Promise.reject(new Error('ESPN no responde'));
    return fetch(HOSTS_UEL[idx] + URL_TABLA_UEL).then(function(r){ if(!r.ok) throw new Error('ESPN ' + r.status); return r.json(); }).catch(function(){ if(idx + 1 < HOSTS_UEL.length) return pedirUEL(idx + 1); throw new Error('ESPN no responde'); });
  }
  function cargarTablaUEL(){
    var det = window.__detalle || null;
    if(!det || !esUEL(det)) return;
    var cajas = document.querySelectorAll('.detail-pos .pos-box');
    if(cajas.length < 2) return;
    var pendientes = 0;
    for(var i = 0; i < cajas.length; i++){ if(/pendiente/.test(cajas[i].textContent || '')) pendientes++; }
    if(pendientes < 2) return;
    cajas[0].innerHTML = '<b>' + escUEL(det.home) + '</b><p>Cargando tabla unificada…</p>';
    cajas[1].innerHTML = '<b>' + escUEL(det.away) + '</b><p>Cargando tabla unificada…</p>';
    notaUEL('Tabla unificada UEFA Europa League 2026-27 (36 equipos) · cargando desde ESPN…');
    pedirUEL(0).then(function(j){
      var entries = [];
      try{ entries = (j.children[0].standings.entries) || []; }catch(e){ entries = []; }
      if(!entries.length) throw new Error('sin entradas');
      var eh = buscarEquipoUEL(entries, det.home);
      var ea = buscarEquipoUEL(entries, det.away);
      if(!eh || !ea) throw new Error('equipo no encontrado');
      cajas[0].innerHTML = cajaPosUEL(det.home, stDeUEL(eh));
      cajas[1].innerHTML = cajaPosUEL(det.away, stDeUEL(ea));
      notaUEL('Tabla unificada UEFA Europa League 2026-27 · 36 equipos · 5 PJ · ESPN (en vivo, al abrir la página)');
    }).catch(function(){
      cajas[0].innerHTML = '<b>' + escUEL(det.home) + '</b><p>pendiente</p>';
      cajas[1].innerHTML = '<b>' + escUEL(det.away) + '</b><p>pendiente</p>';
      notaUEL('No se pudo cargar la tabla unificada de ESPN; la posición queda pendiente.');
    });
  }
  var intentosUEL = 0;
  var timerUEL = setInterval(function(){
    intentosUEL++;
    if(window.__detalle && document.querySelector('.detail-pos')){
      clearInterval(timerUEL);
      cargarTablaUEL();
    } else if(intentosUEL >= 150){
      clearInterval(timerUEL);
    }
  }, 200);
})();
