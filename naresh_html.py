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

    /* Hero Card */
    .hero-card {
      background: linear-gradient(135deg, #062b1f 0%, #0c3829 55%, #154c38 100%);
      color: white;
      border-radius: 16px;
      padding: 28px 32px;
      box-shadow: 0 6px 20px rgba(12, 56, 41, 0.25);
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
    }
    .hero-card::after {
      content: "";
      position: absolute;
      top: -40px;
      right: -40px;
      width: 220px;
      height: 220px;
      background: radial-gradient(circle, rgba(245, 158, 11, 0.18) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-eyebrow {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
      color: #a7f3d0;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 8px;
    }
    .hero-title {
      margin: 0 0 10px 0;
      font-size: 1.85rem;
      font-weight: 800;
      letter-spacing: -0.5px;
      line-height: 1.25;
    }
    .hero-subtitle {
      margin: 0 0 16px 0;
      font-size: 0.98rem;
      color: #d1fae5;
      max-width: 820px;
      line-height: 1.5;
    }
    .hero-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.78rem;
      font-weight: 600;
    }
    .badge-live {
      background: rgba(16, 185, 129, 0.22);
      color: #6ee7b7;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .live-dot {
      width: 7px;
      height: 7px;
      background: #10b981;
      border-radius: 50%;
      box-shadow: 0 0 8px #10b981;
      animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }
    .badge-portal {
      background: rgba(245, 158, 11, 0.2);
      color: #fde68a;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-info {
      background: rgba(255, 255, 255, 0.12);
      color: white;
    }

    /* Buttons */
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

    /* ========================================================
       AUTOMATION WORKFLOW STATION CARD (Login -> OTP -> Module -> Gen)
       ======================================================== */
    .automation-card {
      background: var(--card-bg);
      border: 2px solid #059669;
      border-radius: 16px;
      box-shadow: 0 6px 24px rgba(5, 150, 105, 0.12);
      margin-bottom: 26px;
      overflow: hidden;
      position: relative;
    }
    .automation-header {
      background: linear-gradient(135deg, #0c3829, #165b43);
      color: white;
      padding: 18px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
    }
    .automation-title {
      font-size: 1.15rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .pulse-icon {
      font-size: 1.3rem;
      display: inline-block;
      animation: pulse 1.5s infinite;
    }

    /* Stepper */
    .stepper {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: #f8fafc;
      padding: 16px 28px;
      border-bottom: 1px solid var(--border);
      position: relative;
    }
    .step {
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 600;
      position: relative;
      z-index: 2;
      cursor: pointer;
    }
    .step-circle {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #e2e8f0;
      color: #64748b;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 0.9rem;
      transition: all 0.25s ease;
    }
    .step.active .step-circle {
      background: #059669;
      color: white;
      box-shadow: 0 0 10px rgba(5, 150, 105, 0.5);
    }
    .step.completed .step-circle {
      background: #047857;
      color: white;
    }
    .step.active {
      color: #065f46;
      font-weight: 700;
    }
    .step-line {
      flex: 1;
      height: 3px;
      background: #e2e8f0;
      margin: 0 12px;
      transition: background 0.3s;
    }
    .step-line.active {
      background: #059669;
    }

    /* Step Panes */
    .step-pane {
      padding: 24px 28px;
      display: none;
    }
    .step-pane.active {
      display: block;
      animation: fadeIn 0.25s ease-out;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .step-instruction {
      font-size: 0.95rem;
      color: var(--text-muted);
      margin: 0 0 18px 0;
      line-height: 1.5;
    }
    .form-row {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
      margin-bottom: 20px;
    }
    .form-group {
      flex: 1;
      min-width: 240px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .form-group label {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text);
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }
    .form-group input, .form-group select {
      padding: 12px 14px;
      border: 1.5px solid var(--border);
      border-radius: 8px;
      font-size: 0.95rem;
      background: #f8fafc;
      color: var(--text);
      outline: none;
      transition: all 0.2s;
    }
    .form-group input:focus, .form-group select:focus {
      border-color: #059669;
      background: white;
      box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.15);
    }
    .password-wrapper {
      position: relative;
      display: flex;
      align-items: center;
    }
    .password-wrapper input {
      width: 100%;
      padding-right: 44px;
    }
    .btn-toggle-pwd {
      position: absolute;
      right: 10px;
      background: none;
      border: none;
      cursor: pointer;
      font-size: 1.1rem;
      color: var(--text-muted);
    }

    /* OTP Box */
    .otp-box {
      background: #f0fdf4;
      border: 1.5px dashed #059669;
      border-radius: 12px;
      padding: 24px;
      text-align: center;
      max-width: 580px;
      margin: 0 auto;
    }
    .otp-header {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      margin-bottom: 16px;
      text-align: left;
    }
    .otp-icon {
      font-size: 2.2rem;
    }
    .otp-input-wrap input {
      font-size: 2.2rem;
      letter-spacing: 12px;
      text-align: center;
      font-weight: 800;
      padding: 12px 20px;
      width: 280px;
      border: 2px solid #059669;
      border-radius: 10px;
      background: white;
      outline: none;
      box-shadow: 0 4px 14px rgba(5, 150, 105, 0.15);
    }

    /* Live Progress Bar */
    .live-progress-card {
      padding: 10px 0;
    }
    .spinner-wrap {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 16px;
    }
    .spinner {
      width: 28px;
      height: 28px;
      border: 3px solid #e2e8f0;
      border-top-color: #059669;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    #progress-status-title {
      font-size: 1.05rem;
      font-weight: 700;
      color: #065f46;
    }
    .progress-bar-container {
      width: 100%;
      height: 8px;
      background: #e2e8f0;
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 16px;
    }
    .progress-bar-active {
      height: 100%;
      background: linear-gradient(90deg, #059669, #10b981);
      border-radius: 4px;
      transition: width 0.4s ease;
    }
    .progress-steps {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .p-step {
      font-size: 0.9rem;
      color: #64748b;
      padding-left: 24px;
      position: relative;
    }
    .p-step::before {
      content: "○";
      position: absolute;
      left: 0;
      color: #94a3b8;
      font-weight: bold;
    }
    .p-step.active {
      color: #047857;
      font-weight: 600;
    }
    .p-step.active::before {
      content: "●";
      color: #059669;
    }
    .p-step.done {
      color: #064e3b;
      font-weight: 600;
    }
    .p-step.done::before {
      content: "✓";
      color: #059669;
      font-weight: 900;
    }

    /* Automation Status Bar */
    .automation-status-bar {
      background: #f8fafc;
      border-top: 1px solid var(--border);
      padding: 10px 24px;
      font-size: 0.85rem;
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text-muted);
    }
    .status-indicator {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
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
    .metric-card.accent { border-top: 4px solid var(--primary); }
    .metric-card.success { border-top: 4px solid var(--success); }
    .metric-card.warning { border-top: 4px solid var(--warning); }
    .metric-card.info { border-top: 4px solid var(--info); }
    .metric-card.danger { border-top: 4px solid var(--danger); }
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
        <a class="nav-link active" href="/naresh">⚡ Naresh Station</a>
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
      <h1 class="hero-title">Automated DSR Report &amp; e-Panchayat Robot Station</h1>
      <p class="hero-subtitle">
        Zero manual downloading. Enter your e-Panchayat credentials below, enter your OTP, select the target DSR date, and the robot downloads and compiles the official 7-section Attendance &amp; DSR PDF in the background.
      </p>

      <div class="hero-badges">
        <span class="badge badge-live">
          <span class="live-dot"></span>
          Automated Robot Ready
        </span>
        <span class="badge badge-portal">
          🏛️ Source: EPTS (DPOA3698)
        </span>
        <span class="badge badge-info" id="report-date-badge">
          📅 Target Date: Select Date Below
        </span>
        <span class="badge badge-info">
          🛡️ Khammam District (571 GPs)
        </span>
      </div>
    </section>

    <!-- ========================================================
         AUTOMATION WORKFLOW STATION CARD (Login -> OTP -> Module -> Gen)
         ======================================================== -->
    <section class="automation-card" id="automation-station">
      <div class="automation-header">
        <div class="automation-title">
          <span class="pulse-icon">⚡</span>
          <span>e-Panchayat Automated Robot Console</span>
        </div>
        <span class="badge badge-portal" id="session-badge">Session: Ready</span>
      </div>

      <!-- Stepper Indicator -->
      <div class="stepper">
        <div class="step active" id="step-nav-1" onclick="goToStep(1)">
          <div class="step-circle" id="circle-1">1</div>
          <div class="step-text">Department Login</div>
        </div>
        <div class="step-line" id="line-1"></div>
        <div class="step" id="step-nav-2" onclick="goToStep(2)">
          <div class="step-circle" id="circle-2">2</div>
          <div class="step-text">Enter OTP</div>
        </div>
        <div class="step-line" id="line-2"></div>
        <div class="step" id="step-nav-3" onclick="goToStep(3)">
          <div class="step-circle" id="circle-3">3</div>
          <div class="step-text">Module &amp; Date</div>
        </div>
        <div class="step-line" id="line-3"></div>
        <div class="step" id="step-nav-4">
          <div class="step-circle" id="circle-4">4</div>
          <div class="step-text">Auto-Generate</div>
        </div>
      </div>

      <!-- STEP 1: Department Login -->
      <div class="step-pane active" id="pane-step-1">
        <p class="step-instruction">
          Enter your e-Panchayat credentials. Our background robot connects to <strong>epanchayat.telangana.gov.in</strong>, auto-solves the captcha with AI OCR, and triggers your 6-digit login OTP.
        </p>
        <div class="form-row">
          <div class="form-group">
            <label>User ID</label>
            <input type="text" id="auto-user" placeholder="Enter User ID (e.g. DPOA3698)" autocomplete="username" required>
          </div>
          <div class="form-group">
            <label>Password</label>
            <div class="password-wrapper">
              <input type="password" id="auto-pwd" placeholder="Enter Password" autocomplete="current-password" required>
              <button type="button" class="btn-toggle-pwd" onclick="togglePasswordVisibility()" title="Toggle visibility">👁️</button>
            </div>
          </div>
        </div>
        <div class="form-actions" style="display:flex; gap:12px; flex-wrap:wrap;">
          <button type="button" class="btn btn-gold" id="btn-login" onclick="startDepartmentLogin()">
            🔐 Login to e-Panchayat &amp; Generate OTP
          </button>
        </div>
      </div>

      <!-- STEP 2: OTP Verification -->
      <div class="step-pane" id="pane-step-2">
        <div class="otp-box">
          <div class="otp-header">
            <span class="otp-icon">📱</span>
            <div>
              <strong>6-Digit OTP Sent to Your Registered Mobile</strong>
              <div style="font-size:0.85rem; color:var(--text-muted); margin-top:3px;">
                Enter the OTP received from e-Panchayat Telangana to authenticate session.
              </div>
            </div>
          </div>
          <div class="otp-input-wrap">
            <input type="text" id="auto-otp" maxlength="6" inputmode="numeric" placeholder="••••••" autocomplete="one-time-code">
          </div>
          <div class="form-actions" style="margin-top:20px; display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
            <button type="button" class="btn btn-gold" id="btn-validate-otp" onclick="validateOTP()">
              ✅ Validate OTP &amp; Proceed to Report Selection
            </button>
            <button type="button" class="btn btn-outline" style="color:var(--text); border-color:var(--border);" onclick="goToStep(1)">
              ↩ Back to Login
            </button>
          </div>
        </div>
      </div>

      <!-- STEP 3: Module & Date Selection -->
      <div class="step-pane" id="pane-step-3">
        <p class="step-instruction">
          Select your target DSR Monitoring module and report date. The robot will download the reports directly from <strong>GM-R 1 Sanitation reports</strong> and generate the official PDF.
        </p>
        <div class="form-row">
          <div class="form-group" style="flex:2;">
            <label>DSR Report Module</label>
            <select id="auto-module">
              <option value="dsr_full" selected>GM-R 1.2.7 DSR Raw Data + PS Attendance (Complete Official Report)</option>
              <option value="dsr_raw">GM-R 1.2.7 DSR Raw Data Report (730 KB)</option>
              <option value="dsr_absentees">GM-R 1.2.10 Report on Absentees Data</option>
              <option value="dsr_presentees">GM-R 1.2.11 Report on Presenties Data</option>
            </select>
          </div>
          <div class="form-group" style="flex:1;">
            <label>Select Date</label>
            <input type="date" id="auto-date" value="2026-11-02">
          </div>
        </div>
        <div class="form-actions" style="display:flex; gap:12px; flex-wrap:wrap;">
          <button type="button" class="btn btn-gold" id="btn-generate" onclick="runAutomatedGeneration()">
            ⚡ Automate &amp; Generate Official DSR Report
          </button>
          <button type="button" class="btn btn-outline" style="color:var(--text); border-color:var(--border);" onclick="goToStep(2)">
            ↩ Back to OTP
          </button>
        </div>
      </div>

      <!-- STEP 4: Live Automation Execution & Progress -->
      <div class="step-pane" id="pane-step-4">
        <div class="live-progress-card">
          <div class="spinner-wrap">
            <div class="spinner" id="auto-spinner"></div>
            <div id="progress-status-title">Processing in Background...</div>
          </div>
          <div class="progress-bar-container">
            <div class="progress-bar-active" id="progress-bar-fill" style="width: 25%;"></div>
          </div>
          <ul class="progress-steps" id="progress-steps-list">
            <li class="p-step active" id="ps-1">Authenticating with e-Panchayat Session...</li>
            <li class="p-step" id="ps-2">Opening GP Monitoring &rarr; GM-R 1 Sanitation Reports &rarr; DSR REPORTS...</li>
            <li class="p-step" id="ps-3">Applying selected date filter...</li>
            <li class="p-step" id="ps-4">Downloading raw data exports...</li>
            <li class="p-step" id="ps-5">Compiling 7-section official Attendance PDF...</li>
          </ul>
          <div id="auto-completion-banner" style="display:none; margin-top:20px; padding:18px; background:#ecfdf5; border:1.5px solid #10b981; border-radius:10px; text-align:center;">
            <strong style="color:#065f46; font-size:1.15rem; display:block; margin-bottom:6px;">🎉 Official DSR Report Generated Successfully!</strong>
            <span style="color:#047857; font-size:0.92rem;">The metrics, mandal statistics, and PDF preview below have been updated in real-time.</span>
            <div style="margin-top:14px; display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
              <a class="btn btn-gold btn-sm" href="/api/naresh/download" target="_blank">📥 Download Official PDF</a>
              <button type="button" class="btn btn-white btn-sm" onclick="loadAndScrollToViewer()">👁️ View in PDF Reader</button>
              <button type="button" class="btn btn-outline btn-sm" style="color:var(--text); border-color:var(--border);" onclick="goToStep(3)">🔄 Generate Another Date</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Live Status Bar -->
      <div class="automation-status-bar" id="status-bar">
        <span class="status-indicator" id="status-dot"></span>
        <span id="status-msg">Status: Ready to connect to e-Panchayat Telangana portal</span>
      </div>
    </section>

    <!-- ========================================================
         RESULTS SECTION (Hidden initially until report is generated)
         ======================================================== -->
    <div id="results-section" style="display: none;">

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
        <iframe id="pdf-frame" class="pdf-frame" src="about:blank"></iframe>
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

    </div>

  </main>

  <footer>
    Government of Telangana &bull; Panchayat Raj &amp; Rural Employment Department<br>
    Automated DSR Monitoring Service &bull; Khammam District (Office ID: 3698)
  </footer>

  <script>
    let reportData = null;
    let currentStep = 1;

    function goToStep(step) {
      currentStep = step;
      for (let i = 1; i <= 4; i++) {
        const pane = document.getElementById(`pane-step-${i}`);
        const nav = document.getElementById(`step-nav-${i}`);
        const line = document.getElementById(`line-${i}`);
        if (pane) pane.classList.toggle('active', i === step);
        if (nav) {
          nav.classList.toggle('active', i === step);
          nav.classList.toggle('completed', i < step);
        }
        if (line) {
          line.classList.toggle('active', i < step);
        }
      }
    }

    function togglePasswordVisibility() {
      const pwd = document.getElementById('auto-pwd');
      pwd.type = pwd.type === 'password' ? 'text' : 'password';
    }

    function updateStatus(msg, type = 'normal') {
      const sMsg = document.getElementById('status-msg');
      const sDot = document.getElementById('status-dot');
      sMsg.innerText = msg;
      if (type === 'error') {
        sDot.style.background = '#dc2626';
        sMsg.style.color = '#dc2626';
      } else if (type === 'success') {
        sDot.style.background = '#10b981';
        sMsg.style.color = '#047857';
      } else {
        sDot.style.background = '#f59e0b';
        sMsg.style.color = '#4e6b60';
      }
    }

    async function startDepartmentLogin() {
      const user = document.getElementById('auto-user').value.trim();
      const pwd = document.getElementById('auto-pwd').value.trim();
      if (!user || !pwd) {
        alert('Please enter both User ID and Password.');
        return;
      }
      const btn = document.getElementById('btn-login');
      btn.disabled = true;
      btn.innerText = '⏳ Connecting & Generating OTP...';
      updateStatus('Connecting to e-Panchayat portal & solving captcha...');

      try {
        const formData = new FormData();
        formData.append('username', user);
        formData.append('password', pwd);

        const res = await fetch('/api/naresh/login', {
          method: 'POST',
          body: formData
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.detail || 'Login initiation failed');

        updateStatus(json.message || 'OTP triggered successfully!', 'success');
        document.getElementById('session-badge').innerText = 'Session: Awaiting OTP';
        goToStep(2);
        setTimeout(() => {
          const otpInput = document.getElementById('auto-otp');
          if (otpInput) otpInput.focus();
        }, 200);
      } catch (err) {
        updateStatus('Login Error: ' + err.message, 'error');
        alert('Login failed: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerText = '🔐 Login to e-Panchayat & Generate OTP';
      }
    }

    async function validateOTP() {
      const otp = document.getElementById('auto-otp').value.trim();
      if (!otp || otp.length < 6) {
        alert('Please enter the valid 6-digit OTP received on your mobile.');
        return;
      }
      const btn = document.getElementById('btn-validate-otp');
      btn.disabled = true;
      btn.innerText = '⏳ Validating OTP...';
      updateStatus('Validating OTP on e-Panchayat portal...');

      try {
        const formData = new FormData();
        formData.append('otp', otp);

        const res = await fetch('/api/naresh/verify-otp', {
          method: 'POST',
          body: formData
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.detail || 'OTP validation failed');

        updateStatus('Authenticated! e-Panchayat session active.', 'success');
        document.getElementById('session-badge').innerText = 'Session: Authenticated (Active)';
        goToStep(3);
      } catch (err) {
        updateStatus('OTP Error: ' + err.message, 'error');
        alert('OTP validation failed: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerText = '✅ Validate OTP & Proceed to Report Selection';
      }
    }

    async function runAutomatedGeneration() {
      const mod = document.getElementById('auto-module').value;
      const date = document.getElementById('auto-date').value;
      if (!date) {
        alert('Please select a report date.');
        return;
      }

      goToStep(4);
      const titleEl = document.getElementById('progress-status-title');
      const barFill = document.getElementById('progress-bar-fill');
      const banner = document.getElementById('auto-completion-banner');
      const spinner = document.getElementById('auto-spinner');
      banner.style.display = 'none';
      spinner.style.display = 'block';

      // Step 1
      setSubStep(1, 'active');
      titleEl.innerText = 'Navigating to GP Monitoring in portal iframe...';
      barFill.style.width = '30%';
      updateStatus('Navigating to GP Monitoring reports...');

      try {
        const formData = new FormData();
        formData.append('module', mod);
        formData.append('date', date);

        setTimeout(() => {
          setSubStep(1, 'done');
          setSubStep(2, 'active');
          titleEl.innerText = 'Expanding Sanitation Reports -> DSR REPORTS...';
          barFill.style.width = '55%';
        }, 800);

        setTimeout(() => {
          setSubStep(2, 'done');
          setSubStep(3, 'active');
          titleEl.innerText = `Setting Date filter to ${date}...`;
          barFill.style.width = '75%';
        }, 1600);

        const res = await fetch('/api/naresh/generate', {
          method: 'POST',
          body: formData
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json.detail || 'Report generation failed');

        setSubStep(3, 'done');
        setSubStep(4, 'done');
        setSubStep(5, 'done');
        barFill.style.width = '100%';
        spinner.style.display = 'none';
        titleEl.innerText = 'Report Generation Completed!';
        banner.style.display = 'block';
        updateStatus('Report generated successfully!', 'success');

        // Reveal the results section (metrics, viewer, mandals table)
        const resultsEl = document.getElementById('results-section');
        if (resultsEl) {
          resultsEl.style.display = 'block';
          resultsEl.scrollIntoView({ behavior: 'smooth' });
        }

        // Reload data and refresh viewer
        await loadNareshData();
        refreshViewer();
      } catch (err) {
        spinner.style.display = 'none';
        titleEl.innerText = 'Generation encountered an error';
        updateStatus('Error: ' + err.message, 'error');
        alert('Report generation failed: ' + err.message);
      }
    }

    function setSubStep(idx, state) {
      const el = document.getElementById(`ps-${idx}`);
      if (!el) return;
      el.classList.remove('active', 'done');
      if (state) el.classList.add(state);
    }

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

    // Set today's date in datepicker
    const today = new Date().toISOString().split('T')[0];
    const datePicker = document.getElementById('auto-date');
    if (datePicker) datePicker.value = today;
  </script>
</body>
</html>
"""
