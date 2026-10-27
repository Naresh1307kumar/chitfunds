import logging
from app.database import SessionLocal
from app.models.notification import Notification, NotificationType
from app.models.user import User

# Configure logger for notifications
logger = logging.getLogger("notifications")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('\n%(asctime)s - %(name)s - %(levelname)s\n%(message)s\n' + '='*50)
ch.setFormatter(formatter)
logger.addHandler(ch)

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_mock(to_email: str, subject: str, body: str):
    """Simulates email logging and dispatches via SMTP if SMTP credentials exist."""
    logger.info(f"📧 EMAIL SENT TO: {to_email}\nSUBJECT: {subject}\nBODY:\n{body}")

    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")
    smtp_from = os.getenv("SMTP_FROM_EMAIL", smtp_user or "naresk1213@gmail.com")

    if smtp_user and smtp_password:
        try:
            msg = MIMEMultipart()
            msg['From'] = f"SecureChit Administration <{smtp_from}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_from, to_email, msg.as_string())
            server.quit()
            logger.info(f"✅ REAL EMAIL SUCCESSFULLY DELIVERED VIA SMTP TO: {to_email}")
        except Exception as e:
            logger.error(f"❌ Real SMTP email delivery attempt to {to_email} failed: {e}")

def send_sms_mock(to_phone: str, message: str):
    """Simulates sending an SMS by logging it."""
    logger.info(f"📱 SMS SENT TO: {to_phone}\nMESSAGE: {message}")

def send_whatsapp_mock(to_phone: str, message: str):
    """Simulates sending a WhatsApp message by logging it."""
    logger.info(f"💬 WHATSAPP SENT TO: {to_phone}\nMESSAGE: {message}")

def create_db_notification(db_session, user_id: int, title: str, message: str, notif_type: NotificationType = NotificationType.info):
    """Creates a notification record in the database."""
    try:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notif_type,
            is_read=False
        )
        db_session.add(notif)
        db_session.commit()
        db_session.refresh(notif)
        logger.info(f"💾 NOTIFICATION SAVED IN DB FOR USER {user_id}: {title}")
    except Exception as e:
        db_session.rollback()
        logger.error(f"❌ Failed to save notification in DB: {e}")

def send_winner_notifications(user_name: str, user_email: str, user_phone: str, plan_name: str, prize_amount: float, ticket_number: str, month: int):
    """Formats, logs mock channels and saves a DB notification for the winner."""
    
    subject = f"🎉 Congratulations! You are the winner for {plan_name}"
    
    body = f"""Hello {user_name},

We are thrilled to inform you that you have won the monthly draw for '{plan_name}' (Month {month})!

Winning Ticket: {ticket_number}
Prize Amount: ₹{prize_amount:,.2f}

The prize amount will be credited to your registered bank account soon.
Thank you for being a part of SecureChit!

Best Regards,
SecureChit Administration
"""
    
    sms_message = f"Congrats {user_name}! You won the Month {month} draw for {plan_name}. Prize: Rs.{prize_amount:,.2f}. Ticket: {ticket_number}. - SecureChit"
    
    whatsapp_message = f"""🎉 *Congratulations {user_name}!* 🎉

You have won the monthly draw for *{plan_name}* (Month {month})! 🏆

*Ticket:* {ticket_number}
*Prize Amount:* ₹{prize_amount:,.2f}

We will process your payout shortly. Thank you for choosing SecureChit!"""

    # Send mock notifications
    send_email_mock(user_email, subject, body)
    send_sms_mock(user_phone, sms_message)
    send_whatsapp_mock(user_phone, whatsapp_message)

    # Save to Database
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == user_email).first()
        if user:
            title = f"🎉 Won Monthly Draw: {plan_name}"
            msg = f"Congratulations! You won the Month {month} draw for '{plan_name}'. Winning Ticket: {ticket_number}. Prize: ₹{prize_amount:,.2f}."
            create_db_notification(db, user.id, title, msg, NotificationType.success)
    finally:
        db.close()

def send_payment_submitted_notification(user_id: int, user_name: str, user_email: str, user_phone: str, plan_name: str, month_number: int, amount: float, receipt_number: str, transaction_id: str):
    """Sends email/SMS and saves DB notification when a payment is submitted."""
    subject = f"💳 Payment Received - Receipt #{receipt_number}"
    body = f"""Hello {user_name},

Thank you! We have received your payment request of ₹{amount:,.2f} for '{plan_name}' (Month {month_number}).

Receipt Number: {receipt_number}
Transaction Reference / UTR: {transaction_id}
Status: Pending Admin Approval & Verification

You can view your digital receipt anytime on your member portal.

Best Regards,
SecureChit Team
"""
    send_email_mock(user_email, subject, body)
    send_sms_mock(user_phone, f"SecureChit: Payment of Rs.{amount:,.2f} for {plan_name} Month {month_number} received. Receipt #{receipt_number}. Pending admin verification.")

    db = SessionLocal()
    try:
        title = f"💳 Payment Received - Receipt #{receipt_number}"
        msg = f"Your payment of ₹{amount:,.2f} for '{plan_name}' Month {month_number} (UTR: {transaction_id}) is submitted and pending admin verification."
        create_db_notification(db, user_id, title, msg, NotificationType.info)
    finally:
        db.close()

