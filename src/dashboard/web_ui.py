"""Modern Interactive Dashboard UI for MadadgaarAI."""


def render_dashboard_html() -> str:
    return """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MadadgaarAI — AI-Powered Funding Intelligence Platform</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0a0f1d;
      --bg-surface: #111827;
      --bg-card: rgba(17, 24, 39, 0.75);
      --bg-card-hover: rgba(30, 41, 59, 0.85);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: #6366f1;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --accent-indigo: #6366f1;
      --accent-purple: #a855f7;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --font-sans: 'Outfit', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-base);
      background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.12) 0px, transparent 50%);
      color: var(--text-primary);
      font-family: var(--font-sans);
      min-height: 100vh;
      line-height: 1.5;
    }

    /* Layout Containers */
    .app-container {
      max-width: 1380px;
      margin: 0 auto;
      padding: 24px;
    }

    /* Header Nav */
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 18px 28px;
      background: var(--bg-card);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      margin-bottom: 28px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-logo {
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      font-weight: 800;
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
    }

    .brand-title {
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.5px;
      background: linear-gradient(to right, #ffffff, #cbd5e1);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 400;
      letter-spacing: 0.5px;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: var(--accent-emerald);
      border-radius: 999px;
      font-size: 13px;
      font-weight: 500;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      background: var(--accent-emerald);
      border-radius: 50%;
      box-shadow: 0 0 8px var(--accent-emerald);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.4; }
    }

    /* Hero Banner */
    .hero-banner {
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 24px;
      padding: 32px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.85));
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      margin-bottom: 32px;
      position: relative;
      overflow: hidden;
    }

    .hero-banner::after {
      content: '';
      position: absolute;
      top: -50%;
      right: -10%;
      width: 350px;
      height: 350px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.18), transparent 70%);
      pointer-events: none;
    }

    .hero-title {
      font-size: 32px;
      font-weight: 800;
      letter-spacing: -0.8px;
      margin-bottom: 8px;
    }

    .hero-title span {
      background: linear-gradient(135deg, #818cf8, #c084fc, #38bdf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-desc {
      color: var(--text-secondary);
      font-size: 15px;
      max-width: 680px;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .stat-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-subtle);
      padding: 16px 20px;
      border-radius: 14px;
      text-align: center;
      min-width: 120px;
    }

    .stat-num {
      font-size: 24px;
      font-weight: 700;
      color: #ffffff;
      font-family: var(--font-mono);
    }

    .stat-label {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    /* Tabs Bar */
    .tabs-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 12px;
    }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 15px;
      font-weight: 600;
      padding: 10px 20px;
      border-radius: 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s ease;
    }

    .tab-btn:hover {
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.05);
    }

    .tab-btn.active {
      color: #ffffff;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.25));
      border: 1px solid rgba(99, 102, 241, 0.4);
    }

    /* Search and Filter Panel */
    .search-filter-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 20px;
      margin-bottom: 28px;
    }

    .search-row {
      display: grid;
      grid-template-columns: 1fr auto auto;
      gap: 12px;
      margin-bottom: 14px;
    }

    .input-box {
      width: 100%;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 12px 18px;
      color: #ffffff;
      font-size: 14px;
      font-family: var(--font-sans);
      outline: none;
      transition: border-color 0.2s;
    }

    .input-box:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
    }

    .select-box {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 12px 16px;
      color: #ffffff;
      font-size: 14px;
      font-family: var(--font-sans);
      outline: none;
      cursor: pointer;
    }

    .primary-btn {
      background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
      color: #ffffff;
      border: none;
      border-radius: 10px;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: transform 0.15s, box-shadow 0.15s;
    }

    .primary-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
    }

    .secondary-btn {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-primary);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 8px 14px;
      font-size: 13px;
      font-weight: 500;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .secondary-btn:hover {
      background: rgba(255, 255, 255, 0.12);
    }

    /* Opportunities Cards Grid */
    .opportunities-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
      gap: 20px;
    }

    .foa-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      position: relative;
    }

    .foa-card:hover {
      background: var(--bg-card-hover);
      border-color: rgba(99, 102, 241, 0.4);
      transform: translateY(-3px);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.4);
    }

    .foa-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .agency-tag {
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .agency-DST { background: rgba(99, 102, 241, 0.2); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
    .agency-ANRF { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .agency-CSIR { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .agency-AICTE { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .agency-NSP { background: rgba(6, 182, 212, 0.2); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); }
    .agency-DBT { background: rgba(244, 63, 94, 0.2); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }

    .foa-id-badge {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--text-muted);
      background: rgba(0, 0, 0, 0.3);
      padding: 3px 8px;
      border-radius: 4px;
    }

    .foa-title {
      font-size: 17px;
      font-weight: 600;
      margin-bottom: 8px;
      color: #ffffff;
      line-height: 1.4;
    }

    .foa-summary {
      font-size: 13.5px;
      color: var(--text-secondary);
      margin-bottom: 16px;
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .thematic-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 16px;
    }

    .thematic-pill {
      font-size: 11px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: var(--text-secondary);
      padding: 3px 8px;
      border-radius: 999px;
    }

    .foa-meta-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding: 12px;
      background: rgba(0, 0, 0, 0.25);
      border-radius: 10px;
      margin-bottom: 16px;
    }

    .meta-item-label {
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .meta-item-value {
      font-size: 13.5px;
      font-weight: 600;
      color: #ffffff;
      margin-top: 2px;
    }

    .card-actions {
      display: flex;
      gap: 8px;
      margin-top: auto;
    }

    /* Modal / Drawer */
    .modal-overlay {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 999;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-dialog {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      max-width: 800px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      padding: 32px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 16px;
    }

    .close-btn {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 24px;
      cursor: pointer;
      padding: 4px;
    }

    .close-btn:hover {
      color: #ffffff;
    }

    /* Proposal & Matcher Output */
    .match-item {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 14px;
    }

    .match-score-bar-bg {
      background: rgba(255, 255, 255, 0.1);
      height: 6px;
      border-radius: 3px;
      margin: 8px 0;
      overflow: hidden;
    }

    .match-score-bar-fill {
      height: 100%;
      background: linear-gradient(to right, var(--accent-indigo), var(--accent-emerald));
      border-radius: 3px;
    }

    .badge-eligible {
      color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }

    .badge-warning {
      color: var(--accent-amber);
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.3);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }

    .badge-ineligible {
      color: var(--accent-rose);
      background: rgba(244, 63, 94, 0.15);
      border: 1px solid rgba(244, 63, 94, 0.3);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }

    pre code {
      font-family: var(--font-mono);
      font-size: 13px;
      color: #e2e8f0;
      background: #0f172a;
      padding: 16px;
      border-radius: 10px;
      display: block;
      overflow-x: auto;
      border: 1px solid var(--border-subtle);
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class="app-container">
    <!-- Header -->
    <header>
      <div class="brand-group">
        <div class="brand-logo">M</div>
        <div>
          <h1 class="brand-title">MadadgaarAI</h1>
          <div class="brand-subtitle">AI-POWERED FUNDING INTELLIGENCE & GRANT MATCHING</div>
        </div>
      </div>
      <div class="header-actions">
        <div class="status-pill">
          <span class="status-dot"></span>
          <span id="headerStatusText">Live Pipeline Online</span>
        </div>
        <button class="secondary-btn" onclick="triggerIngestion()">
          🔄 Ingest & Crawl
        </button>
      </div>
    </header>

    <!-- Hero Banner -->
    <div class="hero-banner">
      <div>
        <h2 class="hero-title">Automated Grant Discovery & <span>Semantic Matching</span></h2>
        <p class="hero-desc">
          Unified intelligence platform ingesting and normalizing public circulars across 
          DST, ANRF/SERB, CSIR, AICTE, NSP, and DBT with OCR fallback and Reciprocal Rank Fusion.
        </p>
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-num" id="statTotal">8</div>
          <div class="stat-label">Total Schemes</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" id="statAgencies">6</div>
          <div class="stat-label">Statutory Portals</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" id="statMaxGrant">₹ 60L</div>
          <div class="stat-label">Max Grant Cap</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" id="statAvgDensity">100%</div>
          <div class="stat-label">Schema Validated</div>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-bar">
      <button class="tab-btn active" onclick="switchTab('explore')">
        🔍 Explore Opportunities
      </button>
      <button class="tab-btn" onclick="switchTab('matcher')">
        🎯 Faculty & Student Matcher
      </button>
      <button class="tab-btn" onclick="switchTab('analytics')">
        📊 Academic Taxonomy & Analytics
      </button>
    </div>

    <!-- TAB 1: Explore Opportunities -->
    <div id="tab-explore">
      <div class="search-filter-card">
        <div class="search-row">
          <input type="text" id="searchInput" class="input-box" placeholder="Semantic search e.g. 'clean energy quantum computing fellowship' or 'women scientists biotech'..." onkeyup="if(event.key === 'Enter') runSearch()">
          <select id="agencyFilter" class="select-box" onchange="runSearch()">
            <option value="">All Agencies</option>
            <option value="DST">DST</option>
            <option value="ANRF/SERB">ANRF / SERB</option>
            <option value="CSIR">CSIR</option>
            <option value="AICTE">AICTE</option>
            <option value="NSP">NSP</option>
            <option value="DBT">DBT</option>
          </select>
          <button class="primary-btn" onclick="runSearch()">
            ⚡ Hybrid Search
          </button>
        </div>
      </div>

      <div class="opportunities-grid" id="foaGrid">
        <!-- Rendered via JavaScript -->
      </div>
    </div>

    <!-- TAB 2: Profile Matcher -->
    <div id="tab-matcher" style="display: none;">
      <div class="search-filter-card">
        <h3 style="margin-bottom: 8px; font-size: 18px;">Profile-to-Grant Semantic Alignment Engine</h3>
        <p style="color: var(--text-secondary); font-size: 13.5px; margin-bottom: 20px;">
          Paste your research abstract, project proposal idea, or CV summary. MadadgaarAI computes dense 384-d vector embeddings and validates eligibility constraints.
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 16px;">
          <div>
            <label class="meta-item-label">Applicant Role</label>
            <select id="matchRole" class="select-box" style="width: 100%; margin-top: 4px;">
              <option value="Faculty / Principal Investigator">Faculty / Principal Investigator</option>
              <option value="Early Career Researcher">Early Career Researcher</option>
              <option value="Women Scientists">Women Scientists</option>
              <option value="PhD Scholars & Postdoctoral Fellows">PhD Scholars & Postdocs</option>
              <option value="UG / PG Students">UG / PG Students</option>
              <option value="Startups & Industry Partners">Startups & Industry</option>
            </select>
          </div>
          <div>
            <label class="meta-item-label">Applicant Age (Years)</label>
            <input type="number" id="matchAge" class="input-box" style="margin-top: 4px;" value="38" min="18" max="75">
          </div>
          <div>
            <label class="meta-item-label">Highest Qualification</label>
            <input type="text" id="matchDegree" class="input-box" style="margin-top: 4px;" value="Ph.D. in Computer Science">
          </div>
        </div>

        <div style="margin-bottom: 16px;">
          <label class="meta-item-label">Research Abstract / Statement</label>
          <textarea id="matchAbstract" class="input-box" rows="4" style="margin-top: 4px;" placeholder="Describe your research project, key aims, domain thrust, and technological application..."></textarea>
        </div>

        <button class="primary-btn" onclick="runProfileMatch()">
          🚀 Run Profile Match & Compliance Check
        </button>
      </div>

      <div id="matchResultsContainer">
        <!-- Rendered Results -->
      </div>
    </div>

    <!-- TAB 3: Analytics & Benchmark -->
    <div id="tab-analytics" style="display: none;">
      <div class="search-filter-card">
        <h3 style="margin-bottom: 14px; font-size: 18px;">Indian Funding Intelligence Architecture</h3>
        <p style="color: var(--text-secondary); font-size: 14px; line-height: 1.6; margin-bottom: 20px;">
          MadadgaarAI establishes an end-to-end reproducible pipeline featuring:
          <strong>Asynchronous Crawling</strong> (DST, ANRF, CSIR, AICTE, NSP), <strong>OCR Layout Recovery</strong> via Tesseract, <strong>Pydantic Schema Validation</strong>, <strong>Sentence-Transformers (384-d)</strong>, and <strong>BM25 + Dense RRF Hybrid Search</strong>.
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
          <div style="background: rgba(0,0,0,0.3); padding: 18px; border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div style="color: var(--accent-indigo); font-weight: 700; margin-bottom: 6px;">Hybrid Search (RRF)</div>
            <div style="font-size: 13px; color: var(--text-secondary);">Combines Lexical BM25 keyword matching with Dense Vector Cosine Similarity using Reciprocal Rank Fusion (k=60).</div>
          </div>
          <div style="background: rgba(0,0,0,0.3); padding: 18px; border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div style="color: var(--accent-emerald); font-weight: 700; margin-bottom: 6px;">Fault-Tolerant OCR</div>
            <div style="font-size: 13px; color: var(--text-secondary);">Evaluates character density per page. Low density triggers automated raster OCR extraction fallback.</div>
          </div>
          <div style="background: rgba(0,0,0,0.3); padding: 18px; border-radius: 12px; border: 1px solid var(--border-subtle);">
            <div style="color: var(--accent-purple); font-weight: 700; margin-bottom: 6px;">Downstream Proposal Drafter</div>
            <div style="font-size: 13px; color: var(--text-secondary);">Instant generation of tailored proposal skeletons with MoF OM compliant budget allocations and Gantt milestones.</div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Modal Dialog for Proposal Skeleton / Details -->
  <div class="modal-overlay" id="modalOverlay">
    <div class="modal-dialog">
      <div class="modal-header">
        <h3 id="modalTitle" style="font-size: 20px; color: #ffffff;">Proposal Skeleton</h3>
        <button class="close-btn" onclick="closeModal()">&times;</button>
      </div>
      <div id="modalBody">
        <!-- Injected dynamically -->
      </div>
    </div>
  </div>

  <script>
    let allFOAs = [];

    async function loadOpportunities() {
      try {
        const res = await fetch('/api/foas');
        allFOAs = await res.json();
        renderFOAGrid(allFOAs);
        updateStats(allFOAs);
      } catch (err) {
        console.error('Failed to load opportunities:', err);
      }
    }

    function renderFOAGrid(items) {
      const grid = document.getElementById('foaGrid');
      if (!items || items.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">No funding opportunities found matching criteria.</div>';
        return;
      }

      grid.innerHTML = items.map(foa => {
        const agencyClass = 'agency-' + (foa.agency.replace('/', '_').replace('ANRF_SERB', 'ANRF'));
        const budgetStr = foa.financials.max_amount_inr 
          ? '₹ ' + (foa.financials.max_amount_inr / 100000).toFixed(1) + ' Lakhs'
          : (foa.financials.stipend_monthly_inr ? '₹ ' + foa.financials.stipend_monthly_inr.toLocaleString() + '/mo' : 'As per norms');
        
        const deadlineStr = foa.deadlines.extended_closing_date || foa.deadlines.closing_date || (foa.deadlines.is_rolling ? 'Rolling' : 'N/A');

        return `
          <div class="foa-card">
            <div>
              <div class="foa-card-header">
                <span class="agency-tag ${agencyClass}">${foa.agency}</span>
                <span class="foa-id-badge">${foa.foa_id}</span>
              </div>
              <h3 class="foa-title">${foa.title}</h3>
              <p class="foa-summary">${foa.brief_summary}</p>
              <div class="thematic-pills">
                ${(foa.thematic_areas || []).map(t => `<span class="thematic-pill">${t}</span>`).join('')}
              </div>
              <div class="foa-meta-row">
                <div>
                  <div class="meta-item-label">Max Grant Ceiling</div>
                  <div class="meta-item-value">${budgetStr}</div>
                </div>
                <div>
                  <div class="meta-item-label">Closing Deadline</div>
                  <div class="meta-item-value">${deadlineStr}</div>
                </div>
              </div>
            </div>
            <div class="card-actions">
              <button class="secondary-btn" onclick="draftProposal('${foa.foa_id}')">
                📝 Draft Proposal
              </button>
              <button class="secondary-btn" onclick="downloadCalendar('${foa.foa_id}')">
                📅 .ICS
              </button>
              <a href="${foa.source_url}" target="_blank" class="secondary-btn" style="text-decoration: none;">
                🔗 Portal
              </a>
            </div>
          </div>
        `;
      }).join('');
    }

    function updateStats(items) {
      document.getElementById('statTotal').innerText = items.length;
      const agencies = new Set(items.map(i => i.agency));
      document.getElementById('statAgencies').innerText = agencies.size;
    }

    async function runSearch() {
      const q = document.getElementById('searchInput').value.trim();
      const agency = document.getElementById('agencyFilter').value;

      if (!q && !agency) {
        renderFOAGrid(allFOAs);
        return;
      }

      const res = await fetch('/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: q || "research funding grants",
          agency_filter: agency || null,
          top_k: 10
        })
      });
      const data = await res.json();
      renderFOAGrid(data.map(d => d.foa));
    }

    async function runProfileMatch() {
      const summary = document.getElementById('matchAbstract').value.trim();
      if (!summary) {
        alert('Please enter a research abstract or statement.');
        return;
      }

      const role = document.getElementById('matchRole').value;
      const age = parseInt(document.getElementById('matchAge').value) || 35;
      const degree = document.getElementById('matchDegree').value;

      const container = document.getElementById('matchResultsContainer');
      container.innerHTML = '<div style="text-align: center; padding: 24px;">Computing dense embeddings & matching...</div>';

      const res = await fetch('/api/match-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          research_summary: summary,
          user_role: role,
          applicant_age: age,
          highest_degree: degree,
          top_k: 5
        })
      });

      const results = await res.json();
      container.innerHTML = results.map(m => {
        const badgeClass = m.compliance.status === 'ELIGIBLE' ? 'badge-eligible' : (m.compliance.status === 'WARNING' ? 'badge-warning' : 'badge-ineligible');
        return `
          <div class="match-item">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
              <div>
                <span class="agency-tag agency-${m.foa.agency.replace('/', '_')}">${m.foa.agency}</span>
                <strong style="margin-left: 8px; font-size: 16px;">${m.foa.title}</strong>
              </div>
              <span class="${badgeClass}">${m.compliance.status}</span>
            </div>
            <div style="font-size: 12px; color: var(--text-secondary);">
              Hybrid Match Score: <strong>${(m.relevance_score * 100).toFixed(1)}%</strong> | BM25: ${m.bm25_score} | Dense Sim: ${m.dense_score}
            </div>
            <div class="match-score-bar-bg">
              <div class="match-score-bar-fill" style="width: ${Math.min(100, m.relevance_score * 100)}%;"></div>
            </div>
            <div style="font-size: 13px; color: var(--text-muted); margin-top: 8px;">
              <strong>Eligibility Evaluation:</strong> ${m.compliance.reasons.join(' ')}
            </div>
            <div style="margin-top: 12px; display: flex; gap: 8px;">
              <button class="secondary-btn" onclick="draftProposal('${m.foa.foa_id}')">📝 Draft Proposal</button>
              <button class="secondary-btn" onclick="downloadCalendar('${m.foa.foa_id}')">📅 .ICS Deadline</button>
            </div>
          </div>
        `;
      }).join('');
    }

    async function draftProposal(foaId) {
      const modal = document.getElementById('modalOverlay');
      const body = document.getElementById('modalBody');
      body.innerHTML = 'Generating tailored proposal skeleton...';
      modal.classList.add('active');

      const res = await fetch(`/api/foas/${foaId}/draft-proposal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pi_name: "Dr. Faculty Researcher",
          institution_name: "JK Lakshmipat University, Jaipur"
        })
      });
      const data = await res.json();

      let html = `
        <h4 style="color: var(--accent-indigo); margin-bottom: 12px;">${data.scheme_title} (${data.agency})</h4>
        <div style="margin-bottom: 20px;">
          <h5 style="color: #ffffff; margin-bottom: 8px;">Suggested Budget Allocation (MoF OM Norms)</h5>
          <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px;">
            ${Object.entries(data.suggested_budget_breakdown).map(([k, v]) => `<div><strong>${k}:</strong> ${v}</div>`).join('')}
          </div>
        </div>
        <div>
          <h5 style="color: #ffffff; margin-bottom: 8px;">Proposal Sections & Drafted Content</h5>
          ${data.sections.map(sec => `
            <div style="margin-bottom: 16px;">
              <div style="font-weight: 600; color: #cbd5e1;">${sec.section_title}</div>
              <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px;">${sec.section_description}</div>
              <pre><code>${sec.drafted_content}</code></pre>
            </div>
          `).join('')}
        </div>
      `;
      body.innerHTML = html;
    }

    function downloadCalendar(foaId) {
      window.location.href = `/api/foas/${foaId}/calendar`;
    }

    async function triggerIngestion() {
      const statusText = document.getElementById('headerStatusText');
      statusText.innerText = 'Ingesting circulars...';
      const res = await fetch('/api/ingest/trigger', { method: 'POST' });
      const report = await res.json();
      statusText.innerText = `Ingested: ${report.new_opportunities_indexed} new`;
      await loadOpportunities();
    }

    function switchTab(tabId) {
      document.getElementById('tab-explore').style.display = tabId === 'explore' ? 'block' : 'none';
      document.getElementById('tab-matcher').style.display = tabId === 'matcher' ? 'block' : 'none';
      document.getElementById('tab-analytics').style.display = tabId === 'analytics' ? 'block' : 'none';

      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      event.currentTarget.classList.add('active');
    }

    function closeModal() {
      document.getElementById('modalOverlay').classList.remove('active');
    }

    // Initialize on load
    loadOpportunities();
  </script>
</body>
</html>
"""
