import os,ssl, certifi
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

os.environ['SSL_CERT_FILE'] = certifi.where()
load_dotenv()

def send_email_sendgrid(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send email using SendGrid API key. Returns True on success.
    """
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")

    if not SENDGRID_API_KEY:
        print("DEBUG: SENDGRID_API_KEY not found in environment")
        raise RuntimeError("SENDGRID_API_KEY not set")
    if not FROM_EMAIL:
        print("DEBUG: FROM_EMAIL not found in environment")
        raise RuntimeError("FROM_EMAIL not set")

    try:
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        resp = sg.send(message)
        status = resp.status_code
        print("DEBUG: SendGrid response:", status)
        return 200 <= status < 300
    except Exception as e:
        print("SendGrid send error:", e)
        return False
