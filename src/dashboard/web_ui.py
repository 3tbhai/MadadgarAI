"""Handcrafted Editorial Web UI for Madadgaar — Scholarships, Internships, Grants & Study Desk."""


def render_dashboard_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>Madadgaar — Scholarships, Internships &amp; Research Grants</title>
  <link href="https://fonts.googleapis.com" rel="preconnect"/>
  <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500&family=Noto+Sans+Devanagari:wght@500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,300,0,0" rel="stylesheet"/>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            paper: "#FAF8F5",
            parchment: "#F2EDE6",
            surface: "#FFFFFF",
            line: "#E5DFD6",
            ink: "#1F1D1A",
            muted: "#6B655E",
            clay: "#B44C2E",
            clayDark: "#943A20",
            claySoft: "#FBF1ED",
            slateBlue: "#2B4C7E",
            slateSoft: "#EEF3FA",
            sage: "#276749",
            sageSoft: "#EDF7F1",
            ochre: "#9A6700",
            ochreSoft: "#FDF6E7",
            crimson: "#B91C1C",
            crimsonSoft: "#FEF2F2",
          },
          fontFamily: {
            serif: ["Newsreader", "Georgia", "serif"],
            sans: ["Plus Jakarta Sans", "system-ui", "-apple-system", "sans-serif"],
            devanagari: ["Noto Sans Devanagari", "sans-serif"],
          }
        }
      }
    }
  </script>
  <style>
    html { scroll-behavior: smooth; }
    body {
      background-color: #FAF8F5;
      color: #1F1D1A;
      background-image: radial-gradient(rgba(120, 108, 94, 0.045) 1px, transparent 0);
      background-size: 24px 24px;
    }
    .paper-card {
      background: #FFFFFF;
      border: 1px solid #E5DFD6;
      border-radius: 12px;
      box-shadow: 0 1px 2px rgba(31, 29, 26, 0.04);
      transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
    }
    .paper-card-hover:hover {
      border-color: #D2C8BB;
      box-shadow: 0 8px 24px rgba(31, 29, 26, 0.06);
      transform: translateY(-1px);
    }
    .btn-primary {
      background: #1F1D1A;
      color: #FAF8F5;
      border-radius: 8px;
      transition: background-color 0.15s ease, transform 0.12s ease;
    }
    .btn-primary:hover { background: #36322D; }
    .btn-primary:active { transform: translateY(1px); }
    .btn-clay {
      background: #B44C2E;
      color: #FFFFFF;
      border-radius: 8px;
      transition: background-color 0.15s ease, transform 0.12s ease;
    }
    .btn-clay:hover { background: #943A20; }
    .btn-clay:active { transform: translateY(1px); }
    .btn-secondary {
      background: #FFFFFF;
      color: #1F1D1A;
      border: 1px solid #DDD6CB;
      border-radius: 8px;
      transition: background-color 0.15s ease, border-color 0.15s ease;
    }
    .btn-secondary:hover { background: #F5F1EB; border-color: #C8BEB0; }
    .field-input {
      background: #FCFBF9;
      border: 1px solid #DDD6CB;
      border-radius: 8px;
      transition: border-color 0.15s ease, background-color 0.15s ease, box-shadow 0.15s ease;
    }
    .field-input:focus {
      outline: none;
      background: #FFFFFF;
      border-color: #B44C2E;
      box-shadow: 0 0 0 3px rgba(180, 76, 46, 0.10);
    }
    .skeleton-pulse {
      background: linear-gradient(90deg, #F0EBE3 25%, #F8F5F0 50%, #F0EBE3 75%);
      background-size: 200% 100%;
      animation: shimmer 1.35s infinite linear;
      border-radius: 6px;
    }
    @keyframes shimmer {
      0% { background-position: 200% 0; }
      100% { background-position: -200% 0; }
    }
  </style>
</head>
<body class="font-sans antialiased min-h-screen flex flex-col selection:bg-claySoft selection:text-clayDark">

<!-- ================= TOASTS ================= -->
<div id="toastContainer" class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none px-4 sm:px-0"></div>

<!-- ================= HEADER ================= -->
<header class="sticky top-0 z-40 bg-paper/95 backdrop-blur-md border-b border-line">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
    <!-- Brand -->
    <button onclick="switchWorkspace('opportunities')" class="flex items-center gap-2.5 text-left group shrink-0">
      <svg class="w-8 h-8 shrink-0" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect x="2" y="2" width="32" height="32" rx="9" fill="#B44C2E"/>
        <path d="M11 25V12.5C11 11.67 11.67 11 12.5 11H15.2L18 16.4L20.8 11H23.5C24.33 11 25 11.67 25 12.5V25" stroke="#FAF8F5" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="18" cy="22.5" r="1.8" fill="#F6D7C9"/>
      </svg>
      <div class="leading-tight">
        <span class="font-serif font-semibold text-xl tracking-tight text-ink block">Madadgaar</span>
        <span class="font-devanagari text-[10px] text-muted hidden sm:block -mt-0.5">मददगार · छात्रवृत्ति एवं शोध</span>
      </div>
    </button>

    <!-- Primary 4-Tab Navigation -->
    <nav class="flex items-center gap-1 sm:gap-2 overflow-x-auto h-full">
      <button id="navOpportunities" onclick="switchWorkspace('opportunities')" class="relative h-full px-2.5 sm:px-3 text-[13px] font-semibold text-clay border-b-2 border-clay inline-flex items-center shrink-0">
        Opportunities
      </button>
      <button id="navMatcher" onclick="switchWorkspace('matcher')" class="relative h-full px-2.5 sm:px-3 text-[13px] font-medium text-muted hover:text-ink border-b-2 border-transparent inline-flex items-center shrink-0">
        Match &amp; Resume
      </button>
      <button id="navTracker" onclick="switchWorkspace('tracker')" class="relative h-full px-2.5 sm:px-3 text-[13px] font-medium text-muted hover:text-ink border-b-2 border-transparent inline-flex items-center gap-1.5 shrink-0">
        <span>My Tracker</span>
        <span id="navTrackerCount" class="px-1.5 py-0.5 rounded-full bg-parchment text-ink text-[11px] font-semibold leading-none">0</span>
      </button>
      <button id="navAssistant" onclick="switchWorkspace('assistant')" class="relative h-full px-2.5 sm:px-3 text-[13px] font-medium text-muted hover:text-ink border-b-2 border-transparent inline-flex items-center shrink-0">
        Saral Desk
      </button>
    </nav>

    <!-- Account, Mode & Refresh -->
    <div class="flex items-center gap-2 shrink-0">
      <select id="headerModeSelect" onchange="handleModeSwitch(this.value)" class="hidden px-2.5 py-1.5 text-xs font-medium rounded-lg border border-line bg-white text-ink cursor-pointer" title="Switch your study mode">
        <option value="student">Student</option>
        <option value="researcher">Researcher</option>
        <option value="educator">Educator</option>
      </select>

      <button id="authSignInBtn" onclick="openAuthModal()" class="btn-secondary px-3 py-1.5 text-xs font-semibold inline-flex items-center gap-1.5" title="Sign in to access your personal study desk">
        <span>Sign in</span>
      </button>

      <div id="authUserMenu" class="hidden relative">
        <button onclick="toggleUserDropdown()" class="btn-secondary px-2.5 py-1.5 text-xs font-medium inline-flex items-center gap-2">
          <span id="authUserAvatar" class="w-5 h-5 rounded-full bg-clay text-white text-[11px] font-semibold flex items-center justify-center">U</span>
          <span id="authUserName" class="hidden lg:inline max-w-[95px] truncate">Account</span>
        </button>
        <div id="authUserDropdown" class="hidden absolute right-0 mt-2 w-56 bg-white border border-line rounded-xl shadow-lg p-2 text-xs space-y-1 z-50">
          <div class="px-2.5 py-2 border-b border-line">
            <div id="authDropName" class="font-semibold text-ink truncate"></div>
            <div id="authDropEmail" class="text-[11px] text-muted truncate mt-0.5"></div>
          </div>
          <button onclick="switchWorkspace('assistant'); switchAssistantSubmode('private'); toggleUserDropdown();" class="w-full text-left px-2.5 py-2 rounded-lg hover:bg-parchment font-medium text-ink">My Study Desk</button>
          <button onclick="logoutUser()" class="w-full text-left px-2.5 py-2 rounded-lg text-crimson hover:bg-crimsonSoft font-medium">Sign out</button>
        </div>
      </div>

      <button id="refreshLiveBtn" onclick="triggerLiveRefresh()" class="btn-clay px-3 py-1.5 text-xs font-semibold inline-flex items-center gap-1.5 disabled:opacity-60" title="Check official portals for new listings">
        <span id="refreshIcon" class="material-symbols-outlined text-[15px]">refresh</span>
        <span id="refreshBtnLabel" class="hidden sm:inline">Refresh Live Data</span>
      </button>
    </div>
  </div>
</header>

<!-- ================= MAIN CONTAINER ================= -->
<main class="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-8 space-y-7">

  <!-- ======================================================== -->
  <!-- VIEW 1: OPPORTUNITIES                                    -->
  <!-- ======================================================== -->
  <div id="workspaceOpportunities" class="space-y-6">

    <!-- Editorial Header & Source Tabs -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-2 border-b border-line/80">
      <div class="max-w-2xl">
        <h1 class="font-serif font-semibold text-3xl sm:text-[34px] leading-tight tracking-tight text-ink">
          Scholarships, internships &amp; research grants
        </h1>
        <p class="text-sm text-muted mt-1.5 leading-relaxed">
          Collected directly from government ministries, universities, and company hiring boards so every listing opens on its official page.
        </p>
      </div>

      <div class="flex flex-wrap items-center gap-1.5 text-xs">
        <button data-stype="All" onclick="setSourceType('All')" class="stype-pill px-3 py-1.5 rounded-full bg-ink text-paper font-medium">
          All <span id="statAll" class="ml-1 opacity-80">--</span>
        </button>
        <button data-stype="Government" onclick="setSourceType('Government')" class="stype-pill px-3 py-1.5 rounded-full bg-white border border-line text-muted hover:text-ink hover:border-ink/30 font-medium">
          Government <span id="statGovt" class="ml-1 text-slateBlue">--</span>
        </button>
        <button data-stype="Company / Corporate" onclick="setSourceType('Company / Corporate')" class="stype-pill px-3 py-1.5 rounded-full bg-white border border-line text-muted hover:text-ink hover:border-ink/30 font-medium">
          Companies <span id="statCompany" class="ml-1 text-clay">--</span>
        </button>
        <button data-stype="Foundation / University" onclick="setSourceType('Foundation / University')" class="stype-pill px-3 py-1.5 rounded-full bg-white border border-line text-muted hover:text-ink hover:border-ink/30 font-medium">
          Universities <span id="statFound" class="ml-1 text-sage">--</span>
        </button>
      </div>
    </div>

    <!-- Subtle Portal Warning Banner -->
    <div id="sourceErrorBanner" class="hidden px-4 py-3 bg-ochreSoft border border-ochre/25 rounded-xl text-ochre text-xs flex items-start gap-2.5">
      <span class="material-symbols-outlined text-[17px] shrink-0 mt-0.5">info</span>
      <div>
        <strong class="font-semibold">Some portals took too long to respond:</strong>
        <span id="sourceErrorList" class="block mt-0.5 text-[11px] opacity-90"></span>
      </div>
    </div>

    <!-- Search & Filter Bar -->
    <div class="paper-card p-3.5 sm:p-4 space-y-3">
      <div class="flex flex-col lg:flex-row gap-3">
        <div class="relative flex-1">
          <span class="material-symbols-outlined absolute left-3 top-2.5 text-muted text-[18px]">search</span>
          <input id="filterSearch" type="text" oninput="debouncedFetch()" placeholder="Search by role, organization, field, or skill..." class="field-input w-full pl-9 pr-9 py-2 text-sm text-ink placeholder:text-muted/70"/>
          <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-2.5 top-2 text-muted hover:text-ink" aria-label="Clear search">
            <span class="material-symbols-outlined text-[18px]">close</span>
          </button>
        </div>

        <div class="flex flex-wrap items-center gap-1.5">
          <button data-cat="All" onclick="setCategory('All')" class="cat-pill px-3.5 py-2 text-xs font-semibold rounded-lg bg-claySoft text-clayDark border border-clay/25">All</button>
          <button data-cat="Internship" onclick="setCategory('Internship')" class="cat-pill px-3.5 py-2 text-xs font-medium rounded-lg bg-white text-muted border border-line hover:text-ink">Internships</button>
          <button data-cat="Scholarship" onclick="setCategory('Scholarship')" class="cat-pill px-3.5 py-2 text-xs font-medium rounded-lg bg-white text-muted border border-line hover:text-ink">Scholarships</button>
          <button data-cat="Funding" onclick="setCategory('Funding')" class="cat-pill px-3.5 py-2 text-xs font-medium rounded-lg bg-white text-muted border border-line hover:text-ink">Research Grants</button>

          <button id="toggleFiltersBtn" onclick="toggleAdvancedFilters()" class="btn-secondary px-3 py-2 text-xs font-medium inline-flex items-center gap-1.5 ml-auto lg:ml-1">
            <span class="material-symbols-outlined text-[16px]">tune</span>
            <span>Filters</span>
            <span id="activeFilterCount" class="hidden px-1.5 py-0.5 rounded-full bg-clay text-white text-[10px] font-semibold leading-none">0</span>
          </button>
        </div>
      </div>

      <!-- Collapsible More Filters -->
      <div id="advancedFiltersRow" class="hidden pt-3 border-t border-line grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        <div>
          <label for="filterDomain" class="block text-[11px] font-medium text-muted mb-1">Field</label>
          <select id="filterDomain" onchange="onFilterChange()" class="field-input w-full px-2.5 py-1.5 text-xs text-ink">
            <option value="All">All fields</option>
          </select>
        </div>
        <div>
          <label for="filterDegree" class="block text-[11px] font-medium text-muted mb-1">Academic level</label>
          <select id="filterDegree" onchange="onFilterChange()" class="field-input w-full px-2.5 py-1.5 text-xs text-ink">
            <option value="All">All levels</option>
            <option value="Undergraduate">Undergraduate</option>
            <option value="Postgraduate">Postgraduate</option>
            <option value="PhD / Faculty">PhD / Faculty</option>
          </select>
        </div>
        <div>
          <label for="filterFundingType" class="block text-[11px] font-medium text-muted mb-1">Support type</label>
          <select id="filterFundingType" onchange="onFilterChange()" class="field-input w-full px-2.5 py-1.5 text-xs text-ink">
            <option value="All">All types</option>
          </select>
        </div>
        <div>
          <label for="filterDeadline" class="block text-[11px] font-medium text-muted mb-1">Closing date</label>
          <select id="filterDeadline" onchange="onFilterChange()" class="field-input w-full px-2.5 py-1.5 text-xs text-ink">
            <option value="all">Any active</option>
            <option value="urgent_14d">Within 14 days</option>
            <option value="30d">Next 30 days</option>
            <option value="rolling">Rolling / Open</option>
          </select>
        </div>
        <div>
          <label for="filterSort" class="block text-[11px] font-medium text-muted mb-1">Sort by</label>
          <select id="filterSort" onchange="onFilterChange()" class="field-input w-full px-2.5 py-1.5 text-xs text-ink">
            <option value="deadline_asc">Closing soonest</option>
            <option value="recent_desc">Newest first</option>
            <option value="title_asc">Title A to Z</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Quiet Status & Utility Bar -->
    <div class="flex flex-wrap items-center justify-between gap-2 text-xs text-muted px-0.5">
      <div id="resultsSummaryText" class="font-medium">Loading listings...</div>
      <div class="flex flex-wrap items-center gap-4">
        <span id="cacheStatusLabel" class="text-[11px] text-muted"></span>
        <button id="resetFiltersLink" onclick="resetAllFilters()" class="hidden text-clay hover:underline font-medium">Clear filters</button>
        <button onclick="copyShareableFilterUrl()" class="hover:text-ink inline-flex items-center gap-1 font-medium" title="Copy a link to this filtered view">
          <span class="material-symbols-outlined text-[15px]">share</span> Share
        </button>
        <a id="exportCsvLink" href="/api/opportunities/export.csv" download class="hover:text-ink inline-flex items-center gap-1 font-medium" title="Download as spreadsheet">
          <span class="material-symbols-outlined text-[15px]">download</span> CSV
        </a>
        <a href="/api/calendar/upcoming.ics" download class="hover:text-ink inline-flex items-center gap-1 font-medium">
          <span class="material-symbols-outlined text-[15px]">calendar_month</span> Calendar
        </a>
      </div>
    </div>

    <!-- Opportunities Grid -->
    <div id="opportunitiesGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5"></div>

    <!-- Pagination -->
    <div id="loadMoreWrapper" class="hidden pt-2 text-center">
      <button id="loadMoreBtn" onclick="loadMoreCards()" class="btn-secondary px-6 py-2.5 text-xs font-semibold">
        Load more opportunities
      </button>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- VIEW 2: ELIGIBILITY & RESUME MATCHER                     -->
  <!-- ======================================================== -->
  <div id="workspaceMatcher" class="hidden space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-2 border-b border-line/80">
      <div>
        <h2 class="font-serif font-semibold text-3xl tracking-tight text-ink">Eligibility &amp; Resume Match</h2>
        <p class="text-sm text-muted mt-1">
          Check which scholarships or grants fit your background, or upload a resume to see matching openings.
        </p>
      </div>
      <div class="inline-flex rounded-lg bg-parchment p-1 border border-line">
        <button id="matchModeStudent" onclick="switchMatcherMode('student')" class="px-3.5 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs">Student</button>
        <button id="matchModeResearcher" onclick="switchMatcherMode('researcher')" class="px-3.5 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink">Researcher / Faculty</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <div class="lg:col-span-5 space-y-5">
        <!-- Student Form -->
        <form id="studentMatcherForm" onsubmit="event.preventDefault(); runStudentEligibilityMatch();" class="paper-card p-5 space-y-3.5 text-xs">
          <div class="pb-2 border-b border-line">
            <h3 class="font-serif font-semibold text-lg text-ink">Student profile</h3>
            <p class="text-[11px] text-muted mt-0.5">Used only to check eligibility criteria on this request.</p>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-muted mb-1">Your name</label>
              <input id="smName" type="text" placeholder="e.g. Rohan Kulkarni" class="field-input w-full px-3 py-2 text-ink"/>
            </div>
            <div>
              <label class="block font-medium text-muted mb-1">Gender</label>
              <select id="smGender" class="field-input w-full px-3 py-2 text-ink">
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Transgender">Transgender</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-muted mb-1">Home state</label>
              <select id="smState" class="field-input w-full px-3 py-2 text-ink">
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
              <label class="block font-medium text-muted mb-1">Category</label>
              <select id="smCategory" class="field-input w-full px-3 py-2 text-ink">
                <option value="General / Open">General / Open</option>
                <option value="OBC (Non-Creamy Layer)">OBC (Non-Creamy Layer)</option>
                <option value="SC (Scheduled Caste)">SC (Scheduled Caste)</option>
                <option value="ST (Scheduled Tribe)">ST (Scheduled Tribe)</option>
                <option value="EWS (Economically Weaker Section)">EWS</option>
                <option value="Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)">Minority</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block font-medium text-muted mb-1">Current degree or programme</label>
            <select id="smEdu" class="field-input w-full px-3 py-2 text-ink">
              <option value="UG - Engineering / Technology (B.Tech/B.E.)">UG — Engineering / B.Tech / B.E.</option>
              <option value="UG - General (B.Sc / B.Com / B.A. / BBA / BCA)">UG — B.Sc / B.A. / B.Com</option>
              <option value="UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)">UG — Medical / Nursing</option>
              <option value="Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)">Postgraduate — M.Tech / M.Sc / MBA</option>
              <option value="PhD / Doctoral Research">PhD / Doctoral Research</option>
              <option value="Diploma / Polytechnic">Diploma / Polytechnic</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-muted mb-1">Annual family income (INR)</label>
              <input id="smIncome" type="number" value="250000" min="0" step="25000" class="field-input w-full px-3 py-2 text-ink"/>
            </div>
            <div>
              <label class="block font-medium text-muted mb-1">Percentage (optional)</label>
              <input id="smPct" type="number" placeholder="e.g. 84" min="0" max="100" step="0.5" class="field-input w-full px-3 py-2 text-ink"/>
            </div>
          </div>
          <div class="flex flex-wrap gap-5 pt-1 text-ink">
            <label class="inline-flex items-center gap-2 font-medium cursor-pointer"><input id="smSingleGirl" type="checkbox" class="accent-clay rounded"/> Single girl child</label>
            <label class="inline-flex items-center gap-2 font-medium cursor-pointer"><input id="smPwd" type="checkbox" class="accent-clay rounded"/> PwD (&ge;40%)</label>
          </div>
          <button type="submit" class="btn-primary w-full py-2.5 text-xs font-semibold">
            Find eligible scholarships &amp; internships
          </button>
        </form>

        <!-- Researcher Form -->
        <form id="researcherMatcherForm" onsubmit="event.preventDefault(); runResearcherGrantMatch();" class="hidden paper-card p-5 space-y-3.5 text-xs">
          <div class="pb-2 border-b border-line">
            <h3 class="font-serif font-semibold text-lg text-ink">Researcher &amp; faculty profile</h3>
            <p class="text-[11px] text-muted mt-0.5">Match your research focus against active funding calls.</p>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-muted mb-1">Investigator name</label>
              <input id="rmName" type="text" placeholder="e.g. Dr. Meenakshi Iyer" class="field-input w-full px-3 py-2 text-ink"/>
            </div>
            <div>
              <label class="block font-medium text-muted mb-1">Highest qualification</label>
              <input id="rmDegree" type="text" value="Ph.D." placeholder="e.g. Ph.D. in Biotechnology" class="field-input w-full px-3 py-2 text-ink"/>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-muted mb-1">Institution</label>
              <input id="rmInst" type="text" placeholder="University or research institute" class="field-input w-full px-3 py-2 text-ink"/>
            </div>
            <div>
              <label class="block font-medium text-muted mb-1">Age (optional)</label>
              <input id="rmAge" type="number" placeholder="e.g. 34" min="18" max="75" class="field-input w-full px-3 py-2 text-ink"/>
            </div>
          </div>
          <div>
            <label class="block font-medium text-muted mb-1">Research summary or abstract</label>
            <textarea id="rmSummary" rows="3" class="field-input w-full p-3 text-ink" placeholder="Describe your area of research, methods, or proposed study..."></textarea>
          </div>
          <button type="submit" class="btn-clay w-full py-2.5 text-xs font-semibold">
            Find matching research grants
          </button>
        </form>

        <!-- Resume Upload -->
        <div id="resumeMatcherMount" class="paper-card p-5 space-y-3.5 text-xs">
          <div class="pb-2 border-b border-line">
            <h3 class="font-serif font-semibold text-lg text-ink">Match from your resume</h3>
            <p class="text-[11px] text-muted mt-0.5">Upload a PDF, Word file, or paste your skills below.</p>
          </div>
          <div class="flex items-center gap-2 p-2.5 bg-paper border border-line rounded-lg">
            <input type="file" id="resumeFile" accept=".pdf,.docx,.txt,.md" class="flex-1 text-xs text-muted file:mr-2.5 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-xs file:font-medium file:bg-parchment file:text-ink hover:file:bg-line"/>
            <select id="resumeCatFilter" class="field-input px-2 py-1 text-[11px] font-medium text-ink">
              <option value="All">All types</option>
              <option value="Internship">Internships</option>
              <option value="Scholarship">Scholarships</option>
              <option value="Funding">Grants</option>
            </select>
          </div>
          <textarea id="resumeRawText" rows="3" placeholder="Or paste your resume text or key skills (e.g. B.Tech CSE, Python, PyTorch, Embedded Systems, Molecular Biology)..." class="field-input w-full p-3 text-xs text-ink"></textarea>
          <button type="button" onclick="runResumeSemanticMatch()" class="btn-secondary w-full py-2.5 text-xs font-semibold">
            Find matches from resume
          </button>
        </div>
      </div>

      <!-- Results Column -->
      <div class="lg:col-span-7 space-y-4">
        <div id="matcherResultsContainer" class="paper-card p-8 text-left space-y-2">
          <h3 class="font-serif font-semibold text-xl text-ink">Your matches will appear here</h3>
          <p class="text-sm text-muted leading-relaxed max-w-lg">
            Fill in your student or researcher details on the left, or attach a resume, to see ranked opportunities with eligibility notes and quick draft outlines.
          </p>
        </div>
      </div>
    </div>
  </div>

  <!-- ======================================================== -->
  <!-- VIEW 3: MY TRACKER                                       -->
  <!-- ======================================================== -->
  <div id="workspaceTracker" class="hidden space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-2 border-b border-line/80">
      <div>
        <h2 class="font-serif font-semibold text-3xl tracking-tight text-ink">My Applications</h2>
        <p class="text-sm text-muted mt-1">
          Keep track of saved opportunities by stage or closing date, add personal notes, and set deadline reminders.
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <div class="inline-flex rounded-lg bg-parchment p-1 border border-line">
          <button id="trackerModeKanban" onclick="switchTrackerView('kanban')" class="px-3 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs">Board</button>
          <button id="trackerModeTimeline" onclick="switchTrackerView('timeline')" class="px-3 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink">Timeline</button>
        </div>
        <button onclick="exportSavedKanbanIcs()" class="btn-secondary px-3.5 py-2 text-xs font-semibold inline-flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[16px]">calendar_month</span>
          <span>Add saved to calendar</span>
        </button>
      </div>
    </div>

    <!-- Deadline Reminders -->
    <div class="paper-card p-4 sm:p-5 space-y-3 text-xs">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h3 class="font-serif font-semibold text-base text-ink">Deadline reminders</h3>
          <p class="text-[11px] text-muted">Get notified before your saved applications close.</p>
        </div>
        <button onclick="dispatchTrackerReminders()" class="btn-secondary px-3 py-1.5 text-xs font-medium">
          Check upcoming deadlines
        </button>
      </div>
      <form onsubmit="event.preventDefault(); addTrackerReminder();" class="grid grid-cols-1 sm:grid-cols-12 gap-2.5">
        <select id="remChannel" class="sm:col-span-3 field-input px-3 py-2 font-medium text-ink">
          <option value="browser">Browser alert</option>
          <option value="email">Email digest</option>
          <option value="webhook">Slack / Discord alert</option>
        </select>
        <input id="remTarget" type="text" placeholder="Email address, label, or notification link..." class="sm:col-span-5 field-input px-3 py-2 text-ink"/>
        <select id="remLeadDays" class="sm:col-span-2 field-input px-2.5 py-2 font-medium text-ink">
          <option value="2">2 days before</option>
          <option value="7" selected>7 days before</option>
          <option value="14">14 days before</option>
        </select>
        <button type="submit" class="sm:col-span-2 btn-primary py-2 font-semibold">
          Save alert
        </button>
      </form>
      <div id="trackerRemindersList" class="flex flex-wrap gap-2"></div>
    </div>

    <div id="kanbanBoardGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 items-start"></div>
    <div id="timelineBoardView" class="hidden space-y-3"></div>
  </div>

  <!-- ======================================================== -->
  <!-- VIEW 4: SARAL STUDY DESK & DOCUMENT CHECK                -->
  <!-- ======================================================== -->
  <div id="workspaceAssistant" class="hidden space-y-5">
    <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3 pb-2 border-b border-line/80">
      <div>
        <h2 class="font-serif font-semibold text-3xl tracking-tight text-ink">Saral Study Desk</h2>
        <p class="text-sm text-muted mt-1">Study from your own PDFs and notes with page citations, or check scheme rules and certificates.</p>
      </div>
      <div class="inline-flex rounded-lg bg-parchment p-1 border border-line self-start">
        <button id="submodePrivateBtn" onclick="switchAssistantSubmode('private')" class="px-3.5 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs">
          My Study Assistant
        </button>
        <button id="submodePublicBtn" onclick="switchAssistantSubmode('public')" class="px-3.5 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink">
          Schemes &amp; Document Check
        </button>
      </div>
    </div>

    <!-- SUB-VIEW A: PERSONAL STUDY SPACE -->
    <div id="assistantPrivatePanel" class="space-y-4">
      <div id="privateAuthGate" class="paper-card p-8 sm:p-10 max-w-2xl mx-auto text-center space-y-4">
        <h3 class="font-serif font-semibold text-2xl text-ink">Sign in to open your study desk</h3>
        <p class="text-sm text-muted leading-relaxed max-w-md mx-auto">
          Keep your lecture PDFs, markdown notes, and research papers in your own private library. Switch between Student, Researcher, and Educator styles anytime.
        </p>
        <div class="pt-1">
          <button onclick="openAuthModal()" class="btn-primary px-5 py-2.5 text-xs font-semibold inline-flex items-center gap-2">
            <span>Continue with Google</span>
          </button>
        </div>
      </div>

      <div id="privateWorkspaceGrid" class="hidden grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        <!-- Left: Library & Recent Chats -->
        <div class="lg:col-span-5 space-y-4">
          <div class="paper-card p-4 space-y-3 text-xs">
            <div class="flex items-center justify-between pb-2 border-b border-line">
              <h3 class="font-serif font-semibold text-base text-ink">My Documents</h3>
              <span id="privateDocCount" class="text-[11px] text-muted font-medium">0 files</span>
            </div>

            <div class="flex items-center gap-2 p-2 bg-paper border border-line rounded-lg">
              <input type="file" id="privateDocFile" accept=".pdf,.md,.markdown,.txt" class="flex-1 text-[11px] text-muted file:mr-2 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-[11px] file:font-medium file:bg-parchment file:text-ink"/>
              <button type="button" onclick="uploadPrivateDocument()" class="btn-primary px-3 py-1.5 text-[11px] font-semibold shrink-0">Upload</button>
            </div>

            <form onsubmit="event.preventDefault(); ingestPrivateUrl();" class="flex gap-2">
              <input id="privateUrlInput" type="url" placeholder="Paste an article or paper link (https://...)" class="field-input flex-1 px-3 py-1.5 text-[11px] text-ink"/>
              <button type="submit" class="btn-secondary px-3 py-1.5 text-[11px] font-semibold shrink-0">Add link</button>
            </form>

            <div id="privateDocsList" class="space-y-2 max-h-60 overflow-y-auto"></div>
          </div>

          <div class="paper-card p-4 space-y-2.5 text-xs">
            <div class="flex items-center justify-between pb-2 border-b border-line">
              <h3 class="font-serif font-semibold text-base text-ink">Recent Chats</h3>
              <button onclick="startNewPrivateSession()" class="text-xs font-semibold text-clay hover:underline">+ New chat</button>
            </div>
            <div id="privateSessionsList" class="space-y-1.5 max-h-44 overflow-y-auto"></div>
          </div>
        </div>

        <!-- Right: Study Chat -->
        <div class="lg:col-span-7 paper-card flex flex-col h-[620px] overflow-hidden">
          <div id="privateChatHeader" class="px-5 py-3.5 border-b border-line bg-paper flex flex-wrap items-center justify-between gap-2">
            <div>
              <div class="flex items-center gap-2.5">
                <h3 class="font-serif font-semibold text-lg text-ink">Saral</h3>
                <span id="privateModeBadge" class="px-2.5 py-0.5 rounded-full bg-claySoft text-clayDark text-[11px] font-semibold">Student Mode</span>
              </div>
              <p id="privateModeDesc" class="text-xs text-muted mt-0.5">Clear explanations grounded in your uploaded files.</p>
            </div>
          </div>

          <div id="privateChatMessages" class="flex-1 p-5 overflow-y-auto space-y-3.5 text-sm bg-paper/40">
            <div class="p-4 bg-white border border-line rounded-xl text-xs text-muted leading-relaxed">
              Upload a PDF, note, or paper link on the left, then ask a question here. Click any source citation below a reply to read the exact passage.
            </div>
          </div>

          <form onsubmit="event.preventDefault(); sendPrivateRagStream();" class="p-3.5 border-t border-line bg-white flex gap-2">
            <input id="privateChatInput" type="text" placeholder="Ask about your notes, formulas, or papers..." class="field-input flex-1 px-3.5 py-2 text-sm text-ink"/>
            <button id="privateChatSendBtn" type="submit" class="btn-clay px-4 py-2 text-xs font-semibold">Ask</button>
          </form>
        </div>
      </div>
    </div>

    <!-- SUB-VIEW B: PUBLIC SCHEMES & DOCUMENT CHECKER -->
    <div id="assistantPublicPanel" class="hidden grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <div class="lg:col-span-7 paper-card flex flex-col h-[600px] overflow-hidden">
        <div class="px-5 py-3.5 border-b border-line bg-paper flex items-center justify-between gap-2">
          <div>
            <h3 class="font-serif font-semibold text-lg text-ink">Saral Samjhauti</h3>
            <p class="text-xs text-muted">Ask in English or Hinglish about certificates, bank seeding, or scheme rules.</p>
          </div>
          <select id="ragLang" class="field-input px-2.5 py-1.5 text-xs font-medium text-ink">
            <option value="auto">Auto language</option>
            <option value="en">English</option>
            <option value="hinglish">Hinglish</option>
          </select>
        </div>

        <div class="px-5 py-2.5 bg-parchment/50 border-b border-line flex flex-wrap gap-2 text-xs">
          <button onclick="quickAsk('Aadhaar-NPCI DBT bank seeding kaise karwayein?')" class="px-2.5 py-1 rounded-full bg-white border border-line hover:border-clay/40 text-muted hover:text-ink font-medium">NPCI-DBT seeding</button>
          <button onclick="quickAsk('What are Income and OBC-NCL certificate validity rules?')" class="px-2.5 py-1 rounded-full bg-white border border-line hover:border-clay/40 text-muted hover:text-ink font-medium">Certificate validity</button>
          <button onclick="quickAsk('What are GFR 2017 and JRF/SRF research grant stipend norms?')" class="px-2.5 py-1 rounded-full bg-white border border-line hover:border-clay/40 text-muted hover:text-ink font-medium">JRF &amp; grant norms</button>
        </div>

        <div id="ragMessages" class="flex-1 p-5 overflow-y-auto space-y-3 text-sm bg-paper/40">
          <div class="p-4 bg-white border border-line rounded-xl text-xs sm:text-sm text-muted leading-relaxed">
            Ask any question in <strong class="text-ink">English</strong> or <strong class="text-ink">Hinglish</strong> about scholarship paperwork, Aadhaar-NPCI seeding, income or category certificates, or grant guidelines.
          </div>
        </div>

        <form onsubmit="event.preventDefault(); sendRagQuery();" class="p-3.5 border-t border-line bg-white flex gap-2">
          <input id="ragInput" type="text" placeholder="Type your question in English or Hinglish..." class="field-input flex-1 px-3.5 py-2 text-sm text-ink"/>
          <button type="submit" class="btn-primary px-4 py-2 text-xs font-semibold">Send</button>
        </form>
      </div>

      <div class="lg:col-span-5 paper-card p-5 space-y-4">
        <div class="pb-2 border-b border-line">
          <h3 class="font-serif font-semibold text-lg text-ink">Document readiness check</h3>
          <p class="text-xs text-muted mt-0.5">Upload a PDF or photo, or paste text from an Income Certificate, Marksheet, or CV to check for missing fields.</p>
        </div>

        <div class="flex items-center gap-2 p-2.5 bg-paper border border-line rounded-lg">
          <input type="file" id="docFile" accept=".pdf,.png,.jpg,.jpeg,.webp,.txt" class="flex-1 text-xs text-muted file:mr-2 file:py-1 file:px-2.5 file:rounded-md file:border-0 file:text-xs file:font-medium file:bg-parchment file:text-ink"/>
          <button type="button" onclick="uploadAndAnalyzeDoc()" class="btn-primary px-3 py-1.5 text-xs font-semibold">Scan</button>
        </div>

        <textarea id="docText" rows="5" placeholder="Or paste certificate, marksheet, or CV text here..." class="field-input w-full p-3 text-xs text-ink"></textarea>

        <button type="button" onclick="analyzeDocText()" class="btn-clay w-full py-2.5 text-xs font-semibold">
          Check completeness
        </button>

        <div id="docOutput" class="space-y-2 text-xs"></div>
      </div>
    </div>
  </div>

</main>

<!-- ================= AUTH SIGN-IN MODAL ================= -->
<div id="authModal" class="hidden fixed inset-0 z-50 bg-ink/40 backdrop-blur-xs flex items-center justify-center p-4" onclick="if(event.target===this) closeAuthModal()">
  <div class="bg-white border border-line rounded-2xl shadow-xl max-w-md w-full overflow-hidden">
    <div class="px-5 py-4 border-b border-line bg-paper flex items-center justify-between">
      <h3 class="font-serif font-semibold text-xl text-ink">Sign in to Madadgaar</h3>
      <button onclick="closeAuthModal()" class="p-1.5 rounded-lg text-muted hover:bg-parchment hover:text-ink"><span class="material-symbols-outlined text-[18px] block">close</span></button>
    </div>
    <div class="p-5 space-y-4 text-xs">
      <p class="text-muted leading-relaxed text-sm">
        Sign in to sync your saved applications, keep your study documents private, and switch between Student, Researcher, and Educator modes.
      </p>
      <a id="googleOAuthBtn" href="/api/auth/google/login" class="btn-secondary w-full py-2.5 text-sm font-semibold inline-flex items-center justify-center gap-2.5">
        <svg class="w-4 h-4" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="#4285F4" d="M23.745 12.27c0-.79-.07-1.54-.19-2.27h-11.3v4.51h6.47c-.29 1.48-1.14 2.73-2.4 3.58v3h3.86c2.26-2.09 3.56-5.17 3.56-8.82z"/>
          <path fill="#34A853" d="M12.255 24c3.24 0 5.95-1.08 7.93-2.91l-3.86-3c-1.08.72-2.45 1.16-4.07 1.16-3.13 0-5.78-2.11-6.73-4.96h-3.98v3.09C3.515 21.3 7.565 24 12.255 24z"/>
          <path fill="#FBBC05" d="M5.525 14.29c-.25-.72-.38-1.49-.38-2.29s.14-1.57.38-2.29V6.62h-3.98a11.86 11.86 0 000 10.76l3.98-3.09z"/>
          <path fill="#EA4335" d="M12.255 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C18.205 1.19 15.495 0 12.255 0c-4.69 0-8.74 2.7-10.71 6.62l3.98 3.09c.95-2.85 3.6-4.96 6.73-4.96z"/>
        </svg>
        <span>Continue with Google</span>
      </a>
      <div id="googleOAuthHint" class="hidden p-3 bg-paper border border-line rounded-lg text-xs text-muted">
        Google sign-in is unavailable right now. You can continue as a guest below.
      </div>
      <div id="devLoginSection" class="pt-3 border-t border-line space-y-2.5">
        <div class="text-[11px] font-semibold text-muted">Quick guest access</div>
        <form onsubmit="event.preventDefault(); submitDevLogin();" class="space-y-2.5">
          <input id="devLoginName" type="text" placeholder="Your name" class="field-input w-full px-3 py-2 text-ink"/>
          <input id="devLoginEmail" type="email" placeholder="you@example.com" class="field-input w-full px-3 py-2 text-ink"/>
          <button type="submit" class="btn-primary w-full py-2 font-semibold">
            Continue as guest
          </button>
        </form>
      </div>
    </div>
  </div>
</div>

<!-- ================= CITATION PASSAGE DRAWER ================= -->
<div id="citationModal" class="hidden fixed inset-0 z-50 bg-ink/40 backdrop-blur-xs flex items-center justify-center p-4" onclick="if(event.target===this) closeCitationModal()">
  <div class="bg-white border border-line rounded-2xl shadow-xl max-w-xl w-full max-h-[82vh] flex flex-col overflow-hidden">
    <div class="px-5 py-4 border-b border-line bg-paper flex items-start justify-between gap-2">
      <div>
        <div id="citMetaBadges" class="flex flex-wrap gap-1.5 mb-1.5"></div>
        <h3 id="citDocTitle" class="font-serif font-semibold text-lg text-ink">Source Passage</h3>
      </div>
      <button onclick="closeCitationModal()" class="p-1.5 rounded-lg text-muted hover:bg-parchment hover:text-ink"><span class="material-symbols-outlined text-[18px] block">close</span></button>
    </div>
    <div id="citChunkBody" class="p-5 overflow-y-auto text-sm leading-relaxed text-ink/90 whitespace-pre-wrap bg-white"></div>
  </div>
</div>

<!-- ================= OPPORTUNITY DETAIL MODAL ================= -->
<div id="detailModal" class="hidden fixed inset-0 z-50 bg-ink/40 backdrop-blur-xs flex items-center justify-center p-4" onclick="if(event.target===this) closeDetailModal()">
  <div class="bg-white border border-line rounded-2xl shadow-xl max-w-2xl w-full max-h-[88vh] flex flex-col overflow-hidden">
    <div class="px-5 py-4 border-b border-line bg-paper flex items-start justify-between gap-3">
      <div>
        <div id="dmBadges" class="flex flex-wrap gap-1.5 mb-1.5"></div>
        <h3 id="dmTitle" class="font-serif font-semibold text-xl leading-snug text-ink"></h3>
        <div id="dmOrg" class="text-xs font-medium text-muted mt-1"></div>
      </div>
      <button onclick="closeDetailModal()" class="p-1.5 rounded-lg text-muted hover:bg-parchment hover:text-ink">
        <span class="material-symbols-outlined text-[18px] block">close</span>
      </button>
    </div>
    <div id="dmBody" class="p-5 overflow-y-auto space-y-4 text-sm text-ink/85"></div>
    <div class="px-5 py-3.5 border-t border-line bg-paper flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-2">
        <button id="dmSaveBtn" onclick="toggleSaveCurrentModalOpp()" class="btn-secondary px-3 py-2 text-xs font-semibold inline-flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[16px]">bookmark_border</span>
          <span id="dmSaveLabel">Save</span>
        </button>
        <a id="dmCal" href="#" download class="btn-secondary px-3 py-2 text-xs font-medium inline-flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[16px]">calendar_month</span> Calendar
        </a>
      </div>
      <a id="dmApply" href="#" target="_blank" rel="noopener noreferrer" class="btn-clay px-4 py-2 text-xs font-semibold inline-flex items-center gap-1.5">
        <span>Apply / View Official Source</span>
        <span class="material-symbols-outlined text-[15px]">open_in_new</span>
      </a>
    </div>
  </div>
</div>

<!-- ================= FOOTER ================= -->
<footer class="border-t border-line bg-paper py-5 text-xs text-muted mt-8">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-2">
    <div><span class="font-serif font-semibold text-sm text-ink">Madadgaar</span> &middot; Scholarships, internships &amp; research grants from official portals</div>
    <div class="text-[11px] text-muted">Always verify final dates on the official portal before submitting</div>
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
      success: 'bg-sage text-white border-sage',
      error: 'bg-crimson text-white border-crimson',
      warning: 'bg-ochreSoft text-ochre border-ochre/30',
      info: 'bg-ink text-paper border-ink'
    };
    const toast = document.createElement('div');
    toast.className = `pointer-events-auto px-4 py-3 rounded-xl border shadow-lg text-xs font-medium flex items-center justify-between gap-3 ${styles[type] || styles.info}`;
    toast.innerHTML = `<span>${escapeHtml(message)}</span><button onclick="this.parentElement.remove()" class="opacity-75 hover:opacity-100 text-sm leading-none">&times;</button>`;
    container.appendChild(toast);
    setTimeout(() => { if (toast.parentElement) toast.remove(); }, 4200);
  }

  function switchWorkspace(ws) {
    document.getElementById('workspaceOpportunities').classList.toggle('hidden', ws !== 'opportunities');
    document.getElementById('workspaceMatcher').classList.toggle('hidden', ws !== 'matcher');
    document.getElementById('workspaceTracker').classList.toggle('hidden', ws !== 'tracker');
    document.getElementById('workspaceAssistant').classList.toggle('hidden', ws !== 'assistant');
    const act = 'relative h-full px-2.5 sm:px-3 text-[13px] font-semibold text-clay border-b-2 border-clay inline-flex items-center gap-1.5 shrink-0';
    const inact = 'relative h-full px-2.5 sm:px-3 text-[13px] font-medium text-muted hover:text-ink border-b-2 border-transparent inline-flex items-center gap-1.5 shrink-0';
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
      ? 'px-3.5 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs'
      : 'px-3.5 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink';
    document.getElementById('matchModeResearcher').className = !isStu
      ? 'px-3.5 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs'
      : 'px-3.5 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink';
  }

  async function runStudentEligibilityMatch() {
    const out = document.getElementById('matcherResultsContainer');
    out.innerHTML = '<div class="p-6 text-sm text-muted animate-pulse">Checking opportunities for your profile...</div>';
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
      if (!res.ok) throw new Error('Request failed');
      const results = await res.json();
      if (!results.length) {
        out.innerHTML = '<div class="paper-card p-6 text-sm text-muted">No matching opportunities found for those criteria right now.</div>';
        return;
      }
      out.innerHTML = `<div class="space-y-3.5 text-left">` + results.map(r => {
        const badgeCls = r.eligibility_status === 'ELIGIBLE'
          ? 'bg-sageSoft text-sage'
          : (r.eligibility_status === 'HIGH_PROBABILITY' ? 'bg-ochreSoft text-ochre' : 'bg-crimsonSoft text-crimson');
        const statusLabels = { ELIGIBLE: 'Eligible', HIGH_PROBABILITY: 'Strong match', INELIGIBLE: 'Not eligible' };
        const friendlyStatus = statusLabels[r.eligibility_status] || r.eligibility_status;
        const cleanNote = s => String(s || '').replace(/^[\u2705\u274c\u26a0\ufe0f\u2b50\s]+/, '');
        const reasons = (r.match_reasons || []).slice(0, 3).map(x => `<li class="text-xs text-muted">${escapeHtml(cleanNote(x))}</li>`).join('');
        const disq = (r.disqualifying_conditions || []).slice(0, 2).map(x => `<li class="text-xs text-crimson font-medium">${escapeHtml(cleanNote(x))}</li>`).join('');
        const applyUrl = r.foa.direct_apply_url || r.foa.source_url;
        return `
          <div class="paper-card p-5 space-y-2.5">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${badgeCls}">${escapeHtml(friendlyStatus)}</span>
                <span class="text-xs text-muted font-medium">${Math.round(r.match_percentage || 0)}% match</span>
              </div>
              <span class="text-xs text-muted">${escapeHtml(r.foa.issuing_authority || r.foa.agency)}</span>
            </div>
            <h4 class="font-serif font-semibold text-lg leading-snug text-ink">${escapeHtml(r.foa.title)}</h4>
            <p class="text-xs text-muted line-clamp-2 leading-relaxed">${escapeHtml(r.foa.brief_summary)}</p>
            <ul class="space-y-1 pl-3.5 list-disc">${reasons}${disq}</ul>
            <div class="pt-3 border-t border-line flex flex-wrap items-center justify-between gap-2">
              <span class="text-xs font-medium text-ink">${escapeHtml(r.foa.financials?.raw_budget_text || 'See official notice')}</span>
              <div class="flex items-center gap-2">
                <button onclick="openDraftModalForFoa('${escapeHtml(r.foa.foa_id)}', '${escapeHtml(r.foa.title).replace(/'/g, '')}', '${escapeHtml(applyUrl)}')" class="btn-secondary px-3 py-1.5 text-xs font-medium">Draft SOP</button>
                <a href="${escapeHtml(applyUrl)}" target="_blank" rel="noopener noreferrer" class="btn-primary px-3.5 py-1.5 text-xs font-semibold">Apply</a>
              </div>
            </div>
          </div>
        `;
      }).join('') + `</div>`;
      showToast(`Found ${results.length} matching opportunities.`, 'success');
    } catch (e) {
      out.innerHTML = '<div class="paper-card p-5 text-crimson text-sm">Could not check eligibility right now. Please try again.</div>';
    }
  }

  async function runResearcherGrantMatch() {
    const out = document.getElementById('matcherResultsContainer');
    out.innerHTML = '<div class="p-6 text-sm text-muted animate-pulse">Finding matching research grants...</div>';
    const payload = {
      researcher_name: document.getElementById('rmName').value.trim() || 'Principal Investigator',
      highest_degree: document.getElementById('rmDegree').value.trim() || 'Ph.D.',
      institution_name: document.getElementById('rmInst').value.trim() || 'Academic Institution',
      applicant_age: parseInt(document.getElementById('rmAge').value || '35', 10) || null,
      research_summary: document.getElementById('rmSummary').value.trim() || 'Scientific research',
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
        out.innerHTML = '<div class="paper-card p-6 text-sm text-muted">No matching research grants found.</div>';
        return;
      }
      out.innerHTML = `<div class="space-y-3.5 text-left">` + results.map(m => {
        const st = m.compliance?.status || 'ELIGIBLE';
        const badgeCls = st === 'ELIGIBLE' ? 'bg-sageSoft text-sage' : (st === 'WARNING' ? 'bg-ochreSoft text-ochre' : 'bg-crimsonSoft text-crimson');
        const stLabels = { ELIGIBLE: 'Eligible', WARNING: 'Check criteria', INELIGIBLE: 'Not eligible' };
        const friendlySt = stLabels[st] || st;
        const kws = (m.matching_keywords || []).slice(0, 4).map(k => `<span class="px-2 py-0.5 rounded-md bg-parchment text-muted text-[11px]">${escapeHtml(k)}</span>`).join('');
        const applyUrl = m.foa.direct_apply_url || m.foa.source_url;
        return `
          <div class="paper-card p-5 space-y-2.5">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${badgeCls}">${escapeHtml(friendlySt)}</span>
                <span class="text-xs text-muted font-medium">${(m.relevance_score * 100).toFixed(0)}% fit</span>
                <span class="text-xs text-slateBlue font-medium">${escapeHtml(m.deadline_status || 'Open')}</span>
              </div>
              <span class="text-xs text-muted">${escapeHtml(m.foa.issuing_authority || m.foa.agency)}</span>
            </div>
            <h4 class="font-serif font-semibold text-lg leading-snug text-ink">${escapeHtml(m.foa.title)}</h4>
            <p class="text-xs text-muted leading-relaxed">${escapeHtml(m.explanation?.why_grant_matches || m.foa.brief_summary)}</p>
            ${kws ? `<div class="flex flex-wrap gap-1.5">${kws}</div>` : ''}
            <div class="pt-3 border-t border-line flex flex-wrap items-center justify-between gap-2">
              <span class="text-xs font-medium text-ink">${escapeHtml(m.foa.financials?.raw_budget_text || 'See call ceiling')}</span>
              <div class="flex items-center gap-2">
                <button onclick="openDraftModalForFoa('${escapeHtml(m.foa.foa_id)}', '${escapeHtml(m.foa.title).replace(/'/g, '')}', '${escapeHtml(applyUrl)}')" class="btn-secondary px-3 py-1.5 text-xs font-medium">Draft proposal</button>
                <a href="${escapeHtml(applyUrl)}" target="_blank" rel="noopener noreferrer" class="btn-primary px-3.5 py-1.5 text-xs font-semibold">Official call</a>
              </div>
            </div>
          </div>
        `;
      }).join('') + `</div>`;
      showToast(`Found ${results.length} matching research grants.`, 'success');
    } catch (e) {
      out.innerHTML = '<div class="paper-card p-5 text-crimson text-sm">Could not match research grants right now. Please try again.</div>';
    }
  }

  async function runResumeSemanticMatch() {
    const fileInp = document.getElementById('resumeFile');
    const rawTxt = document.getElementById('resumeRawText').value.trim();
    const cat = document.getElementById('resumeCatFilter').value;
    if ((!fileInp.files || !fileInp.files.length) && !rawTxt) {
      showToast('Upload a resume file or paste your skills first.', 'warning');
      return;
    }
    const out = document.getElementById('matcherResultsContainer');
    out.innerHTML = '<div class="p-6 text-sm text-muted animate-pulse">Reading your resume and finding relevant openings...</div>';

    const fd = new FormData();
    if (fileInp.files && fileInp.files.length) fd.append('file', fileInp.files[0]);
    if (rawTxt) fd.append('raw_text', rawTxt);
    fd.append('category', cat);
    fd.append('top_k', '10');

    try {
      const res = await fetch('/api/resume/match', { method: 'POST', body: fd });
      if (!res.ok) throw new Error('Request failed');
      const data = await res.json();
      const skillsHtml = (data.detected_skills || []).map(s => `<span class="px-2.5 py-0.5 rounded-full bg-parchment text-ink text-[11px] font-medium">${escapeHtml(s)}</span>`).join('');
      const headerHtml = `
        <div class="paper-card p-4 bg-paper/70 text-left space-y-2">
          <div class="flex flex-wrap items-center justify-between gap-2">
            <span class="font-serif font-semibold text-base text-ink">Detected from your resume</span>
            <span class="text-xs font-medium text-slateBlue">${escapeHtml(data.detected_degree)} &middot; ${(data.detected_domains || []).join(', ')}</span>
          </div>
          ${skillsHtml ? `<div class="flex flex-wrap gap-1.5">${skillsHtml}</div>` : '<div class="text-xs text-muted">General academic profile detected.</div>'}
        </div>
      `;

      const cardsHtml = (data.matches || []).map(m => {
        const opp = m.opportunity;
        const matchedChips = (m.matched_skills || []).map(s => `<span class="px-2 py-0.5 rounded-md bg-sageSoft text-sage text-[11px] font-medium">${escapeHtml(s)}</span>`).join('');
        const gapChips = (m.missing_prerequisites || []).map(g => `<li class="text-xs text-ochre">${escapeHtml(g)}</li>`).join('');
        return `
          <div class="paper-card p-5 text-left space-y-2.5">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full bg-claySoft text-clayDark text-[11px] font-semibold">${m.fit_score}% fit</span>
                <span class="text-xs text-muted">${escapeHtml(opp.category)} &middot; ${escapeHtml(opp.source_domain)}</span>
              </div>
              <span class="text-xs font-medium text-slateBlue">${opp.deadline ? escapeHtml(opp.deadline) : 'Rolling'}</span>
            </div>
            <h4 class="font-serif font-semibold text-lg leading-snug text-ink">${escapeHtml(opp.title)}</h4>
            <p class="text-xs text-muted leading-relaxed">${escapeHtml(m.match_summary)}</p>
            ${matchedChips ? `<div class="flex flex-wrap gap-1.5">${matchedChips}</div>` : ''}
            ${gapChips ? `<ul class="space-y-0.5 pl-3.5 list-disc">${gapChips}</ul>` : ''}
            <div class="pt-3 border-t border-line flex items-center justify-between gap-2">
              <span class="text-xs font-medium text-ink">${escapeHtml(opp.stipend_or_amount)}</span>
              <div class="flex items-center gap-2">
                <button onclick="openDraftModalForFoa('${escapeHtml(opp.id)}', '${escapeHtml(opp.title).replace(/'/g, '')}', '${escapeHtml(opp.source_url)}')" class="btn-secondary px-3 py-1.5 text-xs font-medium">Draft SOP</button>
                <a href="${escapeHtml(opp.source_url)}" target="_blank" rel="noopener noreferrer" class="btn-primary px-3.5 py-1.5 text-xs font-semibold">Apply</a>
              </div>
            </div>
          </div>
        `;
      }).join('');

      out.innerHTML = `<div class="space-y-3.5">${headerHtml}${cardsHtml || '<div class="paper-card p-5 text-sm text-muted">No matching opportunities found for this filter.</div>'}</div>`;
      showToast(`Found ${(data.matches || []).length} opportunities matching your resume.`, 'success');
    } catch (e) {
      out.innerHTML = '<div class="paper-card p-5 text-crimson text-sm">Could not analyze your resume right now. Please try again.</div>';
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
        ? 'stype-pill px-3 py-1.5 rounded-full bg-ink text-paper font-medium'
        : 'stype-pill px-3 py-1.5 rounded-full bg-white border border-line text-muted hover:text-ink hover:border-ink/30 font-medium';
    });
    fetchOpportunities();
  }

  function setCategory(cat) {
    selectedCategory = cat;
    document.querySelectorAll('.cat-pill').forEach(btn => {
      const active = btn.getAttribute('data-cat') === cat;
      btn.className = active
        ? 'cat-pill px-3.5 py-2 text-xs font-semibold rounded-lg bg-claySoft text-clayDark border border-clay/25'
        : 'cat-pill px-3.5 py-2 text-xs font-medium rounded-lg bg-white text-muted border border-line hover:text-ink';
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
      <div class="paper-card p-5 space-y-3.5">
        <div class="flex justify-between"><div class="h-4 w-20 skeleton-pulse"></div><div class="h-4 w-16 skeleton-pulse"></div></div>
        <div class="h-5 w-5/6 skeleton-pulse"></div>
        <div class="h-3.5 w-1/2 skeleton-pulse"></div>
        <div class="h-10 w-full skeleton-pulse"></div>
        <div class="h-8 w-full skeleton-pulse"></div>
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
      return `<span class="text-xs text-slateBlue font-medium">${isRolling ? 'Rolling' : 'Open'}</span>`;
    }
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const days = Math.ceil((new Date(deadlineIso + 'T00:00:00') - today) / 86400000);
    if (days <= 14) {
      return `<span class="px-2 py-0.5 rounded-full bg-crimsonSoft text-crimson text-[11px] font-semibold">${days <= 0 ? 'Closes today' : `${days}d left`}</span>`;
    }
    return `<span class="text-xs text-muted font-medium">${deadlineIso}</span>`;
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
        ? 'stype-pill px-3 py-1.5 rounded-full bg-ink text-paper font-medium'
        : 'stype-pill px-3 py-1.5 rounded-full bg-white border border-line text-muted hover:text-ink hover:border-ink/30 font-medium';
    });
    document.querySelectorAll('.cat-pill').forEach(btn => {
      const active = btn.getAttribute('data-cat') === selectedCategory;
      btn.className = active
        ? 'cat-pill px-3.5 py-2 text-xs font-semibold rounded-lg bg-claySoft text-clayDark border border-clay/25'
        : 'cat-pill px-3.5 py-2 text-xs font-medium rounded-lg bg-white text-muted border border-line hover:text-ink';
    });
    if (pendingDomainFromUrl || pendingFundingFromUrl || sp.get('degree_level') || sp.get('deadline_window')) {
      document.getElementById('advancedFiltersRow').classList.remove('hidden');
    }
  }

  function syncFiltersToUrl(params) {
    const cleanParams = new URLSearchParams(params.toString());
    if (cleanParams.get('sort') === 'deadline_asc') cleanParams.delete('sort');
    const qs = cleanParams.toString();
    const hash = window.location.hash || '';
    const newUrl = (qs ? `${window.location.pathname}?${qs}` : window.location.pathname) + hash;
    window.history.replaceState(null, '', newUrl);
    const csvLink = document.getElementById('exportCsvLink');
    if (csvLink) {
      csvLink.href = qs ? `/api/opportunities/export.csv?${params.toString()}` : '/api/opportunities/export.csv';
    }
  }

  async function copyShareableFilterUrl() {
    try {
      await navigator.clipboard.writeText(window.location.href);
      showToast('Link copied to clipboard.', 'success');
    } catch (e) {
      showToast('Copy the link from your browser address bar.', 'info');
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
        `Showing <strong class="text-ink font-semibold">${allFetchedItems.length}</strong> of ${data.total_in_store} active opportunities`;
      document.getElementById('cacheStatusLabel').innerText = data.last_refreshed_at
        ? `Updated ${formatRelativeTime(data.last_refreshed_at)}`
        : '';

      const errBanner = document.getElementById('sourceErrorBanner');
      if (data.source_errors && data.source_errors.length > 0) {
        errBanner.classList.remove('hidden');
        document.getElementById('sourceErrorList').innerText = data.source_errors.join(' · ');
      } else {
        errBanner.classList.add('hidden');
      }

      renderVisibleCards(data.total_in_store);
    } catch (err) {
      document.getElementById('opportunitiesGrid').innerHTML = `
        <div class="col-span-full paper-card p-10 text-center space-y-3">
          <h3 class="font-serif font-semibold text-xl text-ink">Unable to load listings</h3>
          <p class="text-sm text-muted">Something went wrong while loading opportunities. Please try again.</p>
          <button onclick="fetchOpportunities()" class="btn-primary px-4 py-2 text-xs font-semibold">Try again</button>
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
        <div class="col-span-full paper-card p-10 text-center space-y-3">
          <h3 class="font-serif font-semibold text-xl text-ink">No Live Results Found</h3>
          <p class="text-sm text-muted max-w-md mx-auto">
            ${totalInStore === 0
              ? 'No opportunities loaded yet. Click "Refresh Live Data" to check official portals.'
              : 'No opportunities match those filters. Try broadening your search.'}
          </p>
          <div class="flex justify-center gap-2 pt-1">
            <button onclick="resetAllFilters()" class="btn-secondary px-4 py-2 text-xs font-semibold">Reset filters</button>
            <button onclick="triggerLiveRefresh()" class="btn-clay px-4 py-2 text-xs font-semibold">Refresh Live Data</button>
          </div>
        </div>
      `;
      return;
    }

    const slice = allFetchedItems.slice(0, visibleCount);
    grid.innerHTML = slice.map((opp, idx) => {
      const catColor = opp.category === 'Funding'
        ? 'bg-slateSoft text-slateBlue'
        : (opp.category === 'Internship' ? 'bg-claySoft text-clayDark' : 'bg-sageSoft text-sage');

      const srcShort = opp.source_type === 'Government'
        ? 'Government'
        : (opp.source_type === 'Company / Corporate' ? 'Company' : 'University');

      const saved = isOppSaved(opp.id);

      return `
        <article class="paper-card paper-card-hover p-5 flex flex-col justify-between gap-4">
          <div class="space-y-2.5">
            <div class="flex items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold ${catColor}">${escapeHtml(opp.category)}</span>
                <span class="text-[11px] text-muted font-medium">${srcShort}</span>
              </div>
              ${deadlinePill(opp.deadline, opp.is_rolling)}
            </div>

            <div>
              <h3 onclick="openDetailModal(${idx})" class="cursor-pointer font-serif font-semibold text-[18px] leading-snug text-ink hover:text-clay line-clamp-2" title="${escapeHtml(opp.title)}">${escapeHtml(opp.title)}</h3>
              <p class="text-xs text-muted mt-1 truncate">${escapeHtml(opp.organization)}</p>
            </div>

            <p class="text-xs text-muted line-clamp-2 leading-relaxed">${escapeHtml(opp.summary)}</p>

            <div class="flex flex-wrap items-center gap-x-2 gap-y-1 pt-1 text-xs text-ink/85">
              <span class="font-medium truncate max-w-[190px]" title="${escapeHtml(opp.stipend_or_amount)}">${escapeHtml(opp.stipend_or_amount)}</span>
              <span class="text-line">&middot;</span>
              <span class="text-muted">${escapeHtml(opp.degree_level)}</span>
            </div>
          </div>

          <div class="pt-3 border-t border-line flex items-center justify-between gap-2">
            <div class="text-[11px] text-muted leading-tight truncate">
              <span class="text-sage font-medium block">Last verified: ${formatRelativeTime(opp.last_verified_at)}</span>
              <span class="truncate block opacity-80">${escapeHtml(opp.source_domain)}</span>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
              <button onclick="toggleSaveOpportunity(${idx})" class="px-2.5 py-1.5 rounded-lg text-xs font-medium border ${saved ? 'bg-claySoft border-clay/30 text-clayDark' : 'bg-white border-line text-muted hover:text-ink hover:bg-parchment/60'}" title="Save to My Tracker">
                ${saved ? 'Saved' : 'Save'}
              </button>
              <button onclick="openDetailModal(${idx})" class="btn-secondary px-2.5 py-1.5 text-xs font-medium" title="View details &amp; requirements">Details</button>
              <a href="${escapeHtml(opp.source_url)}" target="_blank" rel="noopener noreferrer" class="btn-primary px-3 py-1.5 text-xs font-semibold inline-flex items-center gap-1">
                <span>Apply</span>
                <span class="material-symbols-outlined text-[13px]">arrow_outward</span>
              </a>
            </div>
          </div>
        </article>
      `;
    }).join('');

    if (allFetchedItems.length > visibleCount) {
      loadMoreWrap.classList.remove('hidden');
      document.getElementById('loadMoreBtn').innerText = `Show more (${visibleCount} of ${allFetchedItems.length})`;
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
      <span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-claySoft text-clayDark">${escapeHtml(opp.category)}</span>
      <span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-parchment text-ink">${escapeHtml(opp.source_type)}</span>
      <span class="px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-parchment text-muted">${escapeHtml(opp.domain)}</span>
    `;
    document.getElementById('dmTitle').innerText = opp.title;
    document.getElementById('dmOrg').innerText = `${opp.organization} · ${opp.source_domain}`;
    const saved = isOppSaved(opp.id);
    document.getElementById('dmSaveLabel').innerText = saved ? 'Saved in tracker' : 'Save to tracker';

    document.getElementById('dmBody').innerHTML = `
      <p class="leading-relaxed text-ink/90">${escapeHtml(opp.summary)}</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 p-4 bg-paper border border-line rounded-xl text-xs">
        <div><span class="text-muted block text-[11px] mb-0.5">Award / Stipend</span><strong class="font-semibold text-ink">${escapeHtml(opp.stipend_or_amount)}</strong></div>
        <div><span class="text-muted block text-[11px] mb-0.5">Closing date</span><strong class="font-semibold text-ink">${opp.deadline ? escapeHtml(opp.deadline) : 'Rolling / Open'}</strong></div>
        <div><span class="text-muted block text-[11px] mb-0.5">Eligibility</span><strong class="font-semibold text-ink">${escapeHtml(opp.eligibility)}</strong></div>
        <div><span class="text-muted block text-[11px] mb-0.5">Location</span><strong class="font-semibold text-ink">${escapeHtml(opp.location || 'India / Global')}</strong></div>
      </div>
      <div class="flex flex-wrap items-center justify-between gap-2 pt-1">
        <div class="text-xs text-sage font-medium">
          Official link verified (${formatRelativeTime(opp.last_verified_at)})
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <button id="deepAnalyzeBtn" onclick="runDeepPageAnalysis('${escapeHtml(opp.id)}')" class="btn-secondary px-3 py-1.5 text-xs font-semibold inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[15px]">article</span>
            <span>Summarize requirements</span>
          </button>
          <button id="draftProposalBtn" onclick="runProposalDraft('${escapeHtml(opp.id)}')" class="btn-secondary px-3 py-1.5 text-xs font-semibold inline-flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[15px]">edit_note</span>
            <span>Draft SOP / Proposal</span>
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
      btn.innerHTML = '<span class="material-symbols-outlined text-[15px] animate-spin">refresh</span><span>Reading official page...</span>';
    }
    box.classList.remove('hidden');
    box.innerHTML = '<div class="p-4 bg-paper border border-line rounded-xl text-xs text-muted animate-pulse">Reading the official listing and summarizing key requirements...</div>';

    try {
      const res = await fetch(`/api/opportunities/${encodeURIComponent(oppId)}/deep-analyze`, { method: 'POST' });
      if (!res.ok) throw new Error('Request failed');
      const d = await res.json();

      const eligHtml = (d.eligibility_highlights || []).map(item =>
        `<li class="text-xs text-ink/85 leading-relaxed">${escapeHtml(item)}</li>`
      ).join('');
      const docsHtml = (d.required_documents || []).map(doc =>
        `<span class="px-2.5 py-1 rounded-md bg-white border border-line text-xs text-ink">${escapeHtml(doc)}</span>`
      ).join('');
      const stepsHtml = (d.application_steps || []).map((st, i) => {
        const cleanStep = String(st || '').replace(/^\s*\d+\.\s*/, '');
        return `<li class="text-xs text-ink/85 leading-relaxed"><span class="font-semibold text-ink mr-1">${i + 1}.</span>${escapeHtml(cleanStep)}</li>`;
      }).join('');
      const attachmentsList = d.direct_attachments || d.direct_pdf_urls || [];
      const pdfLinksHtml = attachmentsList.map(u =>
        `<a href="${escapeHtml(u)}" target="_blank" rel="noopener noreferrer" class="px-3 py-1 rounded-md bg-white border border-line hover:border-clay/40 text-xs font-medium text-slateBlue inline-flex items-center gap-1">Official guideline PDF <span class="material-symbols-outlined text-[13px]">arrow_outward</span></a>`
      ).join('');
      const deadlineDisplay = d.extracted_deadline || d.extracted_deadline_text || 'Check official page';
      const sourceLabel = d.is_pdf_parsed ? 'PDF circular' : 'Official page';

      box.innerHTML = `
        <div class="p-4 bg-paper border border-line rounded-xl space-y-3.5 text-xs">
          <div class="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-line">
            <span class="font-serif font-semibold text-base text-ink">Requirements &amp; application summary</span>
            <span class="px-2.5 py-0.5 rounded-full bg-parchment text-muted text-[11px] font-medium">${sourceLabel}</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            <div class="p-3 bg-white border border-line rounded-lg">
              <span class="text-[11px] text-muted block">Stipend / award</span>
              <strong class="text-ink font-semibold">${escapeHtml(d.extracted_financials)}</strong>
            </div>
            <div class="p-3 bg-white border border-line rounded-lg">
              <span class="text-[11px] text-muted block">Deadline</span>
              <strong class="text-ink font-semibold">${escapeHtml(deadlineDisplay)}</strong>
            </div>
          </div>
          ${d.key_excerpt ? `<p class="text-xs text-muted bg-white p-3 rounded-lg border border-line leading-relaxed">${escapeHtml(d.key_excerpt)}</p>` : ''}
          <div>
            <span class="text-[11px] font-semibold text-muted block mb-1.5">Eligibility &amp; key guidelines</span>
            <ul class="space-y-1 pl-4 list-disc">${eligHtml}</ul>
          </div>
          <div>
            <span class="text-[11px] font-semibold text-muted block mb-1.5">Documents to keep ready</span>
            <div class="flex flex-wrap gap-1.5">${docsHtml}</div>
          </div>
          ${pdfLinksHtml ? `<div><span class="text-[11px] font-semibold text-muted block mb-1.5">Attachments</span><div class="flex flex-wrap gap-1.5">${pdfLinksHtml}</div></div>` : ''}
          <div>
            <span class="text-[11px] font-semibold text-muted block mb-1.5">How to apply</span>
            <ol class="space-y-1">${stepsHtml}</ol>
          </div>
        </div>
      `;
      showToast('Requirements summary ready.', 'success');
    } catch (err) {
      box.innerHTML = '<div class="p-3.5 bg-crimsonSoft border border-crimson/20 rounded-xl text-crimson text-xs">Could not read details from the official page right now. Try opening the official link directly.</div>';
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[15px]">refresh</span><span>Refresh summary</span>';
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
      btn.innerHTML = '<span class="material-symbols-outlined text-[15px] animate-spin">refresh</span><span>Drafting...</span>';
    }
    box.classList.remove('hidden');
    box.innerHTML = '<div class="p-4 bg-paper border border-line rounded-xl text-xs text-muted animate-pulse">Preparing a tailored outline and checklist...</div>';

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
        <div class="p-3.5 bg-white border border-line rounded-lg space-y-1">
          <div class="font-semibold text-xs text-ink">${escapeHtml(s.section_title)}</div>
          <div class="text-xs text-muted whitespace-pre-line leading-relaxed">${escapeHtml(s.drafted_content)}</div>
        </div>
      `).join('');
      const chkHtml = (d.compliance_checklist || []).slice(0, 4).map(c => `<li class="text-xs text-ink/85">${escapeHtml(c)}</li>`).join('');

      box.innerHTML = `
        <div class="p-4 bg-paper border border-line rounded-xl space-y-3 text-xs">
          <div class="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-line">
            <span class="font-serif font-semibold text-base text-ink">Draft outline (${(d.sections || []).length} sections)</span>
            <button onclick="copyDraftToClipboard()" class="btn-primary px-3 py-1 text-[11px] font-semibold">Copy full draft</button>
          </div>
          <div class="space-y-2">${secHtml}</div>
          <div>
            <span class="text-[11px] font-semibold text-muted block mb-1">Before you submit</span>
            <ul class="space-y-1 pl-4 list-disc">${chkHtml}</ul>
          </div>
        </div>
      `;
      showToast('Draft outline ready.', 'success');
    } catch (err) {
      box.innerHTML = '<div class="p-3.5 bg-crimsonSoft border border-crimson/20 rounded-xl text-crimson text-xs">Could not prepare the draft right now. Please try again.</div>';
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined text-[15px]">edit_note</span><span>Regenerate draft</span>';
      }
    }
  }

  async function copyDraftToClipboard() {
    if (!lastDraftPlainText) return;
    try {
      await navigator.clipboard.writeText(lastDraftPlainText);
      showToast('Full draft copied to clipboard.', 'success');
    } catch (e) {
      showToast('Copy failed — select and copy text manually.', 'warning');
    }
  }

  function openDraftModalForFoa(foaId, title, applyUrl) {
    const idx = allFetchedItems.findIndex(o => o.id === foaId);
    if (idx >= 0) {
      openDetailModal(idx);
      runProposalDraft(foaId);
      return;
    }
    currentModalOpp = { id: foaId, title: title || foaId, source_url: applyUrl || '' };
    document.getElementById('dmBadges').innerHTML = '<span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-claySoft text-clayDark">Draft outline</span>';
    document.getElementById('dmTitle').innerText = title || foaId;
    document.getElementById('dmOrg').innerText = 'Proposal & SOP Assistant';
    document.getElementById('dmSaveLabel').innerText = isOppSaved(foaId) ? 'Saved in tracker' : 'Save to tracker';
    document.getElementById('dmBody').innerHTML = '<div id="proposalDraftContainer"></div>';
    document.getElementById('dmCal').href = `/api/foas/${encodeURIComponent(foaId)}/calendar`;
    const applyLink = document.getElementById('dmApply');
    if (applyUrl) {
      applyLink.href = applyUrl;
      applyLink.classList.remove('hidden');
    } else {
      applyLink.href = `/api/foas/${encodeURIComponent(foaId)}`;
    }
    document.getElementById('detailModal').classList.remove('hidden');
    runProposalDraft(foaId);
  }

  // Personal Application Tracker
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
        showToast(`Saved "${opp.title.slice(0, 38)}..." to My Tracker.`, 'success');
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
          body: JSON.stringify({
            opp_id: currentModalOpp.id,
            stage: 'Saved',
            title: currentModalOpp.title,
            source_url: currentModalOpp.source_url || ''
          })
        });
        if (!res.ok) throw new Error('Save failed');
        const data = await res.json();
        kanbanItems = data.items || [];
        updateTrackerBadge();
        renderVisibleCards(lastTotalInStore);
      } catch (e) {}
    }
    document.getElementById('dmSaveLabel').innerText = isOppSaved(currentModalOpp.id) ? 'Saved in tracker' : 'Save to tracker';
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
      showToast(`Moved to ${newStage}.`, 'info');
    } catch (e) {
      showToast('Could not update stage.', 'error');
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
      showToast('Note saved.', 'success');
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
      showToast('Could not remove item.', 'error');
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
      ? 'px-3 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs'
      : 'px-3 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink';
    document.getElementById('trackerModeTimeline').className = !isKanban
      ? 'px-3 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs'
      : 'px-3 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink';
    if (!isKanban) renderTimelineView();
  }

  function renderTimelineView() {
    const el = document.getElementById('timelineBoardView');
    if (!el) return;
    if (!kanbanItems.length) {
      el.innerHTML = '<div class="paper-card p-8 text-center text-sm text-muted">Save opportunities to see their deadlines lined up chronologically.</div>';
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
      const urgCls = item.days <= 7 ? 'bg-crimsonSoft text-crimson' : (item.days <= 30 ? 'bg-ochreSoft text-ochre' : 'bg-slateSoft text-slateBlue');
      const urgLbl = item.deadline ? (item.days <= 0 ? 'Closes today' : `${item.days}d left · ${item.deadline}`) : 'Rolling';
      return `
        <div class="paper-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div class="flex items-start gap-3">
            <span class="px-2.5 py-1 rounded-full text-[11px] font-semibold shrink-0 ${urgCls}">${escapeHtml(urgLbl)}</span>
            <div>
              <a href="${escapeHtml(item.source_url)}" target="_blank" rel="noopener noreferrer" class="font-serif font-semibold text-base text-ink hover:text-clay">${escapeHtml(item.title)}</a>
              <div class="text-xs text-muted mt-0.5">${escapeHtml(item.organization)} &middot; ${escapeHtml(item.stage)}${item.notes ? ` &middot; ${escapeHtml(item.notes)}` : ''}</div>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <select onchange="moveKanbanStage('${escapeHtml(item.opp_id)}', this.value)" class="field-input px-2.5 py-1 text-xs font-medium text-ink">
              ${KANBAN_STAGES.map(s => `<option value="${s}" ${s === item.stage ? 'selected' : ''}>${s}</option>`).join('')}
            </select>
            <button onclick="removeKanbanItem('${escapeHtml(item.opp_id)}')" class="p-1.5 rounded-lg text-muted hover:text-crimson hover:bg-crimsonSoft text-xs" title="Remove">&times;</button>
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
    const target = document.getElementById('remTarget').value.trim() || (channel === 'browser' ? 'Browser Alert' : '');
    const lead_days = parseInt(document.getElementById('remLeadDays').value || '7', 10);
    if (!target) { showToast('Enter an email address or notification link.', 'warning'); return; }
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
      showToast(`Reminder saved for ${lead_days} days before deadline.`, 'success');
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
          try { new Notification('Madadgaar Deadline Alert', { body: bItem.preview }); } catch (e) {}
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
    const chLabels = { browser: 'Browser', email: 'Email', webhook: 'Webhook' };
    const pills = trackerReminders.map(r => `
      <span class="px-3 py-1 rounded-full bg-paper border border-line text-xs text-ink inline-flex items-center gap-2">
        <span class="font-semibold">${escapeHtml(chLabels[r.channel] || r.channel)}</span>
        <span class="text-muted">${r.lead_days}d &middot; ${escapeHtml(r.target.slice(0, 32))}</span>
        <button onclick="deleteTrackerReminder(${r.id})" class="text-muted hover:text-crimson font-semibold">&times;</button>
      </span>
    `).join('');
    const dueBadge = (dueAlerts && dueAlerts.length)
      ? `<span class="px-3 py-1 rounded-full bg-crimsonSoft text-crimson text-xs font-semibold">${dueAlerts.length} closing soon</span>`
      : '';
    box.innerHTML = pills + dueBadge;
  }

  async function exportSavedKanbanIcs() {
    if (!kanbanItems.length) {
      showToast('Save at least one opportunity first.', 'warning');
      return;
    }
    try {
      const res = await authFetch(`/api/tracker/${encodeURIComponent(activeSessionId)}/calendar.ics`);
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'madadgaar_saved_deadlines.ics';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      showToast('Could not download calendar right now.', 'error');
    }
  }

  function renderKanbanBoard() {
    const board = document.getElementById('kanbanBoardGrid');
    if (!board) return;
    const stageDot = {
      'Saved': 'bg-clay',
      'Preparing Docs': 'bg-slateBlue',
      'Applied': 'bg-ochre',
      'Result': 'bg-sage'
    };

    board.innerHTML = KANBAN_STAGES.map(stage => {
      const colItems = kanbanItems.filter(i => i.stage === stage);
      const cardsHtml = colItems.length
        ? colItems.map(item => `
            <div class="p-3.5 bg-paper/70 border border-line rounded-xl space-y-2">
              <div class="flex items-start justify-between gap-2">
                <span class="text-[11px] font-medium text-muted">${escapeHtml(item.category)}</span>
                <button onclick="removeKanbanItem('${escapeHtml(item.opp_id)}')" class="text-muted hover:text-crimson text-sm leading-none" title="Remove">&times;</button>
              </div>
              <a href="${escapeHtml(item.source_url)}" target="_blank" rel="noopener noreferrer" class="block font-serif font-semibold text-sm text-ink hover:text-clay leading-snug">
                ${escapeHtml(item.title)}
              </a>
              <div class="text-[11px] text-muted truncate">${escapeHtml(item.organization)}</div>
              <div class="flex items-center justify-between text-[11px] text-ink/80 pt-1">
                <span class="truncate max-w-[115px]">${escapeHtml(item.stipend_or_amount)}</span>
                <span class="font-medium text-slateBlue">${item.deadline ? escapeHtml(item.deadline) : 'Rolling'}</span>
              </div>
              <input type="text" value="${escapeHtml(item.notes || '')}" placeholder="Add a personal note..." onchange="saveKanbanNote('${escapeHtml(item.opp_id)}', '${escapeHtml(item.stage)}', this.value)" class="field-input w-full px-2.5 py-1.5 text-[11px] text-ink"/>
              <div class="pt-2 border-t border-line flex items-center justify-between gap-1">
                <label class="text-[11px] text-muted">Stage</label>
                <select onchange="moveKanbanStage('${escapeHtml(item.opp_id)}', this.value)" class="field-input px-2 py-0.5 text-[11px] font-medium text-ink">
                  ${KANBAN_STAGES.map(s => `<option value="${s}" ${s === item.stage ? 'selected' : ''}>${s}</option>`).join('')}
                </select>
              </div>
            </div>
          `).join('')
        : `<div class="p-6 border border-dashed border-line rounded-xl text-center text-xs text-muted">No items yet</div>`;

      return `
        <div class="paper-card p-3.5 space-y-3">
          <div class="flex items-center justify-between pb-2 border-b border-line">
            <span class="inline-flex items-center gap-2 text-xs font-semibold text-ink">
              <span class="w-2 h-2 rounded-full ${stageDot[stage] || 'bg-clay'}"></span>
              ${escapeHtml(stage)}
            </span>
            <span class="text-xs text-muted font-medium">${colItems.length}</span>
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
    showToast('Checking official portals for the latest listings...', 'info');

    try {
      const res = await fetch('/api/opportunities/refresh?force=true', { method: 'POST' });
      if (!res.ok) throw new Error('Request failed');
      const report = await res.json();
      facetsInitialized = false;
      document.getElementById('filterDomain').innerHTML = '<option value="All">All fields</option>';
      document.getElementById('filterFundingType').innerHTML = '<option value="All">All types</option>';
      await updateStatsCounters();
      await fetchOpportunities();
      showToast(
        `Updated — ${report.total_live_opportunities} active opportunities available.`,
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

  // Public Saral Samjhauti & Document Readiness
  function quickAsk(q) { document.getElementById('ragInput').value = q; sendRagQuery(); }

  async function sendRagQuery() {
    const inp = document.getElementById('ragInput');
    const box = document.getElementById('ragMessages');
    const query = inp.value.trim();
    if (!query) return;
    inp.value = '';
    box.insertAdjacentHTML('beforeend', `<div class="flex justify-end"><div class="max-w-[82%] px-3.5 py-2.5 rounded-2xl rounded-br-sm bg-ink text-paper text-xs sm:text-sm">${escapeHtml(query)}</div></div>`);
    box.scrollTop = box.scrollHeight;
    try {
      const res = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: activeSessionId, language: document.getElementById('ragLang').value })
      });
      const data = await res.json();
      if (data.session_id && !currentUser) { activeSessionId = data.session_id; localStorage.setItem('madadgaar_session_id', activeSessionId); }
      const htmlAns = escapeHtml(data.answer || '')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-ink">$1</strong>')
        .replace(/\*([^*\n]+)\*/g, '<em class="text-muted">$1</em>')
        .replace(/`([^`\n]+)`/g, '<code class="px-1 py-0.5 rounded bg-parchment text-xs">$1</code>')
        .replace(/(https?:\/\/[^\s<)]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-slateBlue underline break-all">$1</a>')
        .replace(/\n/g, '<br/>');
      const cites = (data.citations || []).slice(0, 3).map((c, i) =>
        `<div class="text-xs flex justify-between gap-2 pt-1.5 text-muted"><span class="truncate">[${i+1}] ${escapeHtml(c.title)}</span><a href="${escapeHtml(c.official_url)}" target="_blank" class="text-slateBlue font-medium shrink-0 hover:underline">Source</a></div>`
      ).join('');
      box.insertAdjacentHTML('beforeend', `<div class="p-4 bg-white border border-line rounded-2xl rounded-bl-sm text-xs sm:text-sm space-y-2 leading-relaxed"><div>${htmlAns}</div>${cites ? `<div class="border-t border-line pt-1.5">${cites}</div>` : ''}</div>`);
      box.scrollTop = box.scrollHeight;
    } catch (e) { showToast('Could not reach the assistant right now.', 'error'); }
  }

  async function analyzeDocText() {
    const raw_text = document.getElementById('docText').value.trim();
    if (!raw_text) { showToast('Paste document text first.', 'warning'); return; }
    const out = document.getElementById('docOutput');
    out.innerHTML = '<div class="text-xs text-muted animate-pulse">Checking document...</div>';
    try {
      const res = await fetch('/api/documents/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_text, document_type_hint: 'AUTO' })
      });
      renderDocResult(await res.json());
    } catch (e) { out.innerHTML = '<div class="text-crimson text-xs">Check failed. Please try again.</div>'; }
  }

  async function uploadAndAnalyzeDoc() {
    const inp = document.getElementById('docFile');
    if (!inp.files || !inp.files.length) { showToast('Select a file first.', 'warning'); return; }
    const fd = new FormData();
    fd.append('file', inp.files[0]);
    fd.append('document_type_hint', 'AUTO');
    const out = document.getElementById('docOutput');
    out.innerHTML = '<div class="text-xs text-muted animate-pulse">Reading uploaded file...</div>';
    try {
      const res = await fetch('/api/documents/upload', { method: 'POST', body: fd });
      renderDocResult(await res.json());
    } catch (e) { out.innerHTML = '<div class="text-crimson text-xs">Could not read that file.</div>'; }
  }

  function renderDocResult(data) {
    const out = document.getElementById('docOutput');
    const niceDocType = String(data.document_type || 'Document')
      .replace(/_/g, ' ')
      .toLowerCase()
      .replace(/\b\w/g, c => c.toUpperCase());
    const statusMap = { DETECTED: 'Found', MISSING: 'Missing', WARNING: 'Check' };
    const statusColor = { DETECTED: 'text-sage', MISSING: 'text-crimson', WARNING: 'text-ochre' };
    const fields = (data.extracted_fields || []).map(f =>
      `<div class="p-2.5 bg-paper border border-line rounded-lg flex justify-between gap-2 text-xs"><span><strong class="font-medium text-ink">${escapeHtml(f.field_name)}:</strong> <span class="text-muted">${escapeHtml(f.extracted_value || 'Not found')}</span></span><span class="font-semibold ${statusColor[f.status] || 'text-muted'}">${escapeHtml(statusMap[f.status] || f.status)}</span></div>`
    ).join('');
    out.innerHTML = `
      <div class="font-serif font-semibold text-base text-ink">${escapeHtml(niceDocType)}</div>
      <div class="space-y-1.5">${fields}</div>
      <div class="p-3 bg-ochreSoft/70 border border-ochre/20 rounded-lg text-[11px] text-ochre leading-relaxed">${escapeHtml(data.authenticity_disclaimer)}</div>
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
  // Account Sign-In, Study Mode Switcher & Personal Study Desk
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
      ? 'px-3.5 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs'
      : 'px-3.5 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink';
    document.getElementById('submodePublicBtn').className = !isPriv
      ? 'px-3.5 py-1.5 text-xs font-semibold rounded-md bg-white text-ink shadow-xs'
      : 'px-3.5 py-1.5 text-xs font-medium rounded-md text-muted hover:text-ink';
  }

  function applyAuthUIState() {
    const loggedIn = Boolean(currentUser);
    document.getElementById('authSignInBtn').classList.toggle('hidden', loggedIn);
    document.getElementById('authUserMenu').classList.toggle('hidden', !loggedIn);
    document.getElementById('headerModeSelect').classList.toggle('hidden', !loggedIn);
    document.getElementById('privateAuthGate').classList.toggle('hidden', loggedIn);
    document.getElementById('privateWorkspaceGrid').classList.toggle('hidden', !loggedIn);

    if (loggedIn) {
      activeSessionId = 'user:' + currentUser.id;
      const mc = currentUser.mode_config || {};
      const sel = document.getElementById('headerModeSelect');
      sel.value = currentUser.user_mode || 'student';

      document.getElementById('authUserName').innerText = currentUser.full_name || 'Account';
      document.getElementById('authUserAvatar').innerText = (currentUser.full_name || 'U').charAt(0).toUpperCase();
      document.getElementById('authDropName').innerText = currentUser.full_name || '';
      document.getElementById('authDropEmail').innerText = currentUser.email || '';

      const pBadge = document.getElementById('privateModeBadge');
      pBadge.innerText = mc.display_name || 'Student Mode';
      document.getElementById('privateModeDesc').innerText = mc.description || '';
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
      showToast(`Signed in as ${currentUser.full_name}.`, 'success');
    } catch (e) {
      showToast('Sign-in failed. Check your email and try again.', 'error');
    }
  }

  async function handleModeSwitch(newMode) {
    try {
      const res = await authFetch('/api/auth/mode', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_mode: newMode })
      });
      if (!res.ok) throw new Error('Mode switch failed');
      const data = await res.json();
      currentUser = data.user;
      applyAuthUIState();
      showToast(`Switched to ${currentUser.mode_config?.display_name || newMode}.`, 'info');
    } catch (e) {
      showToast('Could not switch mode right now.', 'error');
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
      document.getElementById('privateDocCount').innerText = `${docs.length} file${docs.length === 1 ? '' : 's'}`;
      const listEl = document.getElementById('privateDocsList');
      if (!docs.length) {
        listEl.innerHTML = '<div class="p-4 border border-dashed border-line rounded-lg text-center text-xs text-muted">No documents added yet.</div>';
        return;
      }
      const badgeStyles = {
        indexed: 'bg-sageSoft text-sage',
        processing: 'bg-slateSoft text-slateBlue animate-pulse',
        pending: 'bg-ochreSoft text-ochre',
        failed: 'bg-crimsonSoft text-crimson'
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
        url: 'Web link',
        arxiv: 'Paper'
      };
      listEl.innerHTML = docs.map(d => `
        <div class="p-3 bg-paper/70 border border-line rounded-lg flex items-center justify-between gap-2">
          <div class="min-w-0">
            <div class="font-medium text-ink truncate" title="${escapeHtml(d.title)}">${escapeHtml(d.title)}</div>
            <div class="flex items-center gap-2 mt-1 text-[11px]">
              <span class="px-2 py-0.5 rounded-full font-medium ${badgeStyles[d.status] || 'bg-parchment text-muted'}">${escapeHtml(statusText[d.status] || d.status)}</span>
              <span class="text-muted">${escapeHtml(typeLabels[d.source_type] || 'Document')}</span>
            </div>
            ${d.status === 'failed' && d.error_message ? `<div class="text-[11px] text-crimson mt-1 truncate" title="${escapeHtml(d.error_message)}">${escapeHtml(d.error_message)}</div>` : ''}
          </div>
          <button onclick="deletePrivateDocument('${escapeHtml(d.id)}')" class="p-1 rounded-md text-muted hover:text-crimson hover:bg-crimsonSoft shrink-0" title="Remove document">&times;</button>
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
      showToast(`Added "${data.document?.title || 'link'}" to your documents.`, 'success');
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
        el.innerHTML = '<div class="text-xs text-muted">Ask a question to start saving your chats.</div>';
        return;
      }
      el.innerHTML = list.map(s => `
        <div class="flex items-center gap-1 rounded-lg border ${s.id === activePrivateSessionId ? 'bg-claySoft border-clay/30 text-clayDark font-medium' : 'bg-paper/60 border-line hover:bg-parchment/60 text-ink'}">
          <button onclick="openPrivateSession('${escapeHtml(s.id)}')" class="flex-1 min-w-0 text-left px-3 py-2 flex items-center justify-between gap-2">
            <span class="truncate">${escapeHtml(s.title)}</span>
            <span class="text-[10px] capitalize text-muted shrink-0">${escapeHtml(s.user_mode)}</span>
          </button>
          <button onclick="deletePrivateSession('${escapeHtml(s.id)}')" class="px-2 py-2 text-muted hover:text-crimson shrink-0" title="Delete chat">&times;</button>
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
      <div class="p-4 bg-white border border-line rounded-xl text-xs text-muted leading-relaxed">
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
          box.insertAdjacentHTML('beforeend', `<div class="flex justify-end"><div class="max-w-[82%] px-3.5 py-2.5 rounded-2xl rounded-br-sm bg-ink text-paper text-xs sm:text-sm">${escapeHtml(m.content)}</div></div>`);
        } else {
          const wrap = document.createElement('div');
          wrap.className = 'p-4 bg-white border border-line rounded-2xl rounded-bl-sm text-xs sm:text-sm space-y-2 leading-relaxed';
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
      .replace(/^###\s+(.*)$/gm, '<div class="font-serif font-semibold text-base text-ink mt-1">$1</div>')
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold text-ink">$1</strong>')
      .replace(/\*([^*\n]+)\*/g, '<em class="text-muted">$1</em>')
      .replace(/`([^`\n]+)`/g, '<code class="px-1 py-0.5 rounded bg-parchment text-xs">$1</code>')
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
      <button onclick="openCitationChunk('${escapeHtml(c.doc_id)}', '${escapeHtml(c.chunk_id)}')" class="px-2.5 py-1 rounded-full bg-paper hover:bg-claySoft border border-line hover:border-clay/30 text-[11px] font-medium text-slateBlue inline-flex items-center gap-1">
        <span>[${idx + 1}] ${escapeHtml(c.doc_title.slice(0, 26))} &middot; p.${c.page_number}</span>
      </button>
    `).join('');
    return `<div class="pt-2.5 border-t border-line flex flex-wrap gap-1.5">${pills}</div>`;
  }

  async function openCitationChunk(docId, chunkId) {
    try {
      const res = await authFetch(`/api/saral/documents/${encodeURIComponent(docId)}/chunks/${encodeURIComponent(chunkId)}`);
      if (!res.ok) throw new Error('Could not open source');
      const data = await res.json();
      const ch = data.chunk;
      document.getElementById('citMetaBadges').innerHTML = `
        <span class="px-2.5 py-0.5 rounded-full bg-claySoft text-clayDark text-[11px] font-semibold">Page ${ch.page_number}</span>
        <span class="px-2.5 py-0.5 rounded-full bg-parchment text-muted text-[11px] font-medium">${escapeHtml(ch.section_header)}</span>
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

    box.insertAdjacentHTML('beforeend', `<div class="flex justify-end"><div class="max-w-[82%] px-3.5 py-2.5 rounded-2xl rounded-br-sm bg-ink text-paper text-xs sm:text-sm">${escapeHtml(query)}</div></div>`);
    const respCard = document.createElement('div');
    respCard.className = 'p-4 bg-white border border-line rounded-2xl rounded-bl-sm text-xs sm:text-sm space-y-2 leading-relaxed';
    respCard.innerHTML = '<div class="private-md-body text-xs text-muted animate-pulse">Thinking...</div><div class="private-cites"></div>';
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
            bodyNode.className = 'private-md-body leading-relaxed text-ink/90';
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
      respCard.innerHTML = '<div class="text-crimson text-xs font-medium">Could not generate a response right now. Please try again.</div>';
    } finally {
      btn.disabled = false;
    }
  }

  (async function init() {
    const sp = new URLSearchParams(window.location.search);
    const authReturned = sp.get('auth') === 'success';
    restoreFiltersFromUrl();
    await initAuthAndModes();
    await loadKanbanTracker();
    await updateStatsCounters();
    await fetchOpportunities();
    if (window.location.hash === '#assistant' || authReturned) {
      switchWorkspace('assistant');
      if (authReturned && currentUser) {
        showToast(`Welcome back, ${currentUser.full_name}.`, 'success');
        sp.delete('auth');
        const cleanQs = sp.toString();
        window.history.replaceState(null, '', cleanQs ? `${window.location.pathname}?${cleanQs}` : window.location.pathname);
      }
    }
  })();
</script>
</body>
</html>
"""
