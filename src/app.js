/* ── Catálogo de Evaluación Educativa ─────────────────────── */

/* ── Structural CAT_CONFIG (keys stay fixed across languages) */
const CAT_CONFIG_BASE = {
  tecnicas:     { cls: 'tec', icon: '🔬', nameKey: 'Técnica',     extraFilterKey: null,          extra2FilterKey: null },
  dimensiones:  { cls: 'dim', icon: '🧭', nameKey: 'Dimensión',   extraFilterKey: 'Categoría',   extra2FilterKey: null },
  instrumentos: { cls: 'ins', icon: '📄', nameKey: 'Instrumento', extraFilterKey: 'Complejidad', extra2FilterKey: null },
  herramientas: { cls: 'her', icon: '🛠️', nameKey: 'Herramienta', extraFilterKey: 'Complejidad', extra2FilterKey: null },
};

function buildCatConfig(lang) {
  const iCats = I18N[lang].cats;
  return Object.fromEntries(
    Object.entries(CAT_CONFIG_BASE).map(([cat, base]) => [cat, { ...base, ...iCats[cat] }])
  );
}

// Relaciones por código: Técnica/Dimensión → Instrumento → Herramienta
const RELATIONS = {
  tecnicas:     { left: null,          right: { cat: 'instrumentos', codeField: 'rel_ins' } },
  dimensiones:  { left: null,          right: { cat: 'instrumentos', codeField: 'rel_ins' } },
  instrumentos: { left: { cat: 'tecnicas',     codeField: 'rel_tec' },
                  right: { cat: 'herramientas', codeField: 'rel_her' } },
  herramientas: { left: { cat: 'instrumentos', codeField: 'rel_ins' }, right: null },
};
const DIMENSION_RELATION = { cat: 'dimensiones', codeField: 'rel_dim' };
const REL_PRIORITY = { principal: 3, complementaria: 2, ocasional: 1 };

const state = {
  data:         {},
  cat:          null,
  extra:        '',
  search:       '',
  selectedName: null,
  lang:         localStorage.getItem('evalmap_lang') || 'es',
  planMode:       false,
  planSelected:   new Map(), // code → { name, cat, item }
  planExpandedDim: null,     // dimension code currently expanded
  gFase:         '',
  gParticipacion: '',
  gModalidad:    '',
  gLugar:        '',
  gAgrupamiento: '',
  gResIA:        '',
};

let CAT_CONFIG = buildCatConfig(state.lang);

const graphVisibleCats = {
  tecnicas: true,
  dimensiones: true,
  instrumentos: true,
  herramientas: true,
};

/* ── i18n helpers ─────────────────────────────────────────── */
function i18n() { return I18N[state.lang]; }

function translateValue(field, val) {
  if (!val) return '';
  const i = i18n();
  const parts = val.split('/').map(v => v.trim());
  if (field === 'Fase') return parts.map(p => i.phaseFull[p] || p).join(' / ');
  return parts.map(p => i.filterValLabels[p] || p).join(' / ');
}

function tabLabel(cat, count = null) {
  const cfg = CAT_CONFIG[cat];
  const suffix = count === null ? '' : ` <span class="tab-count">(${count})</span>`;
  return `${cfg.icon} ${cfg.label}${suffix}`;
}

/* ── Home & static i18n rendering ────────────────────────── */
function renderHome() {
  const i = i18n();
  const hero = document.querySelector('.home-hero');
  if (hero) {
    const h1 = hero.querySelector('h1');
    const p  = hero.querySelector('p');
    if (h1) h1.textContent = i.appTitle;
    if (p)  p.textContent  = i.homeSubtitle;
  }
  const hint = document.querySelector('.home-entry-hint');
  if (hint) hint.textContent = i.homeHint;

  Object.keys(i.cats).forEach(cat => {
    const card = document.querySelector(`.home-card[data-cat="${cat}"]`);
    if (!card) return;
    const h2 = card.querySelector('h2');
    const p  = card.querySelector('p');
    if (h2) h2.textContent = i.cats[cat].label;
    if (p)  p.textContent  = i.cats[cat].homeDesc;
    card.querySelectorAll('.home-card-btn').forEach(btn => btn.textContent = i.startHere);
    const feat = card.querySelector('.home-card-feature');
    if (feat && i.cats[cat].homeFeature) feat.textContent = i.cats[cat].homeFeature;
  });

  const kicker = document.querySelector('.home-card-kicker');
  if (kicker) kicker.textContent = i.transversalLabel;

  const brandSpan = document.querySelector('#btn-home span');
  if (brandSpan) brandSpan.textContent = i.appTitle;

  document.querySelectorAll('.cat-tab[data-cat]').forEach(tab => {
    tab.innerHTML = tabLabel(tab.dataset.cat);
  });

  const ghProject = document.getElementById('footer-gh-project');
  if (ghProject) ghProject.textContent = i.ghProject;
  const ghIssues = document.getElementById('footer-gh-issues');
  if (ghIssues) ghIssues.textContent = i.ghIssues;
  const contentLic = document.getElementById('footer-content-lic');
  if (contentLic) contentLic.textContent = i.contentLicense;
  const codeLic = document.getElementById('footer-code-lic');
  if (codeLic) codeLic.textContent = i.codeLicense;
}

function updateStaticI18n() {
  const i = i18n();
  document.documentElement.lang = i.htmlLang;
  document.title = i.appTitle;

  const btnBack = document.getElementById('btn-nav-back');
  if (btnBack) { btnBack.title = i.backTitle; btnBack.setAttribute('aria-label', i.backTitle); }
  const btnFwd = document.getElementById('btn-nav-fwd');
  if (btnFwd)  { btnFwd.title  = i.fwdTitle;  btnFwd.setAttribute('aria-label', i.fwdTitle); }

  const btnGraph = document.getElementById('btn-toggle-graph');
  if (btnGraph) { btnGraph.textContent = i.level2Label; btnGraph.title = i.level2Title; }
  const btnEss = document.getElementById('btn-toggle-essential');
  if (btnEss) { btnEss.textContent = i.occasionalLabel; btnEss.title = i.occasionalTitle; }

  const catLabel = document.querySelector('.graph-cat-label');
  if (catLabel) catLabel.textContent = i.seeLabel;

  const dragHandle = document.getElementById('detail-drag-handle');
  if (dragHandle) dragHandle.title = i.dragTitle;
  const btnCopy = document.getElementById('btn-copy-card');
  if (btnCopy) btnCopy.title = i.copyTitle;
  const btnPrint = document.getElementById('btn-print-card');
  if (btnPrint) btnPrint.title = i.printTitle;
  const btnDl = document.getElementById('btn-dl-card');
  if (btnDl) btnDl.title = i.dlTitle;

  const btnHome = document.getElementById('btn-home');
  if (btnHome) btnHome.title = i.homeLabel;

  const btnTheme = document.getElementById('btn-theme');
  if (btnTheme) btnTheme.textContent = darkMode ? i.lightMode : i.darkMode;

  const btnPlan = document.getElementById('btn-plan-mode');
  if (btnPlan) {
    btnPlan.textContent = i.planButtonLabel;
    btnPlan.dataset.tooltip = i.planButtonTooltip;
  }
  const btnPlanClear = document.getElementById('btn-plan-clear');
  if (btnPlanClear) btnPlanClear.textContent = i.planClearLabel;

  const aiSpan = document.querySelector('.notebooklm-btn span:last-child');
  if (aiSpan) aiSpan.textContent = i.aiAssistant;
  const aiBtn = document.querySelector('.notebooklm-btn');
  if (aiBtn) aiBtn.title = i.aiAssistant;

  const emptyP = document.querySelector('#detail-empty p');
  if (emptyP) emptyP.innerHTML = i.selectHint;

  const legendSpans = document.querySelectorAll('.graph-legend span');
  if (legendSpans.length >= 4) {
    const dot = (d) => `<svg width="${d}" height="${d}" viewBox="0 0 ${d} ${d}" aria-hidden="true" style="flex-shrink:0"><circle cx="${d/2}" cy="${d/2}" r="${d/2}" fill="currentColor"/></svg>`;
    legendSpans[0].innerHTML = `${dot(14)}${i.legend.principal}`;
    legendSpans[1].innerHTML = `${dot(9)}${i.legend.complementaria}`;
    legendSpans[2].innerHTML = `${dot(4)}${i.legend.ocasional}`;
    legendSpans[3].innerHTML = `<i class="legend-line transversal"></i>${i.legend.transversal}`;
  }

  document.querySelectorAll('.graph-cat-chip[data-graph-cat]').forEach(chip => {
    const cat = chip.dataset.graphCat;
    chip.setAttribute('aria-label', CAT_CONFIG[cat]?.label || cat);
  });

  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === state.lang);
  });
}

/* ── Language switcher ────────────────────────────────────── */
async function setLang(lang) {
  if (!I18N[lang] || lang === state.lang) return;
  if (state.planMode) exitPlanMode();
  state.lang = lang;
  localStorage.setItem('evalmap_lang', lang);
  CAT_CONFIG = buildCatConfig(lang);
  state.gFase = ''; state.gParticipacion = '';
  state.gModalidad = ''; state.gLugar = ''; state.gAgrupamiento = ''; state.gResIA = '';
  renderHome();
  updateStaticI18n();
  renderGlobalFilters();
  await loadData();
  if (state.cat) {
    state.extra = ''; state.search = '';
    showCatalog(state.cat);
    if (state.selectedName) showDetailPanel(state.selectedName, state.cat, false);
  }
}

function updateTabGraphCounts() {
  const counts = Object.fromEntries(Object.keys(CAT_CONFIG).map(cat => [cat, 0]));
  GRAPH.nodes.forEach(node => {
    if (counts[node.cat] !== undefined) counts[node.cat] += 1;
  });
  const i = i18n();
  document.querySelectorAll('.cat-tab[data-cat]').forEach(tab => {
    const count = GRAPH.nodes.length ? counts[tab.dataset.cat] : null;
    tab.innerHTML = tabLabel(tab.dataset.cat, count || null);
    tab.title = '';
  });
  document.querySelectorAll('.graph-cat-chip[data-graph-cat]').forEach(chip => {
    const cat = chip.dataset.graphCat;
    const rawCount = GRAPH.rawNodes.filter(node => node.cat === cat).length;
    const visibleCount = GRAPH.nodes.filter(node => node.cat === cat).length;
    const isCenterCat = detailCurrentCat === cat;
    const requiredBridge = detailCurrentCat !== 'instrumentos' && cat === 'instrumentos' && rawCount > 0;
    const disabled = !rawCount || isCenterCat || requiredBridge;
    const locked = (isCenterCat || requiredBridge) && !!rawCount;
    chip.classList.toggle('off', !graphVisibleCats[cat]);
    chip.classList.toggle('locked', locked);
    chip.disabled = disabled;
    chip.title = !rawCount
      ? i.graphCatHidden
      : isCenterCat
        ? i.graphCatCenter
        : requiredBridge
          ? i.graphCatBridge
          : graphVisibleCats[cat]
            ? i.graphCatHide(CAT_CONFIG[cat].label, visibleCount)
            : i.graphCatShow(CAT_CONFIG[cat].label);
    chip.setAttribute('aria-label', chip.title);
  });
}

