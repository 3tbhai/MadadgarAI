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
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
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

    <!-- Primary 4-Tab Navigation -->
    <nav class="flex items-center gap-1 sm:gap-1.5 overflow-x-auto">
      <button id="navOpportunities" onclick="switchWorkspace('opportunities')" class="px-2.5 sm:px-3 py-1.5 text-xs font-semibold border-2 border-ink bg-accent text-ink shadow-[2px_2px_0px_#18181b] shrink-0">
        Opportunities
      </button>
      <button id="navMatcher" onclick="switchWorkspace('matcher')" class="px-2.5 sm:px-3 py-1.5 text-xs font-semibold border-2 border-transparent text-neutral-600 hover:border-ink hover:text-ink shrink-0">
        Match &amp; Resume
      </button>
      <button id="navTracker" onclick="switchWorkspace('tracker')" class="px-2.5 sm:px-3 py-1.5 text-xs font-semibold border-2 border-transparent text-neutral-600 hover:border-ink hover:text-ink inline-flex items-center gap-1.5 shrink-0">
        <span>My Tracker</span>
        <span id="navTrackerCount" class="px-1.5 py-0.2 bg-ink text-accent font-mono text-[10px] font-bold">0</span>
      </button>
      <button id="navAssistant" onclick="switchWorkspace('assistant')" class="px-2.5 sm:px-3 py-1.5 text-xs font-semibold border-2 border-transparent text-neutral-600 hover:border-ink hover:text-ink shrink-0">
        Saral AI &amp; Docs
      </button>
    </nav>

    <!-- Auth & Refresh Controls -->
    <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
      <!-- Sign In Button (Logged out) -->
      <button id="authSignInBtn" onclick="openAuthModal()" class="nb-btn px-2.5 py-1.5 bg-white hover:bg-accent text-ink text-xs font-bold inline-flex items-center gap-1.5" title="Sign in to access your personal study space">
        <span class="material-symbols-outlined text-[15px]">login</span>
        <span class="hidden md:inline">Sign In</span>
      </button>

      <!-- Authenticated User Avatar Menu (Logged in) -->
      <div id="authUserMenu" class="hidden relative">
        <button onclick="toggleUserDropdown()" class="nb-btn px-2 py-1 bg-white hover:bg-sand text-xs font-bold inline-flex items-center gap-1.5">
          <span id="authUserAvatar" class="w-5 h-5 bg-ink text-accent font-mono text-[10px] font-bold flex items-center justify-center rounded-none">U</span>
          <span id="authUserName" class="hidden lg:inline max-w-[90px] truncate">User</span>
        </button>
        <div id="authUserDropdown" class="hidden absolute right-0 mt-1.5 w-52 bg-white border-2 border-ink shadow-[4px_4px_0px_#18181b] p-3 text-xs space-y-2 z-50">
          <div class="border-b border-neutral-200 pb-2">
            <div id="authDropName" class="font-display font-bold text-ink truncate"></div>
            <div id="authDropEmail" class="text-[11px] text-neutral-500 font-mono truncate"></div>
          </div>
          <button onclick="switchWorkspace('assistant'); switchAssistantSubmode('private'); toggleUserDropdown();" class="w-full text-left px-2 py-1.5 hover:bg-sand font-semibold">My Study Assistant</button>
          <button onclick="logoutUser()" class="w-full text-left px-2 py-1.5 text-vermilion hover:bg-red-50 font-bold">Sign Out</button>
        </div>
      </div>

      <!-- Refresh Live Button -->
      <button id="refreshLiveBtn" onclick="triggerLiveRefresh()" class="nb-btn px-2.5 sm:px-3 py-1.5 bg-ink text-accent hover:bg-accent hover:text-ink text-xs font-semibold inline-flex items-center gap-1.5 disabled:opacity-60" title="Check for the latest opportunities">
        <span id="refreshIcon" class="material-symbols-outlined text-[16px]">sync</span>
        <span id="refreshBtnLabel" class="hidden sm:inline">Refresh Live Data</span>
      </button>
    </div>
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
          Up-to-date internships, scholarships &amp; grants from official government portals and leading companies. Every link is verified.
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
        <strong>Some portals are temporarily unavailable:</strong>
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
            <option value="recent_desc">Newest First</option>
            <option value="title_asc">Title: A → Z</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Subtle Status Strip -->
    <div class="flex flex-wrap items-center justify-between gap-2 text-xs text-neutral-600 px-0.5">
      <div id="resultsSummaryText" class="font-medium">Loading live opportunities...</div>
      <div class="flex flex-wrap items-center gap-3.5">
        <span id="cacheStatusLabel" class="font-mono text-[11px] text-neutral-500"></span>
        <button id="resetFiltersLink" onclick="resetAllFilters()" class="hidden text-vermilion hover:underline font-semibold">Clear filters</button>
        <button onclick="copyShareableFilterUrl()" class="text-ink hover:text-cobalt hover:underline font-semibold inline-flex items-center gap-1" title="Copy shareable filtered link">
          <span class="material-symbols-outlined text-[15px]">share</span> Share View
        </button>
        <a id="exportCsvLink" href="/api/opportunities/export.csv" download class="text-forest hover:underline font-semibold inline-flex items-center gap-1" title="Download filtered results as CSV">
          <span class="material-symbols-outlined text-[15px]">download</span> Export CSV
        </a>
        <a href="/api/calendar/upcoming.ics" download class="text-cobalt hover:underline font-semibold inline-flex items-center gap-1">
          <span class="material-symbols-outlined text-[15px]">calendar_month</span> Add to Calendar
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
  <!-- VIEW 2: ELIGIBILITY MATCHER & RESUME MATCHER             -->
  <!-- ======================================================== -->
  <div id="workspaceMatcher" class="hidden space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
      <div>
        <h2 class="font-display font-bold text-2xl tracking-tight text-ink">Eligibility &amp; Resume Matcher</h2>
        <p class="text-xs sm:text-sm text-neutral-600 mt-0.5">
          Check your eligibility for scholarships and research grants, or upload your resume to discover your best matches.
        </p>
      </div>
      <div class="flex items-center gap-1.5">
        <button id="matchModeStudent" onclick="switchMatcherMode('student')" class="px-3 py-1.5 text-xs font-bold border-2 border-ink bg-ink text-accent">Student Profile</button>
        <button id="matchModeResearcher" onclick="switchMatcherMode('researcher')" class="px-3 py-1.5 text-xs font-bold border-2 border-ink bg-white hover:bg-sand">Researcher / PI</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Left Column: Profile Form (Student or Researcher) -->
      <div class="lg:col-span-5 space-y-5">
        <!-- Student Eligibility Form -->
        <form id="studentMatcherForm" onsubmit="event.preventDefault(); runStudentEligibilityMatch();" class="nb-card p-5 space-y-3.5 text-xs">
          <div class="flex items-center justify-between border-b-2 border-ink pb-2">
            <h3 class="font-display font-bold text-sm">Student Eligibility Profile</h3>
            <span class="px-2 py-0.5 bg-accent border border-ink font-mono text-[10px] font-bold">ELIGIBILITY</span>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Full Name</label>
              <input id="smName" type="text" value="Aarav Sharma" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
            </div>
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Gender</label>
              <select id="smGender" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5">
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Transgender">Transgender</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">State Domicile</label>
              <select id="smState" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5">
                <option value="All India">All India</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Karnataka">Karnataka</option>
                <option value="Delhi NCR">Delhi NCR</option>
                <option value="Rajasthan">Rajasthan</option>
                <option value="Tamil Nadu">Tamil Nadu</option>
                <option value="Assam / North Eastern States">Assam / North Eastern States</option>
              </select>
            </div>
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Social Category</label>
              <select id="smCategory" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5">
                <option value="General / Open">General / Open</option>
                <option value="OBC (Non-Creamy Layer)">OBC (Non-Creamy Layer)</option>
                <option value="SC (Scheduled Caste)">SC (Scheduled Caste)</option>
                <option value="ST (Scheduled Tribe)">ST (Scheduled Tribe)</option>
                <option value="EWS (Economically Weaker Section)">EWS (Economically Weaker Section)</option>
                <option value="Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)">Minority</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block font-semibold text-neutral-600 mb-1">Education Level</label>
            <select id="smEdu" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5">
              <option value="UG - Engineering / Technology (B.Tech/B.E.)">UG - Engineering / B.Tech / B.E.</option>
              <option value="UG - General (B.Sc / B.Com / B.A. / BBA / BCA)">UG - General (B.Sc / B.A / B.Com)</option>
              <option value="UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)">UG - Medical / Nursing</option>
              <option value="Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)">Postgraduate (M.Tech / M.Sc / MBA)</option>
              <option value="PhD / Doctoral Research">PhD / Doctoral Research</option>
              <option value="Diploma / Polytechnic">Diploma / Polytechnic</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Family Income (INR / yr)</label>
              <input id="smIncome" type="number" value="250000" min="0" step="25000" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
            </div>
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Marks / % (Optional)</label>
              <input id="smPct" type="number" value="86" min="0" max="100" step="0.5" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
            </div>
          </div>
          <div class="flex flex-wrap gap-4 pt-1">
            <label class="inline-flex items-center gap-1.5 font-medium"><input id="smSingleGirl" type="checkbox" class="accent-ink"/> Single Girl Child</label>
            <label class="inline-flex items-center gap-1.5 font-medium"><input id="smPwd" type="checkbox" class="accent-ink"/> PwD (&ge;40%)</label>
          </div>
          <button type="submit" class="nb-btn w-full py-2.5 bg-ink text-accent hover:bg-accent hover:text-ink text-xs font-bold">
            Find Eligible Scholarships &amp; Internships
          </button>
        </form>

        <!-- Researcher / PI Grant Compliance Form -->
        <form id="researcherMatcherForm" onsubmit="event.preventDefault(); runResearcherGrantMatch();" class="hidden nb-card p-5 space-y-3.5 text-xs">
          <div class="flex items-center justify-between border-b-2 border-ink pb-2">
            <h3 class="font-display font-bold text-sm">Researcher / Faculty Grant Matcher</h3>
            <span class="px-2 py-0.5 bg-cobalt text-white border border-ink font-mono text-[10px] font-bold">GRANT MATCH</span>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Researcher / PI Name</label>
              <input id="rmName" type="text" value="Dr. Priya Nair" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
            </div>
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Highest Degree</label>
              <input id="rmDegree" type="text" value="Ph.D. in Computer Science" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Institution</label>
              <input id="rmInst" type="text" value="Recognized Indian University" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
            </div>
            <div>
              <label class="block font-semibold text-neutral-600 mb-1">Age (Optional)</label>
              <input id="rmAge" type="number" value="34" min="18" max="75" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
            </div>
          </div>
          <div>
            <label class="block font-semibold text-neutral-600 mb-1">Research Focus &amp; Proposal Abstract</label>
            <textarea id="rmSummary" rows="3" class="w-full bg-cream/60 border-2 border-ink p-2.5" placeholder="e.g. Indigenous AI diagnostics for healthcare biotech, robotics, or space propulsion...">Artificial intelligence and edge computing for affordable medical diagnostics and climate-resilient biotechnology</textarea>
          </div>
          <button type="submit" class="nb-btn w-full py-2.5 bg-cobalt text-white hover:bg-ink hover:text-accent text-xs font-bold">
            Match Research Grants &amp; Verify Compliance
          </button>
        </form>

        <!-- Resume / CV Upload Opportunity Matcher -->
        <div id="resumeMatcherMount" class="nb-card p-5 space-y-3.5 text-xs">
          <div class="flex items-center justify-between border-b-2 border-ink pb-2">
            <h3 class="font-display font-bold text-sm">Resume Matcher</h3>
            <span class="px-2 py-0.5 bg-forest text-white border border-ink font-mono text-[10px] font-bold">RESUME FIT</span>
          </div>
          <p class="text-[11px] text-neutral-600">
            Upload your resume or paste your skills below to see the opportunities that fit your background best.
          </p>
          <div class="flex items-center gap-2 p-2 bg-cream/70 border-2 border-ink">
            <input type="file" id="resumeFile" accept=".pdf,.docx,.txt,.md" class="flex-1 text-xs"/>
            <select id="resumeCatFilter" class="bg-white border border-ink px-2 py-1 text-[11px] font-semibold">
              <option value="All">All Types</option>
              <option value="Internship">Internships</option>
              <option value="Scholarship">Scholarships</option>
              <option value="Funding">Grants</option>
            </select>
          </div>
          <textarea id="resumeRawText" rows="3" placeholder="Or paste your resume / skills / research keywords (e.g. B.Tech CSE, Python, PyTorch, FastAPI, Machine Learning, Robotics)..." class="w-full bg-cream/60 border-2 border-ink p-2.5 text-xs font-mono focus:outline-none focus:bg-white"></textarea>
          <button type="button" onclick="runResumeSemanticMatch()" class="nb-btn w-full py-2.5 bg-accent text-ink hover:bg-ink hover:text-accent text-xs font-bold">
            Find Matches From My Resume
          </button>
        </div>
      </div>

      <!-- Right Column: Match Results -->
      <div class="lg:col-span-7 space-y-4">
        <div id="matcherResultsContainer" class="nb-card p-6 text-center space-y-2">
          <span class="material-symbols-outlined text-4xl text-neutral-400">fact_check</span>
          <h3 class="font-display font-bold text-base">Ready to Check Eligibility</h3>
          <p class="text-xs text-neutral-600 max-w-md mx-auto">
            Fill in your Student or Researcher profile on the left to see tailored matches, clear eligibility notes, and quick SOP or proposal drafts.
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- VIEW 3: PERSONAL APPLICATION KANBAN TRACKER & TIMELINE   -->
  <!-- ======================================================== -->
  <div id="workspaceTracker" class="hidden space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3">
      <div>
        <h2 class="font-display font-bold text-2xl tracking-tight text-ink">My Applications &amp; Deadlines</h2>
        <p class="text-xs sm:text-sm text-neutral-600 mt-0.5">
          Organize your saved opportunities by stage or deadline, set reminders, and add dates to your calendar.
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <div class="inline-flex border-2 border-ink bg-white">
          <button id="trackerModeKanban" onclick="switchTrackerView('kanban')" class="px-3 py-1.5 text-xs font-bold bg-ink text-accent">Board</button>
          <button id="trackerModeTimeline" onclick="switchTrackerView('timeline')" class="px-3 py-1.5 text-xs font-bold bg-white text-ink hover:bg-sand">Timeline</button>
        </div>
        <button onclick="exportSavedKanbanIcs()" class="nb-btn px-3.5 py-2 bg-accent text-ink hover:bg-ink hover:text-accent text-xs font-bold inline-flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[16px]">calendar_month</span>
          <span>Add Saved to Calendar</span>
        </button>
      </div>
    </div>

    <!-- Deadline Reminders Bar -->
    <div class="nb-card p-4 bg-cream/60 space-y-3 text-xs">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="font-display font-bold text-sm flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[18px] text-vermilion">notifications_active</span>
          <span>Deadline Reminders</span>
        </div>
        <button onclick="dispatchTrackerReminders()" class="px-2.5 py-1 bg-white border-2 border-ink hover:bg-accent text-[11px] font-bold">
          Check Reminders
        </button>
      </div>
      <form onsubmit="event.preventDefault(); addTrackerReminder();" class="grid grid-cols-1 sm:grid-cols-12 gap-2">
        <select id="remChannel" class="sm:col-span-3 bg-white border-2 border-ink px-2.5 py-1.5 font-semibold">
          <option value="browser">Browser Alert</option>
          <option value="webhook">Slack / Discord Alert</option>
          <option value="email">Email Digest</option>
        </select>
        <input id="remTarget" type="text" placeholder="Email address, alert label, or notification link..." class="sm:col-span-5 bg-white border-2 border-ink px-2.5 py-1.5"/>
        <select id="remLeadDays" class="sm:col-span-2 bg-white border-2 border-ink px-2 py-1.5 font-semibold">
          <option value="2">2 days before</option>
          <option value="7" selected>7 days before</option>
          <option value="14">14 days before</option>
        </select>
        <button type="submit" class="sm:col-span-2 nb-btn py-1.5 bg-ink text-accent hover:bg-accent hover:text-ink font-bold">
          Add Alert
        </button>
      </form>
      <div id="trackerRemindersList" class="flex flex-wrap gap-2"></div>
    </div>

    <div id="kanbanBoardGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-start"></div>
    <div id="timelineBoardView" class="hidden space-y-3"></div>
  </div>

  <!-- ======================================================== -->
  <!-- VIEW 4: SARAL AI STUDY ASSISTANT & DOCUMENT CHECKER      -->
  <!-- ======================================================== -->
  <div id="workspaceAssistant" class="hidden space-y-5">
    <!-- Sub-mode Switcher Bar -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div class="inline-flex border-2 border-ink bg-white self-start">
        <button id="submodePrivateBtn" onclick="switchAssistantSubmode('private')" class="px-3.5 py-2 text-xs font-bold bg-ink text-accent">
          My Study Assistant
        </button>
        <button id="submodePublicBtn" onclick="switchAssistantSubmode('public')" class="px-3.5 py-2 text-xs font-bold bg-white text-ink hover:bg-sand">
          Schemes &amp; Document Check
        </button>
      </div>
    </div>

    <!-- SUB-VIEW A: PERSONAL STUDY SPACE -->
    <div id="assistantPrivatePanel" class="space-y-4">
      <!-- Login Gate (Shown when unauthenticated) -->
      <div id="privateAuthGate" class="nb-card p-8 text-center space-y-4">
        <div class="w-12 h-12 mx-auto bg-accent border-2 border-ink flex items-center justify-center shadow-[3px_3px_0px_#18181b]">
          <span class="material-symbols-outlined text-2xl text-ink">lock_person</span>
        </div>
        <div class="space-y-1 max-w-lg mx-auto">
          <h2 class="font-display font-bold text-xl text-ink">Sign In to Your Personal Study Space</h2>
          <p class="text-xs text-neutral-600 leading-relaxed">
            Upload your PDFs, lecture notes, circulars, or research papers to get clear, cited answers grounded strictly in your own library.
          </p>
        </div>
        <button onclick="openAuthModal()" class="nb-btn px-5 py-2.5 bg-ink text-accent hover:bg-accent hover:text-ink text-xs font-bold inline-flex items-center gap-2">
          <span class="material-symbols-outlined text-[18px]">passkey</span>
          <span>Continue with Google</span>
        </button>
      </div>

      <!-- Authenticated Private Workspace -->
      <div id="privateWorkspaceGrid" class="hidden grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        <!-- Left: Document Library & Chat Sessions -->
        <div class="lg:col-span-5 space-y-4">
          <div class="nb-card p-4 space-y-3 text-xs">
            <div class="flex items-center justify-between border-b-2 border-ink pb-2">
              <h3 class="font-display font-bold text-sm">My Documents</h3>
              <span id="privateDocCount" class="px-2 py-0.5 bg-cream border border-ink font-mono text-[10px] font-bold">0 docs</span>
            </div>

            <!-- Upload PDF/MD/TXT -->
            <div class="flex items-center gap-2 p-2 bg-cream/70 border-2 border-ink">
              <input type="file" id="privateDocFile" accept=".pdf,.md,.markdown,.txt" class="flex-1 text-[11px]"/>
              <button type="button" onclick="uploadPrivateDocument()" class="nb-btn px-3 py-1 bg-ink text-accent hover:bg-accent hover:text-ink text-[11px] font-bold shrink-0">Upload</button>
            </div>

            <!-- Add Link / Paper -->
            <form onsubmit="event.preventDefault(); ingestPrivateUrl();" class="flex gap-1.5">
              <input id="privateUrlInput" type="url" placeholder="Paste an article or paper link (https://...)" class="flex-1 bg-cream/60 border-2 border-ink px-2.5 py-1.5 text-[11px]"/>
              <button type="submit" class="nb-btn px-3 py-1.5 bg-white hover:bg-accent text-[11px] font-bold shrink-0">Add Link</button>
            </form>

            <!-- Document Status List -->
            <div id="privateDocsList" class="space-y-2 max-h-60 overflow-y-auto"></div>
          </div>

          <!-- Persisted Multi-Turn Sessions -->
          <div class="nb-card p-4 space-y-2.5 text-xs">
            <div class="flex items-center justify-between border-b-2 border-ink pb-2">
              <h3 class="font-display font-bold text-sm">Recent Chats</h3>
              <button onclick="startNewPrivateSession()" class="px-2 py-0.5 bg-accent border border-ink font-mono text-[10px] font-bold hover:bg-ink hover:text-accent">+ New Chat</button>
            </div>
            <div id="privateSessionsList" class="space-y-1.5 max-h-40 overflow-y-auto"></div>
          </div>
        </div>

        <!-- Right: Study Assistant Chat -->
        <div class="lg:col-span-7 nb-card flex flex-col h-[620px]">
          <div id="privateChatHeader" class="px-4 py-3 border-b-2 border-ink bg-accent flex flex-wrap items-center justify-between gap-2">
            <div>
              <div class="flex items-center gap-2">
                <h2 class="font-display font-bold text-base">Saral AI</h2>
                <span class="px-2 py-0.5 bg-ink text-accent font-mono text-[10px] font-bold">PRIVATE LIBRARY</span>
              </div>
              <p class="text-[11px] text-neutral-800 mt-0.5">Clear, grounded answers with clickable citations from your uploaded documents.</p>
            </div>
          </div>

          <!-- Quick Prompts -->
          <div class="px-4 py-2 bg-sand/70 border-b border-neutral-300 flex flex-wrap gap-1.5 text-[11px]">
            <button type="button" onclick="quickPrivateAsk('Summarize the key points from my uploaded documents with citations.')" class="px-2.5 py-1 bg-white border border-ink hover:bg-accent font-semibold text-ink">Summarize key points</button>
            <button type="button" onclick="quickPrivateAsk('List all important deadlines, eligibility criteria, and requirements mentioned in my documents.')" class="px-2.5 py-1 bg-white border border-ink hover:bg-accent font-semibold text-ink">Deadlines &amp; rules</button>
            <button type="button" onclick="quickPrivateAsk('Explain the core concepts and formulas in my uploaded notes step-by-step.')" class="px-2.5 py-1 bg-white border border-ink hover:bg-accent font-semibold text-ink">Explain step-by-step</button>
          </div>

          <div id="privateChatMessages" class="flex-1 p-4 overflow-y-auto space-y-3 text-sm bg-cream/50">
            <div class="p-3.5 bg-white border-2 border-ink text-xs text-neutral-700 leading-relaxed">
              Upload your notes, PDFs, or links on the left, then ask any question here. Click any citation badge to inspect the exact source passage.
            </div>
          </div>

          <form onsubmit="event.preventDefault(); sendPrivateRagStream();" class="p-3 border-t-2 border-ink bg-white flex gap-2">
            <input id="privateChatInput" type="text" placeholder="Ask about your uploaded notes, formulas, or research papers..." class="flex-1 bg-cream/60 border-2 border-ink px-3 py-2 text-sm focus:outline-none focus:bg-white"/>
            <button id="privateChatSendBtn" type="submit" class="nb-btn px-4 py-2 bg-ink text-accent text-xs font-bold hover:bg-accent hover:text-ink">Ask</button>
          </form>
        </div>
      </div>
    </div>

    <!-- SUB-VIEW B: EXISTING PUBLIC SARAL SAMJHAUTI & DOCUMENT CHECKER -->
    <div id="assistantPublicPanel" class="hidden grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
    <!-- Chat -->
    <div class="lg:col-span-7 nb-card flex flex-col h-[600px]">
      <div class="px-4 py-3 border-b-2 border-ink bg-accent flex items-center justify-between gap-2">
        <div>
          <div class="flex items-center gap-2">
            <h2 class="font-display font-bold text-base">Saral Samjhauti AI</h2>
            <span class="px-1.5 py-0.5 bg-ink text-accent font-mono text-[9px] font-bold">BILINGUAL</span>
          </div>
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
  </div>

