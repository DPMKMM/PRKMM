"""Generate pixel-accurate Gram Panchayat Wise DCB PDF report matching official department format."""

from __future__ import annotations

import io
import math
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Rect, String

import tax_service


def format_indian_currency(val: float | int | str) -> str:
    """Format a number into Indian comma notation (e.g., 1,97,509)."""
    try:
        n = int(round(float(val)))
    except (ValueError, TypeError):
        return str(val) if val is not None else "0"
    if n == 0:
        return "0"
    is_neg = n < 0
    s = str(abs(n))
    if len(s) <= 3:
        res = s
    else:
        last3 = s[-3:]
        rest = s[:-3]
        groups = []
        while len(rest) > 2:
            groups.insert(0, rest[-2:])
            rest = rest[:-2]
        if rest:
            groups.insert(0, rest)
        res = ",".join(groups) + "," + last3
    return f"-{res}" if is_neg else res


def get_gradient_color(pct: float | int) -> tuple[str, str]:
    """Return (bg_hex, text_hex) for a smooth 3-color Green -> Yellow -> Red gradient scale.
    Highest collection (100%) = Green (#16A34A)
    Medium collection (50%) = Yellow (#EAB308)
    Lowest collection (0%) = Red (#DC2626)
    """
    try:
        p = max(0.0, min(100.0, float(pct)))
    except (ValueError, TypeError):
        p = 0.0

    if p <= 50.0:
        t = p / 50.0
        # Red (220, 38, 38) -> Yellow (234, 179, 8)
        r = int(220 + t * (234 - 220))
        g = int(38 + t * (179 - 38))
        b = int(38 + t * (8 - 38))
    else:
        t = (p - 50.0) / 50.0
        # Yellow (234, 179, 8) -> Green (22, 163, 74)
        r = int(234 + t * (22 - 234))
        g = int(179 + t * (163 - 179))
        b = int(8 + t * (74 - 8))

    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    text_color = "#000000" if lum > 0.55 else "#FFFFFF"
    hex_bg = f"#{r:02X}{g:02X}{b:02X}"
    return hex_bg, text_color


def make_pct_flowable(pct: float | int, h_row: float, font_size: float = 7.0) -> Drawing:
    """Create a 'line column type' meter for the % column in PDF:
    Displays the bold percentage text with a proportional progress line bar underneath.
    """
    try:
        p = max(0, min(100, int(round(float(pct)))))
    except (ValueError, TypeError):
        p = 0
    bg_hex, _ = get_gradient_color(p)
    w_draw = 33.0
    h_draw = max(13.0, min(h_row - 2.0, 19.0))
    d = Drawing(w_draw, h_draw)

    text_y = h_draw / 2.0 + 1.2
    bar_y = max(1.5, h_draw / 2.0 - 5.2)
    bar_h = 3.2

    # Percentage number
    d.add(String(w_draw / 2.0, text_y, f"{p}%", fontName="Helvetica-Bold", fontSize=font_size, textAnchor="middle", fillColor=colors.HexColor("#111827")))
    # Track line
    d.add(Rect(0, bar_y, w_draw, bar_h, fillColor=colors.HexColor("#E2E8F0"), strokeColor=None, rx=1.5, ry=1.5))
    # Filled progress bar line
    bar_w = max(0.0, min(w_draw, w_draw * (p / 100.0)))
    if bar_w > 0:
        d.add(Rect(0, bar_y, max(bar_w, 1.5), bar_h, fillColor=colors.HexColor(bg_hex), strokeColor=None, rx=1.5, ry=1.5))
    return d


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print 'Page X of Y' on every page."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._saved_page_states: List[Dict[str, Any]] = []

    def showPage(self) -> None:
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self) -> None:
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count: int) -> None:
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#222222"))
        page_str = f"Page {self._pageNumber} of {page_count}"
        # Landscape A4 width is 841.89 pt
        self.drawCentredString(841.89 / 2.0, 16, page_str)
        self.restoreState()


