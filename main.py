"""
SimplifiQ AI Lead Automation System
Main FastAPI server
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import logging
import os
from dotenv import load_dotenv
import asyncio

from enrichment import enrich_company
from pdf_generator import generate_pdf_report
from email_sender import send_email_with_pdf
from sheets_logger import log_to_sheets

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="SimplifiQ Lead Automation")

# Create necessary directories
Path("reports").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

# Data model for form submission
class Lead(BaseModel):
    name: str
    email: str
    company: str
    website: str

@app.get("/", response_class=HTMLResponse)
async def get_form():
    """Serve the lead capture form"""
    try:
        with open("templates/form.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Form file not found</h1>"


@app.post("/submit")
async def submit_lead(lead: Lead):
    """
    Main workflow: receive lead → enrich → generate PDF → send email → log
    """
    try:
        logger.info(f"📝 Received lead: {lead.company} ({lead.email})")
        
        # Step 1: Enrich company data with AI
        logger.info("🔍 Enriching company data...")
        enriched_data = await enrich_company(lead)
        
        # Step 2: Generate personalized PDF
        logger.info("📄 Generating PDF report...")
        pdf_path = generate_pdf_report(lead, enriched_data)
        
        # Step 3: Send email with PDF (WRAPPED IN SAFETY NET)
        logger.info("📧 Sending email...")
        try:
            # Fixed function arguments to match your email_sender.py exactly
            email_result = send_email_with_pdf(lead.email, lead.company, pdf_path)
            
            if email_result:
                logger.info("🎉 Email sent successfully!")
            else:
                logger.warning("⚠️ Email failed to send, but keeping server alive.")
        except Exception as email_err:
            logger.error(f"❌ Failed to send email safely: {str(email_err)}")
        
        # Step 4: Log to Google Sheets (optional)
        try:
            logger.info("📊 Logging to Google Sheets...")
            log_to_sheets(lead, "completed")
        except Exception as e:
            logger.warning(f"⚠️ Sheets logging failed: {e}")
        
        logger.info(f"✅ Lead {lead.company} processed successfully!")
        
        # ALWAYS return success to the frontend so the user doesn't see an error
        return {
            "status": "success",
            "message": f"Report successfully generated for {lead.company}!",
            "company": lead.company,
            "pdf_path": pdf_path
        }
    
    except Exception as e:
        logger.error(f"❌ Critical Error processing lead: {str(e)}")
        try:
            log_to_sheets(lead, f"failed: {str(e)}")
        except:
            pass
        raise HTTPException(status_code=500, detail="We experienced a temporary hiccup processing your request.")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)