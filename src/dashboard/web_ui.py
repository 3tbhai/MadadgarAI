def render_dashboard_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Madadgaar — Sovereign &amp; CSR Scholarship Router</title>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet"/>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet"/>
    <style>
      @layer base { html, body { margin: 0; padding: 0; } body { overscroll-behavior: none; } }
      ::-webkit-scrollbar { width: 8px; height: 8px; }
      ::-webkit-scrollbar-track { background: #f5f0e8; border-left: 2px solid #1a1a1a; }
      ::-webkit-scrollbar-thumb { background: #1a1a1a; }
      .brutalist-shadow { box-shadow: 4px 4px 0px #1a1a1a; }
      .brutalist-shadow-lg { box-shadow: 6px 6px 0px #1a1a1a; }
    </style>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            "primary": "#1a1a1a",
            "primary-container": "#ffcc00",
            "on-primary": "#ffffff",
            "on-primary-container": "#1a1a1a",
            "secondary": "#e63b2e",
            "tertiary": "#0055ff",
            "background": "#f5f0e8",
            "surface": "#f5f0e8",
            "surface-container": "#eee9e0",
            "surface-container-low": "#f2ede5",
            "surface-bright": "#faf7f2",
            "on-surface": "#1a1a1a",
            "on-surface-variant": "#4a4a4a",
            "outline": "#1a1a1a",
            "outline-variant": "#d0cbc3",
            "error": "#cc0000"
          },
          fontFamily: {
            "headline": ["Space Grotesk", "sans-serif"],
            "display": ["Space Grotesk", "sans-serif"],
            "body": ["Inter", "sans-serif"],
            "mono": ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"]
          }
        }
      }
    }
    </script>
</head>
<body class="bg-background font-body text-on-surface antialiased selection:bg-primary-container selection:text-on-primary-container">

<header class="fixed top-0 w-full z-40 bg-background border-b-4 border-outline">
  <div class="h-16 max-w-7xl mx-auto px-4 lg:px-8 flex items-center justify-between">
    <div class="flex items-center gap-4 cursor-pointer" onclick="switchNavTab('vidyarthi')">
      <div class="w-10 h-10 bg-primary flex items-center justify-center border-2 border-outline brutalist-shadow">
        <span class="font-display font-extrabold text-primary-container text-2xl leading-none">M</span>
      </div>
      <div class="flex flex-col">
        <span class="font-display font-black text-xl tracking-wider uppercase leading-none">MADADGAAR</span>
        <span class="font-mono text-[10px] tracking-widest text-on-surface-variant uppercase mt-0.5">Sovereign & CSR Grid</span>
      </div>
    </div>
    
    <nav class="hidden md:flex items-center gap-2" id="mainNavTabs">
      <button class="nav-tab-btn px-4 py-2 uppercase tracking-wider transition-colors bg-primary-container text-on-primary-container border-2 border-outline brutalist-shadow font-bold text-xs" id="tabBtnVidyarthi" onclick="switchNavTab('vidyarthi')">Scholarship Finder</button>
      <button class="nav-tab-btn px-4 py-2 text-xs font-mono uppercase tracking-wider text-on-surface-variant border-2 border-transparent hover:border-outline hover:text-on-surface transition-colors font-bold" id="tabBtnExplore" onclick="switchNavTab('explore')">Explore Portals <span class="bg-primary text-white px-1.5 py-0.5 ml-1" id="statExploreBadge">0</span></button>
      <button class="nav-tab-btn px-4 py-2 text-xs font-mono uppercase tracking-wider text-on-surface-variant border-2 border-transparent hover:border-outline hover:text-on-surface transition-colors font-bold" id="tabBtnFaculty" onclick="switchNavTab('faculty')">Researcher / Faculty</button>
    </nav>
    
    <div class="flex items-center gap-4">
      <button class="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-surface-container border-2 border-outline brutalist-shadow text-xs font-mono hover:bg-primary-container transition-colors font-bold" onclick="triggerDbSync()">
        <span class="material-symbols-outlined text-[16px]">sync</span> SYNC DB
      </button>
      <div class="w-10 h-10 bg-primary flex items-center justify-center border-2 border-outline">
        <span class="material-symbols-outlined text-white text-[20px]">verified_user</span>
      </div>
    </div>
  </div>
</header>

<main class="w-full pt-20 bg-background max-w-7xl mx-auto px-4 lg:px-8 min-h-screen pb-20">

  <!-- ================= TAB 1: VIDYARTHI ================= -->
  <div id="viewVidyarthi" class="flex flex-col w-full space-y-10">
    <section class="border-b-4 border-outline pb-10">
<div class="flex flex-col lg:flex-row items-start lg:items-end justify-between gap-6 mb-8">
<div class="space-y-3 max-w-4xl">
<div class="inline-flex items-center gap-2 px-3 py-1 bg-primary text-primary-container font-mono text-xs font-bold uppercase tracking-widest border border-outline shadow-[3px_3px_0px_#1a1a1a]">
<span class="w-2.5 h-2.5 bg-secondary inline-block animate-pulse"></span>
          DIRECT BENEFIT PIPELINE // STATUS: REVENUE VERIFIED
        </div>
<h1 class="text-4xl sm:text-6xl lg:text-7xl font-display font-extrabold uppercase tracking-tighter text-on-surface leading-[0.92]">
          MADADGAAR /<br/>VIDYARTHI PORTAL <span class="bg-primary-container px-2 border-2 border-outline text-on-primary-container">v2.0</span>
</h1>
<p class="font-mono text-sm sm:text-base text-on-surface uppercase tracking-wide border-l-4 border-secondary pl-3 mt-3">
          Zero middlemen. Zero fees. 100% direct statutory disbursement via PFMS &amp; NPCI Bharat Clearinghouse.
        </p>
