from pptx import Presentation
from pptx.util import Inches, Pt
import sys

def move_slide(prs, old_index, new_index):
    xml_slides = prs.slides._sldIdLst  
    slides = list(xml_slides)
    xml_slides.remove(slides[old_index])
    xml_slides.insert(new_index, slides[old_index])

def add_custom_slide(prs, title_text, bullets):
    # Try to use a blank layout to avoid Gamma's default placeholders
    try:
        layout = prs.slide_layouts[6]
    except:
        layout = prs.slide_layouts[0]
        
    slide = prs.slides.add_slide(layout)
    
    # Remove any existing shapes just to be absolutely clean
    for shape in list(slide.shapes):
        sp = shape.element
        sp.getparent().remove(sp)
        
    # Create Title Text Box manually
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(36)
    
    # Create Body Text Box manually
    bodyBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(5.5))
    btf = bodyBox.text_frame
    btf.word_wrap = True
    
    for i, point in enumerate(bullets):
        p = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
        p.text = "•  " + point
        p.font.size = Pt(22)
        
    return slide

def main():
    ppt_path = r"C:\chit fund\Secure-Chit -demo-ppt.pptx"
    out_path = r"C:\chit fund\Secure-Chit -demo-ppt_FINAL.pptx"
    
    try:
        prs = Presentation(ppt_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    initial_slide_count = len(prs.slides)
    
    user_bullets = [
        "Registration & KYC: User signs up and submits documents for admin approval.",
        "Plan Enrollment: Selects a chit plan and pays the first installment via Razorpay.",
        "Live Bidding: Participates in the monthly reverse auction or requests AI emergency allocation.",
        "Digital Signature: Winner electronically signs the auto-generated Promissory Note using HTML5 Canvas.",
        "Prize Disbursal: Admin verifies the signature and releases the prize amount.",
        "Dividend & Dues: User enjoys automated monthly dividends and pays ongoing installments online."
    ]
    add_custom_slide(prs, "User (Member) Workflow", user_bullets)
    
    admin_bullets = [
        "Member & KYC Verification: Reviews new user registrations and verifies Aadhaar/PAN.",
        "Chit Group Creation: Creates new chit plans, sets rules, and schedules auction dates.",
        "Auction Monitoring: Oversees the live reverse auction and declares the winner.",
        "Dividend Calculation: System handles the 5% commission, Admin ensures dividends are distributed.",
        "Signature Verification: Admin reviews and approves the winner's digital signature on the Promissory Note.",
        "Prize Disbursal: Releases the prize money to the verified winner.",
        "Ledger Audit: Monitors monthly UPI payments and maintains the database audit logs."
    ]
    add_custom_slide(prs, "Admin (Foreman) Workflow", admin_bullets)
    
    integrated_bullets = [
        "Onboarding Phase: User submits KYC -> Admin approves and creates groups.",
        "Auction Phase: User bids in real-time -> Admin monitors and System declares winner.",
        "Documentation Phase: System generates Pronote -> User signs digitally -> Admin verifies signature.",
        "Settlement Phase: Admin disburses prize -> System distributes dividends -> User pays ongoing dues."
    ]
    add_custom_slide(prs, "Integrated System Workflow (User-Admin Link)", integrated_bullets)
    
    # Move the 3 newly added slides to index 2, 3, 4
    move_slide(prs, initial_slide_count, 2)
    move_slide(prs, initial_slide_count, 3)
    move_slide(prs, initial_slide_count, 4)
    
    prs.save(out_path)
    print("SUCCESS")

if __name__ == "__main__":
    main()