/* ── Data loading ─────────────────────────────────────────── */
async function loadData() {
  const keys = ['tecnicas', 'dimensiones', 'instrumentos', 'herramientas'];
  const entries = await Promise.all(
    keys.map(key =>
      fetch(`data/${state.lang}/${key}.json`).then(r => r.json()).then(d => [key, d])
    )
  );
  state.data = Object.fromEntries(entries);

  const i = i18n();
  document.getElementById('count-tec').textContent = i.countTec(state.data.tecnicas.length);
  document.getElementById('count-dim').textContent = i.countDim(state.data.dimensiones.length);
  document.getElementById('count-ins').textContent = i.countIns(state.data.instrumentos.length);
  document.getElementById('count-her').textContent = i.countHer(state.data.herramientas.length);

  document.querySelectorAll('.cat-tab[data-cat]').forEach(tab => {
    tab.innerHTML = tabLabel(tab.dataset.cat);
  });
}

/* ── View management ──────────────────────────────────────── */
function showView(id) {
  document.getElementById('view-home').style.display    = id === 'view-home'    ? 'flex' : 'none';
  document.getElementById('view-catalog').style.display = id === 'view-catalog' ? 'flex' : 'none';
  window.scrollTo(0, 0);
}

function showHome() {
  if (state.planMode) exitPlanMode();
  graphStop();
  GRAPH.nodes = [];
  GRAPH.edges = [];
  GRAPH.rawNodes = [];
  GRAPH.rawEdges = [];
  state.cat = null;
  state.selectedName = null;
  document.getElementById('cat-tabs').style.display    = 'none';
  document.getElementById('catalog-count').style.display = 'none';
  document.getElementById('plan-toolbar').style.display = 'none';
  showView('view-home');
}

function showCatalog(cat) {
  state.cat   = cat;
  state.extra = '';
  state.search = '';
  resetDetailEmpty();
  document.querySelector('.catalog-body').classList.remove('has-detail');

  const cfg = CAT_CONFIG[cat];
  const i   = i18n();

  document.getElementById('cat-tabs').style.display      = 'flex';
  document.getElementById('catalog-count').style.display = '';

  document.querySelectorAll('.cat-tab').forEach(t => {
    t.className = 'cat-tab' + (t.dataset.cat === cat ? ` active-${cfg.cls}` : '');
  });

  document.getElementById('search-input').value = '';
  document.getElementById('search-input').placeholder = i.searchPlaceholder(cfg.label);

  document.getElementById('filter-bar').style.setProperty('--active-color', `var(--c-${cfg.cls})`);
  document.getElementById('detail-panel').style.setProperty('--active-color', `var(--c-${cfg.cls})`);

  renderGlobalFilters();

  const planToolbar = document.getElementById('plan-toolbar');
  if (cat === 'herramientas') {
    planToolbar.style.display = '';
  } else {
    planToolbar.style.display = 'none';
    if (state.planMode) exitPlanMode();
  }
  showView('view-catalog');
  renderCards();
  if (state.planMode) renderPlanCoverage();
}

/* ── Global filters ───────────────────────────────────────── */
const GF_STATE = {
  fase: 'gFase', participacion: 'gParticipacion',
  modalidad: 'gModalidad', lugar: 'gLugar',
  agrupamiento: 'gAgrupamiento', resistenciaIA: 'gResIA',
};

function setDetailEmpty(iconHtml, messageHtml) {
  const el = document.getElementById('detail-empty');
  el.querySelector('.empty-icon').innerHTML = iconHtml;
  el.querySelector('p').innerHTML = messageHtml;
}

function resetDetailEmpty() {
  setDetailEmpty('👈', i18n().selectHint);
}

function applyGlobalFilterToGraph() {
  if (!detailCurrentItem) return;
  if (matchGlobalFilters(detailCurrentItem)) {
    // Item passes filters: restore full detail panel if it was hidden by a filter
    if (document.getElementById('detail-content').style.display === 'none') {
      showDetailPanel(detailCurrentItem[CAT_CONFIG[detailCurrentCat].nameKey], detailCurrentCat, false);
    } else {
      renderGraph(detailCurrentItem, detailCurrentCat);
    }
  } else {
    graphStop();
    GRAPH.nodes = []; GRAPH.edges = [];
    // Keep state.selectedName so the item can be restored when filters change back
    document.querySelectorAll('.cat-card').forEach(c =>
      c.className = c.className.replace(/\bselected-\w+\b/g, '').trim());
    document.getElementById('detail-content').style.display = 'none';
    document.getElementById('detail-empty').style.display = '';
    document.querySelector('.catalog-body').classList.remove('has-detail');
    setDetailEmpty('⚙️', i18n().globalFiltersExcludedHint);
    updateTabGraphCounts();
  }
}

function matchGlobalFilters(item) {
  const gf = i18n().globalFilters;
  return (
    matchField(item, gf.fase.field,          state.gFase) &&
    matchField(item, gf.participacion.field, state.gParticipacion) &&
    matchField(item, gf.modalidad.field,     state.gModalidad) &&
    matchField(item, gf.lugar.field,         state.gLugar) &&
    matchField(item, gf.agrupamiento.field,  state.gAgrupamiento) &&
    matchField(item, gf.resistenciaIA.field, state.gResIA)
  );
}

