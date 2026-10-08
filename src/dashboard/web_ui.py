def render_dashboard_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Madadgaar AI — Sovereign &amp; CSR Scholarship Router</title>
    <link href="https://fonts.googleapis.com" rel="preconnect"/>
    <link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&family=Noto+Sans+Devanagari:wght@600;700;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet"/>
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
            "mono": ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
            "devanagari": ["Noto Sans Devanagari", "sans-serif"]
          }
        }
      }
    }
    </script>
</head>
<body class="bg-background font-body text-on-surface antialiased selection:bg-primary-container selection:text-on-primary-container">

<header class="fixed top-0 w-full z-40 bg-background border-b-4 border-outline">
  <div class="h-16 max-w-7xl mx-auto px-4 lg:px-8 flex items-center justify-between">
    <div class="flex items-center gap-3 cursor-pointer" onclick="switchNavTab('vidyarthi')">
      <div class="w-10 h-10 bg-primary flex items-center justify-center border-2 border-outline brutalist-shadow">
        <span class="font-display font-extrabold text-primary-container text-2xl leading-none">M</span>
      </div>
      <div class="flex flex-col">
        <span class="font-display font-black text-lg sm:text-xl tracking-wider uppercase leading-none">MADADGAAR AI</span>
        <span class="font-devanagari font-bold text-xs tracking-wide text-secondary mt-1 leading-none">मददगार एआई</span>
      </div>
    </div>
    
    <nav class="hidden md:flex items-center gap-2" id="mainNavTabs">
      <button class="nav-tab-btn px-4 py-2 uppercase tracking-wider transition-colors bg-primary-container text-on-primary-container border-2 border-outline brutalist-shadow font-bold text-xs" id="tabBtnVidyarthi" onclick="switchNavTab('vidyarthi')">Scholarship Finder</button>
      <button class="nav-tab-btn px-4 py-2 text-xs font-mono uppercase tracking-wider text-on-surface-variant border-2 border-transparent hover:border-outline hover:text-on-surface transition-colors font-bold" id="tabBtnExplore" onclick="switchNavTab('explore')">Explore Portals <span class="bg-primary text-white px-1.5 py-0.5 ml-1" id="statExploreBadge">0</span></button>
      <button class="nav-tab-btn px-4 py-2 text-xs font-mono uppercase tracking-wider text-on-surface-variant border-2 border-transparent hover:border-outline hover:text-on-surface transition-colors font-bold" id="tabBtnFaculty" onclick="switchNavTab('faculty')">Researcher / Faculty</button>
    </nav>
    
    <div class="flex items-center gap-2 sm:gap-4">
      <button id="syncDbBtn" class="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-surface-container border-2 border-outline brutalist-shadow text-xs font-mono hover:bg-primary-container transition-colors font-bold" onclick="triggerDbSync()">
        <span class="material-symbols-outlined text-[16px]">sync</span> SYNC DB
      </button>
      <div class="w-9 h-9 sm:w-10 sm:h-10 bg-primary flex items-center justify-center border-2 border-outline">
        <span class="material-symbols-outlined text-white text-[18px] sm:text-[20px]">verified_user</span>
      </div>
    </div>
  </div>

  <!-- Mobile Sub-Nav Bar for Easy Touch Switching -->
  <div class="flex md:hidden w-full border-t-2 border-outline bg-surface-container-low px-2 py-1.5 gap-1.5 justify-around items-center">
    <button class="mobile-nav-btn flex-1 py-1 px-2 text-center font-headline font-bold text-[11px] uppercase border border-outline bg-primary-container text-on-primary-container brutalist-shadow" id="mobTabVidyarthi" onclick="switchNavTab('vidyarthi')">Vidyarthi</button>
    <button class="mobile-nav-btn flex-1 py-1 px-2 text-center font-headline font-bold text-[11px] uppercase border border-outline bg-surface-bright text-on-surface" id="mobTabExplore" onclick="switchNavTab('explore')">Explore</button>
    <button class="mobile-nav-btn flex-1 py-1 px-2 text-center font-headline font-bold text-[11px] uppercase border border-outline bg-surface-bright text-on-surface" id="mobTabFaculty" onclick="switchNavTab('faculty')">Faculty</button>
  </div>
</header>

<main class="w-full pt-28 md:pt-20 bg-background max-w-7xl mx-auto px-4 lg:px-8 min-h-screen pb-20">

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
          MADADGAAR AI /<br/>VIDYARTHI PORTAL <span class="bg-primary-container px-2 border-2 border-outline text-on-primary-container">v2.0</span>
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
<span class="text-3xl sm:text-4xl lg:text-5xl font-display font-black tracking-tight text-on-surface" id="statTotalCounter">21 <span class="text-tertiary text-lg">SCHEMES</span></span>
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
<form class="space-y-8" id="matrix-filter-form" onsubmit="event.preventDefault(); runStudentMatch(true);">
<!-- Partitioned Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<!-- Field: Domicile State -->
<div class="bg-surface-bright p-4 border-2 border-outline flex flex-col justify-between">
<label class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block mb-2" for="domicile">
              01 // Domicile State
            </label>
<div class="relative">
<select class="w-full bg-surface-container-low font-headline font-bold text-sm px-3 py-2.5 border-b-2 border-outline focus:outline-none focus:bg-primary-container rounded-none text-on-surface" id="stuState">
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
<select class="w-full bg-surface-container-low font-headline font-bold text-xs sm:text-sm px-2.5 py-2.5 border-b-2 border-outline focus:outline-none focus:bg-primary-container rounded-none text-on-surface truncate" id="stuLevel">
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
<select class="w-full bg-surface-container-low font-headline font-bold text-xs sm:text-sm px-2.5 py-2.5 border-b-2 border-outline focus:outline-none focus:bg-primary-container rounded-none text-on-surface truncate" id="stuCategory">
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
<input checked="" class="sr-only" name="gender" type="radio" value="Female"/>
                Female
              </label>
<label class="cursor-pointer border-2 border-outline text-center py-2 text-xs font-headline font-bold uppercase select-none transition-colors has-[:checked]:bg-primary has-[:checked]:text-primary-container">
<input class="sr-only" name="gender" type="radio" value="Male"/>
                Male
              </label>
<label class="cursor-pointer border-2 border-outline text-center py-2 text-xs font-headline font-bold uppercase select-none transition-colors has-[:checked]:bg-primary has-[:checked]:text-primary-container">
<input class="sr-only" name="gender" type="radio" value="Transgender"/>
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
<input class="w-full h-3 bg-surface-container accent-primary border-2 border-outline rounded-none cursor-pointer" id="stuIncome" max="800000" min="80000" oninput="updateIncomeDisplay(this.value)" step="20000" type="range" value="320000"/>
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
<input class="w-24 bg-surface-container text-3xl font-display font-extrabold p-2 border-2 border-outline text-center text-on-surface focus:outline-none focus:bg-primary-container" id="stuMarks" max="100" min="35" type="number" value="86" oninput="updateMarksDisplay(this.value)"/>
<div class="font-mono text-xs text-on-surface-variant leading-tight">
<span class="font-bold text-on-surface text-sm block" id="marksDisplayLabel">86.00% Aggregate</span>
                Class 12 / Diploma Final CGPA equivalent
              </div>
</div>
<div class="w-full bg-surface-container-highest border border-outline h-2 mt-4 overflow-hidden">
<div class="bg-tertiary h-full transition-all duration-300" id="marksProgressBar" style="width: 86%;"></div>
</div>
</div>
<!-- Statutory Status Toggles (3 Cols) -->
<div class="lg:col-span-3 bg-surface-bright p-5 border-2 border-outline flex flex-col justify-center space-y-4">
<span class="font-mono text-xs font-bold uppercase tracking-wider text-on-surface block">
              07 // Statutory Criteria Flags
            </span>
<label class="flex items-center gap-3 cursor-pointer group">
<input checked="" class="w-5 h-5 border-2 border-outline accent-primary rounded-none" id="stuSingleGirl" type="checkbox"/>
<div class="text-xs font-headline font-bold uppercase leading-tight group-hover:text-tertiary">
                Single Girl Child
                <span class="font-mono block text-[10px] text-on-surface-variant font-normal">(एकल कन्या योजना Quota)</span>
