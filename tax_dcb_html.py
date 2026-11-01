"""HTML template for the House Tax DCB Consolidation & PDF Report Viewer."""

TAX_PAGE_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Telangana ePanchayat · House Tax DCB Consolidation</title>
  <style>
    :root {
      color-scheme: light;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: #f4f7f6;
      color: #15332b;
      line-height: 1.5;
    }

    /* Navbar */
    .navbar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: #0c3829;
      color: white;
      box-shadow: 0 2px 12px rgba(0,0,0,0.15);
    }
    .nav-inner {
      max-width: 1240px;
      margin: 0 auto;
      padding: 0 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      height: 64px;
    }
    .nav-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: white;
    }
    .nav-brand-logo { font-size: 1.7rem; line-height: 1; }
    .nav-brand-titles { display: flex; flex-direction: column; }
    .nav-brand-sup {
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #8cd6b7;
    }
    .nav-brand-main {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: -0.01em;
      color: #ffffff;
    }
    .nav-menu { display: flex; align-items: center; gap: 10px; }
    .nav-link {
      color: #d4e8de;
      text-decoration: none;
      padding: 8px 14px;
      font-weight: 600;
      font-size: 0.92rem;
      border-radius: 8px;
      transition: all 0.15s;
    }
    .nav-link:hover { color: white; background: rgba(255,255,255,0.1); }
    .nav-link.active { color: white; background: #167451; }

    /* Layout */
    main {
      max-width: 1240px;
      margin: 24px auto 60px;
      padding: 0 20px;
    }

    /* Header Banner */
    .hero-strip {
      background: linear-gradient(135deg, #0d3d2c 0%, #167451 100%);
      color: white;
      border-radius: 16px;
      padding: 24px 28px;
      box-shadow: 0 10px 28px rgba(12,56,41,0.14);
      margin-bottom: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .hero-info h1 {
      margin: 4px 0 6px;
      font-size: 1.65rem;
      font-weight: 800;
      letter-spacing: -0.01em;
    }
    .hero-info p {
      margin: 0;
      font-size: 0.92rem;
      color: #d8f3e5;
    }
    .hero-badge {
      display: inline-block;
      background: rgba(255,255,255,0.15);
      border: 1px solid rgba(255,255,255,0.25);
      color: #c4f2dc;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 5px;
    }

    /* Filter & Controls Bar */
    .controls-card {
      background: white;
      border: 1px solid #d9e6df;
      border-radius: 14px;
      padding: 20px 24px;
      box-shadow: 0 6px 20px rgba(23,59,43,0.04);
      margin-bottom: 22px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .controls-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      align-items: flex-end;
    }
    .control-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .control-label {
      font-size: 0.84rem;
      font-weight: 700;
      color: #274b3f;
    }
    select, input[type="text"] {
      padding: 10px 12px;
      border: 1px solid #c2d6cc;
      border-radius: 8px;
      font-size: 0.92rem;
      color: #15332b;
      background: #fafcfb;
      font-family: inherit;
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    select:focus, input[type="text"]:focus {
      border-color: #167451;
      box-shadow: 0 0 0 3px rgba(22, 116, 81, 0.15);
      background: white;
    }
    .actions-bar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
      padding-top: 14px;
      border-top: 1px solid #edf4f0;
    }

    /* Buttons */
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 10px 16px;
      font-size: 0.88rem;
      font-weight: 700;
      border-radius: 8px;
      text-decoration: none;
      cursor: pointer;
      border: none;
      font-family: inherit;
      transition: all 0.15s;
    }
    .btn-primary { background: #167451; color: white; }
    .btn-primary:hover { background: #115d40; }
    .btn-secondary { background: #eaf5ef; color: #167451; border: 1px solid #b9ddcb; }
    .btn-secondary:hover { background: #d7ede1; }
    .btn-pdf { background: #0b5ed7; color: white; }
    .btn-pdf:hover { background: #0948a5; }
    .btn-outline { background: white; color: #2e5445; border: 1px solid #cfe0d7; }
    .btn-outline:hover { background: #f3f9f6; }

    /* KPI Summary Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 14px;
      margin-bottom: 22px;
    }
    .kpi-card {
      background: white;
      border: 1px solid #d9e6df;
      border-radius: 12px;
      padding: 16px 18px;
      box-shadow: 0 4px 16px rgba(23,59,43,0.04);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .kpi-title {
      font-size: 0.74rem;
      font-weight: 700;
      color: #627f74;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .kpi-val {
      font-size: 1.45rem;
      font-weight: 800;
      color: #123d2e;
      line-height: 1.2;
    }
    .kpi-sub {
      font-size: 0.76rem;
      color: #7a948b;
      margin-top: 4px;
    }
    .kpi-card.kpi-highlight {
      border: 2px solid #167451;
      background: #fbfdfc;
    }
    .kpi-card.kpi-highlight .kpi-val {
      color: #167451;
    }

    /* Content Tabs */
    .tabs-wrap {
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      border-bottom: 2px solid #dbe6e0;
    }
    .tab-item {
      padding: 10px 18px;
      font-size: 0.94rem;
      font-weight: 700;
      color: #557267;
      background: transparent;
      border: none;
      border-radius: 8px 8px 0 0;
      cursor: pointer;
      transition: all 0.15s;
      border-bottom: 3px solid transparent;
      margin-bottom: -2px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .tab-item:hover { color: #167451; background: #eef6f2; }
    .tab-item.active {
      color: #167451;
      border-bottom: 3px solid #167451;
      background: #eaf5ef;
    }

    .tab-pane { display: none; }
    .tab-pane.active { display: block; }

    /* PDF Viewer Container */
    .pdf-viewer-card {
      background: white;
      border: 1px solid #d9e6df;
      border-radius: 14px;
      padding: 16px;
      box-shadow: 0 8px 24px rgba(23,59,43,0.06);
    }
    .pdf-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      margin-bottom: 12px;
      border-bottom: 1px solid #eef3f0;
      flex-wrap: wrap;
      gap: 10px;
    }
    .pdf-toolbar-info {
      font-size: 0.9rem;
      font-weight: 700;
      color: #1c4b3a;
    }
    .pdf-iframe {
      width: 100%;
      height: 820px;
      border: 1px solid #cfe0d7;
      border-radius: 8px;
      background: #525659;
    }

    /* Table Card */
    .table-card {
      background: white;
      border: 1px solid #d9e6df;
      border-radius: 14px;
      padding: 20px;
      box-shadow: 0 8px 24px rgba(23,59,43,0.05);
      overflow-x: auto;
    }
    .table-header-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      flex-wrap: wrap;
      gap: 10px;
    }
    .table-title {
      font-size: 1.05rem;
      font-weight: 750;
      color: #15332b;
      margin: 0;
    }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }
    table.data-table th, table.data-table td {
      padding: 9px 12px;
      border: 1px solid #e0ebe5;
    }
    table.data-table th {
      background: #f2f7f4;
      color: #1b4938;
      font-weight: 700;
      white-space: nowrap;
    }
    table.data-table tbody tr:hover {
      background: #f8fcfa;
    }
    .num-cell {
      text-align: right;
      font-variant-numeric: tabular-nums;
    }
    .center-cell {
      text-align: center;
    }
    .pct-line-col {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 3px;
      width: 62px;
      margin: 0 auto;
    }
    .pct-line-val {
      font-weight: 800;
      font-size: 0.82rem;
      color: #111827;
      line-height: 1.1;
    }
    .pct-line-track {
      width: 100%;
      height: 5px;
      background: #e2e8f0;
      border-radius: 3px;
      overflow: hidden;
    }
    .pct-line-fill {
      height: 100%;
      border-radius: 3px;
      transition: width 0.35s ease;
    }
    .pct-meter {
      position: relative;
      width: 68px;
      height: 22px;
      margin: 0 auto;
      background: #edf2ef;
      border: 1px solid #cbd5cf;
      border-radius: 5px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: inset 0 1px 2px rgba(0,0,0,0.06);
    }
    .pct-meter-fill {
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      border-radius: 4px;
      transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .pct-meter-text {
      position: relative;
      z-index: 2;
      font-weight: 800;
      font-size: 0.78rem;
      color: #111827;
      text-shadow: 0 0 3px rgba(255, 255, 255, 0.95), 0 0 1px #ffffff;
      letter-spacing: -0.01em;
    }
    .pct-badge {
      display: inline-block;
      min-width: 42px;
      padding: 2px 7px;
      border-radius: 5px;
      font-weight: 750;
      font-size: 0.82rem;
      color: white;
      text-align: center;
      background: #16874e;
    }
    .total-row {
      font-weight: 750;
      background: #eef6f2 !important;
      border-top: 2px solid #167451;
    }

    /* Pagination */
    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 14px;
      margin-top: 12px;
      border-top: 1px solid #edf4f0;
      font-size: 0.86rem;
      color: #557267;
      flex-wrap: wrap;
      gap: 10px;
    }
    .pagination-btns {
      display: flex;
      gap: 6px;
    }
    .page-btn {
      padding: 5px 12px;
      border: 1px solid #cfe0d7;
      background: white;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.84rem;
      font-weight: 600;
      color: #167451;
    }
    .page-btn:disabled {
      opacity: 0.45;
      cursor: not-allowed;
    }

    /* Status Banner */
    .status-alert {
      display: none;
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 14px;
      font-size: 0.88rem;
      font-weight: 600;
    }
    .status-alert.info { display: block; background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
    .status-alert.success { display: block; background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
    .status-alert.error { display: block; background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }

    footer {
      border-top: 1px solid #dce6e1;
      margin-top: 60px;
      padding: 22px 20px;
      text-align: center;
      color: #5a7369;
      font-size: 0.84rem;
      background: white;
    }

    @media (max-width: 768px) {
      .hero-strip { padding: 18px; }
      .hero-info h1 { font-size: 1.3rem; }
      .pdf-iframe { height: 500px; }
    }
  </style>
</head>
<body>
  <!-- Navbar -->
  <header class="navbar">
    <div class="nav-inner">
      <a class="nav-brand" href="/">
        <span class="nav-brand-logo">🏛️</span>
        <div class="nav-brand-titles">
          <span class="nav-brand-sup">Government of Telangana</span>
          <span class="nav-brand-main">PR &amp; RD Analytics Portal</span>
        </div>
      </a>
      <nav class="nav-menu">
        <a class="nav-link" href="/">🏠 Home</a>
        <a class="nav-link" href="/reports/ps-attendance">📋 PS Attendance</a>
        <a class="nav-link active" href="/reports/tax-dcb">💰 Tax DCB Consolidation</a>
      </nav>
    </div>
  </header>

  <main>
    <!-- Hero Banner -->
    <section class="hero-strip">
      <div class="hero-info">
        <span class="hero-badge">ePanchayat Departmental Live Data</span>
        <h1>Gram Panchayat Wise DCB Status &amp; PDF Report</h1>
        <p>Consolidated Demand, Collection, and Balance (DCB) for House Tax across all Mandals and Gram Panchayats</p>
      </div>
    </section>

    <div id="status-box" class="status-alert"></div>

    <!-- Controls Bar -->
    <section class="controls-card">
      <div class="controls-grid">
        <div class="control-group">
          <label class="control-label" for="district-select">1. Select District <span style="color:#c92a2a">*</span></label>
          <select id="district-select">
            <option value="" selected disabled>-- Select District --</option>
          </select>
        </div>

        <div class="control-group">
          <label class="control-label" for="mandal-select">2. Filter by Mandal</label>
          <select id="mandal-select" disabled>
            <option value="all">-- Select District First --</option>
          </select>
        </div>

        <div class="control-group">
          <label class="control-label" for="search-input">3. Instant Search GP or Mandal</label>
          <input type="text" id="search-input" placeholder="Type Panchayat or Mandal name...">
        </div>

        <div class="control-group" style="justify-content: flex-end;">
          <button type="button" id="btn-generate-report" class="btn btn-primary" style="padding: 10px 22px; font-weight:700; font-size:0.95rem; height:42px; display:flex; align-items:center; justify-content:center; gap:8px;" onclick="onGenerateReportClick()">
            <span>⚡</span> Generate Report
          </button>
        </div>
      </div>

      <div class="actions-bar" id="actions-bar" style="display: none;">
        <a id="btn-download-pdf" href="#" class="btn btn-pdf" download>
          📥 Download PDF Report
        </a>
        <a id="btn-download-excel" href="#" class="btn btn-secondary" download>
          📊 Download Consolidated Excel (.xlsx)
        </a>
        <a id="btn-download-csv" href="#" class="btn btn-outline" download>
          📥 Download CSV
        </a>
        <button type="button" id="btn-refresh" class="btn btn-outline" onclick="refreshLiveData()">
          🔄 Refresh Live from Portal
        </button>
      </div>
    </section>

    <!-- KPI Summary Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-title">Total Mandals</span>
        <div class="kpi-val" id="kpi-mandals">--</div>
        <div class="kpi-sub" id="kpi-district-name">Khammam District</div>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Total Gram Panchayats</span>
        <div class="kpi-val" id="kpi-gps">--</div>
        <div class="kpi-sub" id="kpi-assessments">-- Assessments</div>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Total Demand</span>
        <div class="kpi-val" id="kpi-demand">₹ --</div>
        <div class="kpi-sub" id="kpi-demand-breakdown">Arrear: -- | Current: --</div>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Total Collection</span>
        <div class="kpi-val" id="kpi-collection">₹ --</div>
        <div class="kpi-sub" id="kpi-coll-breakdown">Arrear: -- | Current: --</div>
      </div>
      <div class="kpi-card">
        <span class="kpi-title">Balance Outstanding</span>
        <div class="kpi-val" id="kpi-balance">₹ --</div>
        <div class="kpi-sub" id="kpi-bal-breakdown">Arrear: -- | Current: --</div>
      </div>
      <div class="kpi-card kpi-highlight">
        <span class="kpi-title">Overall Collection %</span>
        <div class="kpi-val" id="kpi-pct">-- %</div>
        <div class="kpi-sub">Target: 100%</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-wrap">
      <button type="button" class="tab-item active" onclick="switchTab('pdf')">
        📄 Official PDF Report Viewer
      </button>
      <button type="button" class="tab-item" onclick="switchTab('abstract')">
        🏛️ Mandal Wise Consolidated Abstract
      </button>
      <button type="button" class="tab-item" onclick="switchTab('detail')">
        📋 Gram Panchayat Wise Detailed DCB Table
      </button>
    </div>

    <!-- PANE 1: Embedded PDF Viewer -->
    <div id="pane-pdf" class="tab-pane active">
      <div class="pdf-viewer-card">
        <div class="pdf-toolbar" id="pdf-toolbar" style="display: none;">
          <div class="pdf-toolbar-info">
            Official Departmental Landscape Format · Generated for <span id="pdf-dist-label">--</span>
          </div>
          <div style="display:flex; gap:8px;">
            <a id="btn-fullscreen-pdf" href="#" target="_blank" class="btn btn-pdf" style="padding:6px 12px; font-size:0.82rem;">
              ↗ Open in Full Screen / Native Viewer
            </a>
            <button type="button" class="btn btn-outline" style="padding:6px 12px; font-size:0.82rem;" onclick="reloadPdfViewer()">
              🔄 Reload PDF
            </button>
          </div>
        </div>
        <div id="pdf-placeholder" style="text-align:center; padding:70px 20px; color:#557267;">
          <div style="font-size:3.2rem; margin-bottom:12px;">🏛️</div>
          <h3 style="font-size:1.3rem; font-weight:700; margin-bottom:8px; color:#173b2b;">Please Select a District</h3>
          <p style="max-width:520px; margin:0 auto; font-size:0.92rem; line-height:1.5; color:#557267;">
            Select a <strong>District</strong> from the controls above (and optionally a specific <strong>Mandal</strong>), then click the <strong>⚡ Generate Report</strong> button to load the official PDF report and consolidated DCB data.
          </p>
        </div>
        <iframe id="pdf-frame" class="pdf-iframe" style="display:none;" src="about:blank"></iframe>
      </div>
    </div>

    <!-- PANE 2: Mandal Abstract Table -->
    <div id="pane-abstract" class="tab-pane">
      <div class="table-card">
        <div class="table-header-row">
          <h2 class="table-title">Mandal Wise DCB Abstract (Consolidated Summary)</h2>
          <span style="font-size:0.86rem; color:#557267;" id="mandal-count-label">-- Mandals</span>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th class="center-cell" style="width:50px;">S.No</th>
              <th>Mandal Name</th>
              <th class="num-cell">Total GPs</th>
              <th class="num-cell">Assessments</th>
              <th class="num-cell">Demand Arrear (₹)</th>
              <th class="num-cell">Demand Current (₹)</th>
              <th class="num-cell">Demand Total (₹)</th>
              <th class="num-cell">Collection Arrear (₹)</th>
              <th class="num-cell">Collection Current (₹)</th>
              <th class="num-cell">Collection Total (₹)</th>
              <th class="num-cell">Balance Arrear (₹)</th>
              <th class="num-cell">Balance Current (₹)</th>
              <th class="num-cell">Balance Total (₹)</th>
              <th class="center-cell">% Coll</th>
            </tr>
          </thead>
          <tbody id="mandal-table-body">
            <tr><td colspan="14" class="center-cell" style="padding:28px; color:#557267;">Please select a District and click <strong>⚡ Generate Report</strong> to display Mandal summary.</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- PANE 3: Gram Panchayat Detail Table -->
    <div id="pane-detail" class="tab-pane">
      <div class="table-card">
        <div class="table-header-row">
          <h2 class="table-title">Gram Panchayat Wise Detailed DCB Table</h2>
          <span style="font-size:0.86rem; color:#557267;" id="gp-count-label">-- GPs found</span>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th class="center-cell" style="width:45px;">S.No</th>
              <th>Mandal</th>
              <th>Gram Panchayat</th>
              <th class="num-cell">Assessments</th>
              <th class="num-cell">Demand Arrear (₹)</th>
              <th class="num-cell">Demand Current (₹)</th>
              <th class="num-cell">Demand Total (₹)</th>
              <th class="num-cell">Collection Arrear (₹)</th>
              <th class="num-cell">Collection Current (₹)</th>
              <th class="num-cell">Collection Total (₹)</th>
              <th class="num-cell">Balance Total (₹)</th>
              <th class="center-cell">% Coll</th>
            </tr>
          </thead>
          <tbody id="gp-table-body">
            <tr><td colspan="12" class="center-cell" style="padding:28px; color:#557267;">Please select a District and click <strong>⚡ Generate Report</strong> to display Gram Panchayat details.</td></tr>
          </tbody>
        </table>

        <div class="pagination-bar">
          <span id="page-info">Showing 0-0 of 0</span>
          <div class="pagination-btns">
            <button type="button" class="page-btn" id="btn-prev" onclick="changePage(-1)">← Previous</button>
            <button type="button" class="page-btn" id="btn-next" onclick="changePage(1)">Next →</button>
          </div>
        </div>
      </div>
    </div>
  </main>

  <footer>
    Executive Analytics &amp; Monitoring Portal · Telangana Panchayat Raj &amp; Rural Development
  </footer>

  <script>
    let allRecords = [];
    let filteredRecords = [];
    let mandalAbstract = [];
    let currentPage = 1;
    const PAGE_SIZE = 50;

    function formatInr(val) {
      if (val === null || val === undefined || isNaN(val)) return '0';
      const n = Math.round(Number(val));
      return n.toLocaleString('en-IN');
    }

    function getGradientColor(pct) {
      pct = Math.max(0, Math.min(100, Number(pct) || 0));
      let r, g, b;
      if (pct <= 50) {
        const t = pct / 50;
        r = Math.round(220 + t * (234 - 220));
        g = Math.round(38 + t * (179 - 38));
        b = Math.round(38 + t * (8 - 38));
      } else {
        const t = (pct - 50) / 50;
        r = Math.round(234 + t * (22 - 234));
        g = Math.round(179 + t * (163 - 179));
        b = Math.round(8 + t * (74 - 8));
      }
      const lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
      const textCol = lum > 0.55 ? '#000000' : '#FFFFFF';
      return { bg: `rgb(${r}, ${g}, ${b})`, text: textCol };
    }

    function renderPctCell(pctVal) {
      const p = Math.max(0, Math.min(100, Math.round(Number(pctVal) || 0)));
      const { bg } = getGradientColor(p);
      const fillW = p > 0 ? Math.max(p, 2) : 0;
      return `<div class="pct-line-col" title="${p}% Collection">
        <span class="pct-line-val">${p}%</span>
        <div class="pct-line-track">
          <div class="pct-line-fill" style="width: ${fillW}%; background: ${bg};"></div>
        </div>
      </div>`;
    }

    function switchTab(tab) {
      document.querySelectorAll('.tab-item').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      event.currentTarget.classList.add('active');
      document.getElementById('pane-' + tab).classList.add('active');
    }

    function reloadPdfViewer() {
      const dist = document.getElementById('district-select').value;
      if (!dist) return;
      const mandal = document.getElementById('mandal-select').value;
      const encDist = encodeURIComponent(dist);
      const isAllMandals = !mandal || mandal === 'all';
      const mandalParam = isAllMandals ? '' : `&mandal=${encodeURIComponent(mandal)}`;
      const frame = document.getElementById('pdf-frame');
      frame.src = `/api/tax/report.pdf?district=${encDist}${mandalParam}&t=${Date.now()}`;
    }

    // Load available districts from API (no auto-selection)
    async function initDistricts() {
      try {
        const res = await fetch('/api/tax/districts');
        const districts = await res.json();
        const sel = document.getElementById('district-select');
        sel.innerHTML = '<option value="" selected disabled>-- Select District --</option>';

        districts.forEach(d => {
          const opt = document.createElement('option');
          opt.value = d.district;
          opt.textContent = `${d.district} (${d.gps_count} GPs)`;
          sel.appendChild(opt);
        });

        const mandalSel = document.getElementById('mandal-select');
        mandalSel.innerHTML = '<option value="all">-- Select District First --</option>';
        mandalSel.disabled = true;

        showStatus('Please select a District and click Generate Report to begin.', 'info');
      } catch (err) {
        showStatus('Error loading districts: ' + err.message, 'error');
      }
    }

    function updateActionLinks() {
      const dist = document.getElementById('district-select').value;
      if (!dist) return;
      const mandal = document.getElementById('mandal-select').value;
      const encDist = encodeURIComponent(dist);
      const isAllMandals = !mandal || mandal === 'all';
      const mandalParam = isAllMandals ? '' : `&mandal=${encodeURIComponent(mandal)}`;

      const pdfUrl = `/api/tax/report.pdf?district=${encDist}${mandalParam}`;
      const pdfDlUrl = `/api/tax/download-pdf?district=${encDist}${mandalParam}`;
      const excelUrl = `/api/tax/download?district=${encDist}${mandalParam}&format=xlsx`;
      const csvUrl = `/api/tax/download?district=${encDist}${mandalParam}&format=csv`;

      const viewPdfBtn = document.getElementById('btn-view-pdf');
      if (viewPdfBtn) viewPdfBtn.href = pdfUrl;
      const dlPdfBtn = document.getElementById('btn-download-pdf');
      if (dlPdfBtn) dlPdfBtn.href = pdfDlUrl;
      const dlExcelBtn = document.getElementById('btn-download-excel');
      if (dlExcelBtn) dlExcelBtn.href = excelUrl;
      const dlCsvBtn = document.getElementById('btn-download-csv');
      if (dlCsvBtn) dlCsvBtn.href = csvUrl;
      const fsPdfBtn = document.getElementById('btn-fullscreen-pdf');
      if (fsPdfBtn) fsPdfBtn.href = pdfUrl;

      const label = isAllMandals ? `${dist} District` : `${mandal} Mandal (${dist} District)`;
      document.getElementById('pdf-dist-label').textContent = label;
      document.getElementById('pdf-frame').src = pdfUrl;
    }

    async function onDistrictChanged() {
      const dist = document.getElementById('district-select').value;
      const mandalSel = document.getElementById('mandal-select');
      if (!dist) {
        mandalSel.innerHTML = '<option value="all">-- Select District First --</option>';
        mandalSel.disabled = true;
        return;
      }
      mandalSel.disabled = false;
      await loadMandals(dist);
      showStatus(`Selected ${dist} District. Click '⚡ Generate Report' to view report and analytics.`, 'info');
    }

    async function onGenerateReportClick() {
      const dist = document.getElementById('district-select').value;
      if (!dist) {
        showStatus('Please select a District first.', 'error');
        document.getElementById('district-select').focus();
        return;
      }
      const mandal = document.getElementById('mandal-select').value;

      const newUrl = new URL(window.location);
      newUrl.searchParams.set('district', dist);
      if (mandal && mandal !== 'all') {
        newUrl.searchParams.set('mandal', mandal);
      } else {
        newUrl.searchParams.delete('mandal');
      }
      window.history.replaceState({}, '', newUrl);

      // Reveal action toolbar & PDF frame
      const actionsBar = document.getElementById('actions-bar');
      if (actionsBar) actionsBar.style.display = 'flex';

      const pdfToolbar = document.getElementById('pdf-toolbar');
      if (pdfToolbar) pdfToolbar.style.display = 'flex';
      const placeholder = document.getElementById('pdf-placeholder');
      if (placeholder) placeholder.style.display = 'none';
      const frame = document.getElementById('pdf-frame');
      if (frame) frame.style.display = 'block';

      updateActionLinks();
      await loadData(dist);
    }

    async function loadMandals(dist) {
      try {
        const res = await fetch(`/api/tax/mandals?district=${encodeURIComponent(dist)}`);
        const mandals = await res.json();
        const sel = document.getElementById('mandal-select');
        sel.innerHTML = '<option value="all">-- All Mandals (Consolidated) --</option>';
        mandals.forEach(m => {
          const opt = document.createElement('option');
          opt.value = m;
          opt.textContent = m;
          sel.appendChild(opt);
        });
      } catch (err) {
        console.error('Error loading mandals', err);
      }
    }

    async function loadData(dist) {
      try {
        showStatus(`Loading consolidated data for ${dist}...`, 'info');
        const mandal = document.getElementById('mandal-select').value;
        const res = await fetch(`/api/tax/data?district=${encodeURIComponent(dist)}&mandal=${encodeURIComponent(mandal)}`);
        const data = await res.json();

        // Summary KPI
        const s = data.summary;
        document.getElementById('kpi-mandals').textContent = s.total_mandals;
        document.getElementById('kpi-district-name').textContent = s.district + (s.mandal !== 'All Mandals' ? ` · ${s.mandal}` : ' District');
        document.getElementById('kpi-gps').textContent = s.total_gps;
        document.getElementById('kpi-assessments').textContent = formatInr(s.total_assessments) + ' Assessments';
        document.getElementById('kpi-demand').textContent = '₹ ' + formatInr(s.total_demand);
        document.getElementById('kpi-demand-breakdown').textContent = `Arrear: ₹ ${formatInr(s.demand_arrear)} | Current: ₹ ${formatInr(s.demand_current)}`;
        document.getElementById('kpi-collection').textContent = '₹ ' + formatInr(s.total_collection);
        document.getElementById('kpi-coll-breakdown').textContent = `Arrear: ₹ ${formatInr(s.collection_arrear)} | Current: ₹ ${formatInr(s.collection_current)}`;
        document.getElementById('kpi-balance').textContent = '₹ ' + formatInr(s.total_balance);
        document.getElementById('kpi-bal-breakdown').textContent = `Arrear: ₹ ${formatInr(s.balance_arrear)} | Current: ₹ ${formatInr(s.balance_current)}`;
        document.getElementById('kpi-pct').textContent = s.overall_percentage + ' %';

        allRecords = data.records || [];
        mandalAbstract = data.mandal_abstract || [];
        filteredRecords = [...allRecords];

        renderMandalTable(mandalAbstract, s);
        applyFilter();
        hideStatus();
      } catch (err) {
        showStatus('Error fetching data: ' + err.message, 'error');
      }
    }

    function renderMandalTable(abstractList, summary) {
      const tbody = document.getElementById('mandal-table-body');
      document.getElementById('mandal-count-label').textContent = `${abstractList.length} Mandals Consolidated`;

      if (!abstractList || abstractList.length === 0) {
        tbody.innerHTML = '<tr><td colspan="14" class="center-cell" style="padding:20px;">No mandal records found.</td></tr>';
        return;
      }

      // Sort Mandal-wise consolidated abstract in ascending order based on % Collection
      abstractList.sort((a, b) => (Number(a.percentage) || 0) - (Number(b.percentage) || 0));

      let html = '';
      abstractList.forEach((m, idx) => {
        const mPct = Math.round(m.percentage);
        const { bg, text } = getGradientColor(mPct);
        html += `<tr>
          <td class="center-cell">${idx + 1}</td>
          <td><strong>${m.mandal}</strong></td>
          <td class="num-cell">${m.total_gps}</td>
          <td class="num-cell">${formatInr(m.assessments)}</td>
          <td class="num-cell">${formatInr(m.demand_arrear)}</td>
          <td class="num-cell">${formatInr(m.demand_current)}</td>
          <td class="num-cell"><strong>${formatInr(m.demand_total)}</strong></td>
          <td class="num-cell">${formatInr(m.collection_arrear)}</td>
          <td class="num-cell">${formatInr(m.collection_current)}</td>
          <td class="num-cell"><strong>${formatInr(m.collection_total)}</strong></td>
          <td class="num-cell">${formatInr(m.balance_arrear)}</td>
          <td class="num-cell">${formatInr(m.balance_current)}</td>
          <td class="num-cell"><strong>${formatInr(m.balance_total)}</strong></td>
          <td class="center-cell">${renderPctCell(mPct)}</td>
        </tr>`;
      });

      // Total row
      const totColor = getGradientColor(summary.overall_percentage);
      html += `<tr class="total-row">
        <td class="center-cell">Σ</td>
        <td><strong>Total (${summary.district})</strong></td>
        <td class="num-cell">${summary.total_gps}</td>
        <td class="num-cell">${formatInr(summary.total_assessments)}</td>
        <td class="num-cell">${formatInr(summary.demand_arrear)}</td>
        <td class="num-cell">${formatInr(summary.demand_current)}</td>
        <td class="num-cell"><strong>${formatInr(summary.total_demand)}</strong></td>
        <td class="num-cell">${formatInr(summary.collection_arrear)}</td>
        <td class="num-cell">${formatInr(summary.collection_current)}</td>
        <td class="num-cell"><strong>${formatInr(summary.total_collection)}</strong></td>
        <td class="num-cell">${formatInr(summary.balance_arrear)}</td>
        <td class="num-cell">${formatInr(summary.balance_current)}</td>
        <td class="num-cell"><strong>${formatInr(summary.total_balance)}</strong></td>
        <td class="center-cell">${renderPctCell(summary.overall_percentage)}</td>
      </tr>`;

      tbody.innerHTML = html;
    }

    function applyFilter() {
      const q = document.getElementById('search-input').value.toLowerCase().trim();
      const mandalSel = document.getElementById('mandal-select').value.toLowerCase();

      filteredRecords = allRecords.filter(r => {
        const matchesMandal = (mandalSel === 'all') || (r.mandal.toLowerCase() === mandalSel);
        const matchesQuery = !q || r.panchayat.toLowerCase().includes(q) || r.mandal.toLowerCase().includes(q);
        return matchesMandal && matchesQuery;
      });

      currentPage = 1;
      renderGpTable();
    }

    function renderGpTable() {
      const tbody = document.getElementById('gp-table-body');
      const total = filteredRecords.length;
      document.getElementById('gp-count-label').textContent = `${total} Gram Panchayats`;

      if (total === 0) {
        tbody.innerHTML = '<tr><td colspan="12" class="center-cell" style="padding:20px;">No Gram Panchayats matching search.</td></tr>';
        document.getElementById('page-info').textContent = 'Showing 0-0 of 0';
        document.getElementById('btn-prev').disabled = true;
        document.getElementById('btn-next').disabled = true;
        return;
      }

      const start = (currentPage - 1) * PAGE_SIZE;
      const end = Math.min(start + PAGE_SIZE, total);
      const pageRows = filteredRecords.slice(start, end);

      let html = '';
      pageRows.forEach((r, idx) => {
        const pct = Math.round(r.calc_percentage || 0);
        const { bg, text } = getGradientColor(pct);
        html += `<tr>
          <td class="center-cell">${start + idx + 1}</td>
          <td>${r.mandal}</td>
          <td><strong>${r.panchayat}</strong></td>
          <td class="num-cell">${formatInr(r.assessments)}</td>
          <td class="num-cell">${formatInr(r.demand_arrear)}</td>
          <td class="num-cell">${formatInr(r.demand_current)}</td>
          <td class="num-cell"><strong>${formatInr(r.demand_total)}</strong></td>
          <td class="num-cell">${formatInr(r.collection_arrear)}</td>
          <td class="num-cell">${formatInr(r.collection_current)}</td>
          <td class="num-cell"><strong>${formatInr(r.collection_total)}</strong></td>
          <td class="num-cell"><strong>${formatInr(r.balance_total)}</strong></td>
          <td class="center-cell">${renderPctCell(pct)}</td>
        </tr>`;
      });

      tbody.innerHTML = html;
      document.getElementById('page-info').textContent = `Showing ${start + 1}-${end} of ${total}`;
      document.getElementById('btn-prev').disabled = currentPage <= 1;
      document.getElementById('btn-next').disabled = end >= total;
    }

    function changePage(delta) {
      currentPage += delta;
      renderGpTable();
    }

    async function refreshLiveData() {
      const btn = document.getElementById('btn-refresh');
      btn.disabled = true;
      btn.textContent = '⏳ Refreshing from epanchayat...';
      showStatus('Downloading latest live DCB data from ePanchayat Telangana portal...', 'info');

      try {
        const res = await fetch('/api/tax/refresh', { method: 'POST' });
        const resData = await res.json();
        showStatus(`Fresh data synced! Total ${resData.total_gps} GPs updated across state.`, 'success');
        const dist = document.getElementById('district-select').value;
        await loadData(dist);
        reloadPdfViewer();
      } catch (err) {
        showStatus('Failed to refresh data: ' + err.message, 'error');
      } finally {
        btn.disabled = false;
        btn.textContent = '🔄 Refresh Live from Portal';
      }
    }

    function showStatus(msg, type = 'info') {
      const el = document.getElementById('status-box');
      el.className = 'status-alert ' + type;
      el.textContent = msg;
    }
    function hideStatus() {
      const el = document.getElementById('status-box');
      el.className = 'status-alert';
      el.textContent = '';
    }

    document.getElementById('district-select').addEventListener('change', onDistrictChanged);
    document.getElementById('mandal-select').addEventListener('change', () => {
      const dist = document.getElementById('district-select').value;
      if (dist) {
        showStatus('Mandal selected. Click ⚡ Generate Report to view report.', 'info');
      }
    });
    document.getElementById('search-input').addEventListener('input', applyFilter);

    // Initial run
    initDistricts();
  </script>
</body>
</html>
"""