function renderGlobalFilters() {
  const pop0 = document.getElementById('gf-popover');
  const wasOpen = pop0 ? pop0.style.display === '' : false;
  const i   = i18n();
  const fvl = i.filterValLabels;
  const gf  = i.globalFilters;
  const bar = document.getElementById('global-filter-bar');
  const cfg = state.cat ? CAT_CONFIG[state.cat] : null;

  const activeCount = [
    state.gFase, state.gParticipacion,
    state.gModalidad, state.gLugar, state.gAgrupamiento, state.gResIA,
    state.extra,
  ].filter(Boolean).length;

  const globalPills = Object.entries(gf).map(([key, gcfg]) => {
    const val = state[GF_STATE[key]];
    if (!val) return '';
    const short = key === 'resistenciaIA' ? `IA: ${fvl[val] || val}` : (fvl[val] || val);
    return `<span class="gf-pill"><span>${short}</span><button class="gf-pill-x" type="button" data-gf="${key}" aria-label="${i.removeLabel}">×</button></span>`;
  }).join('');

  const catCls = cfg ? CAT_CONFIG_BASE[state.cat]?.cls || cfg.cls : '';
  const extraPill = (cfg && cfg.extraFilterLabel && state.extra)
    ? `<span class="gf-pill gf-pill--cat" style="--cat-color:var(--c-${catCls})"><span>${fvl[state.extra] || state.extra}</span><button class="gf-pill-x" type="button" data-gf="extra" aria-label="${i.removeLabel}">×</button></span>`
    : '';

  const esc = val => String(val || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

  const infoIcon = desc => desc
    ? `<span class="gf-info" title="${esc(desc)}">?</span>` : '';

  const popoverRows = Object.entries(gf).map(([key, gcfg]) => {
    const cur = state[GF_STATE[key]];
    return `
      <div class="gf-group">
        <span class="gf-group-label">${gcfg.label}${infoIcon(gcfg.desc)}</span>
        <div class="gf-chips">
          <button class="chip${cur === '' ? ' active' : ''}" type="button" data-gf="${key}" data-gv="">${gcfg.all}</button>
          ${gcfg.vals.map(v => `<button class="chip${cur === v ? ' active' : ''}" type="button" data-gf="${key}" data-gv="${v}">${fvl[v] || v}</button>`).join('')}
        </div>
      </div>`;
  }).join('');

  const catSection = (cfg && cfg.extraFilterLabel) ? `
    <div class="gf-cat-sep"><span>${i.globalFiltersCatSep}</span></div>
    <div class="gf-group" style="--active-color:var(--c-${catCls})">
      <span class="gf-group-label">${cfg.extraFilterLabel.replace(':', '')}${infoIcon(cfg.extraFilterDesc)}</span>
      <div class="gf-chips">
        <button class="chip${!state.extra ? ' active' : ''}" type="button" data-gf="extra" data-gv="">${cfg.extraFilterAll}</button>
        ${cfg.extraFilterVals.map(v => `<button class="chip${state.extra === v ? ' active' : ''}" type="button" data-gf="extra" data-gv="${v}">${fvl[v] || v}</button>`).join('')}
      </div>
    </div>` : '';

  bar.innerHTML = `
    <div class="gf-row">
      <button class="gf-btn${activeCount ? ' gf-btn--on' : ''}" id="gf-trigger" type="button"
              title="${i.globalFiltersBtnTitle}">
        <svg class="gf-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><line x1="3" y1="4" x2="13" y2="4"/><line x1="5" y1="8" x2="11" y2="8"/><line x1="7" y1="12" x2="9" y2="12"/></svg>
        ${i.globalFiltersBtnLabel}${activeCount ? `<span class="gf-badge">${activeCount}</span>` : ''}
        <span class="gf-arrow">▾</span>
      </button>
    </div>
    <div class="gf-popover" id="gf-popover" style="display:none">
      ${activeCount ? `<div class="gf-reset-row"><button class="gf-reset-btn" id="gf-clear" type="button">↺ ${i.globalFiltersClear}</button></div>` : ''}
      ${popoverRows}${catSection}
    </div>`;

  const pBar = document.getElementById('gf-pills-bar');
  if (pBar) {
    pBar.innerHTML = activeCount
      ? `<div class="gf-pills">${globalPills}${extraPill}</div>
         <button class="gf-clear" id="gf-clear-ext" type="button">${i.globalFiltersClear}</button>`
      : '';
  }

  if (wasOpen) {
    document.getElementById('gf-popover').style.display = '';
    document.getElementById('gf-trigger')?.classList.add('gf-btn--open');
    document.getElementById('gf-backdrop')?.classList.add('open');
  }
}

function closeGfPopover() {
  const pop = document.getElementById('gf-popover');
  if (pop) pop.style.display = 'none';
  document.getElementById('gf-trigger')?.classList.remove('gf-btn--open');
  document.getElementById('gf-backdrop')?.classList.remove('open');
}

/* ── Filtering helpers ────────────────────────────────────── */
function matchField(item, key, value) {
  if (!value) return true;
  return item[key] && item[key].includes(value);
}

function normalize(s) {
  return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
}
function matchSearch(item, nameKey, query) {
  if (!query) return true;
  const q = normalize(query);
  return (
    normalize(item[nameKey]             || '').includes(q) ||
    normalize(item['Descripción breve'] || '').includes(q) ||
    normalize(item['Etiquetas']         || '').includes(q)
  );
}

/* ── Card list rendering ──────────────────────────────────── */
function phaseBadges(fase) {
  if (!fase) return '';
  const phases = i18n().phaseFull;
  return fase.split('/').map(f => {
    const t   = f.trim();
    const cls = t === 'Inicial' ? 'ini' : t === 'Proceso' ? 'pro' : 'fin';
    return `<span class="badge badge-fase-${cls}">${phases[t] || t}</span>`;
  }).join('');
}

function renderCards() {
  const cat   = state.cat;
  const cfg   = CAT_CONFIG[cat];
  const items = state.data[cat] || [];

  const filtered = items.filter(item =>
    matchField(item, cfg.extraFilterKey, state.extra) &&
    matchGlobalFilters(item) &&
    matchSearch(item, cfg.nameKey, state.search)
  );

  document.getElementById('filter-bar').style.display = items.length ? '' : 'none';
  document.getElementById('catalog-count').textContent =
    `${filtered.length} / ${items.length}`;
  if (!GRAPH.nodes.length) {
    document.querySelectorAll('.cat-tab[data-cat]').forEach(tab => {
      tab.innerHTML = tabLabel(tab.dataset.cat);
    });
  }

  const grid = document.getElementById('cards-grid');
  grid.scrollTop = 0;

  if (filtered.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">🔍</div>
        ${i18n().noResults}
      </div>`;
    return;
  }

  grid.innerHTML = filtered.map(item => {
    const name      = item[cfg.nameKey];
    const code      = item['Código'];
    const desc      = item['Descripción breve'] || '';
    const badges    = phaseBadges(item['Fase']);
    const safeName  = name.replace(/"/g, '&quot;');
    const planPick  = state.planMode && state.planSelected.has(code);
    const selClass  = !state.planMode && name === state.selectedName ? ` selected-${cfg.cls}` : '';
    const planClass = planPick ? ' plan-selected' : '';
    const checkMark = planPick ? '<span class="plan-check">✓</span>' : '';

    return `
      <div class="cat-card${selClass}${planClass}" style="--active-color:var(--c-${cfg.cls})"
           data-name="${safeName}" data-code="${code}" data-cat="${cat}" role="button" tabindex="0">
        ${checkMark}
        <div class="cat-card-name">${name}</div>
        <div class="cat-card-desc">${desc}</div>
        <div class="cat-card-badges">${badges}</div>
      </div>`;
  }).join('');
}

/* ── Relationship lookup by code ──────────────────────────── */
function findByCodes(codes, targetCat) {
  if (!codes || !codes.length) return [];
  const items = state.data[targetCat] || [];
  return items.filter(i => codes.includes(i['Código']));
}

/* ── Detail panel ─────────────────────────────────────────── */
function showDetailPanel(name, cat, pushHistory = true) {
  if (state.planMode) return;
  if (pushHistory) {
    navHistory.splice(navIndex + 1);
    navHistory.push({ name, cat });
    navIndex = navHistory.length - 1;
    navUpdateButtons();
  }
  Object.keys(graphVisibleCats).forEach(k => { graphVisibleCats[k] = true; });
  state.selectedName = name;

  const cfg  = CAT_CONFIG[cat];
  const item = (state.data[cat] || []).find(i => i[cfg.nameKey] === name);
  if (!item) return;

  const listPanel = document.getElementById('cards-grid');
  document.querySelectorAll('.cat-card').forEach(c => {
    c.className = c.className.replace(/\bselected-\w+\b/g, '').trim();
    if (c.dataset.name === name && c.dataset.cat === cat) {
      c.classList.add(`selected-${cfg.cls}`);
      const top = c.offsetTop - listPanel.offsetTop;
      listPanel.scrollTo({ top: top - 40, behavior: 'smooth' });
    }
  });

  detailCurrentItem = item;
  detailCurrentCat  = cat;

  document.getElementById('detail-empty').style.display   = 'none';
  document.getElementById('detail-content').style.display = 'flex';
  document.querySelector('.catalog-body').classList.add('has-detail');
  if (window.innerWidth <= 720) setTimeout(graphResizeCanvas, 270);

  if (!cardPositionFixed && window.innerWidth > 720) {
    requestAnimationFrame(() => {
      if (window.innerWidth <= 720) return;
      const dc    = document.getElementById('detail-text');
      const panel = dc.parentElement.getBoundingClientRect();
      const rect  = dc.getBoundingClientRect();
      dc.style.bottom = 'auto'; dc.style.right = 'auto';
      dc.style.top    = (rect.top  - panel.top)  + 'px';
      dc.style.left   = (rect.left - panel.left) + 'px';
      cardPositionFixed = true;
    });
  }

  renderGraph(item, cat);
  renderDetailText(item, cat);
}

/* ── Mini force-directed graph ────────────────────────────── */
const G = {
  REPULSION:  120000,
  IDEAL_LEN:  160,
  ATTRACTION: 0.018,
  DAMPING:    0.76,
  GRAVITY:    0.001,
  STRATIFY:   0.045,
  COLUMN_X:   320,
  COOLING:    0.98,
  STOP_ALPHA: 0.001,
  CENTER_R:   26,
  NODE_R:     21,
  NODE_R2:    13,
  LABEL_H:    72,
};

const GPAL = {
  light: {
    tec: { bg: '#FFF7ED', edge: '#FED7AA', stroke: '#EA580C', text: '#C2410C' },
    dim: { bg: '#FDF2F8', edge: '#FBCFE8', stroke: '#DB2777', text: '#BE185D' },
    ins: { bg: '#EFF6FF', edge: '#BFDBFE', stroke: '#2563EB', text: '#1D4ED8' },
    her: { bg: '#ECFDF5', edge: '#A7F3D0', stroke: '#059669', text: '#047857' },
  },
  dark: {
    tec: { bg: 'rgba(234,88,12,0.15)',  edge: '#EA580C', stroke: '#FB923C', text: '#FDBA74' },
    dim: { bg: 'rgba(219,39,119,0.16)', edge: '#DB2777', stroke: '#F472B6', text: '#F9A8D4' },
    ins: { bg: 'rgba(37,99,235,0.15)',  edge: '#3B82F6', stroke: '#60A5FA', text: '#93C5FD' },
    her: { bg: 'rgba(5,150,105,0.15)', edge: '#059669', stroke: '#34D399', text: '#6EE7B7' },
  },
};

const GRAPH = {
  nodes: [], edges: [], rawNodes: [], rawEdges: [], hover: -1, alpha: 1, raf: null, canvas: null,
  camera: { x: 0, y: 0, scale: 1 },
  expanded: false,
  showOccasional: false,
  isPanning: false, panMoved: false,
  panStart: { x: 0, y: 0 }, camStart: { x: 0, y: 0 },
  dragNode: -1,
};

function graphStop() {
  if (GRAPH.raf !== null) { cancelAnimationFrame(GRAPH.raf); GRAPH.raf = null; }
}

function graphBuild(item, cat) {
  const cfg = CAT_CONFIG[cat];
  const nodes = [];
  const edges = [];
  const codeToIdx = new Map();

  nodes.push({
    x: 0, y: 0, vx: 0, vy: 0,
    r: G.CENTER_R, cat, cls: cfg.cls,
    name: item[cfg.nameKey], isCenter: true, targetX: 0,
  });
  codeToIdx.set(item['Código'], 0);

  function getRelationKind(srcItem, relField, targetCode) {
    return srcItem.rel_meta?.[relField]?.[targetCode] || 'complementaria';
  }

  function addEdge(parentIdx, nodeIdx, kind) {
    const existing = edges.find(e => (e.a === parentIdx && e.b === nodeIdx) ||
                                     (e.a === nodeIdx  && e.b === parentIdx));
    if (existing) {
      if (REL_PRIORITY[kind] > REL_PRIORITY[existing.kind]) existing.kind = kind;
      return;
    }
    const isTransversal = nodes[parentIdx]?.cat === 'dimensiones' || nodes[nodeIdx]?.cat === 'dimensiones';
    edges.push({ a: parentIdx, b: nodeIdx, kind, isTransversal });
  }

  function kindRadius(baseR, kind) {
    if (kind === 'complementaria') return Math.round(baseR * 0.65);
    if (kind === 'ocasional')      return Math.max(4, Math.round(baseR * 0.40));
    return baseR;
  }

  function addConnected(srcItem, srcCat, relDef, parentIdx, targetX, baseR) {
    if (!relDef) return [];
    const ncfg     = CAT_CONFIG[relDef.cat];
    const connected = findByCodes(srcItem[relDef.codeField] || [], relDef.cat);
    const result   = [];
    connected.forEach((ni, k) => {
      const code = ni['Código'];
      const kind = getRelationKind(srcItem, relDef.codeField, code);
      const r    = kindRadius(baseR, kind);
      let nodeIdx = codeToIdx.get(code);
      if (nodeIdx === undefined) {
        const spread = connected.length > 1
          ? (k - (connected.length - 1) / 2) * 220 : 0;
        nodeIdx = nodes.length;
        codeToIdx.set(code, nodeIdx);
        nodes.push({
          x: targetX + (Math.random() - 0.5) * 60,
          y: spread  + (Math.random() - 0.5) * 30,
          vx: 0, vy: 0,
          r, baseR, kindPriority: REL_PRIORITY[kind],
          cat: relDef.cat, cls: ncfg.cls,
          name: ni[ncfg.nameKey], isCenter: false, targetX,
        });
      } else if (!nodes[nodeIdx].isCenter && REL_PRIORITY[kind] > (nodes[nodeIdx].kindPriority || 0)) {
        nodes[nodeIdx].r            = kindRadius(nodes[nodeIdx].baseR, kind);
        nodes[nodeIdx].kindPriority = REL_PRIORITY[kind];
      }
      result.push({ idx: nodeIdx, dataItem: ni, dataCat: relDef.cat });
      addEdge(parentIdx, nodeIdx, kind);
    });
    return result;
  }

  const L1 = G.COLUMN_X;
  const L2 = G.COLUMN_X * 2.0;
  const L3 = G.COLUMN_X * 2.7;

  if (cat === 'instrumentos') {
    addConnected(item, cat, RELATIONS[cat].left,  0, -L1, G.NODE_R);
    addConnected(item, cat, DIMENSION_RELATION,   0, -L1, G.NODE_R);
    const tools = addConnected(item, cat, RELATIONS[cat].right, 0,  L1, G.NODE_R);
    if (GRAPH.expanded) {
      tools.forEach(({ idx, dataItem, dataCat }) =>
        addConnected(dataItem, dataCat, DIMENSION_RELATION, idx, L2, G.NODE_R2)
      );
    }
  } else if (cat === 'tecnicas' || cat === 'dimensiones') {
    addConnected(item, cat, DIMENSION_RELATION, 0, -L1, G.NODE_R);
    const l1 = addConnected(item, cat, RELATIONS[cat].right, 0, L1, G.NODE_R);
    l1.forEach(({ idx, dataItem, dataCat }) =>
      addConnected(dataItem, dataCat, RELATIONS[dataCat].right, idx, L2, G.NODE_R2)
    );
    if (GRAPH.expanded) {
      l1.forEach(({ idx, dataItem, dataCat }) => {
        addConnected(dataItem, dataCat, RELATIONS[dataCat].left, idx, L2, G.NODE_R2);
        addConnected(dataItem, dataCat, DIMENSION_RELATION, idx, L2, G.NODE_R2);
      });
    }
  } else {
    addConnected(item, cat, DIMENSION_RELATION, 0, L1, G.NODE_R);
    const l1 = addConnected(item, cat, RELATIONS[cat].left, 0, -L1, G.NODE_R);
    l1.forEach(({ idx, dataItem, dataCat }) =>
      addConnected(dataItem, dataCat, RELATIONS[dataCat].left, idx, -L2, G.NODE_R2)
    );
    if (GRAPH.expanded) {
      l1.forEach(({ idx, dataItem, dataCat }) => {
        addConnected(dataItem, dataCat, DIMENSION_RELATION, idx, L1, G.NODE_R2);
        addConnected(dataItem, dataCat, RELATIONS[dataCat].right, idx, -L3, G.NODE_R2);
      });
    }
  }

  function visibleGraph(rawNodes, rawEdges) {
    const visibleEdges = GRAPH.showOccasional
      ? rawEdges
      : rawEdges.filter(edge => edge.kind !== 'ocasional');
    const categoryVisible = idx => idx === 0 || graphVisibleCats[rawNodes[idx].cat];
    const reachable = new Set([0]);
    let changed = true;
    while (changed) {
      changed = false;
      visibleEdges.forEach(edge => {
        if (reachable.has(edge.a) && !reachable.has(edge.b) && categoryVisible(edge.b)) {
          reachable.add(edge.b);
          changed = true;
        }
        if (reachable.has(edge.b) && !reachable.has(edge.a) && categoryVisible(edge.a)) {
          reachable.add(edge.a);
          changed = true;
        }
      });
    }
    const indexMap = new Map();
    const keptNodes = [];
    rawNodes.forEach((node, idx) => {
      if (!reachable.has(idx)) return;
      indexMap.set(idx, keptNodes.length);
      keptNodes.push(node);
    });
    const keptEdges = visibleEdges
      .filter(edge => reachable.has(edge.a) && reachable.has(edge.b))
      .map(edge => ({ ...edge, a: indexMap.get(edge.a), b: indexMap.get(edge.b) }));
    return { nodes: keptNodes, edges: keptEdges };
  }

  const visible = visibleGraph(nodes, edges);
  GRAPH.rawNodes = nodes;
  GRAPH.rawEdges = edges;
  GRAPH.nodes  = visible.nodes;
  GRAPH.edges  = visible.edges;
  GRAPH.alpha  = 1;
  GRAPH.hover  = -1;
  GRAPH.camera = { x: 0, y: 0, scale: 1 };
  updateTabGraphCounts();
}

function graphTick() {
  const { nodes, edges } = GRAPH;
  const n = nodes.length;

  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      let dx = nodes[j].x - nodes[i].x;
      let dy = nodes[j].y - nodes[i].y;
      const d2 = dx * dx + dy * dy || 0.01;
      const d  = Math.sqrt(d2);
      const f  = (G.REPULSION * GRAPH.alpha) / d2;
      dx /= d; dy /= d;
      nodes[i].vx -= dx * f; nodes[i].vy -= dy * f;
      nodes[j].vx += dx * f; nodes[j].vy += dy * f;
    }
  }

  edges.forEach(({ a, b }) => {
    const na = nodes[a], nb = nodes[b];
    const dx = nb.x - na.x, dy = nb.y - na.y;
    const d  = Math.sqrt(dx * dx + dy * dy) || 0.01;
    const f  = (d - G.IDEAL_LEN) * G.ATTRACTION;
    const ux = dx / d, uy = dy / d;
    na.vx += ux * f; na.vy += uy * f;
    nb.vx -= ux * f; nb.vy -= uy * f;
  });

  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const ni = nodes[i], nj = nodes[j];
      const dx = nj.x - ni.x, dy = nj.y - ni.y;
      const d2 = dx * dx + dy * dy || 0.01;
      const minD = ni.r + nj.r + G.LABEL_H;
      if (d2 < minD * minD) {
        const d    = Math.sqrt(d2);
        const push = (minD - d) / d * 0.5;
        ni.vx -= dx * push; ni.vy -= dy * push;
        nj.vx += dx * push; nj.vy += dy * push;
      }
    }
  }

  nodes.forEach((nd, i) => {
    if (i === 0 || nd.fixed) { nd.vx = 0; nd.vy = 0; return; }
    nd.vx += (nd.targetX - nd.x) * G.STRATIFY;
    nd.vy -= nd.y * G.GRAVITY;
    nd.vx *= G.DAMPING; nd.vy *= G.DAMPING;
    nd.x  += nd.vx;    nd.y  += nd.vy;
  });

  GRAPH.alpha *= G.COOLING;
}

function wrapLabel(ctx, text, maxWidth) {
  const words = text.split(' ');
  const lines = [];
  let line = '';
  for (const word of words) {
    const test = line ? line + ' ' + word : word;
    if (line && ctx.measureText(test).width > maxWidth) {
      lines.push(line);
      line = word;
    } else {
      line = test;
    }
  }
  if (line) lines.push(line);
  return lines.slice(0, 2);
}

function graphDraw() {
  const canvas = GRAPH.canvas;
  if (!canvas) return;
  graphResizeCanvas();
  const dpr  = window.devicePixelRatio || 1;
  const ctx  = canvas.getContext('2d');
  const cw   = canvas.width, ch = canvas.height;
  const w    = cw / dpr, h = ch / dpr;
  const dark = document.documentElement.dataset.theme === 'dark';
  const pal  = dark ? GPAL.dark : GPAL.light;
  const hov  = GRAPH.hover;

  const cam = GRAPH.camera;
  ctx.clearRect(0, 0, cw, ch);
  ctx.save();
  ctx.scale(dpr, dpr);
  ctx.translate(w / 2, h / 2);
  ctx.scale(cam.scale, cam.scale);
  ctx.translate(-cam.x, -cam.y);

  GRAPH.edges.forEach(({ a, b, kind, isTransversal }) => {
    const nb = GRAPH.nodes[b];
    const na = GRAPH.nodes[a];
    const col = isTransversal ? pal.dim : pal[nb.cls];
    ctx.beginPath();
    ctx.moveTo(na.x, na.y);
    ctx.lineTo(nb.x, nb.y);
    ctx.strokeStyle = col.edge + (dark ? '88' : '66');
    ctx.lineWidth   = 2;
    ctx.stroke();
  });

  GRAPH.nodes.forEach((nd, i) => {
    const col   = pal[nd.cls];
    const isHov = i === hov && !nd.isCenter;
    const r     = isHov ? nd.r + 2 : nd.r;
    const alpha = nd.isCenter ? 1.0
      : nd.kindPriority === 3 ? 1.0
      : nd.kindPriority === 2 ? 0.65
      : 0.40;

    ctx.save();
    ctx.globalAlpha = isHov ? Math.min(1, alpha + 0.2) : alpha;
    ctx.beginPath();
    ctx.arc(nd.x, nd.y, r, 0, Math.PI * 2);
    ctx.fillStyle   = col.bg;
    ctx.fill();
    ctx.lineWidth   = nd.isCenter ? 2.5 : isHov ? 2.2 : 1.5;
    ctx.strokeStyle = nd.isCenter || isHov ? col.stroke : col.edge;
    ctx.stroke();
    ctx.restore();

    const fs     = nd.isCenter ? 13 : 11;
    const maxW   = nd.isCenter ? 160 : 140;
    const lineH  = fs + 2;
    const pad    = 3;
    ctx.font         = `${nd.isCenter ? 700 : 500} ${fs}px -apple-system,BlinkMacSystemFont,sans-serif`;
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'top';
    const lines  = wrapLabel(ctx, nd.name, maxW);
    lines.forEach((line, li) => {
      const tw = ctx.measureText(line).width;
      const tx = nd.x;
      const ty = nd.y + r + 4 + li * lineH;
      ctx.fillStyle = dark ? 'rgba(15,23,42,0.82)' : 'rgba(255,255,255,0.88)';
      ctx.fillRect(tx - tw / 2 - pad, ty - 1, tw + pad * 2, fs + 3);
      ctx.fillStyle = col.text;
      ctx.fillText(line, tx, ty);
    });
  });

  ctx.restore();
}

function graphResizeCanvas() {
  const canvas = GRAPH.canvas;
  if (!canvas || !canvas.clientWidth) return;
  const dpr = window.devicePixelRatio || 1;
  canvas.width  = Math.round(canvas.clientWidth  * dpr);
  canvas.height = Math.round(canvas.clientHeight * dpr);
}

function graphHitTest(sx, sy) {
  const canvas = GRAPH.canvas;
  if (!canvas) return -1;
  const dpr = window.devicePixelRatio || 1;
  const w   = canvas.width / dpr, h = canvas.height / dpr;
  const cam = GRAPH.camera;
  const wx = (sx - w / 2) / cam.scale + cam.x;
  const wy = (sy - h / 2) / cam.scale + cam.y;
  for (let i = GRAPH.nodes.length - 1; i >= 0; i--) {
    const nd = GRAPH.nodes[i];
    const dx = wx - nd.x, dy = wy - nd.y;
    if (dx * dx + dy * dy <= (nd.r + 4) * (nd.r + 4)) return i;
  }
  return -1;
}

function graphLoop() {
  if (GRAPH.alpha > G.STOP_ALPHA) graphTick();
  graphDraw();
  GRAPH.raf = requestAnimationFrame(graphLoop);
}

function graphCenterNodeScreen(cat) {
  const canvas = GRAPH.canvas;
  if (!canvas) return { x: canvas ? canvas.clientWidth / 2 : 0, y: 0 };
  const cw = canvas.clientWidth;
  const ch = canvas.clientHeight;

  const card       = document.getElementById('detail-text');
  const canvasRect = canvas.getBoundingClientRect();
  const cardRect   = card ? card.getBoundingClientRect() : null;
  const cardLeft   = cardRect ? Math.max(0, cardRect.left - canvasRect.left) : cw;
  const freeWidth  = cardLeft;

  const PAD = 90;
  const sy  = ch / 2;

  let sx;
  if (cat === 'tecnicas' || cat === 'dimensiones') {
    sx = PAD;
  } else {
    sx = freeWidth / 2;
  }
  return { x: sx, y: sy };
}

function renderGraph(item, cat) {
  graphStop();
  const canvas = document.getElementById('hub-canvas');
  if (!canvas) return;
  const toggleBtn = document.getElementById('btn-toggle-graph');
  if (toggleBtn) {
    toggleBtn.classList.toggle('active', GRAPH.expanded);
    toggleBtn.setAttribute('aria-pressed', String(GRAPH.expanded));
  }
  const essentialBtn = document.getElementById('btn-toggle-essential');
  if (essentialBtn) {
    essentialBtn.classList.toggle('active', GRAPH.showOccasional);
    essentialBtn.setAttribute('aria-pressed', String(GRAPH.showOccasional));
  }
  GRAPH.canvas = canvas;
  graphBuild(item, cat);
  requestAnimationFrame(() => {
    graphResizeCanvas();
    const target   = graphCenterNodeScreen(cat);
    const cw       = canvas.clientWidth;
    const ch       = canvas.clientHeight;
    GRAPH.camera.x = cw / 2 - target.x;
    GRAPH.camera.y = ch / 2 - target.y;
    graphLoop();
  });
}

/* ── Detail text ──────────────────────────────────────────── */
function gridSection(label, value) {
  if (!value) return '';
  return `<div class="ds-item">
    <div class="ds-label">${label}</div>
    <div class="ds-body">${value}</div>
  </div>`;
}

function getRelationNames(item, relField, targetCat) {
  const cfg = CAT_CONFIG[targetCat];
  const items = state.data[targetCat] || [];
  const byCode = new Map(items.map(i => [i['Código'], i[cfg.nameKey]]));
  return (item[relField] || []).map(code => ({
    code,
    name: byCode.get(code) || code,
    kind: item.rel_meta?.[relField]?.[code] || 'complementaria'
  }));
}

function groupedRelationSection(title, relations) {
  if (!relations.length) return '';
  const labels = i18n().relKinds;
  const parts = ['principal', 'complementaria', 'ocasional'].map(kind => {
    const names = relations.filter(r => r.kind === kind).map(r => r.name);
    if (!names.length) return '';
    return `<div class="relation-group"><b>${labels[kind]}:</b> ${names.join(', ')}</div>`;
  }).join('');
  return gridSection(title, parts);
}

function renderDetailText(item, cat) {
  const cfg  = CAT_CONFIG[cat];
  const name = item[cfg.nameKey];
  const i    = i18n();
  const h    = i.detailHeaders[cat];
  const cl   = i.detailChipLabels;

  const metaPairs = [];
  if (item['Fase'])          metaPairs.push([cl.Fase,          translateValue('Fase',          item['Fase'])]);
  if (item['Participación']) metaPairs.push([cl.Participación, translateValue('Participación', item['Participación'])]);
  if (item['Complejidad'])   metaPairs.push([cl.Complejidad,   translateValue('Complejidad',   item['Complejidad'])]);
  if (item['Tipo'])          metaPairs.push([cl.Tipo,          item['Tipo']]);
  const metaChips = metaPairs.map(([k, v]) =>
    `<span class="detail-chip"><b>${k}:</b> ${v}</span>`
  ).join('');

  let gridItems = '';
  if (cat === 'tecnicas') {
    gridItems =
      gridSection(h.gridLabel1, item[h.gridField1]) +
      gridSection(h.gridLabel2, item[h.gridField2]) +
      gridSection(h.gridLabel3, item[h.gridField3]) +
      gridSection(h.gridLabel4, item[h.gridField4]) +
      groupedRelationSection(h.rel_ins, getRelationNames(item, 'rel_ins', 'instrumentos')) +
      groupedRelationSection(h.rel_her, getRelationNames(item, 'rel_her', 'herramientas'));
  } else if (cat === 'dimensiones') {
    gridItems =
      gridSection(h.gridLabel1, item[h.gridField1]) +
      gridSection(h.gridLabel2, item[h.gridField2]) +
      gridSection(h.gridLabel3, item[h.gridField3]) +
      gridSection(h.gridLabel4, item[h.gridField4]) +
      groupedRelationSection(h.rel_ins, getRelationNames(item, 'rel_ins', 'instrumentos')) +
      groupedRelationSection(h.rel_her, getRelationNames(item, 'rel_her', 'herramientas'));
  } else if (cat === 'instrumentos') {
    gridItems =
      gridSection(h.gridLabel1, item[h.gridField1]) +
      groupedRelationSection(h.rel_tec, getRelationNames(item, 'rel_tec', 'tecnicas')) +
      groupedRelationSection(h.rel_dim, getRelationNames(item, 'rel_dim', 'dimensiones')) +
      groupedRelationSection(h.rel_her, getRelationNames(item, 'rel_her', 'herramientas'));
  } else {
    gridItems =
      gridSection(h.gridLabel1, item[h.gridField1]) +
      gridSection(h.gridLabel2, item[h.gridField2]) +
      groupedRelationSection(h.rel_dim, getRelationNames(item, 'rel_dim', 'dimensiones')) +
      groupedRelationSection(h.rel_ins, getRelationNames(item, 'rel_ins', 'instrumentos')) +
      gridSection(h.gridLabel3, item[h.gridField3]) +
      gridSection(h.gridLabel4, item[h.gridField4]);
  }

  const detDesc = item['Descripción detallada'] || '';

  document.getElementById('detail-text-body').scrollTop = 0;
  document.getElementById('detail-text-body').innerHTML = `
    <div class="detail-header">
      <div>
        <span class="modal-type-badge ${cfg.cls}">${cfg.singularLabel}</span>
        <h2 class="detail-title">${name}</h2>
        <p class="detail-subtitle">${item['Descripción breve'] || ''}</p>
      </div>
      ${metaChips ? `<div class="detail-chips">${metaChips}</div>` : ''}
    </div>

    ${detDesc ? `
      <div class="detail-desc-wrap">
        <div class="ds-label">${i.descriptionLabel}</div>
        <div class="detail-desc">${detDesc}</div>
      </div>` : ''}

    ${gridItems ? `<div class="detail-sections-grid">${gridItems}</div>` : ''}`;
}

/* ── Detail card export helpers ───────────────────────────── */
let detailCurrentItem = null;
let detailCurrentCat  = null;
let cardPositionFixed = false;

const navHistory = [];
let   navIndex   = -1;

function navUpdateButtons() {
  const back = document.getElementById('btn-nav-back');
  const fwd  = document.getElementById('btn-nav-fwd');
  if (back) back.disabled = navIndex <= 0;
  if (fwd)  fwd.disabled  = navIndex >= navHistory.length - 1;
}

function itemToMarkdown(item, cat) {
  const cfg  = CAT_CONFIG[cat];
  const name = item[cfg.nameKey];
  const i    = i18n();
  let md = `# ${name}\n\n**${cfg.singularLabel}**\n\n`;
  if (item['Descripción breve']) md += `${item['Descripción breve']}\n\n`;
  const meta = [];
  if (item['Fase'])          meta.push(`**${i.detailChipLabels.Fase}:** ${translateValue('Fase', item['Fase'])}`);
  if (item['Participación']) meta.push(`**${i.detailChipLabels.Participación}:** ${translateValue('Participación', item['Participación'])}`);
  if (item['Complejidad'])   meta.push(`**${i.detailChipLabels.Complejidad}:** ${translateValue('Complejidad', item['Complejidad'])}`);
  if (item['Tipo'])          meta.push(`**${i.detailChipLabels.Tipo}:** ${item['Tipo']}`);
  if (meta.length) md += meta.join(' | ') + '\n\n';
  if (item['Descripción detallada']) md += `## ${i.descriptionLabel}\n\n${item['Descripción detallada']}\n\n`;
  const secs = i.mdSectionLabels[cat] || [];
  secs.forEach(([label, field]) => { if (item[field]) md += `## ${label}\n\n${item[field]}\n\n`; });
  return md.trim();
}

function buildPrintHtml(item, cat) {
  const cfg  = CAT_CONFIG[cat];
  const i    = i18n();
  let body = `<h1>${item[cfg.nameKey]}</h1><p class="type">${cfg.singularLabel}</p>`;
  if (item['Descripción breve']) body += `<p class="brief">${item['Descripción breve']}</p>`;
  const meta = [];
  if (item['Fase'])          meta.push(`<b>${i.detailChipLabels.Fase}:</b> ${translateValue('Fase', item['Fase'])}`);
  if (item['Participación']) meta.push(`<b>${i.detailChipLabels.Participación}:</b> ${translateValue('Participación', item['Participación'])}`);
  if (item['Complejidad'])   meta.push(`<b>${i.detailChipLabels.Complejidad}:</b> ${translateValue('Complejidad', item['Complejidad'])}`);
  if (item['Tipo'])          meta.push(`<b>${i.detailChipLabels.Tipo}:</b> ${item['Tipo']}`);
  if (meta.length) body += `<p class="meta">${meta.join(' &nbsp;·&nbsp; ')}</p>`;
  if (item['Descripción detallada']) body += `<h2>${i.descriptionLabel}</h2><p>${item['Descripción detallada']}</p>`;
  const secs = i.mdSectionLabels[cat] || [];
  secs.forEach(([label, field]) => { if (item[field]) body += `<h2>${label}</h2><p>${item[field]}</p>`; });
  return body;
}

/* ── Theme ────────────────────────────────────────────────── */
let darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.dataset.theme = darkMode ? 'dark' : '';
function toggleTheme() {
  darkMode = !darkMode;
  document.documentElement.dataset.theme = darkMode ? 'dark' : '';
  document.getElementById('btn-theme').textContent = darkMode ? i18n().lightMode : i18n().darkMode;
}

/* ── Events ───────────────────────────────────────────────── */
function initEvents() {
  document.querySelectorAll('.home-card[data-cat]').forEach(card =>
    card.addEventListener('click', () => showCatalog(card.dataset.cat))
  );

  document.getElementById('btn-home').addEventListener('click', showHome);

  document.querySelectorAll('.cat-tab').forEach(tab =>
    tab.addEventListener('click', () => showCatalog(tab.dataset.cat))
  );
  document.getElementById('btn-theme').addEventListener('click', toggleTheme);
  document.getElementById('btn-toggle-graph').addEventListener('click', () => {
    if (!detailCurrentItem || !detailCurrentCat) return;
    GRAPH.expanded = !GRAPH.expanded;
    renderGraph(detailCurrentItem, detailCurrentCat);
  });
  document.getElementById('btn-toggle-essential').addEventListener('click', () => {
    if (!detailCurrentItem || !detailCurrentCat) return;
    GRAPH.showOccasional = !GRAPH.showOccasional;
    renderGraph(detailCurrentItem, detailCurrentCat);
  });
  document.getElementById('btn-nav-back').addEventListener('click', () => {
    if (navIndex <= 0) return;
    navIndex--;
    const { name, cat } = navHistory[navIndex];
    navUpdateButtons();
    showDetailPanel(name, cat, false);
  });
  document.getElementById('btn-nav-fwd').addEventListener('click', () => {
    if (navIndex >= navHistory.length - 1) return;
    navIndex++;
    const { name, cat } = navHistory[navIndex];
    navUpdateButtons();
    showDetailPanel(name, cat, false);
  });
  document.querySelectorAll('.graph-cat-chip[data-graph-cat]').forEach(chip => {
    chip.addEventListener('click', () => {
      if (!detailCurrentItem || !detailCurrentCat) return;
      const cat = chip.dataset.graphCat;
      graphVisibleCats[cat] = !graphVisibleCats[cat];
      if (cat === detailCurrentCat) graphVisibleCats[cat] = true;
      renderGraph(detailCurrentItem, detailCurrentCat);
    });
  });

  document.getElementById('search-input').addEventListener('input', e => {
    state.search = e.target.value.trim();
    renderCards();
  });

  document.getElementById('global-filter-bar').addEventListener('click', e => {
    e.stopPropagation();
    // Toggle popover
    if (e.target.closest('#gf-trigger')) {
      const pop = document.getElementById('gf-popover');
      if (!pop) return;
      const open = pop.style.display !== 'none';
      if (open) {
        closeGfPopover();
      } else {
        pop.style.display = '';
        document.getElementById('gf-trigger').classList.add('gf-btn--open');
        document.getElementById('gf-backdrop')?.classList.add('open');
      }
      return;
    }
    // Chip inside popover
    const chip = e.target.closest('.gf-popover [data-gf]');
    if (chip) {
      const key = chip.dataset.gf;
      if (key === 'extra') state.extra = chip.dataset.gv;
      else state[GF_STATE[key]] = chip.dataset.gv;
      renderGlobalFilters();
      applyGlobalFilterToGraph();
      if (state.cat) renderCards();
      return;
    }
    // × pill remove
    const pillX = e.target.closest('.gf-pill-x');
    if (pillX) {
      const key = pillX.dataset.gf;
      if (key === 'extra') state.extra = '';
      else state[GF_STATE[key]] = '';
      renderGlobalFilters();
      applyGlobalFilterToGraph();
      if (state.cat) renderCards();
      return;
    }
    // Clear all
    if (e.target.closest('#gf-clear') || e.target.closest('#gf-clear-ext')) {
      state.gFase = ''; state.gParticipacion = '';
      state.gModalidad = ''; state.gLugar = ''; state.gAgrupamiento = ''; state.gResIA = '';
      state.extra = '';
      renderGlobalFilters();
      applyGlobalFilterToGraph();
      if (state.cat) renderCards();
    }
  });

  document.getElementById('gf-pills-bar').addEventListener('click', e => {
    const pillX = e.target.closest('.gf-pill-x');
    if (pillX) {
      const key = pillX.dataset.gf;
      if (key === 'extra') state.extra = '';
      else state[GF_STATE[key]] = '';
      renderGlobalFilters();
      applyGlobalFilterToGraph();
      if (state.cat) renderCards();
      return;
    }
    if (e.target.closest('#gf-clear-ext')) {
      state.gFase = ''; state.gParticipacion = '';
      state.gModalidad = ''; state.gLugar = ''; state.gAgrupamiento = ''; state.gResIA = '';
      state.extra = '';
      renderGlobalFilters();
      applyGlobalFilterToGraph();
      if (state.cat) renderCards();
    }
  });

  // Close popover on outside click or backdrop click
  document.addEventListener('click', e => {
    if (!e.target.closest('#global-filter-bar')) closeGfPopover();
  });
  document.getElementById('gf-backdrop').addEventListener('click', closeGfPopover);

  document.getElementById('cards-grid').addEventListener('click', e => {
    const card = e.target.closest('.cat-card[data-name]');
    if (!card) return;
    if (state.planMode) togglePlanItem(card.dataset.code, card.dataset.name, card.dataset.cat);
    else showDetailPanel(card.dataset.name, card.dataset.cat);
  });
  document.getElementById('cards-grid').addEventListener('keydown', e => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const card = e.target.closest('.cat-card[data-name]');
    if (!card) return;
    if (state.planMode) togglePlanItem(card.dataset.code, card.dataset.name, card.dataset.cat);
    else showDetailPanel(card.dataset.name, card.dataset.cat);
  });

  // Language switcher
  document.querySelectorAll('.lang-btn[data-lang]').forEach(btn =>
    btn.addEventListener('click', () => setLang(btn.dataset.lang))
  );

  // Plan mode
  document.getElementById('btn-plan-mode').addEventListener('click', () => {
    if (state.planMode) exitPlanMode(); else enterPlanMode();
  });
  document.getElementById('btn-plan-clear').addEventListener('click', () => {
    state.planSelected = new Map();
    state.planExpandedDim = null;
    updatePlanToolbar();
    renderCards();
    renderPlanCoverage();
  });

  // Plan panel delegation (chip remove, dim expand, suggest add)
  document.getElementById('plan-coverage-panel').addEventListener('click', e => {
    const removeBtn = e.target.closest('.plan-chip-remove');
    if (removeBtn) {
      state.planSelected.delete(removeBtn.dataset.code);
      updatePlanToolbar();
      renderCards();
      renderPlanCoverage();
      return;
    }
    const suggestBtn = e.target.closest('.plan-suggest-btn');
    if (suggestBtn) {
      const code = suggestBtn.dataset.code;
      const name = suggestBtn.dataset.name;
      const item = (state.data.herramientas || []).find(h => h['Código'] === code);
      state.planSelected.set(code, { name, cat: 'herramientas', item });
      state.planExpandedDim = null;
      updatePlanToolbar();
      renderCards();
      renderPlanCoverage();
      return;
    }
    const dimItem = e.target.closest('.plan-dim-item.uncovered');
    if (dimItem) {
      const code = dimItem.dataset.dim;
      state.planExpandedDim = state.planExpandedDim === code ? null : code;
      renderPlanCoverage();
    }
  });

  // Canvas — zoom (wheel), pan (drag), hover, click
  const hubCanvas = document.getElementById('hub-canvas');

  hubCanvas.addEventListener('wheel', e => {
    e.preventDefault();
    const rect   = hubCanvas.getBoundingClientRect();
    const dpr    = window.devicePixelRatio || 1;
    const cw     = hubCanvas.width / dpr, ch = hubCanvas.height / dpr;
    const cam    = GRAPH.camera;
    const mx     = e.clientX - rect.left, my = e.clientY - rect.top;
    const wx     = (mx - cw / 2) / cam.scale + cam.x;
    const wy     = (my - ch / 2) / cam.scale + cam.y;
    const factor = e.deltaY < 0 ? 1.15 : 1 / 1.15;
    cam.scale    = Math.max(0.2, Math.min(6, cam.scale * factor));
    cam.x        = wx - (mx - cw / 2) / cam.scale;
    cam.y        = wy - (my - ch / 2) / cam.scale;
  }, { passive: false });

  hubCanvas.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    const tipEl = document.getElementById('graph-tooltip');
    if (tipEl) tipEl.classList.remove('visible');
    const rect = hubCanvas.getBoundingClientRect();
    const idx  = graphHitTest(e.clientX - rect.left, e.clientY - rect.top);
    if (idx > 0) {
      GRAPH.dragNode  = idx;
      GRAPH.nodes[idx].fixed = true;
      GRAPH.alpha     = Math.max(GRAPH.alpha, 0.3);
      GRAPH.panMoved  = false;
      GRAPH.panStart  = { x: e.clientX, y: e.clientY };
      hubCanvas.style.cursor = 'grabbing';
    } else {
      GRAPH.isPanning = true;
      GRAPH.panMoved  = false;
      GRAPH.panStart  = { x: e.clientX, y: e.clientY };
      GRAPH.camStart  = { x: GRAPH.camera.x, y: GRAPH.camera.y };
      hubCanvas.style.cursor = 'grabbing';
    }
    e.preventDefault();
  });

  hubCanvas.addEventListener('mousemove', e => {
    const rect = hubCanvas.getBoundingClientRect();
    if (GRAPH.dragNode >= 0) {
      if (Math.hypot(e.clientX - GRAPH.panStart.x, e.clientY - GRAPH.panStart.y) > 4)
        GRAPH.panMoved = true;
      const dpr = window.devicePixelRatio || 1;
      const cw  = hubCanvas.width / dpr, ch = hubCanvas.height / dpr;
      const cam = GRAPH.camera;
      const sx  = e.clientX - rect.left;
      const sy  = e.clientY - rect.top;
      const nd  = GRAPH.nodes[GRAPH.dragNode];
      nd.x  = (sx - cw / 2) / cam.scale + cam.x;
      nd.y  = (sy - ch / 2) / cam.scale + cam.y;
      nd.vx = 0; nd.vy = 0;
      return;
    }
    if (GRAPH.isPanning) {
      const dx = e.clientX - GRAPH.panStart.x;
      const dy = e.clientY - GRAPH.panStart.y;
      if (Math.hypot(dx, dy) > 3) GRAPH.panMoved = true;
      GRAPH.camera.x = GRAPH.camStart.x - dx / GRAPH.camera.scale;
      GRAPH.camera.y = GRAPH.camStart.y - dy / GRAPH.camera.scale;
      return;
    }
    const idx = graphHitTest(e.clientX - rect.left, e.clientY - rect.top);
    GRAPH.hover = idx;
    hubCanvas.style.cursor = idx > 0 ? 'pointer' : 'grab';
    const tip = document.getElementById('graph-tooltip');
    if (idx >= 0 && tip) {
      const nd  = GRAPH.nodes[idx];
      const cfg = CAT_CONFIG[nd.cat];
      const dataItem = (state.data[nd.cat] || []).find(i => i[cfg.nameKey] === nd.name);
      const desc = dataItem?.['Descripción breve'] || '';
      tip.innerHTML = `<div class="graph-tooltip-name">${nd.name}</div>${desc ? `<div class="graph-tooltip-desc">${desc}</div>` : ''}`;
      const cx = e.clientX - rect.left;
      const cy = e.clientY - rect.top;
      const tw = 224, th = 80;
      const cw = hubCanvas.clientWidth, ch = hubCanvas.clientHeight;
      const left = cx + 14 + tw > cw ? cx - tw - 10 : cx + 14;
      const top  = cy + 10 + th > ch ? cy - th - 6  : cy + 10;
      tip.style.left = left + 'px';
      tip.style.top  = top  + 'px';
      tip.classList.add('visible');
    } else if (tip) {
      tip.classList.remove('visible');
    }
  });

  hubCanvas.addEventListener('mouseleave', () => {
    if (!GRAPH.isPanning) {
      GRAPH.hover = -1;
      hubCanvas.style.cursor = 'default';
      const tip = document.getElementById('graph-tooltip');
      if (tip) tip.classList.remove('visible');
    }
  });

  document.addEventListener('mouseup', () => {
    if (GRAPH.dragNode >= 0) {
      GRAPH.nodes[GRAPH.dragNode].fixed = false;
      GRAPH.dragNode = -1;
      GRAPH.alpha = Math.max(GRAPH.alpha, 0.1);
      if (GRAPH.canvas) GRAPH.canvas.style.cursor = 'grab';
    }
    if (GRAPH.isPanning) {
      GRAPH.isPanning = false;
      if (GRAPH.canvas) GRAPH.canvas.style.cursor = 'grab';
    }
  });

  hubCanvas.addEventListener('click', e => {
    if (GRAPH.panMoved) { GRAPH.panMoved = false; return; }
    const rect = hubCanvas.getBoundingClientRect();
    const idx  = graphHitTest(e.clientX - rect.left, e.clientY - rect.top);
    if (idx <= 0 || !GRAPH.nodes[idx]) return;
    const nd = GRAPH.nodes[idx];
    if (nd.cat !== state.cat) {
      showCatalog(nd.cat);
      setTimeout(() => showDetailPanel(nd.name, nd.cat), 0);
    } else {
      showDetailPanel(nd.name, nd.cat);
    }
  });

  hubCanvas.addEventListener('dblclick', () => {
    GRAPH.camera = { x: 0, y: 0, scale: 1 };
  });

  // ── Touch support for canvas ─────────────────────────────
  let lastTouchDist = 0;
  let lastTouchMidX = 0, lastTouchMidY = 0;

  hubCanvas.addEventListener('touchstart', e => {
    if (!GRAPH.nodes.length) return;
    e.preventDefault();
    if (e.touches.length === 1) {
      const t = e.touches[0];
      const rect = hubCanvas.getBoundingClientRect();
      const idx  = graphHitTest(t.clientX - rect.left, t.clientY - rect.top);
      if (idx > 0) {
        GRAPH.dragNode = idx;
        GRAPH.nodes[idx].fixed = true;
        GRAPH.alpha    = Math.max(GRAPH.alpha, 0.3);
        GRAPH.panMoved = false;
        GRAPH.panStart = { x: t.clientX, y: t.clientY };
      } else {
        GRAPH.isPanning = true;
        GRAPH.panMoved  = false;
        GRAPH.panStart  = { x: t.clientX, y: t.clientY };
        GRAPH.camStart  = { x: GRAPH.camera.x, y: GRAPH.camera.y };
      }
    } else if (e.touches.length === 2) {
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      lastTouchDist = Math.hypot(dx, dy);
      lastTouchMidX = (e.touches[0].clientX + e.touches[1].clientX) / 2;
      lastTouchMidY = (e.touches[0].clientY + e.touches[1].clientY) / 2;
      GRAPH.isPanning = false;
      if (GRAPH.dragNode >= 0) {
        GRAPH.nodes[GRAPH.dragNode].fixed = false;
        GRAPH.dragNode = -1;
      }
    }
  }, { passive: false });

  hubCanvas.addEventListener('touchmove', e => {
    if (!GRAPH.nodes.length) return;
    e.preventDefault();
    const rect = hubCanvas.getBoundingClientRect();
    if (e.touches.length === 1) {
      const t = e.touches[0];
      if (GRAPH.dragNode >= 0) {
        if (Math.hypot(t.clientX - GRAPH.panStart.x, t.clientY - GRAPH.panStart.y) > 4)
          GRAPH.panMoved = true;
        const dpr = window.devicePixelRatio || 1;
        const cw  = hubCanvas.width / dpr, ch = hubCanvas.height / dpr;
        const cam = GRAPH.camera;
        const nd  = GRAPH.nodes[GRAPH.dragNode];
        nd.x  = (t.clientX - rect.left - cw / 2) / cam.scale + cam.x;
        nd.y  = (t.clientY - rect.top  - ch / 2) / cam.scale + cam.y;
        nd.vx = 0; nd.vy = 0;
        return;
      }
      if (GRAPH.isPanning) {
        const dx = t.clientX - GRAPH.panStart.x;
        const dy = t.clientY - GRAPH.panStart.y;
        if (Math.hypot(dx, dy) > 3) GRAPH.panMoved = true;
        GRAPH.camera.x = GRAPH.camStart.x - dx / GRAPH.camera.scale;
        GRAPH.camera.y = GRAPH.camStart.y - dy / GRAPH.camera.scale;
      }
    } else if (e.touches.length === 2) {
      const dx   = e.touches[0].clientX - e.touches[1].clientX;
      const dy   = e.touches[0].clientY - e.touches[1].clientY;
      const dist = Math.hypot(dx, dy);
      if (lastTouchDist > 0) {
        const dpr  = window.devicePixelRatio || 1;
        const cw   = hubCanvas.width / dpr, ch = hubCanvas.height / dpr;
        const cam  = GRAPH.camera;
        const mx   = ((e.touches[0].clientX + e.touches[1].clientX) / 2) - rect.left;
        const my   = ((e.touches[0].clientY + e.touches[1].clientY) / 2) - rect.top;
        const wx   = (mx - cw / 2) / cam.scale + cam.x;
        const wy   = (my - ch / 2) / cam.scale + cam.y;
        const factor = dist / lastTouchDist;
        cam.scale  = Math.max(0.2, Math.min(6, cam.scale * factor));
        cam.x      = wx - (mx - cw / 2) / cam.scale;
        cam.y      = wy - (my - ch / 2) / cam.scale;
      }
      lastTouchDist = dist;
    }
  }, { passive: false });

  hubCanvas.addEventListener('touchend', e => {
    e.preventDefault();
    const wasPanning = GRAPH.isPanning;
    if (GRAPH.dragNode >= 0) {
      GRAPH.nodes[GRAPH.dragNode].fixed = false;
      GRAPH.dragNode = -1;
      GRAPH.alpha = Math.max(GRAPH.alpha, 0.1);
    }
    GRAPH.isPanning = false;
    lastTouchDist   = 0;
    if (!GRAPH.panMoved && wasPanning && e.changedTouches.length === 1) {
      const t    = e.changedTouches[0];
      const rect = hubCanvas.getBoundingClientRect();
      const idx  = graphHitTest(t.clientX - rect.left, t.clientY - rect.top);
      if (idx > 0 && GRAPH.nodes[idx]) {
        const nd = GRAPH.nodes[idx];
        if (nd.cat !== state.cat) {
          showCatalog(nd.cat);
          setTimeout(() => showDetailPanel(nd.name, nd.cat), 0);
        } else {
          showDetailPanel(nd.name, nd.cat);
        }
      }
    }
    GRAPH.panMoved = false;
  }, { passive: false });

  window.addEventListener('resize', () => {
    graphResizeCanvas();
    if (window.innerWidth <= 720) {
      const dc = document.getElementById('detail-text');
      dc.style.bottom = '';
      dc.style.right  = '';
      dc.style.top    = '';
      dc.style.left   = '';
      dc.style.maxHeight = '';
      cardPositionFixed = false;
    }
  });

  // Draggable detail card
  const detailCard   = document.getElementById('detail-text');
  const dragHandle   = document.getElementById('detail-drag-handle');
  let cardDrag = null;

  document.querySelectorAll('.detail-tool-btn').forEach(btn =>
    btn.addEventListener('mousedown', e => e.stopPropagation())
  );

  function flashBtn(btn) {
    const orig = btn.innerHTML;
    btn.classList.add('btn-ok');
    btn.innerHTML = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8l3.5 3.5L13 4.5"/></svg>';
    btn.disabled = true;
    setTimeout(() => { btn.innerHTML = orig; btn.classList.remove('btn-ok'); btn.disabled = false; }, 1400);
  }

  document.getElementById('btn-copy-card').addEventListener('click', () => {
    if (!detailCurrentItem) return;
    navigator.clipboard.writeText(itemToMarkdown(detailCurrentItem, detailCurrentCat))
      .then(() => flashBtn(document.getElementById('btn-copy-card')));
  });

  document.getElementById('btn-print-card').addEventListener('click', () => {
    if (!detailCurrentItem) return;
    const name = detailCurrentItem[CAT_CONFIG[detailCurrentCat].nameKey];
    const w = window.open('', '_blank');
    w.document.write(`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>${name}</title>
<style>body{font-family:system-ui,sans-serif;max-width:640px;margin:2rem auto;padding:0 1rem;line-height:1.7;color:#1e293b}
h1{font-size:1.5rem;margin-bottom:.2rem}h2{font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#64748b;margin:1.3rem 0 .2rem}
p{margin:0 0 .6rem}.type{color:#64748b;font-style:italic}.brief{font-size:1.05rem}.meta{color:#475569}
@media print{body{margin:0;padding:1cm}}</style></head>
<body>${buildPrintHtml(detailCurrentItem, detailCurrentCat)}
<script>window.onload=()=>window.print()<\/script></body></html>`);
    w.document.close();
  });

  document.getElementById('btn-dl-card').addEventListener('click', () => {
    if (!detailCurrentItem) return;
    const md   = itemToMarkdown(detailCurrentItem, detailCurrentCat);
    const name = detailCurrentItem[CAT_CONFIG[detailCurrentCat].nameKey];
    const blob = new Blob([md], { type: 'text/markdown' });
    const a    = Object.assign(document.createElement('a'), {
      href: URL.createObjectURL(blob),
      download: name.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '') + '.md',
    });
    a.click();
    URL.revokeObjectURL(a.href);
    flashBtn(document.getElementById('btn-dl-card'));
  });

  // Touch drag for detail card
  let touchCardDrag = null;
  dragHandle.addEventListener('touchstart', e => {
    if (e.touches.length !== 1) return;
    e.preventDefault();
    e.stopPropagation();
    if (window.innerWidth <= 720) {
      touchCardDrag = { startY: e.touches[0].clientY, startH: detailCard.offsetHeight };
    } else {
      const rect  = detailCard.getBoundingClientRect();
      const panel = detailCard.parentElement.getBoundingClientRect();
      detailCard.style.bottom = 'auto'; detailCard.style.right = 'auto';
      detailCard.style.top    = (rect.top  - panel.top)  + 'px';
      detailCard.style.left   = (rect.left - panel.left) + 'px';
      touchCardDrag = { desktop: true, startX: e.touches[0].clientX, startY: e.touches[0].clientY,
                        startTop: rect.top - panel.top, startLeft: rect.left - panel.left };
    }
    dragHandle.classList.add('dragging');
  }, { passive: false });

  document.addEventListener('touchmove', e => {
    if (!touchCardDrag) return;
    e.preventDefault();
    if (touchCardDrag.desktop) {
      const panel = detailCard.parentElement.getBoundingClientRect();
      const maxL  = panel.width  - detailCard.offsetWidth;
      const maxT  = panel.height - 40;
      detailCard.style.left = Math.max(0, Math.min(maxL, touchCardDrag.startLeft + e.touches[0].clientX - touchCardDrag.startX)) + 'px';
      detailCard.style.top  = Math.max(0, Math.min(maxT, touchCardDrag.startTop  + e.touches[0].clientY - touchCardDrag.startY)) + 'px';
    } else {
      const dy   = touchCardDrag.startY - e.touches[0].clientY;
      const maxH = detailCard.parentElement.offsetHeight * 0.85;
      detailCard.style.maxHeight = Math.max(80, Math.min(maxH, touchCardDrag.startH + dy)) + 'px';
    }
  }, { passive: false });

  document.addEventListener('touchend', () => {
    if (touchCardDrag) { touchCardDrag = null; dragHandle.classList.remove('dragging'); }
  });

  dragHandle.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    const rect = detailCard.getBoundingClientRect();
    const panel = detailCard.parentElement.getBoundingClientRect();
    detailCard.style.bottom = 'auto';
    detailCard.style.right  = 'auto';
    detailCard.style.top    = (rect.top  - panel.top)  + 'px';
    detailCard.style.left   = (rect.left - panel.left) + 'px';
    cardDrag = { startX: e.clientX, startY: e.clientY,
                 startTop: rect.top - panel.top, startLeft: rect.left - panel.left };
    dragHandle.classList.add('dragging');
    e.preventDefault();
    e.stopPropagation();
  });

  document.addEventListener('mousemove', e => {
    if (!cardDrag) return;
    const panel = detailCard.parentElement.getBoundingClientRect();
    const maxL  = panel.width  - detailCard.offsetWidth;
    const maxT  = panel.height - 40;
    const newL  = Math.max(0, Math.min(maxL, cardDrag.startLeft + e.clientX - cardDrag.startX));
    const newT  = Math.max(0, Math.min(maxT, cardDrag.startTop  + e.clientY - cardDrag.startY));
    detailCard.style.left = newL + 'px';
    detailCard.style.top  = newT + 'px';
  });

  document.addEventListener('mouseup', () => {
    if (cardDrag) { cardDrag = null; dragHandle.classList.remove('dragging'); }
  });
}