</div>
</label>
<label class="flex items-center gap-3 cursor-pointer group">
<input class="w-5 h-5 border-2 border-outline accent-primary rounded-none" id="stuPwd" type="checkbox"/>
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
<span id="matchBtnText">EXECUTE ELIGIBILITY CHECK</span>
<span class="material-symbols-outlined font-black">arrow_forward</span>
</button>
</div>
</form>
</div>
</section>

    <!-- Results Section -->
    <section id="scheme-directory" class="pt-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div class="flex items-center gap-3">
          <span class="w-8 h-8 bg-primary text-primary-container font-display font-black flex items-center justify-center border-2 border-outline">02</span>
          <h2 class="text-3xl font-display font-black uppercase tracking-tight">Scheme Directory</h2>
        </div>
        <div id="resultsMatchBadge" class="font-mono text-xs font-bold uppercase bg-primary-container text-on-primary-container px-3 py-1.5 border-2 border-outline brutalist-shadow">
          READY FOR EVALUATION
        </div>
      </div>
      <div id="studentResultsContainer" class="space-y-6">
        <!-- JS Render -->
      </div>
    </section>
  </div>

  <!-- ================= TAB 2: EXPLORE ================= -->
  <div id="viewExplore" class="hidden flex-col w-full space-y-8 mt-6">
    <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6 border-b-4 border-outline pb-6">
      <div class="space-y-2 max-w-3xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-primary text-primary-container font-mono text-xs font-bold uppercase tracking-widest border border-outline shadow-[3px_3px_0px_#1a1a1a]">
          <span class="w-2.5 h-2.5 bg-tertiary inline-block"></span>
          CENTRAL &amp; CSR OPPORTUNITY REGISTRY // 100% STATUTORY VERIFIED
        </div>
        <h2 class="text-4xl sm:text-5xl font-display font-black uppercase tracking-tight text-on-surface">
          Explore Portal Directory
        </h2>
        <p class="font-mono text-xs sm:text-sm text-on-surface-variant uppercase tracking-wide">
          Direct indexed catalog of Central Ministries, State Welfare Boards, and Section 135 Corporate CSR Foundations. 100% Free Public Access.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <div class="p-3 bg-surface-container border-2 border-outline shadow-[3px_3px_0px_#1a1a1a] font-mono text-xs">
          <div class="text-[10px] text-on-surface-variant uppercase">Catalog Status</div>
          <div class="font-bold text-on-surface text-sm" id="exploreLiveCountBadge">21 Active Schemes</div>
        </div>
      </div>
    </div>
    
    <!-- Search & Filter Console -->
    <div class="bg-surface-bright border-4 border-outline brutalist-shadow-lg p-6 space-y-4">
      <div class="flex flex-col md:flex-row gap-3">
        <div class="relative flex-1">
          <span class="material-symbols-outlined absolute left-3 top-3.5 text-on-surface-variant">search</span>
          <input type="text" id="exploreSearchInput" class="w-full bg-surface-container-low text-on-surface font-headline font-bold pl-11 pr-10 py-3 border-2 border-outline rounded-none focus:bg-primary-container placeholder-on-surface-variant text-sm" placeholder="SEARCH BY SCHEME NAME, KEYWORD, OR TARGET ELIGIBILITY..." oninput="handleExploreSearchInput()" onkeyup="if(event.key === 'Enter') runExploreSearch()"/>
          <button id="clearSearchBtn" class="hidden absolute right-3 top-3 text-on-surface-variant hover:text-on-surface" onclick="clearExploreSearch()">
            <span class="material-symbols-outlined text-sm">close</span>
          </button>
        </div>
        
        <select id="exploreSortFilter" class="bg-surface-container-low text-on-surface font-headline font-bold px-4 py-3 border-2 border-outline rounded-none focus:bg-primary-container text-xs uppercase" onchange="runExploreSearch()">
          <option value="default">SORT: DEFAULT INDEX</option>
          <option value="amount_desc">AMOUNT: HIGH TO LOW</option>
          <option value="title_asc">TITLE: A TO Z</option>
        </select>

        <button class="px-6 py-3 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors flex items-center justify-center gap-2" onclick="runExploreSearch()">
          <span>FILTER</span>
          <span class="material-symbols-outlined text-sm">tune</span>
        </button>
      </div>

      <!-- Quick Category Chips -->
      <div class="flex flex-wrap items-center gap-2 pt-2 border-t-2 border-outline-variant font-mono text-xs">
        <span class="font-bold text-[10px] uppercase tracking-wider text-on-surface-variant mr-1">Filter By Category:</span>
        <button class="explore-chip-btn px-3 py-1 bg-primary text-primary-container border-2 border-outline font-bold uppercase transition-colors" data-filter="" onclick="setExploreAgencyFilter('')">ALL SCHEMES</button>
        <button class="explore-chip-btn px-3 py-1 bg-surface-container text-on-surface border-2 border-outline hover:bg-primary-container font-bold uppercase transition-colors" data-filter="NSP" onclick="setExploreAgencyFilter('NSP')">NSP CENTRAL</button>
        <button class="explore-chip-btn px-3 py-1 bg-surface-container text-on-surface border-2 border-outline hover:bg-primary-container font-bold uppercase transition-colors" data-filter="AICTE" onclick="setExploreAgencyFilter('AICTE')">AICTE TECH</button>
        <button class="explore-chip-btn px-3 py-1 bg-surface-container text-on-surface border-2 border-outline hover:bg-primary-container font-bold uppercase transition-colors" data-filter="State Govt" onclick="setExploreAgencyFilter('State Govt')">STATE GOVT</button>
        <button class="explore-chip-btn px-3 py-1 bg-surface-container text-on-surface border-2 border-outline hover:bg-primary-container font-bold uppercase transition-colors" data-filter="CSR / Foundation" onclick="setExploreAgencyFilter('CSR / Foundation')">CORPORATE CSR</button>
        <button class="explore-chip-btn px-3 py-1 bg-surface-container text-on-surface border-2 border-outline hover:bg-primary-container font-bold uppercase transition-colors" data-filter="UGC" onclick="setExploreAgencyFilter('UGC')">UGC HIGHER ED</button>
      </div>
    </div>

    <!-- Active Search Filter Summary -->
    <div class="flex items-center justify-between font-mono text-xs px-1">
      <div class="text-on-surface-variant">
        SHOWING <span id="exploreResultsCount" class="font-bold text-on-surface">21</span> VERIFIED OPPORTUNITIES
      </div>
      <button onclick="resetExploreFilters()" class="text-secondary hover:underline font-bold uppercase flex items-center gap-1">
        <span class="material-symbols-outlined text-[14px]">refresh</span> Reset Filters
      </button>
    </div>
    
    <!-- Explore Grid -->
    <div id="exploreGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
  </div>

  <!-- ================= TAB 3: FACULTY ================= -->
  <div id="viewFaculty" class="hidden flex-col w-full space-y-8 mt-6">
    <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6 border-b-4 border-outline pb-6">
      <div class="space-y-2 max-w-3xl">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-primary text-primary-container font-mono text-xs font-bold uppercase tracking-widest border border-outline shadow-[3px_3px_0px_#1a1a1a]">
          <span class="w-2.5 h-2.5 bg-secondary inline-block"></span>
          RESEARCH &amp; FACULTY R&amp;D PORTAL // ANRF • SERB • DST • CSIR • ICMR
        </div>
        <h2 class="text-4xl sm:text-5xl font-display font-black uppercase tracking-tight text-on-surface">
          Research Grant Alignment Engine
        </h2>
        <p class="font-mono text-xs sm:text-sm text-on-surface-variant uppercase tracking-wide">
          Semantic vector alignment matching project proposals, research abstracts, and faculty profiles against active national &amp; international grant circulars.
        </p>
      </div>

      <div class="flex items-center gap-3">
        <div class="p-3 bg-surface-container border-2 border-outline shadow-[3px_3px_0px_#1a1a1a] font-mono text-xs">
          <div class="text-[10px] text-on-surface-variant uppercase">Alignment Model</div>
          <div class="font-bold text-on-surface text-sm">all-MiniLM-L6-v2 (384-d)</div>
        </div>
      </div>
    </div>
    
    <!-- Parameter & Abstract Console -->
    <div class="bg-surface-bright border-4 border-outline brutalist-shadow-lg p-6 space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-surface-container-low p-4 border-2 border-outline flex flex-col justify-between">
          <label class="font-mono text-xs font-bold uppercase mb-2 text-on-surface">01 // Applicant Role</label>
          <select id="matchRole" class="w-full bg-surface-bright font-headline font-bold text-xs sm:text-sm px-3 py-2 border-2 border-outline rounded-none focus:bg-primary-container">
            <option value="Faculty / Principal Investigator">Faculty / Principal Investigator</option>
            <option value="Early Career Researcher">Early Career Researcher</option>
            <option value="Women Scientists">Women Scientists (WOS-A / WOS-B)</option>
            <option value="PhD Scholars &amp; Postdoctoral Fellows">PhD Scholars &amp; Postdoctoral Fellows</option>
            <option value="UG / PG Students">UG / PG Student Researchers</option>
          </select>
        </div>
        <div class="bg-surface-container-low p-4 border-2 border-outline flex flex-col justify-between">
          <label class="font-mono text-xs font-bold uppercase mb-2 text-on-surface">02 // Age (Years)</label>
          <input type="number" id="matchAge" value="38" class="w-full bg-surface-bright font-display font-black text-xl px-3 py-1.5 border-2 border-outline rounded-none focus:bg-primary-container text-center"/>
        </div>
        <div class="bg-surface-container-low p-4 border-2 border-outline flex flex-col justify-between">
          <label class="font-mono text-xs font-bold uppercase mb-2 text-on-surface">03 // Highest Qualification</label>
          <input type="text" id="matchDegree" value="Ph.D. Computer Science" class="w-full bg-surface-bright font-headline font-bold text-xs sm:text-sm px-3 py-2 border-2 border-outline rounded-none focus:bg-primary-container"/>
        </div>
        <div class="bg-surface-container-low p-4 border-2 border-outline flex flex-col justify-between">
          <label class="font-mono text-xs font-bold uppercase mb-2 text-on-surface">04 // Institution Tier</label>
          <select id="matchInstTier" class="w-full bg-surface-bright font-headline font-bold text-xs sm:text-sm px-3 py-2 border-2 border-outline rounded-none focus:bg-primary-container">
            <option value="CFTI / IIT / IISc / NIT">CFTI / IIT / IISc / NIT</option>
            <option value="Central / State University">Central / State University</option>
            <option value="AICTE Approved Institute">AICTE Approved Institute</option>
            <option value="National Research Lab">National Lab (CSIR/ICMR)</option>
          </select>
        </div>
      </div>
      
      <!-- Abstract Input with Sample Presets -->
      <div class="bg-surface-container-low p-5 border-2 border-outline flex flex-col space-y-3">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <label class="font-mono text-xs font-bold uppercase text-on-surface" for="matchAbstract">
            05 // Project Proposal Abstract / Technical Objectives
          </label>
          <div class="flex flex-wrap items-center gap-1.5 font-mono text-[11px]">
            <span class="text-on-surface-variant uppercase font-bold text-[10px] mr-1">Demo Quick Loads:</span>
            <button type="button" onclick="loadSampleAbstract(1)" class="px-2 py-0.5 bg-surface-bright border border-outline hover:bg-primary-container transition-colors font-bold uppercase">Sample 1: AI Healthcare</button>
            <button type="button" onclick="loadSampleAbstract(2)" class="px-2 py-0.5 bg-surface-bright border border-outline hover:bg-primary-container transition-colors font-bold uppercase">Sample 2: Quantum</button>
            <button type="button" onclick="loadSampleAbstract(3)" class="px-2 py-0.5 bg-surface-bright border border-outline hover:bg-primary-container transition-colors font-bold uppercase">Sample 3: Solar Energy</button>
          </div>
        </div>
        <textarea id="matchAbstract" rows="4" class="w-full bg-surface-bright font-body font-medium p-3 border-2 border-outline rounded-none focus:bg-primary-container placeholder-on-surface-variant text-sm leading-relaxed" placeholder="Paste your proposed research abstract, methodology, technical scope, or key objectives here to semantically match against active statutory calls..."></textarea>
      </div>
      
      <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
        <button class="px-8 py-3.5 bg-primary text-white font-headline font-bold text-sm uppercase border-4 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors flex items-center justify-center gap-2" onclick="runFacultyMatch()">
          <span id="facultyBtnText">ALIGN PROPOSAL WITH NATIONAL CALLS</span>
          <span class="material-symbols-outlined text-base">model_training</span>
        </button>
        <div class="font-mono text-xs text-on-surface-variant" id="facultyStatusInfo">
          Evaluates against ANRF, DST, DBT, CSIR, and ICMR statutory guidelines.
        </div>
      </div>
    </div>
    
    <!-- Faculty Matched Results Header -->
    <div class="flex items-center justify-between font-mono text-xs border-b-2 border-outline pb-2">
      <span class="font-bold uppercase tracking-wider text-on-surface">SEMANTICALLY ALIGNED GRANT OPPORTUNITIES</span>
      <span id="facultyMatchCountBadge" class="bg-primary text-primary-container px-2 py-0.5 font-bold">READY TO ALIGN</span>
    </div>

    <!-- Results Grid -->
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
    const initHash = window.location.hash.replace('#', '');
    if (['vidyarthi', 'explore', 'faculty'].includes(initHash)) {
      switchNavTab(initHash);
    }
    const urlParams = new URLSearchParams(window.location.search);
    const modalType = urlParams.get('modal');
    const modalId = urlParams.get('id');
    if (modalType && modalId) {
      setTimeout(() => {
        if (modalType === 'hinglish') openHinglishModal(modalId);
        else if (modalType === 'checklist') openDocChecklistModal(modalId);
        else if (modalType === 'proposal') draftProposal(modalId);
        else if (modalType === 'apply') openApplyModal(modalId);
      }, 350);
    }
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
    if (window.location.hash !== '#' + tab) {
      window.location.hash = tab;
    }
    document.getElementById('viewVidyarthi').classList.toggle('hidden', tab !== 'vidyarthi');
    document.getElementById('viewExplore').classList.toggle('hidden', tab !== 'explore');
    document.getElementById('viewFaculty').classList.toggle('hidden', tab !== 'faculty');

    document.querySelectorAll('.nav-tab-btn').forEach(b => {
      b.className = 'nav-tab-btn px-4 py-2 text-xs font-mono uppercase tracking-wider text-on-surface-variant border-2 border-transparent hover:border-outline hover:text-on-surface transition-colors font-bold';
    });

    const activeClass = 'nav-tab-btn px-4 py-2 uppercase tracking-wider transition-colors bg-primary-container text-on-primary-container border-2 border-outline brutalist-shadow font-bold text-xs';
    
    if (tab === 'vidyarthi') document.getElementById('tabBtnVidyarthi').className = activeClass;
    if (tab === 'explore') document.getElementById('tabBtnExplore').className = activeClass;
    if (tab === 'faculty') {
      document.getElementById('tabBtnFaculty').className = activeClass;
      const absEl = document.getElementById('matchAbstract');
      if (absEl && !absEl.value.trim()) {
        setTimeout(() => loadSampleAbstract(1), 100);
      }
    }

    document.querySelectorAll('.mobile-nav-btn').forEach(b => {
      b.className = 'mobile-nav-btn flex-1 py-1 px-2 text-center font-headline font-bold text-[11px] uppercase border border-outline bg-surface-bright text-on-surface';
    });
    const mobActive = 'mobile-nav-btn flex-1 py-1 px-2 text-center font-headline font-bold text-[11px] uppercase border border-outline bg-primary-container text-on-primary-container brutalist-shadow';
    if (tab === 'vidyarthi') {
      const mb = document.getElementById('mobTabVidyarthi');
      if (mb) mb.className = mobActive;
    } else if (tab === 'explore') {
      const mb = document.getElementById('mobTabExplore');
      if (mb) mb.className = mobActive;
    } else if (tab === 'faculty') {
      const mb = document.getElementById('mobTabFaculty');
      if (mb) mb.className = mobActive;
    }
  }

  window.addEventListener('hashchange', () => {
    const h = window.location.hash.replace('#', '');
    if (['vidyarthi', 'explore', 'faculty'].includes(h)) switchNavTab(h);
  });

  function updateMarksDisplay(val) {
    const num = parseFloat(val) || 0;
    const clamped = Math.min(100, Math.max(0, num));
    const lbl = document.getElementById('marksDisplayLabel');
    if (lbl) lbl.innerText = clamped.toFixed(2) + '% Aggregate';
    const bar = document.getElementById('marksProgressBar');
    if (bar) bar.style.width = clamped + '%';
  }

  function updateIncomeDisplay(val) {
    document.getElementById('incomeDisplay').innerText = '≤ ₹ ' + Number(val).toLocaleString('en-IN') + ' / yr';
  }
  function setIncomeVal(val) {
    document.getElementById('stuIncome').value = val;
    updateIncomeDisplay(val);
  }

  async function runStudentMatch(shouldScroll = false) {
    const container = document.getElementById('studentResultsContainer');
    const btnText = document.getElementById('matchBtnText');
    const badge = document.getElementById('resultsMatchBadge');
    if(btnText) btnText.innerHTML = 'CALCULATING ELIGIBILITY...';
    if(badge) badge.innerText = 'EVALUATING SCHEMES...';

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

      const eligibleCount = results.filter(r => r.eligibility_status === 'ELIGIBLE' || r.eligibility_status === 'HIGH_PROBABILITY').length;
      if(badge) {
        badge.innerHTML = `MATCHED: ${eligibleCount} ELIGIBLE (${results.length} TOTAL)`;
      }

      if(shouldScroll) {
        const sec = document.getElementById('scheme-directory');
        if(sec) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    } catch (err) {
      container.innerHTML = '<div class="text-error font-bold">Failed to load.</div>';
    } finally {
      if(btnText) btnText.innerHTML = 'EXECUTE ELIGIBILITY CHECK';
    }
  }

  function formatMinQual(raw) {
    if (!raw) return '12th Pass / Equivalent';
    const low = raw.toLowerCase();
    if (low.includes('85%') || low.includes('85.0%')) return '≥ 85.0% Aggregate';
    if (low.includes('60%')) return '≥ 60.0% Aggregate';
    if (low.includes('55%')) return '≥ 55.0% Aggregate';
    if (low.includes('50%')) return '≥ 50.0% Aggregate';
    if (low.includes('12th') || low.includes('higher secondary')) return '12th Standard Pass';
    if (low.includes('diploma')) return 'Diploma / Polytech';
    if (low.includes('b.tech') || low.includes('engineering') || low.includes('degree')) return 'UG Technical Degree';
    if (low.includes('ph.d') || low.includes('phd')) return 'Doctoral / Ph.D.';
    if (low.includes('postgraduate') || low.includes('master')) return 'Postgraduate (PG)';
    if (raw.length > 22) return raw.substring(0, 20) + '...';
    return raw;
  }

  function formatIncomeCap(foa) {
    const text = ((foa.brief_summary || '') + ' ' + (foa.eligibility && foa.eligibility.raw_eligibility_text ? foa.eligibility.raw_eligibility_text : '')).toLowerCase();
    if (text.includes('2.5') || text.includes('2,50,000')) return '≤ ₹2,50,000 / yr';
    if (text.includes('2.0') || text.includes('2,00,000')) return '≤ ₹2,00,000 / yr';
    if (text.includes('4.5') || text.includes('4,50,000')) return '≤ ₹4,50,000 / yr';
    if (text.includes('6.0') || text.includes('6 lakh') || text.includes('6,00,000')) return '≤ ₹6,00,000 / yr';
    if (text.includes('8.0') || text.includes('8 lakh') || text.includes('8,00,000')) return '≤ ₹8,00,000 / yr';
    if (text.includes('15 lakh') || text.includes('15,00,000')) return '≤ ₹15,00,000 / yr';
    return 'Check Portal Cap';
  }

  function formatBeneficiary(b) {
    if (!b) return 'All Regular Students';
    if (b.includes('UG / PG Students')) return 'UG & PG Students';
    if (b.includes('Women Scientists')) return 'Girl / Female Students';
    if (b.includes('Early Career')) return 'Early Career / Freshers';
    if (b.length > 22) return b.substring(0, 20) + '...';
    return b;
  }

  function formatDeadline(d) {
    if (!d) return 'Annual Cycle';
    if (d.toLowerCase().includes('rolling')) return 'Rolling Cycle';
    if (d.length > 20) {
      const m = d.match(/(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s+\d{4})/);
      if (m) return m[1];
      return d.substring(0, 18) + '...';
    }
    return d;
  }

  function renderStudentCards(results) {
    const container = document.getElementById('studentResultsContainer');
    if(!results || results.length===0){
      container.innerHTML = '<div class="p-8 border-4 border-outline bg-surface-bright font-mono font-bold text-center">NO MATCHES FOUND FOR THESE CRITERIA.</div>'; return;
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

      if (smallText.length > 45) {
          smallText = smallText.substring(0, 42) + '...';
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
      
      const cleanMinQual = formatMinQual(foa.eligibility && foa.eligibility.min_qualification ? foa.eligibility.min_qualification : '');
      const cleanIncome = formatIncomeCap(foa);
      const cleanBeneficiary = formatBeneficiary(foa.eligibility && foa.eligibility.target_beneficiaries && foa.eligibility.target_beneficiaries.length > 0 ? foa.eligibility.target_beneficiaries[0] : '');
      const cleanDeadline = formatDeadline(foa.deadlines && foa.deadlines.raw_deadline_text ? foa.deadlines.raw_deadline_text : '');

      return `
        <article class="scheme-card bg-surface-bright border-3 border-outline shadow-[5px_5px_0px_#1a1a1a] p-6 lg:p-7 relative transition-transform hover:-translate-y-0.5 mb-6">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div class="space-y-3 max-w-3xl flex-1">
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

              <!-- Integration of Docs, Guide and Calendar buttons -->
              <div class="flex flex-wrap gap-2 pt-1 pb-1">
                <button class="px-3.5 py-1.5 bg-surface-container border-2 border-outline font-headline font-bold text-xs uppercase hover:bg-primary-container transition-colors shadow-[2px_2px_0px_#1a1a1a] flex items-center gap-1" onclick="openDocChecklistModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[14px]">checklist</span> Docs Checklist
                </button>
                <button class="px-3.5 py-1.5 bg-surface-container border-2 border-outline font-headline font-bold text-xs uppercase hover:bg-primary-container transition-colors shadow-[2px_2px_0px_#1a1a1a] flex items-center gap-1" onclick="openHinglishModal('${foa.foa_id}')">
                  <span class="material-symbols-outlined text-[14px]">translate</span> Saral Guide (Hinglish)
                </button>
                <a href="/api/foas/${foa.foa_id}/calendar" download class="px-3.5 py-1.5 bg-surface-container border-2 border-outline font-headline font-bold text-xs uppercase hover:bg-primary-container transition-colors shadow-[2px_2px_0px_#1a1a1a] flex items-center gap-1 inline-flex" title="Sync application deadline with Google or Apple Calendar">
                  <span class="material-symbols-outlined text-[14px]">calendar_month</span> Add to Calendar (.ics)
                </a>
              </div>

              <!-- Eligibility Criteria Sub-Grid: guaranteed zero overflow -->
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 font-mono text-xs mt-1 border-t border-outline/30">
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block">Min. Academic</span>
                  <span class="font-bold text-on-surface truncate block" title="${cleanMinQual}">${cleanMinQual}</span>
                </div>
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block">Income Ceiling</span>
                  <span class="font-bold text-on-surface truncate block" title="${cleanIncome}">${cleanIncome}</span>
                </div>
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block">Target Cohort</span>
                  <span class="font-bold text-on-surface truncate block" title="${cleanBeneficiary}">${cleanBeneficiary}</span>
                </div>
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-secondary uppercase block font-bold">Window Closes</span>
                  <span class="font-bold text-secondary truncate block" title="${cleanDeadline}">${cleanDeadline}</span>
                </div>
              </div>

              <!-- Rule Gate Verdict Strip -->
              ${res.match_reasons && res.match_reasons.length > 0 ? `
              <div class="pt-2 flex flex-wrap gap-1.5 items-center">
                <span class="font-mono text-[10px] font-bold uppercase text-on-surface-variant mr-1">Passed Rules:</span>
                ${res.match_reasons.slice(0, 3).map(r => `<span class="px-2 py-0.5 bg-surface-container-high border border-outline font-mono text-[10px] text-on-surface font-semibold flex items-center gap-1">${r.replace(/^[✅❌⚠️⭐]\s*/, '')}</span>`).join('')}
                ${res.match_reasons.length > 3 ? `<span class="font-mono text-[10px] text-on-surface-variant font-bold">+${res.match_reasons.length - 3} more</span>` : ''}
              </div>
              ` : ''}
            </div>
            
            <!-- Benefit Value & Direct Action -->
            <div class="lg:w-64 flex flex-col items-start lg:items-end justify-between border-t-2 lg:border-t-0 lg:border-l-2 border-outline pt-4 lg:pt-0 lg:pl-6 space-y-4 shrink-0">
              <div class="text-left lg:text-right w-full">
                <span class="font-mono text-[10px] uppercase tracking-widest text-on-surface-variant block">Disbursement Amount</span>
                <div class="text-3xl lg:text-4xl font-display font-black text-on-surface leading-tight">${bigAmount}</div>
                <span class="font-mono text-[10px] text-on-surface-variant uppercase font-semibold block mt-1">${smallText || 'Estimated Grant Value'}</span>
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

  let currentExploreAgency = '';
  let exploreSearchDebounceTimer = null;

  function handleExploreSearchInput() {
    const val = document.getElementById('exploreSearchInput').value.trim();
    const clearBtn = document.getElementById('clearSearchBtn');
    if (clearBtn) clearBtn.classList.toggle('hidden', val.length === 0);
    clearTimeout(exploreSearchDebounceTimer);
    exploreSearchDebounceTimer = setTimeout(() => {
      runExploreSearch();
    }, 200);
  }

  function clearExploreSearch() {
    const inp = document.getElementById('exploreSearchInput');
    if (inp) inp.value = '';
    const clearBtn = document.getElementById('clearSearchBtn');
    if (clearBtn) clearBtn.classList.add('hidden');
    runExploreSearch();
  }

  function setExploreAgencyFilter(agency) {
    currentExploreAgency = agency;
    document.querySelectorAll('.explore-chip-btn').forEach(btn => {
      const f = btn.getAttribute('data-filter');
      if (f === agency) {
        btn.className = 'explore-chip-btn px-3 py-1 bg-primary text-primary-container border-2 border-outline font-bold uppercase transition-colors';
      } else {
        btn.className = 'explore-chip-btn px-3 py-1 bg-surface-container text-on-surface border-2 border-outline hover:bg-primary-container font-bold uppercase transition-colors';
      }
    });
    runExploreSearch();
  }

  function resetExploreFilters() {
    const inp = document.getElementById('exploreSearchInput');
    if (inp) inp.value = '';
    const clearBtn = document.getElementById('clearSearchBtn');
    if (clearBtn) clearBtn.classList.add('hidden');
    const sort = document.getElementById('exploreSortFilter');
    if (sort) sort.value = 'default';
    setExploreAgencyFilter('');
  }

  function renderExploreGrid(items) {
    const grid = document.getElementById('exploreGrid');
    const countBadge = document.getElementById('exploreResultsCount');
    if (countBadge) countBadge.innerText = items ? items.length : 0;
    
    if(!items || items.length===0){
      grid.innerHTML = `
        <div class="col-span-full p-12 bg-surface-bright border-4 border-outline brutalist-shadow-lg text-center space-y-4">
          <span class="material-symbols-outlined text-5xl text-secondary">search_off</span>
          <h3 class="font-display font-black text-2xl uppercase">NO MATCHING SCHEMES FOUND</h3>
          <p class="font-mono text-xs text-on-surface-variant max-w-md mx-auto">Try clearing search terms or switching agency filters to view available sovereign and CSR opportunities.</p>
          <button onclick="resetExploreFilters()" class="px-5 py-2.5 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors">
            Reset Filters
          </button>
        </div>
      `;
      return;
    }

    grid.innerHTML = items.map(foa => {
      const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'DIRECT GRANT');
      let displayAmount = 'GRANT';
      const amtMatch = budgetStr.match(/(?:Rs\.?|INR|₹)\s*([\d,]+)/i);
      if (amtMatch) {
          displayAmount = '₹' + amtMatch[1];
      } else if (foa.financials && foa.financials.max_amount_inr) {
          displayAmount = '₹' + foa.financials.max_amount_inr.toLocaleString('en-IN');
      }

      const agency = foa.agency || 'GOVT';
      let tagBg = 'bg-surface-container';
      if (agency.includes('NSP')) tagBg = 'bg-tertiary text-white';
      else if (agency.includes('CSR') || agency.includes('Foundation')) tagBg = 'bg-primary-container text-on-primary-container';
      else if (agency.includes('AICTE')) tagBg = 'bg-secondary text-white';

      const minQual = foa.eligibility && foa.eligibility.min_qualification ? foa.eligibility.min_qualification : '10th / 12th Pass';
      const beneficiary = foa.eligibility && foa.eligibility.target_beneficiaries && foa.eligibility.target_beneficiaries.length > 0 ? foa.eligibility.target_beneficiaries[0] : 'All Students';
      const deadline = foa.deadlines && foa.deadlines.raw_deadline_text ? foa.deadlines.raw_deadline_text : 'Active FY 24-25';

      return `
        <article class="bg-surface-bright border-4 border-outline brutalist-shadow p-5 flex flex-col justify-between h-full transition-transform hover:-translate-y-1">
          <div class="space-y-3">
            <div class="flex items-center justify-between gap-2 border-b-2 border-outline-variant pb-2">
              <span class="px-2.5 py-0.5 ${tagBg} font-mono text-[10px] font-bold uppercase border border-outline">
                ${agency}
              </span>
              <span class="font-mono text-[10px] text-[#138808] font-bold flex items-center gap-1">
                <span class="material-symbols-outlined text-[13px]">verified</span> 100% Free
              </span>
            </div>

            <h3 class="text-lg font-display font-black uppercase leading-tight line-clamp-2">
              ${foa.title}
            </h3>

            <p class="font-body text-xs text-on-surface-variant line-clamp-2 leading-relaxed">
              ${foa.brief_summary}
            </p>

            <!-- Key Criteria Pills -->
            <div class="bg-surface-container-low p-2.5 border border-outline font-mono text-[11px] space-y-1">
              <div class="flex justify-between">
                <span class="text-on-surface-variant text-[10px] uppercase">Eligibility:</span>
                <span class="font-bold text-on-surface text-right truncate max-w-[170px]">${minQual}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-on-surface-variant text-[10px] uppercase">Target Quota:</span>
                <span class="font-bold text-on-surface text-right truncate max-w-[170px]">${beneficiary}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-on-surface-variant text-[10px] uppercase">Deadline:</span>
                <span class="font-bold text-secondary text-right truncate max-w-[170px]">${deadline}</span>
              </div>
            </div>
          </div>

          <div class="space-y-3 border-t-3 border-outline pt-3 mt-4">
            <div class="flex items-baseline justify-between">
              <span class="font-mono text-[10px] uppercase text-on-surface-variant tracking-wider font-bold">Funding Value</span>
              <span class="font-display font-black text-xl text-on-surface">${displayAmount}</span>
            </div>

            <!-- Quick Action Links Bar -->
            <div class="grid grid-cols-2 gap-1.5 font-headline font-bold text-[11px]">
              <button class="py-1.5 px-2 bg-surface-container border border-outline hover:bg-primary-container text-center transition-colors uppercase flex items-center justify-center gap-1" onclick="openHinglishModal('${foa.foa_id}')">
                <span class="material-symbols-outlined text-[13px]">translate</span> Saral Guide
              </button>
              <button class="py-1.5 px-2 bg-surface-container border border-outline hover:bg-primary-container text-center transition-colors uppercase flex items-center justify-center gap-1" onclick="openDocChecklistModal('${foa.foa_id}')">
                <span class="material-symbols-outlined text-[13px]">checklist</span> Docs List
              </button>
            </div>

            <!-- Primary Buttons -->
            <div class="flex gap-2 pt-1">
              <a href="/api/foas/${foa.foa_id}/calendar" download class="py-2 px-2.5 bg-surface-container border-2 border-outline brutalist-shadow hover:bg-primary-container transition-colors flex items-center justify-center" title="Download .ics Calendar Reminder">
                <span class="material-symbols-outlined text-sm">calendar_month</span>
              </a>
              <button class="flex-1 py-2 px-3 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors flex items-center justify-center gap-1" onclick="openApplyModal('${foa.foa_id}')">
                <span>PORTAL DETAILS</span>
                <span class="material-symbols-outlined text-xs">open_in_new</span>
              </button>
            </div>
          </div>
        </article>
      `;
    }).join('');
  }

  async function runExploreSearch() {
    const q = document.getElementById('exploreSearchInput') ? document.getElementById('exploreSearchInput').value.trim() : '';
    const agency = currentExploreAgency;
    const sortBy = document.getElementById('exploreSortFilter') ? document.getElementById('exploreSortFilter').value : 'default';

    let results = [...allOpportunities];

    if (agency) {
      results = results.filter(o => o.agency && o.agency.toLowerCase().includes(agency.toLowerCase()));
    }

    if (q) {
      const qLow = q.toLowerCase();
      results = results.filter(o => 
        (o.title && o.title.toLowerCase().includes(qLow)) ||
        (o.brief_summary && o.brief_summary.toLowerCase().includes(qLow)) ||
        (o.agency && o.agency.toLowerCase().includes(qLow)) ||
        (o.eligibility && o.eligibility.raw_eligibility_text && o.eligibility.raw_eligibility_text.toLowerCase().includes(qLow))
      );
    }

    if (sortBy === 'amount_desc') {
      results.sort((a, b) => {
        const valA = (a.financials && a.financials.max_amount_inr) || 0;
        const valB = (b.financials && b.financials.max_amount_inr) || 0;
        return valB - valA;
      });
    } else if (sortBy === 'title_asc') {
      results.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
    }

    renderExploreGrid(results);
  }

  const sampleAbstracts = {
    1: {
      text: "Development of multimodal deep learning algorithms and vision transformers for early-stage oncology detection, histopathological image classification, and clinical validation across diverse multi-centric cohorts.",
      role: "Faculty / Principal Investigator",
      age: 38,
      degree: "Ph.D. Computer Science"
    },
    2: {
      text: "Quantum error correction codes and noise-resilient variational quantum eigensolvers designed for superconducting multi-qubit architectures and near-term intermediate scale quantum (NISQ) systems.",
      role: "Early Career Researcher",
      age: 32,
      degree: "Ph.D. Physics / Quantum"
    },
    3: {
      text: "Fabrication and degradation analysis of lead-free perovskite-silicon tandem photovoltaic cells for high-efficiency decentralized rural microgrids under extreme humidity and temperature stress.",
      role: "Faculty / Principal Investigator",
      age: 42,
      degree: "Ph.D. Materials Science"
    }
  };

  function loadSampleAbstract(num) {
    const sample = sampleAbstracts[num];
    if (!sample) return;
    const absEl = document.getElementById('matchAbstract');
    const roleEl = document.getElementById('matchRole');
    const ageEl = document.getElementById('matchAge');
    const degEl = document.getElementById('matchDegree');
    if (absEl) absEl.value = sample.text;
    if (roleEl) roleEl.value = sample.role;
    if (ageEl) ageEl.value = sample.age;
    if (degEl) degEl.value = sample.degree;
    runFacultyMatch();
  }

  async function runFacultyMatch() {
    const summary = document.getElementById('matchAbstract').value.trim();
    if(!summary) { alert('PLEASE ENTER OR SELECT A PROPOSAL ABSTRACT FIRST'); return; }
    
    let role = (document.getElementById('matchRole') && document.getElementById('matchRole').value) || "Faculty / Principal Investigator";
    if (!role || !role.trim()) role = "Faculty / Principal Investigator";
    const age = parseInt(document.getElementById('matchAge').value) || 38;
    const degree = (document.getElementById('matchDegree') && document.getElementById('matchDegree').value) || "Ph.D.";
    const container = document.getElementById('facultyResultsContainer');
    const countBadge = document.getElementById('facultyMatchCountBadge');
    
    container.innerHTML = `
      <div class="col-span-full p-12 text-center border-4 border-outline bg-surface-bright brutalist-shadow">
        <div class="inline-flex items-center gap-3 font-mono font-bold text-sm tracking-widest text-primary animate-pulse">
          <span class="material-symbols-outlined text-2xl animate-spin">refresh</span>
          RUNNING HYBRID VECTOR + BM25 MATCHER & COMPLIANCE GATE...
        </div>
      </div>
    `;

    try {
      const res = await fetch('/api/match-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ research_summary: summary, user_role: role, applicant_age: age, highest_degree: degree, top_k: 6 })
      });
      const results = await res.json();
      
      if(!results || !Array.isArray(results) || results.length===0){
        container.innerHTML = '<div class="col-span-full p-8 font-mono font-bold text-center border-4 border-outline bg-surface-bright">NO DIRECT CALLS MATCHED FOR THIS ABSTRACT. TRY BROADENING KEYWORDS.</div>';
        if (countBadge) countBadge.innerText = '0 MATCHES';
        return;
      }

      if (countBadge) countBadge.innerText = `${results.length} CALLS MATCHED`;

      container.innerHTML = results.map(m => {
        const foa = m.foa;
        const comp = m.compliance;
        const isEligible = comp.status === 'ELIGIBLE';
        const matchPct = Math.round((m.relevance_score || 0.85) * 100);
        
        let compBadgeBg = 'bg-primary text-white';
        let compBadgeText = 'ELIGIBILITY PASSED';
        if (comp.status === 'WARNING') {
          compBadgeBg = 'bg-[#ffcc00] text-black';
          compBadgeText = 'COMPLIANCE WARNING';
        } else if (comp.status === 'INELIGIBLE') {
          compBadgeBg = 'bg-secondary text-white';
          compBadgeText = 'RESTRICTION FAILED';
        }

        // Financial grant ceiling
        let budgetDisplay = 'GRANTS-IN-AID';
        if (foa.financials && foa.financials.max_amount_inr) {
          const amt = foa.financials.max_amount_inr;
          if (amt >= 10000000) {
            budgetDisplay = '₹' + (amt / 10000000).toFixed(2) + ' Cr';
          } else {
            budgetDisplay = '₹' + amt.toLocaleString('en-IN');
          }
        } else if (foa.financials && foa.financials.raw_budget_text) {
          budgetDisplay = foa.financials.raw_budget_text.substring(0, 30);
        }

        // Institutional overhead
        const overheadText = foa.financials && foa.financials.institutional_overhead_pct
          ? `${foa.financials.institutional_overhead_pct}% Institute Overhead`
          : 'Standard R&D Overhead';

        // Deadline
        const deadlineText = foa.deadlines && foa.deadlines.raw_deadline_text
          ? foa.deadlines.raw_deadline_text
          : 'Check Call Notice';

        // Keywords
        const keywordsHtml = (m.matching_keywords && m.matching_keywords.length > 0)
          ? m.matching_keywords.slice(0, 4).map(kw => `<span class="px-2 py-0.5 bg-surface-container font-mono text-[10px] font-bold uppercase border border-outline">${kw}</span>`).join('')
          : `<span class="px-2 py-0.5 bg-surface-container font-mono text-[10px] font-bold uppercase border border-outline">R&D Priority</span>`;

        return `
          <article class="bg-surface-bright border-4 border-outline shadow-[5px_5px_0px_#1a1a1a] p-6 lg:p-7 flex flex-col justify-between transition-transform hover:-translate-y-1">
            <div>
              <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                <div class="flex items-center gap-1.5 flex-wrap">
                  <span class="px-2.5 py-0.5 bg-surface-container font-mono text-xs font-black uppercase border-2 border-outline">${foa.agency}</span>
                  <span class="px-2.5 py-0.5 ${compBadgeBg} font-mono text-[11px] font-black uppercase border-2 border-outline">${compBadgeText}</span>
                </div>
                <span class="px-2.5 py-0.5 bg-primary text-white font-mono text-xs font-black uppercase border-2 border-outline tracking-wider">${matchPct}% RELEVANCE</span>
              </div>

              <h3 class="text-xl sm:text-2xl font-display font-extrabold uppercase text-on-surface leading-tight mb-2">
                ${foa.title}
              </h3>

              <p class="font-body text-xs sm:text-sm text-on-surface-variant font-medium leading-relaxed mb-4">
                ${foa.brief_summary}
              </p>

              <!-- Semantic keyword matches -->
              <div class="flex flex-wrap items-center gap-1.5 mb-4">
                <span class="font-mono text-[10px] font-bold uppercase text-on-surface-variant mr-1">Semantic Match:</span>
                ${keywordsHtml}
              </div>

              <!-- Grant Parameters Matrix -->
              <div class="grid grid-cols-2 gap-2 p-3 bg-surface-container-low border-2 border-outline font-mono text-xs mb-4">
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block font-semibold">Grant Ceiling</span>
                  <span class="font-bold text-on-surface text-sm text-primary">${budgetDisplay}</span>
                </div>
                <div class="border-l-2 border-outline pl-2">
                  <span class="text-[10px] text-on-surface-variant uppercase block font-semibold">Host Institute</span>
                  <span class="font-bold text-on-surface">${overheadText}</span>
                </div>
                <div class="border-l-2 border-outline pl-2 mt-1">
                  <span class="text-[10px] text-on-surface-variant uppercase block font-semibold">Target Cohort</span>
                  <span class="font-bold text-on-surface">${foa.eligibility && foa.eligibility.target_beneficiaries && foa.eligibility.target_beneficiaries[0] ? foa.eligibility.target_beneficiaries[0].replace('Principal Investigator', 'PI') : 'Faculty / PI'}</span>
                </div>
                <div class="border-l-2 border-outline pl-2 mt-1">
                  <span class="text-[10px] text-secondary uppercase block font-bold">Call Deadline</span>
                  <span class="font-bold text-secondary truncate block" title="${deadlineText}">${deadlineText}</span>
                </div>
              </div>

              <!-- Compliance Rule Engine Output -->
              <div class="p-3 bg-surface-container border-2 border-outline font-mono text-xs mb-4 space-y-1">
                <div class="font-bold uppercase text-[11px] text-on-surface flex items-center gap-1.5">
                  <span class="material-symbols-outlined text-[15px] ${isEligible ? 'text-primary' : 'text-secondary'}">verified</span>
                  Deterministic Compliance Gate:
                </div>
                ${comp.reasons.map(r => `<div class="text-[11px] text-on-surface-variant pl-4 leading-normal">${r}</div>`).join('')}
              </div>
            </div>

            <!-- Action buttons -->
            <div class="flex flex-wrap gap-2 border-t-4 border-outline pt-4 mt-2">
              <button class="flex-1 min-w-[130px] py-2.5 px-3 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline shadow-[2px_2px_0px_#1a1a1a] hover:bg-primary-container hover:text-primary transition-all flex items-center justify-center gap-1.5" onclick="draftProposal('${foa.foa_id}')">
                <span class="material-symbols-outlined text-[15px]">edit_document</span> Draft Proposal / SOP
              </button>
              <button class="py-2.5 px-3 bg-surface-container font-headline font-bold text-xs uppercase border-2 border-outline shadow-[2px_2px_0px_#1a1a1a] hover:bg-primary-container transition-all flex items-center gap-1" onclick="openDocChecklistModal('${foa.foa_id}')" title="Mandatory Submission Checklist">
                <span class="material-symbols-outlined text-[15px]">checklist</span> Checklist
              </button>
              <a href="/api/foas/${foa.foa_id}/calendar" download class="py-2.5 px-3 bg-surface-container font-headline font-bold text-xs uppercase border-2 border-outline shadow-[2px_2px_0px_#1a1a1a] hover:bg-primary-container transition-all flex items-center gap-1 inline-flex" title="Add submission deadline to calendar">
                <span class="material-symbols-outlined text-[15px]">calendar_month</span> .ics
              </a>
              <a href="${foa.direct_apply_url || foa.source_url}" target="_blank" class="py-2.5 px-3.5 bg-surface-container font-headline font-bold text-xs uppercase border-2 border-outline shadow-[2px_2px_0px_#1a1a1a] hover:bg-primary-container transition-all flex items-center gap-1 inline-flex" title="Open official agency call notice">
                <span>Call Notice</span> <span class="material-symbols-outlined text-[14px]">open_in_new</span>
              </a>
            </div>
          </article>
        `;
      }).join('');
    } catch(e) { container.innerHTML = '<div class="col-span-full p-8 text-secondary font-bold text-center border-4 border-outline bg-surface-bright">FAILED TO MATCH. CHECK SERVER CONNECTION.</div>'; }
  }

  async function openApplyModal(foaId) {
    document.getElementById('applyModalOverlay').classList.remove('hidden');
    try {
      const res = await fetch(`/api/foas/${foaId}`);
      const foa = await res.json();
      if (!res.ok || foa.detail) throw new Error(foa.detail || 'Opportunity not found');
      document.getElementById('modalSchemeTitle').innerText = foa.title;
      document.getElementById('modalAgencyTag').innerText = foa.agency;
      const applyUrl = foa.direct_apply_url || foa.source_url;
      const budgetStr = (foa.financials && foa.financials.raw_budget_text) || (foa.financials && foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString('en-IN') : 'DIRECT GRANT');
      document.getElementById('modalGrantText').innerText = 'BENEFIT: ' + budgetStr;
      document.getElementById('modalApplyLink').href = applyUrl;
      const shareMsg = encodeURIComponent(`Madadgaar Alert: Apply for ${foa.title} (${budgetStr}). Official Portal: ${applyUrl}`);
      const waLink = document.getElementById('modalWhatsappLink');
      if (waLink) waLink.href = `https://api.whatsapp.com/send?text=${shareMsg}`;
      const steps = foa.portal_navigation_steps && foa.portal_navigation_steps.length > 0 ? foa.portal_navigation_steps : ["1. Visit Portal", "2. Register with Aadhaar", "3. Submit forms"];
      document.getElementById('modalStepsTimeline').innerHTML = steps.map(s => `<div class="p-3 border-2 border-outline bg-surface-bright">${s}</div>`).join('');
    } catch(e) {
      document.getElementById('modalSchemeTitle').innerText = 'ERROR LOADING DETAILS';
    }
  }
  function closeApplyModal() { document.getElementById('applyModalOverlay').classList.add('hidden'); }

  async function openDocChecklistModal(foaId) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = "DOCUMENT READINESS CHECKLIST";
    const body = document.getElementById('genericModalBody');
    body.innerHTML = '<div class="font-mono font-bold">LOADING CHECKLIST...</div>';
    modal.classList.remove('hidden');
    try {
      const res = await fetch(`/api/student/scholarships/${foaId}/checklist`);
      const docs = await res.json();
      if (!res.ok || docs.detail || !Array.isArray(docs)) throw new Error('Checklist unavailable');
      body.innerHTML = `
        <div class="mb-4 p-3 bg-primary-container border-2 border-outline font-mono text-xs font-bold text-on-primary-container flex items-center gap-2">
          <span class="material-symbols-outlined text-[18px]">fact_check</span>
          Keep original stamped certificates ready before beginning portal application.
        </div>
        <div class="space-y-3">
          ${docs.map((d,i) => `
            <div class="p-4 border-3 border-outline bg-surface-bright brutalist-shadow">
              <div class="flex items-start justify-between gap-2 mb-2">
                <div class="font-display font-extrabold text-base uppercase text-on-surface">${i+1}. ${d.document_name}</div>
                ${d.is_mandatory ? '<span class="px-2 py-0.5 bg-secondary text-white font-mono text-[10px] font-bold uppercase shrink-0">Mandatory</span>' : '<span class="px-2 py-0.5 bg-surface-container font-mono text-[10px] font-bold uppercase shrink-0">Optional</span>'}
              </div>
              <div class="font-mono text-xs text-on-surface-variant space-y-1 mt-2 border-t border-outline-variant pt-2">
                <div><span class="font-bold text-on-surface">Issuing Authority:</span> ${d.issuing_authority}</div>
                <div><span class="font-bold text-on-surface">Validity &amp; Rule:</span> ${d.validity_and_rules}</div>
                ${d.how_to_obtain ? `<div><span class="font-bold text-on-surface">How to Obtain:</span> ${d.how_to_obtain}</div>` : ''}
              </div>
            </div>
          `).join('')}
        </div>
      `;
    } catch(e) { body.innerHTML = '<div class="text-secondary font-bold p-4">ERROR LOADING CHECKLIST.</div>'; }
  }

  async function openHinglishModal(foaId) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = "SARAL GUIDE (सरल गाइड)";
    const body = document.getElementById('genericModalBody');
    body.innerHTML = '<div class="font-mono font-bold">LOADING GUIDE...</div>';
    modal.classList.remove('hidden');
    try {
      const res = await fetch(`/api/student/scholarships/${foaId}/hinglish`);
      const g = await res.json();
      if (!res.ok || g.detail) throw new Error(g.detail || 'Guide unavailable');
      const shareMsg = encodeURIComponent(`*Madadgaar AI — Saral Guide*\n\n📌 पात्रता: ${g.kaun_apply_kar_sakta_hai}\n💰 लाभ: ${g.kitne_paise_milenge}\n\n⚠️ ${g.aadhaar_seeding_warning}\n\nऑफिशियल पोर्टल: ${g.official_portal_url}`);
      body.innerHTML = `
        <div class="space-y-4">
          <div class="p-4 border-4 border-outline bg-surface-bright brutalist-shadow">
            <h4 class="font-display font-black text-lg mb-2 flex items-center gap-2">
              <span class="material-symbols-outlined text-tertiary">how_to_reg</span>
              ELIGIBILITY (पात्रता)
            </h4>
            <p class="font-body font-medium leading-relaxed">${g.kaun_apply_kar_sakta_hai}</p>
          </div>
          <div class="p-4 border-4 border-outline bg-surface-bright brutalist-shadow">
            <h4 class="font-display font-black text-lg mb-2 flex items-center gap-2">
              <span class="material-symbols-outlined text-[#138808]">payments</span>
              BENEFITS (आर्थिक सहायता)
            </h4>
            <p class="font-body font-medium leading-relaxed">${g.kitne_paise_milenge}</p>
          </div>
          <div class="p-4 border-4 border-outline bg-secondary text-white brutalist-shadow">
            <h4 class="font-display font-black text-lg mb-2 flex items-center gap-2">
              <span class="material-symbols-outlined text-white">warning</span>
              DBT SEEDING NOTICE
            </h4>
            <p class="font-body font-medium leading-relaxed">${g.aadhaar_seeding_warning}</p>
          </div>
          <div class="p-4 border-4 border-outline bg-primary-container text-on-primary-container brutalist-shadow">
            <h4 class="font-display font-black text-lg mb-2 flex items-center gap-2">
              <span class="material-symbols-outlined">shield</span>
              ANTI-SCAM ADVISORY
            </h4>
            <p class="font-body font-medium leading-relaxed">${g.scam_alert}</p>
          </div>
          <div class="pt-2 flex flex-wrap gap-3 justify-between items-center border-t-2 border-outline-variant">
            <a href="https://api.whatsapp.com/send?text=${shareMsg}" target="_blank" class="px-5 py-2.5 bg-[#138808] text-white font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow flex items-center gap-1.5 hover:bg-black transition-colors">
              <span class="material-symbols-outlined text-[16px]">share</span> Share on WhatsApp
            </a>
            <a href="${g.official_portal_url}" target="_blank" class="px-5 py-2.5 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline brutalist-shadow hover:bg-primary-container hover:text-primary transition-colors flex items-center gap-1.5">
              <span>Go to Official Portal</span>
              <span class="material-symbols-outlined text-[16px]">open_in_new</span>
            </a>
          </div>
        </div>
      `;
    } catch(e) { body.innerHTML = '<div class="text-secondary font-bold p-4">ERROR LOADING GUIDE.</div>'; }
  }

  async function draftProposal(foaId) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = "AI PROPOSAL & SOP ARCHITECT";
    const body = document.getElementById('genericModalBody');
    body.innerHTML = `
      <div class="p-8 text-center font-mono font-bold text-sm tracking-widest text-primary animate-pulse">
        <span class="material-symbols-outlined text-3xl animate-spin block mb-2">auto_awesome</span>
        GENERATING TAILORED GRANT PROPOSAL SKELETON...
      </div>
    `;
    modal.classList.remove('hidden');
    try {
      const res = await fetch(`/api/foas/${foaId}/draft-proposal`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ pi_name:"Dr. Principal Investigator", institution_name:"IIT / Central University / NIT" })
      });
      const data = await res.json();
      
      const fullText = `# PROPOSAL: ${data.scheme_title}\nAgency: ${data.agency}\nTarget Deadline: ${data.target_deadline || 'Open'}\n\n` +
        data.sections.map(s => `## ${s.section_title}\n${s.section_description}\n\n${s.drafted_content}\n\nKey Tips:\n${(s.tips||[]).map(t=>'- '+t).join('\n')}\n`).join('\n---\n\n');

      body.innerHTML = `
        <div class="mb-5 pb-4 border-b-2 border-outline flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <span class="px-2.5 py-0.5 bg-primary text-white font-mono text-[11px] font-bold uppercase border border-outline">${data.agency} SCHEME</span>
            <h3 class="font-display font-black text-xl sm:text-2xl mt-1 uppercase text-on-surface">${data.scheme_title}</h3>
          </div>
          <button onclick="navigator.clipboard.writeText(decodeURIComponent('${encodeURIComponent(fullText)}')); alert('Proposal Copied to Clipboard!');" class="px-4 py-2 bg-primary text-white font-headline font-bold text-xs uppercase border-2 border-outline shadow-[2px_2px_0px_#1a1a1a] hover:bg-primary-container hover:text-primary transition-all flex items-center gap-1.5 shrink-0">
            <span class="material-symbols-outlined text-[16px]">content_copy</span> Copy Full Draft
          </button>
        </div>

        <div class="space-y-4">
          ${data.sections.map((s, idx) => `
            <div class="border-3 border-outline bg-surface-bright shadow-[3px_3px_0px_#1a1a1a] p-5">
              <div class="flex items-center justify-between gap-2 mb-2 pb-2 border-b border-outline/30">
                <div class="font-display font-extrabold text-base uppercase text-on-surface flex items-center gap-2">
                  <span class="w-6 h-6 rounded-none bg-primary text-white font-mono text-xs flex items-center justify-center font-bold">${idx+1}</span>
                  ${s.section_title}
                </div>
                <span class="text-[11px] font-mono text-on-surface-variant italic hidden sm:inline">${s.section_description}</span>
              </div>
              <div class="bg-surface-container-low p-3.5 border border-outline font-mono text-xs leading-relaxed text-on-surface mb-3 whitespace-pre-wrap">${s.drafted_content}</div>
              ${s.tips && s.tips.length > 0 ? `
                <div class="font-mono text-[11px] text-on-surface-variant flex items-start gap-1.5 pt-1">
                  <span class="material-symbols-outlined text-[14px] text-secondary shrink-0">lightbulb</span>
                  <span><strong>Reviewer Tip:</strong> ${s.tips[0]}</span>
                </div>
              ` : ''}
            </div>
          `).join('')}
        </div>
      `;
    } catch(e) { body.innerHTML = '<div class="text-secondary font-bold p-4">FAILED TO GENERATE DRAFT PROPOSAL.</div>'; }
  }

  function openInfoModal(title, text) {
    const modal = document.getElementById('genericModalOverlay');
    document.getElementById('genericModalTitle').innerText = title;
    const body = document.getElementById('genericModalBody');
    body.innerHTML = `<div class="p-6 font-body font-medium text-base sm:text-lg border-4 border-outline bg-surface-bright brutalist-shadow">${text}</div>`;
    modal.classList.remove('hidden');
  }
  function closeGenericModal() { document.getElementById('genericModalOverlay').classList.add('hidden'); }
  async function triggerDbSync() {
    const btn = document.getElementById('syncDbBtn');
    if (btn) {
      btn.innerHTML = '<span class="material-symbols-outlined text-[16px] animate-spin">sync</span> SYNCING...';
      btn.disabled = true;
    }
    try {
      await fetch('/api/ingest/trigger', {method:'POST'});
      await loadOpportunities();
      runStudentMatch();
      if (btn) {
        btn.innerHTML = '<span class="material-symbols-outlined text-[16px]">check_circle</span> SYNCED';
      }
    } catch(e) {
      if (btn) {
        btn.innerHTML = '<span class="material-symbols-outlined text-[16px] text-secondary">error</span> FAILED';
      }
    } finally {
      setTimeout(() => {
        if (btn) {
          btn.innerHTML = '<span class="material-symbols-outlined text-[16px]">sync</span> SYNC DB';
          btn.disabled = false;
        }
      }, 2500);
    }
  }
  document.addEventListener('keydown', (e) => { if(e.key==='Escape') { closeApplyModal(); closeGenericModal(); } });
  
  initPlatform();
</script>
</body>
</html>
"""