</div>
<div class="flex flex-col sm:flex-row items-stretch gap-3 w-full lg:w-auto">
<div class="p-3 bg-surface-container border-2 border-outline shadow-[3px_3px_0px_#1a1a1a] font-mono text-xs leading-tight">
<div class="text-on-surface-variant text-[10px] uppercase">Active Protocol</div>
<div class="font-bold text-on-surface mt-0.5">UIDAI-NPCI MAPPER v3</div>
<div class="text-secondary font-bold text-[10px] mt-1">SESSION ACTIVE #8841-IN</div>
</div>
<a class="px-5 py-3 bg-secondary text-white font-headline font-bold text-sm uppercase tracking-wider border-2 border-outline shadow-[4px_4px_0px_#1a1a1a] hover:bg-primary hover:text-white transition-all flex items-center justify-center gap-2" href="#matrix-engine">
<span>CONFIGURE FILTERS</span>
<span class="material-symbols-outlined text-base">arrow_downward</span>
</a>
</div>
</div>
<!-- Live Statutory Metrics Counter Grid -->
<div class="grid grid-cols-2 md:grid-cols-4 border-2 border-outline bg-primary gap-[2px]">
<div class="bg-surface-bright p-5 sm:p-6 flex flex-col justify-between">
<span class="font-mono text-[11px] uppercase tracking-widest text-on-surface-variant font-bold">Total Statutory Pool</span>
<div class="my-2">
<span class="text-3xl sm:text-4xl lg:text-5xl font-display font-black tracking-tight text-on-surface">₹18,450</span>
<span class="font-headline font-bold text-base text-secondary block sm:inline sm:ml-1">CRORE</span>
</div>
<span class="font-mono text-[10px] text-on-surface-variant border-t border-outline-variant pt-2 mt-1">Direct State &amp; CSR Allocations FY 24-25</span>
</div>
<div class="bg-surface-bright p-5 sm:p-6 flex flex-col justify-between">
<span class="font-mono text-[11px] uppercase tracking-widest text-on-surface-variant font-bold">Active Sanction Schemes</span>
<div class="my-2">
<span class="text-3xl sm:text-4xl lg:text-5xl font-display font-black tracking-tight text-on-surface">21</span>
<span class="font-headline font-bold text-base text-tertiary block sm:inline sm:ml-1">SCHEMES</span>
</div>
<span class="font-mono text-[10px] text-on-surface-variant border-t border-outline-variant pt-2 mt-1">Central Ministries + Section 135 CSR</span>
</div>
<div class="bg-primary-container p-5 sm:p-6 flex flex-col justify-between text-on-primary-container">
<span class="font-mono text-[11px] uppercase tracking-widest font-bold">Platform Intermediary Fee</span>
<div class="my-2">
<span class="text-3xl sm:text-4xl lg:text-5xl font-display font-black tracking-tight">₹0</span>
<span class="font-headline font-bold text-base block sm:inline sm:ml-1">/ LIFETIME FREE</span>
</div>
<span class="font-mono text-[10px] border-t border-outline pt-2 mt-1 text-on-primary-container font-semibold">Public Service Grid Directive</span>
</div>
<div class="bg-surface-bright p-5 sm:p-6 flex flex-col justify-between">
<span class="font-mono text-[11px] uppercase tracking-widest text-on-surface-variant font-bold">Eligibility Precision</span>
<div class="my-2">
<span class="text-3xl sm:text-4xl lg:text-5xl font-display font-black tracking-tight text-on-surface">98.4%</span>
</div>
<span class="font-mono text-[10px] text-on-surface-variant border-t border-outline-variant pt-2 mt-1">Deterministic Matrix Rules (Zero Guesswork)</span>
</div>
</div>
</section>

    <!-- Matrix Filter -->
<section class="py-12 border-b-4 border-outline" id="matrix-engine">
<div class="flex flex-col md:flex-row items-start md:items-baseline justify-between mb-6 pb-2 border-b-2 border-outline">
<div class="flex items-center gap-3">
<span class="w-7 h-7 bg-primary text-primary-container font-display font-black text-sm flex items-center justify-center">01</span>
<h2 class="text-2xl sm:text-3xl font-display font-extrabold uppercase tracking-tight text-on-surface">
          Modular Parameter Matrix
        </h2>
</div>
<span class="font-mono text-xs uppercase text-on-surface-variant mt-2 md:mt-0 font-semibold tracking-wider">
        [INPUT PARAMETERS TO FILTER CRITERIA STRICTLY]
      </span>
</div>
<!-- The Matrix Form Container -->
<div class="bg-surface-container border-3 border-outline shadow-[6px_6px_0px_#1a1a1a] p-6 lg:p-8">
<form class="space-y-8" id="matrix-filter-form" onsubmit="event.preventDefault(); runStudentMatch();">
<!-- Partitioned Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<!-- Field: Domicile State -->
<div class="bg-surface-bright p-4 border-2 border-outline flex flex-col justify-between">
<label class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block mb-2" for="domicile">
              01 // Domicile State
            </label>
<div class="relative">
<select class="w-full bg-surface-container-low font-headline font-bold text-sm px-3 py-2.5 border-b-2 border-outline focus:outline-none focus:bg-primary-container rounded-none text-on-surface" id="stuState" onchange="runStudentMatch()">
<option value="All India">All-India Universal (All States)</option>
<option value="Rajasthan">Rajasthan</option>
<option selected="" value="Maharashtra">Maharashtra</option>
<option value="Uttar Pradesh">Uttar Pradesh</option>
<option value="Karnataka">Karnataka</option>
<option value="Delhi NCR">Delhi NCR</option>
<option value="West Bengal">West Bengal</option>
<option value="Bihar">Bihar</option>
</select>
</div>
<span class="text-[10px] font-mono text-on-surface-variant mt-2">Determines State Minority &amp; Merit quotas</span>
</div>
<!-- Field: Academic Level -->
<div class="bg-surface-bright p-4 border-2 border-outline flex flex-col justify-between">
<label class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block mb-2" for="academic-level">
              02 // Academic Level
            </label>
