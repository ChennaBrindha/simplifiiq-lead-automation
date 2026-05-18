import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

logger = logging.getLogger(__name__)

def send_email_with_pdf(to_email: str, company: str, pdf_path: str) -> bool:
    """
    Send professional branded email with PDF attachment
    """
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
            logger.error("Email credentials not configured")
            return False
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Your SimplifiQ AI Audit Report - {company}"
        message["From"] = sender_email
        message["To"] = to_email
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 600px; margin: 0 auto;">
                    <div style="background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%); color: white; padding: 40px 20px; text-align: center;">
                        <h1 style="margin: 0; font-size: 28px;">SimplifiQ</h1>
                        <p>AI Audit Report for {company}</p>
                    </div>
                    <div style="padding: 30px 20px; background: #f8fafc;">
                        <h2 style="color: #1e40af;">Your Personalized AI Audit Report</h2>
                        <p>Thank you for requesting your SimplifiQ AI audit report. Your comprehensive analysis of {company}'s AI opportunities is attached.</p>
                        
                        <h3 style="color: #1e40af;">What's Included:</h3>
                        <ul>
                            <li>Strategic business analysis</li>
                            <li>Specific AI opportunities tailored to your company</li>
                            <li>Phased implementation roadmap</li>
                            <li>ROI projections and success metrics</li>
                        </ul>
                        
                        <p><strong>Next Steps:</strong> Review the attached PDF report and contact our team to discuss implementation strategy.</p>
                    </div>
                    <div style="background: #1f2937; color: white; padding: 20px; text-align: center; font-size: 12px;">
                        <p><strong>SimplifiQ</strong></p>
                        <p>Empowering organizations through strategic AI adoption</p>
                        <p>© 2024 SimplifiQ. All Rights Reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        if os.path.exists(pdf_path):
            try:
                with open(pdf_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(pdf_path)}")
                message.attach(part)
                logger.info(f"PDF attached: {os.path.basename(pdf_path)}")
            except Exception as e:
                logger.error(f"Error attaching PDF: {e}")
                return False
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
                logger.info(f"Email sent to {to_email}")
                return True
        
        except Exception as e:
            logger.warning(f"Port 465 failed: {e}, trying port 587...")
            
            try:
                with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, to_email, message.as_string())
                    logger.info(f"Email sent to {to_email} (port 587)")
                    return True
            
            except Exception as e2:
                logger.error(f"Email failed: {e2}")
                return False
    
    except Exception as e:
        logger.error(f"Email error: {e}")
        return False