import logging
import os
import requests
import base64

logger = logging.getLogger(__name__)

def send_email_with_pdf(to_email: str, company: str, pdf_path: str) -> bool:
    try:
        RESEND_API_KEY = os.getenv("RESEND_API_KEY")
        FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
        
        if not RESEND_API_KEY:
            logger.error("❌ Resend API key not configured")
            return False
        
        if not os.path.exists(pdf_path):
            logger.error(f"❌ PDF file not found: {pdf_path}")
            return False
        
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()
        
        pdf_base64 = base64.b64encode(pdf_content).decode()
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%); color: white; padding: 40px 20px; text-align: center;">
                        <h1 style="margin: 0; font-size: 28px;">SimplifiQ</h1>
                        <p>AI Audit Report for {company}</p>
                    </div>
                    <div style="padding: 30px 20px; background: #f8fafc;">
                        <h2 style="color: #1e40af;">Your Personalized AI Audit Report</h2>
                        <p>Thank you for requesting your SimplifiQ AI audit report. Your comprehensive analysis is attached.</p>
                        <h3 style="color: #1e40af;">What's Included:</h3>
                        <ul>
                            <li>Strategic business analysis</li>
                            <li>Specific AI opportunities</li>
                            <li>Implementation roadmap</li>
                        </ul>
                    </div>
                    <div style="background: #1f2937; color: white; padding: 20px; text-align: center; font-size: 12px;">
                        <p><strong>SimplifiQ</strong> - Empowering organizations through strategic AI adoption</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        payload = {
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": f"Your SimplifiQ AI Audit Report - {company}",
            "html": html_content,
            "attachments": [
                {
                    "filename": os.path.basename(pdf_path),
                    "content": pdf_base64,
                    "encoding": "base64"
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post("https://api.resend.com/emails", json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"✅ Email sent to {to_email} via Resend")
            return True
        else:
            logger.error(f"❌ Resend error: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Email error: {e}")
        return False