<div class="relative">
<select class="w-full bg-surface-container-low font-headline font-bold text-sm px-3 py-2.5 border-b-2 border-outline focus:outline-none focus:bg-primary-container rounded-none text-on-surface" id="stuLevel" onchange="runStudentMatch()">
<option selected="" value="UG - Engineering / Technology (B.Tech/B.E.)">B.Tech / B.E. (Technical Degree)</option>
<option value="UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)">MBBS / BDS / Professional Medical</option>
<option value="Diploma / Polytechnic">Polytechnic Diploma</option>
<option value="UG - General (B.Sc / B.Com / B.A. / BBA / BCA)">B.Sc / B.Com / B.A (General UG)</option>
<option value="Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)">Postgraduate (M.A / M.Sc / M.Com)</option>
<option value="Class 11-12 (Higher Secondary)">Higher Secondary (Class 11-12)</option>
</select>
</div>
<span class="text-[10px] font-mono text-on-surface-variant mt-2">AICTE / UGC / NMC sanction tiers</span>
</div>
<!-- Field: Category -->
<div class="bg-surface-bright p-4 border-2 border-outline flex flex-col justify-between">
<label class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block mb-2" for="caste-category">
              03 // Social Category
            </label>
<div class="relative">
<select class="w-full bg-surface-container-low font-headline font-bold text-sm px-3 py-2.5 border-b-2 border-outline focus:outline-none focus:bg-primary-container rounded-none text-on-surface" id="stuCategory" onchange="runStudentMatch()">
<option value="General / Open">General / Open Merit</option>
<option selected="" value="EWS (Economically Weaker Section)">EWS (Economically Weaker Section)</option>
<option value="OBC (Non-Creamy Layer)">OBC (Non-Creamy Layer)</option>
<option value="SC (Scheduled Caste)">Scheduled Caste (SC)</option>
<option value="ST (Scheduled Tribe)">Scheduled Tribe (ST)</option>
</select>
</div>
<span class="text-[10px] font-mono text-on-surface-variant mt-2">Verified via State Central Caste Registry</span>
</div>
<!-- Field: Gender -->
<div class="bg-surface-bright p-4 border-2 border-outline flex flex-col justify-between">
<label class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block mb-2">
              04 // Gender
            </label>
<div class="grid grid-cols-3 gap-1 pt-1">
<label class="cursor-pointer border-2 border-outline text-center py-2 text-xs font-headline font-bold uppercase select-none transition-colors has-[:checked]:bg-primary has-[:checked]:text-primary-container">
<input checked="" class="sr-only" name="gender" onchange="runStudentMatch()" type="radio" value="Female"/>
                Female
              </label>
<label class="cursor-pointer border-2 border-outline text-center py-2 text-xs font-headline font-bold uppercase select-none transition-colors has-[:checked]:bg-primary has-[:checked]:text-primary-container">
<input class="sr-only" name="gender" onchange="runStudentMatch()" type="radio" value="Male"/>
                Male
              </label>
<label class="cursor-pointer border-2 border-outline text-center py-2 text-xs font-headline font-bold uppercase select-none transition-colors has-[:checked]:bg-primary has-[:checked]:text-primary-container">
<input class="sr-only" name="gender" onchange="runStudentMatch()" type="radio" value="Transgender"/>
                Other
              </label>
</div>
<span class="text-[10px] font-mono text-on-surface-variant mt-2">Special targeted CSR drives for women</span>
</div>
</div>
<!-- Second Row: Income Bracket + Score + Toggles -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
<!-- Income Slider & Presets (6 Cols) -->
<div class="lg:col-span-6 bg-surface-bright p-5 border-2 border-outline flex flex-col justify-between">
<div class="flex items-center justify-between mb-3">
<label class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface" for="income-slider">
                05 // Annual Gross Family Income Bracket
              </label>
<span class="font-display font-extrabold text-lg bg-primary text-primary-container px-2 border border-outline" id="incomeDisplay">
                ≤ ₹ 3,20,000 / yr
              </span>
</div>
<input class="w-full h-3 bg-surface-container accent-primary border-2 border-outline rounded-none cursor-pointer" id="stuIncome" max="800000" min="80000" oninput="updateIncomeDisplay(this.value); runStudentMatch()" step="20000" type="range" value="320000"/>
<!-- Preset Blocks -->
<div class="grid grid-cols-4 gap-2 mt-4 font-mono text-[11px] font-bold">
<button class="py-1.5 px-1 bg-surface-container border border-outline hover:bg-primary-container text-center transition-colors" onclick="setIncomeVal(150000)" type="button">
                &lt; ₹1.5L
              </button>
<button class="py-1.5 px-1 bg-surface-container border border-outline hover:bg-primary-container text-center transition-colors" onclick="setIncomeVal(250000)" type="button">
                ₹2.5L
              </button>
<button class="py-1.5 px-1 bg-surface-container border border-outline hover:bg-primary-container text-center transition-colors" onclick="setIncomeVal(450000)" type="button">
                ₹4.5L (EWS)
              </button>
<button class="py-1.5 px-1 bg-surface-container border border-outline hover:bg-primary-container text-center transition-colors" onclick="setIncomeVal(800000)" type="button">
                ₹8.0L (CSR Max)
              </button>
</div>
</div>
<!-- Academic Score Input (3 Cols) -->
<div class="lg:col-span-3 bg-surface-bright p-5 border-2 border-outline flex flex-col justify-between">
<label class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block mb-2" for="academic-score">
              06 // Prior Exam Score %
            </label>
