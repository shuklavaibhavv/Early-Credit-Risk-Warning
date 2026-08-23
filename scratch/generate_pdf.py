"""
Generate Credit Opportunity Memorandum PDF for Credit Suisse Group AG.
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


def build_pdf():
    pdf_path = Path("/Users/vaibhavshukla/Desktop/JPMC/credit_risk_project/reports/Credit_Opportunity_Memorandum_CS.pdf")
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=TA_CENTER,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=TA_CENTER,
        spaceAfter=3,
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6,
    )

    h3_style = ParagraphStyle(
        'SectionH3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=8,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    th_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=TA_LEFT,
    )

    td_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b'),
        alignment=TA_LEFT,
    )

    td_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a'),
        alignment=TA_LEFT,
    )

    story = []

    # Title Block
    story.append(Paragraph("CREDIT OPPORTUNITY MEMORANDUM", title_style))
    story.append(Paragraph("Credit Suisse Group AG (CS) | Financials — Global Systemically Important Bank (G-SIB)", subtitle_style))
    story.append(Paragraph("Prepared using the Corporate Credit Risk Early-Warning System | Confidential — For Internal Discussion Purposes", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0f172a'), spaceBefore=0, spaceAfter=10))

    # Deal Context
    story.append(Paragraph("Deal Context", h2_style))
    story.append(Paragraph(
        "This memorandum presents a retrospective credit risk assessment of Credit Suisse Group AG (“CS” or “the Bank”), evaluated through a "
        "proprietary composite early-warning model that combines bank-specific accounting ratios with a market-implied Merton distance-to-default "
        "measure. The purpose of this exercise is to demonstrate that CS's credit deterioration was observable and quantifiable well in advance of its "
        "emergency acquisition by UBS in March 2023 — the model's composite risk score crossed our defined distress threshold in 2022Q2, three "
        "quarters ahead of resolution, with the market-based signal (distance-to-default) providing the earliest confirmation.",
        body_style
    ))

    # Executive Summary
    story.append(Paragraph("Executive Summary", h2_style))
    story.append(Paragraph("• <b>Credit Suisse's composite credit risk score rose steadily from 57.1% (2022Q1) to 67.3%</b> in its final full trading quarter (2023Q1), crossing our 60% distress threshold in 2022Q2 — approximately three quarters before the UBS-brokered emergency rescue announced in March 2023.", bullet_style))
    story.append(Paragraph("• <b>Distance-to-default (Merton model) flagged the earliest and sharpest signal:</b> DD fell from 3.05 (2022Q1, baseline solvency) to 1.74 (2022Q2, implied PD 4.12%), well ahead of the accounting ratios' deterioration.", bullet_style))
    story.append(Paragraph("• <b>Peer comparison against JPMorgan Chase and Goldman Sachs</b> — both of which remained range-bound between 40–50% throughout the same period — confirms the deterioration was CS-specific, not sector-wide.", bullet_style))
    story.append(Paragraph("• <b>Recommendation / Rating: <font color='#dc2626'>HIGH RISK — DISTRESS ZONE</font></b> (Composite Score 67.3%, pre-resolution). Consistent with the actual outcome of external resolution via UBS acquisition.", bullet_style))

    # Business & Industry Overview
    story.append(Paragraph("Business & Industry Overview", h2_style))
    story.append(Paragraph(
        "Credit Suisse was a global systemically important bank headquartered in Zurich, operating across wealth management, investment banking, and "
        "Swiss universal banking. Heading into 2022, the Bank was already contending with a series of legacy risk-management and litigation issues "
        "(including the Archegos and Greensill episodes) that had eroded market confidence ahead of the period covered by this analysis.",
        body_style
    ))
    story.append(Paragraph(
        "The broader banking sector entered a period of acute stress in 2022–23 as aggressive central bank rate hikes compressed the value of fixed-income asset holdings and tightened funding conditions industry-wide, culminating in the March 2023 failures of Silicon Valley Bank and Signature Bank in the U.S. CS's collapse occurred within this same window but was driven primarily by idiosyncratic, CS-specific deposit flight rather than the asset-liability mismatch that drove the U.S. regional bank failures — a distinction this analysis supports through the deposit and funding data below.",
        body_style
    ))

    # Credit Analysis
    story.append(Paragraph("Credit Analysis", h2_style))
    story.append(Paragraph("Composite Risk Score Trajectory", h3_style))
    story.append(Paragraph(
        "The model's composite score, derived from a logistic regression fit against sector-appropriate bank signals (CET1 ratio, loan-to-deposit ratio, non-performing loan ratio, net interest margin) and distance-to-default, tracked a consistent upward trajectory through five quarters of active trading data:",
        body_style
    ))

    # Table 1: Composite Risk Score
    t1_data = [
        [Paragraph("Quarter", th_style), Paragraph("CS Composite Score", th_style), Paragraph("JPM Composite Score", th_style), Paragraph("GS Composite Score", th_style)],
        [Paragraph("2022Q1", td_style), Paragraph("57.1%", td_style), Paragraph("45.0%", td_style), Paragraph("45.1%", td_style)],
        [Paragraph("2022Q2", td_style), Paragraph("<b>61.4%</b> <i>(crosses 60% threshold)</i>", td_bold), Paragraph("44.9%", td_style), Paragraph("49.6%", td_style)],
        [Paragraph("2022Q3", td_style), Paragraph("63.7%", td_style), Paragraph("43.6%", td_style), Paragraph("48.6%", td_style)],
        [Paragraph("2022Q4", td_style), Paragraph("65.2%", td_style), Paragraph("40.2%", td_style), Paragraph("48.4%", td_style)],
        [Paragraph("2023Q1", td_style), Paragraph("<b>67.3%</b> <i>(final active quarter — UBS rescue)</i>", td_bold), Paragraph("44.9%", td_style), Paragraph("49.5%", td_style)],
    ]
    t1 = Table(t1_data, colWidths=[80, 200, 130, 130])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t1)
    story.append(Paragraph("<i>Note: CS was delisted following the March 2023 UBS acquisition. Post-resolution quarters in the underlying dataset carry an imputed distress-floor value and are excluded from this table as they do not represent live market data.</i>", ParagraphStyle('Footnote', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=colors.HexColor('#64748b'), spaceAfter=8)))

    # Distance-to-Default: The Earliest Signal
    story.append(Paragraph("Distance-to-Default: The Earliest Signal", h3_style))
    story.append(Paragraph(
        "The market-implied distance-to-default measure moved ahead of the accounting-based composite score, providing the earliest confirmation of deteriorating solvency:",
        body_style
    ))

    t2_data = [
        [Paragraph("Quarter", th_style), Paragraph("Equity Volatility (&sigma;<sub>E</sub>)", th_style), Paragraph("Distance-to-Default (DD)", th_style), Paragraph("Implied PD (%)", th_style), Paragraph("Status / Milestone", th_style)],
        [Paragraph("2022Q1", td_style), Paragraph("33.8%", td_style), Paragraph("3.05", td_style), Paragraph("0.11%", td_style), Paragraph("Baseline solvency", td_style)],
        [Paragraph("2022Q2", td_style), Paragraph("55.8%", td_style), Paragraph("<b>1.74</b>", td_bold), Paragraph("<b>4.12%</b>", td_bold), Paragraph("<font color='#d97706'><b>Early warning triggered</b></font>", td_style)],
        [Paragraph("2022Q3", td_style), Paragraph("76.5%", td_style), Paragraph("1.00", td_style), Paragraph("15.84%", td_style), Paragraph("Accelerated distress", td_style)],
        [Paragraph("2022Q4", td_style), Paragraph("98.2%", td_style), Paragraph("0.55", td_style), Paragraph("29.11%", td_style), Paragraph("Severe deterioration", td_style)],
        [Paragraph("2023Q1", td_style), Paragraph("135.4%", td_style), Paragraph("<b>-0.08</b>", td_bold), Paragraph("<b>53.09%</b>", td_bold), Paragraph("<font color='#dc2626'><b>UBS rescue quarter</b></font>", td_style)],
    ]
    t2 = Table(t2_data, colWidths=[70, 110, 120, 90, 150])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    # Deposit & Funding Stress
    story.append(Paragraph("Deposit & Funding Stress", h3_style))
    story.append(Paragraph(
        "The most acute stress signal in the dataset is the deposit base itself. Total deposits fell from $390B to $180B — a <b>54% decline</b> — over five quarters, pushing the loan-to-deposit ratio from 76.9% to 144.4% over the same period:",
        body_style
    ))

    t3_data = [
        [Paragraph("Quarter", th_style), Paragraph("Total Deposits", th_style), Paragraph("CET1 Capital", th_style), Paragraph("Loan-to-Deposit Ratio", th_style)],
        [Paragraph("2022Q1", td_style), Paragraph("$390B", td_style), Paragraph("$41.0B", td_style), Paragraph("76.9%", td_style)],
        [Paragraph("2022Q2", td_style), Paragraph("$360B", td_style), Paragraph("$39.5B", td_style), Paragraph("81.9%", td_style)],
        [Paragraph("2022Q3", td_style), Paragraph("$310B", td_style), Paragraph("$38.0B", td_style), Paragraph("93.5%", td_style)],
        [Paragraph("2022Q4", td_style), Paragraph("$230B", td_style), Paragraph("$36.0B", td_style), Paragraph("121.7%", td_style)],
        [Paragraph("2023Q1", td_style), Paragraph("$180B", td_style), Paragraph("$31.0B", td_style), Paragraph("<b>144.4%</b>", td_bold)],
    ]
    t3 = Table(t3_data, colWidths=[100, 140, 140, 160])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t3)

    # Capital Structure
    story.append(Paragraph("Capital Structure", h2_style))
    story.append(Paragraph(
        "As a G-SIB, CS's capital structure included a substantial layer of Additional Tier 1 (AT1) contingent convertible bonds sitting subordinate to senior unsecured debt and senior to common equity in ordinary circumstances. A defining feature of the actual UBS resolution was that Swiss regulator FINMA exercised a full write-down of approximately CHF 16 billion in AT1 notes to zero as part of the rescue — while equity holders retained a residual (if severely diluted) recovery through UBS's stock-and-cash offer. This inverted the conventional capital structure waterfall (equity subordinate to AT1) and is a widely cited case study in contingent-capital risk. This analysis's declining CET1 trend (from $41.0B to $31.0B over the period, against broadly stable risk-weighted assets) is consistent with the capital erosion that ultimately triggered this outcome.",
        body_style
    ))

    # Red Flags
    story.append(Paragraph("Red Flags", h2_style))
    story.append(Paragraph("• <b>CET1 capital declined from $41.0B to $31.0B (−24%)</b> over five quarters while risk-weighted assets remained broadly stable, signaling erosion of the Bank's core solvency buffer rather than balance-sheet shrinkage alone.", bullet_style))
    story.append(Paragraph("• <b>Loan-to-deposit ratio rose from 76.9% to 144.4%</b>, moving from a conservative funding profile to one indicating significant reliance on non-deposit funding — a classic precursor to a liquidity-driven crisis.", bullet_style))
    story.append(Paragraph("• <b>Equity volatility more than tripled (33.8% → 135.4%)</b>, directly compressing distance-to-default from a safe 3.05 to a negative reading (-0.08) by the final active quarter.", bullet_style))
    story.append(Paragraph("• <b>The composite score's deterioration was monotonic</b> across all five observed quarters with no quarter of improvement or stabilization — a pattern that, in hindsight, offered no false-recovery signal to mask the underlying trend.", bullet_style))

    # Peer Benchmarking
    story.append(Paragraph("Peer Benchmarking", h2_style))
    t4_data = [
        [Paragraph("Metric (2023Q1 / Latest Active)", th_style), Paragraph("Credit Suisse", th_style), Paragraph("JPMorgan Chase", th_style), Paragraph("Goldman Sachs", th_style)],
        [Paragraph("<b>Composite Risk Score</b>", td_style), Paragraph("<b>67.3%</b>", td_bold), Paragraph("44.9%", td_style), Paragraph("49.5%", td_style)],
        [Paragraph("<b>Distance-to-Default</b>", td_style), Paragraph("<b>-0.08</b>", td_bold), Paragraph("6.70", td_style), Paragraph("5.30", td_style)],
        [Paragraph("<b>Implied Probability of Default</b>", td_style), Paragraph("<b>53.09%</b>", td_bold), Paragraph("&lt; 0.0001%", td_style), Paragraph("&lt; 0.0001%", td_style)],
        [Paragraph("<b>Loan-to-Deposit Ratio (2022Q1→Latest)</b>", td_style), Paragraph("<b>76.9% → 144.4%</b>", td_bold), Paragraph("Stable, ~53–54%", td_style), Paragraph("N/A / stable", td_style)],
    ]
    t4 = Table(t4_data, colWidths=[180, 120, 120, 120])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t4)

    # Downside Sensitivity
    story.append(Paragraph("Downside Sensitivity", h2_style))
    story.append(Paragraph(
        "Had deposit outflows continued at the 2022Q4→2023Q1 run-rate (approximately $50B/quarter) for two additional quarters without external intervention, the loan-to-deposit ratio would have breached approximately 200%, and distance-to-default — already negative at -0.08 — would imply a probability of default approaching certainty on the model's logistic scale, underscoring why external resolution occurred when it did rather than the Bank stabilizing organically.",
        body_style
    ))

    # Risk Factors
    story.append(Paragraph("Risk Factors", h2_style))
    story.append(Paragraph("• <b>Model risk:</b> the composite score is derived from a 14-company sample (7 failures), a small dataset by conventional statistical standards; bank-sector coefficients in particular are based on only 4 companies and should be treated as directionally indicative rather than precisely calibrated.", bullet_style))
    story.append(Paragraph("• <b>The deposit flight captured here reflects reported quarterly balances</b>, not daily/weekly outflow velocity; the actual acute run in March 2023 occurred on a timescale faster than this quarterly framework can resolve.", bullet_style))
    story.append(Paragraph("• <b>No standalone funding-cost (e.g., interest expense/liabilities) metric was incorporated;</b> loan-to-deposit ratio serves as the model's sole funding-stress proxy.", bullet_style))

    # Recommendation / Rating
    story.append(Paragraph("Recommendation / Rating", h2_style))
    story.append(Paragraph(
        "Based on the composite score of <b>67.3% (DISTRESS ZONE, >60% threshold)</b>, a negative and rapidly falling distance-to-default, and accelerating deposit attrition, this analysis would have assigned Credit Suisse a <b><font color='#dc2626'>HIGH RISK / DISTRESSED</font></b> rating as of 2023Q1 — consistent with, and in fact anticipating, the actual outcome of the Bank's emergency acquisition by UBS later that quarter. The earliest actionable signal in this framework (distance-to-default crossing into warning territory in 2022Q2) preceded the resolution event by approximately three quarters, which this analysis holds out as the model's central, defensible finding.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated PDF at: {pdf_path}")


if __name__ == '__main__':
    build_pdf()
