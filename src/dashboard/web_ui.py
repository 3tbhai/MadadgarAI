"""Clean, Simplified Neo-Brutalist Web UI for MadadgaarAI v3.0 — Real-Time Opportunities."""


def render_dashboard_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>MadadgaarAI — Live Internships, Scholarships &amp; Research Grants</title>
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@600;700&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0" rel="stylesheet"/>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            ink: "#18181b",
            cream: "#f7f3eb",
            sand: "#ede7db",
            accent: "#ffcc00",
            vermilion: "#e63b2e",
            cobalt: "#0055ff",
            forest: "#138808",
          },
          fontFamily: {
            display: ["Space Grotesk", "Inter", "sans-serif"],
            sans: ["Inter", "system-ui", "sans-serif"],
            mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Consolas", "monospace"],
            devanagari: ["Noto Sans Devanagari", "sans-serif"],
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #f7f3eb; color: #18181b; }
    .nb-card {
      background: #ffffff;
      border: 2px solid #18181b;
      box-shadow: 3px 3px 0px #18181b;
      transition: transform 0.14s ease, box-shadow 0.14s ease;
    }
    .nb-card:hover {
      transform: translate(-1px, -1px);
      box-shadow: 5px 5px 0px #18181b;
    }
    .nb-btn {
      border: 2px solid #18181b;
      box-shadow: 2px 2px 0px #18181b;
      transition: transform 0.1s ease, box-shadow 0.1s ease, background-color 0.12s ease;
    }
    .nb-btn:active {
      transform: translate(1px, 1px);
      box-shadow: 1px 1px 0px #18181b;
    }
    .skeleton-pulse {
      background: linear-gradient(90deg, #ece6da 25%, #f5f1e8 50%, #ece6da 75%);
      background-size: 200% 100%;
      animation: shimmer 1.2s infinite linear;
    }
    @keyframes shimmer {
      0% { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }
  </style>
</head>
<body class="font-sans antialiased min-h-screen flex flex-col selection:bg-accent selection:text-ink">

<!-- ================= TOASTS ================= -->
<div id="toastContainer" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2.5 max-w-sm w-full pointer-events-none px-4 sm:px-0"></div>

<!-- ================= CLEAN STICKY HEADER ================= -->
<header class="sticky top-0 z-40 bg-cream/95 backdrop-blur border-b-2 border-ink">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between gap-3">
    <!-- Brand -->
    <button onclick="switchWorkspace('opportunities')" class="flex items-center gap-2.5 text-left">
      <div class="w-8 h-8 bg-ink text-accent border-2 border-ink flex items-center justify-center font-display font-bold text-lg shadow-[2px_2px_0px_#ffcc00]">M</div>
      <div class="leading-none">
        <span class="font-display font-bold text-base tracking-tight block">MadadgaarAI</span>
        <span class="font-devanagari text-[10px] text-neutral-600 hidden sm:block mt-0.5">मददगार एआई</span>
      </div>
    </button>

    <!-- Primary 3-Tab Navigation -->
    <nav class="flex items-center gap-1.5">
      <button id="navOpportunities" onclick="switchWorkspace('opportunities')" class="px-3 py-1.5 text-xs font-semibold border-2 border-ink bg-accent text-ink shadow-[2px_2px_0px_#18181b]">
        Opportunities
      </button>
      <button id="navTracker" onclick="switchWorkspace('tracker')" class="px-3 py-1.5 text-xs font-semibold border-2 border-transparent text-neutral-600 hover:border-ink hover:text-ink inline-flex items-center gap-1.5">
        <span>My Tracker</span>
        <span id="navTrackerCount" class="px-1.5 py-0.2 bg-ink text-accent font-mono text-[10px] font-bold">0</span>
      </button>
      <button id="navAssistant" onclick="switchWorkspace('assistant')" class="px-3 py-1.5 text-xs font-semibold border-2 border-transparent text-neutral-600 hover:border-ink hover:text-ink">
        Saral AI &amp; Docs
      </button>
    </nav>

    <!-- Refresh Live Button -->
    <button id="refreshLiveBtn" onclick="triggerLiveRefresh()" class="nb-btn px-3 py-1.5 bg-ink text-accent hover:bg-accent hover:text-ink text-xs font-semibold inline-flex items-center gap-1.5 disabled:opacity-60" title="Crawl live Government & Company portals now">
      <span id="refreshIcon" class="material-symbols-outlined text-[16px]">sync</span>
      <span id="refreshBtnLabel" class="hidden sm:inline">Refresh Live Data</span>
    </button>
  </div>
</header>

<!-- ================= MAIN CONTAINER ================= -->
<main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 space-y-6">

  <!-- ======================================================== -->
  <!-- VIEW 1: SIMPLIFIED LIVE OPPORTUNITIES HUB                -->
  <!-- ======================================================== -->
  <div id="workspaceOpportunities" class="space-y-5">

    <!-- Compact Top Title + Quick Source Pills -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
      <div>
        <h1 class="font-display font-bold text-2xl sm:text-3xl tracking-tight text-ink">
          Live Verified Opportunities
        </h1>
        <p class="text-xs sm:text-sm text-neutral-600 mt-1">
          Real-time internships, scholarships &amp; grants from Government portals and top companies. Every link is HTTP-verified.
        </p>
      </div>

      <!-- Clickable Source Filter Pills -->
      <div class="flex flex-wrap items-center gap-2 text-xs">
        <button data-stype="All" onclick="setSourceType('All')" class="stype-pill px-3 py-1.5 border-2 border-ink bg-ink text-accent font-semibold">
          All <span id="statAll" class="font-mono ml-1 opacity-85">--</span>
        </button>
        <button data-stype="Government" onclick="setSourceType('Government')" class="stype-pill px-3 py-1.5 border-2 border-ink bg-white hover:bg-sand font-semibold">
          Govt Portals <span id="statGovt" class="font-mono ml-1 text-cobalt">--</span>
        </button>
        <button data-stype="Company / Corporate" onclick="setSourceType('Company / Corporate')" class="stype-pill px-3 py-1.5 border-2 border-ink bg-white hover:bg-sand font-semibold">
          Companies <span id="statCompany" class="font-mono ml-1 text-vermilion">--</span>
        </button>
        <button data-stype="Foundation / University" onclick="setSourceType('Foundation / University')" class="stype-pill px-3 py-1.5 border-2 border-ink bg-white hover:bg-sand font-semibold">
          Universities <span id="statFound" class="font-mono ml-1 text-forest">--</span>
        </button>
      </div>
    </div>

    <!-- Actionable Error Banner (only if a live source fails) -->
    <div id="sourceErrorBanner" class="hidden p-3.5 bg-red-50 border-2 border-vermilion text-vermilion text-xs flex items-start gap-2">
      <span class="material-symbols-outlined text-[18px] shrink-0">warning</span>
      <div>
        <strong>Some live sources could not be reached (no mock fallback shown):</strong>
        <span id="sourceErrorList" class="font-mono block mt-0.5 text-[11px]"></span>
      </div>
    </div>

    <!-- Clean Single-Bar Search + Category + Collapsible More Filters -->
    <div class="bg-white border-2 border-ink shadow-[3px_3px_0px_#18181b] p-3.5 space-y-3">
      <div class="flex flex-col lg:flex-row gap-3">
        <!-- Search -->
        <div class="relative flex-1">
          <span class="material-symbols-outlined absolute left-3 top-2.5 text-neutral-400 text-[18px]">search</span>
          <input id="filterSearch" type="text" oninput="debouncedFetch()" placeholder="Search by role, agency, company, or skill (e.g. Stripe, ANRF, UGC, AI, Python)..." class="w-full bg-cream/70 border-2 border-ink pl-9 pr-8 py-2 text-sm focus:outline-none focus:bg-white"/>
          <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-2.5 top-2 text-neutral-500 hover:text-ink">
            <span class="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>

        <!-- Category Segmented Control -->
        <div class="flex flex-wrap items-center gap-1.5">
          <button data-cat="All" onclick="setCategory('All')" class="cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-accent text-ink">All</button>
          <button data-cat="Internship" onclick="setCategory('Internship')" class="cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-white hover:bg-sand">Internships</button>
          <button data-cat="Scholarship" onclick="setCategory('Scholarship')" class="cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-white hover:bg-sand">Scholarships</button>
          <button data-cat="Funding" onclick="setCategory('Funding')" class="cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-white hover:bg-sand">Grants</button>

          <button id="toggleFiltersBtn" onclick="toggleAdvancedFilters()" class="px-3 py-2 text-xs font-semibold border-2 border-ink bg-sand hover:bg-accent inline-flex items-center gap-1">
            <span class="material-symbols-outlined text-[16px]">tune</span>
            <span>Filters</span>
            <span id="activeFilterCount" class="hidden px-1.5 bg-ink text-accent font-mono text-[10px]">0</span>
          </button>
        </div>
      </div>

      <!-- Collapsible Advanced Filters Row -->
      <div id="advancedFiltersRow" class="hidden pt-3 border-t border-neutral-200 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <div>
          <label for="filterDomain" class="block text-[11px] font-semibold text-neutral-500 mb-1">Domain</label>
          <select id="filterDomain" onchange="onFilterChange()" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5 text-xs font-medium">
            <option value="All">All Domains</option>
          </select>
        </div>
        <div>
          <label for="filterDegree" class="block text-[11px] font-semibold text-neutral-500 mb-1">Degree / Level</label>
          <select id="filterDegree" onchange="onFilterChange()" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5 text-xs font-medium">
            <option value="All">All Levels</option>
            <option value="Undergraduate">Undergraduate</option>
            <option value="Postgraduate">Postgraduate</option>
            <option value="PhD / Faculty">PhD / Faculty</option>
          </select>
        </div>
        <div>
          <label for="filterFundingType" class="block text-[11px] font-semibold text-neutral-500 mb-1">Funding Type</label>
          <select id="filterFundingType" onchange="onFilterChange()" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5 text-xs font-medium">
            <option value="All">All Types</option>
          </select>
        </div>
        <div>
          <label for="filterDeadline" class="block text-[11px] font-semibold text-neutral-500 mb-1">Deadline</label>
          <select id="filterDeadline" onchange="onFilterChange()" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5 text-xs font-medium">
            <option value="all">Any Active</option>
            <option value="urgent_14d">Urgent (≤ 14 days)</option>
            <option value="30d">Next 30 days</option>
            <option value="rolling">Rolling / Open</option>
          </select>
        </div>
        <div>
          <label for="filterSort" class="block text-[11px] font-semibold text-neutral-500 mb-1">Sort By</label>
          <select id="filterSort" onchange="onFilterChange()" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5 text-xs font-medium">
            <option value="deadline_asc">Deadline: Soonest</option>
            <option value="recent_desc">Recently Scraped</option>
            <option value="title_asc">Title: A → Z</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Subtle Status Strip -->
    <div class="flex flex-wrap items-center justify-between gap-2 text-xs text-neutral-600 px-0.5">
      <div id="resultsSummaryText" class="font-medium">Loading live opportunities...</div>
      <div class="flex items-center gap-4">
        <span id="cacheStatusLabel" class="font-mono text-[11px] text-neutral-500"></span>
        <button id="resetFiltersLink" onclick="resetAllFilters()" class="hidden text-vermilion hover:underline font-semibold">Clear filters</button>
        <a href="/api/calendar/upcoming.ics" download class="text-cobalt hover:underline font-semibold inline-flex items-center gap-1">
          <span class="material-symbols-outlined text-[15px]">calendar_month</span> Export .ics
        </a>
      </div>
    </div>

    <!-- Clean Opportunity Cards Grid -->
    <div id="opportunitiesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"></div>

    <!-- Pagination / Load More -->
    <div id="loadMoreWrapper" class="hidden pt-2 text-center">
      <button id="loadMoreBtn" onclick="loadMoreCards()" class="nb-btn px-6 py-2.5 bg-white hover:bg-accent text-ink text-xs font-bold">
        Show More Opportunities
      </button>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- VIEW 2: PERSONAL APPLICATION KANBAN TRACKER              -->
  <!-- ======================================================== -->
  <div id="workspaceTracker" class="hidden space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
      <div>
        <h2 class="font-display font-bold text-2xl tracking-tight text-ink">Personal Application Kanban Tracker</h2>
        <p class="text-xs sm:text-sm text-neutral-600 mt-0.5">
          Bookmark live opportunities, track your progress from Saved to Applied, and export your personal deadlines.
        </p>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="exportSavedKanbanIcs()" class="nb-btn px-3.5 py-2 bg-accent text-ink hover:bg-ink hover:text-accent text-xs font-bold inline-flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[16px]">calendar_month</span>
          <span>Export My Saved Deadlines (.ics)</span>
        </button>
      </div>
    </div>

    <div id="kanbanBoardGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-start"></div>
  </div>

  <!-- ======================================================== -->
  <!-- VIEW 3: SARAL SAMJHAUTI AI & DOCUMENT CHECKER            -->
  <!-- ======================================================== -->
  <div id="workspaceAssistant" class="hidden grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    <!-- Chat -->
    <div class="lg:col-span-7 nb-card flex flex-col h-[600px]">
      <div class="px-4 py-3 border-b-2 border-ink bg-accent flex items-center justify-between gap-2">
        <div>
          <h2 class="font-display font-bold text-base">Saral Samjhauti AI</h2>
          <p class="text-[11px] text-neutral-800">Ask in English or Hinglish about certificates, DBT seeding, or live schemes.</p>
        </div>
        <select id="ragLang" class="bg-white border-2 border-ink px-2 py-1 text-xs font-semibold">
          <option value="auto">Auto Lang</option>
          <option value="en">English</option>
          <option value="hinglish">Hinglish</option>
        </select>
      </div>

      <div class="px-4 py-2 bg-sand/70 border-b border-neutral-300 flex flex-wrap gap-1.5 text-[11px]">
        <button onclick="quickAsk('Aadhaar-NPCI DBT bank seeding kaise karwayein?')" class="px-2.5 py-1 bg-white border border-ink hover:bg-accent font-medium">NPCI-DBT Seeding</button>
        <button onclick="quickAsk('What are Income and OBC-NCL certificate validity rules?')" class="px-2.5 py-1 bg-white border border-ink hover:bg-accent font-medium">Certificate Validity</button>
        <button onclick="quickAsk('What are GFR 2017 and JRF/SRF research grant stipend norms?')" class="px-2.5 py-1 bg-white border border-ink hover:bg-accent font-medium">GFR 2017 &amp; JRF Rules</button>
      </div>

      <div id="ragMessages" class="flex-1 p-4 overflow-y-auto space-y-3 text-sm bg-cream/50">
        <div class="p-3.5 bg-white border-2 border-ink text-xs sm:text-sm text-neutral-700 leading-relaxed">
          Namaste! Ask me anything in <strong>English</strong> or <strong>Hinglish</strong> about live ANRF/UGC/ICMR/BIRAC grants, company internships, Aadhaar-NPCI DBT seeding, or certificate rules.
        </div>
      </div>

      <form onsubmit="event.preventDefault(); sendRagQuery();" class="p-3 border-t-2 border-ink bg-white flex gap-2">
        <input id="ragInput" type="text" placeholder="Type your question in English or Hinglish..." class="flex-1 bg-cream/60 border-2 border-ink px-3 py-2 text-sm focus:outline-none focus:bg-white"/>
        <button type="submit" class="nb-btn px-4 py-2 bg-ink text-accent text-xs font-bold hover:bg-accent hover:text-ink">Send</button>
      </form>
    </div>

    <!-- Document Checker -->
    <div class="lg:col-span-5 nb-card p-5 space-y-4">
      <div>
        <h2 class="font-display font-bold text-base">Document Readiness Checker</h2>
        <p class="text-xs text-neutral-600 mt-0.5">Upload a PDF/Image or paste text from an Income Certificate, Marksheet, or CV to spot missing fields.</p>
      </div>

      <div class="flex items-center gap-2 p-2 bg-cream/70 border-2 border-ink">
        <input type="file" id="docFile" accept=".pdf,.png,.jpg,.jpeg,.txt" class="flex-1 text-xs"/>
        <button type="button" onclick="uploadAndAnalyzeDoc()" class="nb-btn px-3 py-1 bg-ink text-white text-xs font-semibold">Scan</button>
      </div>

      <textarea id="docText" rows="5" placeholder="Or paste certificate, marksheet, or CV text here..." class="w-full bg-cream/60 border-2 border-ink p-3 text-xs font-mono focus:outline-none focus:bg-white"></textarea>

      <button type="button" onclick="analyzeDocText()" class="nb-btn w-full py-2.5 bg-accent text-ink text-xs font-bold hover:bg-ink hover:text-accent">
        Check Completeness
      </button>

      <div id="docOutput" class="space-y-2 text-xs"></div>
    </div>
  </div>

</main>

<!-- ================= DETAIL MODAL ================= -->
<div id="detailModal" class="hidden fixed inset-0 z-50 bg-ink/60 backdrop-blur-xs flex items-center justify-center p-4" onclick="if(event.target===this) closeDetailModal()">
  <div class="bg-white border-2 border-ink shadow-[6px_6px_0px_#18181b] max-w-2xl w-full max-h-[88vh] flex flex-col overflow-hidden">
    <div class="p-4 border-b-2 border-ink bg-cream flex items-start justify-between gap-3">
      <div>
        <div id="dmBadges" class="flex flex-wrap gap-1.5 mb-1.5"></div>
        <h3 id="dmTitle" class="font-display font-bold text-lg leading-snug"></h3>
        <div id="dmOrg" class="text-xs font-semibold text-cobalt mt-0.5"></div>
      </div>
      <button onclick="closeDetailModal()" class="p-1 border-2 border-ink bg-white hover:bg-accent">
        <span class="material-symbols-outlined text-[18px] block">close</span>
      </button>
    </div>
    <div id="dmBody" class="p-5 overflow-y-auto space-y-4 text-sm text-neutral-700"></div>
    <div class="p-4 border-t-2 border-ink bg-cream flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <button id="dmSaveBtn" onclick="toggleSaveCurrentModalOpp()" class="nb-btn px-3 py-2 bg-white hover:bg-accent text-xs font-bold inline-flex items-center gap-1">
          <span class="material-symbols-outlined text-[16px]">bookmark_add</span>
          <span id="dmSaveLabel">Save to Tracker</span>
        </button>
        <a id="dmCal" href="#" download class="nb-btn px-3 py-2 bg-white hover:bg-sand text-xs font-semibold inline-flex items-center gap-1">
          <span class="material-symbols-outlined text-[16px]">calendar_month</span> .ics
        </a>
      </div>
      <a id="dmApply" href="#" target="_blank" rel="noopener noreferrer" class="nb-btn px-5 py-2 bg-ink text-accent hover:bg-accent hover:text-ink text-xs font-bold inline-flex items-center gap-1.5">
        <span>Apply / View Official Source</span>
        <span class="material-symbols-outlined text-[15px]">open_in_new</span>
      </a>
    </div>
  </div>
</div>

<!-- ================= FOOTER ================= -->
<footer class="border-t-2 border-ink bg-sand/60 py-4 text-xs text-neutral-600">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-2">
    <div><strong class="text-ink">MadadgaarAI</strong> — Live Government, Company &amp; Research Opportunities</div>
    <div class="flex items-center gap-3 font-mono text-[11px]">
      <a href="/docs" target="_blank" class="hover:underline text-ink">API Docs</a>
      <span>·</span>
      <a href="/api/health" target="_blank" class="hover:underline text-ink">Health</a>
    </div>
  </div>
</footer>

<script>
  let selectedCategory = 'All';
  let selectedSourceType = 'All';
  let allFetchedItems = [];
  let visibleCount = 18;
  let searchDebounce = null;
  let facetsInitialized = false;
  let lastTotalInStore = 0;
  let currentModalIdx = null;
  let currentModalOpp = null;
  let kanbanItems = [];
  const KANBAN_STAGES = ['Saved', 'Preparing Docs', 'Applied', 'Result'];
  let activeSessionId = localStorage.getItem('madadgaar_session_id') || '';
  if (!activeSessionId) {
    activeSessionId = 'sess-' + Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
    localStorage.setItem('madadgaar_session_id', activeSessionId);
  }

  function escapeHtml(str) {
    return String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const styles = {
      success: 'bg-forest text-white',
      error: 'bg-vermilion text-white',
      warning: 'bg-accent text-ink',
      info: 'bg-ink text-accent'
    };
    const toast = document.createElement('div');
    toast.className = `pointer-events-auto px-3.5 py-2.5 border-2 border-ink shadow-[3px_3px_0px_#18181b] text-xs font-semibold flex items-center justify-between gap-3 ${styles[type] || styles.info}`;
    toast.innerHTML = `<span>${escapeHtml(message)}</span><button onclick="this.parentElement.remove()" class="font-bold opacity-80 hover:opacity-100">✕</button>`;
    container.appendChild(toast);
    setTimeout(() => { if (toast.parentElement) toast.remove(); }, 4500);
  }

  function switchWorkspace(ws) {
    document.getElementById('workspaceOpportunities').classList.toggle('hidden', ws !== 'opportunities');
    document.getElementById('workspaceTracker').classList.toggle('hidden', ws !== 'tracker');
    document.getElementById('workspaceAssistant').classList.toggle('hidden', ws !== 'assistant');
    const act = 'px-3 py-1.5 text-xs font-semibold border-2 border-ink bg-accent text-ink shadow-[2px_2px_0px_#18181b] inline-flex items-center gap-1.5';
    const inact = 'px-3 py-1.5 text-xs font-semibold border-2 border-transparent text-neutral-600 hover:border-ink hover:text-ink inline-flex items-center gap-1.5';
    document.getElementById('navOpportunities').className = ws === 'opportunities' ? act : inact;
    document.getElementById('navTracker').className = ws === 'tracker' ? act : inact;
    document.getElementById('navAssistant').className = ws === 'assistant' ? act : inact;
    if (ws === 'tracker') {
      renderKanbanBoard();
    }
  }

  function toggleAdvancedFilters() {
    document.getElementById('advancedFiltersRow').classList.toggle('hidden');
  }

  function setSourceType(st) {
    selectedSourceType = st;
    document.querySelectorAll('.stype-pill').forEach(btn => {
      const active = btn.getAttribute('data-stype') === st;
      btn.className = active
        ? 'stype-pill px-3 py-1.5 border-2 border-ink bg-ink text-accent font-semibold'
        : 'stype-pill px-3 py-1.5 border-2 border-ink bg-white hover:bg-sand font-semibold';
    });
    fetchOpportunities();
  }

  function setCategory(cat) {
    selectedCategory = cat;
    document.querySelectorAll('.cat-pill').forEach(btn => {
      const active = btn.getAttribute('data-cat') === cat;
      btn.className = active
        ? 'cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-accent text-ink'
        : 'cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-white hover:bg-sand';
    });
    fetchOpportunities();
  }

  function onFilterChange() {
    updateFilterBadgeCount();
    fetchOpportunities();
  }

  function updateFilterBadgeCount() {
    let count = 0;
    if (document.getElementById('filterDomain').value !== 'All') count++;
    if (document.getElementById('filterDegree').value !== 'All') count++;
    if (document.getElementById('filterFundingType').value !== 'All') count++;
    if (document.getElementById('filterDeadline').value !== 'all') count++;
    const badge = document.getElementById('activeFilterCount');
    badge.innerText = count;
    badge.classList.toggle('hidden', count === 0);

    const anyActive = count > 0 || selectedCategory !== 'All' || selectedSourceType !== 'All' || document.getElementById('filterSearch').value.trim().length > 0;
    document.getElementById('resetFiltersLink').classList.toggle('hidden', !anyActive);
  }

  function debouncedFetch() {
    const val = document.getElementById('filterSearch').value.trim();
    document.getElementById('clearSearchBtn').classList.toggle('hidden', !val);
    updateFilterBadgeCount();
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(fetchOpportunities, 220);
  }

  function clearSearch() {
    document.getElementById('filterSearch').value = '';
    document.getElementById('clearSearchBtn').classList.add('hidden');
    onFilterChange();
  }

  function resetAllFilters() {
    selectedCategory = 'All';
    selectedSourceType = 'All';
    document.getElementById('filterSearch').value = '';
    document.getElementById('clearSearchBtn').classList.add('hidden');
    document.getElementById('filterDomain').value = 'All';
    document.getElementById('filterDegree').value = 'All';
    document.getElementById('filterFundingType').value = 'All';
    document.getElementById('filterDeadline').value = 'all';
    document.getElementById('filterSort').value = 'deadline_asc';
    setSourceType('All');
    setCategory('All');
    updateFilterBadgeCount();
  }

  function renderSkeletons(count = 6) {
    document.getElementById('loadMoreWrapper').classList.add('hidden');
    document.getElementById('opportunitiesGrid').innerHTML = Array.from({ length: count }).map(() => `
      <div class="nb-card p-5 space-y-3">
        <div class="flex justify-between"><div class="h-4 w-20 skeleton-pulse"></div><div class="h-4 w-16 skeleton-pulse"></div></div>
        <div class="h-5 w-5/6 skeleton-pulse"></div>
        <div class="h-4 w-1/2 skeleton-pulse"></div>
        <div class="h-10 w-full skeleton-pulse"></div>
        <div class="h-9 w-full skeleton-pulse"></div>
      </div>
    `).join('');
  }

  function formatRelativeTime(iso) {
    if (!iso) return 'just now';
    const mins = Math.max(0, Math.floor((Date.now() - new Date(iso).getTime()) / 60000));
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.floor(mins / 60);
    return hrs < 24 ? `${hrs}h ago` : `${Math.floor(hrs / 24)}d ago`;
  }

  function deadlinePill(deadlineIso, isRolling) {
    if (!deadlineIso) {
      return `<span class="text-[11px] font-mono text-cobalt font-semibold">${isRolling ? 'Rolling' : 'Open'}</span>`;
    }
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const days = Math.ceil((new Date(deadlineIso + 'T00:00:00') - today) / 86400000);
    if (days <= 14) {
      return `<span class="px-2 py-0.5 bg-vermilion text-white text-[10px] font-mono font-bold">${days}d left</span>`;
    }
    return `<span class="text-[11px] font-mono text-neutral-600 font-medium">${deadlineIso}</span>`;
  }

  function populateFacets(facets) {
    if (!facets || facetsInitialized) return;
    const domSel = document.getElementById('filterDomain');
    (facets.domains || []).forEach(d => {
      const o = document.createElement('option'); o.value = d; o.textContent = d; domSel.appendChild(o);
    });
    const ftSel = document.getElementById('filterFundingType');
    (facets.funding_types || []).forEach(f => {
      const o = document.createElement('option'); o.value = f; o.textContent = f; ftSel.appendChild(o);
    });
    facetsInitialized = true;
  }

  async function updateStatsCounters() {
    try {
      const res = await fetch('/api/stats');
      if (!res.ok) return;
      const s = await res.json();
      const sb = s.source_type_breakdown || {};
      document.getElementById('statAll').innerText = s.total_opportunities || 0;
      document.getElementById('statGovt').innerText = sb['Government'] || 0;
      document.getElementById('statCompany').innerText = sb['Company / Corporate'] || 0;
      document.getElementById('statFound').innerText = sb['Foundation / University'] || 0;
    } catch (e) {}
  }

  async function fetchOpportunities() {
    renderSkeletons(6);
    updateFilterBadgeCount();
    const params = new URLSearchParams();
    if (selectedCategory !== 'All') params.set('category', selectedCategory);
    if (selectedSourceType !== 'All') params.set('source_type', selectedSourceType);
    const dom = document.getElementById('filterDomain').value;
    if (dom !== 'All') params.set('domain', dom);
    const deg = document.getElementById('filterDegree').value;
    if (deg !== 'All') params.set('degree_level', deg);
    const ft = document.getElementById('filterFundingType').value;
    if (ft !== 'All') params.set('funding_type', ft);
    const dl = document.getElementById('filterDeadline').value;
    if (dl !== 'all') params.set('deadline_window', dl);
    const q = document.getElementById('filterSearch').value.trim();
    if (q) params.set('q', q);
    params.set('sort', document.getElementById('filterSort').value);

    try {
      const res = await fetch(`/api/opportunities?${params.toString()}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      populateFacets(data.facets);
      allFetchedItems = data.items || [];
      lastTotalInStore = data.total_in_store || 0;
      visibleCount = 18;

      document.getElementById('resultsSummaryText').innerHTML =
        `Showing <strong class="text-ink">${allFetchedItems.length}</strong> of ${data.total_in_store} live verified opportunities`;
      document.getElementById('cacheStatusLabel').innerText = data.last_refreshed_at
        ? `Synced ${formatRelativeTime(data.last_refreshed_at)}`
        : '';

      const errBanner = document.getElementById('sourceErrorBanner');
      if (data.source_errors && data.source_errors.length > 0) {
        errBanner.classList.remove('hidden');
        document.getElementById('sourceErrorList').innerText = data.source_errors.join(' | ');
      } else {
        errBanner.classList.add('hidden');
      }

      renderVisibleCards(data.total_in_store);
    } catch (err) {
      document.getElementById('opportunitiesGrid').innerHTML = `
        <div class="col-span-full nb-card p-10 text-center space-y-3">
          <span class="material-symbols-outlined text-4xl text-vermilion">cloud_off</span>
          <h3 class="font-display font-bold text-lg">Unable to Load Live Opportunities</h3>
          <p class="text-xs text-neutral-600">Backend query failed (${escapeHtml(err.message)}). No mock data shown.</p>
          <button onclick="fetchOpportunities()" class="nb-btn px-4 py-2 bg-ink text-accent text-xs font-bold">Retry</button>
        </div>
      `;
      showToast('Failed to load live opportunities.', 'error');
    }
  }

  function loadMoreCards() {
    visibleCount += 18;
    renderVisibleCards(allFetchedItems.length);
  }

  function renderVisibleCards(totalInStore) {
    const grid = document.getElementById('opportunitiesGrid');
    const loadMoreWrap = document.getElementById('loadMoreWrapper');

    if (!allFetchedItems.length) {
      loadMoreWrap.classList.add('hidden');
      grid.innerHTML = `
        <div class="col-span-full nb-card p-10 text-center space-y-3">
          <span class="material-symbols-outlined text-4xl text-neutral-400">search_off</span>
          <h3 class="font-display font-bold text-lg">No Live Results Found</h3>
          <p class="text-xs text-neutral-600 max-w-md mx-auto">
            ${totalInStore === 0
              ? 'No opportunities cached yet. Click "Refresh Live Data" to fetch from live portals.'
              : 'No live opportunities match your current filters.'}
          </p>
          <div class="flex justify-center gap-2 pt-1">
            <button onclick="resetAllFilters()" class="nb-btn px-4 py-2 bg-white hover:bg-sand text-xs font-bold">Reset Filters</button>
            <button onclick="triggerLiveRefresh()" class="nb-btn px-4 py-2 bg-ink text-accent text-xs font-bold">Refresh Live Data</button>
          </div>
        </div>
      `;
      return;
    }

    const slice = allFetchedItems.slice(0, visibleCount);
    grid.innerHTML = slice.map((opp, idx) => {
      const catColor = opp.category === 'Funding'
        ? 'bg-cobalt text-white'
        : (opp.category === 'Internship' ? 'bg-ink text-accent' : 'bg-accent text-ink');

      const srcShort = opp.source_type === 'Government'
        ? 'Govt'
        : (opp.source_type === 'Company / Corporate' ? 'Company' : 'Uni / Org');

      return `
        <article class="nb-card p-5 flex flex-col justify-between gap-4">
          <div class="space-y-2.5">
            <!-- Row 1: Category + Source + Deadline -->
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-1.5">
                <span class="px-2 py-0.5 text-[10px] font-mono font-bold uppercase border border-ink ${catColor}">${escapeHtml(opp.category)}</span>
                <span class="px-2 py-0.5 text-[10px] font-mono font-semibold bg-cream border border-ink/40 text-neutral-700">${srcShort}</span>
              </div>
              ${deadlinePill(opp.deadline, opp.is_rolling)}
            </div>

            <!-- Row 2: Title & Org -->
            <div>
              <h3 onclick="openDetailModal(${idx})" class="cursor-pointer font-display font-bold text-[15px] leading-snug text-ink hover:text-cobalt line-clamp-2" title="${escapeHtml(opp.title)}">${escapeHtml(opp.title)}</h3>
              <p class="text-xs font-medium text-neutral-600 mt-0.5 truncate">${escapeHtml(opp.organization)}</p>
            </div>

            <!-- Row 3: Concise Summary -->
            <p class="text-xs text-neutral-600 line-clamp-2 leading-relaxed">${escapeHtml(opp.summary)}</p>

            <!-- Row 4: Compact Key Meta -->
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1 pt-1 text-[11px] font-mono text-neutral-700">
              <span class="font-semibold truncate max-w-[180px]" title="${escapeHtml(opp.stipend_or_amount)}">💰 ${escapeHtml(opp.stipend_or_amount)}</span>
              <span class="text-neutral-400">·</span>
              <span>${escapeHtml(opp.degree_level)}</span>
            </div>
          </div>

          <!-- Footer: Trust Signal & Clean CTA -->
          <div class="pt-3 border-t border-neutral-200 flex items-center justify-between gap-2">
            <div class="text-[10px] font-mono text-neutral-500 leading-tight truncate">
              <span class="text-forest font-semibold block">Last verified: ${formatRelativeTime(opp.last_verified_at)}</span>
              <span class="truncate block">${escapeHtml(opp.source_domain)}</span>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
              <button onclick="toggleSaveOpportunity(${idx})" class="px-2 py-1.5 text-[11px] font-bold border-2 border-ink ${isOppSaved(opp.id) ? 'bg-accent text-ink' : 'bg-white hover:bg-sand text-neutral-700'}" title="Save to Personal Kanban Tracker">
                ${isOppSaved(opp.id) ? '★ Saved' : '+ Save'}
              </button>
              <button onclick="openDetailModal(${idx})" class="px-2.5 py-1.5 text-[11px] font-semibold border-2 border-ink bg-cream hover:bg-sand" title="View full details & Deep Analyze">Details</button>
              <a href="${escapeHtml(opp.source_url)}" target="_blank" rel="noopener noreferrer" class="nb-btn px-3 py-1.5 bg-ink text-white hover:bg-accent hover:text-ink text-[11px] font-bold inline-flex items-center gap-1">
                <span>Apply</span>
                <span class="material-symbols-outlined text-[14px]">open_in_new</span>
              </a>
            </div>
          </div>
        </article>
      `;
    }).join('');

    if (allFetchedItems.length > visibleCount) {
      loadMoreWrap.classList.remove('hidden');
      document.getElementById('loadMoreBtn').innerText = `Show More (${visibleCount} of ${allFetchedItems.length} shown)`;
    } else {
      loadMoreWrap.classList.add('hidden');
    }
  }

  function openDetailModal(idx) {
    const opp = allFetchedItems[idx];
    if (!opp) return;
    currentModalIdx = idx;
    currentModalOpp = opp;
    document.getElementById('dmBadges').innerHTML = `
      <span class="px-2 py-0.5 text-[10px] font-mono font-bold uppercase border border-ink bg-accent">${escapeHtml(opp.category)}</span>
      <span class="px-2 py-0.5 text-[10px] font-mono font-semibold border border-ink bg-white">${escapeHtml(opp.source_type)}</span>
      <span class="px-2 py-0.5 text-[10px] font-mono font-semibold border border-ink bg-white">${escapeHtml(opp.domain)}</span>
    `;
    document.getElementById('dmTitle').innerText = opp.title;
    document.getElementById('dmOrg').innerText = `${opp.organization} · ${opp.source_domain}`;
    const saved = isOppSaved(opp.id);
    document.getElementById('dmSaveLabel').innerText = saved ? '★ Saved in Tracker' : '+ Save to Tracker';

    document.getElementById('dmBody').innerHTML = `
      <p class="leading-relaxed">${escapeHtml(opp.summary)}</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 p-3.5 bg-cream border-2 border-ink text-xs">
        <div><span class="text-neutral-500 block font-mono text-[10px]">AMOUNT / STIPEND</span><strong>${escapeHtml(opp.stipend_or_amount)}</strong></div>
        <div><span class="text-neutral-500 block font-mono text-[10px]">DEADLINE</span><strong>${opp.deadline ? escapeHtml(opp.deadline) : 'Rolling / Ongoing'}</strong></div>
        <div><span class="text-neutral-500 block font-mono text-[10px]">ELIGIBILITY</span><strong>${escapeHtml(opp.eligibility)}</strong></div>
        <div><span class="text-neutral-500 block font-mono text-[10px]">LOCATION</span><strong>${escapeHtml(opp.location || 'Global / India')}</strong></div>
      </div>
      <div class="flex flex-wrap items-center justify-between gap-2 pt-1">
        <div class="text-[11px] font-mono text-forest font-semibold">
          ✓ Link HTTP ${opp.http_status} verified (${formatRelativeTime(opp.last_verified_at)})
        </div>
        <button id="deepAnalyzeBtn" onclick="runDeepPageAnalysis('${escapeHtml(opp.id)}')" class="nb-btn px-3 py-1.5 bg-accent text-ink hover:bg-ink hover:text-accent text-xs font-bold inline-flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[15px]">plumbing</span>
          <span>Deep Analyze Official Page / Circular</span>
        </button>
      </div>
      <div id="deepAnalysisContainer" class="hidden pt-2"></div>
    `;
    document.getElementById('dmCal').href = `/api/opportunities/${encodeURIComponent(opp.id)}/calendar`;
    document.getElementById('dmApply').href = opp.source_url;
    document.getElementById('detailModal').classList.remove('hidden');
  }

  async function runDeepPageAnalysis(oppId) {
    const btn = document.getElementById('deepAnalyzeBtn');
    const box = document.getElementById('deepAnalysisContainer');
    if (!box) return;
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span class="material-symbols-outlined text-[15px] animate-spin">sync</span><span>Reading Live Official Page...</span>';
    }
    box.classList.remove('hidden');
    box.innerHTML = '<div class="p-3.5 bg-cream border-2 border-ink font-mono text-xs animate-pulse">Fetching live destination HTML/PDF circular &amp; running layout + entity extraction...</div>';

    try {
      const res = await fetch(`/api/opportunities/${encodeURIComponent(oppId)}/deep-analyze`, { method: 'POST' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const d = await res.json();

      const eligHtml = (d.eligibility_highlights || []).map(item =>
        `<li class="flex items-start gap-1.5"><span class="text-cobalt font-bold">▪</span><span>${escapeHtml(item)}</span></li>`
      ).join('');
      const docsHtml = (d.required_documents || []).map(doc =>
        `<span class="px-2 py-1 bg-white border border-ink text-[11px] font-mono font-semibold">📄 ${escapeHtml(doc)}</span>`
      ).join('');
      const stepsHtml = (d.application_steps || []).map((st, i) => {
        const cleanStep = String(st || '').replace(/^\s*\d+\.\s*/, '');
        return `<li class="text-xs"><strong class="font-mono text-ink">${i + 1}.</strong> ${escapeHtml(cleanStep)}</li>`;
      }).join('');
      const attachmentsList = d.direct_attachments || d.direct_pdf_urls || [];
      const pdfLinksHtml = attachmentsList.map(u =>
        `<a href="${escapeHtml(u)}" target="_blank" rel="noopener noreferrer" class="px-2.5 py-1 bg-white border border-ink hover:bg-accent text-[11px] font-mono font-bold text-cobalt inline-flex items-center gap-1">📎 Official PDF / Circular ↗</a>`
      ).join('');
      const deadlineDisplay = d.extracted_deadline || d.extracted_deadline_text || 'Check Official Page';
      const statusBadge = d.http_status ? `HTTP ${escapeHtml(d.http_status)} · ` : '';

      box.innerHTML = `
        <div class="p-4 bg-sand/70 border-2 border-ink space-y-3 text-xs">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-ink/20 pb-2">
            <span class="font-display font-bold text-sm text-ink">Deep-Page Official Circular Intelligence</span>
            <span class="px-2 py-0.5 bg-ink text-accent font-mono text-[10px] font-bold">${statusBadge}${escapeHtml(d.content_type || 'text/html')}${d.word_count ? ` · ${d.word_count} words` : ''}</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div class="p-2.5 bg-white border border-ink">
              <span class="text-[10px] font-mono text-neutral-500 block">EXTRACTED FINANCIALS / STIPEND</span>
              <strong class="text-ink">${escapeHtml(d.extracted_financials)}</strong>
            </div>
            <div class="p-2.5 bg-white border border-ink">
              <span class="text-[10px] font-mono text-neutral-500 block">EXTRACTED DEADLINE</span>
              <strong class="text-ink">${escapeHtml(deadlineDisplay)}</strong>
            </div>
          </div>
          ${d.key_excerpt ? `<p class="text-[11px] text-neutral-700 bg-white/80 p-2 border border-ink/30 leading-relaxed">${escapeHtml(d.key_excerpt)}</p>` : ''}
          <div>
            <span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Key Eligibility &amp; Guidelines From Page</span>
            <ul class="space-y-1 text-neutral-800">${eligHtml}</ul>
          </div>
          <div>
            <span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Required Documents Checklist</span>
            <div class="flex flex-wrap gap-1.5">${docsHtml}</div>
          </div>
          ${pdfLinksHtml ? `<div><span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Direct Circular / Guideline Attachments</span><div class="flex flex-wrap gap-1.5">${pdfLinksHtml}</div></div>` : ''}
          <div>
            <span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Application Steps</span>
            <ol class="space-y-1 text-neutral-800">${stepsHtml}</ol>
          </div>
        </div>
      `;
      showToast('Deep-page circular analysis complete.', 'success');
    } catch (err) {
      box.innerHTML = `<div class="p-3 bg-red-50 border-2 border-vermilion text-vermilion text-xs font-semibold">Could not deep-analyze page (${escapeHtml(err.message)}).</div>`;
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[15px]">check_circle</span><span>Re-Run Deep Analysis</span>';
      }
    }
  }

  // Personal Kanban Application Tracker
  function isOppSaved(oppId) {
    return kanbanItems.some(k => k.opp_id === oppId);
  }

  function updateTrackerBadge() {
    const el = document.getElementById('navTrackerCount');
    if (el) el.innerText = kanbanItems.length;
  }

  async function loadKanbanTracker() {
    try {
      const res = await fetch(`/api/tracker/${encodeURIComponent(activeSessionId)}`);
      if (!res.ok) return;
      const data = await res.json();
      kanbanItems = data.items || [];
      updateTrackerBadge();
    } catch (e) {}
  }

  async function toggleSaveOpportunity(idx) {
    const opp = allFetchedItems[idx];
    if (!opp) return;
    if (isOppSaved(opp.id)) {
      await removeKanbanItem(opp.id);
    } else {
      try {
        const res = await fetch(`/api/tracker/${encodeURIComponent(activeSessionId)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ opp_id: opp.id, stage: 'Saved' })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        kanbanItems = data.items || [];
        updateTrackerBadge();
        renderVisibleCards(lastTotalInStore);
        showToast(`Saved "${opp.title.slice(0, 38)}..." to My Tracker!`, 'success');
      } catch (e) {
        showToast('Could not save opportunity to tracker.', 'error');
      }
    }
  }

  async function toggleSaveCurrentModalOpp() {
    if (!currentModalOpp) return;
    if (isOppSaved(currentModalOpp.id)) {
      await removeKanbanItem(currentModalOpp.id);
    } else if (currentModalIdx !== null && allFetchedItems[currentModalIdx] && allFetchedItems[currentModalIdx].id === currentModalOpp.id) {
      await toggleSaveOpportunity(currentModalIdx);
    } else {
      try {
        const res = await fetch(`/api/tracker/${encodeURIComponent(activeSessionId)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ opp_id: currentModalOpp.id, stage: 'Saved' })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        kanbanItems = data.items || [];
        updateTrackerBadge();
        renderVisibleCards(lastTotalInStore);
      } catch (e) {}
    }
    document.getElementById('dmSaveLabel').innerText = isOppSaved(currentModalOpp.id) ? '★ Saved in Tracker' : '+ Save to Tracker';
  }

  async function moveKanbanStage(oppId, newStage) {
    try {
      const res = await fetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/${encodeURIComponent(oppId)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage: newStage })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      kanbanItems = data.items || [];
      updateTrackerBadge();
      renderKanbanBoard();
      showToast(`Moved to "${newStage}"`, 'info');
    } catch (e) {
      showToast('Failed to update stage.', 'error');
    }
  }

  async function saveKanbanNote(oppId, stage, noteText) {
    try {
      const res = await fetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/${encodeURIComponent(oppId)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage, notes: noteText })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      kanbanItems = data.items || [];
      showToast('Note saved to tracker.', 'success');
    } catch (e) {
      showToast('Could not save note.', 'error');
    }
  }

  async function removeKanbanItem(oppId) {
    try {
      const res = await fetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/${encodeURIComponent(oppId)}`, {
        method: 'DELETE'
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      kanbanItems = data.items || [];
      updateTrackerBadge();
      renderKanbanBoard();
      renderVisibleCards(lastTotalInStore);
      showToast('Removed from tracker.', 'info');
    } catch (e) {
      showToast('Failed to remove item.', 'error');
    }
  }

  function exportSavedKanbanIcs() {
    if (!kanbanItems.length) {
      showToast('Save at least one opportunity to export your personal deadlines.', 'warning');
      return;
    }
    window.location.href = `/api/tracker/${encodeURIComponent(activeSessionId)}/calendar.ics`;
  }

  function renderKanbanBoard() {
    const board = document.getElementById('kanbanBoardGrid');
    if (!board) return;
    const stageColors = {
      'Saved': 'bg-accent text-ink',
      'Preparing Docs': 'bg-cobalt text-white',
      'Applied': 'bg-ink text-accent',
      'Result': 'bg-forest text-white'
    };

    board.innerHTML = KANBAN_STAGES.map(stage => {
      const colItems = kanbanItems.filter(i => i.stage === stage);
      const cardsHtml = colItems.length
        ? colItems.map(item => `
            <div class="p-3.5 bg-cream/70 border-2 border-ink space-y-2">
              <div class="flex items-start justify-between gap-2">
                <span class="px-1.5 py-0.5 text-[10px] font-mono font-bold border border-ink bg-white">${escapeHtml(item.category)}</span>
                <button onclick="removeKanbanItem('${escapeHtml(item.opp_id)}')" class="text-neutral-400 hover:text-vermilion text-xs font-bold" title="Remove">✕</button>
              </div>
              <a href="${escapeHtml(item.source_url)}" target="_blank" rel="noopener noreferrer" class="block font-display font-bold text-xs text-ink hover:text-cobalt leading-snug">
                ${escapeHtml(item.title)} ↗
              </a>
              <div class="text-[11px] text-neutral-600 truncate">${escapeHtml(item.organization)}</div>
              <div class="flex items-center justify-between text-[10px] font-mono text-neutral-700 pt-1">
                <span class="truncate max-w-[110px]">💰 ${escapeHtml(item.stipend_or_amount)}</span>
                <span class="font-semibold">${item.deadline ? escapeHtml(item.deadline) : 'Rolling'}</span>
              </div>
              <input type="text" value="${escapeHtml(item.notes || '')}" placeholder="Add note (e.g. pending NOC)..." onchange="saveKanbanNote('${escapeHtml(item.opp_id)}', '${escapeHtml(item.stage)}', this.value)" class="w-full bg-white border border-ink/40 px-2 py-1 text-[11px] focus:outline-none focus:border-ink"/>
              <div class="pt-2 border-t border-neutral-300 flex items-center justify-between gap-1">
                <label class="text-[10px] font-mono text-neutral-500">Stage:</label>
                <select onchange="moveKanbanStage('${escapeHtml(item.opp_id)}', this.value)" class="bg-white border border-ink px-1.5 py-0.5 text-[11px] font-semibold">
                  ${KANBAN_STAGES.map(s => `<option value="${s}" ${s === item.stage ? 'selected' : ''}>${s}</option>`).join('')}
                </select>
              </div>
            </div>
          `).join('')
        : `<div class="p-6 border-2 border-dashed border-neutral-300 text-center text-xs text-neutral-400">No items in ${escapeHtml(stage)}</div>`;

      return `
        <div class="nb-card p-3.5 space-y-3">
          <div class="flex items-center justify-between border-b-2 border-ink pb-2">
            <span class="px-2 py-0.5 text-xs font-display font-bold border border-ink ${stageColors[stage] || 'bg-accent'}">${escapeHtml(stage)}</span>
            <span class="font-mono text-xs font-bold">${colItems.length}</span>
          </div>
          <div class="space-y-2.5">${cardsHtml}</div>
        </div>
      `;
    }).join('');
  }

  function closeDetailModal() {
    document.getElementById('detailModal').classList.add('hidden');
  }

  async function triggerLiveRefresh() {
    const btn = document.getElementById('refreshLiveBtn');
    const icon = document.getElementById('refreshIcon');
    const label = document.getElementById('refreshBtnLabel');
    btn.disabled = true;
    icon.classList.add('animate-spin');
    if (label) label.innerText = 'Syncing...';
    renderSkeletons(6);
    showToast('Crawling live Government portals & top company boards...', 'info');

    try {
      const res = await fetch('/api/opportunities/refresh?force=true', { method: 'POST' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const report = await res.json();
      facetsInitialized = false;
      document.getElementById('filterDomain').innerHTML = '<option value="All">All Domains</option>';
      document.getElementById('filterFundingType').innerHTML = '<option value="All">All Types</option>';
      await updateStatsCounters();
      await fetchOpportunities();
      showToast(
        `Synced ${report.total_live_opportunities} live opportunities (${report.broken_links_discarded} broken & ${report.expired_filtered} expired removed).`,
        report.source_errors && report.source_errors.length > 0 ? 'warning' : 'success'
      );
    } catch (err) {
      showToast(`Live refresh failed: ${err.message}`, 'error');
      await fetchOpportunities();
    } finally {
      btn.disabled = false;
      icon.classList.remove('animate-spin');
      if (label) label.innerText = 'Refresh Live Data';
    }
  }

  // Saral AI & Document Checker
  function quickAsk(q) { document.getElementById('ragInput').value = q; sendRagQuery(); }

  async function sendRagQuery() {
    const inp = document.getElementById('ragInput');
    const box = document.getElementById('ragMessages');
    const query = inp.value.trim();
    if (!query) return;
    inp.value = '';
    box.insertAdjacentHTML('beforeend', `<div class="flex justify-end"><div class="max-w-[80%] px-3 py-2 bg-ink text-accent border-2 border-ink text-xs font-semibold">${escapeHtml(query)}</div></div>`);
    box.scrollTop = box.scrollHeight;
    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: activeSessionId, language: document.getElementById('ragLang').value })
      });
      const data = await res.json();
      if (data.session_id) { activeSessionId = data.session_id; localStorage.setItem('madadgaar_session_id', activeSessionId); }
      const htmlAns = escapeHtml(data.answer || '')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*([^*\n]+)\*/g, '<em class="text-neutral-600">$1</em>')
        .replace(/`([^`\n]+)`/g, '<code class="px-1 py-0.5 bg-sand font-mono text-[11px]">$1</code>')
        .replace(/(https?:\/\/[^\s<)]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-cobalt underline break-all">$1</a>')
        .replace(/\n/g, '<br/>');
      const cites = (data.citations || []).slice(0, 3).map((c, i) =>
        `<div class="text-[11px] font-mono flex justify-between gap-2 pt-1"><span class="truncate">[${i+1}] ${escapeHtml(c.title)}</span><a href="${escapeHtml(c.official_url)}" target="_blank" class="text-cobalt font-bold shrink-0 hover:underline">Source ↗</a></div>`
      ).join('');
      box.insertAdjacentHTML('beforeend', `<div class="p-3.5 bg-white border-2 border-ink text-xs sm:text-sm space-y-2"><div>${htmlAns}</div>${cites ? `<div class="border-t border-neutral-200 pt-1.5">${cites}</div>` : ''}</div>`);
      box.scrollTop = box.scrollHeight;
    } catch (e) { showToast('Saral AI unavailable.', 'error'); }
  }

  async function analyzeDocText() {
    const raw_text = document.getElementById('docText').value.trim();
    if (!raw_text) { showToast('Paste document text first.', 'warning'); return; }
    const out = document.getElementById('docOutput');
    out.innerHTML = '<div class="font-mono animate-pulse">Analyzing...</div>';
    try {
      const res = await fetch('/api/documents/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_text, document_type_hint: 'AUTO' })
      });
      renderDocResult(await res.json());
    } catch (e) { out.innerHTML = '<div class="text-vermilion font-semibold">Analysis failed.</div>'; }
  }

  async function uploadAndAnalyzeDoc() {
    const inp = document.getElementById('docFile');
    if (!inp.files || !inp.files.length) { showToast('Select a file first.', 'warning'); return; }
    const fd = new FormData();
    fd.append('file', inp.files[0]);
    fd.append('document_type_hint', 'AUTO');
    const out = document.getElementById('docOutput');
    out.innerHTML = '<div class="font-mono animate-pulse">Scanning file...</div>';
    try {
      const res = await fetch('/api/documents/upload', { method: 'POST', body: fd });
      renderDocResult(await res.json());
    } catch (e) { out.innerHTML = '<div class="text-vermilion font-semibold">File scan failed.</div>'; }
  }

  function renderDocResult(data) {
    const out = document.getElementById('docOutput');
    const fields = (data.extracted_fields || []).map(f =>
      `<div class="p-2 bg-cream border border-ink flex justify-between gap-2 font-mono text-[11px]"><span><strong>${escapeHtml(f.field_name)}:</strong> ${escapeHtml(f.extracted_value || 'Missing')}</span><span class="font-bold">${escapeHtml(f.status)}</span></div>`
    ).join('');
    out.innerHTML = `
      <div class="font-mono font-bold text-cobalt">${escapeHtml(data.document_type)} (${escapeHtml(data.extraction_method)})</div>
      <div class="space-y-1.5">${fields}</div>
      <div class="p-2 bg-accent/60 border border-ink text-[10px] font-medium">${escapeHtml(data.authenticity_disclaimer)}</div>
    `;
  }

  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeDetailModal(); });

  (async function init() {
    await loadKanbanTracker();
    await updateStatsCounters();
    await fetchOpportunities();
  })();
</script>
</body>
</html>
"""
