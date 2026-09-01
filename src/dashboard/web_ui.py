"""Modern Interactive Dashboard UI for MadadgaarAI with Student Scholarship Hub (Vidyarthi AI)."""


def render_dashboard_html() -> str:
    return r"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MadadgaarAI — Indian Student Scholarships & Research Funding Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #0a0f1d;
      --bg-surface: #111827;
      --bg-card: rgba(17, 24, 39, 0.78);
      --bg-card-hover: rgba(30, 41, 59, 0.9);
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
      --accent-orange: #fb923c;
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
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
        radial-gradient(at 50% 50%, rgba(16, 185, 129, 0.05) 0px, transparent 50%);
      color: var(--text-primary);
      font-family: var(--font-sans);
      min-height: 100vh;
      line-height: 1.5;
    }

    .app-container {
      max-width: 1400px;
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
      border-radius: 18px;
      margin-bottom: 24px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .brand-logo {
      width: 46px;
      height: 46px;
      background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
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
      font-weight: 500;
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

    /* Scam Shield Banner */
    .scam-shield-banner {
      background: linear-gradient(90deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.15));
      border: 1px solid rgba(16, 185, 129, 0.35);
      border-radius: 14px;
      padding: 14px 20px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    .scam-shield-content {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 13.5px;
      color: #e2e8f0;
    }

    .scam-shield-badge {
      background: var(--accent-emerald);
      color: #0f172a;
      font-weight: 700;
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Hero Banner */
    .hero-banner {
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 24px;
      padding: 28px 32px;
      background: linear-gradient(135deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.9));
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      margin-bottom: 24px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }

    .hero-title {
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 8px;
      letter-spacing: -0.5px;
    }

    .hero-title span {
      background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-desc {
      color: var(--text-secondary);
      font-size: 14.5px;
      max-width: 720px;
      line-height: 1.6;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
    }

    .stat-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 16px 20px;
      text-align: center;
      min-width: 110px;
    }

    .stat-num {
      font-size: 22px;
      font-weight: 800;
      color: var(--text-primary);
      font-family: var(--font-mono);
    }

    .stat-label {
      font-size: 11.5px;
      color: var(--text-muted);
      margin-top: 4px;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Tabs Bar */
    .tabs-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 24px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 12px;
      overflow-x: auto;
    }

    .tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-secondary);
      padding: 10px 20px;
      border-radius: 10px;
      font-size: 14px;
      font-weight: 600;
      font-family: var(--font-sans);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all 0.2s;
    }

    .tab-btn:hover {
      color: var(--text-primary);
      background: rgba(255, 255, 255, 0.05);
    }

    .tab-btn.active {
      color: #ffffff;
      background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.25));
      border: 1px solid rgba(99, 102, 241, 0.4);
      box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
    }

    /* Panels & Cards */
    .panel-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: 18px;
      padding: 24px;
      margin-bottom: 28px;
    }

    .input-box, .select-box {
      width: 100%;
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 12px 16px;
      color: #ffffff;
      font-size: 14px;
      font-family: var(--font-sans);
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .input-box:focus, .select-box:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
    }

    .primary-btn {
      background: linear-gradient(135deg, var(--accent-indigo), var(--accent-purple));
      color: #ffffff;
      border: none;
      border-radius: 10px;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 600;
      font-family: var(--font-sans);
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
      background: rgba(255, 255, 255, 0.07);
      color: var(--text-primary);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 8px 14px;
      font-size: 13px;
      font-weight: 500;
      font-family: var(--font-sans);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none;
    }

    .secondary-btn:hover {
      background: rgba(255, 255, 255, 0.14);
      color: #ffffff;
    }

    .direct-apply-btn {
      background: linear-gradient(135deg, #10b981, #059669);
      color: #ffffff;
      border: none;
      border-radius: 8px;
      padding: 8px 16px;
      font-size: 13.5px;
      font-weight: 700;
      font-family: var(--font-sans);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none;
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
    }

    .direct-apply-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(16, 185, 129, 0.5);
      color: #ffffff;
    }

    .whatsapp-btn {
      background: rgba(37, 211, 102, 0.15);
      color: #25d366;
      border: 1px solid rgba(37, 211, 102, 0.35);
      border-radius: 8px;
      padding: 8px 14px;
      font-size: 13px;
      font-weight: 600;
      font-family: var(--font-sans);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
      text-decoration: none;
    }

    .whatsapp-btn:hover {
      background: rgba(37, 211, 102, 0.25);
    }

    /* Scholarship & Grant Cards */
    .opportunities-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(430px, 1fr));
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
      transition: transform 0.2s, border-color 0.2s;
    }

    .foa-card:hover {
      transform: translateY(-2px);
      border-color: rgba(99, 102, 241, 0.35);
    }

    .foa-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }

    .agency-tag {
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .agency-DST { background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.3); }
    .agency-ANRF { background: rgba(168, 85, 247, 0.15); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.3); }
    .agency-CSIR { background: rgba(6, 182, 212, 0.15); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); }
    .agency-AICTE { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .agency-NSP { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .agency-DBT { background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }
    .agency-UGC { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
    .agency-STATE_GOVT { background: rgba(251, 146, 60, 0.15); color: #fdba74; border: 1px solid rgba(251, 146, 60, 0.3); }
    .agency-CSR_FOUNDATION { background: rgba(236, 72, 153, 0.15); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.3); }

    .foa-title {
      font-size: 17px;
      font-weight: 700;
      line-height: 1.4;
      margin-bottom: 8px;
      color: #ffffff;
    }

    .foa-summary {
      font-size: 13.5px;
      color: var(--text-secondary);
      line-height: 1.55;
      margin-bottom: 14px;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .benefit-highlight-box {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.08));
      border: 1px solid rgba(16, 185, 129, 0.25);
      border-radius: 10px;
      padding: 10px 14px;
      margin-bottom: 14px;
    }

    .benefit-amount-title {
      font-size: 11px;
      color: var(--accent-emerald);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.5px;
    }

    .benefit-amount-val {
      font-size: 14.5px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 2px;
    }

    .thematic-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 14px;
    }

    .thematic-pill {
      font-size: 11.5px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      padding: 3px 8px;
      border-radius: 6px;
      color: var(--text-secondary);
    }

    .card-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 14px;
      padding-top: 14px;
      border-top: 1px solid var(--border-subtle);
    }

    /* Badges */
    .badge-eligible {
      color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.35);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
    }

    .badge-warning {
      color: var(--accent-amber);
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
    }

    .badge-ineligible {
      color: var(--accent-rose);
      background: rgba(244, 63, 94, 0.15);
      border: 1px solid rgba(244, 63, 94, 0.35);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
    }

    /* Modals */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }

    .modal-overlay.active {
      display: flex;
    }

    .modal-content {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: 20px;
      max-width: 840px;
      width: 100%;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
    }

    .modal-header {
      padding: 20px 24px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-title {
      font-size: 19px;
      font-weight: 700;
      color: #ffffff;
    }

    .modal-body {
      padding: 24px;
      overflow-y: auto;
      font-size: 14px;
      line-height: 1.6;
    }

    .close-btn {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      font-size: 24px;
      cursor: pointer;
    }

    .close-btn:hover { color: #ffffff; }

    /* Checklist Card */
    .checklist-item {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 16px;
      margin-bottom: 12px;
    }

    .checklist-item-title {
      font-size: 15px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 4px;
    }

    .checklist-meta {
      font-size: 12.5px;
      color: var(--text-secondary);
      margin-top: 4px;
    }

    .checklist-meta strong {
      color: var(--accent-cyan);
    }
  </style>
</head>
<body>
  <div class="app-container">
    <!-- Header -->
    <header>
      <div class="brand-group">
        <div class="brand-logo">🎓</div>
        <div>
          <h1 class="brand-title">MadadgaarAI</h1>
          <div class="brand-subtitle">INDIAN STUDENT SCHOLARSHIP & RESEARCH GRANT INTELLIGENCE</div>
        </div>
      </div>
      <div class="header-actions">
        <div class="status-pill">
          <span class="status-dot"></span>
          <span id="headerStatusText">Live National Pipeline Online</span>
        </div>
        <button class="secondary-btn" onclick="triggerIngestion()">
          🔄 Refresh Schemas
        </button>
      </div>
    </header>

    <!-- Scam Shield Banner -->
    <div class="scam-shield-banner">
      <div class="scam-shield-content">
        <span class="scam-shield-badge">🛡️ Scam Shield</span>
        <span>
          <strong>100% Free Government Application Guarantee:</strong> All central (NSP), state (MahaDBT, UP), AICTE, and UGC scholarships are completely free to apply. Never pay any registration fees to unauthorized agents.
        </span>
      </div>
    </div>

    <!-- Hero Banner -->
    <div class="hero-banner">
      <div>
        <h2 class="hero-title">Zero-Knowledge <span>Scholarship & Grant Discovery</span></h2>
        <p class="hero-desc">
          Empowering Indian students & researchers to find guaranteed financial aid across Central NSP, AICTE, UGC, State Portals, DST, and CSR Trusts with automated document checklists and plain-language Hindi/Hinglish guides.
        </p>
      </div>
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-num" id="statTotal">21</div>
          <div class="stat-label">Total Schemes</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" id="statAgencies">8+</div>
          <div class="stat-label">Portals & Trusts</div>
        </div>
        <div class="stat-card">
          <div class="stat-num">₹ 50K-60L</div>
          <div class="stat-label">Financial Aid</div>
        </div>
        <div class="stat-card">
          <div class="stat-num" style="color: var(--accent-emerald);">100%</div>
          <div class="stat-label">Free & Verified</div>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-bar">
      <button class="tab-btn active" onclick="switchTab('student-hub')">
        🎓 Vidyarthi Scholarship Hub (विद्यार्थी छात्रवृत्ति)
      </button>
      <button class="tab-btn" onclick="switchTab('explore-grants')">
        🔍 All Schemes & Research Grants (सभी योजनाएं)
      </button>
      <button class="tab-btn" onclick="switchTab('faculty-matcher')">
        🎯 Faculty & Researcher Matcher
      </button>
    </div>

    <!-- TAB 1: Vidyarthi Scholarship Hub -->
    <div id="tab-student-hub">
      <div class="panel-card">
        <h3 style="font-size: 19px; font-weight: 700; margin-bottom: 6px; color: #ffffff;">
          🎯 "Am I Eligible?" Student Scholarship Wizard (पात्रता जांचें)
        </h3>
        <p style="color: var(--text-secondary); font-size: 14px; margin-bottom: 20px;">
          Select your state, education level, category, and family income to instantly discover all 100% eligible Central & State scholarships with required document checklists.
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 16px;">
          <div>
            <label style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">State of Domicile (मूल निवास)</label>
            <select id="stuState" class="select-box" style="margin-top: 6px;">
              <option value="All India">All India / Any State</option>
              <option value="Uttar Pradesh">Uttar Pradesh</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Bihar">Bihar</option>
              <option value="Rajasthan">Rajasthan</option>
              <option value="Madhya Pradesh">Madhya Pradesh</option>
              <option value="West Bengal">West Bengal</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Assam / North Eastern States">Assam / North Eastern States (NER)</option>
              <option value="Delhi NCR">Delhi NCR</option>
            </select>
          </div>

          <div>
            <label style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">Current Education Level (कक्षा / डिग्री)</label>
            <select id="stuLevel" class="select-box" style="margin-top: 6px;">
              <option value="UG - Engineering / Technology (B.Tech/B.E.)">UG - Engineering / Technology (B.Tech/B.E.)</option>
              <option value="Diploma / Polytechnic">Diploma / Polytechnic</option>
              <option value="UG - Medical / Paramedical (MBBS/BDS/B.Pharm/Nursing)">UG - Medical / Paramedical</option>
              <option value="UG - General (B.Sc / B.Com / B.A. / BBA / BCA)">UG - General (B.Sc/B.Com/B.A.)</option>
              <option value="Class 11-12 (Higher Secondary)">Class 11-12 (Higher Secondary)</option>
              <option value="Class 9-10 (Pre-Matric)">Class 9-10 (Pre-Matric)</option>
              <option value="Postgraduate (M.Tech / M.Sc / M.Com / M.A. / MBA / MCA)">Postgraduate (Master's Degree)</option>
              <option value="PhD / Doctoral Research">PhD / Doctoral Research</option>
            </select>
          </div>

          <div>
            <label style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">Social Category (जाति / वर्ग)</label>
            <select id="stuCategory" class="select-box" style="margin-top: 6px;">
              <option value="General / Open">General / Open</option>
              <option value="OBC (Non-Creamy Layer)">OBC (Non-Creamy Layer)</option>
              <option value="SC (Scheduled Caste)">SC (Scheduled Caste)</option>
              <option value="ST (Scheduled Tribe)">ST (Scheduled Tribe)</option>
              <option value="EWS (Economically Weaker Section)">EWS (Economically Weaker)</option>
              <option value="Minority (Muslim/Christian/Sikh/Buddhist/Jain/Parsi)">Minority (Muslim/Sikh/Christian/Jain)</option>
            </select>
          </div>

          <div>
            <label style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">Gender (लिंग)</label>
            <select id="stuGender" class="select-box" style="margin-top: 6px;">
              <option value="Female">Female (छात्रा)</option>
              <option value="Male">Male (छात्र)</option>
              <option value="Transgender">Transgender</option>
            </select>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 20px;">
          <div>
            <label style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">Annual Family Income (वार्षिक पारिवारिक आय)</label>
            <input type="number" id="stuIncome" class="input-box" style="margin-top: 6px;" value="200000" step="25000">
            <div style="display: flex; gap: 6px; margin-top: 6px;">
              <button class="secondary-btn" style="padding: 3px 8px; font-size: 11px;" onclick="setIncome(150000)">₹1.5L</button>
              <button class="secondary-btn" style="padding: 3px 8px; font-size: 11px;" onclick="setIncome(250000)">₹2.5L</button>
              <button class="secondary-btn" style="padding: 3px 8px; font-size: 11px;" onclick="setIncome(450000)">₹4.5L</button>
              <button class="secondary-btn" style="padding: 3px 8px; font-size: 11px;" onclick="setIncome(800000)">₹8.0L</button>
            </div>
          </div>

          <div>
            <label style="font-size: 12px; color: var(--text-secondary); font-weight: 600;">10th / 12th Marks (अंक %)</label>
            <input type="number" id="stuMarks" class="input-box" style="margin-top: 6px;" value="86" min="35" max="100">
          </div>

          <div style="display: flex; flex-direction: column; justify-content: center; gap: 8px;">
            <label style="display: flex; align-items: center; gap: 8px; font-size: 13px; cursor: pointer;">
              <input type="checkbox" id="stuSingleGirl">
              <span>Single Girl Child in Family (एकल पुत्री)</span>
            </label>
            <label style="display: flex; align-items: center; gap: 8px; font-size: 13px; cursor: pointer;">
              <input type="checkbox" id="stuPwd">
              <span>Differently Abled / PwD >=40% (दिव्यांग)</span>
            </label>
          </div>

          <div style="display: flex; align-items: flex-end;">
            <button class="primary-btn" style="width: 100%; height: 45px; justify-content: center;" onclick="runStudentMatch()">
              ⚡ Find My Scholarships (खोजें)
            </button>
          </div>
        </div>
      </div>

      <div id="studentResultsContainer">
        <!-- Results rendered here -->
      </div>
    </div>

    <!-- TAB 2: Explore All Grants & Opportunities -->
    <div id="tab-explore-grants" style="display: none;">
      <div class="panel-card">
        <div style="display: grid; grid-template-columns: 1fr auto auto; gap: 12px;">
          <input type="text" id="searchInput" class="input-box" placeholder="Search by scheme name or keywords (e.g. 'Pragati scholarship', 'AI research grant', 'women')..." onkeyup="if(event.key === 'Enter') runSearch()">
          <select id="agencyFilter" class="select-box" onchange="runSearch()">
            <option value="">All Portals & Agencies</option>
            <option value="NSP">NSP (National Scholarship)</option>
            <option value="AICTE">AICTE</option>
            <option value="UGC">UGC</option>
            <option value="State Govt">State Govt Portals</option>
            <option value="CSR / Foundation">CSR Foundations</option>
            <option value="DST">DST</option>
            <option value="ANRF/SERB">ANRF / SERB</option>
            <option value="CSIR">CSIR</option>
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

    <!-- TAB 3: Faculty Matcher -->
    <div id="tab-faculty-matcher" style="display: none;">
      <div class="panel-card">
        <h3 style="font-size: 18px; margin-bottom: 6px;">Researcher & Faculty Project Alignment</h3>
        <p style="color: var(--text-secondary); font-size: 13.5px; margin-bottom: 20px;">
          Paste your research abstract, grant proposal idea, or CV excerpt to match against DST, ANRF/SERB, CSIR, and DBT calls.
        </p>

        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 16px;">
          <div>
            <label style="font-size: 12px; color: var(--text-secondary);">Applicant Role</label>
            <select id="matchRole" class="select-box" style="margin-top: 4px;">
              <option value="Faculty / Principal Investigator">Faculty / Principal Investigator</option>
              <option value="Early Career Researcher">Early Career Researcher</option>
              <option value="Women Scientists">Women Scientists</option>
              <option value="PhD Scholars & Postdoctoral Fellows">PhD Scholars & Postdocs</option>
            </select>
          </div>
          <div>
            <label style="font-size: 12px; color: var(--text-secondary);">Age (Years)</label>
            <input type="number" id="matchAge" class="input-box" style="margin-top: 4px;" value="38">
          </div>
          <div>
            <label style="font-size: 12px; color: var(--text-secondary);">Highest Degree</label>
            <input type="text" id="matchDegree" class="input-box" style="margin-top: 4px;" value="Ph.D. in Computer Science">
          </div>
        </div>

        <div style="margin-bottom: 16px;">
          <label style="font-size: 12px; color: var(--text-secondary);">Research Proposal / Abstract</label>
          <textarea id="matchAbstract" class="input-box" rows="4" style="margin-top: 4px;" placeholder="Describe your scientific objectives, domain thrust, and methodologies..."></textarea>
        </div>

        <button class="primary-btn" onclick="runProfileMatch()">⚡ Align & Check Compliance</button>
      </div>

      <div id="matchResultsContainer"></div>
    </div>
  </div>

  <!-- Universal Modal for Document Checklist / Hinglish Guide / Proposal -->
  <div class="modal-overlay" id="modalOverlay" onclick="if(event.target === this) closeModal()">
    <div class="modal-content">
      <div class="modal-header">
        <div class="modal-title" id="modalTitle">Scheme Information</div>
        <button class="close-btn" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body" id="modalBody">
        <!-- Injected via JS -->
      </div>
    </div>
  </div>

  <script>
    let allFOAs = [];

    async function initApp() {
      await loadOpportunities();
      runStudentMatch(); // Auto-run initial student search
    }

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

    function setIncome(val) {
      document.getElementById('stuIncome').value = val;
    }

    function updateStats(items) {
      document.getElementById('statTotal').innerText = items.length;
    }

    function renderFOAGrid(items) {
      const grid = document.getElementById('foaGrid');
      if (!items || items.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">No opportunities found matching criteria.</div>';
        return;
      }

      grid.innerHTML = items.map(foa => {
        const agencyClean = foa.agency.replace('/', '_').replace(' ', '_');
        const budgetStr = foa.financials.raw_budget_text || (foa.financials.max_amount_inr ? '₹ ' + (foa.financials.max_amount_inr).toLocaleString() : 'As per norms');
        const deadlineStr = foa.deadlines.extended_closing_date || foa.deadlines.closing_date || (foa.deadlines.is_rolling ? 'Rolling Call' : 'Open');
        const applyLink = foa.direct_apply_url || foa.source_url;

        return `
          <div class="foa-card">
            <div>
              <div class="foa-card-header">
                <span class="agency-tag agency-${agencyClean}">${foa.agency}</span>
                <span style="font-size: 11.5px; color: var(--text-muted); font-family: var(--font-mono);">${foa.foa_id}</span>
              </div>
              <h3 class="foa-title">${foa.title}</h3>
              <p class="foa-summary">${foa.brief_summary}</p>
              
              <div class="benefit-highlight-box">
                <div class="benefit-amount-title">Financial Assistance</div>
                <div class="benefit-amount-val">${budgetStr}</div>
              </div>

              <div class="thematic-pills">
                ${(foa.thematic_areas || []).map(t => `<span class="thematic-pill">${t}</span>`).join('')}
              </div>
            </div>

            <div class="card-actions">
              <button class="direct-apply-btn" onclick="openNavGuide('${foa.foa_id}')">🚀 Apply & Portal Guide (आवेदन सेतु) ↗</button>
              <button class="secondary-btn" onclick="openDocChecklist('${foa.foa_id}')">📄 Documents</button>
              <button class="secondary-btn" onclick="openHinglishGuide('${foa.foa_id}')">🇮🇳 सरल गाइड</button>
              <button class="secondary-btn" onclick="downloadCalendar('${foa.foa_id}')">📅 .ICS</button>
              <a href="${applyLink}" target="_blank" rel="noopener noreferrer" class="secondary-btn">🌐 Official Portal ↗</a>
            </div>
          </div>
        `;
      }).join('');
    }

    async function runStudentMatch() {
      const container = document.getElementById('studentResultsContainer');
      container.innerHTML = '<div style="text-align: center; padding: 30px; color: var(--text-secondary);">⚡ Checking eligibility rules across Central, State & CSR schemes...</div>';

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
        renderStudentResults(results);
      } catch (err) {
        container.innerHTML = '<div style="color: var(--accent-rose); text-align: center;">Error evaluating scholarships.</div>';
      }
    }

    function renderStudentResults(results) {
      const container = document.getElementById('studentResultsContainer');
      if (!results || results.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 40px; color: var(--text-muted);">No student scholarships found.</div>';
        return;
      }

      const eligibleCount = results.filter(r => r.eligibility_status === 'ELIGIBLE' || r.eligibility_status === 'HIGH_PROBABILITY').length;

      let html = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
          <h4 style="font-size: 17px; font-weight: 700; color: #ffffff;">
            🎯 Recommended Scholarships for Your Profile (${eligibleCount} Eligible Schemes Found)
          </h4>
        </div>
        <div class="opportunities-grid">
      `;

      html += results.map(res => {
        const foa = res.foa;
        const agencyClean = foa.agency.replace('/', '_').replace(' ', '_');
        const badgeClass = res.eligibility_status === 'ELIGIBLE' ? 'badge-eligible' : (res.eligibility_status === 'HIGH_PROBABILITY' ? 'badge-eligible' : (res.eligibility_status === 'WARNING' ? 'badge-warning' : 'badge-ineligible'));
        const badgeText = res.eligibility_status === 'ELIGIBLE' ? '100% ELIGIBLE' : (res.eligibility_status === 'HIGH_PROBABILITY' ? 'HIGH PROBABILITY' : res.eligibility_status);

        const applyLink = res.direct_apply_url || foa.direct_apply_url || res.portal_url;
        const whatsappText = encodeURIComponent(`🎓 *Scholarship Alert: ${foa.title}*\n💰 Benefit: ${res.estimated_financial_benefit}\n🏛️ Official Portal: ${applyLink}\nCheck your eligibility on MadadgaarAI!`);

        return `
          <div class="foa-card">
            <div>
              <div class="foa-card-header">
                <span class="agency-tag agency-${agencyClean}">${foa.agency}</span>
                <span class="${badgeClass}">${badgeText} (${res.match_percentage}%)</span>
              </div>

              <h3 class="foa-title">${foa.title}</h3>
              <p class="foa-summary">${foa.brief_summary}</p>

              <div class="benefit-highlight-box">
                <div class="benefit-amount-title">Scholarship Benefit</div>
                <div class="benefit-amount-val">${res.estimated_financial_benefit}</div>
              </div>

              <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 12px; background: rgba(0,0,0,0.25); padding: 10px; border-radius: 8px;">
                ${res.match_reasons.map(r => `<div style="color: #cbd5e1; margin-bottom: 3px;">${r}</div>`).join('')}
                ${res.warning_reasons.map(w => `<div style="color: var(--accent-rose); margin-bottom: 3px;">${w}</div>`).join('')}
              </div>
            </div>

            <div class="card-actions">
              <button class="direct-apply-btn" onclick="openNavGuide('${foa.foa_id}')">🚀 Apply & Portal Guide (आवेदन सेतु) ↗</button>
              <button class="secondary-btn" onclick="openDocChecklist('${foa.foa_id}')">📄 Documents</button>
              <button class="secondary-btn" onclick="openHinglishGuide('${foa.foa_id}')">🇮🇳 सरल गाइड</button>
              <a href="https://api.whatsapp.com/send?text=${whatsappText}" target="_blank" class="whatsapp-btn">📲 Share</a>
              <a href="${applyLink}" target="_blank" rel="noopener noreferrer" class="secondary-btn">🌐 Portal ↗</a>
            </div>
          </div>
        `;
      }).join('');

      html += '</div>';
      container.innerHTML = html;
    }

    async function openDocChecklist(foaId) {
      const modal = document.getElementById('modalOverlay');
      const title = document.getElementById('modalTitle');
      const body = document.getElementById('modalBody');

      title.innerText = "📄 Mandatory Document Checklist & Guidance";
      body.innerHTML = '<div style="text-align: center; padding: 20px;">Loading requirements...</div>';
      modal.classList.add('active');

      try {
        const res = await fetch(`/api/student/scholarships/${foaId}/checklist`);
        const docs = await res.json();

        let html = `
          <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 12px; border-radius: 10px; margin-bottom: 18px; font-size: 13px; color: #a7f3d0;">
            ⚠️ <strong>Pro-Tip:</strong> Keep scanned copies of all these documents in PDF format under 200 KB before starting the online application.
          </div>
        `;

        html += docs.map((d, idx) => `
          <div class="checklist-item">
            <div class="checklist-item-title">${idx + 1}. ${d.document_name}</div>
            <div class="checklist-meta">🏛️ <strong>Issuing Authority:</strong> ${d.issuing_authority}</div>
            <div class="checklist-meta">📋 <strong>Validity & Rules:</strong> ${d.validity_and_rules}</div>
            <div class="checklist-meta">📍 <strong>How to Obtain:</strong> ${d.how_to_obtain}</div>
          </div>
        `).join('');

        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div style="color: var(--accent-rose);">Failed to load document checklist.</div>';
      }
    }

    async function openHinglishGuide(foaId) {
      const modal = document.getElementById('modalOverlay');
      const title = document.getElementById('modalTitle');
      const body = document.getElementById('modalBody');

      title.innerText = "🇮🇳 Saral Samjhauti (सरल भाषा में समझें)";
      body.innerHTML = '<div style="text-align: center; padding: 20px;">Loading guide...</div>';
      modal.classList.add('active');

      try {
        const res = await fetch(`/api/student/scholarships/${foaId}/hinglish`);
        const guide = await res.json();

        let html = `
          <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15)); border: 1px solid rgba(99, 102, 241, 0.3); padding: 16px; border-radius: 12px; margin-bottom: 18px;">
            <h4 style="color: #ffffff; margin-bottom: 6px; font-size: 16px;">👥 कौन-कौन अप्लाई कर सकता है? (Eligibility)</h4>
            <p style="color: #cbd5e1; font-size: 13.5px;">${guide.kaun_apply_kar_sakta_hai}</p>
          </div>

          <div style="background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 16px; border-radius: 12px; margin-bottom: 18px;">
            <h4 style="color: var(--accent-emerald); margin-bottom: 6px; font-size: 16px;">💰 कितने पैसे मिलेंगे? (Financial Support)</h4>
            <p style="color: #ffffff; font-size: 14px; font-weight: 600;">${guide.kitne_paise_milenge}</p>
          </div>

          <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-subtle); padding: 16px; border-radius: 12px; margin-bottom: 18px;">
            <h4 style="color: #ffffff; margin-bottom: 8px; font-size: 15px;">📑 क्या-क्या जरूरी डॉक्यूमेंट्स चाहिए?</h4>
            <ul style="list-style: none; padding-left: 0;">
              ${guide.zaruri_documents.map(d => `<li style="padding: 4px 0; color: #cbd5e1; font-size: 13px;">${d}</li>`).join('')}
            </ul>
          </div>

          <div style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); padding: 14px; border-radius: 10px; margin-bottom: 16px; font-size: 13px; color: #fde68a;">
            ${guide.aadhaar_seeding_warning}
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--border-subtle);">
            <div>
              <div style="font-size: 12px; color: var(--text-muted);">आधिकारिक पोर्टल:</div>
              <strong style="color: #ffffff;">${guide.official_portal_name}</strong>
            </div>
            <a href="${guide.official_portal_url}" target="_blank" class="primary-btn">
              पोर्टल पर जाएं ↗
            </a>
          </div>
        `;

          body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div style="color: var(--accent-rose);">Failed to load guide.</div>';
      }
    }

    async function openNavGuide(foaId) {
      const modal = document.getElementById('modalOverlay');
      const title = document.getElementById('modalTitle');
      const body = document.getElementById('modalBody');

      title.innerText = "🏛️ Official Government Application Gateway (सरकारी आवेदन सेतु)";
      body.innerHTML = '<div style="text-align: center; padding: 24px; color: var(--text-secondary);">⚡ Loading verified government portal instructions...</div>';
      modal.classList.add('active');

      try {
        const res = await fetch(`/api/foas/${foaId}`);
        const foa = await res.json();

        const steps = (foa.portal_navigation_steps && foa.portal_navigation_steps.length > 0) ? foa.portal_navigation_steps : [
          `1. Open the verified official portal (${foa.source_url}).`,
          "2. Complete student One Time Registration (OTR) with Aadhaar number & Mobile OTP.",
          `3. Search and select scheme: '${foa.title}'.`,
          "4. Fill academic details and upload required income/caste certificates.",
          "5. Verify your bank account has active Aadhaar-NPCI DBT mapping before submission."
        ];

        const applyUrl = foa.direct_apply_url || foa.source_url;
        const portalDomain = new URL(applyUrl).hostname;
        const whatsappText = encodeURIComponent(`🎓 *Scholarship Guidance: ${foa.title}*\n🏛️ Official Portal: ${applyUrl}\nCheck your eligibility on MadadgaarAI!`);

        let html = `
          <!-- Header Banner -->
          <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.18), rgba(99, 102, 241, 0.18)); border: 1px solid rgba(16, 185, 129, 0.4); padding: 18px; border-radius: 12px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="background: rgba(16, 185, 129, 0.25); color: #34d399; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.4);">
                🛡️ NIC / GOVT VERIFIED GATEWAY
              </span>
              <span style="font-size: 12px; color: var(--text-muted); font-family: var(--font-mono);">${foa.agency}</span>
            </div>
            <h3 style="color: #ffffff; font-size: 17px; margin-bottom: 6px; line-height: 1.4;">${foa.title}</h3>
            <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; color: #cbd5e1;">
              <span>🌐 Official Web Domain: <strong style="color: #60a5fa;">${portalDomain}</strong></span>
              <button class="secondary-btn" style="padding: 2px 8px; font-size: 11px;" onclick="navigator.clipboard.writeText('${applyUrl}'); alert('Official portal URL copied to clipboard!');">📋 Copy URL</button>
            </div>
          </div>

          <!-- Trust & Anti-Scam Notice -->
          <div style="background: rgba(16, 185, 129, 0.08); border: 1px dashed rgba(16, 185, 129, 0.35); padding: 12px 16px; border-radius: 10px; margin-bottom: 20px; font-size: 12.5px; color: #a7f3d0; display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 20px;">🛡️</span>
            <div>
              <strong>100% Free Government Application:</strong> Government scholarships never charge application fees. Apply only on official <code>.gov.in</code> / <code>.org</code> domains.
            </div>
          </div>

          <!-- Visual Click-by-Click Navigation Map -->
          <h4 style="color: #ffffff; font-size: 15px; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
            🧭 Step-by-Step Portal Navigation Path (बिना भटके सीधे फॉर्म भरें):
          </h4>
          <div style="display: flex; flex-direction: column; gap: 10px; margin-bottom: 22px;">
            ${steps.map((step, idx) => `
              <div style="background: rgba(15, 23, 42, 0.75); border: 1px solid var(--border-subtle); padding: 12px 16px; border-radius: 10px; font-size: 13.5px; color: #f1f5f9; display: flex; gap: 12px; align-items: flex-start;">
                <span style="background: var(--accent-indigo); color: #ffffff; border-radius: 50%; width: 24px; height: 24px; display: inline-flex; align-items: center; justify-content: center; font-size: 11.5px; font-weight: 700; flex-shrink: 0; margin-top: 1px;">${idx + 1}</span>
                <span style="line-height: 1.5;">${step.replace(/^[0-9]+\.\s*/, '')}</span>
              </div>
            `).join('')}
          </div>

          <!-- Pre-Flight Readiness Checklist -->
          <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid var(--border-subtle); padding: 16px; border-radius: 12px; margin-bottom: 24px;">
            <h5 style="color: #ffffff; font-size: 14px; margin-bottom: 10px;">📋 Pre-Flight Document Readiness Check (आवेदन शुरू करने से पहले जांचें):</h5>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12.5px; color: #cbd5e1;">
              <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                <input type="checkbox" checked disabled>
                <span>Aadhaar Card with Mobile OTP</span>
              </label>
              <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                <input type="checkbox" checked disabled>
                <span>Income Certificate (valid year)</span>
              </label>
              <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                <input type="checkbox" checked disabled>
                <span>Class 10th / 12th Marksheets</span>
              </label>
              <label style="display: flex; align-items: center; gap: 6px; cursor: pointer;">
                <input type="checkbox" checked disabled>
                <span>Bank Account Aadhaar-NPCI Seeded</span>
              </label>
            </div>
          </div>

          <!-- Action Footer Buttons -->
          <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 18px; border-top: 1px solid var(--border-subtle); flex-wrap: wrap; gap: 12px;">
            <a href="https://api.whatsapp.com/send?text=${whatsappText}" target="_blank" class="whatsapp-btn">
              📲 Share Guidance on WhatsApp
            </a>
            <a href="${applyUrl}" target="_blank" rel="noopener noreferrer" class="direct-apply-btn" style="padding: 11px 24px; font-size: 14.5px;">
              🚀 Launch Official Government Portal (पोर्टल खोलें) ↗
            </a>
          </div>
        `;

        body.innerHTML = html;
      } catch (err) {
        body.innerHTML = '<div style="color: var(--accent-rose);">Failed to load application bridge.</div>';
      }
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
          query: q || "scholarship and grants",
          agency_filter: agency || null,
          top_k: 15
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
      const age = parseInt(document.getElementById('matchAge').value) || 38;
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
      container.innerHTML = `
        <div class="opportunities-grid" style="margin-top: 20px;">
          ${results.map(m => `
            <div class="foa-card">
              <div>
                <div class="foa-card-header">
                  <span class="agency-tag agency-${m.foa.agency.replace('/', '_').replace(' ', '_')}">${m.foa.agency}</span>
                  <span class="badge-eligible">${(m.relevance_score * 100).toFixed(1)}% Match</span>
                </div>
                <h3 class="foa-title">${m.foa.title}</h3>
                <p class="foa-summary">${m.foa.brief_summary}</p>
                <div style="font-size: 12.5px; color: var(--text-secondary); margin-bottom: 10px;">
                  <strong>Compliance:</strong> ${m.compliance.reasons.join(' ')}
                </div>
              </div>
              <div class="card-actions">
                <button class="secondary-btn" onclick="draftProposal('${m.foa.foa_id}')">📝 Draft Proposal</button>
                <button class="secondary-btn" onclick="downloadCalendar('${m.foa.foa_id}')">📅 .ICS</button>
                <a href="${m.foa.source_url}" target="_blank" class="secondary-btn">🌐 Portal ↗</a>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    async function draftProposal(foaId) {
      const modal = document.getElementById('modalOverlay');
      const title = document.getElementById('modalTitle');
      const body = document.getElementById('modalBody');

      title.innerText = "📝 Proposal Skeleton & Budget Drafter";
      body.innerHTML = 'Generating tailored proposal skeleton...';
      modal.classList.add('active');

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
        <h4 style="color: var(--accent-indigo); margin-bottom: 12px;">${data.scheme_title} (${data.agency})</h4>
        <div style="margin-bottom: 20px;">
          <h5 style="color: #ffffff; margin-bottom: 8px;">Suggested Budget Allocation (MoF OM Norms)</h5>
          <div style="background: rgba(0,0,0,0.3); padding: 12px; border-radius: 8px;">
            ${Object.entries(data.suggested_budget_breakdown).map(([k, v]) => `<div><strong>${k}:</strong> ${v}</div>`).join('')}
          </div>
        </div>
        <div>
          <h5 style="color: #ffffff; margin-bottom: 8px;">Proposal Sections</h5>
          ${data.sections.map(sec => `
            <div style="margin-bottom: 16px;">
              <div style="font-weight: 600; color: #cbd5e1;">${sec.section_title}</div>
              <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 4px;">${sec.section_description}</div>
              <pre style="background: #0f172a; padding: 12px; border-radius: 8px; font-size: 12.5px; overflow-x: auto; color: #e2e8f0;"><code>${sec.drafted_content}</code></pre>
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
      statusText.innerText = 'Refreshing all schemas & pipelines...';
      const res = await fetch('/api/ingest/trigger', { method: 'POST' });
      const report = await res.json();
      statusText.innerText = `Ingested: ${report.new_opportunities_indexed} new`;
      await loadOpportunities();
      runStudentMatch();
    }

    function switchTab(tabId) {
      document.getElementById('tab-student-hub').style.display = tabId === 'student-hub' ? 'block' : 'none';
      document.getElementById('tab-explore-grants').style.display = tabId === 'explore-grants' ? 'block' : 'none';
      document.getElementById('tab-faculty-matcher').style.display = tabId === 'faculty-matcher' ? 'block' : 'none';

      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      event.currentTarget.classList.add('active');
    }

    function closeModal() {
      document.getElementById('modalOverlay').classList.remove('active');
    }

    // Initialize application
    initApp();
  </script>
</body>
</html>
"""
