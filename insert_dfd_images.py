import shutil
import copy
from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from lxml import etree

# Load original document
src = r'C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5\.user_uploaded\media_1790855418312.docx'
out = r'C:\chit fund\SecureChit_Report_With_DFDs.docx'
shutil.copy(src, out)
doc = Document(out)

# Image files
img_level0 = r'C:\chit fund\DFD_Level_0_Word_Fitted.png'
img_level1 = r'C:\chit fund\DFD_Level_1_Decomposition.png'
img_4tier  = r'C:\chit fund\Four_Tier_Architecture.png'

# Caption style helper
def add_image_centered(doc, paragraph, image_path, width_inches, caption_text):
    """
    Inserts image + caption AFTER the given paragraph in the document.
    Returns the last inserted paragraph.
    """
    # We'll insert new paragraphs after the target paragraph by manipulating the XML
    parent = paragraph._element.getparent()
    idx = list(parent).index(paragraph._element)

    # Create image paragraph
    img_para = doc.add_paragraph()
    img_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = img_para.add_run()
    run.add_picture(image_path, width=Inches(width_inches))
    # Move to correct position
    parent.insert(idx + 1, img_para._element)
    parent.remove(img_para._element)
    parent.insert(idx + 1, img_para._element)

    # Create caption paragraph
    cap_para = doc.add_paragraph()
    cap_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap_run = cap_para.add_run(caption_text)
    cap_run.bold = True
    cap_run.font.size = Pt(11)
    # Move to correct position
    parent.insert(idx + 2, cap_para._element)
    parent.remove(cap_para._element)
    parent.insert(idx + 2, cap_para._element)

    return cap_para

# Find target paragraphs by index
paragraphs = doc.paragraphs
target_level0 = None   # Para 563: 'Context Level Diagram (Level 0 DFD)'
target_level1 = None   # Para 570: 'System Overview & Subsystem Decomposition (Level 1 DFD)'
target_4tier  = None   # Para 536: 'SYSTEM DESIGN' section -> look for module design or we'll add at end of Level 1

for i, para in enumerate(paragraphs):
    text = para.text.strip()
    if 'Context Level Diagram' in text and target_level0 is None:
        target_level0 = para
        print(f"Found Level 0 target at para {i}: {repr(text[:60])}")
    if 'System Overview' in text and 'Level 1' in text and target_level1 is None:
        target_level1 = para
        print(f"Found Level 1 target at para {i}: {repr(text[:60])}")
    if 'Auction Bidding' in text and 'Level 2' in text and target_4tier is None:
        target_4tier = para
        print(f"Found Level 2 / 4-tier target at para {i}: {repr(text[:60])}")

# Insert Level 0 DFD image after "Context Level Diagram (Level 0 DFD)" paragraph
if target_level0:
    parent = target_level0._element.getparent()
    idx = list(parent).index(target_level0._element)

    # Image paragraph
    img_p = doc.add_paragraph()
    img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p.add_run().add_picture(img_level0, width=Inches(4.5))
    parent.insert(idx + 1, img_p._element)
    parent.remove(img_p._element)
    parent.insert(idx + 1, img_p._element)

    # Caption paragraph
    cap_p = doc.add_paragraph()
    cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap_p.add_run("Figure 4.1: Level 0 Context Diagram showing Member User, Admin Foreman, Central System, and PostgreSQL Database.")
    r.bold = True
    r.font.size = Pt(11)
    parent.insert(idx + 2, cap_p._element)
    parent.remove(cap_p._element)
    parent.insert(idx + 2, cap_p._element)
    print("Inserted Level 0 DFD image")

# Insert Level 1 DFD image after "System Overview & Subsystem Decomposition (Level 1 DFD)" paragraph
if target_level1:
    parent = target_level1._element.getparent()
    idx = list(parent).index(target_level1._element)

    img_p = doc.add_paragraph()
    img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p.add_run().add_picture(img_level1, width=Inches(4.5))
    parent.insert(idx + 1, img_p._element)
    parent.remove(img_p._element)
    parent.insert(idx + 1, img_p._element)

    cap_p = doc.add_paragraph()
    cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap_p.add_run("Figure 4.3: Level 1 DFD (Decomposition Diagram)")
    r.bold = True
    r.font.size = Pt(11)
    parent.insert(idx + 2, cap_p._element)
    parent.remove(cap_p._element)
    parent.insert(idx + 2, cap_p._element)
    print("Inserted Level 1 DFD image")

# Insert Four Tier Architecture image after "Auction Bidding & Pronote Workflow (Level 2 DFD)" paragraph
if target_4tier:
    parent = target_4tier._element.getparent()
    idx = list(parent).index(target_4tier._element)

    img_p = doc.add_paragraph()
    img_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    img_p.add_run().add_picture(img_4tier, width=Inches(4.7))
    parent.insert(idx + 1, img_p._element)
    parent.remove(img_p._element)
    parent.insert(idx + 1, img_p._element)

    cap_p = doc.add_paragraph()
    cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cap_p.add_run("Figure 4.4: Four-Tier Architecture Diagram of SecureChit Platform")
    r.bold = True
    r.font.size = Pt(11)
    parent.insert(idx + 2, cap_p._element)
    parent.remove(cap_p._element)
    parent.insert(idx + 2, cap_p._element)
    print("Inserted Four-Tier Architecture image")

# Save final document
doc.save(out)
print(f"\nDocument saved successfully: {out}")