/* ── Plan / coverage mode ────────────────────────────────── */

function enterPlanMode() {
  state.planMode = true;
  state.selectedName = null;
  document.querySelector('.catalog-body').classList.remove('has-detail');
  document.getElementById('btn-plan-mode').classList.add('active');
  document.getElementById('detail-content').style.display = 'none';
  renderCards();
  renderPlanCoverage();
}

function exitPlanMode() {
  state.planMode = false;
  state.planSelected = new Map();
  document.getElementById('btn-plan-mode').classList.remove('active');
  document.getElementById('plan-coverage-panel').style.display = 'none';
  document.getElementById('detail-empty').style.display = '';
  resetDetailEmpty();
  updatePlanToolbar();
  renderCards();
}

function updatePlanToolbar() {
  const i = i18n();
  const n = state.planSelected.size;
  const infoEl = document.getElementById('plan-info');
  const clearEl = document.getElementById('btn-plan-clear');
  if (infoEl) infoEl.textContent = n > 0 ? i.planItemCount(n) : '';
  if (clearEl) clearEl.style.display = n > 0 ? '' : 'none';
}

function togglePlanItem(code, name, cat) {
  if (state.planSelected.has(code)) {
    state.planSelected.delete(code);
  } else {
    const item = (state.data[cat] || []).find(i => i['Código'] === code);
    state.planSelected.set(code, { name, cat, item });
  }
  updatePlanToolbar();
  renderCards();
  renderPlanCoverage();
}

