import smtplib
from email.mime.text import MIMEText
import logging
from flask import current_app

logger = logging.getLogger(__name__)

def send_email(recipients, subject, body):
    """Trimite un email plain-text prin SMTP (Gmail)."""
    cfg = current_app.config
    host = cfg.get('SMTP_HOST', 'smtp.gmail.com')
    port = cfg.get('SMTP_PORT', 587)
    user = cfg.get('SMTP_USER', '')
    password = cfg.get('SMTP_PASSWORD', '')
    sender = cfg.get('SMTP_FROM', '') or user

    if not user or not password:
        logger.error('Credențiale SMTP lipsă — emailul nu a fost trimis')
        return False

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(user, password)
            server.sendmail(sender, recipients, msg.as_string())
        logger.info('Email trimis către %s', recipients)
        return True
    except Exception:
        logger.exception('Eroare la trimiterea emailului')
        return False
