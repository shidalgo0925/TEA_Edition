(function(){
  let step = 1;
  const total = 7;
  const btnBack = document.getElementById('btnBack');
  const btnNext = document.getElementById('btnNext');
  const btnCommit = document.getElementById('btnCommit');
  const wizProgress = document.getElementById('wizProgress');

  const el = (id)=>document.getElementById(id);

  function showStep(n){
    for(let i=1;i<=total;i++){
      const s = el('step'+i);
      if(s){ s.classList.toggle('d-none', i!==n); }
    }
    btnBack.disabled = (n===1);
    btnNext.textContent = (n===total) ? 'Finalizar' : 'Siguiente';
    wizProgress.style.width = Math.round((n/total)*100)+'%';
    wizProgress.textContent = `Paso ${n}/${total}`;
  }

  btnBack?.addEventListener('click', ()=>{ if(step>1){ step--; showStep(step); }});
  btnNext?.addEventListener('click', async ()=>{
    if(step===3){
      // Llamar /suggest
      const metas_crudas = el('metasCrudas').value;
      let restricciones = {};
      try { restricciones = JSON.parse(el('restricciones').value || "{}"); } catch(e){ restricciones = {}; }
      const horizonte = el('horizonte').value;
      const res = await fetch('/api/ai/plan/suggest', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ metas_crudas, restricciones, horizonte })
      });
      const j = await res.json();
      window.__draft = j.draft || {};
      el('smartPreview').textContent = JSON.stringify(window.__draft?.metas_smart || [], null, 2);
    }
    if(step===4){
      el('breakdownPreview').textContent = JSON.stringify({
        rocas: window.__draft?.rocas_semanales || [],
        microacciones: window.__draft?.microacciones || {}
      }, null, 2);
    }
    if(step===5){
      el('calendarPreview').textContent = JSON.stringify(window.__draft?.microacciones || {}, null, 2);
      el('finalPreview').textContent = JSON.stringify(window.__draft || {}, null, 2);
    }
    if(step<total){ step++; showStep(step); }
  });

  btnCommit?.addEventListener('click', async ()=>{
    const res = await fetch('/api/ai/plan/commit', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ draft: window.__draft, user_id: 1 })
    });
    const j = await res.json();
    el('commitMsg').textContent = j.ok ? 'Guardado (simulado). ✅' : 'Error al guardar';
  });

  // init
  showStep(step);
})();
