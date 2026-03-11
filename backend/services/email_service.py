import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from core.config import settings

logger = logging.getLogger(__name__)

def send_report_email(to_email: str, subject: str, body: str) -> bool:
    """
    Sends an email using the SendGrid API.
    """
    if not settings.SENDGRID_API_KEY:
        logger.warning("SENDGRID_API_KEY not configured. Skipping email delivery.")
        return False
        
    sender = settings.EMAIL_FROM or settings.EMAIL_SENDER or "noreply@example.com"
        
    message = Mail(
        from_email=sender,
        to_emails=to_email,
        subject=subject,
        html_content=body,
        plain_text_content=body
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.info(f"Report emailed successfully to {to_email}. Status code: {response.status_code}")
        return True
    except Exception as e:
        error_msg = str(e)
        if hasattr(e, "body"):
            error_msg += f" - Response: {e.body}"
        logger.error(f"Failed to send email to {to_email} via SendGrid: {error_msg}")
        return False
