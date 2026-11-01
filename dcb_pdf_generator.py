"""Generate pixel-accurate Gram Panchayat Wise DCB PDF report matching official department format."""

from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

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
    force_regenerate: bool = False,
    report_date_str: Optional[str] = None,
) -> tuple[str, bytes]:
    """Return filename and bytes of the generated DCB report for the district."""
    safe_dist = district_name.strip().replace(" ", "_").title()
    reports_dir = Path(__file__).resolve().parent / "data" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = reports_dir / f"{safe_dist}_House_Tax_DCB_Report.pdf"

    if not force_regenerate and pdf_path.exists() and pdf_path.stat().st_size > 1000:
        return pdf_path.name, pdf_path.read_bytes()

    content = generate_dcb_pdf(
        district_name=district_name,
        output_path_or_buffer=pdf_path,
        report_date_str=report_date_str,
    )
    return pdf_path.name, content


def generate_dcb_pdf(
    district_name: str = "Khammam",
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
        topMargin=22,
        bottomMargin=28,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DCBTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13.5,
        leading=16,
        alignment=1,  # Centered
        textColor=colors.HexColor("#0B5ED7"),
        spaceAfter=10,
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
    col_widths = [26, 76, 96, 52, 58, 60, 54, 58, 60, 46, 52, 58, 62, 36]

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
        "Write off\ncurrent",
        "Balance\nArrears",
        "Balance\nCurrent",
        "Balance\nTotal",
        "%",
    ]

    header_row = [Paragraph(h.replace("\n", "<br/>"), cell_hdr_style) for h in headers]

    flowables = []

    # Title is placed on Page 1
    flowables.append(Paragraph(f"Gram Panchayat Wise DCB status as on {report_date_str}", title_style))

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
        tot_wo = m_df["write_off"].sum()
        tot_b_arr = m_df["balance_arrear"].sum()
        tot_b_cur = m_df["balance_current"].sum()
        tot_b_tot = m_df["balance_total"].sum()
        tot_pct = int(round(tot_c_tot / tot_d_tot * 100)) if tot_d_tot > 0 else 0

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
            Paragraph(format_indian_currency(tot_wo), cell_total_num),
            Paragraph(format_indian_currency(tot_b_arr), cell_total_num),
            Paragraph(format_indian_currency(tot_b_cur), cell_total_num),
            Paragraph(format_indian_currency(tot_b_tot), cell_total_num),
            Paragraph(str(tot_pct), cell_pct_style),
        ]

        # Chunk the mandal rows into pages
        gp_records = m_df.to_dict(orient="records")
        total_gps = len(gp_records)
        cursor = 0

        while cursor < total_gps:
            if not is_first_page:
                flowables.append(PageBreak())
            is_first_page = False

            # Check how many rows can fit on this page
            # If remaining rows + 1 (total row) <= 24, fit all and add total row
            remaining = total_gps - cursor
            if remaining + 1 <= 24:
                chunk_size = remaining
                is_last_chunk_of_mandal = True
            elif remaining <= 23:
                # If 23 remaining, putting all 23 leaves 1 total row for next page alone.
                # Better to put 21-22 rows now so next page has some rows plus total
                chunk_size = 21
                is_last_chunk_of_mandal = False
            else:
                chunk_size = 23
                is_last_chunk_of_mandal = False

            chunk = gp_records[cursor : cursor + chunk_size]
            table_data = [header_row]
            table_styles = [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                ("LEFTPADDING", (0, 0), (-1, -1), 2.5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2.5),
            ]

            for idx, r in enumerate(chunk):
                s_no = cursor + idx + 1
                pct_val = int(round(r.get("calc_percentage", 0)))
                row = [
                    Paragraph(str(s_no), cell_body_center),
                    Paragraph(r.get("mandal", ""), cell_body_left),
                    Paragraph(r.get("panchayat", ""), cell_body_left),
                    Paragraph(format_indian_currency(r.get("demand_arrear", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("demand_current", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("demand_total", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("collection_arrear", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("collection_current", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("collection_total", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("write_off", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("balance_arrear", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("balance_current", 0)), cell_body_right),
                    Paragraph(format_indian_currency(r.get("balance_total", 0)), cell_body_right),
                    Paragraph(str(pct_val), cell_pct_style),
                ]
                row_idx = len(table_data)
                table_data.append(row)

                # Set % background to official green badge
                table_styles.append(("BACKGROUND", (13, row_idx), (13, row_idx), colors.HexColor("#16874e")))

            if is_last_chunk_of_mandal:
                tot_idx = len(table_data)
                table_data.append(total_row)
                table_styles.append(("BACKGROUND", (13, tot_idx), (13, tot_idx), colors.HexColor("#16874e")))
                table_styles.append(("SPAN", (0, tot_idx), (1, tot_idx)))  # Span S.No and Mandal Name

            t = Table(table_data, colWidths=col_widths, repeatRows=1)
            t.setStyle(TableStyle(table_styles))
            flowables.append(t)

            cursor += chunk_size

    doc.build(flowables, canvasmaker=NumberedCanvas)

    if isinstance(target, io.BytesIO):
        return target.getvalue()
    elif isinstance(target, (str, Path)):
        return Path(target).read_bytes()
    return buffer.getvalue()
