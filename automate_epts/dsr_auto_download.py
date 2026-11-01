"""
Exact Automated Pipeline for e-Panchayat DSR Report
Downloads:
  1. GM-R 1.2.7 DSR Raw Data Report -> raw_dsr.xlsx
  2. GM-R 1.2.10 Report on Absentees Data -> absentees.xlsx
  3. GM-R 1.2.11 Report on Presenties Data -> presentees.xlsx
And runs report_generator.py to produce official DSR Attendance PDF report.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

from epts_automation import EPTSAutomation, BASE_DIR, DOWNLOADS_DIR, OTP_FILE

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_SCREENSHOT = BASE_DIR / "enlarged_reports.png"
MENU_URL = "https://tgprepanchayat.telangana.gov.in/PSPerformance/DynamicReportsMenu2Array"


def get_my_iframe(page):
    """Returns the content iframe named 'my-iframe'."""
    for f in page.frames:
        if f.name == "my-iframe" or "PSPerformance" in f.url:
            return f
    # fallback to frame #2 if present
    if len(page.frames) > 2:
        return page.frames[2]
    return None


def download_single_report(page, iframe, code, key, today_str):
    print(f"\n[*] Navigating to menu in iframe...", flush=True)
    iframe.goto(MENU_URL, wait_until="domcontentloaded")
    time.sleep(2)

    print("[*] Clicking 'Enlarge All'...", flush=True)
    try:
        iframe.locator("text='Enlarge All'").first.click()
        time.sleep(1)
    except Exception as e:
        print(f"[-] Note on Enlarge All: {e}", flush=True)

    print("[*] Expanding 'DSR REPORTS' sub-section...", flush=True)
    try:
        dsr_header = iframe.locator("text='DSR REPORTS'").first
        if dsr_header.is_visible():
            dsr_header.click()
            time.sleep(1.5)
    except Exception as e:
        print(f"[-] Note on DSR REPORTS: {e}", flush=True)

    print(f"[*] Locating report link for {code}...", flush=True)
    link = iframe.locator(f"a:has-text('{code}')").first
    link.wait_for(state="visible", timeout=10000)
    print(f"[+] Found link for {code}. Clicking...", flush=True)
    link.click()
    time.sleep(3)

    ss_path = BASE_DIR / f"page_{code.replace('.', '_')}.png"
    page.screenshot(path=str(ss_path))
    print(f"[+] Saved view screenshot to {ss_path}", flush=True)

    print(f"[*] Setting date to {today_str} in iframe...", flush=True)
    iframe.evaluate(f"""() => {{
        const el = document.getElementById('ContentPlaceHolder1_txtFromDate');
        if (el) {{
            el.removeAttribute('readonly');
            el.value = '{today_str}';
            el.dispatchEvent(new Event('change'));
        }}
        const inputs = document.querySelectorAll("input[id*='Date' i], input[name*='Date' i]");
        for (const inp of inputs) {{
            inp.removeAttribute('readonly');
            inp.value = '{today_str}';
            inp.dispatchEvent(new Event('change'));
        }}
    }}""")
    time.sleep(1)

    print("[*] Clicking 'Download' / 'Download Excel' button and waiting for file...", flush=True)
    dl_btn = iframe.locator("input[value*='Download' i], button:has-text('Download'), a:has-text('Download')").first
    dl_btn.wait_for(state="visible", timeout=10000)

    with page.expect_download(timeout=60000) as dl_info:
        dl_btn.click()

    dl = dl_info.value
    ext = Path(dl.suggested_filename).suffix or ".xls"
    dest = DOWNLOADS_DIR / f"{key}{ext}"
    dl.save_as(str(dest))
    print(f"[SUCCESS] Downloaded {key} -> {dest} (Size: {dest.stat().st_size} bytes)", flush=True)
    return dest


def run_pipeline():
    print("=" * 60, flush=True)
    print(" e-Panchayat Automated DSR Report Generation Pipeline", flush=True)
    print("=" * 60, flush=True)

    app = EPTSAutomation(headless=False)
    try:
        app.ensure_logged_in()

        print("\n[*] Navigating to GP Monitoring...", flush=True)
        app.select_menu("GP Monitoring")
        time.sleep(3)

        iframe = get_my_iframe(app.page)
        if not iframe:
            raise RuntimeError("Could not find 'my-iframe' content frame.")
        print(f"[+] Content iframe identified: {iframe.url}", flush=True)

        today_str = datetime.now().strftime("%d/%m/%Y")
        print(f"[*] Target Report Date: {today_str}", flush=True)

        downloaded_paths = {}

        # 1. GM-R 1.2.7 DSR Raw Data Report
        try:
            p1 = download_single_report(app.page, iframe, "1.2.7", "raw_dsr", today_str)
            downloaded_paths["raw_dsr"] = p1
        except Exception as e:
            print(f"[ERROR] Failed downloading 1.2.7: {e}", flush=True)

        # 2. GM-R 1.2.10 Report on Absentees Data
        try:
            p2 = download_single_report(app.page, iframe, "1.2.10", "absentees", today_str)
            downloaded_paths["absentees"] = p2
        except Exception as e:
            print(f"[ERROR] Failed downloading 1.2.10: {e}", flush=True)

        # 3. GM-R 1.2.11 Report on Presenties Data
        try:
            p3 = download_single_report(app.page, iframe, "1.2.11", "presentees", today_str)
            downloaded_paths["presentees"] = p3
        except Exception as e:
            print(f"[ERROR] Failed downloading 1.2.11: {e}", flush=True)

        print("\n" + "=" * 55, flush=True)
        print("[+] Download Summary:", flush=True)
        for k, v in downloaded_paths.items():
            print(f"    - {k}: {v} ({v.stat().st_size} bytes)", flush=True)

        # Automated PDF Report Generation
        raw_dsr_path = downloaded_paths.get("raw_dsr")
        if raw_dsr_path and raw_dsr_path.exists():
            print("\n" + "=" * 55, flush=True)
            print("[*] Executing report_generator.py to generate Official DSR Attendance PDF...", flush=True)
            cmd = [
                sys.executable,
                str(BASE_DIR.parent / "report_generator.py"),
                str(raw_dsr_path),
            ]
            if "presentees" in downloaded_paths:
                cmd.extend(["--presentees", str(downloaded_paths["presentees"])])
            if "absentees" in downloaded_paths:
                cmd.extend(["--absentees", str(downloaded_paths["absentees"])])

            output_pdf = DOWNLOADS_DIR / f"Official_DSR_Report_{today_str.replace('/', '-')}.pdf"
            cmd.extend(["--output", str(output_pdf)])

            print(f"[*] Command: {' '.join(cmd)}", flush=True)
            proc = subprocess.run(cmd, capture_output=True, text=True)
            print(proc.stdout, flush=True)
            if proc.stderr:
                print(proc.stderr, flush=True)

            if output_pdf.exists():
                print(f"\n[SUCCESS] Final Official DSR Attendance PDF Generated:\n--> {output_pdf} (Size: {output_pdf.stat().st_size} bytes)", flush=True)
        else:
            print("[!] Raw DSR file was not downloaded, skipping PDF report generation.", flush=True)

    except Exception as e:
        print(f"\n[ERROR] Pipeline encountered an error: {e}", flush=True)
        import traceback
        traceback.print_exc()
    finally:
        print("[*] Closing browser session...", flush=True)
        app.close()
        print("[+] Done.", flush=True)


if __name__ == "__main__":
    run_pipeline()
