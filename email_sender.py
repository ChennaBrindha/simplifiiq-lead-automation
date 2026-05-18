"""
UPDATED email_sender.py
Uses SendGrid API for guaranteed Railway-compatible email delivery
"""

import os
import base64
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition
)

logger = logging.getLogger(__name__)


def send_email_with_pdf(to_email: str, company: str, pdf_path: str) -> bool:
    """
    Send professional PDF report using SendGrid API
    Railway-compatible
    """

    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL = os.getenv("FROM_EMAIL")

    if not SENDGRID_API_KEY or not FROM_EMAIL:
        logger.error("❌ Missing SendGrid credentials")
        return False

    try:
        # Read PDF file
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        encoded_pdf = base64.b64encode(pdf_data).decode()

        # Email body
        subject = f"Your AI Transformation Report for {company}"

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

        # Create mail object
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )

        # Attach PDF
        attached_file = Attachment(
            FileContent(encoded_pdf),
            FileName(os.path.basename(pdf_path)),
            FileType("application/pdf"),
            Disposition("attachment")
        )

        message.attachment = attached_file

        # Send email
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Email sent successfully to {to_email}")
            return True
        else:
            logger.error(f"❌ SendGrid failed with status: {response.status_code}")
            return False

    except Exception as e:
        logger.error(f"❌ Email sending failed: {str(e)}")
        return False