def get_or_generate_dcb_pdf(
    district_name: str = "Khammam",
    mandal_name: Optional[str] = None,
    force_regenerate: bool = True,
    report_date_str: Optional[str] = None,
) -> tuple[str, bytes]:
    """Return filename and bytes of the generated DCB report for the district / mandal."""
    safe_dist = district_name.strip().replace(" ", "_").title()
    safe_mandal = ""
    is_single_mandal = bool(mandal_name and mandal_name.strip().lower() not in ("all", "all mandals", ""))
    if is_single_mandal and mandal_name:
        safe_mandal = "_" + mandal_name.strip().replace(" ", "_").title()

    reports_dir = Path(__file__).resolve().parent / "data" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = reports_dir / f"{safe_dist}{safe_mandal}_House_Tax_DCB_Report.pdf"

    if not force_regenerate and pdf_path.exists() and pdf_path.stat().st_size > 1000:
        return pdf_path.name, pdf_path.read_bytes()

    content = generate_dcb_pdf(
        district_name=district_name,
        mandal_name=mandal_name,
        output_path_or_buffer=pdf_path,
        report_date_str=report_date_str,
    )
    return pdf_path.name, content


def generate_dcb_pdf(
    district_name: str = "Khammam",
    mandal_name: Optional[str] = None,
    output_path_or_buffer: Any = None,
    report_date_str: Optional[str] = None,
) -> bytes:
    """Generate the official landscape Gram Panchayat Wise DCB PDF report.
    Returns bytes and writes to output_path_or_buffer if provided.
    """
    df = tax_service.get_df()

    if district_name and district_name.lower() not in ("all", "all districts"):
        df_dist = df[df["district"].str.lower() == district_name.strip().lower()].copy()
    else:
        df_dist = df.copy()

    is_single_mandal = bool(mandal_name and mandal_name.strip().lower() not in ("all", "all mandals", ""))
    if is_single_mandal and mandal_name:
        df_dist = df_dist[df_dist["mandal"].str.lower() == mandal_name.strip().lower()].copy()

    if report_date_str is None:
        report_date_str = datetime.now().strftime("%d-%b-%Y")

    # Document setup: Landscape A4 with 24pt left/right margins, 22pt top, 28pt bottom
    buffer = io.BytesIO()
    target = output_path_or_buffer if isinstance(output_path_or_buffer, (str, Path)) else buffer

    doc = SimpleDocTemplate(
        str(target) if isinstance(target, (str, Path)) else target,
        pagesize=landscape(A4),
        leftMargin=24,
        rightMargin=24,
        topMargin=16,
        bottomMargin=22,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DCBTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=15,
        alignment=1,  # Centered
        textColor=colors.HexColor("#0B5ED7"),
        spaceAfter=6,
    )

    cell_hdr_style = ParagraphStyle(
        "DCBCellHdr",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8.5,
        alignment=1,  # Center
        textColor=colors.black,
    )

    cell_body_left = ParagraphStyle(
        "DCBCellBodyLeft",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=8.5,
        alignment=0,  # Left
        textColor=colors.black,
    )

    cell_body_right = ParagraphStyle(
        "DCBCellBodyRight",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=8.5,
        alignment=2,  # Right
        textColor=colors.black,
    )

    cell_body_center = ParagraphStyle(
        "DCBCellBodyCenter",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=8.5,
        alignment=1,  # Center
        textColor=colors.black,
    )

    cell_pct_style = ParagraphStyle(
        "DCBCellPct",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
        alignment=1,  # Center
        textColor=colors.white,
    )

    cell_total_label = ParagraphStyle(
        "DCBCellTotalLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8.5,
        alignment=0,
        textColor=colors.black,
    )

    cell_total_num = ParagraphStyle(
        "DCBCellTotalNum",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=8.5,
        alignment=2,
        textColor=colors.black,
    )

    # Column widths summing to 794 pt (fits 841.89 pt page with 24 pt margins)
    col_widths = [28, 82, 110, 54, 60, 64, 56, 60, 64, 54, 60, 64, 38]

    headers = [
        "S No",
        "Mandal Name",
        "Panchayat Name",
        "Demand\nArreas",
        "Demand\nCurrent",
        "Demand\nTotal",
        "Collection\nArrears",
        "Collection\nCurrent",
        "Collection\nTotal",
        "Balance\nArrears",
        "Balance\nCurrent",
        "Balance\nTotal",
        "%",
    ]

    header_row = [Paragraph(h.replace("\n", "<br/>"), cell_hdr_style) for h in headers]

    flowables = []

    # Title text based on District level vs Mandal level
    if is_single_mandal and mandal_name:
        clean_mandal = mandal_name.strip().title()
        title_text = f"{clean_mandal} Mandal - Gram Panchayat Wise DCB status as on {report_date_str}"
    else:
        clean_dist = district_name.strip().title() if district_name and district_name.lower() not in ("all", "all districts") else "State"
        title_text = f"{clean_dist} District - Gram Panchayat Wise DCB status as on {report_date_str}"

    # Group by Mandal
    mandals = sorted(df_dist["mandal"].unique())
    is_first_page = True

    # Row capacity per page
    # Page 1 has title so max rows is 22; subsequent pages have no title so max rows is 24
    for m_idx, mandal_name in enumerate(mandals):
        m_df = df_dist[df_dist["mandal"] == mandal_name].copy()
        # Sort GPs within mandal by percentage descending, then demand_total descending
        m_df = m_df.sort_values(by=["calc_percentage", "demand_total", "panchayat"], ascending=[False, False, True])

        # Calculate mandal totals
        tot_d_arr = m_df["demand_arrear"].sum()
        tot_d_cur = m_df["demand_current"].sum()
        tot_d_tot = m_df["demand_total"].sum()
        tot_c_arr = m_df["collection_arrear"].sum()
        tot_c_cur = m_df["collection_current"].sum()
        tot_c_tot = m_df["collection_total"].sum()
        tot_b_arr = m_df["balance_arrear"].sum()
        tot_b_cur = m_df["balance_current"].sum()
        tot_b_tot = m_df["balance_total"].sum()
        tot_pct = int(round(tot_c_tot / tot_d_tot * 100)) if tot_d_tot > 0 else 0

        tot_bg_hex, tot_fg_hex = get_gradient_color(tot_pct)
        tot_pct_style = ParagraphStyle(
            f"TotPct_{m_idx}",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9,
            alignment=1,
            textColor=colors.HexColor(tot_fg_hex),
        )

        total_row = [
            Paragraph("", cell_total_label),
            Paragraph(f"{mandal_name} Total", cell_total_label),
            Paragraph("", cell_total_label),
            Paragraph(format_indian_currency(tot_d_arr), cell_total_num),
            Paragraph(format_indian_currency(tot_d_cur), cell_total_num),
            Paragraph(format_indian_currency(tot_d_tot), cell_total_num),
            Paragraph(format_indian_currency(tot_c_arr), cell_total_num),
            Paragraph(format_indian_currency(tot_c_cur), cell_total_num),
            Paragraph(format_indian_currency(tot_c_tot), cell_total_num),
            Paragraph(format_indian_currency(tot_b_arr), cell_total_num),
            Paragraph(format_indian_currency(tot_b_cur), cell_total_num),
            Paragraph(format_indian_currency(tot_b_tot), cell_total_num),
            Paragraph(str(tot_pct), tot_pct_style),
        ]

        # Chunk the mandal rows into pages using best fit
        # Below 25 to 28 GPs -> single page. Around 40 GPs -> 2 pages.
        gp_records = m_df.to_dict(orient="records")
        total_gps = len(gp_records)
        num_pages_mandal = max(1, math.ceil(total_gps / 28))
        gps_per_page = math.ceil(total_gps / num_pages_mandal)

        cursor = 0
        for page_idx in range(num_pages_mandal):
            if not is_first_page:
                flowables.append(PageBreak())
            is_first_page = False

            # Every page displays the official title with District or Mandal Name
            flowables.append(Paragraph(title_text, title_style))

            is_last_chunk_of_mandal = (page_idx == num_pages_mandal - 1)
            chunk_size = total_gps - cursor if is_last_chunk_of_mandal else gps_per_page
            chunk = gp_records[cursor : cursor + chunk_size]

            # Calculate exact available vertical height to fill the entire page space
            avail_h = 555.27 - 28.0 - 14.0
            h_hdr = 22.0
            n_data_and_total = len(chunk) + (1 if is_last_chunk_of_mandal else 0)
            h_row = (avail_h - h_hdr) / float(n_data_and_total)

            # Proportional font size and leading based on expanded row height
            if h_row >= 24.0:
                f_sz = 8.2
                f_lead = 9.8
            elif h_row >= 20.0:
                f_sz = 7.6
                f_lead = 9.0
            else:
                f_sz = 7.0
                f_lead = 8.2

            cur_cell_left = ParagraphStyle(f"CBL_{m_idx}_{page_idx}", parent=styles["Normal"], fontName="Helvetica", fontSize=f_sz, leading=f_lead, alignment=0, textColor=colors.black)
            cur_cell_right = ParagraphStyle(f"CBR_{m_idx}_{page_idx}", parent=styles["Normal"], fontName="Helvetica", fontSize=f_sz, leading=f_lead, alignment=2, textColor=colors.black)
            cur_cell_center = ParagraphStyle(f"CBC_{m_idx}_{page_idx}", parent=styles["Normal"], fontName="Helvetica", fontSize=f_sz, leading=f_lead, alignment=1, textColor=colors.black)

            tot_cell_label = ParagraphStyle(f"TL_{m_idx}_{page_idx}", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=f_sz, leading=f_lead, alignment=0, textColor=colors.black)
            tot_cell_num = ParagraphStyle(f"TN_{m_idx}_{page_idx}", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=f_sz, leading=f_lead, alignment=2, textColor=colors.black)

            table_data = [header_row]
            row_heights = [h_hdr]
            table_styles = [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2.2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2.2),
            ]

            for idx, r in enumerate(chunk):
                s_no = cursor + idx + 1
                pct_val = int(round(r.get("calc_percentage", 0)))
                row_bg_hex, row_fg_hex = get_gradient_color(pct_val)
                row_pct_style = ParagraphStyle(
                    f"RowPct_{s_no}_{cursor}_{idx}",
                    parent=styles["Normal"],
                    fontName="Helvetica-Bold",
                    fontSize=f_sz + 0.3,
                    leading=f_lead,
                    alignment=1,
                    textColor=colors.HexColor(row_fg_hex),
                )

                row = [
                    Paragraph(str(s_no), cur_cell_center),
                    Paragraph(r.get("mandal", ""), cur_cell_left),
                    Paragraph(r.get("panchayat", ""), cur_cell_left),
                    Paragraph(format_indian_currency(r.get("demand_arrear", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("demand_current", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("demand_total", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("collection_arrear", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("collection_current", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("collection_total", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("balance_arrear", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("balance_current", 0)), cur_cell_right),
                    Paragraph(format_indian_currency(r.get("balance_total", 0)), cur_cell_right),
                    make_pct_flowable(pct_val, h_row, f_sz),
                ]
                row_idx = len(table_data)
                table_data.append(row)
                row_heights.append(h_row)

            if is_last_chunk_of_mandal:
                tot_idx = len(table_data)
                cur_total_row = [
                    Paragraph("", tot_cell_label),
                    Paragraph(f"{mandal_name} Total", tot_cell_label),
                    Paragraph("", tot_cell_label),
                    Paragraph(format_indian_currency(tot_d_arr), tot_cell_num),
                    Paragraph(format_indian_currency(tot_d_cur), tot_cell_num),
                    Paragraph(format_indian_currency(tot_d_tot), tot_cell_num),
                    Paragraph(format_indian_currency(tot_c_arr), tot_cell_num),
                    Paragraph(format_indian_currency(tot_c_cur), tot_cell_num),
                    Paragraph(format_indian_currency(tot_c_tot), tot_cell_num),
                    Paragraph(format_indian_currency(tot_b_arr), tot_cell_num),
                    Paragraph(format_indian_currency(tot_b_cur), tot_cell_num),
                    Paragraph(format_indian_currency(tot_b_tot), tot_cell_num),
                    make_pct_flowable(tot_pct, h_row, f_sz),
                ]
                table_data.append(cur_total_row)
                row_heights.append(h_row)
                table_styles.append(("SPAN", (0, tot_idx), (1, tot_idx)))  # Span S.No and Mandal Name

            t = Table(table_data, colWidths=col_widths, rowHeights=row_heights, repeatRows=1)
            t.setStyle(TableStyle(table_styles))
            flowables.append(t)

            cursor += chunk_size

    doc.build(flowables, canvasmaker=NumberedCanvas)

    if isinstance(target, io.BytesIO):
        return target.getvalue()
    elif isinstance(target, (str, Path)):
        return Path(target).read_bytes()
    return buffer.getvalue()