def send_payment_verified_notification(user_id: int, user_name: str, user_email: str, user_phone: str, plan_name: str, month_number: int, amount: float, receipt_number: str):
    """Sends email/SMS and saves DB notification when a payment is approved/verified by Admin."""
    subject = f"✅ Payment Verified & Approved - Receipt #{receipt_number}"
    body = f"""Hello {user_name},

Great news! Your installment payment of ₹{amount:,.2f} for '{plan_name}' (Month {month_number}) has been verified and approved by the admin.

Receipt Number: {receipt_number}
Status: Verified & Completed

Thank you for your timely payment!

Best Regards,
SecureChit Administration
"""
    send_email_mock(user_email, subject, body)
    send_sms_mock(user_phone, f"SecureChit: Your payment of Rs.{amount:,.2f} for {plan_name} Month {month_number} has been verified and approved!")

    db = SessionLocal()
    try:
        title = f"✅ Payment Approved - Receipt #{receipt_number}"
        msg = f"Your payment of ₹{amount:,.2f} for '{plan_name}' Month {month_number} has been verified and approved."
        create_db_notification(db, user_id, title, msg, NotificationType.success)
    finally:
        db.close()

def send_10th_due_reminder_notifications():
    """Queries all unpaid monthly installments and sends 10th monthly due reminders to members before 15th auction draw."""
    from app.models.installment import Installment, InstallmentStatus
    from app.models.plan_member import PlanMember
    from app.models.chit_plan import ChitPlan

    db = SessionLocal()
    try:
        pending_installments = db.query(Installment).filter(
            Installment.status.in_([InstallmentStatus.pending, InstallmentStatus.overdue])
        ).all()

        reminded_users = 0
        for inst in pending_installments:
            pm = db.query(PlanMember).filter(PlanMember.id == inst.plan_member_id).first()
            if not pm:
                continue
            user = db.query(User).filter(User.id == pm.user_id).first()
            plan = db.query(ChitPlan).filter(ChitPlan.id == inst.plan_id).first()
            if user and plan:
                subject = f"⏰ Payment Due Reminder: 15th Auction Draw for {plan.plan_name}"
                body = f"""Hello {user.name},

This is a reminder that your monthly installment of ₹{inst.total_amount:,.2f} for '{plan.plan_name}' (Month {inst.month_number}) is pending!

The 15th Monthly Auction Draw is approaching soon. Please complete your payment via UPI/GPay on your member dashboard before the 15th to participate in this month's draw.

Best Regards,
SecureChit Team
"""
                send_email_mock(user.email, subject, body)
                send_sms_mock(user.phone, f"SecureChit Reminder: Your Month {inst.month_number} due of Rs.{inst.total_amount:,.2f} for {plan.plan_name} is pending before 15th draw. Please pay now!")

                title = f"⏰ 10th Monthly Due Reminder - {plan.plan_name}"
                msg = f"Your Month {inst.month_number} installment of ₹{inst.total_amount:,.2f} for '{plan.plan_name}' is pending before the upcoming 15th auction draw."
                create_db_notification(db, user.id, title, msg, NotificationType.warning)
                reminded_users += 1

        logger.info(f"⏰ Sent 10th Monthly Due Reminders to {reminded_users} members.")
        return reminded_users
    finally:
        db.close()

def send_draw_announcement_to_all_members(plan_id: int, plan_name: str, winner_name: str, ticket_number: str, prize_amount: float, month_number: int):
    """Sends email/DB notification to ALL members of a chit plan announcing the 15th monthly draw winner."""
    from app.models.plan_member import PlanMember

    db = SessionLocal()
    try:
        members = db.query(PlanMember).filter(PlanMember.plan_id == plan_id).all()
        for pm in members:
            user = db.query(User).filter(User.id == pm.user_id).first()
            if user:
                subject = f"🏆 Month {month_number} Draw Winner Announcement - {plan_name}"
                body = f"""Hello {user.name},

The Month {month_number} Auction Draw for '{plan_name}' has been successfully completed!

🏆 Winner: {winner_name}
🎟️ Winning Ticket: {ticket_number}
💰 Prize Amount: ₹{prize_amount:,.2f}

Congratulations to the winner! Next month's draw will take place on the 15th.

Best Regards,
SecureChit Administration
"""
                send_email_mock(user.email, subject, body)
                title = f"🏆 Month {month_number} Draw Winner Announced: {plan_name}"
                msg = f"Month {month_number} draw for '{plan_name}' completed! Winner: {winner_name} (Ticket #{ticket_number}) won ₹{prize_amount:,.2f}."
                create_db_notification(db, user.id, title, msg, NotificationType.info)
    finally:
        db.close()
