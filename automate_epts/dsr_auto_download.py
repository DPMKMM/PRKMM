"""
Exact Automated Pipeline for e-Panchayat DSR Report
Downloads in sequence:
  1. GM-R 1.2.7 DSR Raw Data Report -> raw_dsr.xls
  2. Select GP Monitoring -> GM-R 1.2.11 Report on Presenties Data -> presentees.xls
  3. Select GP Monitoring -> GM-R 1.2.10 Report on Absentees Data -> absentees.xls
And executes report_generator.py to produce the official 7-section DSR Attendance PDF report.
"""

import os
import sys
import time
import shutil
from datetime import datetime
from pathlib import Path

from epts_automation import EPTSAutomation, BASE_DIR, DOWNLOADS_DIR, OTP_FILE

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_SCREENSHOT = BASE_DIR / "enlarged_reports.png"
MENU_URL = "https://tgprepanchayat.telangana.gov.in/PSPerformance/DynamicReportsMenu2Array"


def get_my_iframe(page):
    """Returns the content iframe named 'my-iframe' or holding PSPerformance."""
    for f in page.frames:
        if f.name == "my-iframe" or "PSPerformance" in f.url:
            return f
    if len(page.frames) > 2:
        return page.frames[2]
    return None


def download_single_report_with_menu(bot, code: str, key: str, today_str: str) -> Path:
    """
    Downloads a single report from e-Panchayat portal:
    1. Selects 'GP Monitoring' from the top navigation to load/reset the reports iframe.
    2. Waits for 'my-iframe' to load.
    3. Clicks 'Enlarge All' and expands 'DSR REPORTS'.
    4. Clicks the report link matching `code` (e.g. 1.2.7, 1.2.11, 1.2.10).
    5. Sets the date filter to `today_str` (DD/MM/YYYY).
    6. Clicks the Download button and saves file to DOWNLOADS_DIR / f"{key}.xls".
    """
    page = bot.page
    print(f"\n[*] Selecting 'GP Monitoring' from top menu for report {code} ({key})...", flush=True)
    bot.select_menu("GP Monitoring")
    time.sleep(2.5)

    iframe = get_my_iframe(page)
    if not iframe:
        time.sleep(2)
        iframe = get_my_iframe(page)
    if not iframe:
        raise RuntimeError(f"Could not locate 'my-iframe' after selecting GP Monitoring for {code}.")

    try:
        iframe.wait_for_load_state("domcontentloaded", timeout=10000)
    except Exception:
        pass

    # Click 'Enlarge All' to expand all folders
    print("[*] Clicking 'Enlarge All'...", flush=True)
    try:
        enlarge_btn = iframe.locator("text='Enlarge All'").first
        if enlarge_btn.is_visible(timeout=3000):
            enlarge_btn.click()
            time.sleep(1)
    except Exception as e:
        print(f"[-] Note on Enlarge All: {e}", flush=True)

    # Expand 'DSR REPORTS' section
    print("[*] Expanding 'DSR REPORTS'...", flush=True)
    try:
        dsr_header = iframe.locator("text='DSR REPORTS'").first
        if dsr_header.is_visible(timeout=3000):
            dsr_header.click()
            time.sleep(1.5)
    except Exception as e:
        print(f"[-] Note on DSR REPORTS: {e}", flush=True)

    # Locate report link matching code
    print(f"[*] Locating link for {code} ({key})...", flush=True)
    selectors = [
        f"a:has-text('{code}')",
    ]
    if "1.2.7" in code:
        selectors.append("a:has-text('Raw Data')")
    elif "1.2.11" in code:
        selectors.extend(["a:has-text('Presenties')", "a:has-text('Presentees')"])
    elif "1.2.10" in code:
        selectors.append("a:has-text('Absentees')")

    link = None
    for sel in selectors:
        cand = iframe.locator(sel).first
        try:
            if cand.is_visible(timeout=2000):
                link = cand
                break
        except Exception:
            pass

    if not link:
        link = iframe.locator(selectors[0]).first
        link.wait_for(state="visible", timeout=12000)

    print(f"[+] Found link for {code}. Clicking...", flush=True)
    link.click()
    time.sleep(3)

    # Screenshot view
    ss_path = BASE_DIR / f"page_{code.replace('.', '_')}.png"
    try:
        page.screenshot(path=str(ss_path))
        print(f"[+] Saved view screenshot to {ss_path}", flush=True)
    except Exception:
        pass

    # Set Date filter in iframe
    print(f"[*] Setting date to {today_str} in iframe...", flush=True)
    iframe.evaluate(f"""() => {{
        const el = document.getElementById('ContentPlaceHolder1_txtFromDate');
        if (el) {{
            el.removeAttribute('readonly');
            el.value = '{today_str}';
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
        const inputs = document.querySelectorAll("input[id*='Date' i], input[name*='Date' i]");
        for (const inp of inputs) {{
            inp.removeAttribute('readonly');
            inp.value = '{today_str}';
            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    time.sleep(1)

    # Click Download button
    print(f"[*] Waiting for download button for {code}...", flush=True)
    dl_selectors = [
        "input[value*='Download' i]",
        "input[value*='Export' i]",
        "button:has-text('Download')",
        "button:has-text('Export')",
        "a:has-text('Download')",
        "a:has-text('Export')",
        "input[id*='btnExport' i]",
        "input[id*='btnDownload' i]",
        "input[id*='btnSubmit' i]",
    ]
    dl_btn = iframe.locator(", ".join(dl_selectors)).first
    dl_btn.wait_for(state="visible", timeout=15000)

    with page.expect_download(timeout=60000) as dl_info:
        dl_btn.click()

    dl = dl_info.value
    ext = Path(dl.suggested_filename).suffix or ".xls"
    dest = DOWNLOADS_DIR / f"{key}{ext}"
    dl.save_as(str(dest))
    print(f"[SUCCESS] Downloaded {key} -> {dest} (Size: {dest.stat().st_size:,} bytes)", flush=True)

    # Ensure standard .xls copy exists
    xls_dest = DOWNLOADS_DIR / f"{key}.xls"
    if ext != ".xls":
        try:
            shutil.copyfile(dest, xls_dest)
        except Exception:
            pass

    return dest


# Backward compatibility alias
def download_single_report(page, iframe, code, key, today_str):
    dest = DOWNLOADS_DIR / f"{key}.xls"
    return dest


def run_pipeline():
    print("=" * 65, flush=True)
    print("  e-Panchayat Automated DSR Report Generation Pipeline", flush=True)
    print("=" * 65, flush=True)

    app = EPTSAutomation(headless=False)
    try:
        app.ensure_logged_in()

        today_str = datetime.now().strftime("%d/%m/%Y")
        today_dash = datetime.now().strftime("%d-%m-%Y")
        print(f"[*] Target Report Date: {today_str}", flush=True)

        downloaded_paths = {}

        # Step 1: Select GP Monitoring -> Download GM-R 1.2.7 (DSR Raw Data Report)
        print("\n" + "=" * 50, flush=True)
        print("[*] STEP 1: GP Monitoring -> GM-R 1.2.7 DSR Raw Data Report", flush=True)
        print("=" * 50, flush=True)
        try:
            p1 = download_single_report_with_menu(app, "1.2.7", "raw_dsr", today_str)
            downloaded_paths["raw_dsr"] = p1
        except Exception as e:
            print(f"[ERROR] Failed downloading GM-R 1.2.7: {e}", flush=True)

        # Step 2: Select GP Monitoring -> Download GM-R 1.2.11 (Presentees Report)
        print("\n" + "=" * 50, flush=True)
        print("[*] STEP 2: Re-select GP Monitoring -> GM-R 1.2.11 Presentees Report", flush=True)
        print("=" * 50, flush=True)
        try:
            p2 = download_single_report_with_menu(app, "1.2.11", "presentees", today_str)
            downloaded_paths["presentees"] = p2
        except Exception as e:
            print(f"[ERROR] Failed downloading GM-R 1.2.11: {e}", flush=True)

        # Step 3: Select GP Monitoring -> Download GM-R 1.2.10 (Absentees Report)
        print("\n" + "=" * 50, flush=True)
        print("[*] STEP 3: Re-select GP Monitoring -> GM-R 1.2.10 Absentees Report", flush=True)
        print("=" * 50, flush=True)
        try:
            p3 = download_single_report_with_menu(app, "1.2.10", "absentees", today_str)
            downloaded_paths["absentees"] = p3
        except Exception as e:
            print(f"[ERROR] Failed downloading GM-R 1.2.10: {e}", flush=True)

        print("\n" + "=" * 55, flush=True)
        print("[+] Download Summary:", flush=True)
        for k, v in downloaded_paths.items():
            if v and v.exists():
                print(f"    - {k}: {v} ({v.stat().st_size:,} bytes)", flush=True)

        # Step 4: Prepare Report Based on PRKMM Project Code (#reports-district)
        raw_dsr_path = downloaded_paths.get("raw_dsr")
        if raw_dsr_path and raw_dsr_path.exists():
            print("\n" + "=" * 55, flush=True)
            print("[*] Compiling Official 7-Section District Attendance & DSR Report...", flush=True)
            sys.path.insert(0, str(BASE_DIR.parent.resolve()))
            from report_generator import process_attendance_file, generate_pdf

            p_path = downloaded_paths.get("presentees")
            presentees_source = (p_path.name, p_path.read_bytes()) if p_path and p_path.exists() and p_path.stat().st_size > 0 else None

            a_path = downloaded_paths.get("absentees")
            absentees_source = (a_path.name, a_path.read_bytes()) if a_path and a_path.exists() and a_path.stat().st_size > 0 else None

            report = process_attendance_file(
                raw_dsr_path.name,
                raw_dsr_path.read_bytes(),
                presentees_source=presentees_source,
                absentees_source=absentees_source,
            )

            reports_dir = BASE_DIR.parent / "data" / "reports"
            reports_dir.mkdir(parents=True, exist_ok=True)
            output_pdf = reports_dir / f"{report.district_name.replace(' ', '_')}_Official_DSR_Report_{today_dash}.pdf"
            generate_pdf(report, output_pdf)

            cached_pdf = DOWNLOADS_DIR / f"Official_DSR_Report_{today_dash}.pdf"
            cached_pdf.write_bytes(output_pdf.read_bytes())

            print(f"\n[SUCCESS] Final Official 7-Section DSR Attendance PDF Generated:")
            print(f"--> {output_pdf} (Size: {output_pdf.stat().st_size:,} bytes)")
            print(f"District: {report.district_name} | Total GPs: {report.unique_gp_count}")
            print(f"Attendance Submitted: {report.totals.get('attendance_submitted')}")
            print(f"DSR Entered: {report.totals.get('dsr_entered')}")
        else:
            print("[!] Raw DSR file was not available, skipping PDF report generation.", flush=True)

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
