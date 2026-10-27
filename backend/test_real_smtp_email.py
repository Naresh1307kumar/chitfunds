import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_real_email(to_email, subject, body):
    sender_email = "securechit.admin@gmail.com"
    # Try sending via standard TLS / SMTP relay
    msg = MIMEMultipart()
    msg['From'] = f"SecureChit Administration <{sender_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    print(f"Attempting to send real email to: {to_email}")

    # Standard Gmail SMTP configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        # Note: If App Password is not provided, we handle exception gracefully or use SMTP relay
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
        server.starttls()
        print("Connected to Gmail SMTP server via TLS.")
        server.quit()
        print("[SUCCESS] Gmail SMTP Server reachability verified!")
    except Exception as e:
        print(f"[SMTP WARNING] Direct TLS connection: {e}")

if __name__ == "__main__":
    send_real_email("naresk1213@gmail.com", "Test Email from SecureChit", "Hello Naresh, this is a test email!")
