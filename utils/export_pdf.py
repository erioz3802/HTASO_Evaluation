"""PDF export functionality using ReportLab."""
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image


def generate_pdf_report(data: Dict[str, Any], logo_path: Optional[Path] = None) -> BytesIO:
    """Generate a PDF report from evaluation data.

    Args:
        data: Evaluation data dictionary
        logo_path: Optional path to logo image

    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    # Setup styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="Heading1Center",
        parent=styles['Heading1'],
        alignment=1  # Center alignment
    ))

    story = []

    # Add logo if available
    if logo_path and logo_path.exists():
        try:
            img = Image(str(logo_path), width=120, height=120)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 12))
        except Exception:
            pass  # Skip logo if there's an error

    # Title
    story.append(Paragraph("HTASO Umpire Evaluation Report", styles["Heading1Center"]))
    story.append(Spacer(1, 12))

    # Prepared date
    prepared_on = datetime.now().strftime('%B %d, %Y')
    story.append(Paragraph(f"Prepared on {prepared_on}", styles["Normal"]))
    story.append(Spacer(1, 18))

    # Basic details table
    details_data = [
        ["Evaluator Name", data.get("evaluator_name", "N/A")],
        ["Trainer Name", data.get("trainer_name", "N/A")],
        ["Training Date", data.get("training_date", "N/A")],
        ["Observation Date", data.get("observation_date", "N/A") or "N/A"],
        ["Location", data.get("training_location", "N/A") or "N/A"],
        ["Type of Evaluation", data.get("eval_type", "N/A") or "N/A"],
        ["Submission Date", data.get("submission_date", "N/A")],
        ["Rated Items", str(data.get("rated_item_count", 0))],
    ]

    # Calculate HTASO average and rank
    total_score = data.get("total_score", 0)
    total_possible = data.get("total_possible", 0)
    if total_possible and total_possible > 0:
        htaso_avg = 6.0 - (total_score / (total_possible / 5.0))
        rank = round(htaso_avg)
        average_score = total_score / total_possible
        details_data.append(["HTASO Average", f"{htaso_avg:.2f}"])
        details_data.append(["Rank", str(rank)])
        details_data.append(["Percentage", f"{average_score:.0%}"])
    else:
        htaso_avg = None
        rank = None
        details_data.append(["HTASO Average", "N/A"])

    details_table = Table(details_data, colWidths=[180, 360])
    details_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1D3557")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("BOX", (0, 0), (-1, -1), 0.75, colors.grey),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 18))

    # Section scores table
    section_totals = data.get("section_totals", [])
    if section_totals:
        story.append(Paragraph("Section Scores", styles["Heading2"]))
        section_data = [["Section", "HTASO Avg", "Rank", "Percentage"]]
        for entry in section_totals:
            sec_possible = entry.get("possible", 0)
            sec_score = entry.get("score", 0)
            if sec_possible and sec_possible > 0:
                sec_htaso_avg = 6.0 - (sec_score / (sec_possible / 5.0))
                sec_rank = round(sec_htaso_avg)
                percent_text = f"{entry.get('percentage', 0):.0%}"
                section_data.append([
                    entry.get("section", "General"),
                    f"{sec_htaso_avg:.2f}",
                    str(sec_rank),
                    percent_text
                ])
            else:
                section_data.append([
                    entry.get("section", "General"),
                    "—", "—", "N/A"
                ])

        section_table = Table(section_data, colWidths=[200, 100, 80, 160])
        section_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2A9D8F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("BOX", (0, 0), (-1, -1), 0.75, colors.grey),
        ]))
        story.append(section_table)
        story.append(Spacer(1, 18))

    # Overall score summary
    if htaso_avg is not None:
        story.append(Paragraph(
            f"Overall HTASO Average: {htaso_avg:.2f} | Rank: {rank}",
            styles["Normal"]
        ))
    else:
        story.append(Paragraph("Overall Score: N/A", styles["Normal"]))
    story.append(Spacer(1, 18))

    # Ratings grouped by section
    ratings = data.get("ratings", [])
    if ratings:
        # Group ratings by section and subsection
        from collections import OrderedDict
        grouped = OrderedDict()
        for item in ratings:
            section_name = item.get("section") or "General"
            subsection_name = item.get("subsection") or "Criteria"
            if section_name not in grouped:
                grouped[section_name] = OrderedDict()
            if subsection_name not in grouped[section_name]:
                grouped[section_name][subsection_name] = []
            grouped[section_name][subsection_name].append(item)

        # Add ratings to PDF
        for section, subsections in grouped.items():
            story.append(Paragraph(section, styles["Heading2"]))
            for subsection, items in subsections.items():
                story.append(Paragraph(subsection, styles["Heading3"]))
                for item in items:
                    selection = item.get("selection") or "Not Rated"
                    prompt = item.get("prompt", "")
                    story.append(Paragraph(f"• {prompt} ({selection})", styles["Normal"]))
                story.append(Spacer(1, 6))
            story.append(Spacer(1, 12))

    # Recommendation
    story.append(Paragraph("Overall Recommendation", styles["Heading2"]))
    recommendation = data.get("recommendation") or "Not Selected"
    story.append(Paragraph(recommendation, styles["Normal"]))
    story.append(Spacer(1, 18))

    # Comments
    comments = data.get("comments", {})
    if comments:
        story.append(Paragraph("Evaluator Comments", styles["Heading2"]))
        comment_sections = [
            ("Strengths Observed", "strengths"),
            ("Areas for Improvement", "improvement"),
            ("Development Recommendations", "development"),
            ("Overall Assessment Comments", "overall")
        ]

        for title, key in comment_sections:
            text = comments.get(key, "")
            if text:
                story.append(Paragraph(title, styles["Heading3"]))
                # Replace newlines with HTML breaks
                cleaned = text.replace("\n", "<br/>")
                story.append(Paragraph(cleaned, styles["Normal"]))
                story.append(Spacer(1, 6))

    # Build PDF
    doc.build(story)

    # Return buffer
    buffer.seek(0)
    return buffer


def get_pdf_filename(evaluator_name: str) -> str:
    """Generate a standard filename for PDF export.

    Args:
        evaluator_name: Name of the evaluator

    Returns:
        Filename string
    """
    # Sanitize filename
    safe_name = "".join(c for c in evaluator_name if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name or "Evaluation"
    timestamp = datetime.now().strftime('%Y%m%d')
    return f"HTASO_Evaluation_{safe_name}_{timestamp}.pdf"
