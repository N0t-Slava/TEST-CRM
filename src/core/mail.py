import logging
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from jinja2 import Template
from core.config import settings

logger = logging.getLogger(__name__)



async def send_mail(to: str, subject: str, template_str: str, context: dict):
    """Безопасная асинхронная отправка email с HTML-шаблоном"""

    html = Template(template_str).render(**context)
    msg = MIMEText(html, "html", "utf-8")
    msg["From"] = settings.smtp_user
    msg["To"] = to
    msg["Subject"] = subject

    try:
        async with SMTP(
            hostname=settings.smtp_host,
            port=587,
            start_tls=True,
            timeout=10,
        ) as smtp:
            _send_via()
            logger.info(f"Email sent to {to} via STARTTLS")

    except Exception as tls_error:
        logger.error(f"Failed to send email to {to}: {tls_error}")
        
        try:
            async with SMTP(
                hostname=settings.smtp_host,
                port=465,
                use_tls=True,
                timeout=10,
            ) as smtp:
                _send_via()
                logger.info(f"Email sent to {to} via SSL (fallback)")

        except Exception as ssl_error:
            logger.error(f"Failed to send email to {to}: {ssl_error}")
            raise RuntimeError("Mail delivery failed") from ssl_error
        
async def _send_via(smtp: SMTP, msg):
    await smtp.login(settings.smtp_user, settings.smtp_pass)
    await smtp.send_message(msg)