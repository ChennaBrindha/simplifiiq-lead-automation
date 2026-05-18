"""
UPDATED email_sender.py
Uses standard SMTP delivery using SENDER_EMAIL and SENDER_PASSWORD from Railway
"""

import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

logger = logging.getLogger(__name__)


def send_email_with_pdf(to_email: str, company: str, pdf_path: str) -> bool:
    """
    Send professional PDF report using standard SMTP
    Railway-compatible
    """
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    if not SENDER_EMAIL or not SENDER_PASSWORD:
        logger.error("❌ Missing email credentials (SENDER_EMAIL or SENDER_PASSWORD)")
        return False

    # Automatically detect SMTP settings based on your email provider
    smtp_server = "smtp.gmail.com"  # Default to Gmail
    smtp_port = 587  # Standard TLS Port

    if "@outlook.com" in SENDER_EMAIL.lower() or "@hotmail.com" in SENDER_EMAIL.lower():
        smtp_server = "smtp-mail.outlook.com"
    elif "@yahoo.com" in SENDER_EMAIL.lower():
        smtp_server = "smtp.mail.yahoo.com"

    try:
        # Create message container
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = f"Your AI Transformation Report for {company}"

        # Email HTML body
        html_content = f"""
        <html>
            <body>
                <h2>Professional AI Strategy Report</h2>
                <p>Thank you for your interest in AI transformation solutions for <strong>{company}</strong>.</p>

                <p>Please find attached your personalized strategic report containing:</p>

                <ul>
                    <li>Business analysis</li>
                    <li>AI opportunities</li>
                    <li>Implementation roadmap</li>
                    <li>Strategic recommendations</li>
                </ul>

                <p>We look forward to helping {company} accelerate its AI journey.</p>

                <br>

                <p>Best regards,<br>
                SimplifiQ AI Automation Team</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(html_content, "html"))

        # Read and attach the PDF file
        with open(pdf_path, "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())

        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(pdf_path)}",
        )
        msg.attach(attachment)

        # Connect to server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade connection to secure TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        logger.info(f"✅ Email sent successfully via SMTP to {to_email}")
        return True

    except Exception as e:
        logger.error(f"❌ SMTP Email sending failed: {str(e)}")
        return False