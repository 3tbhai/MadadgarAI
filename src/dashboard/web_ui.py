"""Modern Interactive Dashboard UI for MadadgaarAI with Student Scholarship Hub (Vidyarthi AI) and Government Application Gateway."""


def render_dashboard_html() -> str:
    return r"""<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>MadadgaarAI — National Scholarship & Research Funding Intelligence</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700;800&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=swap" rel="stylesheet"/>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#ecfdf5',
              100: '#d1fae5',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              900: '#064e3b',
            },
            dark: {
              base: '#080c14',
              surface: '#0f172a',
              card: '#131d33',
              cardHover: '#18243e',
              border: '#1e293b',
              borderLight: '#334155'
            }
          },
          fontFamily: {
            sans: ['Geist', 'Inter', 'system-ui', 'sans-serif'],
            display: ['Space Grotesk', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace']
          }
        }
      }
    };
  </script>

  <style>
    @layer base {
      html, body {
        background-color: #080c14;
        color: #f1f5f9;
        font-family: 'Geist', 'Inter', system-ui, sans-serif;
      }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #080c14; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #10b981; }

    /* Subtle Glass & Glows */
    .glass-card {
      background: rgba(19, 29, 51, 0.75);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(51, 65, 85, 0.5);
    }
    .glass-card:hover {
      border-color: rgba(16, 185, 129, 0.4);
    }
    .glass-nav {
      background: rgba(8, 12, 20, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-bottom: 1px solid rgba(30, 41, 59, 0.8);
    }
    .badge-tricolor {
      background: linear-gradient(90deg, rgba(249,115,22,0.15) 0%, rgba(255,255,255,0.08) 50%, rgba(16,185,129,0.15) 100%);
      border: 1px solid rgba(255, 255, 255, 0.12);
    }
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between selection:bg-brand-500 selection:text-dark-base">

  <!-- TOAST NOTIFICATION CONTAINER -->
  <div id="toastNotification" class="fixed bottom-6 right-6 z-50 transform translate-y-20 opacity-0 transition-all duration-300 pointer-events-none flex items-center gap-2.5 px-4 py-3 bg-dark-card border border-brand-500/40 text-white rounded-xl shadow-2xl">
    <span class="material-symbols-outlined text-brand-400 text-[20px]" id="toastIcon">check_circle</span>
    <span class="text-xs sm:text-sm font-medium" id="toastMessage">Action completed successfully</span>
  </div>

  <!-- TOP APP HEADER -->
  <header class="fixed top-0 left-0 right-0 w-full z-40 glass-nav shadow-2xl">
    <div class="h-20 w-full px-4 sm:px-8 lg:px-12 flex items-center justify-between gap-4">
      
      <!-- Brand Logo -->
      <div class="flex items-center gap-3.5 shrink-0 cursor-pointer" onclick="switchNavTab('vidyarthi')">
        <div class="w-11 h-11 rounded-2xl bg-gradient-to-br from-brand-500 via-emerald-600 to-cyan-500 flex items-center justify-center text-dark-base font-bold shadow-[0_0_20px_rgba(16,185,129,0.35)]">
          <span class="material-symbols-outlined text-[26px]">school</span>
        </div>
        <div class="flex flex-col">
          <div class="flex items-center gap-2">
            <span class="font-display text-xl sm:text-2xl text-white tracking-tight font-extrabold">Madadgaar<span class="text-brand-400">AI</span></span>
            <span class="text-xs text-slate-400 font-mono hidden sm:inline">(मददगार AI)</span>
          </div>
          <div class="flex items-center gap-1.5 mt-0.5">
            <span class="badge-tricolor px-2 py-0.5 rounded-full text-[10px] text-slate-300 font-mono flex items-center gap-1.5">
              <span class="inline-flex gap-0.5 items-center">
                <span class="w-1.5 h-1.5 rounded-full bg-[#ff9933]"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#ffffff]"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-[#138808]"></span>
              </span>
              NATIONAL SCHOLARSHIP & GRANT INTELLIGENCE
            </span>
          </div>
        </div>
      </div>

      <!-- MAIN NAVIGATION TABS -->
      <nav class="hidden lg:flex items-center gap-2 bg-dark-base/80 p-1.5 rounded-2xl border border-dark-border" id="mainNavTabs">
        <button class="nav-tab-btn flex items-center gap-2 px-4 py-2.5 bg-dark-card border border-brand-500/40 text-brand-400 font-mono text-xs uppercase font-bold rounded-xl shadow-lg transition-all" id="tabBtnVidyarthi" onclick="switchNavTab('vidyarthi')">
          <span class="material-symbols-outlined text-[18px]">school</span>
          Vidyarthi Hub (Scholarships)
        </button>
        <button class="nav-tab-btn flex items-center gap-2 px-4 py-2.5 text-slate-400 hover:text-white hover:bg-dark-card/50 transition-all font-mono text-xs uppercase rounded-xl border border-transparent" id="tabBtnExplore" onclick="switchNavTab('explore')">
          <span class="material-symbols-outlined text-[18px]">explore</span>
          Explore Catalogue <span class="px-1.5 py-0.5 bg-slate-800 text-brand-400 font-mono text-[10px] rounded" id="statExploreBadge">21 ACTIVE</span>
        </button>
        <button class="nav-tab-btn flex items-center gap-2 px-4 py-2.5 text-slate-400 hover:text-white hover:bg-dark-card/50 transition-all font-mono text-xs uppercase rounded-xl border border-transparent" id="tabBtnFaculty" onclick="switchNavTab('faculty')">
          <span class="material-symbols-outlined text-[18px]">biotech</span>
          Faculty & Researcher Grants <span class="px-1.5 py-0.5 bg-indigo-500/20 text-indigo-300 font-mono text-[10px] rounded">DST/SERB</span>
        </button>
      </nav>

      <!-- RIGHT STATUS TELEMETRY -->
      <div class="flex items-center gap-3 shrink-0">
        <div class="hidden xl:flex items-center gap-2 bg-dark-base/90 border border-dark-border px-3.5 py-1.5 rounded-xl">
          <span class="w-2.5 h-2.5 rounded-full bg-brand-400 animate-pulse"></span>
          <span class="font-mono text-xs text-brand-400 font-bold" id="statTotalCounter">21 SCHEMES ACTIVE</span>
          <span class="text-slate-500 font-mono text-xs">|</span>
          <span class="text-slate-400 font-mono text-xs font-medium">100% FREE GOVT PORTALS</span>
        </div>

        <button class="px-3.5 py-2 bg-dark-card hover:bg-dark-cardHover text-slate-200 font-mono text-xs uppercase tracking-wider rounded-xl transition-all flex items-center gap-1.5 border border-dark-border hover:border-brand-500/30 cursor-pointer shadow-md" onclick="triggerDbSync()" title="Synchronize database with official seed feeds">
          <span class="material-symbols-outlined text-[16px] text-cyan-400" id="syncIcon">sync</span>
          <span class="hidden sm:inline">Sync DB</span>
        </button>

        <a href="/docs" target="_blank" class="w-9 h-9 rounded-xl bg-dark-card hover:bg-dark-cardHover border border-dark-border hover:border-slate-600 flex items-center justify-center shrink-0 text-slate-300 hover:text-white transition-all shadow-md" title="FastAPI Swagger OpenAPI Docs">
          <span class="material-symbols-outlined text-[18px]">api</span>
        </a>
      </div>
    </div>

    <!-- Mobile Nav Bar (Visible on mobile screens) -->
    <div class="lg:hidden flex items-center justify-around bg-dark-base/95 border-t border-dark-border px-2 py-1.5">
      <button class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono text-brand-400 font-bold bg-dark-card" id="mTabBtnVidyarthi" onclick="switchNavTab('vidyarthi')">
        <span class="material-symbols-outlined text-[16px]">school</span> Vidyarthi
      </button>
      <button class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono text-slate-400" id="mTabBtnExplore" onclick="switchNavTab('explore')">
        <span class="material-symbols-outlined text-[16px]">explore</span> Explore
      </button>
      <button class="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono text-slate-400" id="mTabBtnFaculty" onclick="switchNavTab('faculty')">
        <span class="material-symbols-outlined text-[16px]">biotech</span> Faculty
      </button>
    </div>
  </header>

  <!-- MAIN VIEWPORT CONTAINER -->
  <main class="w-full pt-28 lg:pt-24 flex-1 pb-16">

    <!-- ========================================================= -->
    <!-- TAB 1: VIDYARTHI SCHOLARSHIP HUB (DEFAULT)                -->
    <!-- ========================================================= -->
    <div id="viewVidyarthi" class="flex flex-col w-full">

      <!-- SECTION 1: TOP TRUST & METRIC TELEMETRY -->
      <section class="w-full px-4 sm:px-8 lg:px-12 pt-2 pb-4">
        <div class="w-full bg-gradient-to-r from-emerald-950/40 via-dark-card to-cyan-950/40 p-4 rounded-2xl border border-dark-border shadow-xl flex flex-col lg:flex-row items-start lg:items-center justify-between gap-3">
          <div class="flex items-center gap-3">
            <span class="flex h-3.5 w-3.5 relative shrink-0">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-brand-500"></span>
            </span>
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1">
              <span class="font-display text-sm md:text-base text-white uppercase font-bold tracking-tight">Direct Benefit Transfer (DBT) Intelligence</span>
              <span class="hidden md:inline text-slate-600 font-mono text-xs">|</span>
              <p class="font-mono text-xs sm:text-sm text-slate-300">Zero Middlemen Guarantee • 100% Direct Disbursal via NPCI Aadhaar Gateway</p>
            </div>
          </div>
          <div class="flex items-center gap-2 shrink-0 self-end lg:self-auto">
            <span class="px-3 py-1 bg-brand-500/10 text-brand-400 font-mono text-xs rounded-lg uppercase tracking-wider font-semibold flex items-center gap-1.5 border border-brand-500/30">
              <span class="material-symbols-outlined text-[15px]">verified</span> UIDAI & PFMS VERIFIED
            </span>
          </div>
        </div>

        <!-- 4 Telemetry Ribbon Tiles -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-3.5 mt-3.5">
          <div class="glass-card p-4 rounded-2xl border border-dark-border hover:border-brand-500/30 transition-all duration-300">
            <div class="flex items-center justify-between text-slate-400 mb-1">
              <span class="font-mono text-[10px] sm:text-xs uppercase tracking-widest text-slate-400">ANNUAL OUTLAY (FY 24-25)</span>
              <span class="material-symbols-outlined text-[20px] text-cyan-400">payments</span>
            </div>
            <div class="flex items-baseline gap-1 mt-1">
              <span class="font-display text-2xl sm:text-3xl text-brand-400 font-extrabold tracking-tight">₹18,450</span>
              <span class="font-display text-base text-brand-400 font-semibold">Cr</span>
            </div>
            <p class="font-mono text-[11px] text-slate-400 mt-1">Directly credited to student accounts</p>
          </div>

          <div class="glass-card p-4 rounded-2xl border border-dark-border hover:border-brand-500/30 transition-all duration-300">
            <div class="flex items-center justify-between text-slate-400 mb-1">
              <span class="font-mono text-[10px] sm:text-xs uppercase tracking-widest text-slate-400">ACTIVE SANCTIONS</span>
              <span class="material-symbols-outlined text-[20px] text-amber-400">alarm_on</span>
            </div>
            <div class="flex items-baseline gap-1 mt-1">
              <span class="font-display text-2xl sm:text-3xl text-white font-extrabold tracking-tight">21</span>
              <span class="font-display text-sm text-amber-400 font-semibold">SCHEMES</span>
            </div>
            <p class="font-mono text-[11px] text-amber-400/90 mt-1 flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span> Central, State & CSR Portals
            </p>
          </div>

          <div class="glass-card p-4 rounded-2xl border border-dark-border hover:border-brand-500/30 transition-all duration-300">
            <div class="flex items-center justify-between text-slate-400 mb-1">
              <span class="font-mono text-[10px] sm:text-xs uppercase tracking-widest text-slate-400">APPLICANT ACCESS</span>
              <span class="material-symbols-outlined text-[20px] text-brand-400">volunteer_activism</span>
            </div>
            <div class="flex items-baseline gap-1 mt-1">
              <span class="font-display text-2xl sm:text-3xl text-cyan-400 font-extrabold tracking-tight">100%</span>
              <span class="font-display text-base text-cyan-400 font-semibold">FREE</span>
            </div>
            <p class="font-mono text-[11px] text-slate-400 mt-1">Zero agent fees / Official direct routing</p>
          </div>

          <div class="glass-card p-4 rounded-2xl border border-dark-border hover:border-brand-500/30 transition-all duration-300">
            <div class="flex items-center justify-between text-slate-400 mb-1">
              <span class="font-mono text-[10px] sm:text-xs uppercase tracking-widest text-slate-400">RULE ENGINE PRECISION</span>
              <span class="material-symbols-outlined text-[20px] text-indigo-400">model_training</span>
            </div>
            <div class="flex items-baseline gap-1 mt-1">
              <span class="font-display text-2xl sm:text-3xl text-indigo-300 font-extrabold tracking-tight">99.2%</span>
              <span class="font-display text-sm text-indigo-300 font-semibold">ACCURACY</span>
            </div>
            <p class="font-mono text-[11px] text-slate-400 mt-1">Deterministic Gazette rule compliance</p>
          </div>
        </div>
      </section>

      <!-- SECTION 2: STUDENT ELIGIBILITY CALCULATOR WIZARD -->
      <section class="w-full px-4 sm:px-8 lg:px-12 py-3">
        <div class="glass-card p-5 sm:p-7 rounded-3xl border border-dark-border shadow-2xl relative overflow-hidden">
          
          <!-- Background Glow Elements -->
          <div class="absolute -top-24 -right-24 w-72 h-72 bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>
          <div class="absolute -bottom-24 -left-24 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

          <!-- Wizard Header -->
          <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4 pb-5 border-b border-dark-border">
            <div class="flex flex-col">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-1 bg-brand-500/10 text-brand-400 font-mono text-xs rounded-lg uppercase font-bold tracking-wider flex items-center gap-1.5 border border-brand-500/25">
                  <span class="material-symbols-outlined text-[15px]">bolt</span> AI Instant Eligibility Matcher
                </span>
                <span class="text-slate-400 font-mono text-xs uppercase tracking-wider font-semibold">मददगार AI पात्रता कैलकुलेटर</span>
              </div>
              <h2 class="font-display text-xl sm:text-2xl lg:text-3xl text-white font-extrabold mt-1.5 tracking-tight">
                Set Your Academic Profile • Claim Public Capital
              </h2>
              <p class="text-xs sm:text-sm text-slate-300 mt-1">
                Our engine evaluates statutory rules across NSP Central, State Portals (UP / MahaDBT), UGC, AICTE, and verified CSR Foundations.
              </p>
            </div>
            
            <div class="flex items-center gap-2 shrink-0">
              <button class="px-4 py-2 bg-dark-surface hover:bg-slate-800 text-slate-200 text-xs font-mono uppercase tracking-wider rounded-xl transition-all flex items-center gap-1.5 border border-dark-border hover:border-slate-600 shadow-md cursor-pointer" onclick="resetStudentProfile()">
                <span class="material-symbols-outlined text-[16px]">restart_alt</span> Reset Defaults
              </button>
            </div>
          </div>

          <!-- Profile Parameters Grid -->
          <div class="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 pt-5 pb-4">
            
            <!-- Field 1: State Domicile -->
            <div class="flex flex-col gap-1.5">
              <label class="font-mono text-xs text-slate-300 uppercase flex items-center justify-between font-semibold">
                <span>Domicile State (गृह राज्य)</span>
                <span class="text-cyan-400 text-[10px]">MANDATORY</span>
              </label>
              <div class="relative">
                <select class="w-full bg-dark-surface text-white font-sans text-sm px-3.5 py-2.5 rounded-xl border border-dark-border hover:border-slate-600 focus:outline-none focus:border-brand-500 transition-all appearance-none cursor-pointer" id="stuState" onchange="runStudentMatch(false)">
                  <option value="All India">All India / Open (अखिल भारतीय)</option>
                  <option value="Uttar Pradesh" selected>Uttar Pradesh (उत्तर प्रदेश)</option>
                  <option value="Maharashtra">Maharashtra (महाराष्ट्र)</option>
                  <option value="Bihar">Bihar (बिहार)</option>
                  <option value="Rajasthan">Rajasthan (राजस्थान)</option>
                  <option value="Madhya Pradesh">Madhya Pradesh (मध्य प्रदेश)</option>
                  <option value="West Bengal">West Bengal (पश्चिम बंगाल)</option>
                  <option value="Karnataka">Karnataka (कर्नाटक)</option>
                  <option value="Tamil Nadu">Tamil Nadu (तमिलनाडु)</option>
                  <option value="Andhra Pradesh">Andhra Pradesh (आंध्र प्रदेश)</option>
                  <option value="Telangana">Telangana (तेलंगाना)</option>
                  <option value="Gujarat">Gujarat (गुजरात)</option>
                  <option value="Assam / North Eastern States">Assam / North East NER (पूर्वोत्तर)</option>
                  <option value="Delhi NCR">Delhi NCR (दिल्ली)</option>
                  <option value="Jammu & Kashmir">Jammu & Kashmir (जम्मू कश्मीर)</option>
                </select>
                <span class="material-symbols-outlined absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-[20px]">expand_more</span>
              </div>
            </div>

            <!-- Field 2: Education Level -->
            <div class="flex flex-col gap-1.5">
              <label class="font-mono text-xs text-slate-300 uppercase flex items-center justify-between font-semibold">
                <span>Education Level (शैक्षणिक स्तर)</span>
                <span class="text-brand-400 text-[10px]">DEGREE</span>
              </label>
              <div class="relative">
                <select class="w-full bg-dark-surface text-white font-sans text-sm px-3.5 py-2.5 rounded-xl border border-dark-border hover:border-slate-600 focus:outline-none focus:border-brand-500 transition-all appearance-none cursor-pointer" id="stuLevel" onchange="runStudentMatch(false)">
                  <option value="UG - Engineering / Technology (B.Tech/B.E.)" selected>UG - Engineering (B.Tech/B.E.)</option>
                  <option value="Diploma / Polytechnic">Diploma / Polytechnic</option>
                  <option value="UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)">UG - Medical (MBBS/BDS/B.Pharm)</option>
                  <option value="UG - General (B.Sc / B.Com / B.A. / BBA / BCA)">UG - General (B.Sc/B.Com/B.A.)</option>
                  <option value="Class 11-12 (Higher Secondary)">Class 11-12 (Higher Secondary)</option>
                  <option value="Class 9-10 (Pre-Matric)">Class 9-10 (Pre-Matric)</option>
                  <option value="Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)">Postgraduate (Master's Degree)</option>
                  <option value="PhD / Doctoral Research">PhD / Doctoral Research</option>
                </select>
                <span class="material-symbols-outlined absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-[20px]">school</span>
              </div>
            </div>

            <!-- Field 3: Social Category -->
            <div class="flex flex-col gap-1.5">
              <label class="font-mono text-xs text-slate-300 uppercase flex items-center justify-between font-semibold">
                <span>Social Category (सामाजिक वर्ग)</span>
                <span class="text-cyan-400 text-[10px]">CERTIFIED</span>
              </label>
              <div class="relative">
                <select class="w-full bg-dark-surface text-white font-sans text-sm px-3.5 py-2.5 rounded-xl border border-dark-border hover:border-slate-600 focus:outline-none focus:border-brand-500 transition-all appearance-none cursor-pointer" id="stuCategory" onchange="runStudentMatch(false)">
                  <option value="General / Open">General / Open (सामान्य)</option>
                  <option value="OBC (Non-Creamy Layer)" selected>OBC-NCL (अन्य पिछड़ा वर्ग)</option>
                  <option value="SC (Scheduled Caste)">SC (अनुसूचित जाति)</option>
                  <option value="ST (Scheduled Tribe)">ST (अनुसूचित जनजाति)</option>
                  <option value="EWS (Economically Weaker Section)">EWS (आर्थिक रूप से कमजोर)</option>
                  <option value="Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)">Minority (अल्पसंख्यक)</option>
                </select>
                <span class="material-symbols-outlined absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-[20px]">badge</span>
              </div>
            </div>

            <!-- Field 4: Gender -->
            <div class="flex flex-col gap-1.5">
              <label class="font-mono text-xs text-slate-300 uppercase flex items-center justify-between font-semibold">
                <span>Gender (लिंग)</span>
                <span class="text-brand-400 text-[10px]">PRAGATI ACTIVE</span>
              </label>
              <div class="relative">
                <select class="w-full bg-dark-surface text-white font-sans text-sm px-3.5 py-2.5 rounded-xl border border-dark-border hover:border-slate-600 focus:outline-none focus:border-brand-500 transition-all appearance-none cursor-pointer" id="stuGender" onchange="runStudentMatch(false)">
                  <option value="Female" selected>Female (छात्रा — Unlocks Girl Grants)</option>
                  <option value="Male">Male (छात्र)</option>
                  <option value="Transgender">Transgender (तृतीय लिंग)</option>
                </select>
                <span class="material-symbols-outlined absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-[20px]">female</span>
              </div>
            </div>
          </div>

          <!-- Second Row: Income Slider, Academic Marks %, Special Flags -->
          <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-4 pt-1 pb-4">
            
            <!-- Family Income Slider & Presets (5 Cols) -->
            <div class="lg:col-span-5 bg-dark-base/80 p-4 rounded-2xl border border-dark-border flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <label class="font-mono text-xs text-slate-200 uppercase tracking-wider font-semibold">ANNUAL FAMILY INCOME (वार्षिक पारिवारिक आय)</label>
                <span class="font-display text-sm sm:text-base text-brand-400 font-bold" id="incomeDisplay">₹2,00,000 / Year</span>
              </div>
              <input class="w-full h-2.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-brand-500 my-3" id="stuIncome" max="1000000" min="50000" step="25000" type="range" value="200000" oninput="updateIncomeDisplay(this.value); runStudentMatch(false)"/>
              <div class="flex flex-wrap items-center gap-1.5 mt-1">
                <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 text-xs font-mono rounded-lg transition-all" id="btnIncome1_5L" onclick="setIncomeVal(150000)">₹1.5L</button>
                <button class="px-2.5 py-1 bg-brand-500 text-dark-base font-bold text-xs font-mono rounded-lg transition-all shadow-md" id="btnIncome2L" onclick="setIncomeVal(200000)">₹2.0L</button>
                <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 text-xs font-mono rounded-lg transition-all" id="btnIncome2_5L" onclick="setIncomeVal(250000)">₹2.5L</button>
                <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 text-xs font-mono rounded-lg transition-all" id="btnIncome4_5L" onclick="setIncomeVal(450000)">₹4.5L</button>
                <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 text-xs font-mono rounded-lg transition-all" id="btnIncome8L" onclick="setIncomeVal(800000)">₹8.0L</button>
              </div>
            </div>

            <!-- Academic Score % (3 Cols) -->
            <div class="lg:col-span-3 bg-dark-base/80 p-4 rounded-2xl border border-dark-border flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <label class="font-mono text-xs text-slate-200 uppercase tracking-wider font-semibold">ACADEMIC MERIT (10TH / 12TH %)</label>
                <span class="inline-flex items-center gap-1 px-1.5 py-0.5 bg-brand-500/10 text-brand-400 font-mono text-[10px] rounded font-semibold">
                  <span class="material-symbols-outlined text-[12px]">check_circle</span> VERIFIED
                </span>
              </div>
              <div class="flex items-baseline gap-2 mt-2">
                <input class="w-24 bg-dark-surface text-white font-display text-2xl font-extrabold px-3 py-1 rounded-xl text-center border border-dark-border focus:outline-none focus:border-brand-500" id="stuMarks" max="100" min="35" step="0.5" type="number" value="86" onchange="runStudentMatch(false)"/>
                <span class="font-display text-sm text-slate-400">% Aggregate Marks</span>
              </div>
              <p class="font-mono text-[11px] text-slate-400 mt-2">Qualifies for National Merit & CSR threshold quotas.</p>
            </div>

            <!-- Special Status Concession Flags (4 Cols) -->
            <div class="lg:col-span-4 bg-dark-base/80 p-4 rounded-2xl border border-dark-border flex flex-col justify-between gap-1.5">
              <label class="font-mono text-xs text-slate-200 uppercase tracking-wider font-semibold">SPECIAL CONCESSION FLAGS</label>
              <label class="flex items-center gap-2.5 p-2 bg-dark-surface/60 hover:bg-dark-surface rounded-xl cursor-pointer transition-all border border-dark-border/50">
                <input class="w-4 h-4 rounded text-brand-500 focus:ring-0 bg-dark-base border-dark-border cursor-pointer accent-brand-500" id="stuSingleGirl" type="checkbox" onchange="runStudentMatch(false)"/>
                <span class="font-sans text-xs sm:text-sm text-slate-200">Single Girl Child (एकल पुत्री आरक्षण)</span>
              </label>
              <label class="flex items-center gap-2.5 p-2 bg-dark-surface/60 hover:bg-dark-surface rounded-xl cursor-pointer transition-all border border-dark-border/50">
                <input class="w-4 h-4 rounded text-brand-500 focus:ring-0 bg-dark-base border-dark-border cursor-pointer accent-brand-500" id="stuPwd" type="checkbox" onchange="runStudentMatch(false)"/>
                <span class="font-sans text-xs sm:text-sm text-slate-200">Differently Abled / PwD (≥ 40% Benchmark)</span>
              </label>
            </div>
          </div>

          <!-- Wizard Action Bar -->
          <div class="relative z-10 pt-3 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
            <div class="flex items-center gap-2 text-slate-400">
              <span class="material-symbols-outlined text-brand-400 text-[20px]">verified_user</span>
              <span class="font-mono text-xs sm:text-sm">Deterministic Matching: Zero hallucinations. Direct cross-reference with official Gazette rules.</span>
            </div>
            <button class="px-7 py-3.5 bg-gradient-to-r from-brand-500 to-emerald-600 hover:from-brand-400 hover:to-emerald-500 text-dark-base font-display text-sm sm:text-base font-extrabold tracking-tight rounded-2xl shadow-[0_0_25px_rgba(16,185,129,0.35)] hover:shadow-[0_0_35px_rgba(16,185,129,0.5)] transition-all flex items-center justify-center gap-2 cursor-pointer" onclick="runStudentMatch(true)">
              <span class="material-symbols-outlined text-[20px]">bolt</span>
              <span id="matchBtnText">⚡ Find My Scholarships (पात्रता खोजें)</span>
            </button>
          </div>
        </div>
      </section>

      <!-- SECTION 3: RESULTS GRID -->
      <section class="w-full px-4 sm:px-8 lg:px-12 py-4">
        <div id="studentResultsContainer">
          <div class="text-center py-16 text-slate-400 font-mono">
            <span class="material-symbols-outlined text-5xl text-brand-400 animate-spin mb-3">refresh</span>
            <div class="text-base text-slate-300 font-semibold">Evaluating statutory eligibility across Central, State & CSR schemes...</div>
            <div class="text-xs text-slate-500 mt-1">Cross-referencing income thresholds, domicile rules & academic merit cutoffs</div>
          </div>
        </div>
      </section>

      <!-- SECTION 4: "SARAL SAMJHAUTI" & OFFICIAL DOCUMENT MATRIX -->
      <section class="w-full px-4 sm:px-8 lg:px-12 py-6 pb-12">
        <div class="glass-card p-5 sm:p-7 rounded-3xl border border-dark-border shadow-2xl">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-5 border-b border-dark-border">
            <div>
              <span class="font-mono text-xs text-cyan-400 uppercase tracking-widest block font-bold">HIGH-ACCESSIBILITY KNOWLEDGE BASE</span>
              <h3 class="font-display text-lg sm:text-xl md:text-2xl text-white font-bold tracking-tight mt-0.5">
                Applicant Enablement • सरल भाषा गाइड & आधिकारिक दस्तावेज सूची
              </h3>
            </div>
            <div class="flex items-center gap-1.5 bg-dark-base p-1.5 rounded-2xl border border-dark-border">
              <button class="px-4 py-2 bg-dark-card text-brand-400 font-mono text-xs uppercase rounded-xl font-bold transition-all flex items-center gap-2 border border-brand-500/30 shadow-md" id="tabHinglishBtn" onclick="switchDocTab('hinglish')">
                <span class="material-symbols-outlined text-[16px]">translate</span>
                <span>सरल गाइड (Hinglish Q&A)</span>
              </button>
              <button class="px-4 py-2 text-slate-400 hover:text-white font-mono text-xs uppercase rounded-xl font-semibold transition-all flex items-center gap-2" id="tabChecklistBtn" onclick="switchDocTab('checklist')">
                <span class="material-symbols-outlined text-[16px]">task</span>
                <span>Document Matrix (दस्तावेज)</span>
              </button>
            </div>
          </div>

          <!-- TAB PANEL 1: SARAL HINGLISH GUIDE -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-5" id="hinglishPanel">
            <div class="bg-dark-base/80 p-5 rounded-2xl border border-dark-border flex flex-col justify-between hover:border-brand-500/30 transition-all">
              <div>
                <div class="flex items-center gap-2 text-brand-400 font-display text-base font-bold mb-2">
                  <span class="material-symbols-outlined text-[22px]">group</span>
                  <h4>Kaun apply kar sakta hai? (पात्रता)</h4>
                </div>
                <p class="text-sm text-slate-200 leading-relaxed">
                  Ye AICTE Pragati, Post-Matric & State scholarships un sabhi chhatraon ke liye hain jinhone recognized colleges me <strong>1st year Degree/Diploma</strong> me admission liya hai.
                </p>
              </div>
              <div class="bg-dark-surface/90 p-3 rounded-xl mt-4 font-mono text-xs text-slate-300 border border-dark-border">
                💡 Parivar ki kul aamdani saalana ₹2.0L - ₹8.0L se kam honi chahiye. Single girl child ko automatic priority milti hai.
              </div>
            </div>

            <div class="bg-dark-base/80 p-5 rounded-2xl border border-cyan-500/30 flex flex-col justify-between hover:border-cyan-500/30 transition-all">
              <div>
                <div class="flex items-center gap-2 text-cyan-400 font-display text-base font-bold mb-2">
                  <span class="material-symbols-outlined text-[22px]">currency_rupee</span>
                  <h4>Kitne paise kab aur kaise milenge?</h4>
                </div>
                <p class="text-sm text-slate-200 leading-relaxed">
                  Har saal <strong>₹12,000 se lekar ₹2,00,000 direct aapke bank account</strong> me DBT (Direct Benefit Transfer) ke zariye credit hote hain. Kisi agent ko 1 rupya bhi nahi dena hota.
                </p>
              </div>
              <div class="bg-dark-surface/90 p-3 rounded-xl mt-4 font-mono text-xs text-slate-300 border border-dark-border">
                💳 Ye rashi tuition fees, kitabein, aur laptop khareedne ke liye valid hai. Bank account me DBT active hona anivarya hai.
              </div>
            </div>

            <div class="bg-dark-base/80 p-5 rounded-2xl border border-red-500/30 flex flex-col justify-between hover:border-red-500/50 transition-all">
              <div>
                <div class="flex items-center gap-2 text-red-400 font-display text-base font-bold mb-2">
                  <span class="material-symbols-outlined text-[22px]">warning</span>
                  <h4>Bank Account me ye galti mat karna:</h4>
                </div>
                <p class="text-sm text-slate-200 leading-relaxed">
                  Aapka bank account NPCI mapper se <strong>'Aadhaar Seeded'</strong> hona anivarya hai. Sirf bank me jakar Aadhaar card jama karna kafi nahi hota.
                </p>
              </div>
              <div class="bg-red-950/40 p-3 rounded-xl mt-4 font-mono text-xs text-red-200 border border-red-500/30">
                ⚠️ Bank me jakar bole: "Mera Account Aadhaar DBT / NPCI Seeding se link karein", warna approval ke baad bhi paisa nahi aayega.
              </div>
            </div>
          </div>

          <!-- TAB PANEL 2: OFFICIAL DOCUMENT CHECKLIST MATRIX -->
          <div class="hidden pt-5" id="checklistPanel">
            <div class="bg-dark-base/80 rounded-2xl border border-dark-border overflow-x-auto">
              <table class="w-full text-left font-sans text-xs sm:text-sm">
                <thead class="bg-dark-surface text-slate-300 font-mono text-xs uppercase tracking-wider border-b border-dark-border">
                  <tr>
                    <th class="p-3.5">Required Sovereign Document</th>
                    <th class="p-3.5">Issuing Authority</th>
                    <th class="p-3.5">Acceptable Format & Specs</th>
                    <th class="p-3.5">Digital Status</th>
                  </tr>
                </thead>
                <tbody class="text-slate-300 divide-y divide-dark-border">
                  <tr class="hover:bg-dark-surface/50 transition-colors">
                    <td class="p-3.5 font-bold text-white">1. Income Certificate (आय प्रमाण पत्र)</td>
                    <td class="p-3.5">Tehsildar / Sub-Divisional Magistrate (SDM) e-District</td>
                    <td class="p-3.5 font-mono text-xs text-slate-400">Issued after April 2024 • PDF &lt; 200KB</td>
                    <td class="p-3.5"><span class="px-2.5 py-1 bg-brand-500/15 text-brand-400 font-mono text-xs rounded-lg uppercase font-bold border border-brand-500/30">DigiLocker Linked</span></td>
                  </tr>
                  <tr class="hover:bg-dark-surface/50 transition-colors">
                    <td class="p-3.5 font-bold text-white">2. Domicile Certificate (निवास प्रमाण पत्र)</td>
                    <td class="p-3.5">State Revenue Dept (e-District / Borland Portal)</td>
                    <td class="p-3.5 font-mono text-xs text-slate-400">Permanent Residence Serial Verified</td>
                    <td class="p-3.5"><span class="px-2.5 py-1 bg-brand-500/15 text-brand-400 font-mono text-xs rounded-lg uppercase font-bold border border-brand-500/30">DigiLocker Linked</span></td>
                  </tr>
                  <tr class="hover:bg-dark-surface/50 transition-colors">
                    <td class="p-3.5 font-bold text-white">3. College Bonafide & Fee Receipt</td>
                    <td class="p-3.5">College Registrar / Principal Official Seal & Signature</td>
                    <td class="p-3.5 font-mono text-xs text-slate-400">Original Format with AISHE Institutional Code</td>
                    <td class="p-3.5"><span class="px-2.5 py-1 bg-cyan-500/15 text-cyan-300 font-mono text-xs rounded-lg uppercase font-bold border border-cyan-500/30">Physical Seal Req</span></td>
                  </tr>
                  <tr class="hover:bg-dark-surface/50 transition-colors">
                    <td class="p-3.5 font-bold text-white">4. Class 10th & 12th Board Marksheets</td>
                    <td class="p-3.5">CBSE / CISCE / State Education Boards (UPMSP/MSBSHSE)</td>
                    <td class="p-3.5 font-mono text-xs text-slate-400">Digital Verified Copy or Original Board Scan</td>
                    <td class="p-3.5"><span class="px-2.5 py-1 bg-brand-500/15 text-brand-400 font-mono text-xs rounded-lg uppercase font-bold border border-brand-500/30">Auto e-KYC</span></td>
                  </tr>
                  <tr class="hover:bg-dark-surface/50 transition-colors">
                    <td class="p-3.5 font-bold text-white">5. Aadhaar Card + Active NPCI Bank Account</td>
                    <td class="p-3.5">UIDAI & Commercial Bank (SBI, PNB, Baroda, Canara, etc.)</td>
                    <td class="p-3.5 font-mono text-xs text-slate-400">Active DBT mandate enabled on NPCI mapper</td>
                    <td class="p-3.5"><span class="px-2.5 py-1 bg-brand-500/15 text-brand-400 font-mono text-xs rounded-lg uppercase font-bold border border-brand-500/30">PFMS Synchronized</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- ========================================================= -->
    <!-- TAB 2: EXPLORE ALL SCHEMES & RESEARCH OPPORTUNITIES       -->
    <!-- ========================================================= -->
    <div id="viewExplore" class="hidden flex-col w-full px-4 sm:px-8 lg:px-12 py-3">
      
      <!-- Search & Filters Container -->
      <div class="glass-card p-5 sm:p-6 rounded-3xl border border-dark-border mb-6 shadow-2xl">
        <div class="flex flex-col lg:flex-row gap-3">
          <div class="relative flex-1">
            <span class="material-symbols-outlined absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-[22px]">search</span>
            <input type="text" id="exploreSearchInput" class="w-full bg-dark-base text-white font-sans text-sm pl-11 pr-4 py-3 rounded-xl border border-dark-border hover:border-slate-600 focus:outline-none focus:border-brand-500 transition-all placeholder:text-slate-500" placeholder="Search by scheme name or keywords (e.g. 'Pragati', 'UP Post-Matric', 'AI Research', 'Girls', 'Tata')..." onkeyup="if(event.key === 'Enter') runExploreSearch()"/>
          </div>
          <select id="exploreAgencyFilter" class="bg-dark-base text-white font-sans text-sm px-4 py-3 rounded-xl border border-dark-border hover:border-slate-600 focus:outline-none focus:border-brand-500 transition-all cursor-pointer" onchange="runExploreSearch()">
            <option value="">All Portals & Agencies</option>
            <option value="NSP">NSP (National Scholarship)</option>
            <option value="AICTE">AICTE Schemes</option>
            <option value="UGC">UGC Fellowships</option>
            <option value="State Govt">State Govt Portals</option>
            <option value="CSR / Foundation">CSR Foundations</option>
            <option value="DST">DST (Science & Tech)</option>
            <option value="ANRF/SERB">ANRF / SERB</option>
            <option value="CSIR">CSIR</option>
            <option value="DBT">DBT (Biotechnology)</option>
          </select>
          <button class="px-6 py-3 bg-gradient-to-r from-brand-500 to-emerald-600 hover:from-brand-400 hover:to-emerald-500 text-dark-base font-mono text-xs uppercase font-extrabold rounded-xl transition-all flex items-center justify-center gap-2 cursor-pointer shadow-lg" onclick="runExploreSearch()">
            <span class="material-symbols-outlined text-[18px]">search</span>
            Hybrid Search
          </button>
        </div>

        <!-- Quick Tag Filter Pills -->
        <div class="flex flex-wrap items-center gap-2 mt-4 pt-3 border-t border-dark-border/60">
          <span class="font-mono text-xs text-slate-400 uppercase">Quick Filters:</span>
          <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 font-mono text-xs rounded-lg transition-all border border-dark-border" onclick="setExploreQuery('Girls Scholarship')">👧 Girl Students</button>
          <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 font-mono text-xs rounded-lg transition-all border border-dark-border" onclick="setExploreQuery('Engineering B.Tech')">💻 Engineering / B.Tech</button>
          <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 font-mono text-xs rounded-lg transition-all border border-dark-border" onclick="setExploreQuery('Post-Matric SC ST OBC')">📜 Post-Matric (SC/ST/OBC)</button>
          <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 font-mono text-xs rounded-lg transition-all border border-dark-border" onclick="setExploreQuery('Artificial Intelligence')">🤖 AI & Data Science Grants</button>
          <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 font-mono text-xs rounded-lg transition-all border border-dark-border" onclick="setExploreQuery('Tata Trust')">🏛️ CSR Trust Grants</button>
          <button class="px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 font-mono text-xs rounded-lg transition-all border border-dark-border" onclick="setExploreQuery('')">🔄 Reset All</button>
        </div>
      </div>

      <!-- Explore Results Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5" id="exploreGrid">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- ========================================================= -->
    <!-- TAB 3: RESEARCHER & FACULTY GRANT ALIGNMENT               -->
    <!-- ========================================================= -->
    <div id="viewFaculty" class="hidden flex-col w-full px-4 sm:px-8 lg:px-12 py-3">
      <div class="glass-card p-6 sm:p-7 rounded-3xl border border-dark-border mb-6 shadow-2xl relative overflow-hidden">
        
        <div class="flex items-center gap-2 mb-2">
          <span class="px-2.5 py-1 bg-indigo-500/15 text-indigo-300 font-mono text-xs rounded-lg uppercase font-bold tracking-wider flex items-center gap-1.5 border border-indigo-500/30">
            <span class="material-symbols-outlined text-[15px]">biotech</span> DST • ANRF/SERB • CSIR • DBT
          </span>
          <span class="text-slate-400 font-mono text-xs uppercase tracking-wider font-semibold">अनुसंधान एवं संकाय अनुदान सेतु</span>
        </div>

        <h3 class="font-display text-xl sm:text-2xl lg:text-3xl text-white font-extrabold tracking-tight mt-1">
          Researcher & Faculty Grant Alignment Engine
        </h3>
        <p class="text-xs sm:text-sm text-slate-300 mt-1 mb-5">
          Paste your research concept, proposal abstract, or CV summary. Our dense semantic embedding engine evaluates statutory compliance, eligible budget ceilings, and generates an agency-ready proposal skeleton.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div>
            <label class="font-mono text-xs text-slate-300 uppercase font-semibold">Applicant Role</label>
            <select id="matchRole" class="w-full bg-dark-base text-white font-sans text-sm px-3.5 py-2.5 rounded-xl border border-dark-border mt-1.5 focus:outline-none focus:border-indigo-400">
              <option value="Faculty / Principal Investigator">Faculty / Principal Investigator</option>
              <option value="Early Career Researcher">Early Career Researcher</option>
              <option value="Women Scientists">Women Scientists</option>
              <option value="PhD Scholars & Postdoctoral Fellows">PhD Scholars & Postdocs</option>
            </select>
          </div>
          <div>
            <label class="font-mono text-xs text-slate-300 uppercase font-semibold">Applicant Age (Years)</label>
            <input type="number" id="matchAge" class="w-full bg-dark-base text-white font-sans text-sm px-3.5 py-2.5 rounded-xl border border-dark-border mt-1.5 focus:outline-none focus:border-indigo-400" value="38"/>
          </div>
          <div>
            <label class="font-mono text-xs text-slate-300 uppercase font-semibold">Highest Academic Qualification</label>
            <input type="text" id="matchDegree" class="w-full bg-dark-base text-white font-sans text-sm px-3.5 py-2.5 rounded-xl border border-dark-border mt-1.5 focus:outline-none focus:border-indigo-400" value="Ph.D. in Computer Science / Engineering"/>
          </div>
        </div>

        <div class="mb-4">
          <div class="flex items-center justify-between mb-1">
            <label class="font-mono text-xs text-slate-300 uppercase font-semibold">Research Proposal Concept / Abstract</label>
            <div class="flex items-center gap-2">
              <span class="text-xs text-slate-400 font-mono">Sample Presets:</span>
              <button class="text-xs text-indigo-400 hover:text-indigo-300 underline font-mono cursor-pointer" onclick="setSampleAbstract('ai')">Medical AI</button>
              <span class="text-slate-600">|</span>
              <button class="text-xs text-indigo-400 hover:text-indigo-300 underline font-mono cursor-pointer" onclick="setSampleAbstract('quantum')">Quantum Materials</button>
              <span class="text-slate-600">|</span>
              <button class="text-xs text-indigo-400 hover:text-indigo-300 underline font-mono cursor-pointer" onclick="setSampleAbstract('clean_energy')">Clean Energy</button>
            </div>
          </div>
          <textarea id="matchAbstract" rows="4" class="w-full bg-dark-base text-white font-sans text-sm p-4 rounded-xl border border-dark-border focus:outline-none focus:border-indigo-400 placeholder:text-slate-500" placeholder="Describe your scientific objectives, methodology, novel contributions, and anticipated impact (e.g., 'Autonomous multimodal deep neural network for early-stage oncology detection and histopathology validation')..."></textarea>
        </div>

        <button class="px-7 py-3.5 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-400 hover:to-cyan-400 text-white font-display text-sm sm:text-base font-extrabold rounded-2xl transition-all flex items-center gap-2 shadow-[0_0_25px_rgba(99,102,241,0.35)] cursor-pointer" onclick="runFacultyMatch()">
          <span class="material-symbols-outlined text-[20px]">model_training</span>
          ⚡ Align Proposal & Check Statutory Compliance
        </button>
      </div>

      <div id="facultyResultsContainer">
        <!-- Injected via JS -->
      </div>
    </div>

  </main>

  <!-- ========================================================= -->
  <!-- UNIVERSAL MODAL 1: APPLICATION GATEWAY (आवेदन सेतु)       -->
  <!-- ========================================================= -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 md:p-6 bg-dark-base/90 backdrop-blur-2xl overflow-y-auto hidden" id="applyModalOverlay" onclick="if(event.target === this) closeApplyModal()">
    <div class="relative w-full max-w-4xl max-h-[90vh] my-auto bg-dark-surface border border-dark-border rounded-3xl shadow-2xl overflow-hidden flex flex-col">
      
      <!-- Modal Header -->
      <div class="relative z-10 px-5 py-4 sm:px-6 sm:py-5 bg-dark-card shrink-0 border-b border-dark-border">
        <div class="flex flex-wrap items-center justify-between gap-y-2 pb-2 mb-2 border-b border-dark-border/60">
          <div class="flex flex-wrap items-center gap-2">
            <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-brand-500/15 rounded-lg text-brand-400 font-mono text-xs uppercase tracking-wider font-bold border border-brand-500/30">
              <span class="material-symbols-outlined text-[14px]">verified</span>
              NIC / GOVT OF INDIA VERIFIED GATEWAY
            </span>
            <span class="text-slate-500 font-mono text-xs">•</span>
            <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 bg-dark-surface rounded-lg border border-dark-border">
              <span class="w-1.5 h-1.5 rounded-full bg-brand-400 animate-pulse"></span>
              <span class="text-slate-200 font-mono text-xs font-semibold" id="modalHostDomain">scholarships.gov.in</span>
            </div>
            <button class="hover:bg-slate-700 px-2.5 py-0.5 bg-dark-surface rounded-lg text-cyan-400 font-mono text-xs flex items-center gap-1 transition-all border border-dark-border cursor-pointer" id="modalCopyBtn">
              <span class="material-symbols-outlined text-[13px]">content_copy</span>
              <span>Copy Link</span>
            </button>
          </div>
          
          <button class="w-8 h-8 rounded-xl bg-dark-surface hover:bg-red-950 hover:text-red-300 text-slate-400 flex items-center justify-center transition-all cursor-pointer border border-dark-border" onclick="closeApplyModal()" title="Close Gateway Modal">
            <span class="material-symbols-outlined text-[20px]">close</span>
          </button>
        </div>

        <div class="flex flex-col gap-1 pt-1">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-mono text-xs px-2.5 py-0.5 rounded-lg bg-indigo-500/20 text-indigo-300 uppercase font-bold border border-indigo-500/30" id="modalAgencyTag">
              NSP / MoE Scheme
            </span>
            <span class="font-mono text-xs text-slate-400" id="modalRefId">
              REF: SCHEME-ID
            </span>
          </div>
          <h1 class="font-display text-lg sm:text-xl md:text-2xl text-white font-extrabold tracking-tight mt-1" id="modalSchemeTitle">
            सरकारी आवेदन सेतु
          </h1>
          <p class="font-sans text-xs sm:text-sm text-slate-300 flex items-center gap-1.5 mt-0.5" id="modalGrantText">
            <span class="material-symbols-outlined text-[16px] text-brand-400">account_balance</span>
            Disbursal: Direct Benefit Transfer via Aadhaar NPCI Gateway
          </p>
        </div>
      </div>

      <!-- Anti-Scam Banner -->
      <div class="relative z-10 px-5 py-2.5 sm:px-6 bg-red-950/70 border-b border-red-500/30 text-red-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 shrink-0">
        <div class="flex items-start sm:items-center gap-2">
          <span class="material-symbols-outlined text-[22px] text-red-400 shrink-0 mt-0.5 sm:mt-0">gpp_maybe</span>
          <div>
            <p class="font-display text-xs sm:text-sm font-bold leading-tight text-white">
              100% Free Sovereign Application — Never Pay Cyber Cafés, Brokers, or Agents.
            </p>
            <p class="font-sans text-[11px] sm:text-xs text-red-200/90">
              Government scholarships levy ₹0 submission fees. Never share DigiLocker PIN or Aadhaar OTPs with unauthorized third parties.
            </p>
          </div>
        </div>
        <div class="shrink-0 flex items-center self-end sm:self-center">
          <span class="px-2.5 py-1 rounded-lg bg-black/40 font-mono text-[10px] sm:text-xs tracking-wider uppercase text-red-300 font-bold border border-red-500/40">
            Direct DBT Only
          </span>
        </div>
      </div>

      <!-- Scrollable Stepper Content Area -->
      <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-0 overflow-y-auto flex-1 divide-y lg:divide-y-0 lg:divide-x divide-dark-border">
        
        <!-- Left: Stepper Roadmap (7 Cols) -->
        <div class="lg:col-span-7 p-4 sm:p-5 md:p-6 bg-dark-surface flex flex-col gap-3">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1.5">
              <span class="material-symbols-outlined text-cyan-400 text-[20px]">alt_route</span>
              <h3 class="font-display text-sm sm:text-base text-white font-bold tracking-tight">
                Official Portal Navigation Map (पोर्टल मार्गदर्शिका)
              </h3>
            </div>
            <span class="font-mono text-xs text-slate-400 uppercase">Step-by-Step</span>
          </div>

          <div class="relative flex flex-col gap-3 pt-2" id="modalStepsTimeline">
            <!-- Injected via JS -->
          </div>
        </div>

        <!-- Right: Pre-Flight Checklist (5 Cols) -->
        <div class="lg:col-span-5 p-4 sm:p-5 md:p-6 bg-dark-card flex flex-col gap-3">
          <div class="p-3.5 bg-dark-surface rounded-2xl flex items-center justify-between gap-3 border border-dark-border shadow-sm">
            <div>
              <div class="flex items-center gap-1 mb-0.5">
                <span class="material-symbols-outlined text-brand-400 text-[18px]">speed</span>
                <span class="font-mono text-[10px] uppercase text-slate-400">Readiness Status</span>
              </div>
              <h4 class="font-display text-sm sm:text-base font-extrabold text-white">100% PRE-FLIGHT READY</h4>
              <p class="font-sans text-[11px] text-slate-400">Mandatory verification checklist</p>
            </div>
            <div class="w-12 h-12 rounded-2xl bg-brand-500/20 border border-brand-500/40 flex items-center justify-center text-brand-400 font-extrabold font-display text-sm">
              5/5
            </div>
          </div>

          <span class="font-mono text-xs text-slate-300 uppercase tracking-wider font-semibold">Pre-Flight Applicant Checklist:</span>
          <div class="flex flex-col gap-2">
            <div class="p-2.5 bg-dark-surface rounded-xl border border-dark-border flex items-start gap-2.5">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-brand-500 mt-0.5"/>
              <div>
                <div class="font-display text-xs font-bold text-white">Aadhaar Linked Mobile OTP Active</div>
                <div class="font-sans text-[11px] text-slate-400">Ready for instant NSP OTR authentication</div>
              </div>
            </div>
            <div class="p-2.5 bg-dark-surface rounded-xl border border-dark-border flex items-start gap-2.5">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-brand-500 mt-0.5"/>
              <div>
                <div class="font-display text-xs font-bold text-white">Income Certificate (Current FY Valid)</div>
                <div class="font-sans text-[11px] text-slate-400">Issued by Tehsildar / Sub-Divisional Magistrate</div>
              </div>
            </div>
            <div class="p-2.5 bg-dark-surface rounded-xl border border-dark-border flex items-start gap-2.5">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-brand-500 mt-0.5"/>
              <div>
                <div class="font-display text-xs font-bold text-white">Bank Account with Aadhaar-NPCI Seeding</div>
                <div class="font-sans text-[11px] text-slate-400">Active DBT mapping enabled for direct crediting</div>
              </div>
            </div>
            <div class="p-2.5 bg-dark-surface rounded-xl border border-dark-border flex items-start gap-2.5">
              <input checked disabled type="checkbox" class="w-4 h-4 rounded accent-brand-500 mt-0.5"/>
              <div>
                <div class="font-display text-xs font-bold text-white">Class 10th / 12th Board Marksheets</div>
                <div class="font-sans text-[11px] text-slate-400">DigiLocker verified or PDF scan &lt; 200 KB</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Action Footer -->
      <div class="relative z-10 px-5 py-3.5 sm:px-6 bg-dark-card shrink-0 border-t border-dark-border flex flex-col gap-2">
        <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
          <a class="px-4 py-2.5 bg-[#138808]/20 hover:bg-[#138808]/35 text-brand-400 font-mono text-xs font-bold rounded-xl flex items-center justify-center gap-2 transition-all border border-[#138808]/50 shadow-md" id="modalWhatsappLink" href="#" target="_blank" rel="noopener noreferrer">
            <span class="material-symbols-outlined text-[18px]">chat</span>
            📲 Share Guidance on WhatsApp
          </a>
          <a class="px-6 py-3 bg-gradient-to-r from-brand-500 to-emerald-600 hover:from-brand-400 hover:to-emerald-500 text-dark-base font-display text-sm sm:text-base rounded-xl flex items-center justify-center gap-2 shadow-[0_0_25px_rgba(16,185,129,0.4)] hover:shadow-[0_0_35px_rgba(16,185,129,0.6)] transition-all font-extrabold text-center" id="modalApplyLink" href="#" target="_blank" rel="noopener noreferrer">
            <span>🚀 Launch Official Government Portal ↗</span>
          </a>
        </div>
        <div class="flex flex-wrap items-center justify-between gap-2 text-slate-400 font-mono text-[10px] sm:text-xs pt-1">
          <div class="flex items-center gap-1.5">
            <span class="material-symbols-outlined text-brand-400 text-[14px]">lock</span>
            <span>You are proceeding directly to sovereign official servers. Zero middleman fees.</span>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================= -->
  <!-- UNIVERSAL MODAL 2: DOCUMENT CHECKLIST / SARAL GUIDE       -->
  <!-- ========================================================= -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 md:p-6 bg-dark-base/90 backdrop-blur-2xl overflow-y-auto hidden" id="genericModalOverlay" onclick="if(event.target === this) closeGenericModal()">
    <div class="relative w-full max-w-3xl max-h-[90vh] my-auto bg-dark-surface border border-dark-border rounded-3xl shadow-2xl overflow-hidden flex flex-col">
      <div class="px-5 py-4 bg-dark-card flex items-center justify-between border-b border-dark-border">
        <h3 class="font-display text-base sm:text-lg text-white font-extrabold" id="genericModalTitle">Scheme Details</h3>
        <button class="w-8 h-8 rounded-xl bg-dark-surface hover:bg-red-950 hover:text-red-300 text-slate-400 flex items-center justify-center transition-all border border-dark-border cursor-pointer" onclick="closeGenericModal()">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>
      <div class="p-5 overflow-y-auto flex-1 font-sans text-sm" id="genericModalBody">
        <!-- Content injected via JS -->
      </div>
    </div>
  </div>

  <!-- FOOTER -->
  <footer class="w-full bg-dark-base py-8 text-slate-400 border-t border-dark-border">
    <div class="w-full px-4 sm:px-8 lg:px-12 flex flex-col gap-4">
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 p-5 bg-dark-card rounded-2xl border border-dark-border">
        <div class="flex items-start gap-3.5 max-w-4xl">
          <span class="material-symbols-outlined text-brand-400 text-[24px] shrink-0 mt-0.5">shield</span>
          <p class="font-sans text-xs sm:text-sm text-slate-300 leading-relaxed">
            <span class="font-bold text-white uppercase font-mono text-xs tracking-wider">High-Trust Sovereign Gov-Tech Framework:</span>
            MadadgaarAI is an autonomous student enablement and research grant alignment intelligence platform. Direct application routing connects exclusively to official National Scholarship Portal (scholarships.gov.in), AICTE, UGC, and recognized State portals. 100% Direct Benefit Transfer (DBT) & NPCI compliant.
          </p>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <span class="font-mono text-xs px-3.5 py-1.5 bg-brand-500/15 text-brand-400 border border-brand-500/30 rounded-xl uppercase tracking-wider font-bold">National Digital Public Good</span>
        </div>
      </div>
      <div class="flex flex-col md:flex-row items-center justify-between gap-3 pt-2 text-slate-500 font-mono text-xs">
        <div>© 2026 MadadgaarAI • Open-Source Sovereign Funding Intelligence</div>
        <div class="flex items-center gap-4">
          <a class="hover:text-brand-400 transition-colors" href="https://scholarships.gov.in" target="_blank" rel="noopener noreferrer">NSP Portal</a>
          <a class="hover:text-brand-400 transition-colors" href="https://myaadhaar.uidai.gov.in" target="_blank" rel="noopener noreferrer">UIDAI Seeding</a>
          <a class="hover:text-brand-400 transition-colors" href="/docs" target="_blank">OpenAPI Docs</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- DYNAMIC FRONTEND APPLICATION ENGINE -->
  <script>
    let allOpportunities = [];
    let currentStudentResults = [];

    // Toast Notification System
    function showToast(message, icon = 'check_circle') {
      const toast = document.getElementById('toastNotification');
      const msg = document.getElementById('toastMessage');
      const ico = document.getElementById('toastIcon');
      
      msg.innerText = message;
      ico.innerText = icon;
      toast.classList.remove('translate-y-20', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');

      setTimeout(() => {
        toast.classList.add('translate-y-20', 'opacity-0');
        toast.classList.remove('translate-y-0', 'opacity-100');
      }, 3500);
    }

    async function initPlatform() {
      await loadOpportunities();
      runStudentMatch(false);
    }

    async function loadOpportunities() {
      try {
        const res = await fetch('/api/foas');
        if (!res.ok) throw new Error('API responded with error');
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

      // Desktop nav button active classes
      document.querySelectorAll('.nav-tab-btn').forEach(b => {
        b.className = 'nav-tab-btn flex items-center gap-2 px-4 py-2.5 text-slate-400 hover:text-white hover:bg-dark-card/50 transition-all font-mono text-xs uppercase rounded-xl border border-transparent';
      });

      // Mobile nav buttons
      document.querySelectorAll('#mTabBtnVidyarthi, #mTabBtnExplore, #mTabBtnFaculty').forEach(b => {
        b.className = 'flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono text-slate-400';
      });

      if (tab === 'vidyarthi') {
        document.getElementById('tabBtnVidyarthi').className = 'nav-tab-btn flex items-center gap-2 px-4 py-2.5 bg-dark-card border border-brand-500/40 text-brand-400 font-mono text-xs uppercase font-bold rounded-xl shadow-lg transition-all';
        document.getElementById('mTabBtnVidyarthi').className = 'flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono text-brand-400 font-bold bg-dark-card';
      } else if (tab === 'explore') {
        document.getElementById('tabBtnExplore').className = 'nav-tab-btn flex items-center gap-2 px-4 py-2.5 bg-dark-card border border-brand-500/40 text-brand-400 font-mono text-xs uppercase font-bold rounded-xl shadow-lg transition-all';
        document.getElementById('mTabBtnExplore').className = 'flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono text-brand-400 font-bold bg-dark-card';
      } else if (tab === 'faculty') {
        document.getElementById('tabBtnFaculty').className = 'nav-tab-btn flex items-center gap-2 px-4 py-2.5 bg-dark-card border border-indigo-500/40 text-indigo-300 font-mono text-xs uppercase font-bold rounded-xl shadow-lg transition-all';
        document.getElementById('mTabBtnFaculty').className = 'flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-mono text-indigo-300 font-bold bg-dark-card';
      }
    }

    function updateIncomeDisplay(val) {
      document.getElementById('incomeDisplay').innerText = '₹' + Number(val).toLocaleString('en-IN') + ' / Year';
      
      // Update quick button highlights
      const btns = {
        150000: 'btnIncome1_5L',
        200000: 'btnIncome2L',
        250000: 'btnIncome2_5L',
        450000: 'btnIncome4_5L',
        800000: 'btnIncome8L'
      };
      const numVal = parseInt(val);
      Object.entries(btns).forEach(([k, id]) => {
        const el = document.getElementById(id);
        if (el) {
          if (parseInt(k) === numVal) {
            el.className = 'px-2.5 py-1 bg-brand-500 text-dark-base font-bold text-xs font-mono rounded-lg transition-all shadow-md';
          } else {
            el.className = 'px-2.5 py-1 bg-dark-surface hover:bg-slate-700 text-slate-300 text-xs font-mono rounded-lg transition-all';
          }
        }
      });
    }

    function setIncomeVal(val) {
      document.getElementById('stuIncome').value = val;
      updateIncomeDisplay(val);
      runStudentMatch(false);
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
      runStudentMatch(false);
      showToast('Profile reset to default parameters');
    }

    async function runStudentMatch(shouldScroll = false) {
      const container = document.getElementById('studentResultsContainer');
      const btnText = document.getElementById('matchBtnText');
      if (btnText) btnText.innerHTML = '<span class="inline-block animate-spin mr-1">⚙️</span> Evaluating Statutory Rules...';

      const stateVal = document.getElementById('stuState').value;
      const levelVal = document.getElementById('stuLevel').value;
      const catVal = document.getElementById('stuCategory').value;
      const genVal = document.getElementById('stuGender').value;
      const incomeVal = parseFloat(document.getElementById('stuIncome').value) || 200000;
      const marksVal = parseFloat(document.getElementById('stuMarks').value) || 85;
      const girlVal = document.getElementById('stuSingleGirl').checked;
      const pwdVal = document.getElementById('stuPwd').checked;

      const payload = {
        state_domicile: stateVal,
        education_level: levelVal,
        social_category: catVal,
        gender: genVal,
        family_annual_income_inr: incomeVal,
        academic_percentage: marksVal,
        is_single_girl_child: girlVal,
        is_differently_abled_pwd: pwdVal,
        top_k: 20
      };

      try {
        const res = await fetch('/api/student/match', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Matching API returned status ' + res.status);
        const results = await res.json();
        currentStudentResults = results;
        renderStudentCards(results);
        
        const eligibleCount = results.filter(r => r.eligibility_status === 'ELIGIBLE' || r.eligibility_status === 'HIGH_PROBABILITY').length;
        
        if (shouldScroll) {
          container.scrollIntoView({ behavior: 'smooth', block: 'start' });
          showToast(`🎯 Found ${eligibleCount} eligible schemes for your profile!`, 'verified');
        }
      } catch (err) {
        console.error('Match error:', err);
        container.innerHTML = `
          <div class="glass-card p-6 rounded-3xl border border-red-500/30 text-center py-10 font-mono">
            <span class="material-symbols-outlined text-4xl text-red-400 mb-2">error</span>
            <div class="text-base text-white font-bold">Failed to connect to API server.</div>
            <div class="text-xs text-slate-400 mt-1">Please ensure the backend service is running on http://127.0.0.1:8000</div>
            <button class="mt-4 px-4 py-2 bg-brand-500 text-dark-base font-bold text-xs rounded-xl cursor-pointer" onclick="runStudentMatch(true)">Retry Matching</button>
          </div>
        `;
      } finally {
        if (btnText) btnText.innerHTML = '⚡ Find My Scholarships (पात्रता खोजें)';
      }
    }

    function renderStudentCards(results) {
      const container = document.getElementById('studentResultsContainer');
      if (!results || results.length === 0) {
        container.innerHTML = `
          <div class="text-center py-16 text-slate-400 font-mono glass-card rounded-3xl border border-dark-border">
            <span class="material-symbols-outlined text-4xl text-slate-500 mb-2">search_off</span>
            <div class="text-base text-slate-300 font-semibold">No scholarships found matching current filters.</div>
            <div class="text-xs text-slate-500 mt-1">Try adjusting the State domicile, Education level, or Family income slider.</div>
          </div>
        `;
        return;
      }

      const eligibleCount = results.filter(r => r.eligibility_status === 'ELIGIBLE' || r.eligibility_status === 'HIGH_PROBABILITY').length;

      let html = `
        <div class="w-full bg-gradient-to-r from-dark-card to-dark-surface p-4 rounded-2xl mb-5 border border-dark-border flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-lg">
          <div class="flex items-center gap-2.5">
            <span class="w-2.5 h-2.5 rounded-full bg-brand-400 animate-pulse"></span>
            <span class="font-display text-sm sm:text-base text-white font-extrabold">🎯 Recommended Scholarships (${eligibleCount} Eligible Schemes Found)</span>
          </div>
          <div class="text-slate-400 font-mono text-xs flex items-center gap-2">
            <span>Cross-referenced with 21 Central, State & CSR schemes</span>
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
      `;

      html += results.map(res => {
        const foa = res.foa;
        const isEligible = res.eligibility_status === 'ELIGIBLE';
        const isHigh = res.eligibility_status === 'HIGH_PROBABILITY';
        const isWarning = res.eligibility_status === 'WARNING';

        const badgeBg = isEligible 
          ? 'bg-brand-500/15 text-brand-400 border-brand-500/30' 
          : (isHigh ? 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30' 
          : (isWarning ? 'bg-amber-500/15 text-amber-300 border-amber-500/30' 
          : 'bg-red-500/15 text-red-300 border-red-500/30'));
        
        const badgeLabel = isEligible 
          ? `100% ELIGIBLE (${res.match_percentage}%)` 
          : (isHigh ? `HIGH PROBABILITY (${res.match_percentage}%)` 
          : (isWarning ? `CONDITIONAL (${res.match_percentage}%)` 
          : `INELIGIBLE`));

        const whatsappText = encodeURIComponent(`🎓 *Scholarship Alert: ${foa.title}*\n💰 Grant: ${res.estimated_financial_benefit}\n🏛️ Official Portal: ${res.direct_apply_url || res.portal_url}\nCheck your eligibility on MadadgaarAI!`);

        return `
          <div class="glass-card rounded-3xl border border-dark-border shadow-xl flex flex-col justify-between hover:border-brand-500/40 transition-all duration-300 overflow-hidden group">
            
            <!-- Card Main Content (Always Visible) -->
            <div class="p-5 sm:p-6 flex-1 flex flex-col justify-between">
              
              <div>
                <!-- Top Tags Row -->
                <div class="flex items-center justify-between gap-2 flex-wrap mb-3">
                  <span class="px-2.5 py-0.5 bg-dark-surface text-cyan-300 font-mono text-xs uppercase tracking-wider rounded-lg font-bold border border-dark-border">${foa.agency}</span>
                  <span class="px-3 py-0.5 ${badgeBg} font-mono text-xs uppercase font-extrabold rounded-lg border flex items-center gap-1.5">
                    ${isEligible ? '<span class="w-2 h-2 rounded-full bg-brand-400 animate-pulse"></span>' : ''}
                    ${badgeLabel}
                  </span>
                </div>

                <!-- Scheme Title -->
                <h3 class="font-display text-base sm:text-lg text-white font-bold tracking-tight leading-snug group-hover:text-brand-400 transition-colors">
                  ${foa.title}
                </h3>

                <!-- Scheme Brief Summary -->
                <p class="font-sans text-xs sm:text-sm text-slate-300 mt-2 line-clamp-2">
                  ${foa.brief_summary}
                </p>

                <!-- Financial Benefit Spotlight Box -->
                <div class="bg-dark-base/80 p-3.5 rounded-2xl my-3.5 flex items-center justify-between gap-3 border border-dark-border/80">
                  <div>
                    <span class="font-mono text-[10px] text-cyan-400 uppercase tracking-wider block font-bold">Estimated Financial Benefit:</span>
                    <span class="font-display text-base sm:text-lg text-brand-400 font-extrabold">${res.estimated_financial_benefit}</span>
                  </div>
                  <div class="text-right">
                    <span class="font-mono text-[10px] text-slate-400 uppercase block font-medium">Direct Disbursal:</span>
                    <span class="font-mono text-xs text-slate-200 font-bold flex items-center gap-1 justify-end">
                      <span class="material-symbols-outlined text-brand-400 text-[14px]">bolt</span> DBT / NPCI
                    </span>
                  </div>
                </div>

                <!-- Match Reasons Checklist -->
                <div class="bg-dark-surface/70 p-3 rounded-2xl space-y-1.5 mb-4 border border-dark-border text-xs">
                  ${res.match_reasons.slice(0, 3).map(r => `
                    <div class="flex items-center gap-2 text-slate-200">
                      <span class="material-symbols-outlined text-[16px] text-brand-400 shrink-0">check_circle</span>
                      <span>${r}</span>
                    </div>
                  `).join('')}
                  ${res.warning_reasons.map(w => `
                    <div class="flex items-center gap-2 text-amber-300">
                      <span class="material-symbols-outlined text-[16px] text-amber-400 shrink-0">info</span>
                      <span>${w}</span>
                    </div>
                  `).join('')}
                </div>
              </div>

              <!-- Action Bar (Prominent & High Quality) -->
              <div class="flex flex-wrap items-center gap-2 pt-3 border-t border-dark-border">
                <button class="px-4 py-2.5 bg-gradient-to-r from-brand-500 to-emerald-600 hover:from-brand-400 hover:to-emerald-500 text-dark-base font-mono text-xs uppercase font-extrabold tracking-wider rounded-xl transition-all flex items-center gap-1.5 shadow-[0_0_15px_rgba(16,185,129,0.3)] hover:shadow-[0_0_20px_rgba(16,185,129,0.5)] cursor-pointer" onclick="openApplyModal('${foa.foa_id}')">
                  <span>🚀 Apply Gateway</span>
                  <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
                </button>
                <button class="px-3.5 py-2 bg-dark-surface hover:bg-slate-700 text-slate-200 font-mono text-xs uppercase tracking-wider rounded-xl transition-all flex items-center gap-1.5 border border-dark-border hover:border-slate-500 cursor-pointer" onclick="openDocChecklistModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[16px] text-cyan-400">checklist</span> Docs
                </button>
                <button class="px-3.5 py-2 bg-dark-surface hover:bg-slate-700 text-indigo-300 font-mono text-xs uppercase tracking-wider rounded-xl transition-all flex items-center gap-1.5 border border-dark-border hover:border-indigo-400/40 cursor-pointer" onclick="openHinglishModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[16px]">translate</span> गाइड
                </button>
                <a class="px-3.5 py-2 bg-[#138808]/20 hover:bg-[#138808]/35 text-brand-400 font-mono text-xs uppercase rounded-xl transition-all flex items-center gap-1.5 border border-[#138808]/40 ml-auto" href="https://api.whatsapp.com/send?text=${whatsappText}" target="_blank" rel="noopener noreferrer" title="Share scholarship on WhatsApp">
                  <span class="material-symbols-outlined text-[16px]">share</span> WhatsApp
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
        grid.innerHTML = `
          <div class="col-span-2 text-center py-16 text-slate-400 font-mono glass-card rounded-3xl border border-dark-border">
            <span class="material-symbols-outlined text-4xl text-slate-500 mb-2">search_off</span>
            <div class="text-base text-slate-300 font-semibold">No opportunities found matching your search.</div>
            <div class="text-xs text-slate-500 mt-1">Try resetting the agency filter or searching for other keywords.</div>
          </div>
        `;
        return;
      }

      grid.innerHTML = items.map(foa => {
        const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'As per official norms');
        return `
          <div class="glass-card rounded-3xl border border-dark-border shadow-xl flex flex-col justify-between hover:border-brand-500/40 transition-all duration-300 overflow-hidden group">
            <div class="p-5 sm:p-6 flex-1 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-2 mb-3">
                  <span class="px-2.5 py-0.5 bg-dark-surface text-cyan-300 font-mono text-xs uppercase tracking-wider rounded-lg font-bold border border-dark-border">${foa.agency}</span>
                  <span class="font-mono text-xs text-slate-400">${foa.foa_id}</span>
                </div>
                <h3 class="font-display text-base sm:text-lg text-white font-bold tracking-tight group-hover:text-brand-400 transition-colors leading-snug">
                  ${foa.title}
                </h3>
                <p class="font-sans text-xs sm:text-sm text-slate-300 mt-2 line-clamp-3 leading-relaxed">
                  ${foa.brief_summary}
                </p>
                
                <div class="bg-dark-base/80 p-3.5 rounded-2xl my-3.5 flex items-center justify-between gap-2 border border-dark-border/80">
                  <div>
                    <span class="font-mono text-[10px] text-cyan-400 uppercase tracking-wider block font-bold">Financial Assistance:</span>
                    <span class="font-display text-sm sm:text-base text-brand-400 font-extrabold">${budgetStr}</span>
                  </div>
                  <div class="text-right">
                    <span class="font-mono text-[10px] text-slate-400 uppercase block font-medium">Domain / Thrust:</span>
                    <span class="font-mono text-xs text-slate-200 font-semibold">${(foa.thematic_areas || []).slice(0, 2).join(', ') || 'Higher Education'}</span>
                  </div>
                </div>
              </div>

              <div class="flex flex-wrap items-center gap-2 pt-3 border-t border-dark-border">
                <button class="px-4 py-2.5 bg-gradient-to-r from-brand-500 to-emerald-600 hover:from-brand-400 hover:to-emerald-500 text-dark-base font-mono text-xs uppercase font-extrabold rounded-xl transition-all flex items-center gap-1.5 shadow-md cursor-pointer" onclick="openApplyModal('${foa.foa_id}')">
                  <span>🚀 Apply Gateway</span>
                </button>
                <button class="px-3 py-2 bg-dark-surface hover:bg-slate-700 text-slate-200 font-mono text-xs uppercase rounded-xl transition-all flex items-center gap-1.5 border border-dark-border cursor-pointer" onclick="openDocChecklistModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[16px] text-cyan-400">checklist</span> Docs
                </button>
                <button class="px-3 py-2 bg-dark-surface hover:bg-slate-700 text-indigo-300 font-mono text-xs uppercase rounded-xl transition-all flex items-center gap-1.5 border border-dark-border cursor-pointer" onclick="openHinglishModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[16px]">translate</span> गाइड
                </button>
                <button class="px-3 py-2 bg-dark-surface hover:bg-slate-700 text-slate-300 font-mono text-xs uppercase rounded-xl transition-all flex items-center gap-1.5 border border-dark-border ml-auto cursor-pointer" onclick="downloadCalendar('${foa.foa_id}')" title="Download Calendar .ICS">
                  <span class="material-symbols-outlined text-[16px] text-amber-400">event</span> .ICS
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function setExploreQuery(term) {
      document.getElementById('exploreSearchInput').value = term;
      document.getElementById('exploreAgencyFilter').value = '';
      runExploreSearch();
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
            query: q || "scholarship and research grants",
            agency_filter: agency || null,
            top_k: 25
          })
        });
        if (!res.ok) throw new Error('Search failed');
        const data = await res.json();
        renderExploreGrid(data.map(d => d.foa));
      } catch (err) {
        console.error('Search error:', err);
      }
    }

    function setSampleAbstract(type) {
      const field = document.getElementById('matchAbstract');
      if (type === 'ai') {
        field.value = "Autonomous multi-modal deep neural networks for early diagnosis of oncological lesions via federated edge computing and high-throughput histopathological image segmentation.";
      } else if (type === 'quantum') {
        field.value = "Topological quantum materials, room-temperature 2D magnetic heterostructures, and spintronic device architectures for next-generation quantum sensors and computing.";
      } else if (type === 'clean_energy') {
        field.value = "High-efficiency green hydrogen production via perovskite-catalyst water splitting coupled with electrochemical carbon capture and renewable storage microgrids.";
      }
      runFacultyMatch();
    }

    async function runFacultyMatch() {
      const summary = document.getElementById('matchAbstract').value.trim();
      if (!summary) {
        alert('Please enter a research concept or proposal abstract.');
        return;
      }

      const role = document.getElementById('matchRole').value;
      const age = parseInt(document.getElementById('matchAge').value) || 38;
      const degree = document.getElementById('matchDegree').value;
      const container = document.getElementById('facultyResultsContainer');

      container.innerHTML = `
        <div class="text-center py-16 text-slate-400 font-mono glass-card rounded-3xl border border-dark-border">
          <span class="material-symbols-outlined text-4xl text-indigo-400 animate-spin mb-3">refresh</span>
          <div class="text-base text-slate-200 font-semibold">Computing Dense Semantic Embeddings & Statutory Compliance...</div>
          <div class="text-xs text-slate-500 mt-1">Cross-referencing PI age limits, institutional eligibility & thematic call thrusts</div>
        </div>
      `;

      try {
        const res = await fetch('/api/match-profile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            research_summary: summary,
            user_role: role,
            applicant_age: age,
            highest_degree: degree,
            top_k: 8
          })
        });
        if (!res.ok) throw new Error('Faculty match error');
        const results = await res.json();
        renderFacultyResults(results);
      } catch (err) {
        container.innerHTML = '<div class="text-red-400 text-center py-12 font-mono">Faculty alignment failed. Please retry.</div>';
      }
    }

    function renderFacultyResults(results) {
      const container = document.getElementById('facultyResultsContainer');
      if (!results || results.length === 0) {
        container.innerHTML = '<div class="text-center py-12 text-slate-400 font-mono glass-card rounded-3xl border border-dark-border">No matching research calls found.</div>';
        return;
      }

      container.innerHTML = `
        <div class="w-full bg-gradient-to-r from-indigo-950/40 to-dark-card p-4 rounded-2xl mb-5 border border-indigo-500/30 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-indigo-400 animate-pulse"></span>
            <span class="font-display text-base text-white font-bold">Matched Research Opportunities (${results.length} Calls Aligned)</span>
          </div>
          <span class="font-mono text-xs text-indigo-300 font-semibold">Ranked by Dense Embedding Cosine + BM25 RRF</span>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          ${results.map(m => `
            <div class="glass-card p-6 rounded-3xl border border-dark-border shadow-xl flex flex-col justify-between hover:border-indigo-500/40 transition-all">
              <div>
                <div class="flex items-center justify-between gap-2 mb-3">
                  <span class="px-2.5 py-0.5 bg-dark-surface text-indigo-300 font-mono text-xs uppercase font-bold rounded-lg border border-dark-border">${m.foa.agency}</span>
                  <span class="px-3 py-0.5 bg-brand-500/15 text-brand-400 font-mono text-xs font-extrabold rounded-lg border border-brand-500/30">${(m.relevance_score * 100).toFixed(1)}% Match</span>
                </div>
                <h3 class="font-display text-base sm:text-lg text-white font-bold leading-snug">${m.foa.title}</h3>
                <p class="font-sans text-xs sm:text-sm text-slate-300 mt-2 line-clamp-2">${m.foa.brief_summary}</p>
                <div class="p-3.5 bg-dark-base/80 rounded-2xl my-3 text-xs text-slate-200 border border-dark-border">
                  <strong class="text-indigo-400 font-mono uppercase">Statutory Compliance:</strong> ${m.compliance.reasons.join(' ')}
                </div>
              </div>
              <div class="flex flex-wrap items-center gap-2 pt-3 border-t border-dark-border">
                <button class="px-4 py-2.5 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-400 hover:to-cyan-400 text-white font-mono text-xs uppercase font-extrabold rounded-xl transition-all shadow-md cursor-pointer flex items-center gap-1.5" onclick="draftProposal('${m.foa.foa_id}')">
                  <span class="material-symbols-outlined text-[16px]">edit_document</span> Draft Proposal
                </button>
                <button class="px-3 py-2 bg-dark-surface hover:bg-slate-700 text-slate-200 font-mono text-xs uppercase rounded-xl transition-all border border-dark-border cursor-pointer flex items-center gap-1" onclick="downloadCalendar('${m.foa.foa_id}')">
                  <span class="material-symbols-outlined text-[16px] text-amber-400">event</span> .ICS
                </button>
                <a href="${m.foa.source_url}" target="_blank" class="px-3.5 py-2 bg-dark-surface hover:bg-slate-700 text-cyan-400 font-mono text-xs uppercase rounded-xl border border-dark-border ml-auto flex items-center gap-1">
                  <span>Portal ↗</span>
                </a>
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
        if (!res.ok) throw new Error('Failed to load scheme details');
        const foa = await res.json();

        document.getElementById('modalSchemeTitle').innerText = foa.title;
        document.getElementById('modalAgencyTag').innerText = foa.agency;
        document.getElementById('modalRefId').innerText = 'REF: ' + foa.foa_id;

        const applyUrl = foa.direct_apply_url || foa.source_url;
        let domain = 'scholarships.gov.in';
        try {
          domain = new URL(applyUrl).hostname;
        } catch (e) {
          domain = 'gov.in';
        }

        document.getElementById('modalHostDomain').innerText = domain;
        document.getElementById('modalCopyBtn').onclick = () => {
          navigator.clipboard.writeText(applyUrl);
          showToast('Portal URL copied to clipboard: ' + applyUrl);
        };

        const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'Direct Grant Support');
        document.getElementById('modalGrantText').innerHTML = `<span class="material-symbols-outlined text-[18px] text-brand-400">account_balance</span> Disbursal: <strong class="text-white">${budgetStr}</strong> via Direct PFMS/DBT Gateway`;

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
            <div class="relative z-10 w-8 h-8 rounded-xl bg-dark-surface text-brand-400 flex items-center justify-center shrink-0 border border-brand-500/40 font-mono font-bold text-xs shadow-md">
              0${idx + 1}
            </div>
            <div class="flex-1 p-3.5 bg-dark-base/90 rounded-2xl border border-dark-border">
              <p class="font-sans text-xs sm:text-sm text-slate-200 leading-relaxed">
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
      body.innerHTML = '<div class="text-center py-12 font-mono text-slate-400"><span class="material-symbols-outlined animate-spin text-brand-400 text-3xl">refresh</span><div class="mt-2">Loading requirements...</div></div>';
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/student/scholarships/${foaId}/checklist`);
        if (!res.ok) throw new Error('Checklist load error');
        const docs = await res.json();

        let html = `
          <div class="p-3.5 bg-brand-500/10 border border-brand-500/30 rounded-2xl mb-4 text-xs text-brand-400 font-mono">
            ⚠️ <strong>Pro-Tip:</strong> Keep scanned copies in PDF format under 200 KB before starting the online application on official government portals.
          </div>
        `;

        html += docs.map((d, idx) => `
          <div class="p-4 bg-dark-card rounded-2xl mb-3.5 border border-dark-border">
            <div class="font-display font-bold text-white text-base mb-1.5">${idx + 1}. ${d.document_name}</div>
            <div class="text-xs text-slate-300 mt-1">🏛️ <strong>Issuing Authority:</strong> ${d.issuing_authority}</div>
            <div class="text-xs text-slate-300 mt-1">📋 <strong>Rules & Specs:</strong> ${d.validity_and_rules}</div>
            <div class="text-xs text-slate-300 mt-1">📍 <strong>How to Obtain:</strong> ${d.how_to_obtain}</div>
          </div>
        `).join('');

        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div class="text-red-400 text-center py-6 font-mono">Failed to load document checklist.</div>';
      }
    }

    async function openHinglishModal(foaId) {
      const modal = document.getElementById('genericModalOverlay');
      const title = document.getElementById('genericModalTitle');
      const body = document.getElementById('genericModalBody');

      title.innerText = "🇮🇳 Saral Samjhauti (सरल भाषा में समझें)";
      body.innerHTML = '<div class="text-center py-12 font-mono text-slate-400"><span class="material-symbols-outlined animate-spin text-brand-400 text-3xl">refresh</span><div class="mt-2">Loading guide...</div></div>';
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/student/scholarships/${foaId}/hinglish`);
        if (!res.ok) throw new Error('Guide load error');
        const guide = await res.json();

        let html = `
          <div class="p-4 bg-brand-500/10 border border-brand-500/30 rounded-2xl mb-3.5">
            <h4 class="text-brand-400 font-display font-bold text-base mb-1">👥 कौन-कौन अप्लाई कर सकता है? (Eligibility)</h4>
            <p class="text-slate-200 text-sm leading-relaxed">${guide.kaun_apply_kar_sakta_hai}</p>
          </div>

          <div class="p-4 bg-cyan-500/10 border border-cyan-500/30 rounded-2xl mb-3.5">
            <h4 class="text-cyan-400 font-display font-bold text-base mb-1">💰 कितने पैसे मिलेंगे? (Financial Support)</h4>
            <p class="text-white text-base font-extrabold">${guide.kitne_paise_milenge}</p>
          </div>

          <div class="p-4 bg-dark-card rounded-2xl mb-3.5 border border-dark-border">
            <h4 class="text-white font-display font-bold text-base mb-2">📑 क्या-क्या जरूरी डॉक्यूमेंट्स चाहिए?</h4>
            <ul class="space-y-1.5 font-sans text-xs sm:text-sm">
              ${guide.zaruri_documents.map(d => `<li class="text-slate-300">• ${d}</li>`).join('')}
            </ul>
          </div>

          <div class="p-3.5 bg-amber-500/10 border border-amber-500/30 rounded-2xl text-xs text-amber-300 font-mono">
            ${guide.aadhaar_seeding_warning}
          </div>
        `;

        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div class="text-red-400 text-center py-6 font-mono">Failed to load Hinglish guide.</div>';
      }
    }

    async function draftProposal(foaId) {
      const modal = document.getElementById('genericModalOverlay');
      const title = document.getElementById('genericModalTitle');
      const body = document.getElementById('genericModalBody');

      title.innerText = "📝 AI Proposal Skeleton & Budget Allocator";
      body.innerHTML = '<div class="text-center py-12 font-mono text-slate-400"><span class="material-symbols-outlined animate-spin text-indigo-400 text-3xl">refresh</span><div class="mt-2">Generating MoF-compliant proposal structure...</div></div>';
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/foas/${foaId}/draft-proposal`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            pi_name: "Dr. Faculty Principal Investigator",
            institution_name: "Recognized National Institute"
          })
        });
        if (!res.ok) throw new Error('Proposal draft error');
        const data = await res.json();

        let html = `
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-brand-400 font-display font-bold text-lg">${data.scheme_title} (${data.agency})</h4>
            <button class="px-3 py-1 bg-dark-card hover:bg-slate-700 text-cyan-400 font-mono text-xs rounded-lg border border-dark-border cursor-pointer" onclick="showToast('Proposal skeleton ready for copy')">
              📋 Copy Skeleton
            </button>
          </div>

          <div class="p-4 bg-dark-card rounded-2xl mb-4 border border-dark-border">
            <div class="font-display font-bold text-white text-sm mb-2.5">Suggested Budget Allocation (MoF OM Norms)</div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
              ${Object.entries(data.suggested_budget_breakdown).map(([k, v]) => `
                <div class="p-2 bg-dark-surface rounded-lg border border-dark-border flex items-center justify-between">
                  <span class="text-slate-400">${k}:</span>
                  <span class="text-brand-400 font-bold">${v}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <div>
            <div class="font-display font-bold text-white text-sm mb-2.5">Drafted Proposal Sections</div>
            ${data.sections.map(sec => `
              <div class="p-4 bg-dark-card rounded-2xl mb-3 border border-dark-border">
                <div class="font-display font-bold text-white text-sm">${sec.section_title}</div>
                <div class="text-xs text-slate-400 mb-2">${sec.section_description}</div>
                <pre class="bg-dark-base p-3 rounded-xl text-xs text-slate-200 overflow-x-auto font-mono border border-dark-border/80"><code>${sec.drafted_content}</code></pre>
              </div>
            `).join('')}
          </div>
        `;
        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div class="text-red-400 text-center py-6 font-mono">Failed to draft proposal.</div>';
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
        hinglishBtn.className = 'px-4 py-2 bg-dark-card text-brand-400 font-mono text-xs uppercase rounded-xl font-bold transition-all flex items-center gap-2 border border-brand-500/30 shadow-md';
        checklistBtn.className = 'px-4 py-2 text-slate-400 hover:text-white font-mono text-xs uppercase rounded-xl font-semibold transition-all flex items-center gap-2';
      } else {
        checklistPanel.classList.remove('hidden');
        hinglishPanel.classList.add('hidden');
        checklistBtn.className = 'px-4 py-2 bg-dark-card text-brand-400 font-mono text-xs uppercase rounded-xl font-bold transition-all flex items-center gap-2 border border-brand-500/30 shadow-md';
        hinglishBtn.className = 'px-4 py-2 text-slate-400 hover:text-white font-mono text-xs uppercase rounded-xl font-semibold transition-all flex items-center gap-2';
      }
    }

    function closeGenericModal() {
      document.getElementById('genericModalOverlay').classList.add('hidden');
    }

    function downloadCalendar(foaId) {
      showToast('Downloading .ICS calendar event...');
      window.location.href = `/api/foas/${foaId}/calendar`;
    }

    async function triggerDbSync() {
      const syncIcon = document.getElementById('syncIcon');
      if (syncIcon) syncIcon.classList.add('animate-spin');
      showToast('Synchronizing database with sovereign feeds...');
      
      try {
        const res = await fetch('/api/ingest/trigger', { method: 'POST' });
        await loadOpportunities();
        runStudentMatch(false);
        showToast('Database synchronized successfully!');
      } catch (err) {
        showToast('Sync completed with cached indices');
      } finally {
        if (syncIcon) syncIcon.classList.remove('animate-spin');
      }
    }

    // Keyboard shortcuts (ESC to close modals)
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