function calcDimCoverage() {
  return (state.data.dimensiones || []).map(dim => {
    const dimCode = dim['Código'];
    const covered = [...state.planSelected.values()].some(
      info => info.item?.rel_dim?.includes(dimCode)
    );
    return {
      code: dimCode,
      name: dim[CAT_CONFIG.dimensiones.nameKey],
      cat:  dim['Categoría'],
      covered,
    };
  }).sort((a, b) => b.covered - a.covered);
}

function renderPlanCoverage() {
  const i = i18n();
  const panel = document.getElementById('plan-coverage-panel');
  if (!panel) return;
  panel.style.display = '';
  document.getElementById('detail-content').style.display = 'none';
  document.getElementById('detail-empty').style.display = 'none';

  const n = state.planSelected.size;

  if (n === 0) {
    panel.innerHTML = `
      <div class="plan-empty-state">
        <div class="plan-empty-icon">🗂️</div>
        <div class="plan-empty-title">${i.planEmptyTitle}</div>
        <div class="plan-empty-desc">${i.planEmptyDesc}</div>
      </div>`;
    return;
  }

  const coverage = calcDimCoverage();
  const coveredCount = coverage.filter(d => d.covered).length;
  const total = coverage.length;
  const pct = Math.round(coveredCount / total * 100);

  // Group by category, covered first within each group
  const groups = {};
  coverage.forEach(d => {
    if (!groups[d.cat]) groups[d.cat] = [];
    groups[d.cat].push(d);
  });

  const groupsHtml = Object.entries(groups).map(([cat, dims]) => {
    const items = dims.map(d => {
      if (d.covered) {
        return `<div class="plan-dim-item covered"><span class="plan-dim-icon">✓</span><span class="plan-dim-name">${d.name}</span></div>`;
      }
      const isExp = d.code === state.planExpandedDim;
      const allCovering = (state.data.herramientas || []).filter(h => h.rel_dim?.includes(d.code));
      const suggestions = allCovering.filter(h => !state.planSelected.has(h['Código']));
      const emptyMsg = allCovering.length === 0
        ? i.planEvidenceOnlyDim
        : i.planAllSelectedForDim;
      const suggestHtml = isExp ? `
        <div class="plan-suggest-list">
          ${suggestions.length
            ? suggestions.map(h => `<button class="plan-suggest-btn" data-code="${h['Código']}" data-name="${h[CAT_CONFIG.herramientas.nameKey]}">＋ ${h[CAT_CONFIG.herramientas.nameKey]}</button>`).join('')
            : `<span class="plan-suggest-empty">${emptyMsg}</span>`}
        </div>` : '';
      return `
        <div class="plan-dim-item uncovered${isExp ? ' expanded' : ''}" data-dim="${d.code}">
          <div class="plan-dim-row-main">
            <span class="plan-dim-icon">–</span>
            <span class="plan-dim-name">${d.name}</span>
            <span class="plan-dim-add" title="${i.planShowInstrumentsTitle}">${isExp ? '▲' : '+'}</span>
          </div>
          ${suggestHtml}
        </div>`;
    }).join('');
    return `<div class="plan-group"><div class="plan-group-label">${cat}</div>${items}</div>`;
  }).join('');

  const chipsHtml = [...state.planSelected.entries()].map(([code, v]) => `
    <span class="plan-her-chip">
      ${v.name}<button class="plan-chip-remove" data-code="${code}" aria-label="${i.removeLabel}">×</button>
    </span>`).join('');

  panel.innerHTML = `
    <div class="plan-header-block">
      <div class="plan-cov-title">${i.planTitle}</div>
      <div class="plan-progress-wrap">
        <div class="plan-progress-bar"><div class="plan-progress-fill" style="width:${pct}%"></div></div>
        <span class="plan-progress-label">${i.planProgress(coveredCount, total)}</span>
      </div>
      <div class="plan-her-chips">${chipsHtml}</div>
    </div>
    <div class="plan-groups">${groupsHtml}</div>`;
}

/* ── Init ─────────────────────────────────────────────────── */
async function init() {
  CAT_CONFIG = buildCatConfig(state.lang);
  initEvents();
  renderHome();
  updateStaticI18n();
  renderGlobalFilters();
  await loadData();
}

init();