</main>

<!-- ================= AUTH SIGN-IN MODAL ================= -->
<div id="authModal" class="hidden fixed inset-0 z-50 bg-ink/60 backdrop-blur-xs flex items-center justify-center p-4" onclick="if(event.target===this) closeAuthModal()">
  <div class="bg-white border-2 border-ink shadow-[6px_6px_0px_#18181b] max-w-md w-full overflow-hidden">
    <div class="p-4 border-b-2 border-ink bg-accent flex items-center justify-between">
      <h3 class="font-display font-bold text-base text-ink">Sign In to Saral AI</h3>
      <button onclick="closeAuthModal()" class="p-1 border-2 border-ink bg-white hover:bg-sand"><span class="material-symbols-outlined text-[16px] block">close</span></button>
    </div>
    <div class="p-5 space-y-4 text-xs">
      <p class="text-neutral-600 leading-relaxed">
        Sign in to save your private documents, keep your chat history, and sync your personal application tracker across sessions.
      </p>
      <a id="googleOAuthBtn" href="/api/auth/google/login" class="nb-btn w-full py-2.5 bg-white hover:bg-cream text-ink font-bold inline-flex items-center justify-center gap-2">
        <span class="font-display font-bold text-base text-cobalt">G</span>
        <span>Continue with Google</span>
      </a>
      <div id="googleOAuthHint" class="hidden p-2 bg-cream border border-ink/40 text-[11px] text-neutral-600">
        Google sign-in is currently unavailable. You can continue with Guest Access below.
      </div>
      <div id="devLoginSection" class="pt-3 border-t-2 border-ink/15 space-y-2.5">
        <div class="font-mono text-[10px] font-bold uppercase text-neutral-500">Quick Guest Sign-In</div>
        <form onsubmit="event.preventDefault(); submitDevLogin();" class="space-y-2">
          <input id="devLoginName" type="text" value="Aarav Student" placeholder="Full Name" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
          <input id="devLoginEmail" type="email" value="student@madadgaarai.local" placeholder="Email Address" class="w-full bg-cream/60 border-2 border-ink px-2.5 py-1.5"/>
          <button type="submit" class="nb-btn w-full py-2 bg-ink text-accent hover:bg-accent hover:text-ink font-bold">
            Continue as Guest
          </button>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- ================= CITATION PASSAGE DRAWER ================= -->
