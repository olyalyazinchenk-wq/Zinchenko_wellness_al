import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, 
    Table, TableStyle, PageBreak, KeepTogether, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / "assets" / "fonts"

# Palette Apple/Luxury
COLOR_DARK = colors.HexColor("#0f172a") # Slate 900
COLOR_TEXT = colors.HexColor("#334155") # Slate 700
COLOR_SOFT = colors.HexColor("#f8fafc") # Slate 50
COLOR_ACCENT = colors.HexColor("#94a3b8") # Slate 400
COLOR_GOLD = colors.HexColor("#d4af37")

try:
    pdfmetrics.registerFont(TTFont('Montserrat', str(FONTS_DIR / 'Montserrat-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Montserrat-Bold', str(FONTS_DIR / 'Montserrat-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('Montserrat-Medium', str(FONTS_DIR / 'Montserrat-Medium.ttf')))
    pdfmetrics.registerFont(TTFont('Montserrat-Italic', str(FONTS_DIR / 'Montserrat-Italic.ttf')))
    FONT_NAME = 'Montserrat'
    FONT_BOLD = 'Montserrat-Bold'
    FONT_MID = 'Montserrat-Medium'
except:
    FONT_NAME = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_MID = 'Helvetica'

def draw_cover(canvas, doc):
    """Draws the luxurious dark cover page."""
    canvas.saveState()
    # Dark Background
    canvas.setFillColor(COLOR_DARK)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    
    # Subtitle / Logo area
    canvas.setFillColor(colors.white)
    canvas.setFont(FONT_NAME, 10)
    canvas.drawString(25*mm, A4[1] - 30*mm, "ОЛЬГА ЗИНЧЕНКО")
    canvas.setFillColor(COLOR_ACCENT)
    canvas.setFont(FONT_NAME, 8)
    canvas.drawString(25*mm, A4[1] - 35*mm, "Н У Т Р И Ц И О Л О Г")
    
    # Big Title
    canvas.setFillColor(colors.white)
    canvas.setFont(FONT_BOLD, 36)
    canvas.drawString(25*mm, A4[1] - 120*mm, "ПЕРСОНАЛЬНОЕ")
    canvas.drawString(25*mm, A4[1] - 135*mm, "WELLNESS ДОСЬЕ")
    
    # Accent line
    canvas.setStrokeColor(COLOR_GOLD)
    canvas.setLineWidth(2)
    canvas.line(25*mm, A4[1] - 145*mm, 85*mm, A4[1] - 145*mm)
    
    canvas.setFillColor(COLOR_ACCENT)
    canvas.setFont(FONT_NAME, 12)
    canvas.drawString(25*mm, A4[1] - 160*mm, "Разбор состояния и маршрут")
    canvas.drawString(25*mm, A4[1] - 165*mm, "нутрициологического сопровождения")
    
    # Client name injected at the bottom
    # We will pass name via a global or doc.client_name if bound
    canvas.restoreState()

def draw_inner(canvas, doc):
    """Draws standard headers and footers for inner pages."""
    canvas.saveState()
    # Header Line
    canvas.setStrokeColor(COLOR_SOFT)
    canvas.setLineWidth(1)
    canvas.line(20*mm, A4[1] - 15*mm, A4[0] - 20*mm, A4[1] - 15*mm)
    
    # Header text
    canvas.setFillColor(COLOR_ACCENT)
    canvas.setFont(FONT_NAME, 8)
    canvas.drawString(20*mm, A4[1] - 12*mm, "WELLNESS ДОСЬЕ | ОЛЬГА ЗИНЧЕНКО")
    
    # Page Number
    page_num = canvas.getPageNumber()
    canvas.drawRightString(A4[0] - 20*mm, 15*mm, str(page_num))
    canvas.restoreState()


def create_dossier_pdf(data: dict, output_path: str):
    doc = BaseDocTemplate(
        output_path, 
        pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=25*mm, bottomMargin=25*mm
    )
    
    # Frames
    frame_cover = Frame(0, 0, A4[0], A4[1], id='cover_frame', leftPadding=25*mm, bottomPadding=40*mm)
    frame_inner = Frame(20*mm, 20*mm, A4[0]-40*mm, A4[1]-45*mm, id='inner_frame')
    
    doc.addPageTemplates([
        PageTemplate(id='Cover', frames=frame_cover, onPage=draw_cover),
        PageTemplate(id='Inner', frames=frame_inner, onPage=draw_inner)
    ])
    
    styles = getSampleStyleSheet()
    
    style_cover_client = ParagraphStyle(
        'CoverClient', fontName=FONT_MID, fontSize=12, textColor=colors.white, leading=16
    )
    style_h1 = ParagraphStyle(
        'H1', fontName=FONT_BOLD, fontSize=18, leading=22, textColor=COLOR_DARK, 
        spaceBefore=25, spaceAfter=15, 
        borderPadding=(0,0,5,0), borderColor=COLOR_ACCENT, borderWidth=0.5 # subtle underline idea, handled via platypus
    )
    style_p = ParagraphStyle(
        'P', fontName=FONT_NAME, fontSize=11, leading=18, textColor=COLOR_TEXT, spaceAfter=12
    )
    style_alert_text = ParagraphStyle(
        'AlertP', fontName=FONT_MID, fontSize=11, leading=18, textColor=colors.HexColor("#7f1d1d")
    )
    
    story = []
    
    # Cover content (pushed to bottom by padding)
    story.append(Spacer(1, 160*mm))
    story.append(Paragraph(f"Пациент:<br/>{data.get('client_profile', 'Клиент')}", style_cover_client))
    
    # Force Inner template
    story.append(PageBreak())
    story.append(Spacer(1, 5*mm)) # fix frame top space
    
    sections = [
        ("ОСНОВНОЙ ЗАПРОС", data.get("main_request")),
        ("РАБОЧИЕ ГИПОТЕЗЫ", data.get("working_hypotheses")),
        ("ПРИОРИТЕТЫ", data.get("support_priorities")),
        ("СТРАТЕГИЯ ПИТАНИЯ", data.get("diet_strategy")),
        ("ОБРАЗ ЖИЗНИ И РЕЖИМ", data.get("lifestyle")),
        ("ЗОНЫ КОНТРОЛЯ", data.get("additional_control")),
    ]
    
    for title, content in sections:
        if content:
            block = []
            block.append(Paragraph(title, style_h1))
            # Bullet point handling
            lines = str(content).split('\\n') if '\\n' in content else str(content).split('\n')
            for line in lines:
                text = line.strip()
                if not text: continue
                # Simple formatting
                if text.startswith('•') or text.startswith('-') or (text[0].isdigit() and text[1]=='.'):
                    # Use table to indent bullets for extreme premium look
                    bullet_table = Table([[Paragraph(text, style_p)]], colWidths=[A4[0]-40*mm])
                    bullet_table.setStyle(TableStyle([
                        ('LEFTMARGIN', (0,0), (-1,-1), 10*mm),
                        ('TOPPADDING', (0,0), (-1,-1), 0),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
                    ]))
                    block.append(bullet_table)
                else:
                    block.append(Paragraph(text, style_p))
            story.append(KeepTogether(block))
            story.append(Spacer(1, 10*mm))
            
    # Highlighted Conclusion
    concl = data.get("final_conclusion")
    if concl:
        c_table = Table([[Paragraph("ИТОГОВОЕ ЗАКЛЮЧЕНИЕ", style_h1)], [Paragraph(concl, style_p)]], colWidths=[A4[0]-40*mm])
        c_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
            ('TOPPADDING', (0,0), (-1,-1), 15),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
            ('LEFTPADDING', (0,0), (-1,-1), 15),
            ('RIGHTPADDING', (0,0), (-1,-1), 15),
            ('LINEAFTER', (0,0), (0,-1), 0, colors.white),
        ]))
        story.append(Spacer(1, 10*mm))
        story.append(KeepTogether([c_table]))
    
    # Schemes Table
    schemes = data.get("schemes", [])
    if schemes:
        story.append(PageBreak())
        story.append(Paragraph("СТАРТОВАЯ СХЕМА", style_h1))
        story.append(Paragraph("Ниже приведены рабочие схемы именно как нутрицевтическая поддержка.", style_p))
        
        t_data = []
        for i, s in enumerate(schemes):
            bg = colors.HexColor("#ffffff") if i % 2 == 0 else colors.HexColor("#f8fafc")
            t_data.append([
                Paragraph(s.get("time", ""), ParagraphStyle('tbl_p', parent=style_p, textColor=COLOR_ACCENT, fontSize=10)),
                Paragraph(f"<b>{s.get('name', '')}</b>", style_p),
                Paragraph(s.get("comment", ""), ParagraphStyle('tbl_p2', parent=style_p, fontSize=10))
            ])
            
        t = Table(t_data, colWidths=[35*mm, 55*mm, 80*mm])
        t_style = [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 12),
            ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0"))
        ]
        # alternating backgrounds
        for row in range(len(t_data)):
            if row % 2 == 1:
                t_style.append(('BACKGROUND', (0,row), (-1,row), colors.HexColor("#f8fafc")))
                
        t.setStyle(TableStyle(t_style))
        story.append(t)
        
    doc.build(story)
    return output_path

if __name__ == "__main__":
    import test_data
    import tempfile
    tf = Path(tempfile.gettempdir()) / "test_dossier_premium.pdf"
    create_dossier_pdf(test_data.DUMMY_DATA, str(tf))
    print(f"Generated at: {tf}")
