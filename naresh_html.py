"""HTML template for the Naresh Automated DSR & Attendance Report Page (/naresh)."""

NARESH_PAGE_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Naresh Portal | Automated DSR & Attendance Analytics | Khammam District</title>
  <style>
    :root {
      color-scheme: light;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
      --primary: #0c3829;
      --primary-light: #165b43;
      --accent: #d97706;
      --accent-hover: #b45309;
      --bg: #f3f6f4;
      --card-bg: #ffffff;
      --text: #132a22;
      --text-muted: #4e6b60;
      --border: #d4e0da;
      --success: #059669;
      --warning: #d97706;
      --danger: #dc2626;
      --info: #2563eb;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
    }

    /* Navbar */
    .navbar {
      position: sticky;
      top: 0;
      z-index: 1000;
      background: var(--primary);
      color: white;
      box-shadow: 0 3px 14px rgba(0,0,0,0.18);
    }
    .nav-inner {
      max-width: 1280px;
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
      font-weight: 700;
      font-size: 1.05rem;
    }
    .nav-brand-badge {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      color: #1a1a1a;
      font-size: 0.72rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .nav-links {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    .nav-link {
      color: #d1fae5;
      text-decoration: none;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 0.9rem;
      font-weight: 500;
      transition: all 0.2s;
    }
    .nav-link:hover {
      background: rgba(255,255,255,0.1);
      color: white;
    }
    .nav-link.active {
      background: rgba(255,255,255,0.18);
      color: #fbbf24;
      font-weight: 700;
    }

    /* Container */
    .container {
      max-width: 1280px;
      margin: 24px auto;
      padding: 0 20px;
    }

    /* Hero Banner */
    .hero-card {
      background: linear-gradient(135deg, #0c3829 0%, #165b43 65%, #1e7e5c 100%);
      color: white;
      padding: 30px;
      border-radius: 14px;
      box-shadow: 0 8px 24px rgba(12, 56, 41, 0.2);
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
    }
    .hero-card::after {
      content: "";
      position: absolute;
      right: -40px;
      top: -40px;
      width: 220px;
      height: 220px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(251, 191, 36, 0.15) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-eyebrow {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.8rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #fbbf24;
      font-weight: 700;
      margin-bottom: 8px;
    }
    .hero-title {
      font-size: 1.85rem;
      font-weight: 800;
      margin: 0 0 8px 0;
      letter-spacing: -0.5px;
    }
    .hero-subtitle {
      font-size: 1rem;
      color: #e6f4ee;
      margin: 0 0 20px 0;
      max-width: 800px;
      line-height: 1.45;
    }
    .hero-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      border-radius: 999px;
      font-size: 0.8rem;
      font-weight: 600;
    }
    .badge-live {
      background: rgba(16, 185, 129, 0.25);
      border: 1px solid #10b981;
      color: #a7f3d0;
    }
    .badge-info {
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: #f3f4f6;
    }
    .badge-portal {
      background: rgba(251, 191, 36, 0.2);
      border: 1px solid #fbbf24;
      color: #fef3c7;
    }
    .live-dot {
      width: 8px;
      height: 8px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* Action Buttons Bar */
    .actions-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 20px;
      padding-top: 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 11px 22px;
      border-radius: 8px;
      font-size: 0.95rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      border: none;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn-gold {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      color: #1a1a1a;
      box-shadow: 0 4px 12px rgba(217, 119, 6, 0.35);
    }
    .btn-gold:hover {
      background: linear-gradient(135deg, #fbbf24, #f59e0b);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(217, 119, 6, 0.45);
    }
    .btn-white {
      background: white;
      color: var(--primary);
      box-shadow: 0 3px 10px rgba(0,0,0,0.12);
    }
    .btn-white:hover {
      background: #f8fafc;
      transform: translateY(-2px);
    }
    .btn-outline {
      background: rgba(255, 255, 255, 0.1);
      color: white;
      border: 1px solid rgba(255, 255, 255, 0.4);
    }
    .btn-outline:hover {
      background: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
    }

    /* Metrics Grid */
    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .metric-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      display: flex;
      flex-direction: column;
      position: relative;
      transition: transform 0.2s;
    }
    .metric-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    }
    .metric-card.accent {
      border-top: 4px solid var(--primary);
    }
    .metric-card.success {
      border-top: 4px solid var(--success);
    }
    .metric-card.warning {
      border-top: 4px solid var(--warning);
    }
    .metric-card.info {
      border-top: 4px solid var(--info);
    }
    .metric-card.danger {
      border-top: 4px solid var(--danger);
    }
    .metric-label {
      font-size: 0.8rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }
    .metric-value {
      font-size: 2rem;
      font-weight: 800;
      color: var(--text);
      line-height: 1.1;
      margin-bottom: 4px;
    }
    .metric-sub {
      font-size: 0.82rem;
      color: var(--text-muted);
    }

    /* PDF Preview Section */
    .viewer-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 3px 12px rgba(0,0,0,0.05);
      margin-bottom: 24px;
      overflow: hidden;
    }
    .viewer-header {
      padding: 16px 20px;
      background: #f8fafc;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }
    .viewer-title {
      font-weight: 700;
      font-size: 1.05rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .viewer-actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }
    .btn-sm {
      padding: 7px 14px;
      font-size: 0.85rem;
      border-radius: 6px;
    }
    .pdf-frame {
      width: 100%;
      height: 750px;
      border: none;
      background: #525659;
    }

    /* Mandals Table */
    .table-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 3px 12px rgba(0,0,0,0.05);
      margin-bottom: 24px;
      overflow: hidden;
    }
    .table-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .table-title {
      font-weight: 700;
      font-size: 1.05rem;
    }
    .search-input {
      padding: 8px 14px;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-size: 0.9rem;
      width: 240px;
      outline: none;
    }
    .search-input:focus {
      border-color: var(--primary);
    }
    .table-responsive {
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }
    th {
      background: #f8fafc;
      text-align: left;
      padding: 12px 16px;
      font-weight: 700;
      color: var(--text-muted);
      border-bottom: 2px solid var(--border);
    }
    td {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      color: var(--text);
    }
    tr:hover td {
      background: #f9fbf9;
    }
    .text-right { text-align: right; }
    .text-center { text-align: center; }
    .pct-bar-wrap {
      width: 90px;
      height: 7px;
      background: #e2e8f0;
      border-radius: 4px;
      display: inline-block;
      overflow: hidden;
      vertical-align: middle;
      margin-left: 8px;
    }
    .pct-bar-fill {
      height: 100%;
      background: var(--success);
      border-radius: 4px;
    }

    /* Footer */
    footer {
      text-align: center;
      padding: 30px 20px;
      color: var(--text-muted);
      font-size: 0.85rem;
      border-top: 1px solid var(--border);
      margin-top: 40px;
    }
  </style>
</head>
<body>

  <!-- Navigation Bar -->
  <header class="navbar">
    <div class="nav-inner">
      <a class="nav-brand" href="/naresh">
        <span>🏛️ Telangana Panchayat Raj</span>
        <span class="nav-brand-badge">Naresh Portal</span>
      </a>
      <nav class="nav-links">
        <a class="nav-link" href="/#home">Home</a>
        <a class="nav-link" href="/#reports-district">District Monitoring</a>
        <a class="nav-link" href="/#reports-mandal">Mandal Monitoring</a>
        <a class="nav-link" href="/reports/tax-dcb">House Tax DCB</a>
        <a class="nav-link active" href="/naresh">⚡ Naresh Feed</a>
      </nav>
    </div>
  </header>

  <!-- Main Content -->
  <main class="container">

    <!-- Hero Card -->
    <section class="hero-card">
      <div class="hero-eyebrow">
        <span>Khammam District Panchayat Office</span>
        <span>•</span>
        <span>Office ID: 3698</span>
      </div>
      <h1 class="hero-title">Naresh Automated DSR & Attendance Report</h1>
      <p class="hero-subtitle">
        Live automated daily report generated directly from <strong>e-Panchayat Telangana (EPTS) Portal</strong> exports. 
        Zero file upload required — view your official 7-section monitoring PDF, analyze mandal stats, or download instantly.
      </p>

      <div class="hero-badges">
        <span class="badge badge-live">
          <span class="live-dot"></span>
          Live Automated Feed Active
        </span>
        <span class="badge badge-portal">
          🏛️ Source: EPTS (DPOA3698)
        </span>
        <span class="badge badge-info" id="report-date-badge">
          📅 Target Date: Loading...
        </span>
        <span class="badge badge-info">
          🛡️ Khammam District (571 GPs)
        </span>
      </div>

      <div class="actions-bar">
        <button type="button" class="btn btn-gold" onclick="loadAndScrollToViewer()">
          👁️ View Official District PDF
        </button>
        <a id="btn-download-pdf" class="btn btn-white" href="/api/naresh/download" target="_blank">
          📥 Download Official PDF
        </a>
        <a class="btn btn-outline" href="/#reports-district?auto=true">
          📊 Open in Main Dashboard (No Upload Required)
        </a>
        <a class="btn btn-outline" href="/#reports-mandal?auto=true">
          📋 Mandal Level Report
        </a>
      </div>
    </section>

    <!-- Metrics Cards Grid -->
    <section class="metrics-grid" id="metrics-container">
      <div class="metric-card accent">
        <div class="metric-label">Total Gram Panchayats</div>
        <div class="metric-value" id="val-total-gps">571</div>
        <div class="metric-sub">Khammam District Total</div>
      </div>
      <div class="metric-card success">
        <div class="metric-label">Attendance Submitted</div>
        <div class="metric-value" id="val-att-submitted">560</div>
        <div class="metric-sub" id="sub-att-pct">98.1% Compliance</div>
      </div>
      <div class="metric-card info">
        <div class="metric-label">DSR Entered</div>
        <div class="metric-value" id="val-dsr-entered">404</div>
        <div class="metric-sub" id="sub-dsr-pct">70.8% of Eligible (415)</div>
      </div>
      <div class="metric-card success">
        <div class="metric-label">Present Before 9 AM</div>
        <div class="metric-value" id="val-before-9">85</div>
        <div class="metric-sub">Timely PS Attendance</div>
      </div>
      <div class="metric-card warning">
        <div class="metric-label">On Leave / Training</div>
        <div class="metric-value" id="val-on-leave">145</div>
        <div class="metric-sub">74 Leave + 71 Training</div>
      </div>
      <div class="metric-card danger">
        <div class="metric-label">Attendance Pending</div>
        <div class="metric-value" id="val-pending">11</div>
        <div class="metric-sub">Requires Follow-up</div>
      </div>
    </section>

    <!-- PDF Viewer Card -->
    <section class="viewer-card" id="viewer-section">
      <div class="viewer-header">
        <div class="viewer-title">
          <span>📄</span>
          <span>Official 7-Section District Attendance &amp; DSR Monitoring PDF</span>
        </div>
        <div class="viewer-actions">
          <a class="btn btn-gold btn-sm" href="/api/naresh/download" target="_blank">
            📥 Download PDF
          </a>
          <button type="button" class="btn btn-white btn-sm" onclick="refreshViewer()">
            🔄 Reload Preview
          </button>
        </div>
      </div>
      <iframe id="pdf-frame" class="pdf-frame" src="/api/naresh/view"></iframe>
    </section>

    <!-- Mandal Breakdown Table Card -->
    <section class="table-card">
      <div class="table-header">
        <div class="table-title">Mandal-wise Attendance &amp; DSR Performance (20 Mandals)</div>
        <input type="text" id="mandal-search" class="search-input" placeholder="Search Mandal..." onkeyup="filterMandals()">
      </div>
      <div class="table-responsive">
        <table id="mandals-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Mandal Name</th>
              <th class="text-center">Total GPs</th>
              <th class="text-center">Submitted</th>
              <th class="text-center">Attendance %</th>
              <th class="text-center">Before 9 AM</th>
              <th class="text-center">On Leave / Meet</th>
              <th class="text-center">Pending</th>
              <th class="text-center">DSR Entered</th>
            </tr>
          </thead>
          <tbody id="mandals-tbody">
            <tr><td colspan="9" class="text-center" style="padding: 24px;">Loading live mandal performance data...</td></tr>
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <footer>
    Government of Telangana &bull; Panchayat Raj &amp; Rural Employment Department<br>
    Automated DSR Monitoring Service &bull; Khammam District (Office ID: 3698)
  </footer>

  <script>
    let reportData = null;

    async function loadNareshData() {
      try {
        const res = await fetch('/api/naresh/data');
        if (!res.ok) throw new Error('Failed to load data');
        reportData = await res.json();
        
        // Update Badges & Date
        if (reportData.report_date) {
          document.getElementById('report-date-badge').innerText = `📅 Date: ${reportData.report_date}`;
        }

        // Update Totals
        const t = reportData.totals || {};
        document.getElementById('val-total-gps').innerText = t.unique_gps || 571;
        document.getElementById('val-att-submitted').innerText = t.attendance_submitted || 560;
        const pct = t.overall_attendance_pct ? Number(t.overall_attendance_pct).toFixed(1) : '98.1';
        document.getElementById('sub-att-pct').innerText = `${pct}% Compliance`;
        document.getElementById('val-dsr-entered').innerText = t.dsr_entered || 404;
        const dsrElig = t.dsr_eligible || 415;
        const dsrPct = dsrElig > 0 ? ((t.dsr_entered / dsrElig) * 100).toFixed(1) : '0';
        document.getElementById('sub-dsr-pct').innerText = `${dsrPct}% of Eligible (${dsrElig})`;
        document.getElementById('val-before-9').innerText = t.before_9 || 85;
        const leaveTotal = (t.on_leave || 74) + (t.meeting_training || 71);
        document.getElementById('val-on-leave').innerText = leaveTotal;
        document.getElementById('val-pending').innerText = t.pending || 11;

        // Render Mandals Table
        renderMandals(reportData.mandal_rows || []);
      } catch (e) {
        console.error('Error loading Naresh automated feed:', e);
      }
    }

    function renderMandals(rows) {
      const tbody = document.getElementById('mandals-tbody');
      if (!rows || rows.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">No mandal rows available</td></tr>';
        return;
      }
      let html = '';
      rows.forEach((r, idx) => {
        const pct = r.attendance_pct ? Number(r.attendance_pct).toFixed(1) : '0';
        html += `<tr>
          <td>${idx + 1}</td>
          <td><strong>${r.mandal || ''}</strong></td>
          <td class="text-center">${r.total_gps || 0}</td>
          <td class="text-center">${r.submitted || 0}</td>
          <td class="text-center">
            <strong>${pct}%</strong>
            <span class="pct-bar-wrap"><span class="pct-bar-fill" style="width: ${Math.min(100, pct)}%"></span></span>
          </td>
          <td class="text-center" style="color: var(--success); font-weight: 600;">${r.before_9 || 0}</td>
          <td class="text-center">${(r.on_leave || 0) + (r.meeting_training || 0)}</td>
          <td class="text-center" style="color: ${r.pending > 0 ? 'var(--danger)' : 'var(--text-muted)'}; font-weight: ${r.pending > 0 ? '700' : '400'};">${r.pending || 0}</td>
          <td class="text-center" style="color: var(--info); font-weight: 600;">${r.dsr_entered || 0}</td>
        </tr>`;
      });
      tbody.innerHTML = html;
    }

    function filterMandals() {
      const q = document.getElementById('mandal-search').value.toLowerCase();
      const trs = document.querySelectorAll('#mandals-tbody tr');
      trs.forEach(tr => {
        const text = tr.innerText.toLowerCase();
        tr.style.display = text.includes(q) ? '' : 'none';
      });
    }

    function loadAndScrollToViewer() {
      document.getElementById('viewer-section').scrollIntoView({ behavior: 'smooth' });
    }

    function refreshViewer() {
      const frame = document.getElementById('pdf-frame');
      frame.src = '/api/naresh/view?t=' + Date.now();
    }

    window.addEventListener('DOMContentLoaded', loadNareshData);
  </script>
</body>
</html>
"""
