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

def send_email_mock(to_email: str, subject: str, body: str):
    """Simulates sending an email by logging it."""
    logger.info(f"📧 EMAIL SENT TO: {to_email}\nSUBJECT: {subject}\nBODY:\n{body}")

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
        # Find user by email
        user = db.query(User).filter(User.email == user_email).first()
        if user:
            title = f"🎉 Won Monthly Draw: {plan_name}"
            msg = f"Congratulations! You won the Month {month} draw for '{plan_name}'. Winning Ticket: {ticket_number}. Prize: ₹{prize_amount:,.2f}."
            create_db_notification(db, user.id, title, msg, NotificationType.success)
    finally:
        db.close()