<div class="flex items-center gap-3">
<input class="w-24 bg-surface-container text-3xl font-display font-extrabold p-2 border-2 border-outline text-center text-on-surface focus:outline-none focus:bg-primary-container" id="stuMarks" onchange="runStudentMatch()" max="100" min="35" type="number" value="86"/>
<div class="font-mono text-xs text-on-surface-variant leading-tight">
<span class="font-bold text-on-surface text-sm block">86.00% Aggregate</span>
                Class 12 / Diploma Final CGPA equivalent
              </div>
</div>
<div class="w-full bg-surface-container-highest border border-outline h-2 mt-4 overflow-hidden">
<div class="bg-tertiary h-full w-[86%]"></div>
</div>
</div>
<!-- Statutory Status Toggles (3 Cols) -->
<div class="lg:col-span-3 bg-surface-bright p-5 border-2 border-outline flex flex-col justify-center space-y-4">
<span class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block">
              07 // Statutory Criteria Flags
            </span>
<label class="flex items-center gap-3 cursor-pointer group">
<input checked="" class="w-5 h-5 border-2 border-outline accent-primary rounded-none" id="stuSingleGirl" onchange="runStudentMatch()" type="checkbox"/>
<div class="text-xs font-headline font-bold uppercase leading-tight group-hover:text-tertiary">
                Single Girl Child
                <span class="font-mono block text-[10px] text-on-surface-variant font-normal">(एकल कन्या योजना Quota)</span>
</div>
</label>
<label class="flex items-center gap-3 cursor-pointer group">
<input class="w-5 h-5 border-2 border-outline accent-primary rounded-none" id="stuPwd" onchange="runStudentMatch()" type="checkbox"/>
<div class="text-xs font-headline font-bold uppercase leading-tight group-hover:text-tertiary">
                Differently Abled
                <span class="font-mono block text-[10px] text-on-surface-variant font-normal">(PwD UDID ≥ 40% Certified)</span>
</div>
</label>
</div>
</div>
<!-- Action Row -->
<div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t-2 border-outline">
<div class="font-mono text-xs text-on-surface flex items-center gap-2">
<span class="w-3 h-3 bg-primary inline-block"></span>
            Matrix Rule Engine matches across 4 Central Ministries &amp; 12 CSR Funds directly.
          </div>
<button class="w-full sm:w-auto px-8 py-4 bg-primary-container text-on-primary-container font-headline font-black text-base uppercase tracking-wider border-2 border-outline shadow-[5px_5px_0px_#1a1a1a] hover:bg-primary hover:text-white transition-all flex items-center justify-center gap-3" type="submit">
<span>EXECUTE ELIGIBILITY CHECK</span>
<span class="material-symbols-outlined font-black">arrow_forward</span>
</button>
</div>
</form>
</div>
</section>

    <!-- Results Section -->
    <section>
      <div class="flex items-center gap-3 mb-6">
        <span class="w-8 h-8 bg-primary text-primary-container font-display font-black flex items-center justify-center border-2 border-outline">02</span>
        <h2 class="text-3xl font-display font-black uppercase tracking-tight">Scheme Directory</h2>
      </div>
      <div id="studentResultsContainer" class="space-y-6">
        <!-- JS Render -->
      </div>
    </section>
  </div>

  <!-- ================= TAB 2: EXPLORE ================= -->
  <div id="viewExplore" class="hidden flex-col w-full space-y-8 mt-6">
    <div class="flex items-center gap-3 mb-2">
      <h2 class="text-4xl font-display font-black uppercase tracking-tight">Portal Explorer</h2>
    </div>
    
    <div class="bg-surface-container border-4 border-outline brutalist-shadow-lg p-6">
      <div class="flex flex-col md:flex-row gap-4">
        <input type="text" id="exploreSearchInput" class="flex-1 bg-surface-bright text-on-surface font-headline font-bold px-4 py-3 border-4 border-outline rounded-none focus:bg-primary-container placeholder-on-surface-variant" placeholder="SEARCH BY KEYWORD..." onkeyup="if(event.key === 'Enter') runExploreSearch()"/>
        <select id="exploreAgencyFilter" class="bg-surface-bright text-on-surface font-headline font-bold px-4 py-3 border-4 border-outline rounded-none focus:bg-primary-container" onchange="runExploreSearch()">
            <option value="">ALL AGENCIES</option>
            <option value="NSP">NSP</option>
            <option value="AICTE">AICTE</option>
            <option value="UGC">UGC</option>
            <option value="State Govt">STATE GOVT</option>
            <option value="CSR / Foundation">CSR</option>
            <option value="DST">DST</option>
            <option value="ANRF/SERB">ANRF/SERB</option>
            <option value="CSIR">CSIR</option>
            <option value="DBT">DBT</option>
        </select>
        <button class="px-8 py-3 bg-primary text-white font-headline font-black border-4 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors flex items-center gap-2" onclick="runExploreSearch()">
          SEARCH <span class="material-symbols-outlined">search</span>
        </button>
      </div>
    </div>
    
    <div id="exploreGrid" class="space-y-6"></div>
  </div>

  <!-- ================= TAB 3: FACULTY ================= -->
  <div id="viewFaculty" class="hidden flex-col w-full space-y-8 mt-6">
    <div class="flex items-center gap-3 mb-2">
      <h2 class="text-4xl font-display font-black uppercase tracking-tight">Research Grant Alignment</h2>
    </div>
    
    <div class="bg-surface-container border-4 border-outline brutalist-shadow-lg p-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-surface-bright p-4 border-2 border-outline flex flex-col">
          <label class="font-mono text-xs font-bold uppercase mb-2">Role</label>
          <select id="matchRole" class="w-full bg-surface-container-low font-headline font-bold px-3 py-2.5 border-b-2 border-outline rounded-none focus:bg-primary-container">
            <option>Faculty / PI</option>
            <option>Early Career Researcher</option>
            <option>Women Scientists</option>
            <option>PhD / Postdocs</option>
          </select>
        </div>
        <div class="bg-surface-bright p-4 border-2 border-outline flex flex-col">
          <label class="font-mono text-xs font-bold uppercase mb-2">Age</label>
          <input type="number" id="matchAge" value="38" class="w-full bg-surface-container-low font-headline font-bold px-3 py-2 border-b-2 border-outline rounded-none focus:bg-primary-container"/>
        </div>
        <div class="bg-surface-bright p-4 border-2 border-outline flex flex-col">
          <label class="font-mono text-xs font-bold uppercase mb-2">Degree</label>
          <input type="text" id="matchDegree" value="Ph.D. CS" class="w-full bg-surface-container-low font-headline font-bold px-3 py-2 border-b-2 border-outline rounded-none focus:bg-primary-container"/>
        </div>
      </div>
      
      <div class="bg-surface-bright p-4 border-2 border-outline flex flex-col mb-6">
        <label class="font-mono text-xs font-bold uppercase mb-2">Abstract / Objective</label>
        <textarea id="matchAbstract" rows="4" class="w-full bg-surface-container-low font-body font-medium p-3 border-2 border-outline rounded-none focus:bg-primary-container" placeholder="Describe objectives..."></textarea>
      </div>
      
      <button class="px-8 py-4 bg-primary text-white font-headline font-black text-base uppercase border-4 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors flex items-center gap-2" onclick="runFacultyMatch()">
        ALIGN PROPOSAL <span class="material-symbols-outlined">model_training</span>
      </button>
    </div>
    
    <div id="facultyResultsContainer" class="grid grid-cols-1 lg:grid-cols-2 gap-6"></div>
  </div>

