import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_dfd_standalone_docx():
    doc = Document()
    
    # 1 inch margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Base Font
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_title.add_run("SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\nDATA FLOW DIAGRAMS (DFD)")
    r.bold = True
    r.font.size = Pt(18)
    p_title.paragraph_format.space_after = Pt(24)

    # 1. Level 0 DFD
    p_h0 = doc.add_paragraph()
    p_h0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p_h0.add_run("Level-0 (DFD) – System Context Diagram")
    r0.bold = True
    r0.font.size = Pt(14)
    
    if os.path.exists("dfd_level_0.png"):
        p_img0 = doc.add_paragraph()
        p_img0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img0.add_run().add_picture("dfd_level_0.png", width=Inches(6.8))
    
    doc.add_page_break()

    # 2. Level 1 DFD
    p_h1 = doc.add_paragraph()
    p_h1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_h1.add_run("Level-1 (DFD) – Administrator & Organization Governance Module")
    r1.bold = True
    r1.font.size = Pt(14)
    
    if os.path.exists("dfd_level_1.png"):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.add_run().add_picture("dfd_level_1.png", width=Inches(6.8))
    
    doc.add_page_break()

    # 3. Level 2 DFD
    p_h2 = doc.add_paragraph()
    p_h2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p_h2.add_run("Level-2 (DFD) – Auction Bidding & Pronote Execution Module")
    r2.bold = True
    r2.font.size = Pt(14)
    
    if os.path.exists("dfd_level_2.png"):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.add_run().add_picture("dfd_level_2.png", width=Inches(6.8))

    filename = r"c:\chit fund\SecureChit_Photo_Style_DFD_Diagrams.docx"
    doc.save(filename)
    print(f"Saved standalone DFD docx: {filename}")

if __name__ == "__main__":
    create_dfd_standalone_docx()
