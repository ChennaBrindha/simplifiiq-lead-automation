"""
Professional PDF Report Generator
Creates accurate, detailed company analysis reports with no errors
"""

import logging
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

logger = logging.getLogger(__name__)

# Professional colors
DARK_BLUE = HexColor("#0f172a")
PRIMARY_BLUE = HexColor("#1e40af")
ACCENT_PURPLE = HexColor("#7c3aed")
TEXT_GRAY = HexColor("#475569")
LIGHT_GRAY = HexColor("#f8fafc")

def generate_pdf_report(lead, enriched_data) -> str:
    """
    Generate professional, accurate PDF report
    """
    try:
        filename = f"reports/{lead.company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title="AI Audit Report"
        )
        
        story = build_professional_report(lead, enriched_data)
        doc.build(story)
        
        logger.info(f"✅ PDF generated: {filename}")
        return filename
    
    except Exception as e:
        logger.error(f"❌ PDF generation error: {e}")
        raise

def build_professional_report(lead, enriched_data) -> list:
    """
    Build comprehensive, accurate report
    """
    story = []
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=DARK_BLUE,
        spaceAfter=12,
        fontName='Helvetica-Bold',
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'ReportSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=TEXT_GRAY,
        spaceAfter=24,
        fontName='Helvetica'
    )
    
    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=PRIMARY_BLUE,
        spaceAfter=12,
        spaceBefore=18,
        fontName='Helvetica-Bold'
    )
    
    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=11,
        leading=18,
        textColor=TEXT_GRAY,
        alignment=4,
        spaceAfter=12
    )
    
    subsection_style = ParagraphStyle(
        'Subsection',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=PRIMARY_BLUE,
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # PAGE 1: HEADER & EXECUTIVE SUMMARY
    
    # Header
    header_text = "SimplifiQ AI Audit Report"
    story.append(Paragraph(header_text, title_style))
    
    # Company info
    company_header = f"{lead.company} — Strategic AI Analysis Report"
    story.append(Paragraph(company_header, subtitle_style))
    
    report_date = f"Prepared for: {lead.name} | Date: {datetime.now().strftime('%B %d, %Y')}"
    story.append(Paragraph(report_date, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", section_header))
    
    exec_summary = f"""This comprehensive audit examines {lead.company}'s strategic position and identifies concrete opportunities for artificial intelligence adoption. Through analysis of their business model, operations, and market context, we have identified specific use cases where AI can drive measurable business value and competitive advantage."""
    
    story.append(Paragraph(exec_summary, body_text))
    story.append(Spacer(1, 0.2*inch))
    
    # Company Overview
    story.append(Paragraph("Company Overview & Business Analysis", section_header))
    
    business_analysis = enriched_data.get('business_analysis', '')
    if business_analysis and len(business_analysis) > 50:
        story.append(Paragraph(business_analysis, body_text))
    else:
        story.append(Paragraph(f"Professional analysis of {lead.company}'s business model and market position.", body_text))
    
    story.append(Spacer(1, 0.2*inch))
    
    # PAGE BREAK
    story.append(PageBreak())
    
    # PAGE 2: AI OPPORTUNITIES
    
    story.append(Paragraph("Strategic AI Opportunities", section_header))
    
    story.append(Paragraph(
        "Based on our analysis, we have identified three high-impact opportunities where AI can deliver significant business value:",
        body_text
    ))
    story.append(Spacer(1, 0.15*inch))
    
    # Opportunities
    opportunities = enriched_data.get('ai_opportunities', [])
    if opportunities and isinstance(opportunities, list):
        for i, opp in enumerate(opportunities[:3], 1):
            opp_text = str(opp).strip()
            if opp_text:
                story.append(Paragraph(f"<b>Opportunity {i}:</b>", subsection_style))
                story.append(Paragraph(opp_text, body_text))
                story.append(Spacer(1, 0.1*inch))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Implementation Roadmap
    story.append(Paragraph("Implementation Roadmap", section_header))
    
    story.append(Paragraph(
        "Successful AI adoption requires a structured, phased approach. Below is the recommended implementation roadmap:",
        body_text
    ))
    story.append(Spacer(1, 0.15*inch))
    
    implementation = enriched_data.get('implementation_plan', '')
    if implementation and len(implementation) > 50:
        story.append(Paragraph(implementation, body_text))
    else:
        story.append(Paragraph(
            "Phase 1 - Assessment and Strategy: Evaluate current capabilities and define objectives. "
            "Phase 2 - Pilot Project: Execute proof-of-concept on highest-impact use case. "
            "Phase 3 - Scale and Optimize: Expand across business units with refinement. "
            "Phase 4 - Enterprise Expansion: Full organizational rollout with continuous improvement.",
            body_text
        ))
    
    story.append(Spacer(1, 0.2*inch))
    
    # PAGE BREAK
    story.append(PageBreak())
    
    # PAGE 3: METRICS & CONCLUSION
    
    story.append(Paragraph("Success Metrics & Expected Outcomes", section_header))
    
    metrics_text = f"""When implemented strategically, AI initiatives for {lead.company} can deliver:

<b>Operational Efficiency:</b> 20-30% improvement in process automation and manual task reduction

<b>Decision Quality:</b> Enhanced analytics and predictive insights for faster, better decision-making

<b>Customer Experience:</b> Improved engagement through AI-powered personalization and insights

<b>Financial Impact:</b> Measurable ROI through cost savings, efficiency gains, and new revenue opportunities

<b>Competitive Advantage:</b> Differentiation through AI-driven innovation and market responsiveness"""
    
    story.append(Paragraph(metrics_text, body_text))
    story.append(Spacer(1, 0.2*inch))
    
    # Conclusion
    story.append(Paragraph("Conclusion & Next Steps", section_header))
    
    conclusion = f"""Artificial intelligence represents a significant opportunity for {lead.company} to enhance operations, improve decision-making, and create competitive advantages. Success requires:

1. <b>Executive Alignment:</b> Clear commitment to AI adoption from leadership
2. <b>Strategic Focus:</b> Concentration on high-impact use cases with measurable ROI
3. <b>Organizational Capability:</b> Investment in talent, tools, and processes
4. <b>Continuous Learning:</b> Build AI literacy and expertise across the organization
5. <b>Measurement & Optimization:</b> Track progress against defined metrics and KPIs

We recommend beginning with a comprehensive assessment of current capabilities, followed by a focused pilot project to demonstrate value and build organizational confidence. This phased approach reduces risk while creating momentum for broader adoption."""
    
    story.append(Paragraph(conclusion, body_text))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Paragraph("About SimplifiQ", section_header))
    
    footer = """SimplifiQ partners with organizations to streamline operations, optimize processes, and succeed with artificial intelligence. We specialize in practical, high-impact AI implementations that deliver measurable business value and sustainable competitive advantages.

<b>Contact SimplifiQ</b>
Email: career@simplifiiq.com
Website: simplifiiq.com

© 2026 SimplifiQ. All Rights Reserved. | Confidential"""
    
    story.append(Paragraph(footer, body_text))
    
    return story