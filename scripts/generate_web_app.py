import json, os

base_dir = r'c:\Users\abdal\Desktop\RE4E'
json_path = os.path.join(base_dir, 'data', 'ccna1_exam.json')
with open(json_path, 'r', encoding='utf-8') as f:
    exam_data = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="fr" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CCNA 1</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            darkbg: '#09090b',
            darkcard: '#18181b',
            darkborder: '#27272a'
          }
        }
      }
    }
  </script>
  <style>
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #09090b; }
    ::-webkit-scrollbar-thumb { background: #27272a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #3f3f46; }
    mark { background-color: rgba(234, 179, 8, 0.25); color: #fde047; padding: 0 2px; border-radius: 2px; }
  </style>
</head>
<body class="bg-darkbg text-zinc-100 font-sans antialiased text-xs p-2.5 min-h-screen">

  <!-- Entête ultra discret -->
  <div class="flex items-center justify-between mb-2 pb-1.5 border-b border-darkborder">
    <div class="flex items-center gap-1.5">
      <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
      <span class="font-semibold text-zinc-500 text-[10px] tracking-wider">CCNA 1</span>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="openMiniWindow()" title="Ouvrir en fenêtre mini flottante" class="text-zinc-500 hover:text-zinc-300 bg-zinc-900 px-1.5 py-0.5 rounded border border-zinc-800 hover:border-zinc-700 transition text-[9px]">
        🗗 Fenêtre
      </button>
      <span id="counter" class="text-[9px] text-zinc-600 font-mono"></span>
    </div>
  </div>

  <!-- Barre de recherche -->
  <div class="relative mb-2">
    <input 
      type="text" 
      id="search" 
      autofocus
      placeholder="Tapez les mots de la question..." 
      class="w-full bg-darkcard border border-darkborder rounded-md px-3 py-1.5 text-xs text-white placeholder-zinc-600 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition shadow-sm"
      oninput="onSearch(this.value)"
    />
    <button id="clearBtn" onclick="clearSearch()" class="hidden absolute right-2.5 top-1.5 text-zinc-500 hover:text-zinc-300 text-xs">
      ✕
    </button>
  </div>

  <!-- Liste des résultats (vide par défaut) -->
  <div id="results" class="space-y-1.5">
  </div>

  <!-- Modal Schéma -->
  <div id="imageModal" class="fixed inset-0 bg-black/80 hidden z-50 flex items-center justify-center p-3" onclick="closeModal()">
    <div class="bg-darkcard border border-darkborder p-3 rounded-lg max-w-lg w-full relative" onclick="event.stopPropagation()">
      <div class="flex justify-between items-center mb-2">
        <span id="modalTitle" class="text-xs font-semibold text-zinc-300">Schéma</span>
        <button onclick="closeModal()" class="text-zinc-400 hover:text-white text-sm">✕</button>
      </div>
      <img id="modalImg" src="" alt="Schéma" class="max-h-[70vh] mx-auto rounded border border-darkborder object-contain" />
    </div>
  </div>

  <script>
    const EXAM_DATA = __DATA_PLACEHOLDER__;

    function normalize(str) {
      if (!str) return '';
      return str.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').replace(/[^a-z0-9\\s]/g, ' ');
    }

    EXAM_DATA.forEach(item => {
      item.norm_q = normalize(item.question);
      item.norm_ans = normalize(item.correct_answers.join(' '));
      item.norm_exp = normalize(item.explanation || '');
    });

    function highlight(text, words) {
      if (!words || !words.length) return text;
      let regex = new RegExp(`(${words.filter(w => w.length > 1).join('|')})`, 'gi');
      return text.replace(regex, '<mark>$1</mark>');
    }

    function search(query) {
      const q = normalize(query.trim());
      if (!q) return [];

      const words = q.split(/\\s+/).filter(Boolean);
      if (!words.length) return [];

      const scored = [];
      for (const item of EXAM_DATA) {
        let score = 0;
        if (item.norm_q.includes(q)) score += 200;
        if (words.every(w => item.norm_q.includes(w))) score += 100;

        for (const w of words) {
          if (item.norm_q.includes(w)) score += 30;
          if (item.norm_ans.includes(w)) score += 25;
          if (item.norm_exp.includes(w)) score += 10;
        }

        if (score > 0) scored.push({ score, item });
      }

      scored.sort((a, b) => b.score - a.score);
      return scored.slice(0, 10).map(s => s.item);
    }

    function renderResults(items, queryWords = []) {
      const container = document.getElementById('results');
      const counter = document.getElementById('counter');
      const input = document.getElementById('search');

      if (!input.value.trim()) {
        container.innerHTML = '';
        counter.innerText = '';
        return;
      }

      counter.innerText = `${items.length} R`;

      if (!items.length) {
        container.innerHTML = `<div class="text-center py-6 text-zinc-600 text-xs">Aucun résultat trouvé.</div>`;
        return;
      }

      container.innerHTML = items.map(item => {
        const highlightedQ = highlight(item.question, queryWords);
        const ansList = item.correct_answers.map(ans => {
          const highlightedAns = highlight(ans, queryWords);
          return `<div class="bg-emerald-950/40 border border-emerald-800/40 text-emerald-400 px-2 py-1 rounded font-semibold text-[11px] leading-tight select-text">
            ✔ ${highlightedAns}
          </div>`;
        }).join('');

        const schemaBtn = item.has_image && item.image_file ? `
          <button onclick="showImage('${item.image_file}', 'Q${item.original_number}')" class="text-[9px] bg-sky-950/60 border border-sky-800/50 text-sky-400 hover:text-sky-200 px-1 py-0.5 rounded transition">
            🖼️ Schéma
          </button>
        ` : '';

        return `
          <div class="bg-darkcard border border-darkborder hover:border-zinc-700 p-2 rounded-md transition shadow-sm">
            <div class="flex items-center justify-between gap-2 mb-1">
              <div class="flex items-center gap-1.5">
                <span class="bg-zinc-800 text-zinc-400 font-bold px-1.5 py-0.5 rounded text-[9px]">Q${item.original_number}</span>
                ${schemaBtn}
              </div>
              <button onclick="copyAnswer(this, ${item.id})" class="text-[9px] bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-emerald-400 px-1.5 py-0.5 rounded transition">
                Copier
              </button>
            </div>
            <p class="text-zinc-300 mb-1.5 leading-snug text-[11px]">${highlightedQ}</p>
            <div class="space-y-1">${ansList}</div>
          </div>
        `;
      }).join('');
    }

    function onSearch(val) {
      const clearBtn = document.getElementById('clearBtn');
      if (val.trim()) {
        clearBtn.classList.remove('hidden');
      } else {
        clearBtn.classList.add('hidden');
      }
      const words = normalize(val).split(/\\s+/).filter(Boolean);
      renderResults(search(val), words);
    }

    function clearSearch() {
      const input = document.getElementById('search');
      input.value = '';
      input.focus();
      onSearch('');
    }

    function copyAnswer(btn, itemId) {
      const item = EXAM_DATA.find(x => x.id === itemId);
      if (item) {
        navigator.clipboard.writeText(item.correct_answers.join('\\n'));
        const originalText = btn.innerText;
        btn.innerText = 'Copié !';
        btn.classList.add('text-emerald-400');
        setTimeout(() => {
          btn.innerText = originalText;
          btn.classList.remove('text-emerald-400');
        }, 1000);
      }
    }

    function showImage(path, title) {
      document.getElementById('modalTitle').innerText = `Schéma ${title}`;
      document.getElementById('modalImg').src = path;
      document.getElementById('imageModal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('imageModal').classList.add('hidden');
    }

    function openMiniWindow() {
      window.open(window.location.href, 'CCNAMini', 'width=430,height=440,menubar=no,toolbar=no,location=no,status=no');
    }

    // Auto-sélection automatique de tout le texte dès qu'on revient sur la page / input
    const searchInput = document.getElementById('search');
    
    window.addEventListener('focus', () => {
      searchInput.focus();
      searchInput.select();
    });

    searchInput.addEventListener('focus', () => {
      setTimeout(() => searchInput.select(), 10);
    });

    searchInput.addEventListener('mouseup', (e) => {
      // Empêche de désélectionner lors d'un clic de focus
      if (document.activeElement === searchInput && searchInput.selectionStart !== searchInput.selectionEnd) {
        return;
      }
    });

    // Raccourcis clavier
    window.addEventListener('keydown', (e) => {
      if (e.ctrlKey && (e.key === 'f' || e.key === 'F')) {
        e.preventDefault();
        window.close();
      }
      if (e.key === 'Escape') clearSearch();
      if (e.key === '/' && document.activeElement !== searchInput) {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
    });

    // Au démarrage : affichage minimum de base (vide)
    renderResults([]);
  </script>
</body>
</html>
"""

final_html = html_template.replace('__DATA_PLACEHOLDER__', json.dumps(exam_data, ensure_ascii=False))
out_path = os.path.join(base_dir, 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print('Updated standalone web app at:', out_path)
