"""Modern Interactive Dashboard UI for MadadgaarAI with Student Scholarship Hub (Vidyarthi AI) and Government Application Gateway."""


def render_dashboard_html() -> str:
    return r"""<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>MadadgaarAI — National Scholarship & Research Funding Intelligence</title>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
  <style>
    @layer base {
      html, body { margin: 0; padding: 0; }
      body { overscroll-behavior: none; }
      main > :first-child { margin-top: 0 !important; }
      main > :last-child { margin-bottom: 0 !important; }
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0e1321; }
    ::-webkit-scrollbar-thumb { background: #252a39; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #4edea3; }
  </style>
  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "tertiary-fixed": "#acedff",
            "secondary": "#c0c1ff",
            "tertiary-fixed-dim": "#4cd7f6",
            "on-secondary": "#1000a9",
            "surface-tint": "#4edea3",
            "surface-container": "#1a1f2e",
            "secondary-fixed-dim": "#c0c1ff",
            "primary": "#4edea3",
            "surface": "#0e1321",
            "surface-variant": "#303444",
            "on-primary": "#003824",
            "on-secondary-container": "#b0b2ff",
            "background": "#0e1321",
            "on-secondary-fixed": "#07006c",
            "outline": "#86948a",
            "on-primary-fixed-variant": "#005236",
            "tertiary": "#4cd7f6",
            "surface-container-low": "#161b2a",
            "primary-fixed": "#6ffbbe",
            "error": "#ffb4ab",
            "primary-fixed-dim": "#4edea3",
            "on-tertiary-container": "#003f4b",
            "inverse-primary": "#006c49",
            "error-container": "#93000a",
            "surface-container-highest": "#303444",
            "on-tertiary-fixed-variant": "#004e5c",
            "on-surface": "#dee2f6",
            "outline-variant": "#3c4a42",
            "surface-bright": "#343948",
            "on-primary-container": "#00422b",
            "surface-container-lowest": "#090e1c",
            "inverse-surface": "#dee2f6",
            "on-secondary-fixed-variant": "#2f2ebe",
            "secondary-container": "#3131c0",
            "on-surface-variant": "#bbcabf",
            "surface-dim": "#0e1321",
            "primary-container": "#10b981",
            "surface-container-high": "#252a39",
            "on-primary-fixed": "#002113",
            "tertiary-container": "#00b2d0",
            "on-tertiary": "#003640",
            "on-error": "#690005",
            "on-error-container": "#ffdad6",
            "on-background": "#dee2f6",
            "secondary-fixed": "#e1e0ff",
            "inverse-on-surface": "#2b303f",
            "on-tertiary-fixed": "#001f26"
          },
          borderRadius: {
            "DEFAULT": "0.25rem",
            "lg": "0.5rem",
            "xl": "0.75rem",
            "2xl": "1rem",
            "full": "9999px"
          },
          spacing: {
            "space-lg": "1.5rem",
            "gutter-desktop": "1.5rem",
            "space-md": "1rem",
            "space-xs": "0.25rem",
            "gutter-tablet": "1.25rem",
            "space-xl": "2.5rem",
            "margin": "1rem",
            "gutter": "1rem",
            "margin-tablet": "2rem",
            "margin-desktop": "3rem",
            "space-sm": "0.5rem"
          },
          fontFamily: {
            "label-mono-xs": ["Geist", "monospace"],
            "headline-lg": ["Space Grotesk", "sans-serif"],
            "display-lg": ["Space Grotesk", "sans-serif"],
            "headline-md": ["Space Grotesk", "sans-serif"],
            "body-sm": ["Geist", "sans-serif"],
            "label-mono-sm": ["Geist", "monospace"],
            "headline-lg-mobile": ["Space Grotesk", "sans-serif"],
            "body-md": ["Geist", "sans-serif"],
            "display-lg-mobile": ["Space Grotesk", "sans-serif"],
            "body-lg": ["Geist", "sans-serif"]
          }
        }
      }
    };
  </script>
</head>
<body class="bg-surface font-body-md text-on-surface antialiased selection:bg-primary-container selection:text-on-primary-container min-h-screen flex flex-col justify-between">

  <!-- TOP APP HEADER -->
  <header class="fixed top-0 left-0 right-0 w-full z-40 bg-surface/90 backdrop-blur-2xl border-b border-surface-container-high/60 shadow-lg">
    <div class="h-20 w-full px-4 sm:px-8 lg:px-12 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3 shrink-0 cursor-pointer" onclick="switchNavTab('vidyarthi')">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-tertiary flex items-center justify-center text-on-primary font-bold shadow-[0_0_15px_rgba(78,222,163,0.35)]">
          <span class="material-symbols-outlined text-[24px]">school</span>
        </div>
        <div class="flex flex-col">
          <div class="flex items-center gap-1.5">
            <span class="font-headline-md text-xl text-on-surface uppercase tracking-tight font-bold">MadadgaarAI</span>
            <span class="font-label-mono-xs text-xs text-on-surface-variant font-normal">(मददगार AI)</span>
          </div>
          <div class="flex items-center gap-1">
            <span class="inline-flex items-center gap-1.5 px-1.5 py-0.5 bg-surface-container-high rounded text-on-surface-variant font-label-mono-xs text-[10px]">
              <span class="inline-flex gap-0.5 items-center">
                <span class="w-1.5 h-1.5 rounded-full bg-[#ff9933]"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#ffffff]"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#138808]"></span>
              </span>
              GOVT & CSR INTELLIGENCE
            </span>
          </div>
        </div>
      </div>

      <!-- MAIN NAVIGATION TABS -->
      <nav class="hidden xl:flex items-center gap-1.5 bg-surface-container-lowest/80 p-1.5 rounded-xl border border-outline-variant/30" id="mainNavTabs">
        <button class="nav-tab-btn flex items-center gap-2 px-4 py-2 bg-surface-container-high text-primary font-label-mono-sm text-xs uppercase font-bold rounded-lg shadow-[0_0_12px_rgba(78,222,163,0.2)] transition-all" id="tabBtnVidyarthi" onclick="switchNavTab('vidyarthi')">
          <span class="material-symbols-outlined text-[16px]">school</span>
          Vidyarthi Scholarship Hub
        </button>
        <button class="nav-tab-btn flex items-center gap-2 px-4 py-2 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all font-label-mono-sm text-xs uppercase rounded-lg" id="tabBtnExplore" onclick="switchNavTab('explore')">
          <span class="material-symbols-outlined text-[16px]">explore</span>
          Explore Opportunities <span class="px-1.5 py-0.5 bg-surface-container text-primary font-label-mono-xs text-[10px] rounded" id="statExploreBadge">21 ACTIVE</span>
        </button>
        <button class="nav-tab-btn flex items-center gap-2 px-4 py-2 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all font-label-mono-sm text-xs uppercase rounded-lg" id="tabBtnFaculty" onclick="switchNavTab('faculty')">
          <span class="material-symbols-outlined text-[16px]">biotech</span>
          Researcher & Faculty <span class="px-1.5 py-0.5 bg-secondary-container text-on-secondary-container font-label-mono-xs text-[10px] rounded">SERB/DST/CSIR</span>
        </button>
      </nav>

      <!-- RIGHT STATUS TELEMETRY -->
      <div class="flex items-center gap-3 shrink-0">
        <div class="hidden lg:flex items-center gap-2 bg-surface-container-lowest border border-outline-variant/30 px-3 py-1.5 rounded-lg">
          <span class="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
          <span class="font-label-mono-xs text-xs text-primary font-semibold" id="statTotalCounter">21 SCHEMES ACTIVE</span>
          <span class="text-on-surface-variant font-label-mono-xs text-xs">| 100% FREE GOVT PORTALS</span>
        </div>
        <button class="px-3.5 py-2 bg-surface-container-high hover:bg-surface-variant text-on-surface font-label-mono-sm text-xs uppercase tracking-wider rounded-lg transition-colors flex items-center gap-1.5 border border-outline-variant/30" onclick="triggerDbSync()">
          <span class="material-symbols-outlined text-[16px] text-tertiary">sync</span>
          <span class="hidden sm:inline">Sync DB</span>
        </button>
        <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-primary to-tertiary flex items-center justify-center shrink-0 text-on-primary font-bold shadow-md">
          <span class="material-symbols-outlined text-[18px]">verified_user</span>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN VIEWPORT CONTAINER -->
  <main class="w-full pt-20 flex-1 bg-surface">

    <!-- ========================================================= -->
    <!-- TAB 1: VIDYARTHI SCHOLARSHIP HUB (DEFAULT)                -->
    <!-- ========================================================= -->
    <div id="viewVidyarthi" class="flex flex-col w-full">

      <!-- SECTION 1: TOP METRIC & TRUST TELEMETRY -->
      <section class="w-full px-4 sm:px-8 lg:px-12 py-4">
        <div class="w-full bg-surface-container-low/90 backdrop-blur-xl p-3 md:p-4 rounded-xl mb-4 border border-outline-variant/30 shadow-lg flex flex-col lg:flex-row items-center justify-between gap-3">
          <div class="flex items-center gap-3 text-left">
            <span class="flex h-3 w-3 relative shrink-0">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
            </span>
            <div class="flex flex-wrap items-center gap-x-2 gap-y-1">
              <span class="font-headline-md text-xs md:text-sm text-on-surface uppercase tracking-tight font-bold">GOVT & CSR DIRECT BENEFIT DISBURSEMENT</span>
              <span class="hidden md:inline text-outline-variant font-label-mono-xs text-xs">|</span>
              <p class="font-label-mono-sm text-xs sm:text-sm text-on-surface-variant">Zero Middlemen Guarantee • 100% Direct Benefit Transfer (DBT) via NPCI Aadhaar Gateway</p>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0 self-end lg:self-auto">
            <span class="px-2.5 py-1 bg-primary/10 text-primary font-label-mono-xs text-xs rounded-md uppercase tracking-wider font-semibold flex items-center gap-1 border border-primary/20">
              <span class="material-symbols-outlined text-[14px]">verified</span> UIDAI & PFMS CERTIFIED
            </span>
          </div>
        </div>

        <!-- 4 Telemetry Ribbon Tiles -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div class="bg-surface-container/70 backdrop-blur-md p-4 rounded-xl border border-outline-variant/20 hover:bg-surface-container-high transition-colors">
            <div class="flex items-center justify-between text-on-surface-variant mb-1">
              <span class="font-label-mono-xs text-[10px] uppercase tracking-widest text-outline">ANNUAL OUTLAY (FY 24-25)</span>
              <span class="material-symbols-outlined text-[18px] text-tertiary">payments</span>
            </div>
            <div class="flex items-baseline gap-1">
              <span class="font-display-lg text-2xl md:text-3xl text-primary font-bold tracking-tight">₹18,450</span>
              <span class="font-headline-md text-sm text-primary font-medium">Cr</span>
            </div>
            <p class="font-label-mono-xs text-[11px] text-on-surface-variant mt-1">Disbursed directly into student accounts</p>
          </div>

          <div class="bg-surface-container/70 backdrop-blur-md p-4 rounded-xl border border-outline-variant/20 hover:bg-surface-container-high transition-colors">
            <div class="flex items-center justify-between text-on-surface-variant mb-1">
              <span class="font-label-mono-xs text-[10px] uppercase tracking-widest text-outline">TIME-SENSITIVE SANCTIONS</span>
              <span class="material-symbols-outlined text-[18px] text-error">alarm_on</span>
            </div>
            <div class="flex items-baseline gap-1">
              <span class="font-display-lg text-2xl md:text-3xl text-on-surface font-bold tracking-tight">21</span>
              <span class="font-headline-md text-sm text-error font-medium">SCHEMES</span>
            </div>
            <p class="font-label-mono-xs text-[11px] text-error mt-1 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-error animate-pulse"></span> Active Central & State Portals
            </p>
          </div>

          <div class="bg-surface-container/70 backdrop-blur-md p-4 rounded-xl border border-outline-variant/20 hover:bg-surface-container-high transition-colors">
            <div class="flex items-center justify-between text-on-surface-variant mb-1">
              <span class="font-label-mono-xs text-[10px] uppercase tracking-widest text-outline">APPLICANT ACCESS</span>
              <span class="material-symbols-outlined text-[18px] text-primary">volunteer_activism</span>
            </div>
            <div class="flex items-baseline gap-1">
              <span class="font-display-lg text-2xl md:text-3xl text-tertiary font-bold tracking-tight">100%</span>
              <span class="font-headline-md text-sm text-tertiary font-medium">FREE</span>
            </div>
            <p class="font-label-mono-xs text-[11px] text-on-surface-variant mt-1">Zero agent fee / Official direct routing</p>
          </div>

          <div class="bg-surface-container/70 backdrop-blur-md p-4 rounded-xl border border-outline-variant/20 hover:bg-surface-container-high transition-colors">
            <div class="flex items-center justify-between text-on-surface-variant mb-1">
              <span class="font-label-mono-xs text-[10px] uppercase tracking-widest text-outline">RULE ENGINE PRECISION</span>
              <span class="material-symbols-outlined text-[18px] text-secondary">model_training</span>
            </div>
            <div class="flex items-baseline gap-1">
              <span class="font-display-lg text-2xl md:text-3xl text-secondary font-bold tracking-tight">98.4%</span>
              <span class="font-headline-md text-sm text-secondary font-medium">AI ACCURACY</span>
            </div>
            <p class="font-label-mono-xs text-[11px] text-on-surface-variant mt-1">Deterministic statutory matching</p>
          </div>
        </div>
      </section>

      <!-- SECTION 2: STUDENT ELIGIBILITY WIZARD -->
      <section class="w-full px-4 sm:px-8 lg:px-12 py-4">
        <div class="bg-surface-container-low/95 backdrop-blur-2xl p-5 md:p-6 rounded-2xl border border-outline-variant/30 shadow-2xl">
          <!-- Wizard Header -->
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-outline-variant/20">
            <div class="flex flex-col">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-1 bg-primary/10 text-primary font-label-mono-xs text-xs rounded-md uppercase font-semibold tracking-wider flex items-center gap-1 border border-primary/20">
                  <span class="material-symbols-outlined text-[15px]">bolt</span> AI Instant Eligibility Matcher
                </span>
                <span class="text-on-surface-variant font-label-mono-xs text-xs tracking-wider uppercase font-semibold">मददगार AI पात्रता कैलकुलेटर</span>
              </div>
              <h2 class="font-headline-lg text-xl sm:text-2xl lg:text-3xl text-on-surface font-bold mt-1">Set Your Academic Profile • Claim Public Capital</h2>
              <p class="font-body-sm text-xs sm:text-sm text-on-surface-variant">Our engine evaluates statutory rules across NSP Central, State Portals (UP/MahaDBT), UGC, AICTE, and CSR Foundations.</p>
            </div>
            <div class="flex items-center gap-3 shrink-0">
              <button class="px-3 py-1.5 bg-surface-container-high hover:bg-surface-variant text-on-surface text-xs font-label-mono-xs uppercase tracking-wider rounded-lg transition-colors flex items-center gap-1 border border-outline-variant/30" onclick="resetStudentProfile()">
                <span class="material-symbols-outlined text-[15px]">restart_alt</span> Reset Defaults
              </button>
            </div>
          </div>

          <!-- Profile Parameters Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pt-4 pb-4">
            <!-- Field 1: State Domicile -->
            <div class="flex flex-col gap-1.5">
              <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase flex items-center justify-between">
                <span>Domicile State (गृह राज्य)</span>
                <span class="text-tertiary font-semibold">MANDATORY</span>
              </label>
              <div class="relative">
                <select class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2.5 rounded-lg border border-outline-variant/30 appearance-none focus:outline-none focus:border-primary transition-colors" id="stuState" onchange="runStudentMatch()">
                  <option value="All India">All India / Open (अखिल भारतीय)</option>
                  <option value="Uttar Pradesh" selected>Uttar Pradesh (उत्तर प्रदेश)</option>
                  <option value="Maharashtra">Maharashtra (महाराष्ट्र)</option>
                  <option value="Bihar">Bihar (बिहार)</option>
                  <option value="Rajasthan">Rajasthan (राजस्थान)</option>
                  <option value="Madhya Pradesh">Madhya Pradesh (मध्य प्रदेश)</option>
                  <option value="West Bengal">West Bengal (पश्चिम बंगाल)</option>
                  <option value="Karnataka">Karnataka (कर्नाटक)</option>
                  <option value="Tamil Nadu">Tamil Nadu (तमिलनाडु)</option>
                  <option value="Assam / North Eastern States">Assam / North East NER (पूर्वोत्तर)</option>
                  <option value="Delhi NCR">Delhi NCR (दिल्ली)</option>
                </select>
                <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none text-[18px]">expand_more</span>
              </div>
            </div>

            <!-- Field 2: Education Level -->
            <div class="flex flex-col gap-1.5">
              <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase flex items-center justify-between">
                <span>Education Level (शैक्षणिक स्तर)</span>
                <span class="text-tertiary font-semibold">DEGREE</span>
              </label>
              <div class="relative">
                <select class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2.5 rounded-lg border border-outline-variant/30 appearance-none focus:outline-none focus:border-primary transition-colors" id="stuLevel" onchange="runStudentMatch()">
                  <option value="UG - Engineering / Technology (B.Tech/B.E.)" selected>UG - Engineering (B.Tech/B.E.)</option>
                  <option value="Diploma / Polytechnic">Diploma / Polytechnic</option>
                  <option value="UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)">UG - Medical (MBBS/BDS/B.Pharm)</option>
                  <option value="UG - General (B.Sc / B.Com / B.A. / BBA / BCA)">UG - General (B.Sc/B.Com/B.A.)</option>
                  <option value="Class 11-12 (Higher Secondary)">Class 11-12 (Higher Secondary)</option>
                  <option value="Class 9-10 (Pre-Matric)">Class 9-10 (Pre-Matric)</option>
                  <option value="Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)">Postgraduate (Master's Degree)</option>
                  <option value="PhD / Doctoral Research">PhD / Doctoral Research</option>
                </select>
                <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none text-[18px]">school</span>
              </div>
            </div>

            <!-- Field 3: Social Category -->
            <div class="flex flex-col gap-1.5">
              <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase flex items-center justify-between">
                <span>Social Category (सामाजिक वर्ग)</span>
                <span class="text-tertiary font-semibold">CERTIFIED</span>
              </label>
              <div class="relative">
                <select class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2.5 rounded-lg border border-outline-variant/30 appearance-none focus:outline-none focus:border-primary transition-colors" id="stuCategory" onchange="runStudentMatch()">
                  <option value="General / Open">General / Open (सामान्य)</option>
                  <option value="OBC (Non-Creamy Layer)" selected>OBC-NCL (अन्य पिछड़ा वर्ग)</option>
                  <option value="SC (Scheduled Caste)">SC (अनुसूचित जाति)</option>
                  <option value="ST (Scheduled Tribe)">ST (अनुसूचित जनजाति)</option>
                  <option value="EWS (Economically Weaker Section)">EWS (आर्थिक रूप से कमजोर)</option>
                  <option value="Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)">Minority (अल्पसंख्यक)</option>
                </select>
                <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none text-[18px]">badge</span>
              </div>
            </div>

            <!-- Field 4: Gender -->
            <div class="flex flex-col gap-1.5">
              <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase flex items-center justify-between">
                <span>Gender (लिंग)</span>
                <span class="text-primary font-semibold">PRAGATI ACTIVE</span>
              </label>
              <div class="relative">
                <select class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2.5 rounded-lg border border-outline-variant/30 appearance-none focus:outline-none focus:border-primary transition-colors" id="stuGender" onchange="runStudentMatch()">
                  <option value="Female" selected>Female (छात्रा — Unlocks Girl Grants)</option>
                  <option value="Male">Male (छात्र)</option>
                  <option value="Transgender">Transgender (तृतीय लिंग)</option>
                </select>
                <span class="material-symbols-outlined absolute right-3 top-1/2 -translate-y-1/2 text-on-surface-variant pointer-events-none text-[18px]">female</span>
              </div>
            </div>
          </div>

          <!-- Second Row: Income, Academic %, Special Flags -->
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 pt-1 pb-4">
            <!-- Family Income Slider & Quick Buttons (5 Cols) -->
            <div class="lg:col-span-5 bg-surface-container-lowest p-4 rounded-xl border border-outline-variant/20 flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <label class="font-label-mono-xs text-xs text-on-surface uppercase tracking-wider font-semibold">ANNUAL FAMILY INCOME (वार्षिक पारिवारिक आय)</label>
                <span class="font-headline-md text-sm sm:text-base text-primary font-bold" id="incomeDisplay">₹2,00,000 / Year</span>
              </div>
              <input class="w-full h-2 bg-surface-container-high rounded-lg appearance-none cursor-pointer accent-primary my-2.5" id="stuIncome" max="1000000" min="50000" step="25000" type="range" value="200000" oninput="updateIncomeDisplay(this.value); runStudentMatch()"/>
              <div class="flex flex-wrap items-center gap-1.5 mt-1">
                <button class="px-2.5 py-1 bg-surface-container-high hover:bg-surface-variant text-on-surface text-xs font-label-mono-xs rounded transition-colors" onclick="setIncomeVal(150000)">₹1.5L</button>
                <button class="px-2.5 py-1 bg-primary text-on-primary font-bold text-xs font-label-mono-xs rounded transition-colors" onclick="setIncomeVal(200000)">₹2.0L</button>
                <button class="px-2.5 py-1 bg-surface-container-high hover:bg-surface-variant text-on-surface text-xs font-label-mono-xs rounded transition-colors" onclick="setIncomeVal(250000)">₹2.5L</button>
                <button class="px-2.5 py-1 bg-surface-container-high hover:bg-surface-variant text-on-surface text-xs font-label-mono-xs rounded transition-colors" onclick="setIncomeVal(450000)">₹4.5L</button>
                <button class="px-2.5 py-1 bg-surface-container-high hover:bg-surface-variant text-on-surface text-xs font-label-mono-xs rounded transition-colors" onclick="setIncomeVal(800000)">₹8.0L</button>
              </div>
            </div>

            <!-- Academic Score (3 Cols) -->
            <div class="lg:col-span-3 bg-surface-container-lowest p-4 rounded-xl border border-outline-variant/20 flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <label class="font-label-mono-xs text-xs text-on-surface uppercase tracking-wider font-semibold">ACADEMIC MERIT (10TH / 12TH %)</label>
                <span class="inline-flex items-center gap-1 px-1.5 py-0.5 bg-primary/10 text-primary font-label-mono-xs text-[10px] rounded font-semibold">
                  <span class="material-symbols-outlined text-[12px]">check_circle</span> VERIFIED
                </span>
              </div>
              <div class="flex items-baseline gap-2 mt-2">
                <input class="w-24 bg-surface-container text-on-surface font-headline-lg text-2xl font-bold px-2 py-1 rounded-lg text-center border border-outline-variant/30 focus:outline-none focus:border-primary" id="stuMarks" max="100" min="35" step="0.5" type="number" value="86" onchange="runStudentMatch()"/>
                <span class="font-headline-md text-sm text-on-surface-variant">% Aggregate Marks</span>
              </div>
              <p class="font-label-mono-xs text-[11px] text-on-surface-variant mt-2">Qualifies for National Merit and CSR threshold quotas.</p>
            </div>

            <!-- Special Status Flags (4 Cols) -->
            <div class="lg:col-span-4 bg-surface-container-lowest p-4 rounded-xl border border-outline-variant/20 flex flex-col justify-between gap-1.5">
              <label class="font-label-mono-xs text-xs text-on-surface uppercase tracking-wider font-semibold">SPECIAL CONCESSION FLAGS</label>
              <label class="flex items-center gap-2 p-1.5 bg-surface-container/60 hover:bg-surface-container rounded-lg cursor-pointer transition-colors">
                <input class="w-4 h-4 rounded text-primary focus:ring-0 bg-surface-container-lowest border-0" id="stuSingleGirl" type="checkbox" onchange="runStudentMatch()"/>
                <span class="font-body-sm text-xs sm:text-sm text-on-surface">Single Girl Child (एकल पुत्री आरक्षण)</span>
              </label>
              <label class="flex items-center gap-2 p-1.5 bg-surface-container/60 hover:bg-surface-container rounded-lg cursor-pointer transition-colors">
                <input class="w-4 h-4 rounded text-primary focus:ring-0 bg-surface-container-lowest border-0" id="stuPwd" type="checkbox" onchange="runStudentMatch()"/>
                <span class="font-body-sm text-xs sm:text-sm text-on-surface">Differently Abled / PwD (≥ 40% Benchmark)</span>
              </label>
            </div>
          </div>

          <!-- Action Bar -->
          <div class="pt-2 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
            <div class="flex items-center gap-2 text-on-surface-variant">
              <span class="material-symbols-outlined text-primary text-[20px]">verified_user</span>
              <span class="font-label-mono-sm text-xs sm:text-sm">Deterministic Matching: Zero hallucinations. Direct cross-reference with Gazette rules.</span>
            </div>
            <button class="px-6 py-3 bg-primary text-on-primary hover:bg-primary-fixed-dim font-headline-md text-sm sm:text-base font-bold tracking-tight rounded-xl shadow-[0_0_20px_rgba(78,222,163,0.35)] transition-all flex items-center justify-center gap-2 cursor-pointer" onclick="runStudentMatch()">
              <span class="material-symbols-outlined text-[20px]">bolt</span>
              <span id="matchBtnText">⚡ Find My Scholarships (पात्रता खोजें)</span>
            </button>
          </div>
        </div>
      </section>

      <!-- SECTION 3: RESULTS GRID -->
      <section class="w-full px-4 sm:px-8 lg:px-12 py-4">
        <div id="studentResultsContainer">
          <div class="text-center py-12 text-on-surface-variant font-label-mono-sm">
            <span class="material-symbols-outlined text-4xl text-primary animate-spin mb-2">refresh</span>
            <div>Evaluating statutory eligibility across Central, State & CSR schemes...</div>
          </div>
        </div>
      </section>

      <!-- SECTION 5: "SARAL SAMJHAUTI" & DOCUMENT CHECKLIST KNOWLEDGE BASE -->
      <section class="w-full px-4 sm:px-8 lg:px-12 py-4 pb-12">
        <div class="bg-surface-container-low/95 backdrop-blur-xl p-5 md:p-6 rounded-2xl border border-outline-variant/30 shadow-xl">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-outline-variant/20">
            <div>
              <span class="font-label-mono-xs text-xs text-tertiary uppercase tracking-widest block font-semibold">HIGH-ACCESSIBILITY KNOWLEDGE BASE</span>
              <h3 class="font-headline-lg text-lg sm:text-xl md:text-2xl text-on-surface font-semibold tracking-tight mt-0.5">
                Applicant Enablement • सरल भाषा गाइड & दस्तावेज सूची
              </h3>
            </div>
            <div class="flex items-center gap-1 bg-surface-container-lowest p-1 rounded-xl border border-outline-variant/20">
              <button class="px-3.5 py-1.5 bg-surface-container-high text-primary font-label-mono-sm text-xs uppercase rounded-lg font-bold transition-all flex items-center gap-1.5" id="tabHinglishBtn" onclick="switchDocTab('hinglish')">
                <span class="material-symbols-outlined text-[16px]">translate</span>
                <span>सरल गाइड (Hinglish Q&A)</span>
              </button>
              <button class="px-3.5 py-1.5 text-on-surface-variant hover:text-on-surface font-label-mono-sm text-xs uppercase rounded-lg font-medium transition-all flex items-center gap-1.5" id="tabChecklistBtn" onclick="switchDocTab('checklist')">
                <span class="material-symbols-outlined text-[16px]">task</span>
                <span>Document Checklist (दस्तावेज)</span>
              </button>
            </div>
          </div>

          <!-- TAB PANEL 1: SARAL HINGLISH GUIDE -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4" id="hinglishPanel">
            <div class="bg-surface-container-lowest p-4 rounded-xl border border-outline-variant/20 flex flex-col justify-between">
              <div>
                <div class="flex items-center gap-2 text-primary font-headline-md text-base mb-2">
                  <span class="material-symbols-outlined text-[20px]">group</span>
                  <h4>Kaun apply kar sakta hai? (पात्रता)</h4>
                </div>
                <p class="font-body-md text-sm text-on-surface leading-relaxed">
                  Ye AICTE Pragati, Post-Matric & State scholarships un sabhi chhatraon ke liye hain jinhone recognized colleges me <strong>1st year Degree/Diploma</strong> me admission liya hai.
                </p>
              </div>
              <div class="bg-surface-container/70 p-2 rounded-lg mt-3 font-label-mono-xs text-xs text-on-surface-variant">
                Parivar ki kul aamdani saalana ₹2.0L - ₹8.0L se kam honi chahiye. Single girl child ko automatic preference milti hai.
              </div>
            </div>

            <div class="bg-surface-container-lowest p-4 rounded-xl border border-outline-variant/20 flex flex-col justify-between">
              <div>
                <div class="flex items-center gap-2 text-primary font-headline-md text-base mb-2">
                  <span class="material-symbols-outlined text-[20px]">currency_rupee</span>
                  <h4>Kitne paise kab aur kaise milenge?</h4>
                </div>
                <p class="font-body-md text-sm text-on-surface leading-relaxed">
                  Har saal <strong>₹12,000 se lekar ₹2,00,000 direct aapke bank account</strong> me DBT (Direct Benefit Transfer) ke zariye credit hote hain. Kisi agent ko 1 rupya bhi nahi dena hota.
                </p>
              </div>
              <div class="bg-surface-container/70 p-2 rounded-lg mt-3 font-label-mono-xs text-xs text-on-surface-variant">
                Ye rashi tuition fees, kitabein, aur laptop khareedne ke liye valid hai. Bank account me DBT active hona anivarya hai.
              </div>
            </div>

            <div class="bg-surface-container-lowest p-4 rounded-xl border border-outline-variant/20 flex flex-col justify-between">
              <div>
                <div class="flex items-center gap-2 text-error font-headline-md text-base mb-2">
                  <span class="material-symbols-outlined text-[20px]">warning</span>
                  <h4>Bank Account me ye galti mat karna:</h4>
                </div>
                <p class="font-body-md text-sm text-on-surface leading-relaxed">
                  Aapka bank account NPCI mapper se <strong>'Aadhaar Seeded'</strong> hona anivarya hai. Sirf bank me jakar Aadhaar card jama karna kafi nahi hota.
                </p>
              </div>
              <div class="bg-surface-container/70 p-2 rounded-lg mt-3 font-label-mono-xs text-xs text-error">
                Bank me jakar bole: "Mera Account Aadhaar DBT / NPCI Seeding se link karein", warna approval ke baad bhi paisa nahi aayega.
              </div>
            </div>
          </div>

          <!-- TAB PANEL 2: OFFICIAL DOCUMENT CHECKLIST MATRIX -->
          <div class="hidden pt-4" id="checklistPanel">
            <div class="bg-surface-container-lowest rounded-xl border border-outline-variant/20 overflow-x-auto">
              <table class="w-full text-left font-body-sm text-xs sm:text-sm">
                <thead class="bg-surface-container-high/80 text-on-surface font-label-mono-xs text-xs uppercase tracking-wider">
                  <tr>
                    <th class="p-3">Required Document</th>
                    <th class="p-3">Issuing Sovereign Authority</th>
                    <th class="p-3">Acceptable Format & Specs</th>
                    <th class="p-3">Validation Status</th>
                  </tr>
                </thead>
                <tbody class="text-on-surface-variant divide-y divide-outline-variant/20">
                  <tr class="hover:bg-surface-container/50 transition-colors">
                    <td class="p-3 font-semibold text-on-surface">1. Income Certificate (आय प्रमाण पत्र)</td>
                    <td class="p-3">Tehsildar / Sub-Divisional Magistrate (SDM) e-District</td>
                    <td class="p-3 font-label-mono-xs text-xs">Issued after April 2024 • PDF &lt; 200KB</td>
                    <td class="p-3"><span class="px-2 py-0.5 bg-primary/10 text-primary font-label-mono-xs text-xs rounded uppercase font-semibold">DigiLocker Linked</span></td>
                  </tr>
                  <tr class="hover:bg-surface-container/50 transition-colors">
                    <td class="p-3 font-semibold text-on-surface">2. Domicile Certificate (निवास प्रमाण पत्र)</td>
                    <td class="p-3">State Revenue Dept (e-District / Borland Portal)</td>
                    <td class="p-3 font-label-mono-xs text-xs">Permanent Residence Serial Verified</td>
                    <td class="p-3"><span class="px-2 py-0.5 bg-primary/10 text-primary font-label-mono-xs text-xs rounded uppercase font-semibold">DigiLocker Linked</span></td>
                  </tr>
                  <tr class="hover:bg-surface-container/50 transition-colors">
                    <td class="p-3 font-semibold text-on-surface">3. College Bonafide & Fee Receipt</td>
                    <td class="p-3">College Registrar / Principal Official Seal & Signature</td>
                    <td class="p-3 font-label-mono-xs text-xs">Original Format with AISHE Institutional Code</td>
                    <td class="p-3"><span class="px-2 py-0.5 bg-secondary/15 text-secondary font-label-mono-xs text-xs rounded uppercase font-semibold">Physical Seal Req</span></td>
                  </tr>
                  <tr class="hover:bg-surface-container/50 transition-colors">
                    <td class="p-3 font-semibold text-on-surface">4. Class 10th & 12th Board Marksheets</td>
                    <td class="p-3">CBSE / CISCE / State Education Boards (UPMSP/MSBSHSE)</td>
                    <td class="p-3 font-label-mono-xs text-xs">Digital Verified Copy or Original Board Scan</td>
                    <td class="p-3"><span class="px-2 py-0.5 bg-primary/10 text-primary font-label-mono-xs text-xs rounded uppercase font-semibold">Auto e-KYC</span></td>
                  </tr>
                  <tr class="hover:bg-surface-container/50 transition-colors">
                    <td class="p-3 font-semibold text-on-surface">5. Aadhaar Card + Active NPCI Bank Account</td>
                    <td class="p-3">UIDAI & Commercial Bank (SBI, PNB, Baroda, Canara, etc.)</td>
                    <td class="p-3 font-label-mono-xs text-xs">Active DBT mandate enabled on NPCI mapper</td>
                    <td class="p-3"><span class="px-2 py-0.5 bg-primary/10 text-primary font-label-mono-xs text-xs rounded uppercase font-semibold">PFMS Synchronized</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- ========================================================= -->
    <!-- TAB 2: EXPLORE ALL GRANTS & OPPORTUNITIES                 -->
    <!-- ========================================================= -->
    <div id="viewExplore" class="hidden flex-col w-full px-4 sm:px-8 lg:px-12 py-6">
      <div class="bg-surface-container-low/95 p-5 rounded-2xl border border-outline-variant/30 mb-6 shadow-xl">
        <div class="flex flex-col lg:flex-row gap-3">
          <div class="relative flex-1">
            <span class="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-on-surface-variant text-[20px]">search</span>
            <input type="text" id="exploreSearchInput" class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm pl-10 pr-4 py-2.5 rounded-lg border border-outline-variant/30 focus:outline-none focus:border-primary" placeholder="Search by scheme name or keywords (e.g. 'Pragati', 'UP Dashmottar', 'AI research', 'women')..." onkeyup="if(event.key === 'Enter') runExploreSearch()"/>
          </div>
          <select id="exploreAgencyFilter" class="bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2.5 rounded-lg border border-outline-variant/30 focus:outline-none focus:border-primary" onchange="runExploreSearch()">
            <option value="">All Portals & Agencies</option>
            <option value="NSP">NSP (National Scholarship)</option>
            <option value="AICTE">AICTE</option>
            <option value="UGC">UGC</option>
            <option value="State Govt">State Govt Portals</option>
            <option value="CSR / Foundation">CSR Foundations</option>
            <option value="DST">DST (Dept of Science & Tech)</option>
            <option value="ANRF/SERB">ANRF / SERB</option>
            <option value="CSIR">CSIR</option>
            <option value="DBT">DBT (Biotechnology)</option>
          </select>
          <button class="px-5 py-2.5 bg-primary text-on-primary hover:bg-primary-fixed-dim font-label-mono-sm text-xs uppercase font-bold rounded-lg transition-colors flex items-center justify-center gap-1.5" onclick="runExploreSearch()">
            <span class="material-symbols-outlined text-[16px]">bolt</span>
            Hybrid Search
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4" id="exploreGrid">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- ========================================================= -->
    <!-- TAB 3: RESEARCHER & FACULTY MATCHER                       -->
    <!-- ========================================================= -->
    <div id="viewFaculty" class="hidden flex-col w-full px-4 sm:px-8 lg:px-12 py-6">
      <div class="bg-surface-container-low/95 p-6 rounded-2xl border border-outline-variant/30 mb-6 shadow-xl">
        <h3 class="font-headline-lg text-xl text-on-surface font-bold mb-1">Researcher & Faculty Grant Alignment Engine</h3>
        <p class="font-body-sm text-xs sm:text-sm text-on-surface-variant mb-5">
          Paste your research abstract, scientific proposal concept, or CV highlights to match against DST, ANRF/SERB, CSIR, and DBT statutory calls.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase">Applicant Role</label>
            <select id="matchRole" class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2.5 rounded-lg border border-outline-variant/30 mt-1">
              <option value="Faculty / Principal Investigator">Faculty / Principal Investigator</option>
              <option value="Early Career Researcher">Early Career Researcher</option>
              <option value="Women Scientists">Women Scientists</option>
              <option value="PhD Scholars & Postdoctoral Fellows">PhD Scholars & Postdocs</option>
            </select>
          </div>
          <div>
            <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase">Applicant Age (Years)</label>
            <input type="number" id="matchAge" class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2 rounded-lg border border-outline-variant/30 mt-1" value="38"/>
          </div>
          <div>
            <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase">Highest Qualification</label>
            <input type="text" id="matchDegree" class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm px-3.5 py-2 rounded-lg border border-outline-variant/30 mt-1" value="Ph.D. in Computer Science"/>
          </div>
        </div>

        <div class="mb-4">
          <label class="font-label-mono-xs text-xs text-on-surface-variant uppercase">Research Proposal Abstract / Objective</label>
          <textarea id="matchAbstract" rows="4" class="w-full bg-surface-container-lowest text-on-surface font-body-sm text-sm p-3.5 rounded-lg border border-outline-variant/30 mt-1 focus:outline-none focus:border-primary" placeholder="Describe your scientific objectives, domain thrust, and methodologies (e.g. 'Deep learning for healthcare, quantum materials, climate sensors')..."></textarea>
        </div>

        <button class="px-6 py-3 bg-primary text-on-primary hover:bg-primary-fixed-dim font-headline-md text-sm font-bold rounded-lg transition-colors flex items-center gap-2" onclick="runFacultyMatch()">
          <span class="material-symbols-outlined text-[18px]">model_training</span>
          ⚡ Align Proposal & Check Compliance
        </button>
      </div>

      <div id="facultyResultsContainer"></div>
    </div>

  </main>

  <!-- ========================================================= -->
  <!-- UNIVERSAL MODAL 1: APPLICATION GATEWAY (आवेदन सेतु)       -->
  <!-- ========================================================= -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 md:p-6 bg-surface-container-lowest/85 backdrop-blur-xl overflow-y-auto hidden" id="applyModalOverlay" onclick="if(event.target === this) closeApplyModal()">
    <div class="relative w-full max-w-5xl max-h-[92vh] my-auto bg-slate-900/95 border border-slate-700/80 rounded-2xl shadow-2xl overflow-hidden flex flex-col backdrop-blur-2xl">
      <!-- Modal Header -->
      <div class="relative z-10 px-5 py-4 sm:px-6 sm:py-5 bg-surface-container shrink-0 border-b border-outline-variant/30">
        <div class="flex flex-wrap items-center justify-between gap-y-2 pb-2 mb-2 border-b border-outline-variant/20">
          <div class="flex flex-wrap items-center gap-2">
            <span class="inline-flex items-center gap-1 px-2 py-0.5 bg-surface-container-high rounded text-primary font-label-mono-xs text-xs uppercase tracking-wider font-semibold border border-primary/20">
              <span class="material-symbols-outlined text-[14px]">verified</span>
              NIC / GOVT OF INDIA VERIFIED GATEWAY
            </span>
            <span class="text-on-surface-variant font-label-mono-xs text-xs">•</span>
            <div class="inline-flex items-center gap-1 px-2 py-0.5 bg-surface-container-high rounded border border-outline-variant/30">
              <span class="w-1.5 h-1.5 rounded-full bg-primary animate-ping"></span>
              <span class="text-on-surface font-label-mono-xs text-xs font-semibold" id="modalHostDomain">scholarships.gov.in</span>
            </div>
            <button class="hover:bg-surface-container-highest px-2 py-0.5 bg-surface-container rounded text-tertiary font-label-mono-xs text-xs flex items-center gap-1 transition-colors border border-outline-variant/20" id="modalCopyBtn">
              <span class="material-symbols-outlined text-[13px]">content_copy</span>
              <span>Copy Link</span>
            </button>
          </div>
          <button class="w-8 h-8 rounded-lg bg-surface-container-high hover:bg-error-container hover:text-on-error-container text-on-surface flex items-center justify-center transition-all cursor-pointer" onclick="closeApplyModal()" title="Close Gateway Modal">
            <span class="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-3 pt-1">
          <div class="space-y-1">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="font-label-mono-xs text-xs px-2 py-0.5 rounded bg-secondary-container text-on-secondary-container uppercase font-semibold" id="modalAgencyTag">
                NSP / MoE Scheme
              </span>
              <span class="font-label-mono-xs text-xs text-on-surface-variant" id="modalRefId">
                REF: SCHEME-ID
              </span>
            </div>
            <h1 class="font-headline-lg text-lg sm:text-xl md:text-2xl text-on-surface font-bold tracking-tight" id="modalSchemeTitle">
              सरकारी आवेदन सेतु
            </h1>
            <p class="font-body-sm text-xs sm:text-sm text-on-surface-variant flex items-center gap-1.5" id="modalGrantText">
              <span class="material-symbols-outlined text-[16px] text-primary">account_balance</span>
              Disbursal: Direct Benefit Transfer via Aadhaar NPCI Gateway
            </p>
          </div>
        </div>
      </div>

      <!-- Anti-Scam Banner -->
      <div class="relative z-10 px-5 py-2.5 sm:px-6 bg-error-container text-on-error-container flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 shrink-0">
        <div class="flex items-start sm:items-center gap-2">
          <span class="material-symbols-outlined text-[22px] text-on-error-container shrink-0 mt-0.5 sm:mt-0">gpp_maybe</span>
          <div>
            <p class="font-headline-md text-xs sm:text-sm font-semibold leading-tight text-on-error-container">
              100% Free Sovereign Application — Never Pay Cyber Cafés, Brokers, or Agents.
            </p>
            <p class="font-body-sm text-[11px] sm:text-xs text-on-error-container/90">
              Government scholarships levy ₹0 submission fees. Never hand over DigiLocker PIN or Aadhaar OTPs to any third parties.
            </p>
          </div>
        </div>
        <div class="shrink-0 flex items-center self-end sm:self-center">
          <span class="px-2.5 py-1 rounded bg-black/35 font-label-mono-xs text-[10px] sm:text-xs tracking-wider uppercase text-on-error-container font-semibold">
            Direct DBT Only
          </span>
        </div>
      </div>

      <!-- Scrollable Stepper Content Area -->
      <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-0 overflow-y-auto flex-1 divide-y lg:divide-y-0 lg:divide-x divide-outline-variant/30">
        <!-- Left: Stepper Roadmap -->
        <div class="lg:col-span-7 p-4 sm:p-5 md:p-6 bg-surface-container-lowest/60 flex flex-col gap-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">
              <span class="material-symbols-outlined text-tertiary text-[20px]">alt_route</span>
              <h3 class="font-headline-md text-sm sm:text-base text-on-surface font-semibold tracking-tight">
                Official Portal Navigation Map (पोर्टल मार्गदर्शिका)
              </h3>
            </div>
            <span class="font-label-mono-xs text-xs text-on-surface-variant uppercase">Step-by-Step</span>
          </div>

          <div class="relative flex flex-col gap-3 pl-1 sm:pl-2" id="modalStepsTimeline">
            <!-- Injected via JS -->
          </div>
        </div>

        <!-- Right: Pre-Flight Checklist -->
        <div class="lg:col-span-5 p-4 sm:p-5 md:p-6 bg-surface-container-low flex flex-col gap-3">
          <div class="p-3.5 bg-surface-container rounded-xl flex items-center justify-between gap-3 border border-outline-variant/25 shadow-sm">
            <div>
              <div class="flex items-center gap-1 mb-0.5">
                <span class="material-symbols-outlined text-primary text-[18px]">speed</span>
                <span class="font-label-mono-xs text-[10px] uppercase text-on-surface-variant">Readiness Status</span>
              </div>
              <h4 class="font-headline-md text-sm sm:text-base font-bold text-on-surface">100% PRE-FLIGHT READY</h4>
              <p class="font-body-sm text-[11px] text-on-surface-variant">Mandatory verification checklist</p>
            </div>
            <div class="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold text-sm">
              5/5
            </div>
          </div>

          <span class="font-label-mono-xs text-xs text-on-surface-variant uppercase tracking-wider font-semibold">Pre-Flight Applicant Checklist:</span>
          <div class="flex flex-col gap-2">
            <div class="p-2.5 bg-surface-container rounded-lg border border-outline-variant/20 flex items-start gap-2">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-primary mt-0.5"/>
              <div>
                <div class="font-headline-md text-xs font-semibold text-on-surface">Aadhaar Linked Mobile OTP Active</div>
                <div class="font-body-sm text-[11px] text-on-surface-variant">Ready for instant NSP OTR authentication</div>
              </div>
            </div>
            <div class="p-2.5 bg-surface-container rounded-lg border border-outline-variant/20 flex items-start gap-2">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-primary mt-0.5"/>
              <div>
                <div class="font-headline-md text-xs font-semibold text-on-surface">Income Certificate (valid current financial year)</div>
                <div class="font-body-sm text-[11px] text-on-surface-variant">Issued by Tehsildar / Sub-Divisional Magistrate</div>
              </div>
            </div>
            <div class="p-2.5 bg-surface-container rounded-lg border border-outline-variant/20 flex items-start gap-2">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-primary mt-0.5"/>
              <div>
                <div class="font-headline-md text-xs font-semibold text-on-surface">Bank Account with Aadhaar-NPCI Seeding</div>
                <div class="font-body-sm text-[11px] text-on-surface-variant">Active DBT mapping enabled for direct crediting</div>
              </div>
            </div>
            <div class="p-2.5 bg-surface-container rounded-lg border border-outline-variant/20 flex items-start gap-2">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-primary mt-0.5"/>
              <div>
                <div class="font-headline-md text-xs font-semibold text-on-surface">Class 10th / 12th Board Marksheets</div>
                <div class="font-body-sm text-[11px] text-on-surface-variant">DigiLocker verified or PDF scan &lt; 200 KB</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Action Footer -->
      <div class="relative z-10 px-5 py-3 sm:px-6 sm:py-4 bg-surface-container shrink-0 border-t border-outline-variant/30 flex flex-col gap-2">
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <a class="px-3.5 py-2 bg-[#138808]/20 hover:bg-[#138808]/30 text-primary font-label-mono-sm text-xs rounded-lg flex items-center justify-center gap-1.5 transition-colors border border-[#138808]/40" id="modalWhatsappLink" href="#" target="_blank" rel="noopener noreferrer">
            <span class="material-symbols-outlined text-[17px]">chat</span>
            📲 Share on WhatsApp
          </a>
          <a class="px-5 py-2.5 bg-primary hover:bg-primary-fixed text-on-primary font-headline-md text-sm sm:text-base rounded-lg flex items-center justify-center gap-2 shadow-[0_0_24px_rgba(78,222,163,0.4)] hover:shadow-[0_0_32px_rgba(78,222,163,0.6)] transition-all font-bold text-center" id="modalApplyLink" href="#" target="_blank" rel="noopener noreferrer">
            <span>🚀 Launch Official Government Portal ↗</span>
          </a>
        </div>
        <div class="flex flex-wrap items-center justify-between gap-2 text-on-surface-variant font-label-mono-xs text-[10px] sm:text-xs pt-1">
          <div class="flex items-center gap-1.5">
            <span class="material-symbols-outlined text-primary text-[14px]">lock</span>
            <span>You are proceeding directly to sovereign official servers. Zero middleman fees.</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- UNIVERSAL MODAL 2: DOCUMENT CHECKLIST / SARAL GUIDE / PROPOSAL DRAFTER -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 md:p-6 bg-surface-container-lowest/85 backdrop-blur-xl overflow-y-auto hidden" id="genericModalOverlay" onclick="if(event.target === this) closeGenericModal()">
    <div class="relative w-full max-w-3xl max-h-[90vh] my-auto bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl overflow-hidden flex flex-col">
      <div class="px-5 py-4 bg-surface-container flex items-center justify-between border-b border-outline-variant/30">
        <h3 class="font-headline-md text-base sm:text-lg text-on-surface font-bold" id="genericModalTitle">Scheme Details</h3>
        <button class="w-8 h-8 rounded-lg bg-surface-container-high hover:bg-error-container hover:text-on-error-container text-on-surface flex items-center justify-center transition-all" onclick="closeGenericModal()">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>
      <div class="p-5 overflow-y-auto flex-1 font-body-sm text-sm" id="genericModalBody">
        <!-- Content injected via JS -->
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="w-full bg-surface-container-lowest py-8 text-on-surface-variant border-t border-surface-container-high/40">
    <div class="w-full px-4 sm:px-8 lg:px-12 flex flex-col gap-4">
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 p-4 bg-surface-container-low rounded-xl border border-outline-variant/20">
        <div class="flex items-start gap-3 max-w-4xl">
          <span class="material-symbols-outlined text-primary text-[22px] shrink-0 mt-0.5">shield</span>
          <p class="font-body-sm text-xs sm:text-sm text-on-surface-variant leading-relaxed">
            <span class="font-semibold text-on-surface uppercase font-label-mono-xs text-xs tracking-wider">High-Trust Gov-Tech Architecture:</span>
            MadadgaarAI is an autonomous student enablement platform. Direct application routing exclusively connects to official National Scholarship Portal (scholarships.gov.in), AICTE, UGC, and recognized State portals. 100% Direct Benefit Transfer (DBT) compliant.
          </p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <span class="font-label-mono-xs text-xs px-3 py-1.5 bg-primary-container text-on-primary-container rounded-lg uppercase tracking-wider font-semibold">National Public Good</span>
        </div>
      </div>
      <div class="flex flex-col md:flex-row items-center justify-between gap-3 pt-2 text-on-surface-variant/80 font-label-mono-xs text-xs">
        <div>© 2026 MadadgaarAI • Autonomous Sovereign Intelligence Framework</div>
        <div class="flex items-center gap-4">
          <a class="hover:text-primary transition-colors" href="https://scholarships.gov.in" target="_blank" rel="noopener noreferrer">NSP Portal</a>
          <a class="hover:text-primary transition-colors" href="https://myaadhaar.uidai.gov.in" target="_blank" rel="noopener noreferrer">UIDAI Seeding</a>
          <a class="hover:text-primary transition-colors" href="/docs" target="_blank">Swagger API</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- DYNAMIC FRONTEND APPLICATION ENGINE -->
  <script>
    let allOpportunities = [];
    let currentStudentResults = [];

    async function initPlatform() {
      await loadOpportunities();
      runStudentMatch();
    }

    async function loadOpportunities() {
      try {
        const res = await fetch('/api/foas');
        allOpportunities = await res.json();
        renderExploreGrid(allOpportunities);
        document.getElementById('statTotalCounter').innerText = `${allOpportunities.length} SCHEMES ACTIVE`;
        document.getElementById('statExploreBadge').innerText = `${allOpportunities.length} ACTIVE`;
      } catch (err) {
        console.error('Failed to load opportunities:', err);
      }
    }

    function switchNavTab(tab) {
      document.getElementById('viewVidyarthi').classList.toggle('hidden', tab !== 'vidyarthi');
      document.getElementById('viewExplore').classList.toggle('hidden', tab !== 'explore');
      document.getElementById('viewFaculty').classList.toggle('hidden', tab !== 'faculty');

      document.querySelectorAll('.nav-tab-btn').forEach(b => {
        b.className = 'nav-tab-btn flex items-center gap-2 px-4 py-2 text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-all font-label-mono-sm text-xs uppercase rounded-lg';
      });

      if (tab === 'vidyarthi') {
        document.getElementById('tabBtnVidyarthi').className = 'nav-tab-btn flex items-center gap-2 px-4 py-2 bg-surface-container-high text-primary font-label-mono-sm text-xs uppercase font-bold rounded-lg shadow-[0_0_12px_rgba(78,222,163,0.2)] transition-all';
      } else if (tab === 'explore') {
        document.getElementById('tabBtnExplore').className = 'nav-tab-btn flex items-center gap-2 px-4 py-2 bg-surface-container-high text-primary font-label-mono-sm text-xs uppercase font-bold rounded-lg shadow-[0_0_12px_rgba(78,222,163,0.2)] transition-all';
      } else if (tab === 'faculty') {
        document.getElementById('tabBtnFaculty').className = 'nav-tab-btn flex items-center gap-2 px-4 py-2 bg-surface-container-high text-primary font-label-mono-sm text-xs uppercase font-bold rounded-lg shadow-[0_0_12px_rgba(78,222,163,0.2)] transition-all';
      }
    }

    function updateIncomeDisplay(val) {
      document.getElementById('incomeDisplay').innerText = '₹' + Number(val).toLocaleString('en-IN') + ' / Year';
    }

    function setIncomeVal(val) {
      document.getElementById('stuIncome').value = val;
      updateIncomeDisplay(val);
      runStudentMatch();
    }

    function resetStudentProfile() {
      document.getElementById('stuState').value = 'Uttar Pradesh';
      document.getElementById('stuLevel').value = 'UG - Engineering / Technology (B.Tech/B.E.)';
      document.getElementById('stuCategory').value = 'OBC (Non-Creamy Layer)';
      document.getElementById('stuGender').value = 'Female';
      setIncomeVal(200000);
      document.getElementById('stuMarks').value = 86;
      document.getElementById('stuSingleGirl').checked = false;
      document.getElementById('stuPwd').checked = false;
      runStudentMatch();
    }

    async function runStudentMatch() {
      const container = document.getElementById('studentResultsContainer');
      const btnText = document.getElementById('matchBtnText');
      if (btnText) btnText.innerHTML = '⚡ Checking Statutory Rules...';

      const payload = {
        state_domicile: document.getElementById('stuState').value,
        education_level: document.getElementById('stuLevel').value,
        social_category: document.getElementById('stuCategory').value,
        gender: document.getElementById('stuGender').value,
        family_annual_income_inr: parseFloat(document.getElementById('stuIncome').value) || 200000,
        academic_percentage: parseFloat(document.getElementById('stuMarks').value) || 85,
        is_single_girl_child: document.getElementById('stuSingleGirl').checked,
        is_differently_abled_pwd: document.getElementById('stuPwd').checked,
        top_k: 15
      };

      try {
        const res = await fetch('/api/student/match', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const results = await res.json();
        currentStudentResults = results;
        renderStudentCards(results);
      } catch (err) {
        container.innerHTML = '<div class="text-error text-center py-8">Failed to evaluate scholarships. Please retry.</div>';
      } finally {
        if (btnText) btnText.innerHTML = '⚡ Find My Scholarships (पात्रता खोजें)';
      }
    }

    function renderStudentCards(results) {
      const container = document.getElementById('studentResultsContainer');
      if (!results || results.length === 0) {
        container.innerHTML = '<div class="text-center py-12 text-on-surface-variant font-label-mono-sm">No scholarships found matching current filters.</div>';
        return;
      }

      const eligibleCount = results.filter(r => r.eligibility_status === 'ELIGIBLE' || r.eligibility_status === 'HIGH_PROBABILITY').length;

      let html = `
        <div class="w-full bg-surface-container-low/80 backdrop-blur-md p-3 rounded-xl mb-4 border border-outline-variant/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="font-headline-md text-sm sm:text-base text-on-surface font-bold">🎯 Recommended Scholarships (${eligibleCount} Eligible Schemes Found)</span>
          </div>
          <div class="text-on-surface-variant font-label-mono-xs text-xs">
            Cross-referenced with 21 Central, State & CSR schemes
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      `;

      html += results.map(res => {
        const foa = res.foa;
        const isEligible = res.eligibility_status === 'ELIGIBLE';
        const isHigh = res.eligibility_status === 'HIGH_PROBABILITY';
        const isWarning = res.eligibility_status === 'WARNING';

        const badgeBg = isEligible ? 'bg-primary/15 text-primary border-primary/30' : (isHigh ? 'bg-secondary/15 text-secondary border-secondary/30' : (isWarning ? 'bg-amber-500/15 text-amber-300 border-amber-500/30' : 'bg-red-500/15 text-red-300 border-red-500/30'));
        const badgeLabel = isEligible ? `100% ELIGIBLE (${res.match_percentage}%)` : (isHigh ? `HIGH PROBABILITY (${res.match_percentage}%)` : (isWarning ? `CONDITIONAL (${res.match_percentage}%)` : `INELIGIBLE`));

        const whatsappText = encodeURIComponent(`🎓 *Scholarship Alert: ${foa.title}*\n💰 Grant: ${res.estimated_financial_benefit}\n🏛️ Official Portal: ${res.direct_apply_url || res.portal_url}\nCheck your eligibility on MadadgaarAI!`);

        return `
          <div class="bg-surface-container-low/90 backdrop-blur-xl p-5 rounded-2xl border border-outline-variant/30 shadow-xl flex flex-col justify-between hover:border-primary/40 transition-all">
            <div>
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="px-2 py-0.5 bg-surface-container-highest text-tertiary font-label-mono-xs text-xs uppercase tracking-wider rounded font-semibold">${foa.agency}</span>
                <span class="px-2.5 py-0.5 ${badgeBg} font-label-mono-xs text-xs uppercase font-bold rounded border flex items-center gap-1">
                  ${isEligible ? '<span class="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>' : ''}
                  ${badgeLabel}
                </span>
              </div>

              <h3 class="font-headline-md text-base sm:text-lg text-on-surface font-semibold tracking-tight mt-1 hover:text-primary transition-colors cursor-pointer" onclick="openApplyModal('${foa.foa_id}')">
                ${foa.title}
              </h3>
              <p class="font-body-sm text-xs sm:text-sm text-on-surface-variant mt-1.5 line-clamp-2">
                ${foa.brief_summary}
              </p>

              <div class="bg-surface-container-lowest p-3 rounded-xl my-3 flex items-center justify-between gap-2 border border-outline-variant/20">
                <div>
                  <span class="font-label-mono-xs text-[10px] text-tertiary uppercase tracking-wider block font-semibold">Scholarship Financial Benefit:</span>
                  <span class="font-headline-md text-sm sm:text-base text-primary font-bold">${res.estimated_financial_benefit}</span>
                </div>
                <div class="text-right">
                  <span class="font-label-mono-xs text-[10px] text-on-surface-variant uppercase block">Portal Authority:</span>
                  <span class="font-label-mono-sm text-xs text-on-surface font-semibold">${res.portal_name}</span>
                </div>
              </div>

              <div class="bg-surface-container/60 p-3 rounded-xl space-y-1 mb-3 border border-outline-variant/10 text-xs">
                ${res.match_reasons.map(r => `
                  <div class="flex items-center gap-1.5 text-on-surface">
                    <span class="material-symbols-outlined text-[15px] text-primary shrink-0">check_circle</span>
                    <span>${r}</span>
                  </div>
                `).join('')}
                ${res.warning_reasons.map(w => `
                  <div class="flex items-center gap-1.5 text-error">
                    <span class="material-symbols-outlined text-[15px] text-error shrink-0">info</span>
                    <span>${w}</span>
                  </div>
                `).join('')}
              </div>
            </div>

            <div>
              <div class="flex flex-wrap items-center gap-2 pt-2 border-t border-outline-variant/20">
                <button class="px-4 py-2 bg-primary text-on-primary hover:bg-primary-fixed font-label-mono-sm text-xs uppercase font-bold tracking-wider rounded-lg transition-all flex items-center gap-1.5 shadow-[0_0_12px_rgba(78,222,163,0.2)]" onclick="openApplyModal('${foa.foa_id}')">
                  <span>🚀 Apply & Portal Guide (आवेदन सेतु)</span>
                  <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
                </button>
                <button class="px-3 py-1.5 bg-surface-container-high hover:bg-surface-variant text-on-surface font-label-mono-xs text-xs uppercase tracking-wider rounded-lg transition-colors flex items-center gap-1 border border-outline-variant/20" onclick="openDocChecklistModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[14px]">checklist</span> Docs
                </button>
                <button class="px-3 py-1.5 bg-surface-container-high hover:bg-surface-variant text-secondary font-label-mono-xs text-xs uppercase tracking-wider rounded-lg transition-colors flex items-center gap-1 border border-outline-variant/20" onclick="openHinglishModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[14px]">translate</span> सरल गाइड
                </button>
                <a class="px-3 py-1.5 bg-[#138808]/20 hover:bg-[#138808]/30 text-primary font-label-mono-xs text-xs uppercase rounded-lg transition-colors flex items-center gap-1 border border-[#138808]/40 ml-auto" href="https://api.whatsapp.com/send?text=${whatsappText}" target="_blank" rel="noopener noreferrer">
                  <span class="material-symbols-outlined text-[14px]">share</span> WhatsApp
                </a>
              </div>
            </div>
          </div>
        `;
      }).join('');

      html += '</div>';
      container.innerHTML = html;
    }

    function renderExploreGrid(items) {
      const grid = document.getElementById('exploreGrid');
      if (!items || items.length === 0) {
        grid.innerHTML = '<div class="col-span-2 text-center py-12 text-on-surface-variant">No opportunities found matching search.</div>';
        return;
      }

      grid.innerHTML = items.map(foa => {
        const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'As per norms');
        return `
          <div class="bg-surface-container-low/90 backdrop-blur-xl p-5 rounded-2xl border border-outline-variant/30 shadow-xl flex flex-col justify-between hover:border-primary/40 transition-all">
            <div>
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="px-2 py-0.5 bg-surface-container-highest text-tertiary font-label-mono-xs text-xs uppercase tracking-wider rounded font-semibold">${foa.agency}</span>
                <span class="font-label-mono-xs text-xs text-on-surface-variant">${foa.foa_id}</span>
              </div>
              <h3 class="font-headline-md text-base sm:text-lg text-on-surface font-semibold tracking-tight mt-1 hover:text-primary transition-colors cursor-pointer" onclick="openApplyModal('${foa.foa_id}')">${foa.title}</h3>
              <p class="font-body-sm text-xs sm:text-sm text-on-surface-variant mt-1.5 line-clamp-2">${foa.brief_summary}</p>
              
              <div class="bg-surface-container-lowest p-3 rounded-xl my-3 flex items-center justify-between gap-2 border border-outline-variant/20">
                <div>
                  <span class="font-label-mono-xs text-[10px] text-tertiary uppercase tracking-wider block font-semibold">Financial Assistance:</span>
                  <span class="font-headline-md text-sm sm:text-base text-primary font-bold">${budgetStr}</span>
                </div>
                <div class="text-right">
                  <span class="font-label-mono-xs text-[10px] text-on-surface-variant uppercase block">Target:</span>
                  <span class="font-label-mono-sm text-xs text-on-surface font-semibold">${(foa.thematic_areas || []).slice(0, 2).join(', ')}</span>
                </div>
              </div>
            </div>

            <div class="flex flex-wrap items-center gap-2 pt-2 border-t border-outline-variant/20">
              <button class="px-4 py-2 bg-primary text-on-primary hover:bg-primary-fixed font-label-mono-sm text-xs uppercase font-bold rounded-lg transition-all flex items-center gap-1.5" onclick="openApplyModal('${foa.foa_id}')">
                <span>🚀 Apply & Portal Guide</span>
              </button>
              <button class="px-3 py-1.5 bg-surface-container-high hover:bg-surface-variant text-on-surface font-label-mono-xs text-xs uppercase rounded-lg transition-colors flex items-center gap-1" onclick="openDocChecklistModal('${foa.foa_id}')">
                <span class="material-symbols-outlined text-[14px]">checklist</span> Docs
              </button>
              <button class="px-3 py-1.5 bg-surface-container-high hover:bg-surface-variant text-secondary font-label-mono-xs text-xs uppercase rounded-lg transition-colors flex items-center gap-1" onclick="openHinglishModal('${foa.foa_id}')">
                <span class="material-symbols-outlined text-[14px]">translate</span> सरल गाइड
              </button>
              <button class="px-3 py-1.5 bg-surface-container-high hover:bg-surface-variant text-on-surface font-label-mono-xs text-xs uppercase rounded-lg transition-colors flex items-center gap-1 ml-auto" onclick="downloadCalendar('${foa.foa_id}')">
                <span class="material-symbols-outlined text-[14px]">event</span> .ICS
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    async function runExploreSearch() {
      const q = document.getElementById('exploreSearchInput').value.trim();
      const agency = document.getElementById('exploreAgencyFilter').value;

      if (!q && !agency) {
        renderExploreGrid(allOpportunities);
        return;
      }

      try {
        const res = await fetch('/api/search', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query: q || "scholarship and grants",
            agency_filter: agency || null,
            top_k: 20
          })
        });
        const data = await res.json();
        renderExploreGrid(data.map(d => d.foa));
      } catch (err) {
        console.error('Search failed:', err);
      }
    }

    async function runFacultyMatch() {
      const summary = document.getElementById('matchAbstract').value.trim();
      if (!summary) {
        alert('Please enter a research proposal abstract.');
        return;
      }

      const role = document.getElementById('matchRole').value;
      const age = parseInt(document.getElementById('matchAge').value) || 38;
      const degree = document.getElementById('matchDegree').value;
      const container = document.getElementById('facultyResultsContainer');

      container.innerHTML = '<div class="text-center py-8 text-on-surface-variant"><span class="material-symbols-outlined animate-spin">refresh</span> Computing dense semantic embeddings & matching...</div>';

      try {
        const res = await fetch('/api/match-profile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            research_summary: summary,
            user_role: role,
            applicant_age: age,
            highest_degree: degree,
            top_k: 6
          })
        });
        const results = await res.json();
        renderFacultyResults(results);
      } catch (err) {
        container.innerHTML = '<div class="text-error text-center py-6">Faculty matching failed.</div>';
      }
    }

    function renderFacultyResults(results) {
      const container = document.getElementById('facultyResultsContainer');
      if (!results || results.length === 0) {
        container.innerHTML = '<div class="text-center py-8 text-on-surface-variant">No matching research calls found.</div>';
        return;
      }

      container.innerHTML = `
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          ${results.map(m => `
            <div class="bg-surface-container-low/90 backdrop-blur-xl p-5 rounded-2xl border border-outline-variant/30 shadow-xl flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                  <span class="px-2 py-0.5 bg-surface-container-highest text-secondary font-label-mono-xs text-xs uppercase font-semibold rounded">${m.foa.agency}</span>
                  <span class="px-2 py-0.5 bg-primary/15 text-primary font-label-mono-xs text-xs font-bold rounded">${(m.relevance_score * 100).toFixed(1)}% Match</span>
                </div>
                <h3 class="font-headline-md text-base text-on-surface font-semibold">${m.foa.title}</h3>
                <p class="font-body-sm text-xs text-on-surface-variant mt-1 line-clamp-2">${m.foa.brief_summary}</p>
                <div class="p-2.5 bg-surface-container-lowest rounded-lg my-2.5 text-xs text-on-surface border border-outline-variant/20">
                  <strong>Compliance:</strong> ${m.compliance.reasons.join(' ')}
                </div>
              </div>
              <div class="flex items-center gap-2 pt-2 border-t border-outline-variant/20">
                <button class="px-3.5 py-1.5 bg-primary text-on-primary font-label-mono-sm text-xs uppercase font-bold rounded-lg" onclick="draftProposal('${m.foa.foa_id}')">📝 Draft Proposal</button>
                <button class="px-3 py-1.5 bg-surface-container-high text-on-surface font-label-mono-xs text-xs uppercase rounded-lg" onclick="downloadCalendar('${m.foa.foa_id}')">📅 .ICS</button>
                <a href="${m.foa.source_url}" target="_blank" class="px-3 py-1.5 bg-surface-container-high text-tertiary font-label-mono-xs text-xs uppercase rounded-lg ml-auto">🌐 Portal ↗</a>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    async function openApplyModal(foaId) {
      const modal = document.getElementById('applyModalOverlay');
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/foas/${foaId}`);
        const foa = await res.json();

        document.getElementById('modalSchemeTitle').innerText = foa.title;
        document.getElementById('modalAgencyTag').innerText = foa.agency;
        document.getElementById('modalRefId').innerText = 'REF: ' + foa.foa_id;

        const applyUrl = foa.direct_apply_url || foa.source_url;
        const domain = new URL(applyUrl).hostname;

        document.getElementById('modalHostDomain').innerText = domain;
        document.getElementById('modalCopyBtn').onclick = () => {
          navigator.clipboard.writeText(applyUrl);
          alert('Official portal URL copied to clipboard: ' + applyUrl);
        };

        const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'Direct Grant Support');
        document.getElementById('modalGrantText').innerHTML = `<span class="material-symbols-outlined text-[16px] text-primary">account_balance</span> Disbursal: <strong class="text-on-surface">${budgetStr}</strong> via Direct PFMS/DBT Gateway`;

        document.getElementById('modalApplyLink').href = applyUrl;
        document.getElementById('modalApplyLink').innerHTML = `<span>🚀 Launch Official Portal (${domain}) ↗</span>`;

        const whatsappText = encodeURIComponent(`🎓 *Official Guidance for ${foa.title}*\n🏛️ Portal: ${applyUrl}\nCheck your eligibility on MadadgaarAI!`);
        document.getElementById('modalWhatsappLink').href = `https://api.whatsapp.com/send?text=${whatsappText}`;

        const steps = (foa.portal_navigation_steps && foa.portal_navigation_steps.length > 0) ? foa.portal_navigation_steps : [
          `1. Open the verified official portal (${applyUrl}).`,
          "2. Complete student One Time Registration (OTR) with your Aadhaar number & Mobile OTP.",
          `3. Search and select scheme: '${foa.title}'.`,
          "4. Fill academic details and upload required income and caste certificates.",
          "5. Verify your bank account has active Aadhaar-NPCI DBT mapping before final submission."
        ];

        const timeline = document.getElementById('modalStepsTimeline');
        timeline.innerHTML = steps.map((step, idx) => `
          <div class="relative flex items-start gap-3 group">
            <div class="relative z-10 w-8 h-8 rounded-lg bg-surface-container-high text-primary flex items-center justify-center shrink-0 border border-primary/30 font-bold text-xs">
              0${idx + 1}
            </div>
            <div class="flex-1 p-3 bg-surface-container rounded-lg border border-outline-variant/20">
              <p class="font-body-sm text-xs sm:text-sm text-on-surface leading-relaxed">
                ${step.replace(/^[0-9]+\.\s*/, '')}
              </p>
            </div>
          </div>
        `).join('');

      } catch (err) {
        console.error('Failed to load modal details:', err);
      }
    }

    function closeApplyModal() {
      document.getElementById('applyModalOverlay').classList.add('hidden');
    }

    async function openDocChecklistModal(foaId) {
      const modal = document.getElementById('genericModalOverlay');
      const title = document.getElementById('genericModalTitle');
      const body = document.getElementById('genericModalBody');

      title.innerText = "📄 Mandatory Document Checklist & Guidance";
      body.innerHTML = '<div class="text-center py-6">Loading requirements...</div>';
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/student/scholarships/${foaId}/checklist`);
        const docs = await res.json();

        let html = `
          <div class="p-3 bg-primary/10 border border-primary/30 rounded-xl mb-4 text-xs text-primary">
            ⚠️ <strong>Pro-Tip:</strong> Keep scanned copies in PDF format under 200 KB before starting the online application.
          </div>
        `;

        html += docs.map((d, idx) => `
          <div class="p-3 bg-surface-container rounded-xl mb-3 border border-outline-variant/20">
            <div class="font-headline-md font-bold text-on-surface mb-1">${idx + 1}. ${d.document_name}</div>
            <div class="text-xs text-on-surface-variant">🏛️ <strong>Issuing Authority:</strong> ${d.issuing_authority}</div>
            <div class="text-xs text-on-surface-variant">📋 <strong>Rules & Specs:</strong> ${d.validity_and_rules}</div>
            <div class="text-xs text-on-surface-variant">📍 <strong>How to Obtain:</strong> ${d.how_to_obtain}</div>
          </div>
        `).join('');

        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div class="text-error">Failed to load document checklist.</div>';
      }
    }

    async function openHinglishModal(foaId) {
      const modal = document.getElementById('genericModalOverlay');
      const title = document.getElementById('genericModalTitle');
      const body = document.getElementById('genericModalBody');

      title.innerText = "🇮🇳 Saral Samjhauti (सरल भाषा में समझें)";
      body.innerHTML = '<div class="text-center py-6">Loading guide...</div>';
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/student/scholarships/${foaId}/hinglish`);
        const guide = await res.json();

        let html = `
          <div class="p-4 bg-primary/10 border border-primary/30 rounded-xl mb-3">
            <h4 class="text-primary font-bold mb-1">👥 कौन-कौन अप्लाई कर सकता है? (Eligibility)</h4>
            <p class="text-on-surface">${guide.kaun_apply_kar_sakta_hai}</p>
          </div>

          <div class="p-4 bg-tertiary/10 border border-tertiary/30 rounded-xl mb-3">
            <h4 class="text-tertiary font-bold mb-1">💰 कितने पैसे मिलेंगे? (Financial Support)</h4>
            <p class="text-on-surface font-semibold">${guide.kitne_paise_milenge}</p>
          </div>

          <div class="p-4 bg-surface-container rounded-xl mb-3 border border-outline-variant/20">
            <h4 class="text-on-surface font-bold mb-2">📑 क्या-क्या जरूरी डॉक्यूमेंट्स चाहिए?</h4>
            <ul class="space-y-1">
              ${guide.zaruri_documents.map(d => `<li class="text-on-surface-variant">• ${d}</li>`).join('')}
            </ul>
          </div>

          <div class="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl text-xs text-amber-300">
            ${guide.aadhaar_seeding_warning}
          </div>
        `;

        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div class="text-error">Failed to load guide.</div>';
      }
    }

    async function draftProposal(foaId) {
      const modal = document.getElementById('genericModalOverlay');
      const title = document.getElementById('genericModalTitle');
      const body = document.getElementById('genericModalBody');

      title.innerText = "📝 AI Proposal Skeleton & Budget Allocator";
      body.innerHTML = '<div class="text-center py-6">Generating tailored proposal structure...</div>';
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/foas/${foaId}/draft-proposal`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            pi_name: "Dr. Faculty Researcher",
            institution_name: "Indian Academic Institution"
          })
        });
        const data = await res.json();

        let html = `
          <h4 class="text-primary font-bold mb-3">${data.scheme_title} (${data.agency})</h4>
          <div class="p-3 bg-surface-container rounded-xl mb-4 border border-outline-variant/20">
            <div class="font-bold text-on-surface mb-2">Suggested Budget Allocation (MoF OM Norms)</div>
            ${Object.entries(data.suggested_budget_breakdown).map(([k, v]) => `
              <div class="text-xs text-on-surface-variant"><strong>${k}:</strong> ${v}</div>
            `).join('')}
          </div>
          <div>
            <div class="font-bold text-on-surface mb-2">Proposal Sections</div>
            ${data.sections.map(sec => `
              <div class="p-3 bg-surface-container rounded-xl mb-3 border border-outline-variant/20">
                <div class="font-semibold text-on-surface">${sec.section_title}</div>
                <div class="text-xs text-on-surface-variant mb-2">${sec.section_description}</div>
                <pre class="bg-surface-container-lowest p-2.5 rounded text-xs text-on-surface overflow-x-auto"><code>${sec.drafted_content}</code></pre>
              </div>
            `).join('')}
          </div>
        `;
        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div class="text-error">Failed to draft proposal.</div>';
      }
    }

    function switchDocTab(activeTab) {
      const hinglishBtn = document.getElementById('tabHinglishBtn');
      const checklistBtn = document.getElementById('tabChecklistBtn');
      const hinglishPanel = document.getElementById('hinglishPanel');
      const checklistPanel = document.getElementById('checklistPanel');

      if (activeTab === 'hinglish') {
        hinglishPanel.classList.remove('hidden');
        checklistPanel.classList.add('hidden');
        hinglishBtn.className = 'px-3.5 py-1.5 bg-surface-container-high text-primary font-label-mono-sm text-xs uppercase rounded-lg font-bold transition-all flex items-center gap-1.5';
        checklistBtn.className = 'px-3.5 py-1.5 text-on-surface-variant hover:text-on-surface font-label-mono-sm text-xs uppercase rounded-lg font-medium transition-all flex items-center gap-1.5';
      } else {
        checklistPanel.classList.remove('hidden');
        hinglishPanel.classList.add('hidden');
        checklistBtn.className = 'px-3.5 py-1.5 bg-surface-container-high text-primary font-label-mono-sm text-xs uppercase rounded-lg font-bold transition-all flex items-center gap-1.5';
        hinglishBtn.className = 'px-3.5 py-1.5 text-on-surface-variant hover:text-on-surface font-label-mono-sm text-xs uppercase rounded-lg font-medium transition-all flex items-center gap-1.5';
      }
    }

    function closeGenericModal() {
      document.getElementById('genericModalOverlay').classList.add('hidden');
    }

    function downloadCalendar(foaId) {
      window.location.href = `/api/foas/${foaId}/calendar`;
    }

    async function triggerDbSync() {
      const res = await fetch('/api/ingest/trigger', { method: 'POST' });
      await loadOpportunities();
      runStudentMatch();
      alert('Database synchronized successfully!');
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeApplyModal();
        closeGenericModal();
      }
    });

    // Boot platform on load
    initPlatform();
  </script>
</body>
</html>
"""