</main>

<!-- ================= MODALS ================= -->

<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-primary/80 backdrop-blur-sm hidden" id="applyModalOverlay" onclick="if(event.target === this) closeApplyModal()">
  <div class="w-full max-w-3xl bg-surface border-4 border-outline brutalist-shadow-lg flex flex-col max-h-[90vh]">
    <div class="p-6 bg-surface-bright border-b-4 border-outline flex justify-between items-start">
      <div>
        <span class="px-2 py-1 bg-primary text-white font-mono text-[10px] font-bold uppercase border-2 border-outline" id="modalAgencyTag">AGENCY</span>
        <h2 class="text-2xl font-display font-black uppercase mt-3" id="modalSchemeTitle">TITLE</h2>
      </div>
      <button class="border-2 border-outline w-10 h-10 flex items-center justify-center hover:bg-secondary hover:text-white transition-colors bg-surface" onclick="closeApplyModal()">
        <span class="material-symbols-outlined font-black">close</span>
      </button>
    </div>
    
    <div class="p-4 bg-secondary text-white font-mono text-xs font-bold uppercase border-b-4 border-outline flex items-center gap-2">
      <span class="material-symbols-outlined">warning</span> ZERO FEE GUARANTEE. DO NOT PAY AGENTS.
    </div>
    
    <div class="p-6 overflow-y-auto font-body space-y-4 flex-1">
      <div id="modalGrantText" class="font-headline font-bold text-lg"></div>
      <div class="font-mono text-sm font-bold uppercase border-b-2 border-outline pb-2 mt-4">STEPS TO APPLY</div>
      <div id="modalStepsTimeline" class="space-y-3 font-medium text-sm"></div>
    </div>
    
    <div class="p-6 border-t-4 border-outline bg-surface-container flex flex-wrap gap-4 justify-between">
      <a id="modalWhatsappLink" class="px-6 py-3 bg-[#138808] text-white font-headline font-bold uppercase border-2 border-outline brutalist-shadow flex items-center gap-2" href="#" target="_blank">
        <span class="material-symbols-outlined">share</span> WhatsApp
      </a>
      <a id="modalApplyLink" class="px-6 py-3 bg-primary text-white font-headline font-bold uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors flex items-center gap-2" href="#" target="_blank">
        PORTAL <span class="material-symbols-outlined">open_in_new</span>
      </a>
    </div>
  </div>
</div>

<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-primary/80 backdrop-blur-sm hidden" id="genericModalOverlay" onclick="if(event.target === this) closeGenericModal()">
  <div class="w-full max-w-2xl bg-surface border-4 border-outline brutalist-shadow-lg flex flex-col max-h-[90vh]">
    <div class="p-5 bg-surface-bright border-b-4 border-outline flex justify-between items-center">
      <h2 class="text-xl font-display font-black uppercase" id="genericModalTitle">INFO</h2>
      <button class="border-2 border-outline w-8 h-8 flex items-center justify-center hover:bg-secondary hover:text-white transition-colors bg-surface" onclick="closeGenericModal()">
        <span class="material-symbols-outlined font-black">close</span>
      </button>
    </div>
    <div class="p-6 overflow-y-auto font-body flex-1" id="genericModalBody"></div>
  </div>
</div>