<div id="citationModal" class="hidden fixed inset-0 z-50 bg-ink/60 backdrop-blur-xs flex items-center justify-center p-4" onclick="if(event.target===this) closeCitationModal()">
  <div class="bg-white border-2 border-ink shadow-[6px_6px_0px_#18181b] max-w-xl w-full max-h-[82vh] flex flex-col overflow-hidden">
    <div class="p-4 border-b-2 border-ink bg-cream flex items-start justify-between gap-2">
      <div>
        <div id="citMetaBadges" class="flex flex-wrap gap-1.5 mb-1"></div>
        <h3 id="citDocTitle" class="font-display font-bold text-base text-ink">Source Passage</h3>
      </div>
      <button onclick="closeCitationModal()" class="p-1 border-2 border-ink bg-white hover:bg-accent"><span class="material-symbols-outlined text-[16px] block">close</span></button>
    </div>
    <div id="citChunkBody" class="p-5 overflow-y-auto text-xs leading-relaxed text-neutral-800 whitespace-pre-wrap bg-cream/40"></div>
  </div>
</div>

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
          <span class="material-symbols-outlined text-[16px]">calendar_month</span> Calendar
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
    <div><strong class="text-ink">MadadgaarAI</strong> — Verified Scholarships, Internships &amp; Research Grants</div>
    <div class="text-[11px] text-neutral-500">Official Sources · Updated Regularly</div>
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
  let anonSessionId = localStorage.getItem('madadgaar_session_id') || '';
  if (!anonSessionId) {
    anonSessionId = 'sess-' + Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
    localStorage.setItem('madadgaar_session_id', anonSessionId);
  }
  let activeSessionId = anonSessionId;
  let pendingRefreshPromise = null;

  async function authFetch(url, options = {}) {
    const opts = { ...options, credentials: 'include' };
    let res = await fetch(url, opts);
    if (res.status === 401 && !options._retried) {
      if (!pendingRefreshPromise) {
        pendingRefreshPromise = fetch('/api/auth/refresh', { method: 'POST', credentials: 'include' })
          .then(r => r.ok)
          .catch(() => false)
          .finally(() => { pendingRefreshPromise = null; });
      }
      const refreshed = await pendingRefreshPromise;
      if (refreshed) {
        res = await fetch(url, { ...opts, _retried: true });
      }
    }
    return res;
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
    document.getElementById('workspaceMatcher').classList.toggle('hidden', ws !== 'matcher');
    document.getElementById('workspaceTracker').classList.toggle('hidden', ws !== 'tracker');
    document.getElementById('workspaceAssistant').classList.toggle('hidden', ws !== 'assistant');
    const act = 'px-2.5 sm:px-3 py-1.5 text-xs font-semibold border-2 border-ink bg-accent text-ink shadow-[2px_2px_0px_#18181b] inline-flex items-center gap-1.5 shrink-0';
    const inact = 'px-2.5 sm:px-3 py-1.5 text-xs font-semibold border-2 border-transparent text-neutral-600 hover:border-ink hover:text-ink inline-flex items-center gap-1.5 shrink-0';
    document.getElementById('navOpportunities').className = ws === 'opportunities' ? act : inact;
    document.getElementById('navMatcher').className = ws === 'matcher' ? act : inact;
    document.getElementById('navTracker').className = ws === 'tracker' ? act : inact;
    document.getElementById('navAssistant').className = ws === 'assistant' ? act : inact;
    if (ws === 'tracker') {
      renderKanbanBoard();
      renderTimelineView();
      loadTrackerReminders();
    }
  }

  function switchMatcherMode(mode) {
    const isStu = mode === 'student';
    document.getElementById('studentMatcherForm').classList.toggle('hidden', !isStu);
    document.getElementById('researcherMatcherForm').classList.toggle('hidden', isStu);
    document.getElementById('matchModeStudent').className = isStu
      ? 'px-3 py-1.5 text-xs font-bold border-2 border-ink bg-ink text-accent'
      : 'px-3 py-1.5 text-xs font-bold border-2 border-ink bg-white hover:bg-sand';
    document.getElementById('matchModeResearcher').className = !isStu
      ? 'px-3 py-1.5 text-xs font-bold border-2 border-ink bg-ink text-accent'
      : 'px-3 py-1.5 text-xs font-bold border-2 border-ink bg-white hover:bg-sand';
  }

  async function runStudentEligibilityMatch() {
    const out = document.getElementById('matcherResultsContainer');
    out.innerHTML = '<div class="p-6 font-mono text-xs animate-pulse">Evaluating live opportunities against your student profile...</div>';
    const payload = {
      full_name: document.getElementById('smName').value.trim() || 'Student',
      gender: document.getElementById('smGender').value,
      state_domicile: document.getElementById('smState').value,
      education_level: document.getElementById('smEdu').value,
      social_category: document.getElementById('smCategory').value,
      family_annual_income_inr: parseFloat(document.getElementById('smIncome').value || '0'),
      academic_percentage: parseFloat(document.getElementById('smPct').value || '0') || null,
      is_single_girl_child: document.getElementById('smSingleGirl').checked,
      is_differently_abled_pwd: document.getElementById('smPwd').checked,
      top_k: 12
    };
    try {
      const res = await fetch('/api/student/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const results = await res.json();
      if (!results.length) {
        out.innerHTML = '<div class="nb-card p-6 text-xs text-neutral-600">No matching student opportunities found in the current live dataset.</div>';
        return;
      }
      out.innerHTML = `<div class="space-y-3 text-left">` + results.map(r => {
        const badgeCls = r.eligibility_status === 'ELIGIBLE'
          ? 'bg-forest text-white'
          : (r.eligibility_status === 'HIGH_PROBABILITY' ? 'bg-accent text-ink' : 'bg-vermilion text-white');
        const statusLabels = { ELIGIBLE: 'Eligible', HIGH_PROBABILITY: 'Strong Match', INELIGIBLE: 'Not Eligible' };
        const friendlyStatus = statusLabels[r.eligibility_status] || r.eligibility_status;
        const reasons = (r.match_reasons || []).slice(0, 3).map(x => `<li class="text-[11px] text-neutral-700">${escapeHtml(x)}</li>`).join('');
        const disq = (r.disqualifying_conditions || []).slice(0, 2).map(x => `<li class="text-[11px] text-vermilion font-medium">${escapeHtml(x)}</li>`).join('');
        return `
          <div class="nb-card p-4 space-y-2">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-1.5">
                <span class="px-2 py-0.5 text-[10px] font-mono font-bold border border-ink ${badgeCls}">${escapeHtml(friendlyStatus)}</span>
                <span class="px-2 py-0.5 text-[10px] font-mono font-bold bg-cream border border-ink">${Math.round(r.match_percentage || 0)}% Fit</span>
              </div>
              <span class="text-[11px] font-mono text-neutral-500">${escapeHtml(r.foa.agency)}</span>
            </div>
            <h4 class="font-display font-bold text-sm text-ink">${escapeHtml(r.foa.title)}</h4>
            <p class="text-xs text-neutral-600 line-clamp-2">${escapeHtml(r.foa.brief_summary)}</p>
            <ul class="space-y-0.5">${reasons}${disq}</ul>
            <div class="pt-2 border-t border-neutral-200 flex flex-wrap items-center justify-between gap-2">
              <span class="text-[11px] font-mono font-semibold text-neutral-700">💰 ${escapeHtml(r.foa.financials?.raw_budget_text || 'See official notice')}</span>
              <div class="flex items-center gap-1.5">
                <button onclick="openDraftModalForFoa('${escapeHtml(r.foa.foa_id)}', '${escapeHtml(r.foa.title).replace(/'/g, '')}')" class="px-2.5 py-1 text-[11px] font-bold border-2 border-ink bg-accent hover:bg-ink hover:text-accent">Draft SOP / Proposal</button>
                <a href="${escapeHtml(r.foa.direct_apply_url || r.foa.source_url)}" target="_blank" rel="noopener noreferrer" class="nb-btn px-3 py-1 bg-ink text-white text-[11px] font-bold">Apply ↗</a>
              </div>
            </div>
          </div>
        `;
      }).join('') + `</div>`;
      showToast(`Found ${results.length} matching opportunities for your profile!`, 'success');
    } catch (e) {
      out.innerHTML = `<div class="nb-card p-5 text-vermilion text-xs font-semibold">Could not check eligibility right now. Please try again.</div>`;
    }
  }

  async function runResearcherGrantMatch() {
    const out = document.getElementById('matcherResultsContainer');
    out.innerHTML = '<div class="p-6 font-mono text-xs animate-pulse">Finding matching research grants for your profile...</div>';
    const payload = {
      researcher_name: document.getElementById('rmName').value.trim() || 'Dr. Principal Investigator',
      highest_degree: document.getElementById('rmDegree').value.trim() || 'Ph.D.',
      institution_name: document.getElementById('rmInst').value.trim() || 'University',
      applicant_age: parseInt(document.getElementById('rmAge').value || '35', 10) || null,
      research_summary: document.getElementById('rmSummary').value.trim() || 'AI and scientific research',
      top_k: 10
    };
    try {
      const res = await fetch('/api/match-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Request failed');
      const results = await res.json();
      if (!results.length) {
        out.innerHTML = '<div class="nb-card p-6 text-xs text-neutral-600">No matching research grants found.</div>';
        return;
      }
      out.innerHTML = `<div class="space-y-3 text-left">` + results.map(m => {
        const st = m.compliance?.status || 'ELIGIBLE';
        const badgeCls = st === 'ELIGIBLE' ? 'bg-forest text-white' : (st === 'WARNING' ? 'bg-accent text-ink' : 'bg-vermilion text-white');
        const stLabels = { ELIGIBLE: 'Eligible', WARNING: 'Check Criteria', INELIGIBLE: 'Not Eligible' };
        const friendlySt = stLabels[st] || st;
        const kws = (m.matching_keywords || []).slice(0, 4).map(k => `<span class="px-1.5 py-0.5 bg-cream border border-ink/50 font-mono text-[10px]">${escapeHtml(k)}</span>`).join('');
        return `
          <div class="nb-card p-4 space-y-2">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-1.5">
                <span class="px-2 py-0.5 text-[10px] font-mono font-bold border border-ink ${badgeCls}">${escapeHtml(friendlySt)}</span>
                <span class="px-2 py-0.5 text-[10px] font-mono font-bold bg-cream border border-ink">${(m.relevance_score * 100).toFixed(0)}% Match</span>
                <span class="text-[10px] font-mono text-cobalt font-semibold">${escapeHtml(m.deadline_status || 'OPEN')}</span>
              </div>
              <span class="text-[11px] font-mono text-neutral-500">${escapeHtml(m.foa.agency)}</span>
            </div>
            <h4 class="font-display font-bold text-sm text-ink">${escapeHtml(m.foa.title)}</h4>
            <p class="text-xs text-neutral-700 leading-relaxed">${escapeHtml(m.explanation?.why_grant_matches || m.foa.brief_summary)}</p>
            <div class="flex flex-wrap gap-1">${kws}</div>
            <div class="pt-2 border-t border-neutral-200 flex flex-wrap items-center justify-between gap-2">
              <span class="text-[11px] font-mono font-semibold text-neutral-700">💰 ${escapeHtml(m.foa.financials?.raw_budget_text || 'See call ceiling')}</span>
              <div class="flex items-center gap-1.5">
                <button onclick="openDraftModalForFoa('${escapeHtml(m.foa.foa_id)}', '${escapeHtml(m.foa.title).replace(/'/g, '')}')" class="px-2.5 py-1 text-[11px] font-bold border-2 border-ink bg-accent hover:bg-ink hover:text-accent">📝 Draft Proposal</button>
                <a href="${escapeHtml(m.foa.direct_apply_url || m.foa.source_url)}" target="_blank" rel="noopener noreferrer" class="nb-btn px-3 py-1 bg-ink text-white text-[11px] font-bold">Official Call ↗</a>
              </div>
            </div>
          </div>
        `;
      }).join('') + `</div>`;
      showToast(`Found ${results.length} matching research grants!`, 'success');
    } catch (e) {
      out.innerHTML = `<div class="nb-card p-5 text-vermilion text-xs font-semibold">Could not match research grants right now. Please try again.</div>`;
    }
  }

  async function runResumeSemanticMatch() {
    const fileInp = document.getElementById('resumeFile');
    const rawTxt = document.getElementById('resumeRawText').value.trim();
    const cat = document.getElementById('resumeCatFilter').value;
    if ((!fileInp.files || !fileInp.files.length) && !rawTxt) {
      showToast('Upload a resume file or paste resume text first.', 'warning');
      return;
    }
    const out = document.getElementById('matcherResultsContainer');
    out.innerHTML = '<div class="p-6 font-mono text-xs animate-pulse">Analyzing your resume and finding best matches...</div>';

    const fd = new FormData();
    if (fileInp.files && fileInp.files.length) fd.append('file', fileInp.files[0]);
    if (rawTxt) fd.append('raw_text', rawTxt);
    fd.append('category', cat);
    fd.append('top_k', '10');

    try {
      const res = await fetch('/api/resume/match', { method: 'POST', body: fd });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      const skillsHtml = (data.detected_skills || []).map(s => `<span class="px-2 py-0.5 bg-accent/70 border border-ink font-mono text-[10px] font-bold">${escapeHtml(s)}</span>`).join('');
      const headerHtml = `
        <div class="nb-card p-4 bg-cream/70 text-left space-y-2">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="font-display font-bold text-sm">Your Resume Profile</span>
            <span class="font-mono text-[11px] font-bold text-cobalt">${escapeHtml(data.detected_degree)} · ${(data.detected_domains || []).join(', ')}</span>
          </div>
          ${skillsHtml ? `<div class="flex flex-wrap gap-1">${skillsHtml}</div>` : '<div class="text-[11px] text-neutral-500">General academic profile detected.</div>'}
        </div>
      `;

      const cardsHtml = (data.matches || []).map(m => {
        const opp = m.opportunity;
        const matchedChips = (m.matched_skills || []).map(s => `<span class="px-1.5 py-0.5 bg-forest/15 text-forest border border-forest/40 font-mono text-[10px] font-bold">✓ ${escapeHtml(s)}</span>`).join('');
        const gapChips = (m.missing_prerequisites || []).map(g => `<li class="text-[11px] text-vermilion">⚠ ${escapeHtml(g)}</li>`).join('');
        return `
          <div class="nb-card p-4 text-left space-y-2">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-1.5">
                <span class="px-2 py-0.5 bg-ink text-accent font-mono text-[10px] font-bold border border-ink">${m.fit_score}% Fit</span>
                <span class="px-2 py-0.5 bg-cream border border-ink font-mono text-[10px] font-bold">${escapeHtml(opp.category)}</span>
                <span class="text-[10px] font-mono text-neutral-500">${escapeHtml(opp.source_domain)}</span>
              </div>
              <span class="text-[11px] font-mono font-semibold text-cobalt">${opp.deadline ? escapeHtml(opp.deadline) : 'Rolling'}</span>
            </div>
            <h4 class="font-display font-bold text-sm text-ink">${escapeHtml(opp.title)}</h4>
            <p class="text-xs text-neutral-600">${escapeHtml(m.match_summary)}</p>
            ${matchedChips ? `<div class="flex flex-wrap gap-1">${matchedChips}</div>` : ''}
            ${gapChips ? `<ul class="space-y-0.5">${gapChips}</ul>` : ''}
            <div class="pt-2 border-t border-neutral-200 flex items-center justify-between gap-2">
              <span class="text-[11px] font-mono font-semibold">💰 ${escapeHtml(opp.stipend_or_amount)}</span>
              <div class="flex items-center gap-1.5">
                <button onclick="openDraftModalForFoa('${escapeHtml(opp.id)}', '${escapeHtml(opp.title).replace(/'/g, '')}')" class="px-2.5 py-1 text-[11px] font-bold border-2 border-ink bg-white hover:bg-accent">Draft SOP</button>
                <a href="${escapeHtml(opp.source_url)}" target="_blank" rel="noopener noreferrer" class="nb-btn px-3 py-1 bg-ink text-white text-[11px] font-bold">Apply ↗</a>
              </div>
            </div>
          </div>
        `;
      }).join('');

      out.innerHTML = `<div class="space-y-3">${headerHtml}${cardsHtml || '<div class="nb-card p-5 text-xs">No matching opportunities found for this filter.</div>'}</div>`;
      showToast(`Found ${(data.matches || []).length} opportunities matching your resume!`, 'success');
    } catch (e) {
      out.innerHTML = `<div class="nb-card p-5 text-vermilion text-xs font-semibold">Could not analyze your resume right now. Please try again.</div>`;
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

  let pendingDomainFromUrl = null;
  let pendingFundingFromUrl = null;

  function restoreFiltersFromUrl() {
    const sp = new URLSearchParams(window.location.search);
    if (sp.get('category')) selectedCategory = sp.get('category');
    if (sp.get('source_type')) selectedSourceType = sp.get('source_type');
    if (sp.get('q')) {
      document.getElementById('filterSearch').value = sp.get('q');
      document.getElementById('clearSearchBtn').classList.remove('hidden');
    }
    if (sp.get('degree_level')) document.getElementById('filterDegree').value = sp.get('degree_level');
    if (sp.get('deadline_window')) document.getElementById('filterDeadline').value = sp.get('deadline_window');
    if (sp.get('sort')) document.getElementById('filterSort').value = sp.get('sort');
    if (sp.get('domain')) pendingDomainFromUrl = sp.get('domain');
    if (sp.get('funding_type')) pendingFundingFromUrl = sp.get('funding_type');

    document.querySelectorAll('.stype-pill').forEach(btn => {
      const active = btn.getAttribute('data-stype') === selectedSourceType;
      btn.className = active
        ? 'stype-pill px-3 py-1.5 border-2 border-ink bg-ink text-accent font-semibold'
        : 'stype-pill px-3 py-1.5 border-2 border-ink bg-white hover:bg-sand font-semibold';
    });
    document.querySelectorAll('.cat-pill').forEach(btn => {
      const active = btn.getAttribute('data-cat') === selectedCategory;
      btn.className = active
        ? 'cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-accent text-ink'
        : 'cat-pill px-3 py-2 text-xs font-semibold border-2 border-ink bg-white hover:bg-sand';
    });
    if (pendingDomainFromUrl || pendingFundingFromUrl || sp.get('degree_level') || sp.get('deadline_window')) {
      document.getElementById('advancedFiltersRow').classList.remove('hidden');
    }
  }

  function syncFiltersToUrl(params) {
    const cleanParams = new URLSearchParams(params.toString());
    if (cleanParams.get('sort') === 'deadline_asc') cleanParams.delete('sort');
    const qs = cleanParams.toString();
    const newUrl = qs ? `${window.location.pathname}?${qs}` : window.location.pathname;
    window.history.replaceState(null, '', newUrl);
    const csvLink = document.getElementById('exportCsvLink');
    if (csvLink) {
      csvLink.href = qs ? `/api/opportunities/export.csv?${params.toString()}` : '/api/opportunities/export.csv';
    }
  }

  async function copyShareableFilterUrl() {
    try {
      await navigator.clipboard.writeText(window.location.href);
      showToast('Shareable filtered link copied to clipboard!', 'success');
    } catch (e) {
      showToast('URL updated in your address bar — copy it to share.', 'info');
    }
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
    let needsRefetch = false;
    if (pendingDomainFromUrl) {
      domSel.value = pendingDomainFromUrl;
      pendingDomainFromUrl = null;
      needsRefetch = true;
    }
    if (pendingFundingFromUrl) {
      ftSel.value = pendingFundingFromUrl;
      pendingFundingFromUrl = null;
      needsRefetch = true;
    }
    if (needsRefetch) fetchOpportunities();
  }

  async function updateStatsCounters() {
    try {
      const res = await fetch('/api/stats');
      if (res.ok) {
        const s = await res.json();
        const sb = s.source_type_breakdown || {};
        document.getElementById('statAll').innerText = s.total_opportunities || 0;
        document.getElementById('statGovt').innerText = sb['Government'] || 0;
        document.getElementById('statCompany').innerText = sb['Company / Corporate'] || 0;
        document.getElementById('statFound').innerText = sb['Foundation / University'] || 0;
      }
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
    syncFiltersToUrl(params);

    try {
      const res = await fetch(`/api/opportunities?${params.toString()}`);
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      populateFacets(data.facets);
      allFetchedItems = data.items || [];
      lastTotalInStore = data.total_in_store || 0;
      visibleCount = 18;

      document.getElementById('resultsSummaryText').innerHTML =
        `Showing <strong class="text-ink">${allFetchedItems.length}</strong> of ${data.total_in_store} verified opportunities`;
      document.getElementById('cacheStatusLabel').innerText = data.last_refreshed_at
        ? `Updated ${formatRelativeTime(data.last_refreshed_at)}`
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
          <h3 class="font-display font-bold text-lg">Unable to Load Opportunities</h3>
          <p class="text-xs text-neutral-600">We couldn't load listings right now. Please try again in a moment.</p>
          <button onclick="fetchOpportunities()" class="nb-btn px-4 py-2 bg-ink text-accent text-xs font-bold">Retry</button>
        </div>
      `;
      showToast('Could not load opportunities right now.', 'error');
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
              ? 'No opportunities loaded yet. Click "Refresh Live Data" to check official portals.'
              : 'No opportunities match your current filters.'}
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
              <button onclick="toggleSaveOpportunity(${idx})" class="px-2 py-1.5 text-[11px] font-bold border-2 border-ink ${isOppSaved(opp.id) ? 'bg-accent text-ink' : 'bg-white hover:bg-sand text-neutral-700'}" title="Save to My Tracker">
                ${isOppSaved(opp.id) ? '★ Saved' : '+ Save'}
              </button>
              <button onclick="openDetailModal(${idx})" class="px-2.5 py-1.5 text-[11px] font-semibold border-2 border-ink bg-cream hover:bg-sand" title="View details & requirements">Details</button>
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
          ✓ Official link verified (${formatRelativeTime(opp.last_verified_at)})
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <button id="deepAnalyzeBtn" onclick="runDeepPageAnalysis('${escapeHtml(opp.id)}')" class="nb-btn px-3 py-1.5 bg-accent text-ink hover:bg-ink hover:text-accent text-xs font-bold inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[15px]">article</span>
            <span>Summarize Requirements</span>
          </button>
          <button id="draftProposalBtn" onclick="runProposalDraft('${escapeHtml(opp.id)}')" class="nb-btn px-3 py-1.5 bg-white text-ink hover:bg-cobalt hover:text-white text-xs font-bold inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[15px]">edit_note</span>
            <span>Draft Proposal / SOP</span>
          </button>
        </div>
      </div>
      <div id="deepAnalysisContainer" class="hidden pt-2"></div>
      <div id="proposalDraftContainer" class="hidden pt-2"></div>
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
      btn.innerHTML = '<span class="material-symbols-outlined text-[15px] animate-spin">sync</span><span>Reading Official Details...</span>';
    }
    box.classList.remove('hidden');
    box.innerHTML = '<div class="p-3.5 bg-cream border-2 border-ink font-mono text-xs animate-pulse">Reading the official listing and summarizing key requirements...</div>';

    try {
      const res = await fetch(`/api/opportunities/${encodeURIComponent(oppId)}/deep-analyze`, { method: 'POST' });
      if (!res.ok) throw new Error('Request failed');
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
      const sourceLabel = d.is_pdf_parsed ? 'PDF Circular' : 'Official Source';

      box.innerHTML = `
        <div class="p-4 bg-sand/70 border-2 border-ink space-y-3 text-xs">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-ink/20 pb-2">
            <span class="font-display font-bold text-sm text-ink">Requirements &amp; Application Summary</span>
            <span class="px-2 py-0.5 bg-ink text-accent font-mono text-[10px] font-bold">${sourceLabel}</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div class="p-2.5 bg-white border border-ink">
              <span class="text-[10px] font-mono text-neutral-500 block">STIPEND / AWARD</span>
              <strong class="text-ink">${escapeHtml(d.extracted_financials)}</strong>
            </div>
            <div class="p-2.5 bg-white border border-ink">
              <span class="text-[10px] font-mono text-neutral-500 block">DEADLINE</span>
              <strong class="text-ink">${escapeHtml(deadlineDisplay)}</strong>
            </div>
          </div>
          ${d.key_excerpt ? `<p class="text-[11px] text-neutral-700 bg-white/80 p-2 border border-ink/30 leading-relaxed">${escapeHtml(d.key_excerpt)}</p>` : ''}
          <div>
            <span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Eligibility &amp; Key Guidelines</span>
            <ul class="space-y-1 text-neutral-800">${eligHtml}</ul>
          </div>
          <div>
            <span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Required Documents Checklist</span>
            <div class="flex flex-wrap gap-1.5">${docsHtml}</div>
          </div>
          ${pdfLinksHtml ? `<div><span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Official Guidelines &amp; Attachments</span><div class="flex flex-wrap gap-1.5">${pdfLinksHtml}</div></div>` : ''}
          <div>
            <span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Application Steps</span>
            <ol class="space-y-1 text-neutral-800">${stepsHtml}</ol>
          </div>
        </div>
      `;
      showToast('Requirements summary ready.', 'success');
    } catch (err) {
      box.innerHTML = `<div class="p-3 bg-red-50 border-2 border-vermilion text-vermilion text-xs font-semibold">Could not read details from the official page right now. Try opening the official link directly.</div>`;
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[15px]">check_circle</span><span>Refresh Summary</span>';
      }
    }
  }

  let lastDraftPlainText = '';

  async function runProposalDraft(oppId) {
    const btn = document.getElementById('draftProposalBtn');
    const box = document.getElementById('proposalDraftContainer');
    if (!box) return;
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span class="material-symbols-outlined text-[15px] animate-spin">sync</span><span>Drafting...</span>';
    }
    box.classList.remove('hidden');
    box.innerHTML = '<div class="p-3.5 bg-cream border-2 border-ink font-mono text-xs animate-pulse">Preparing your proposal outline and checklist...</div>';

    try {
      const res = await fetch(`/api/foas/${encodeURIComponent(oppId)}/draft-proposal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      if (!res.ok) throw new Error('Request failed');
      const d = await res.json();
      const sections = (d.sections || []).slice(0, 5);
      lastDraftPlainText = (d.sections || []).map(s => `${s.section_title}\n${s.drafted_content}`).join('\n\n');
      const secHtml = sections.map(s => `
        <div class="p-2.5 bg-white border border-ink space-y-1">
          <div class="font-display font-bold text-xs text-ink">${escapeHtml(s.section_title)}</div>
          <div class="text-[11px] text-neutral-700 whitespace-pre-line leading-relaxed">${escapeHtml(s.drafted_content)}</div>
        </div>
      `).join('');
      const chkHtml = (d.compliance_checklist || []).slice(0, 4).map(c => `<li class="text-[11px]">✓ ${escapeHtml(c)}</li>`).join('');

      box.innerHTML = `
        <div class="p-4 bg-cream border-2 border-ink space-y-3 text-xs">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-ink/20 pb-2">
            <span class="font-display font-bold text-sm text-ink">Draft Proposal / SOP Outline (${(d.sections || []).length} Sections)</span>
            <button onclick="copyDraftToClipboard()" class="px-2.5 py-1 bg-ink text-accent border border-ink font-mono text-[10px] font-bold hover:bg-accent hover:text-ink">Copy Full Draft</button>
          </div>
          <div class="space-y-2">${secHtml}</div>
          <div>
            <span class="text-[10px] font-mono font-bold uppercase text-neutral-600 block mb-1">Key Checklist</span>
            <ul class="space-y-0.5 text-neutral-800">${chkHtml}</ul>
          </div>
        </div>
      `;
      showToast('Draft outline ready!', 'success');
    } catch (err) {
      box.innerHTML = `<div class="p-3 bg-red-50 border-2 border-vermilion text-vermilion text-xs font-semibold">Could not prepare the draft right now. Please try again.</div>`;
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[15px]">edit_note</span><span>Regenerate Draft</span>';
      }
    }
  }

  async function copyDraftToClipboard() {
    if (!lastDraftPlainText) return;
    try {
      await navigator.clipboard.writeText(lastDraftPlainText);
      showToast('Full draft copied to clipboard!', 'success');
    } catch (e) {
      showToast('Copy failed — select and copy text manually.', 'warning');
    }
  }

  function openDraftModalForFoa(foaId, title) {
    const idx = allFetchedItems.findIndex(o => o.id === foaId);
    if (idx >= 0) {
      openDetailModal(idx);
      runProposalDraft(foaId);
      return;
    }
    currentModalOpp = { id: foaId, title: title || foaId };
    document.getElementById('dmBadges').innerHTML = '<span class="px-2 py-0.5 text-[10px] font-mono font-bold uppercase border border-ink bg-accent">Draft Outline</span>';
    document.getElementById('dmTitle').innerText = title || foaId;
    document.getElementById('dmOrg').innerText = 'Proposal & SOP Assistant';
    document.getElementById('dmBody').innerHTML = '<div id="proposalDraftContainer"></div>';
    document.getElementById('dmCal').href = `/api/foas/${encodeURIComponent(foaId)}/calendar`;
    document.getElementById('dmApply').href = '#';
    document.getElementById('detailModal').classList.remove('hidden');
    runProposalDraft(foaId);
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
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}`);
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
        const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ opp_id: opp.id, stage: 'Saved' })
        });
        if (!res.ok) throw new Error('Save failed');
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
        const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ opp_id: currentModalOpp.id, stage: 'Saved' })
        });
        if (!res.ok) throw new Error('Save failed');
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
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/${encodeURIComponent(oppId)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage: newStage })
      });
      if (!res.ok) throw new Error('Move failed');
      const data = await res.json();
      kanbanItems = data.items || [];
      updateTrackerBadge();
      renderKanbanBoard();
      renderTimelineView();
      showToast(`Moved to "${newStage}"`, 'info');
    } catch (e) {
      showToast('Failed to update stage.', 'error');
    }
  }

  async function saveKanbanNote(oppId, stage, noteText) {
    try {
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/${encodeURIComponent(oppId)}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage, notes: noteText })
      });
      if (!res.ok) throw new Error('Note save failed');
      const data = await res.json();
      kanbanItems = data.items || [];
      showToast('Note saved to tracker.', 'success');
    } catch (e) {
      showToast('Could not save note.', 'error');
    }
  }

  async function removeKanbanItem(oppId) {
    try {
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/${encodeURIComponent(oppId)}`, {
        method: 'DELETE'
      });
      if (!res.ok) throw new Error('Delete failed');
      const data = await res.json();
      kanbanItems = data.items || [];
      updateTrackerBadge();
      renderKanbanBoard();
      renderTimelineView();
      renderVisibleCards(lastTotalInStore);
      showToast('Removed from tracker.', 'info');
    } catch (e) {
      showToast('Failed to remove item.', 'error');
    }
  }

  let trackerViewMode = 'kanban';
  let trackerReminders = [];

  function switchTrackerView(mode) {
    trackerViewMode = mode;
    const isKanban = mode === 'kanban';
    document.getElementById('kanbanBoardGrid').classList.toggle('hidden', !isKanban);
    document.getElementById('timelineBoardView').classList.toggle('hidden', isKanban);
    document.getElementById('trackerModeKanban').className = isKanban
      ? 'px-3 py-1.5 text-xs font-bold bg-ink text-accent'
      : 'px-3 py-1.5 text-xs font-bold bg-white text-ink hover:bg-sand';
    document.getElementById('trackerModeTimeline').className = !isKanban
      ? 'px-3 py-1.5 text-xs font-bold bg-ink text-accent'
      : 'px-3 py-1.5 text-xs font-bold bg-white text-ink hover:bg-sand';
    if (!isKanban) renderTimelineView();
  }

  function renderTimelineView() {
    const el = document.getElementById('timelineBoardView');
    if (!el) return;
    if (!kanbanItems.length) {
      el.innerHTML = '<div class="nb-card p-8 text-center text-xs text-neutral-500">Save opportunities to see them plotted on your chronological deadline timeline.</div>';
      return;
    }
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const enriched = kanbanItems.map(item => {
      let days = 9999;
      if (item.deadline) {
        days = Math.ceil((new Date(item.deadline + 'T00:00:00') - today) / 86400000);
      }
      return { ...item, days };
    }).sort((a, b) => a.days - b.days);

    el.innerHTML = enriched.map(item => {
      const urgCls = item.days <= 7 ? 'bg-vermilion text-white' : (item.days <= 30 ? 'bg-accent text-ink' : 'bg-cobalt text-white');
      const urgLbl = item.deadline ? (item.days <= 0 ? 'Closes Today' : `${item.days}d left · ${item.deadline}`) : 'Rolling / Ongoing';
      return `
        <div class="nb-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="flex items-start gap-3">
            <span class="px-2.5 py-1 text-[11px] font-mono font-bold border border-ink shrink-0 ${urgCls}">${escapeHtml(urgLbl)}</span>
            <div>
              <a href="${escapeHtml(item.source_url)}" target="_blank" rel="noopener noreferrer" class="font-display font-bold text-sm text-ink hover:text-cobalt">${escapeHtml(item.title)} ↗</a>
              <div class="text-xs text-neutral-600">${escapeHtml(item.organization)} · <span class="font-mono">${escapeHtml(item.stage)}</span>${item.notes ? ` · 📝 ${escapeHtml(item.notes)}` : ''}</div>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <select onchange="moveKanbanStage('${escapeHtml(item.opp_id)}', this.value)" class="bg-cream border-2 border-ink px-2 py-1 text-xs font-semibold">
              ${KANBAN_STAGES.map(s => `<option value="${s}" ${s === item.stage ? 'selected' : ''}>${s}</option>`).join('')}
            </select>
            <button onclick="removeKanbanItem('${escapeHtml(item.opp_id)}')" class="px-2 py-1 border-2 border-ink bg-white hover:bg-vermilion hover:text-white text-xs font-bold">✕</button>
          </div>
        </div>
      `;
    }).join('');
  }

  async function loadTrackerReminders() {
    try {
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/reminders`);
      if (!res.ok) return;
      const data = await res.json();
      trackerReminders = data.reminders || [];
      renderRemindersList(data.due_alerts || []);
    } catch (e) {}
  }

  async function addTrackerReminder() {
    const channel = document.getElementById('remChannel').value;
    const target = document.getElementById('remTarget').value.trim() || (channel === 'browser' ? 'In-App Browser Alert' : '');
    const lead_days = parseInt(document.getElementById('remLeadDays').value || '7', 10);
    if (!target) { showToast('Enter a webhook URL or email address.', 'warning'); return; }
    if (channel === 'browser' && typeof Notification !== 'undefined' && Notification.permission === 'default') {
      try { await Notification.requestPermission(); } catch (e) {}
    }
    try {
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/reminders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ channel, target, lead_days })
      });
      if (!res.ok) throw new Error('Save failed');
      const data = await res.json();
      trackerReminders = data.reminders || [];
      document.getElementById('remTarget').value = '';
      renderRemindersList(data.due_alerts || []);
      showToast(`Reminder set for ${lead_days} days before deadline.`, 'success');
    } catch (e) { showToast('Could not save reminder.', 'error'); }
  }

  async function deleteTrackerReminder(remId) {
    try {
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/reminders/${remId}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      trackerReminders = data.reminders || [];
      renderRemindersList([]);
      showToast('Reminder removed.', 'info');
    } catch (e) {}
  }

  async function dispatchTrackerReminders() {
    try {
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/reminders/dispatch`, { method: 'POST' });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      const list = data.dispatched || [];
      if (!list.length) {
        showToast('Add a reminder above first to check upcoming deadlines.', 'warning');
        return;
      }
      const totalDue = list.reduce((acc, x) => acc + (x.due_count || 0), 0);
      if (totalDue > 0 && typeof Notification !== 'undefined' && Notification.permission === 'granted') {
        const bItem = list.find(x => x.channel === 'browser' && x.due_count > 0);
        if (bItem) {
          try { new Notification('MadadgaarAI Deadline Alert', { body: bItem.preview }); } catch (e) {}
        }
      }
      showToast(
        totalDue > 0 ? `${totalDue} saved deadline(s) closing soon.` : 'All caught up — no urgent deadlines right now.',
        totalDue > 0 ? 'warning' : 'success'
      );
    } catch (e) { showToast('Could not check reminders right now.', 'error'); }
  }

  function renderRemindersList(dueAlerts) {
    const box = document.getElementById('trackerRemindersList');
    if (!box) return;
    const pills = trackerReminders.map(r => `
      <span class="px-2.5 py-1 bg-white border border-ink font-mono text-[11px] inline-flex items-center gap-1.5">
        <strong>${escapeHtml(r.channel.toUpperCase())}</strong> (${r.lead_days}d): ${escapeHtml(r.target.slice(0, 32))}
        <button onclick="deleteTrackerReminder(${r.id})" class="text-vermilion font-bold ml-1">✕</button>
      </span>
    `).join('');
    const dueBadge = (dueAlerts && dueAlerts.length)
      ? `<span class="px-2.5 py-1 bg-vermilion text-white border border-ink font-mono text-[11px] font-bold">⏰ ${dueAlerts.length} closing soon</span>`
      : '';
    box.innerHTML = pills + dueBadge;
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
    if (label) label.innerText = 'Updating...';
    renderSkeletons(6);
    showToast('Checking official portals for the latest opportunities...', 'info');

    try {
      const res = await fetch('/api/opportunities/refresh?force=true', { method: 'POST' });
      if (!res.ok) throw new Error('Request failed');
      const report = await res.json();
      facetsInitialized = false;
      document.getElementById('filterDomain').innerHTML = '<option value="All">All Domains</option>';
      document.getElementById('filterFundingType').innerHTML = '<option value="All">All Types</option>';
      await updateStatsCounters();
      await fetchOpportunities();
      showToast(
        `Updated! ${report.total_live_opportunities} active opportunities available.`,
        report.source_errors && report.source_errors.length > 0 ? 'warning' : 'success'
      );
    } catch (err) {
      showToast('Could not update opportunities right now. Please try again.', 'error');
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
    const niceDocType = String(data.document_type || 'Document')
      .replace(/_/g, ' ')
      .toLowerCase()
      .replace(/\b\w/g, c => c.toUpperCase());
    const fields = (data.extracted_fields || []).map(f =>
      `<div class="p-2 bg-cream border border-ink flex justify-between gap-2 font-mono text-[11px]"><span><strong>${escapeHtml(f.field_name)}:</strong> ${escapeHtml(f.extracted_value || 'Missing')}</span><span class="font-bold">${escapeHtml(f.status)}</span></div>`
    ).join('');
    out.innerHTML = `
      <div class="font-display font-bold text-cobalt text-sm">${escapeHtml(niceDocType)}</div>
      <div class="space-y-1.5">${fields}</div>
      <div class="p-2 bg-accent/60 border border-ink text-[10px] font-medium">${escapeHtml(data.authenticity_disclaimer)}</div>
    `;
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeDetailModal();
      closeAuthModal();
      closeCitationModal();
    }
  });

  // =================================================================
  // Account Sign-In, Study Mode Switcher & Personal Study Assistant
  // =================================================================
  let authConfig = null;
  let currentUser = null;
  let activePrivateSessionId = null;
  let docPollTimer = null;

  function openAuthModal() {
    document.getElementById('authModal').classList.remove('hidden');
  }
  function closeAuthModal() {
    document.getElementById('authModal').classList.add('hidden');
  }
  function closeCitationModal() {
    document.getElementById('citationModal').classList.add('hidden');
  }
  function toggleUserDropdown() {
    document.getElementById('authUserDropdown').classList.toggle('hidden');
  }

  function switchAssistantSubmode(mode) {
    const isPriv = mode === 'private';
    document.getElementById('assistantPrivatePanel').classList.toggle('hidden', !isPriv);
    document.getElementById('assistantPublicPanel').classList.toggle('hidden', isPriv);
    document.getElementById('submodePrivateBtn').className = isPriv
      ? 'px-3.5 py-2 text-xs font-bold bg-ink text-accent'
      : 'px-3.5 py-2 text-xs font-bold bg-white text-ink hover:bg-sand';
    document.getElementById('submodePublicBtn').className = !isPriv
      ? 'px-3.5 py-2 text-xs font-bold bg-ink text-accent'
      : 'px-3.5 py-2 text-xs font-bold bg-white text-ink hover:bg-sand';
  }

  function quickPrivateAsk(promptText) {
    const inp = document.getElementById('privateChatInput');
    if (!inp) return;
    inp.value = promptText;
    inp.focus();
    sendPrivateRagStream();
  }

  function applyAuthUIState() {
    const loggedIn = Boolean(currentUser);
    document.getElementById('authSignInBtn').classList.toggle('hidden', loggedIn);
    document.getElementById('authUserMenu').classList.toggle('hidden', !loggedIn);
    document.getElementById('privateAuthGate').classList.toggle('hidden', loggedIn);
    document.getElementById('privateWorkspaceGrid').classList.toggle('hidden', !loggedIn);

    if (loggedIn) {
      activeSessionId = 'user:' + currentUser.id;
      document.getElementById('authUserName').innerText = currentUser.full_name || 'User';
      document.getElementById('authUserAvatar').innerText = (currentUser.full_name || 'U').charAt(0).toUpperCase();
      document.getElementById('authDropName').innerText = currentUser.full_name || '';
      document.getElementById('authDropEmail').innerText = currentUser.email || '';
    } else {
      activeSessionId = anonSessionId;
    }
  }

  async function initAuthAndModes() {
    try {
      const cfgRes = await fetch('/api/auth/config');
      if (cfgRes.ok) {
        authConfig = await cfgRes.json();
        if (!authConfig.google_oauth_code_flow_enabled) {
          document.getElementById('googleOAuthBtn').classList.add('opacity-50', 'pointer-events-none');
          document.getElementById('googleOAuthHint').classList.remove('hidden');
        }
        if (authConfig.google_oauth_code_flow_enabled || !authConfig.dev_auth_allowed) {
          document.getElementById('devLoginSection').classList.add('hidden');
        }
      }
      const meRes = await authFetch('/api/auth/me');
      if (meRes.ok) {
        const me = await meRes.json();
        currentUser = me.user;
        applyAuthUIState();
        await loadPrivateDocuments();
        await loadPrivateSessions();
      } else {
        currentUser = null;
        applyAuthUIState();
      }
    } catch (e) {}
  }

  async function submitDevLogin() {
    const full_name = document.getElementById('devLoginName').value.trim();
    const email = document.getElementById('devLoginEmail').value.trim();
    try {
      const res = await fetch('/api/auth/dev-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, full_name })
      });
      if (!res.ok) throw new Error('Sign-in failed');
      const data = await res.json();
      currentUser = data.user;
      closeAuthModal();
      applyAuthUIState();
      await loadKanbanTracker();
      await loadPrivateDocuments();
      await loadPrivateSessions();
      showToast(`Signed in as ${currentUser.full_name}`, 'success');
    } catch (e) {
      showToast('Sign-in failed. Check your email and try again.', 'error');
    }
  }

  async function logoutUser() {
    try {
      await fetch('/api/auth/logout', { method: 'POST', credentials: 'include' });
    } catch (e) {}
    currentUser = null;
    activePrivateSessionId = null;
    document.getElementById('authUserDropdown').classList.add('hidden');
    applyAuthUIState();
    await loadKanbanTracker();
    renderKanbanBoard();
    renderTimelineView();
    showToast('Signed out.', 'info');
  }

  async function loadPrivateDocuments() {
    if (!currentUser) return;
    try {
      const res = await authFetch('/api/saral/documents');
      if (!res.ok) return;
      const data = await res.json();
      const docs = data.documents || [];
      document.getElementById('privateDocCount').innerText = `${docs.length} doc${docs.length === 1 ? '' : 's'}`;
      const listEl = document.getElementById('privateDocsList');
      if (!docs.length) {
        listEl.innerHTML = '<div class="p-3 border border-dashed border-neutral-300 text-center text-[11px] text-neutral-500">No documents uploaded yet.</div>';
        return;
      }
      const badgeStyles = {
        indexed: 'bg-forest text-white',
        processing: 'bg-cobalt text-white animate-pulse',
        pending: 'bg-accent text-ink',
        failed: 'bg-vermilion text-white'
      };
      const statusText = {
        indexed: 'Ready',
        processing: 'Reading...',
        pending: 'Queued',
        failed: 'Failed'
      };
      const typeLabels = {
        pdf: 'PDF',
        markdown: 'Note',
        text: 'Text',
        url: 'Web Link',
        arxiv: 'Research Paper'
      };
      listEl.innerHTML = docs.map(d => `
        <div class="p-2.5 bg-cream/60 border border-ink flex items-center justify-between gap-2">
          <div class="min-w-0">
            <div class="font-bold text-ink truncate" title="${escapeHtml(d.title)}">${escapeHtml(d.title)}</div>
            <div class="flex items-center gap-1.5 mt-0.5 font-mono text-[10px]">
              <span class="px-1.5 py-0.2 border border-ink font-bold uppercase ${badgeStyles[d.status] || 'bg-sand'}">${escapeHtml(statusText[d.status] || d.status)}</span>
              <span class="text-neutral-600">${escapeHtml(typeLabels[d.source_type] || 'Document')}</span>
            </div>
          </div>
          <button onclick="deletePrivateDocument('${escapeHtml(d.id)}')" class="px-2 py-1 border border-ink bg-white hover:bg-vermilion hover:text-white text-[10px] font-bold shrink-0" title="Remove document">✕</button>
        </div>
      `).join('');

      const anyPending = docs.some(d => d.status === 'pending' || d.status === 'processing');
      clearTimeout(docPollTimer);
      if (anyPending) {
        docPollTimer = setTimeout(loadPrivateDocuments, 1800);
      }
    } catch (e) {}
  }

  async function uploadPrivateDocument() {
    const inp = document.getElementById('privateDocFile');
    if (!inp.files || !inp.files.length) { showToast('Select a PDF, Markdown, or TXT file first.', 'warning'); return; }
    const fd = new FormData();
    fd.append('file', inp.files[0]);
    try {
      const res = await authFetch('/api/saral/documents/upload', { method: 'POST', body: fd });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Upload failed');
      inp.value = '';
      showToast(data.deduplicated ? 'This document is already in your library.' : 'Uploaded! Preparing your document...', 'success');
      await loadPrivateDocuments();
    } catch (e) { showToast('Could not upload this file. Please try again.', 'error'); }
  }

  async function ingestPrivateUrl() {
    const inp = document.getElementById('privateUrlInput');
    const url = inp.value.trim();
    if (!url) return;
    showToast('Adding link to your documents...', 'info');
    try {
      const res = await authFetch('/api/saral/documents/ingest-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Could not add link');
      inp.value = '';
      showToast(`Added "${data.document?.title || 'link'}" to your documents!`, 'success');
      await loadPrivateDocuments();
    } catch (e) { showToast('Could not add that link. Please check the URL and try again.', 'error'); }
  }

  async function deletePrivateDocument(docId) {
    try {
      const res = await authFetch(`/api/saral/documents/${encodeURIComponent(docId)}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Delete failed');
      showToast('Document removed.', 'info');
      await loadPrivateDocuments();
    } catch (e) { showToast('Could not remove document.', 'error'); }
  }

  async function loadPrivateSessions() {
    if (!currentUser) return;
    try {
      const res = await authFetch('/api/saral/sessions');
      if (!res.ok) return;
      const data = await res.json();
      const list = data.sessions || [];
      const el = document.getElementById('privateSessionsList');
      if (!list.length) {
        el.innerHTML = '<div class="text-[11px] text-neutral-500">Ask a question to start saving your chats.</div>';
        return;
      }
      el.innerHTML = list.map(s => `
        <div class="flex items-center gap-1 border border-ink ${s.id === activePrivateSessionId ? 'bg-accent font-bold' : 'bg-cream/50 hover:bg-sand'}">
          <button onclick="openPrivateSession('${escapeHtml(s.id)}')" class="flex-1 min-w-0 text-left px-2.5 py-1.5 flex items-center justify-between gap-2">
            <span class="truncate">${escapeHtml(s.title)}</span>
          </button>
          <button onclick="deletePrivateSession('${escapeHtml(s.id)}')" class="px-2 py-1.5 text-[10px] font-bold text-neutral-500 hover:text-vermilion shrink-0" title="Delete chat">✕</button>
        </div>
      `).join('');
    } catch (e) {}
  }

  async function deletePrivateSession(sid) {
    try {
      const res = await authFetch(`/api/saral/sessions/${encodeURIComponent(sid)}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Delete failed');
      if (activePrivateSessionId === sid) {
        startNewPrivateSession();
      } else {
        await loadPrivateSessions();
      }
      showToast('Chat removed.', 'info');
    } catch (e) { showToast('Could not remove chat.', 'error'); }
  }

  function startNewPrivateSession() {
    activePrivateSessionId = null;
    document.getElementById('privateChatMessages').innerHTML = `
      <div class="p-3.5 bg-white border-2 border-ink text-xs text-neutral-700 leading-relaxed">
        Started a new chat. Ask anything about your uploaded documents.
      </div>
    `;
    loadPrivateSessions();
  }

  async function openPrivateSession(sid) {
    activePrivateSessionId = sid;
    try {
      const res = await authFetch(`/api/saral/sessions/${encodeURIComponent(sid)}/messages`);
      if (!res.ok) return;
      const data = await res.json();
      const box = document.getElementById('privateChatMessages');
      box.innerHTML = '';
      (data.messages || []).forEach(m => {
        if (m.role === 'user') {
          box.insertAdjacentHTML('beforeend', `<div class="flex justify-end"><div class="max-w-[82%] px-3 py-2 bg-ink text-accent border-2 border-ink text-xs font-semibold">${escapeHtml(m.content)}</div></div>`);
        } else {
          const wrap = document.createElement('div');
          wrap.className = 'p-3.5 bg-white border-2 border-ink text-xs sm:text-sm space-y-2';
          wrap.innerHTML = `<div class="private-md-body">${formatMarkdownHtml(m.content)}</div>${renderCitationPillsHtml(m.citations || [])}`;
          box.appendChild(wrap);
          renderMathSafe(wrap);
        }
      });
      box.scrollTop = box.scrollHeight;
      loadPrivateSessions();
    } catch (e) {}
  }

  function formatMarkdownHtml(raw) {
    return escapeHtml(raw || '')
      .replace(/^###\s+(.*)$/gm, '<div class="font-display font-bold text-sm text-ink mt-1">$1</div>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*\n]+)\*/g, '<em class="text-neutral-600">$1</em>')
      .replace(/`([^`\n]+)`/g, '<code class="px-1 py-0.5 bg-sand font-mono text-[11px]">$1</code>')
      .replace(/\n/g, '<br/>');
  }

  function renderMathSafe(el) {
    try {
      if (typeof renderMathInElement === 'function') {
        renderMathInElement(el, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '$', right: '$', display: false }
          ],
          throwOnError: false
        });
      }
    } catch (e) {}
  }

  function renderCitationPillsHtml(citations) {
    if (!citations || !citations.length) return '';
    const pills = citations.map((c, idx) => `
      <button onclick="openCitationChunk('${escapeHtml(c.doc_id)}', '${escapeHtml(c.chunk_id)}')" class="px-2 py-1 bg-cream hover:bg-accent border border-ink font-mono text-[10px] font-bold text-cobalt inline-flex items-center gap-1">
        <span>[${idx + 1}] ${escapeHtml(c.doc_title.slice(0, 26))} · p.${c.page_number}</span>
      </button>
    `).join('');
    return `<div class="pt-2 border-t border-neutral-200 flex flex-wrap gap-1.5">${pills}</div>`;
  }

  async function openCitationChunk(docId, chunkId) {
    try {
      const res = await authFetch(`/api/saral/documents/${encodeURIComponent(docId)}/chunks/${encodeURIComponent(chunkId)}`);
      if (!res.ok) throw new Error('Could not open source');
      const data = await res.json();
      const ch = data.chunk;
      document.getElementById('citMetaBadges').innerHTML = `
        <span class="px-2 py-0.5 bg-accent border border-ink font-mono text-[10px] font-bold">Page ${ch.page_number}</span>
        <span class="px-2 py-0.5 bg-white border border-ink font-mono text-[10px] font-semibold">${escapeHtml(ch.section_header)}</span>
      `;
      document.getElementById('citDocTitle').innerText = ch.doc_title;
      const body = document.getElementById('citChunkBody');
      body.innerText = ch.content;
      renderMathSafe(body);
      document.getElementById('citationModal').classList.remove('hidden');
    } catch (e) {
      showToast('Could not open source passage.', 'error');
    }
  }

  async function sendPrivateRagStream() {
    const inp = document.getElementById('privateChatInput');
    const btn = document.getElementById('privateChatSendBtn');
    const box = document.getElementById('privateChatMessages');
    const query = inp.value.trim();
    if (!query || !currentUser) return;
    inp.value = '';
    btn.disabled = true;

    box.insertAdjacentHTML('beforeend', `<div class="flex justify-end"><div class="max-w-[82%] px-3 py-2 bg-ink text-accent border-2 border-ink text-xs font-semibold">${escapeHtml(query)}</div></div>`);
    const respCard = document.createElement('div');
    respCard.className = 'p-3.5 bg-white border-2 border-ink text-xs sm:text-sm space-y-2';
    respCard.innerHTML = '<div class="private-md-body font-mono text-xs animate-pulse">Thinking...</div><div class="private-cites"></div>';
    box.appendChild(respCard);
    box.scrollTop = box.scrollHeight;

    let accText = '';
    let latestCitations = [];

    try {
      const res = await authFetch('/api/saral/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: activePrivateSessionId })
      });
      if (!res.ok) {
        throw new Error('Response unavailable');
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      const bodyNode = respCard.querySelector('.private-md-body');
      const citesNode = respCard.querySelector('.private-cites');

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split('\n\n');
        buffer = events.pop() || '';
        for (const rawEvt of events) {
          const line = rawEvt.trim();
          if (!line.startsWith('data:')) continue;
          const payload = JSON.parse(line.slice(5).trim());
          if (payload.type === 'meta') {
            if (payload.session_id) activePrivateSessionId = payload.session_id;
            latestCitations = payload.citations || [];
            citesNode.innerHTML = renderCitationPillsHtml(latestCitations);
            bodyNode.className = 'private-md-body leading-relaxed';
          } else if (payload.type === 'delta') {
            accText += payload.text || '';
            bodyNode.innerHTML = formatMarkdownHtml(accText);
            box.scrollTop = box.scrollHeight;
          } else if (payload.type === 'done') {
            renderMathSafe(bodyNode);
          }
        }
      }
      await loadPrivateSessions();
    } catch (e) {
      respCard.innerHTML = `<div class="text-vermilion font-semibold text-xs">Could not generate a response right now. Please try again.</div>`;
    } finally {
      btn.disabled = false;
    }
  }

  (async function init() {
    restoreFiltersFromUrl();
    await initAuthAndModes();
    await loadKanbanTracker();
    await updateStatsCounters();
    await fetchOpportunities();
  })();
</script>
</body>
</html>
"""
