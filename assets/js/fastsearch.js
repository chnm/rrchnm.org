/*
  Fast Search — adapted from Craig Mod's gist
  https://gist.github.com/cmod/5410eae147e4318164258742dd053993
  Customized for RRCHNM: Cmd-K / Ctrl-K shortcut, styled modal
*/

const CONFIG = {
  shortcuts: {
    open: { key: 'k', metaKey: true, altKey: false, ctrlKey: false, shiftKey: false }
  },
  search: {
    minChars: 2,
    maxResults: 10,
    fields: { title: true, description: true, section: true }
  }
};

(function () {
  const fastSearch = document.getElementById('fastSearch');
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');
  if (!fastSearch || !searchInput || !searchResults) return;

  let searchIndex = null;
  let searchVisible = false;
  let resultsAvailable = false;

  // Load index eagerly on page load
  loadSearchIndex();

  async function loadSearchIndex() {
    try {
      const response = await fetch('/index.json');
      if (!response.ok) throw new Error('Failed to load search index');
      const data = await response.json();
      searchIndex = data.map(item => ({
        ...item,
        searchableTitle: item.title?.toLowerCase() || '',
        searchableDesc: item.desc?.toLowerCase() || '',
        searchableSection: item.section?.toLowerCase() || ''
      }));
      if (searchInput.value) performSearch(searchInput.value);
    } catch (error) {
      console.error('Error loading search index:', error);
      searchResults.innerHTML = '<li class="search-message">Error loading search index.</li>';
    }
  }

  function simpleFuzzyMatch(text, term) {
    if (text.includes(term)) return true;
    if (term.length < 3) return false;
    let matches = 0;
    let lastMatchIndex = -1;
    for (let i = 0; i < term.length; i++) {
      const found = text.indexOf(term[i], lastMatchIndex + 1);
      if (found > -1) { matches++; lastMatchIndex = found; }
    }
    return matches === term.length;
  }

  function matchesShortcut(event, sc) {
    // Support both Cmd-K (Mac) and Ctrl-K (Win/Linux)
    return event.key === sc.key && (event.metaKey || event.ctrlKey) && !event.altKey && !event.shiftKey;
  }

  var searchOpener = null;

  function openSearch() {
    searchVisible = true;
    searchOpener = document.activeElement;
    fastSearch.style.visibility = 'visible';
    fastSearch.removeAttribute('aria-hidden');
    searchInput.focus();
    searchInput.value = '';
    searchResults.innerHTML = '';
  }

  function closeSearch() {
    searchVisible = false;
    fastSearch.style.visibility = 'hidden';
    fastSearch.setAttribute('aria-hidden', 'true');
    searchInput.value = '';
    searchResults.innerHTML = '';
    if (searchOpener && searchOpener.focus) searchOpener.focus();
    searchOpener = null;
  }

  // Close on backdrop click
  fastSearch.addEventListener('click', function (e) {
    if (e.target === fastSearch) closeSearch();
  });

  document.addEventListener('keydown', function (event) {
    if (matchesShortcut(event, CONFIG.shortcuts.open)) {
      event.preventDefault();
      searchVisible ? closeSearch() : openSearch();
    }

    if (event.key === 'Escape' && searchVisible) {
      closeSearch();
    }

    if (event.key === 'Enter' && searchVisible) {
      const firstResult = searchResults.querySelector('a');
      if (firstResult) { event.preventDefault(); window.location.href = firstResult.href; }
    }

    if (searchVisible && resultsAvailable) {
      const links = Array.from(searchResults.getElementsByTagName('a'));
      if (!links.length) return;
      const active = document.activeElement;

      if (event.key === 'ArrowDown') {
        event.preventDefault();
        if (active === searchInput) { links[0].focus(); }
        else if (active.tagName === 'A') {
          const i = links.indexOf(active);
          if (i < links.length - 1) links[i + 1].focus();
        }
      }

      if (event.key === 'ArrowUp') {
        event.preventDefault();
        if (active === links[0]) { searchInput.focus(); }
        else if (active.tagName === 'A') {
          const i = links.indexOf(active);
          if (i > 0) links[i - 1].focus();
        }
      }
    }
  });

  function performSearch(term) {
    term = term.toLowerCase().trim();
    if (!term || !searchIndex) { searchResults.innerHTML = ''; resultsAvailable = false; return; }
    if (term.length < CONFIG.search.minChars) {
      searchResults.innerHTML = '<li class="search-message">Keep typing...</li>';
      resultsAvailable = false;
      return;
    }

    const searchTerms = term.split(/\s+/).filter(t => t.length > 0);

    const results = searchIndex
      .map(item => {
        let score = 0;
        const matchesAllTerms = searchTerms.every(t => {
          let matched = false;
          if (CONFIG.search.fields.title) {
            if (item.searchableTitle.startsWith(t)) { score += 5; matched = true; }
            else if (item.searchableTitle.includes(t)) { score += 4; matched = true; }
            else if (simpleFuzzyMatch(item.searchableTitle, t)) { score += 1; matched = true; }
          }
          if (!matched) {
            if (CONFIG.search.fields.description && item.searchableDesc.includes(t)) { score += 0.5; matched = true; }
            if (CONFIG.search.fields.section && item.searchableSection.includes(t)) { score += 0.5; matched = true; }
          }
          return matched;
        });
        return { item, score: matchesAllTerms ? score : 0 };
      })
      .filter(r => r.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, CONFIG.search.maxResults)
      .map(r => r.item);

    resultsAvailable = results.length > 0;

    if (!resultsAvailable) {
      searchResults.innerHTML = '<li class="search-message">No results found.</li>';
      return;
    }

    searchResults.innerHTML = results.map(item => {
      var section = item.section ? item.section.charAt(0).toUpperCase() + item.section.slice(1) : '';
      var metaParts = [];
      if (section) metaParts.push(escapeHtml(section));
      if (item.date) metaParts.push(escapeHtml(item.date));
      return '<li><a href="' + escapeHtml(item.permalink) + '" tabindex="0">' +
        '<span class="search-title">' + escapeHtml(item.title) + '</span>' +
        '<span class="search-meta">' + metaParts.join(' &middot; ') + '</span>' +
        '</a></li>';
    }).join('');
  }

  searchInput.addEventListener('input', function () {
    if (!searchIndex) {
      searchResults.innerHTML = '<li class="search-message">Loading search index...</li>';
      return;
    }
    performSearch(this.value);
  });

  function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
})();
