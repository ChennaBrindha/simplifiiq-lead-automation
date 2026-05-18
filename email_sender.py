import os
import logging
from pathlib import Path
import resend

logger = logging.getLogger(__name__)

def send_email_with_pdf(to_email: str, company_name: str, pdf_path: str) -> bool:
    resend.api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("FROM_EMAIL") # e.g., "onboarding@resend.dev" for testing
    
    if not resend.api_key or not from_email:
        logger.error("❌ Resend environment variables missing.")
        return False

    try:
        path = Path(pdf_path)
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        # Send via Resend's clean API over HTTPS (Railway-friendly!)
        response = resend.Emails.send({
            "from": from_email,
            "to": to_email,
            "subject": f"Your Personalized AI Roadmap & Audit for {company_name}",
            "html": f"<p>Thank you! Your custom audit for <strong>{company_name}</strong> is attached.</p>",
            "attachments": [
                {
                    "filename": path.name,
                    "content": list(pdf_bytes) # Resend accepts raw bytes as a list
                }
            ]
        })
        logger.info(f"🎉 Email sent successfully via Resend to {to_email}!")
        return True
    except Exception as e:
        logger.error(f"❌ Resend API Error: {e}")
        return False