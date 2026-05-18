"""
Email Sender Module
Sends personalized emails with PDF attachments using Gmail SMTP
"""

import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

logger = logging.getLogger(__name__)

def send_email_with_pdf(
    to_email: str,
    pdf_path: str,
    company_name: str,
    prospect_name: str
) -> bool:
    """
    Send personalized email with PDF attachment
    
    Args:
        to_email: Recipient email address
        pdf_path: Path to the PDF file
        company_name: Name of the company
        prospect_name: Name of the prospect
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get email credentials from environment
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
            logger.error("❌ Email credentials not found in environment variables")
            return False
        
        # Check if PDF file exists
        if not Path(pdf_path).exists():
            logger.error(f"❌ PDF file not found: {pdf_path}")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f"Your Personalized AI Audit Report - {company_name}"
        
        # Create email body
        html_body = create_email_body(prospect_name, company_name)
        
        # Attach HTML content
        msg.attach(MIMEText(html_body, 'html'))
        
        # Attach PDF
        attach_pdf(msg, pdf_path)
        
        # Send email
        send_via_smtp(sender_email, sender_password, to_email, msg)
        
        logger.info(f"✅ Email sent successfully to {to_email}")
        return True
    
    except Exception as e:
        logger.error(f"❌ Email sending failed: {str(e)}")
        return False

def create_email_body(prospect_name: str, company_name: str) -> str:
    """
    Create professional HTML email body
    """
    html_body = f"""
    <html>
        <head>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
                    line-height: 1.6;
                    color: #1f2937;
                    background-color: #f3f4f6;
                    padding: 20px 0;
                }}
                .email-container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }}
                .header-logo {{
                    font-size: 28px;
                    font-weight: 800;
                    margin-bottom: 8px;
                    letter-spacing: -0.5px;
                }}
                .header-tagline {{
                    font-size: 12px;
                    opacity: 0.9;
                    letter-spacing: 1px;
                    text-transform: uppercase;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .greeting {{
                    font-size: 16px;
                    margin-bottom: 20px;
                    font-weight: 600;
                }}
                .main-text {{
                    color: #4b5563;
                    margin-bottom: 24px;
                    line-height: 1.7;
                }}
                .highlight-box {{
                    background: linear-gradient(135deg, #f0f9ff 0%, #f3e8ff 100%);
                    padding: 24px;
                    border-radius: 10px;
                    border: 1px solid #e9d5ff;
                    margin: 28px 0;
                }}
                .highlight-title {{
                    font-size: 15px;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 12px;
                }}
                .highlight-box ul {{
                    list-style: none;
                    margin: 0;
                    padding: 0;
                }}
                .highlight-box li {{
                    padding: 8px 0;
                    padding-left: 24px;
                    position: relative;
                    color: #475569;
                    font-size: 14px;
                }}
                .highlight-box li:before {{
                    content: "✓";
                    position: absolute;
                    left: 0;
                    color: #1e40af;
                    font-weight: bold;
                    font-size: 16px;
                }}
                .cta-button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
                    color: white;
                    padding: 14px 32px;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 14px;
                    margin: 28px 0;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3);
                    transition: all 0.3s ease;
                }}
                .cta-button:hover {{
                    opacity: 0.9;
                }}
                .section-title {{
                    font-size: 16px;
                    font-weight: 700;
                    color: #1f2937;
                    margin-top: 28px;
                    margin-bottom: 12px;
                }}
                .next-steps {{
                    background-color: #f8fafc;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 24px 0;
                }}
                .next-steps ul {{
                    list-style: none;
                    margin: 0;
                    padding: 0;
                }}
                .next-steps li {{
                    padding: 8px 0;
                    padding-left: 24px;
                    position: relative;
                    color: #475569;
                    font-size: 14px;
                }}
                .next-steps li:before {{
                    content: "→";
                    position: absolute;
                    left: 0;
                    color: #1e40af;
                    font-weight: bold;
                    font-size: 16px;
                }}
                .closing {{
                    color: #4b5563;
                    margin: 24px 0;
                    line-height: 1.7;
                    font-size: 14px;
                }}
                .signature {{
                    font-weight: 600;
                    color: #1f2937;
                    margin-top: 28px;
                }}
                .footer {{
                    background-color: #1e293b;
                    color: white;
                    padding: 30px;
                    text-align: center;
                    font-size: 13px;
                    border-top: 1px solid #e2e8f0;
                }}
                .footer-logo {{
                    font-size: 18px;
                    font-weight: 800;
                    margin-bottom: 12px;
                }}
                .footer-content {{
                    opacity: 0.9;
                    margin: 8px 0;
                }}
                .footer a {{
                    color: #93c5fd;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <!-- Header -->
                <div class="header">
                    <div class="header-logo">SimplifiQ</div>
                    <div class="header-tagline">AI-Powered Business Intelligence</div>
                </div>

                <!-- Content -->
                <div class="content">
                    <div class="greeting">Hello {prospect_name},</div>

                    <div class="main-text">
                        Thank you for your interest in exploring how artificial intelligence can transform {company_name}. 
                        We have prepared a comprehensive, personalized analysis of your organization and identified 
                        strategic opportunities for AI adoption that can drive measurable business value.
                    </div>

                    <!-- Highlight Box -->
                    <div class="highlight-box">
                        <div class="highlight-title">📎 Your AI Audit Report is Ready</div>
                        <ul>
                            <li>Executive Summary & Market Position</li>
                            <li>Industry-Specific AI Opportunities</li>
                            <li>Implementation Roadmap</li>
                            <li>Expected ROI & Success Metrics</li>
                        </ul>
                    </div>

                    <!-- Next Steps Section -->
                    <div class="section-title">What's Next?</div>
                    <div class="main-text">
                        We would welcome the opportunity to discuss how these insights can specifically benefit {company_name}. 
                        Our team specializes in helping organizations like yours evaluate, plan, and implement AI solutions that 
                        deliver real results.
                    </div>

                    <div class="next-steps">
                        <div class="highlight-title" style="margin-bottom: 12px;">Our Team Can Help You:</div>
                        <ul>
                            <li>Conduct a comprehensive AI readiness assessment</li>
                            <li>Design and execute pilot projects</li>
                            <li>Develop strategic implementation roadmaps</li>
                            <li>Optimize ROI across your organization</li>
                        </ul>
                    </div>

                    <center>
                        <a href="mailto:career@simplifiiq.com?subject=AI Audit Discussion - {company_name}" class="cta-button">
                            Schedule Your Consultation
                        </a>
                    </center>

                    <div class="closing">
                        Should you have any questions regarding the audit report or would like to discuss specific 
                        opportunities in more detail, please don't hesitate to reach out. We're here to help.
                    </div>

                    <div class="signature">
                        Best regards,<br/>
                        <strong>SimplifiQ Strategic Team</strong><br/>
                        <span style="font-weight: normal; color: #64748b;">AI Solutions for Enterprise</span>
                    </div>
                </div>

                <!-- Footer -->
                <div class="footer">
                    <div class="footer-logo">SimplifiQ</div>
                    <div class="footer-content">
                        <strong>Email:</strong> <a href="mailto:career@simplifiiq.com">career@simplifiiq.com</a>
                    </div>
                    <div class="footer-content">
                        <strong>Web:</strong> <a href="https://simplifiiq.com">simplifiiq.com</a>
                    </div>
                    <div class="footer-content" style="margin-top: 16px; opacity: 0.7;">
                        © 2024 SimplifiQ. All Rights Reserved.<br/>
                        This message was sent to you regarding your AI audit inquiry.
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    return html_body

def attach_pdf(msg: MIMEMultipart, pdf_path: str) -> None:
    """
    Attach PDF file to email message
    """
    try:
        with open(pdf_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        
        # Add header
        filename = Path(pdf_path).name
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )
        
        msg.attach(part)
        logger.info(f"✅ PDF attached: {filename}")
    
    except Exception as e:
        logger.error(f"❌ Failed to attach PDF: {e}")
        raise

def send_via_smtp(sender_email: str, sender_password: str, to_email: str, msg: MIMEMultipart) -> None:
    """
    Send email via Gmail SMTP server
    """
    try:
        # Gmail SMTP server settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        
        # Create secure connection
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
        
        # Login
        server.login(sender_email, sender_password)
        logger.info("✅ Gmail login successful")
        
        # Send email
        server.send_message(msg)
        logger.info("✅ Email sent via SMTP")
        
        # Quit
        server.quit()
    
    except smtplib.SMTPAuthenticationError:
        logger.error("❌ Gmail authentication failed - check credentials")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"❌ SMTP error: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
        raise

def test_email_connection() -> bool:
    """
    Test if email credentials are valid
    """
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        
        if not sender_email or not sender_password:
            logger.error("Email credentials not found")
            return False
        
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5)
        server.login(sender_email, sender_password)
        server.quit()
        
        logger.info("✅ Email connection test passed")
        return True
    
    except Exception as e:
        logger.error(f"❌ Email connection test failed: {e}")
        return False