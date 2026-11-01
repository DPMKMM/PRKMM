# e-Panchayat Telangana (EPTS) Automated Report Pipeline (`automate_epts`)

Automated end-to-end workflow for **e-Panchayat Telangana (EPTS)**:
- Login with AI captcha auto-detection
- OTP verification
- Frame-aware navigation under `GP Monitoring` -> `GM-R 1. Sanitation reports` -> `DSR REPORTS`
- Automatic download of:
  1. **GM-R 1.2.7 DSR Raw Data Report** (`raw_dsr.xls`)
  2. **GM-R 1.2.10 Report on Absentees Data** (`absentees.xls`)
  3. **GM-R 1.2.11 Report on Presenties Data** (`presentees.xls`)
- Automatic generation of the official **DSR Attendance PDF Report** via `report_generator.py`!

All downloads, configs, and outputs are strictly stored inside:
`e:\Google Antigravity\DSR_App_Website\automate_epts\`

---

## Folder Layout
```
automate_epts/
├── config.json              # Saved credentials (User ID: DPOA3698, Password)
├── downloads/               # All downloaded .xls files and generated PDF reports
│   ├── raw_dsr.xls
│   ├── absentees.xls
│   ├── presentees.xls
│   └── Official_DSR_Report_<date>.pdf
├── dsr_auto_download.py     # Complete automated download & report pipeline
├── epts_automation.py       # Core Playwright automation & interactive CLI
├── run_automation.bat       # 1-click Windows launcher
└── README.md
```

---

## How to Run Anytime

### Method 1: Double-Click
Simply double-click [`run_automation.bat`](run_automation.bat) inside the `automate_epts` folder.

### Method 2: Command Line
```powershell
.venv\Scripts\python automate_epts\dsr_auto_download.py
```
When prompted, enter the 6-digit SMS OTP sent to your phone, and the pipeline will automatically perform all downloads and generate the official PDF report!
