"""FastAPI webserver for Khammam PS attendance reports."""

from __future__ import annotations

import hmac
import hashlib
import json
import logging
import os
import re
import tempfile
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, Response

from integrations import (
    ALLOWED_EXTENSIONS,
    JobRecord,
    JobTracker,
    LocalJobTracker,
    LocalStorage,
    Storage,
    utc_now,
)
from report_generator import (
    InputValidationError,
    detect_file_metadata,
    generate_mandal_pdf,
    generate_pdf,
    process_attendance_file,
)


logger = logging.getLogger("khammam_attendance")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(message)s")
MAX_UPLOAD_BYTES = 30 * 1024 * 1024
JOB_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,100}$")
WEB_JOB_COOKIE_NAME = "khammam_web_report"
WEB_JOB_TTL_SECONDS = 60 * 60
WEB_UPLOADS_PER_HOUR = 20
REPORT_FILENAME_PATTERN = re.compile(r"^PS_Attendance_Report_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.pdf$")

UPLOAD_PAGE_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Telangana PR &amp; RD · Executive Analytics Portal</title>
  <style>
    :root { color-scheme: light; font-family: Inter, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Arial, sans-serif; }
    * { box-sizing: border-box; }
    body { margin: 0; background: #f3f7f5; color: #15332b; line-height: 1.5; }

    /* Top Navigation Bar */
    .navbar { position: sticky; top: 0; z-index: 1000; background: #0c3829; color: white; box-shadow: 0 2px 12px rgba(0,0,0,0.15); }
    .nav-inner { max-width: 1080px; margin: 0 auto; padding: 0 20px; display: flex; align-items: center; justify-content: space-between; height: 64px; }
    .nav-brand { display: flex; align-items: center; gap: 12px; text-decoration: none; color: white; cursor: pointer; }
    .nav-brand-logo { font-size: 1.7rem; line-height: 1; }
    .nav-brand-titles { display: flex; flex-direction: column; }
    .nav-brand-sup { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #8cd6b7; }
    .nav-brand-main { font-size: 1.05rem; font-weight: 800; letter-spacing: -0.01em; color: #ffffff; }

    .nav-menu { display: flex; align-items: center; gap: 6px; }
    .nav-link { color: #d4e8de; text-decoration: none; padding: 8px 14px; font-weight: 600; font-size: 0.92rem; border-radius: 8px; transition: all 0.15s; cursor: pointer; }
    .nav-link:hover { color: white; background: rgba(255,255,255,0.1); }
    .nav-link.active { color: white; background: #167451; }

    /* Submenu Dropdown */
    .dropdown { position: relative; display: inline-block; }
    .dropdown-btn { background: transparent; border: none; color: #d4e8de; padding: 8px 14px; font-weight: 600; font-size: 0.92rem; border-radius: 8px; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: all 0.15s; font-family: inherit; }
    .dropdown-btn:hover { color: white; background: rgba(255,255,255,0.1); }
    .dropdown-btn.active { color: white; background: #167451; }
    .caret { font-size: 0.75rem; transition: transform 0.2s; }
    .dropdown:hover .caret, .dropdown.open .caret { transform: rotate(180deg); }

    .dropdown-menu { display: none; position: absolute; top: calc(100% + 4px); right: 0; min-width: 320px; background: white; border: 1px solid #d9e6df; border-radius: 14px; box-shadow: 0 16px 36px rgba(12,56,41,0.18); padding: 8px; z-index: 1001; }
    .dropdown:hover .dropdown-menu, .dropdown.open .dropdown-menu { display: block; animation: dropdownFade 0.15s ease-out; }
    @keyframes dropdownFade { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: translateY(0); } }

    .dropdown-header { font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #5a7369; padding: 8px 12px 4px; }
    .dropdown-divider { height: 1px; background: #e5eee9; margin: 6px 0; }
    .dropdown-item { display: flex; align-items: flex-start; gap: 10px; padding: 9px 12px; border-radius: 9px; text-decoration: none; color: #15332b; transition: background 0.15s; cursor: pointer; }
    .dropdown-item:hover { background: #f0f7f3; }
    .dropdown-item-icon { font-size: 1.25rem; line-height: 1.2; flex-shrink: 0; }
    .dropdown-item-content strong { display: block; font-size: 0.88rem; color: #15332b; font-weight: 700; }
    .dropdown-item-content span { font-size: 0.78rem; color: #5a7369; line-height: 1.35; display: block; }
    .dropdown-item.disabled { opacity: 0.65; cursor: not-allowed; background: transparent !important; }
    .badge-soon { display: inline-block; font-size: 0.68rem; font-weight: 700; background: #fef3c7; color: #92400e; padding: 1px 6px; border-radius: 4px; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.04em; }

    /* Layout Container */
    main { max-width: 1080px; margin: 30px auto 60px; padding: 0 20px; }
    .page-view { display: none; }
    .page-view.active { display: block; }

    /* HOME VIEW STYLES */
    .hero-banner { background: linear-gradient(135deg, #0d3d2c 0%, #167451 100%); color: white; border-radius: 20px; padding: clamp(28px, 5vw, 44px); box-shadow: 0 16px 40px rgba(12,56,41,0.16); margin-bottom: 28px; position: relative; overflow: hidden; }
    .hero-banner::after { content: ""; position: absolute; right: -50px; bottom: -50px; width: 260px; height: 260px; background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%); border-radius: 50%; pointer-events: none; }
    .hero-badge { display: inline-block; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: #c4f2dc; font-size: 0.76rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; padding: 4px 10px; border-radius: 6px; margin-bottom: 12px; }
    .hero-title { margin: 0 0 10px; font-size: clamp(1.8rem, 4vw, 2.4rem); font-weight: 800; line-height: 1.2; letter-spacing: -0.02em; }
    .hero-desc { font-size: 1.02rem; line-height: 1.6; color: #e1f3ea; margin: 0; max-width: 760px; }

    .section-heading { display: flex; align-items: baseline; justify-content: space-between; margin: 34px 0 16px; }
    .section-heading h2 { margin: 0; font-size: 1.45rem; font-weight: 800; color: #15332b; letter-spacing: -0.01em; }
    .section-heading span { font-size: 0.88rem; color: #5a7369; font-weight: 500; }

    /* Module Cards Grid */
    .modules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
    .module-card { background: white; border: 1px solid #d9e6df; border-radius: 18px; padding: 24px; box-shadow: 0 10px 30px rgba(23,59,43,0.06); display: flex; flex-direction: column; justify-content: space-between; transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s; position: relative; }
    .module-card:hover { transform: translateY(-3px); box-shadow: 0 16px 36px rgba(23,59,43,0.12); }
    .module-card.active-module { border: 2px solid #167451; background: #ffffff; }

    .module-card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
    .module-icon-wrap { font-size: 2rem; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; background: #eaf5ef; }
    .module-badge { font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; padding: 4px 8px; border-radius: 6px; }
    .badge-live { background: #d1fae5; color: #065f46; border: 1px solid #a7f3d0; }
    .badge-planned { background: #f3f4f6; color: #4b5563; border: 1px solid #e5e7eb; }

    .module-card h3 { margin: 0 0 8px; font-size: 1.2rem; font-weight: 700; color: #15332b; }
    .module-card p { font-size: 0.9rem; color: #4d665e; line-height: 1.55; margin: 0 0 18px; flex-grow: 1; }
    .module-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: auto; }

    .btn-action { display: inline-flex; align-items: center; gap: 6px; padding: 10px 16px; font-size: 0.88rem; font-weight: 700; border-radius: 8px; text-decoration: none; cursor: pointer; border: none; font-family: inherit; transition: background 0.15s; }
    .btn-primary { background: #167451; color: white; }
    .btn-primary:hover { background: #125e41; }
    .btn-secondary { background: #eaf5ef; color: #167451; border: 1px solid #b9ddcb; }
    .btn-secondary:hover { background: #d7ede1; }
    .btn-disabled { background: #f3f4f6; color: #9ca3af; cursor: not-allowed; border: 1px solid #e5e7eb; }

    /* Guidelines Notice Card on Home */
    .info-card { background: white; border: 1px solid #d9e6df; border-radius: 18px; padding: 26px; margin-top: 28px; box-shadow: 0 10px 30px rgba(23,59,43,0.05); }
    .info-card h3 { margin: 0 0 12px; font-size: 1.15rem; color: #15332b; }
    .guideline-list { margin: 0; padding-left: 20px; color: #486158; font-size: 0.92rem; line-height: 1.7; }

    /* REPORT VIEW STYLES */
    .breadcrumb-bar { margin-bottom: 16px; }
    .back-btn { display: inline-flex; align-items: center; gap: 6px; color: #167451; text-decoration: none; font-weight: 700; font-size: 0.92rem; padding: 7px 14px; background: white; border: 1px solid #cfe0d7; border-radius: 8px; transition: background 0.15s; cursor: pointer; font-family: inherit; }
    .back-btn:hover { background: #eaf5ef; }

    .report-card { background: white; border: 1px solid #d9e6df; border-radius: 18px; padding: clamp(24px, 5vw, 42px); box-shadow: 0 14px 40px #173b2b12; max-width: 860px; margin: 0 auto; }
    .eyebrow { color: #247558; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: .8rem; }
    h1 { margin: 10px 0 6px; font-size: clamp(1.8rem, 4.5vw, 2.3rem); line-height: 1.15; }
    p.intro { line-height: 1.6; color: #486158; margin-top: 0; margin-bottom: 20px; }
    
    /* Navigation Tabs inside report */
    .tabs-header { display: flex; gap: 8px; margin: 20px 0 24px; border-bottom: 2px solid #e1ebe5; }
    .tab-btn { background: transparent; border: none; padding: 11px 20px; font-size: 0.98rem; font-weight: 700; color: #5a7369; cursor: pointer; border-radius: 8px 8px 0 0; transition: all .15s; border-bottom: 3px solid transparent; margin-bottom: -2px; font-family: inherit; }
    .tab-btn:hover { color: #167451; background: #f0f7f3; }
    .tab-btn.active { color: #167451; border-bottom: 3px solid #167451; background: #eef6f2; }

    .tab-content { display: none; }
    .tab-content.active { display: block; }

    .field-group { margin: 18px 0; }
    label { display: block; margin: 0 0 6px; font-weight: 650; font-size: 0.95rem; }
    .req { color: #c92a2a; }
    .badge { font-size: 0.74rem; font-weight: 700; padding: 2px 7px; border-radius: 5px; margin-left: 6px; text-transform: uppercase; letter-spacing: .04em; }
    .badge-rec { background: #e3f5eb; color: #167451; }
    .badge-opt { background: #fff3d6; color: #855c06; }
    .hint { font-size: 0.82rem; color: #5a7369; margin-top: 5px; line-height: 1.45; }
    input[type="file"], input[type="text"], select { width: 100%; box-sizing: border-box; padding: 11px 13px; border: 1px solid #bfd1c7; border-radius: 9px; background: white; color: #15332b; font-size: 0.95rem; font-family: inherit; }
    input[type="file"] { background: #fbfdfc; }
    button[type="submit"] { display: inline-block; border: 0; border-radius: 10px; background: #167451; color: white; padding: 13px 22px; font-weight: 700; font-size: 1rem; text-decoration: none; cursor: pointer; transition: background .15s; font-family: inherit; }
    button[type="submit"]:hover { background: #125e41; }
    button[type="submit"]:disabled { opacity: .6; cursor: wait; }
    .actions { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin-top: 24px; }
    .notice { margin: 16px 0; padding: 12px 14px; border-radius: 10px; background: #eef6f2; border-left: 4px solid #167451; color: #1b4938; line-height: 1.5; font-size: 0.88rem; }
    .message { min-height: 1.5em; margin-top: 14px; color: #8b2635; font-weight: 600; }
    .message.success { color: #176247; }
    .fine-print { border-top: 1px solid #e5eee9; margin-top: 26px; padding-top: 18px; font-size: 0.88rem; color: #627b72; line-height: 1.55; }

    /* Footer */
    footer { border-top: 1px solid #dce6e1; margin-top: 60px; padding: 22px 20px; text-align: center; color: #5a7369; font-size: 0.84rem; background: white; }

    @media (max-width: 640px) {
      .nav-brand-sup { display: none; }
      .nav-menu { gap: 2px; }
      .nav-link, .dropdown-btn { padding: 8px 10px; font-size: 0.85rem; }
      .dropdown-menu { min-width: 270px; right: -30px; }
      .hero-banner { padding: 22px; }
    }
  </style>
</head>
<body>
  <!-- Top Navigation Bar -->
  <header class="navbar">
    <div class="nav-inner">
      <a class="nav-brand" href="#home" onclick="navigateTo('home')">
        <span class="nav-brand-logo">🏛️</span>
        <div class="nav-brand-titles">
          <span class="nav-brand-sup">Government of Telangana</span>
          <span class="nav-brand-main">PR &amp; RD Analytics Portal</span>
        </div>
      </a>
      <nav class="nav-menu">
        <a class="nav-link active" id="nav-home" href="#home" onclick="navigateTo('home')">Home</a>
        
        <!-- Reports Submenu Dropdown -->
        <div class="dropdown" id="reports-dropdown-container">
          <button type="button" class="dropdown-btn" id="nav-reports-btn" onclick="toggleDropdown()">
            Reports &amp; Analytics <span class="caret">▾</span>
          </button>
          <div class="dropdown-menu" id="reports-dropdown-menu">
            <div class="dropdown-header">Active Reports</div>
            <a class="dropdown-item" href="#reports-district" onclick="navigateTo('reports', 'district')">
              <span class="dropdown-item-icon">🏢</span>
              <div class="dropdown-item-content">
                <strong>District Level Monitoring</strong>
                <span>7-Section Comprehensive District PDF Report</span>
              </div>
            </a>
            <a class="dropdown-item" href="#reports-mandal" onclick="navigateTo('reports', 'mandal')">
              <span class="dropdown-item-icon">🏛️</span>
              <div class="dropdown-item-content">
                <strong>Mandal Level Monitoring</strong>
                <span>Focused 2-Page Mandal Officer PDF Report</span>
              </div>
            </a>

            <div class="dropdown-divider"></div>
            <div class="dropdown-header">Upcoming Reporting Options</div>

            <div class="dropdown-item disabled">
              <span class="dropdown-item-icon">💰</span>
              <div class="dropdown-item-content">
                <strong>GP Tax Collection &amp; Finances</strong>
                <span>House Tax &amp; Non-Tax DCB Progress</span>
                <span class="badge-soon">Coming Soon</span>
              </div>
            </div>
          </div>
        </div>
      </nav>
    </div>
  </header>

  <main>
    <!-- VIEW 1: Home Dashboard -->
    <div id="view-home" class="page-view active">
      <section class="hero-banner">
        <span class="hero-badge">Panchayat Raj &amp; Rural Development Department</span>
        <h1 class="hero-title">Executive Monitoring &amp; Analytics Portal</h1>
        <p class="hero-desc">
          Official departmental analytics platform empowering District Officers and Mandal Officers to automated performance tracking, morning attendance compliance, and daily status analytics.
        </p>
      </section>

      <div class="section-heading">
        <h2>Departmental Reporting Modules</h2>
        <span>Select an active module or explore upcoming tools</span>
      </div>

      <div class="modules-grid">
        <!-- Module 1: PS Attendance & DSR Analytics (ACTIVE) -->
        <div class="module-card active-module">
          <div>
            <div class="module-card-header">
              <div class="module-icon-wrap">📋</div>
              <span class="module-badge badge-live">● Active · Live</span>
            </div>
            <h3>PS Attendance &amp; DSR Analytics</h3>
            <p>
              Upload portal exports to verify Panchayat Secretary morning attendance and Daily Status Report (DSR) entries. Generates official executive PDF reports for District Officers and Mandal MPOs/MPDOs with late submissions (after 9 AM) highlighted in red.
            </p>
          </div>
          <div class="module-actions">
            <button type="button" class="btn-action btn-primary" onclick="navigateTo('reports', 'district')">
              🏢 District Monitoring
            </button>
            <button type="button" class="btn-action btn-secondary" onclick="navigateTo('reports', 'mandal')">
              🏛️ Mandal Monitoring
            </button>
          </div>
        </div>

        <!-- Module 2: Tax Collection (Upcoming) -->
        <div class="module-card">
          <div>
            <div class="module-card-header">
              <div class="module-icon-wrap">💰</div>
              <span class="module-badge badge-planned">Coming Soon</span>
            </div>
            <h3>GP Tax Collection &amp; Finances</h3>
            <p>
              Real-time Demand, Collection, and Balance (DCB) monitoring for House Tax across Gram Panchayats.
            </p>
          </div>
          <div class="module-actions">
            <button type="button" class="btn-action btn-disabled" disabled>Planned Module</button>
          </div>
        </div>
      </div>
    </div>

    <!-- VIEW 2: Report Tool (PS Attendance & DSR Analytics) -->
    <div id="view-reports" class="page-view">
      <div class="breadcrumb-bar">
        <button type="button" class="back-btn" onclick="navigateTo('home')">
          ← Back to Home Dashboard
        </button>
      </div>

      <section class="report-card">
        <div class="eyebrow" id="page-eyebrow">Telangana Panchayat Raj &amp; Rural Development</div>
        <h1>PS Attendance &amp; DSR Analytics</h1>
        <p class="intro">Generate official Gram Panchayat morning attendance and DSR analytics reports directly from your uploaded portal exports.</p>
        
        <!-- Top Level Tabs -->
        <div class="tabs-header" role="tablist">
          <button type="button" class="tab-btn active" id="tab-btn-district" onclick="switchMonitoringTab('district')">
            🏢 District Level Monitoring
          </button>
          <button type="button" class="tab-btn" id="tab-btn-mandal" onclick="switchMonitoringTab('mandal')">
            🏛️ Mandal Level Monitoring
          </button>
        </div>

        <!-- TAB 1: District Level Monitoring -->
        <div id="tab-district" class="tab-content active">
          <div class="notice">
            <strong>District Monitoring:</strong> Automatically detects your District, all Mandals, and Gram Panchayats directly from the uploaded raw data file. When Presentees and Absentees files are provided, secretary details (Name, Mobile, Nature of Posting) are dynamically matched by LGD code.
          </div>

          <form id="upload-form" class="district-form">
            <div class="field-group">
              <label for="attendance-file">1. Attendance &amp; DSR Raw Data File <span class="req">*</span></label>
              <input id="attendance-file" name="file" type="file" required accept=".xls,.xlsx,.csv">
              <div class="hint">Portal export containing District, Division, Mandal, Panchayat Name, LGD, First &amp; Second Attendance, and DSR Status.</div>
            </div>

            <div class="field-group">
              <label for="presentees-file">2. Presentees PS Details File <span class="badge badge-rec">Recommended</span></label>
              <input id="presentees-file" name="presentees_file" type="file" accept=".xls,.xlsx,.csv">
              <div class="hint">Export of present secretaries with Panchayat LGD Code, PS Name, Designation, Nature of Posting, and Mobile Number.</div>
            </div>

            <div class="field-group">
              <label for="absentees-file">3. Absentees PS Details File <span class="badge badge-opt">Optional</span></label>
              <input id="absentees-file" name="absentees_file" type="file" accept=".xls,.xlsx,.csv">
              <div class="hint">Export of absent secretaries. Not required if all secretaries submitted attendance.</div>
            </div>

            <div class="actions">
              <button id="generate-button" type="submit">Generate and download report</button>
            </div>
            <div id="report-message" class="message" role="status" aria-live="polite"></div>
          </form>
        </div>

        <!-- TAB 2: Mandal Level Monitoring -->
        <div id="tab-mandal" class="tab-content">
          <div class="notice">
            <strong>Mandal Monitoring:</strong> Designed specifically for Mandal officers. Upload <strong>only your RAW data file</strong>. Your Mandal is detected automatically to generate the 2-page report: <strong>Page 1</strong> with Mandal Abstract Summary, Attendance Pending GPs, DSR Pending GPs, and GPs Submitted Attendance After 9 AM; <strong>Page 2</strong> with complete Gram Panchayat Attendance &amp; DSR Status (with times after 9:00 AM and pending DSR highlighted in red).
          </div>

          <form id="mandal-form">
            <div class="field-group">
              <label for="mandal-attendance-file">1. Attendance &amp; DSR Raw Data File <span class="req">*</span></label>
              <input id="mandal-attendance-file" name="file" type="file" required accept=".xls,.xlsx,.csv">
              <div class="hint">Upload your attendance raw data file. Mandal name is auto-detected directly from the file.</div>
            </div>

            <div class="field-group">
              <label for="mandal-display">2. Uploaded Mandal</label>
              <input id="mandal-display" type="text" readonly placeholder="Mandal name will appear here automatically after upload..." style="font-weight: 600; color: #167451; background: #fbfdfc;">
              <input type="hidden" id="mandal-select" name="mandal_name">
              <div class="hint" id="mandal-detect-hint">Mandal name detected from the uploaded raw data file.</div>
            </div>

            <div class="actions">
              <button id="mandal-generate-button" type="submit">Generate Mandal Report (PDF)</button>
            </div>
            <div id="mandal-report-message" class="message" role="status" aria-live="polite"></div>
          </form>
        </div>

        <p class="fine-print">Supported formats: Excel (.xls, .xlsx), CSV, or portal HTML tables exported with a .xls extension. The PDF report downloads automatically once analytics finish.</p>
      </section>
    </div>
  </main>

  <footer>
    Executive Analytics &amp; Monitoring Portal Designed and Developed by DPMs
  </footer>

  <script>
    (() => {
      // View Navigation
      window.navigateTo = function(view, tab, anchor) {
        const homeView = document.getElementById('view-home');
        const reportsView = document.getElementById('view-reports');
        const navHome = document.getElementById('nav-home');
        const navReportsBtn = document.getElementById('nav-reports-btn');
        closeDropdown();

        if (view === 'reports') {
          homeView.classList.remove('active');
          reportsView.classList.add('active');
          navHome.classList.remove('active');
          navReportsBtn.classList.add('active');
          if (tab) {
            window.switchMonitoringTab(tab);
            window.location.hash = `#reports-${tab}`;
          } else {
            window.location.hash = '#reports';
          }
          window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          reportsView.classList.remove('active');
          homeView.classList.add('active');
          navHome.classList.add('active');
          navReportsBtn.classList.remove('active');
          if (anchor) {
            window.location.hash = `#${anchor}`;
            const el = document.getElementById(anchor);
            if (el) el.scrollIntoView({ behavior: 'smooth' });
          } else {
            window.location.hash = '#home';
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }
        }
      };

      // Dropdown toggle
      const dropdownContainer = document.getElementById('reports-dropdown-container');
      window.toggleDropdown = function() {
        dropdownContainer.classList.toggle('open');
      };
      function closeDropdown() {
        dropdownContainer.classList.remove('open');
      }
      document.addEventListener('click', (e) => {
        if (!dropdownContainer.contains(e.target)) {
          closeDropdown();
        }
      });

      // Hash routing
      function handleHash() {
        const hash = window.location.hash.toLowerCase();
        if (hash.startsWith('#reports-mandal')) {
          window.navigateTo('reports', 'mandal');
        } else if (hash.startsWith('#reports-district')) {
          window.navigateTo('reports', 'district');
        } else if (hash.startsWith('#reports')) {
          window.navigateTo('reports');
        } else if (hash === '#guidelines' || hash === '#guidelines-section') {
          window.navigateTo('home', null, 'guidelines-section');
        } else {
          window.navigateTo('home');
        }
      }
      window.addEventListener('hashchange', handleHash);

      // Tab switching inside report
      window.switchMonitoringTab = function(mode) {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        if (mode === 'mandal') {
          document.getElementById('tab-btn-mandal').classList.add('active');
          document.getElementById('tab-mandal').classList.add('active');
        } else {
          document.getElementById('tab-btn-district').classList.add('active');
          document.getElementById('tab-district').classList.add('active');
        }
      };

      function showMessage(element, message, success = false) {
        element.textContent = message;
        element.classList.toggle('success', success);
      }

      async function readResponse(response) {
        const body = await response.json().catch(() => ({}));
        if (!response.ok) {
          const detail = body.detail;
          const message = typeof detail === 'string' ? detail : (detail?.message || 'The request failed.');
          throw new Error(message);
        }
        return body;
      }

      async function apiJson(url, options = {}) {
        const response = await fetch(url, { credentials: 'same-origin', ...options });
        return readResponse(response);
      }

      // Dynamic Mandal detection when Mandal file is chosen
      const mandalFileInput = document.getElementById('mandal-attendance-file');
      const mandalDisplay = document.getElementById('mandal-display');
      const mandalSelect = document.getElementById('mandal-select');
      const mandalDetectHint = document.getElementById('mandal-detect-hint');

      mandalFileInput.addEventListener('change', async () => {
        const file = mandalFileInput.files[0];
        if (!file) return;
        mandalDisplay.value = 'Detecting Mandal from file…';
        mandalDetectHint.textContent = 'Reading uploaded file…';
        try {
          const data = new FormData();
          data.append('file', file);
          const meta = await apiJson('/api/web/detect-mandals', { method: 'POST', body: data });
          if (meta.mandals && meta.mandals.length > 0) {
            const mandalName = meta.mandals[0];
            mandalDisplay.value = mandalName;
            mandalSelect.value = mandalName;
            mandalDetectHint.textContent = `Detected District: ${meta.district_name || 'Telangana'} | Uploaded Mandal: ${mandalName}`;
          } else {
            mandalDisplay.value = 'No mandal found';
            mandalSelect.value = '';
            mandalDetectHint.textContent = 'Could not detect mandal in the file.';
          }
        } catch (err) {
          mandalDisplay.value = 'Failed to detect mandal';
          mandalSelect.value = '';
          mandalDetectHint.textContent = err.message || 'Error detecting mandal.';
        }
      });

      // Generic job runner
      async function runReportJob(formData, submitBtn, messageEl, fallbackFilename) {
        submitBtn.disabled = true;
        showMessage(messageEl, 'Uploading and processing the attendance data…');
        try {
          let job = await apiJson('/api/web/reports', { method: 'POST', body: formData });
          const jobId = job.job_id;
          if (!jobId) throw new Error('The service did not return a report job ID.');
          let attempts = 0;
          while (job.status === 'Submitted' || job.status === 'Processing') {
            showMessage(messageEl, `Report ${job.status.toLowerCase()}…`);
            if (attempts++ > 180) throw new Error('The report is taking too long. Please try again later.');
            await new Promise(resolve => setTimeout(resolve, 2000));
            job = await apiJson(`/api/web/reports/${encodeURIComponent(jobId)}`);
          }
          if (job.status !== 'Completed') throw new Error(job.notes || 'The report job did not complete.');
          showMessage(messageEl, 'Report ready. Downloading PDF…', true);
          const pdfResponse = await fetch(`/api/web/reports/${encodeURIComponent(jobId)}/download`, {
            credentials: 'same-origin'
          });
          if (!pdfResponse.ok) await readResponse(pdfResponse);
          const blob = await pdfResponse.blob();
          const objectUrl = URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = objectUrl;
          const disposition = pdfResponse.headers.get('Content-Disposition') || '';
          const fileName = /filename="?([^";]+)"?/i.exec(disposition)?.[1];
          link.download = fileName || fallbackFilename;
          document.body.appendChild(link);
          link.click();
          link.remove();
          setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
          showMessage(messageEl, 'Report downloaded successfully! You can upload another file.', true);
        } catch (error) {
          showMessage(messageEl, error.message || 'Report generation failed.');
        } finally {
          submitBtn.disabled = false;
        }
      }

      // District form submission
      document.getElementById('upload-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const file = document.getElementById('attendance-file').files[0];
        if (!file) return;
        const data = new FormData();
        data.append('file', file);
        data.append('report_mode', 'district');
        const pres = document.getElementById('presentees-file').files[0];
        if (pres) data.append('presentees_file', pres);
        const abs = document.getElementById('absentees-file').files[0];
        if (abs) data.append('absentees_file', abs);
        runReportJob(data, document.getElementById('generate-button'), document.getElementById('report-message'), 'District_PS_Attendance_Report.pdf');
      });

      // Mandal form submission
      document.getElementById('mandal-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const file = mandalFileInput.files[0];
        if (!file) return;
        const mandalName = mandalSelect.value || mandalDisplay.value || '';
        const data = new FormData();
        data.append('file', file);
        data.append('report_mode', 'mandal');
        if (mandalName && mandalName !== 'No mandal found' && mandalName !== 'Failed to detect mandal' && mandalName !== 'Detecting Mandal from file…') {
          data.append('mandal_name', mandalName);
        }
        runReportJob(data, document.getElementById('mandal-generate-button'), document.getElementById('mandal-report-message'), `${mandalName || 'Mandal'}_Attendance_Report.pdf`);
      });

      // Handle initial route on page load
      handleHash();
    })();
  </script>
</body>
</html>"""


@dataclass(frozen=True)
class Settings:
    session_secret: str
    data_dir: Path
    max_upload_bytes: int

    @classmethod
    def from_env(cls) -> "Settings":
        try:
            max_bytes = int(os.getenv("MAX_UPLOAD_BYTES", str(MAX_UPLOAD_BYTES)))
        except ValueError as exc:
            raise RuntimeError("MAX_UPLOAD_BYTES must be an integer.") from exc
        if max_bytes < 1 or max_bytes > 100 * 1024 * 1024:
            raise RuntimeError("MAX_UPLOAD_BYTES must be between 1 byte and 100 MB.")
        session_secret = os.getenv("WEB_SESSION_SECRET", "").strip()
        if not session_secret:
            # Keep existing Render deployments working while the environment
            # variable is migrated from the former API-token name.
            session_secret = os.getenv("APP_API_TOKEN", "").strip()
        return cls(
            session_secret=session_secret,
            data_dir=Path(os.getenv("DATA_DIR", "./data")).resolve(),
            max_upload_bytes=max_bytes,
        )


def _clean_filename(value: str | None) -> str:
    raw = (value or "attendance.xls").replace("\\", "/").split("/")[-1].strip()
    return raw or "attendance.xls"


def _validate_job_id(value: str | None) -> str:
    candidate = (value or uuid4().hex).strip()
    if not JOB_ID_PATTERN.fullmatch(candidate):
        raise HTTPException(status_code=400, detail="JobID must contain 1-100 letters, numbers, underscores, or hyphens.")
    return candidate


def _make_report_filename(report_date: date, requested_at: str) -> str:
    try:
        uploaded_at = datetime.fromisoformat(requested_at.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError):
        uploaded_at = datetime.now(timezone.utc)
    if uploaded_at.tzinfo is None:
        uploaded_at = uploaded_at.replace(tzinfo=timezone.utc)
    india_time = uploaded_at.astimezone(timezone(timedelta(hours=5, minutes=30)))
    return f"PS_Attendance_Report_{report_date:%Y-%m-%d}_{india_time:%H-%M-%S}.pdf"


def _record_report_filename(record: JobRecord) -> str:
    match = re.search(r"(?:^|;\s*)Download filename: ([A-Za-z0-9_-]+\.pdf)(?:$|;)", record.notes)
    if match:
        return match.group(1)
    if record.local_pdf_path:
        candidate = Path(record.local_pdf_path).name
        if candidate.endswith(".pdf"):
            return candidate
    return "PS_Attendance_Report.pdf"


def _safe_error(exc: Exception) -> tuple[int, str]:
    if isinstance(exc, InputValidationError):
        return 422, str(exc)
    if isinstance(exc, PermissionError):
        return 403, str(exc)
    if isinstance(exc, FileNotFoundError):
        return 404, str(exc)
    if isinstance(exc, ValueError):
        return 400, str(exc)
    return 500, "Report processing failed. Check the service logs for details."


def _read_upload(file: UploadFile, max_bytes: int) -> bytes:
    filename = _clean_filename(file.filename)
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Allowed file types are .xls, .xlsx, and .csv.")
    output = bytearray()
    while True:
        chunk = file.file.read(1024 * 1024)
        if not chunk:
            break
        output.extend(chunk)
        if len(output) > max_bytes:
            raise HTTPException(status_code=413, detail=f"File exceeds the {max_bytes // (1024 * 1024)} MB upload limit.")
    if not output:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    return bytes(output)


def create_app(
    settings: Settings | None = None,
    tracker: JobTracker | None = None,
    storage: Storage | None = None,
) -> FastAPI:
    config = settings or Settings.from_env()
    if config.session_secret and len(config.session_secret) < 32:
        raise RuntimeError("WEB_SESSION_SECRET must contain at least 32 characters.")

    storage = storage or LocalStorage(config.data_dir)
    tracker = tracker or LocalJobTracker(config.data_dir / "attendance_jobs.sqlite3")
    api = FastAPI(
        title="Khammam PS Attendance Analytics",
        version="3.1.0",
        description="Upload attendance and PS details files and download formatted reports.",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
    api.state.settings = config
    api.state.tracker = tracker
    api.state.storage = storage
    api.state.web_upload_attempts = {}

    @api.get("/", response_class=HTMLResponse, include_in_schema=False)
    def home() -> HTMLResponse:
        return HTMLResponse(UPLOAD_PAGE_HTML)

    @api.get("/reports/ps-attendance", response_class=HTMLResponse, include_in_schema=False)
    def ps_attendance_page() -> HTMLResponse:
        return HTMLResponse(UPLOAD_PAGE_HTML)

    @api.middleware("http")
    async def limit_content_length(request: Request, call_next: Any) -> Response:
        if request.url.path == "/api/web/reports" and request.method == "POST":
            raw_length = request.headers.get("content-length")
            if raw_length:
                try:
                    # Allow up to 3 files plus multipart boundary overhead
                    if int(raw_length) > (config.max_upload_bytes * 3) + 1024 * 1024:
                        return JSONResponse(status_code=413, content={"detail": "Multipart request is too large."})
                except ValueError:
                    return JSONResponse(status_code=400, content={"detail": "Invalid Content-Length header."})
        return await call_next(request)

    def _check_web_upload_rate_limit(request: Request) -> None:
        now = time.monotonic()
        cutoff = now - 60 * 60
        attempts_by_ip: dict[str, list[float]] = api.state.web_upload_attempts
        for address, attempts in list(attempts_by_ip.items()):
            recent = [attempt for attempt in attempts if attempt > cutoff]
            if recent:
                attempts_by_ip[address] = recent
            else:
                attempts_by_ip.pop(address, None)
        address = request.client.host if request.client else "unknown"
        attempts = attempts_by_ip.setdefault(address, [])
        if len(attempts) >= WEB_UPLOADS_PER_HOUR:
            raise HTTPException(
                status_code=429,
                detail="Upload limit reached. Please try again later.",
                headers={"Retry-After": "3600"},
            )
        attempts.append(now)

    def _make_web_job_cookie(job_id: str) -> str:
        issued_at = str(int(time.time()))
        payload = f"{job_id}.{issued_at}"
        signature = hmac.new(
            config.session_secret.encode("utf-8"), payload.encode("ascii"), hashlib.sha256,
        ).hexdigest()
        return f"{payload}.{signature}"

    def _web_job_cookie_is_valid(request: Request, job_id: str) -> bool:
        cookie = request.cookies.get(WEB_JOB_COOKIE_NAME, "")
        try:
            cookie_job_id, issued_text, supplied_signature = cookie.split(".", maxsplit=2)
            issued_at = int(issued_text)
        except (ValueError, TypeError):
            return False
        now = int(time.time())
        if cookie_job_id != job_id or issued_at > now + 60 or now - issued_at > WEB_JOB_TTL_SECONDS:
            return False
        payload = f"{cookie_job_id}.{issued_text}"
        expected_signature = hmac.new(
            config.session_secret.encode("utf-8"), payload.encode("ascii"), hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(supplied_signature, expected_signature)

    def _get_web_job(job_id: str, request: Request) -> JobRecord:
        stable_id = _validate_job_id(job_id)
        if not config.session_secret:
            raise HTTPException(status_code=503, detail="Report sessions are not configured.")
        if not _web_job_cookie_is_valid(request, stable_id):
            raise HTTPException(status_code=401, detail="This report session is invalid or expired.")
        record = tracker.get(stable_id)
        if not record:
            raise HTTPException(status_code=404, detail="Report job was not found.")
        return record

    def _new_record(job_id: str, filename: str, requested_by: str) -> JobRecord:
        return JobRecord(
            job_id=job_id,
            uploaded_file=filename,
            requested_by=(requested_by or "unknown")[:320],
            requested_at=utc_now(),
        )

    def _process_job(
        job_id: str,
        source: tuple[str, bytes],
        presentees: tuple[str, bytes] | None = None,
        absentees: tuple[str, bytes] | None = None,
        report_mode: str = "district",
        mandal_name: str | None = None,
    ) -> JobRecord:
        current = tracker.get(job_id)
        if not current:
            raise FileNotFoundError("Report job was not found.")
        if current.status == "Completed":
            return current
        if not tracker.claim(job_id):
            current = tracker.get(job_id) or current
            if current.status == "Completed":
                return current
            raise RuntimeError("Report job is already being processed.")

        try:
            filename, raw_bytes = source
            report = process_attendance_file(
                filename,
                raw_bytes,
                presentees_source=presentees,
                absentees_source=absentees,
            )
            clean_dist = re.sub(r"[^A-Za-z0-9_-]", "_", report.district_name)
            if report_mode == "mandal":
                target_mandal = mandal_name.strip() if (mandal_name and mandal_name.strip()) else (
                    report.mandal_rows[0]["mandal"] if report.mandal_rows else "Mandal"
                )
                clean_mandal = re.sub(r"[^A-Za-z0-9_-]", "_", target_mandal)
                download_filename = f"{clean_dist}_{clean_mandal}_Attendance_Report_{report.report_date:%d-%b-%Y}.pdf"
                with tempfile.TemporaryDirectory(prefix="mandal_attendance_") as directory:
                    output_path = Path(directory) / download_filename
                    generate_mandal_pdf(report, output_path, mandal_name=target_mandal)
                    output_reference = storage.save_pdf(job_id, output_path)
            else:
                download_filename = _make_report_filename(report.report_date, current.requested_at)
                with tempfile.TemporaryDirectory(prefix="district_attendance_") as directory:
                    output_path = Path(directory) / download_filename
                    generate_pdf(report, output_path)
                    output_reference = storage.save_pdf(job_id, output_path)

            completed = tracker.update(
                job_id,
                status="Completed",
                output_pdf=output_reference,
                local_pdf_path=str(config.data_dir / "reports" / download_filename),
                notes=(
                    f"District: {report.district_name}; Mode: {report_mode}; "
                    f"Unique GPs: {report.unique_gp_count}; duplicate LGD rows excluded: "
                    f"{report.duplicate_lgd_rows}; rows without LGD excluded: {report.missing_lgd_rows}; "
                    f"conflicting LGDs: {len(report.conflicts)}; Download filename: {download_filename}"
                ),
            )
            logger.info(json.dumps({
                "event": "job_completed",
                "job_id": job_id,
                "mode": report_mode,
                "district": report.district_name,
                "unique_gps": report.unique_gp_count,
            }))
            return completed
        except Exception as exc:
            _, safe_message = _safe_error(exc)
            tracker.update(job_id, status="Failed", notes=safe_message[:1000])
            logger.error(json.dumps({
                "event": "job_failed",
                "job_id": job_id,
                "error_type": type(exc).__name__,
                "message": safe_message,
            }))
            raise

    @api.get("/health")
    def health() -> dict[str, str]:
        return {
            "status": "ok",
            "service": "PS Attendance Analytics",
            "storage": "local",
            "job_tracking": "local_sqlite",
        }

    @api.post("/api/web/detect-mandals", include_in_schema=False)
    def detect_mandals(
        request: Request,
        file: UploadFile = File(...),
    ) -> JSONResponse:
        _check_web_upload_rate_limit(request)
        filename = _clean_filename(file.filename)
        raw = _read_upload(file, config.max_upload_bytes)
        try:
            metadata = detect_file_metadata(filename, raw)
            return JSONResponse(content=metadata)
        except Exception as exc:
            status_code, safe_message = _safe_error(exc)
            raise HTTPException(status_code=status_code, detail=safe_message)

    @api.post("/api/web/reports", status_code=200, include_in_schema=False)
    def create_web_report(
        request: Request,
        file: UploadFile = File(...),
        presentees_file: UploadFile | None = File(default=None),
        absentees_file: UploadFile | None = File(default=None),
        report_mode: str = Form(default="district"),
        mandal_name: str = Form(default=""),
        requested_by: str = Form(default="", alias="RequestedBy"),
    ) -> JSONResponse:
        if not config.session_secret:
            raise HTTPException(status_code=503, detail="Report sessions are not configured.")
        _check_web_upload_rate_limit(request)
        filename = _clean_filename(file.filename)
        raw = _read_upload(file, config.max_upload_bytes)

        presentees_data: tuple[str, bytes] | None = None
        if presentees_file and presentees_file.filename and presentees_file.filename.strip():
            p_name = _clean_filename(presentees_file.filename)
            p_bytes = _read_upload(presentees_file, config.max_upload_bytes)
            presentees_data = (p_name, p_bytes)

        absentees_data: tuple[str, bytes] | None = None
        if absentees_file and absentees_file.filename and absentees_file.filename.strip():
            a_name = _clean_filename(absentees_file.filename)
            a_bytes = _read_upload(absentees_file, config.max_upload_bytes)
            absentees_data = (a_name, a_bytes)

        job_id = uuid4().hex
        record, _ = tracker.create(_new_record(job_id, filename, requested_by))
        try:
            completed = _process_job(
                job_id,
                (filename, raw),
                presentees=presentees_data,
                absentees=absentees_data,
                report_mode=report_mode,
                mandal_name=mandal_name,
            )
        except Exception as exc:
            status_code, safe_message = _safe_error(exc)
            failed = tracker.get(job_id)
            raise HTTPException(status_code=status_code, detail={
                "job_id": job_id,
                "status": failed.status if failed else "Failed",
                "message": safe_message,
            }) from None
        response = JSONResponse(completed.public_dict())
        response.set_cookie(
            WEB_JOB_COOKIE_NAME,
            _make_web_job_cookie(job_id),
            max_age=WEB_JOB_TTL_SECONDS,
            httponly=True,
            secure=request.url.scheme == "https",
            samesite="strict",
            path="/api/web/reports",
        )
        return response

    @api.get("/api/web/reports/{job_id}", include_in_schema=False)
    def get_web_report(job_id: str, request: Request) -> dict[str, str]:
        return _get_web_job(job_id, request).public_dict()

    @api.get("/api/web/reports/{job_id}/download", include_in_schema=False)
    def download_web_report(job_id: str, request: Request) -> Response:
        record = _get_web_job(job_id, request)
        if record.status != "Completed" or not record.output_pdf:
            raise HTTPException(status_code=409, detail=f"Report is not ready (status: {record.status}).")
        try:
            pdf_bytes = storage.read_pdf(record.output_pdf, record.local_pdf_path)
        except Exception as exc:
            status_code, message = _safe_error(exc)
            raise HTTPException(status_code=status_code, detail=message) from None
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{_record_report_filename(record)}"'},
        )

    return api
app = create_app()
