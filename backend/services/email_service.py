import logging
import yagmail
from core.config import settings

logger = logging.getLogger(__name__)

def send_report_email(to_email: str, subject: str, body: str) -> bool:
    """
    Sends an email using standard SMTP.
    """
    if not settings.EMAIL_SENDER or not settings.EMAIL_PASSWORD:
        logger.warning("Email credentials not configured. Skipping email delivery.")
        return False
        
    try:
        yag = yagmail.SMTP(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
        yag.send(to=to_email, subject=subject, contents=body)
        logger.info(f"Report emailed to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False