<!-- ================= SCRIPTS ================= -->
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
      document.getElementById('statTotalCounter').innerHTML = `${allOpportunities.length} <span class="text-tertiary text-lg">LIVE</span>`;
      document.getElementById('statExploreBadge').innerText = `${allOpportunities.length}`;
    } catch (err) {
      console.error(err);
    }
  }

  function switchNavTab(tab) {
    document.getElementById('viewVidyarthi').classList.toggle('hidden', tab !== 'vidyarthi');
    document.getElementById('viewExplore').classList.toggle('hidden', tab !== 'explore');
    document.getElementById('viewFaculty').classList.toggle('hidden', tab !== 'faculty');

    document.querySelectorAll('.nav-tab-btn').forEach(b => {
      b.className = 'nav-tab-btn px-4 py-2 text-xs font-mono uppercase tracking-wider text-on-surface-variant border-2 border-transparent hover:border-outline hover:text-on-surface transition-colors font-bold';
    });

    const activeClass = 'nav-tab-btn px-4 py-2 uppercase tracking-wider transition-colors bg-primary-container text-on-primary-container border-2 border-outline brutalist-shadow font-bold text-xs';
    
    if (tab === 'vidyarthi') document.getElementById('tabBtnVidyarthi').className = activeClass;
    if (tab === 'explore') document.getElementById('tabBtnExplore').className = activeClass;
    if (tab === 'faculty') document.getElementById('tabBtnFaculty').className = activeClass;
  }

  function updateIncomeDisplay(val) {
    document.getElementById('incomeDisplay').innerText = '≤ ₹ ' + Number(val).toLocaleString('en-IN') + ' / yr';
  }
  function setIncomeVal(val) {
    document.getElementById('stuIncome').value = val;
    updateIncomeDisplay(val);
    runStudentMatch();
  }

  async function runStudentMatch() {
    const container = document.getElementById('studentResultsContainer');
    const btnText = document.getElementById('matchBtnText');
    if(btnText) btnText.innerHTML = 'EXECUTING...';

    const payload = {
      state_domicile: document.getElementById('stuState').value,
      education_level: document.getElementById('stuLevel').value,
      social_category: document.getElementById('stuCategory').value,
      gender: document.querySelector('input[name="gender"]:checked').value,
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
      container.innerHTML = '<div class="text-error font-bold">Failed to load.</div>';
    } finally {
      if(btnText) btnText.innerHTML = 'EXECUTE CHECK';
    }
  }

  function renderStudentCards(results) {
    const container = document.getElementById('studentResultsContainer');
    if(!results || results.length===0){
      container.innerHTML = '<div class="font-mono font-bold">NO MATCHES FOUND.</div>'; return;
    }
    container.innerHTML = results.map(res => {
      const foa = res.foa;
      const isEl = res.eligibility_status === 'ELIGIBLE';
      const badge = isEl ? '100% MATCH' : res.eligibility_status;
      const bg = isEl ? 'bg-primary text-primary-container' : 'bg-surface-container text-on-surface';
      
      const agencyText = foa.agency || 'AGENCY';
      
      // Extract clean amount for large display
      let rawBenefit = res.estimated_financial_benefit || 'GRANT';
      let bigAmount = 'GRANT';
      let smallText = rawBenefit;
      
      const amtMatch = rawBenefit.match(/(?:Rs\.?|INR|₹)\s*([\d,]+)/i);
      if (amtMatch) {
          bigAmount = '₹' + amtMatch[1];
          smallText = rawBenefit.replace(amtMatch[0], '').trim();
          smallText = smallText.replace(/^[^\w\s]+/, '').trim();
      } else if (foa.financials && foa.financials.max_amount_inr) {
          bigAmount = '₹' + foa.financials.max_amount_inr.toLocaleString('en-IN');
      }

      if (smallText.length > 50) {
          smallText = smallText.substring(0, 47) + '...';
      }

      // Dynamic Right Side Rendering
      let btnColor = 'bg-primary text-white hover:bg-primary-container hover:text-on-primary-container';
      let btnText = 'APPLY DIRECT PORTAL';
      let btnIcon = 'open_in_new';
      
      if (agencyText.includes('AICTE') || agencyText.includes('NSP')) {
          btnColor = 'bg-tertiary text-white hover:bg-primary hover:text-white';
          btnText = 'GO TO NSP PORTAL';
      } else if (agencyText.includes('UGC')) {
          btnColor = 'bg-surface-container text-on-surface hover:bg-primary hover:text-white';
          btnText = 'DETAILS & GUIDELINES';
          btnIcon = 'description';
      }
      
      let minQual = foa.eligibility && foa.eligibility.min_qualification ? foa.eligibility.min_qualification : 'Check Portal';
      let beneficiary = foa.eligibility && foa.eligibility.target_beneficiaries && foa.eligibility.target_beneficiaries.length > 0 ? foa.eligibility.target_beneficiaries[0] : 'All';
      let deadline = foa.deadlines && foa.deadlines.raw_deadline_text ? foa.deadlines.raw_deadline_text : 'See Portal';

      return `
        <article class="scheme-card bg-surface-bright border-3 border-outline shadow-[5px_5px_0px_#1a1a1a] p-6 lg:p-7 relative transition-transform hover:-translate-y-0.5 mb-6">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div class="space-y-3 max-w-3xl">
              <div class="flex flex-wrap items-center gap-2">
                <span class="px-2.5 py-0.5 ${bg} font-mono text-[11px] font-bold uppercase border border-outline">
                  ${badge} (${res.match_percentage}%)
                </span>
                <span class="px-2.5 py-0.5 bg-surface-container-highest text-on-surface font-mono text-[11px] font-bold uppercase border border-outline">
                  ${agencyText}
                </span>
                <span class="px-2.5 py-0.5 bg-surface-container text-on-surface font-mono text-[11px] font-bold uppercase border border-outline flex items-center gap-1">
                  <span class="material-symbols-outlined text-[13px] text-secondary">verified</span>
                  Direct NPCI Credit
                </span>
              </div>
              <h3 class="text-xl sm:text-2xl font-display font-extrabold uppercase text-on-surface leading-tight">
                ${foa.title}
              </h3>
              <p class="font-body text-xs sm:text-sm text-on-surface-variant leading-relaxed">
                ${foa.brief_summary}
              </p>

              <!-- Integration of the existing Docs and Guide buttons -->
              <div class="flex flex-wrap gap-2 pt-2 pb-2">
                <button class="px-3.5 py-1.5 bg-surface-container border-2 border-outline font-headline font-bold text-xs uppercase hover:bg-primary-container transition-colors shadow-[2px_2px_0px_#1a1a1a]" onclick="openDocChecklistModal('${foa.foa_id}')">Docs Checklist</button>
                <button class="px-3.5 py-1.5 bg-surface-container border-2 border-outline font-headline font-bold text-xs uppercase hover:bg-primary-container transition-colors shadow-[2px_2px_0px_#1a1a1a]" onclick="openHinglishModal('${foa.foa_id}')">Saral Guide (Hinglish)</button>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 font-mono text-xs mt-2">
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block">Min. 12th Marks</span>
                  <span class="font-bold text-on-surface">${minQual.substring(0,25)}</span>
                </div>
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block">Family Income Cap</span>
                  <span class="font-bold text-on-surface">≤ ₹6,00,000 / yr</span>
                </div>
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block">Target Cohort</span>
                  <span class="font-bold text-on-surface">${beneficiary.substring(0,25)}</span>
                </div>
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-secondary uppercase block font-bold">Window Closes</span>
                  <span class="font-bold text-secondary">${deadline.substring(0,25)}</span>
                </div>
              </div>
            </div>
            
            <!-- Benefit Value & Direct Action -->
            <div class="lg:w-64 flex flex-col items-start lg:items-end justify-between border-t-2 lg:border-t-0 lg:border-l-2 border-outline pt-4 lg:pt-0 lg:pl-6 space-y-4 shrink-0">
              <div class="text-left lg:text-right w-full">
                <span class="font-mono text-[10px] uppercase tracking-widest text-on-surface-variant block">Disbursement Amount</span>
                <div class="text-3xl lg:text-4xl font-display font-black text-on-surface">${bigAmount}</div>
                <span class="font-mono text-[10px] text-on-surface-variant uppercase font-semibold block mt-1">Estimated Grant Value</span>
              </div>
              <button class="w-full py-3 px-4 ${btnColor} font-headline font-bold text-xs uppercase tracking-wider text-center border-2 border-outline shadow-[3px_3px_0px_#1a1a1a] transition-all flex items-center justify-center gap-2" onclick="openApplyModal('${foa.foa_id}')">
                <span>${btnText}</span>
                <span class="material-symbols-outlined text-sm">${btnIcon}</span>
              </button>
            </div>
          </div>
        </article>
      `;
    }).join('');
  }

  function renderExploreGrid(items) {
    const grid = document.getElementById('exploreGrid');
    if(!items || items.length===0){
      grid.innerHTML = '<div class="font-mono font-bold">NO RESULTS.</div>'; return;
    }
    grid.innerHTML = items.map(foa => {
      const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'GRANT');
      return `
        <article class="bg-surface-bright border-4 border-outline brutalist-shadow p-6 flex flex-col justify-between h-full">
          <div>
            <div class="flex justify-between items-start mb-3">
              <span class="px-2 py-0.5 bg-surface-container font-mono text-[11px] font-bold uppercase border-2 border-outline">${foa.agency}</span>
            </div>
            <h3 class="text-xl font-display font-black uppercase leading-tight mb-2">${foa.title}</h3>
            <p class="font-body text-sm font-medium line-clamp-3 mb-4">${foa.brief_summary}</p>
          </div>
          <div class="flex items-center justify-between border-t-4 border-outline pt-4">
            <div class="font-display font-black text-xl">${budgetStr}</div>
            <button class="px-4 py-2 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors" onclick="openApplyModal('${foa.foa_id}')">PORTAL</button>
          </div>
        </article>
      `;
    }).join('');
  }

  async function runExploreSearch() {
    const q = document.getElementById('exploreSearchInput').value.trim();
    const agency = document.getElementById('exploreAgencyFilter').value;
    if(!q && !agency) { renderExploreGrid(allOpportunities); return; }
    try {
      const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q || "scholarship", agency_filter: agency || null, top_k: 20 })
      });
      const data = await res.json();
      renderExploreGrid(data.map(d => d.foa));
    } catch (e) {}
  }

  async function runFacultyMatch() {
    const summary = document.getElementById('matchAbstract').value.trim();
    if(!summary) { alert('ENTER ABSTRACT'); return; }
    
    const role = document.getElementById('matchRole').value;
    const age = parseInt(document.getElementById('matchAge').value) || 38;
    const degree = document.getElementById('matchDegree').value;
    const container = document.getElementById('facultyResultsContainer');
    container.innerHTML = '<div class="font-mono font-bold">MATCHING...</div>';

    try {
      const res = await fetch('/api/match-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ research_summary: summary, user_role: role, applicant_age: age, highest_degree: degree, top_k: 6 })
      });
      const results = await res.json();
      
      if(!results || results.length===0){ container.innerHTML = '<div class="font-mono font-bold">NO MATCHES.</div>'; return; }
      
      container.innerHTML = results.map(m => `
        <article class="bg-surface-bright border-4 border-outline brutalist-shadow p-6 flex flex-col justify-between">
          <div>
            <div class="flex justify-between items-center mb-2">
              <span class="px-2 py-0.5 bg-surface-container font-mono text-[11px] font-bold uppercase border-2 border-outline">${m.foa.agency}</span>
              <span class="px-2 py-0.5 bg-primary text-white font-mono text-[11px] font-bold uppercase border-2 border-outline">${(m.relevance_score*100).toFixed(0)}% MATCH</span>
            </div>
            <h3 class="text-xl font-display font-black uppercase mb-2">${m.foa.title}</h3>
            <p class="font-body text-sm font-medium mb-3">${m.foa.brief_summary}</p>
            <div class="p-3 bg-surface-container border-2 border-outline font-mono text-xs mb-4">
              <strong>COMPLIANCE:</strong> ${m.compliance.reasons.join(' ')}
            </div>
          </div>
          <div class="flex gap-2 border-t-4 border-outline pt-4">
            <button class="flex-1 py-2 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors" onclick="draftProposal('${m.foa.foa_id}')">DRAFT PROPOSAL</button>
            <a href="${m.foa.source_url}" target="_blank" class="px-4 py-2 bg-surface-container font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container transition-colors">PORTAL</a>
          </div>
        </article>
      `).join('');
    } catch(e) { container.innerHTML = '<div class="text-error font-bold">ERROR.</div>'; }
  }

  async function openApplyModal(foaId) {
    document.getElementById('applyModalOverlay').classList.remove('hidden');
    try {
      const res = await fetch(`/api/foas/${foaId}`);
      const foa = await res.json();
      document.getElementById('modalSchemeTitle').innerText = foa.title;
      document.getElementById('modalAgencyTag').innerText = foa.agency;
      const applyUrl = foa.direct_apply_url || foa.source_url;
      const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'DIRECT GRANT');
      document.getElementById('modalGrantText').innerText = 'BENEFIT: ' + budgetStr;
      document.getElementById('modalApplyLink').href = applyUrl;
      const steps = foa.portal_navigation_steps && foa.portal_navigation_steps.length > 0 ? foa.portal_navigation_steps : ["1. Visit Portal", "2. Register with Aadhaar", "3. Submit forms"];
      document.getElementById('modalStepsTimeline').innerHTML = steps.map(s => `<div class="p-3 border-2 border-outline bg-surface-bright">${s}</div>`).join('');
    } catch(e) {}
  }
  function closeApplyModal() { document.getElementById('applyModalOverlay').classList.add('hidden'); }

  async function openDocChecklistModal(foaId) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = "DOCUMENT CHECKLIST";
    const body = document.getElementById('genericModalBody');
    body.innerHTML = '<div class="font-mono font-bold">LOADING...</div>';
    modal.classList.remove('hidden');
    try {
      const res = await fetch(`/api/student/scholarships/${foaId}/checklist`);
      const docs = await res.json();
      body.innerHTML = docs.map((d,i) => `
        <div class="mb-4 p-4 border-4 border-outline bg-surface-bright brutalist-shadow">
          <div class="font-display font-black text-lg mb-2">${i+1}. ${d.document_name}</div>
          <div class="font-mono text-sm">AUTHORITY: ${d.issuing_authority}</div>
          <div class="font-mono text-sm">RULES: ${d.validity_and_rules}</div>
        </div>
      `).join('');
    } catch(e) { body.innerHTML = 'ERROR'; }
  }

  async function openHinglishModal(foaId) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = "SARAL GUIDE";
    const body = document.getElementById('genericModalBody');
    body.innerHTML = '<div class="font-mono font-bold">LOADING...</div>';
    modal.classList.remove('hidden');
    try {
      const res = await fetch(`/api/student/scholarships/${foaId}/hinglish`);
      const g = await res.json();
      body.innerHTML = `
        <div class="space-y-4">
          <div class="p-4 border-4 border-outline bg-surface-bright brutalist-shadow">
            <h4 class="font-display font-black text-lg mb-2">ELIGIBILITY (पात्रता)</h4>
            <p class="font-body font-medium">${g.kaun_apply_kar_sakta_hai}</p>
          </div>
          <div class="p-4 border-4 border-outline bg-surface-bright brutalist-shadow">
            <h4 class="font-display font-black text-lg mb-2">BENEFITS (फायदे)</h4>
            <p class="font-body font-medium">${g.kitne_paise_milenge}</p>
          </div>
          <div class="p-4 border-4 border-outline bg-secondary text-white brutalist-shadow">
            <h4 class="font-display font-black text-lg mb-2">WARNING</h4>
            <p class="font-body font-medium">${g.aadhaar_seeding_warning}</p>
          </div>
        </div>
      `;
    } catch(e) { body.innerHTML = 'ERROR'; }
  }

  async function draftProposal(foaId) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = "PROPOSAL DRAFT";
    const body = document.getElementById('genericModalBody');
    body.innerHTML = '<div class="font-mono font-bold">DRAFTING...</div>';
    modal.classList.remove('hidden');
    try {
      const res = await fetch(`/api/foas/${foaId}/draft-proposal`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ pi_name:"Dr. Researcher", institution_name:"Institute" })
      });
      const data = await res.json();
      body.innerHTML = `
        <h3 class="font-display font-black text-xl mb-4">${data.scheme_title}</h3>
        ${data.sections.map(s => `
          <div class="mb-4 border-4 border-outline bg-surface-bright brutalist-shadow p-4">
            <div class="font-display font-black text-lg mb-2">${s.section_title}</div>
            <pre class="whitespace-pre-wrap font-mono text-xs">${s.drafted_content}</pre>
          </div>
        `).join('')}
      `;
    } catch(e) { body.innerHTML = 'ERROR'; }
  }

  function openInfoModal(title, text) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = title;
    const body = document.getElementById('genericModalBody');
    body.innerHTML = `<div class="p-6 font-body font-medium text-base sm:text-lg border-4 border-outline bg-surface-bright brutalist-shadow">${text}</div>`;
    modal.classList.remove('hidden');
  }
  function closeGenericModal() { document.getElementById('genericModalOverlay').classList.add('hidden'); }
  async function triggerDbSync() { await fetch('/api/ingest/trigger', {method:'POST'}); await loadOpportunities(); runStudentMatch(); alert('SYNC COMPLETE'); }
  document.addEventListener('keydown', (e) => { if(e.key==='Escape') { closeApplyModal(); closeGenericModal(); } });
  
  initPlatform();
</script>
</body>
</html>
"""
