"""
UPDATED main.py
Mandatory PDF generation + mandatory downloadable report link
Email failure will not block report delivery
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

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

# Directories
Path("reports").mkdir(exist_ok=True)
Path("templates").mkdir(exist_ok=True)

# Serve reports publicly
app.mount("/reports", StaticFiles(directory="reports"), name="reports")


class Lead(BaseModel):
    name: str
    email: str
    company: str
    website: str


@app.get("/", response_class=HTMLResponse)
async def get_form():
    try:
        with open("templates/form.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Form file not found</h1>"


@app.post("/submit")
async def submit_lead(lead: Lead):
    try:
        logger.info(f"📝 Received lead: {lead.company} ({lead.email})")

        # Step 1: Enrichment
        logger.info("🔍 Enriching company data...")
        enriched_data = await enrich_company(lead)

        # Step 2: PDF generation
        logger.info("📄 Generating PDF report...")
        pdf_path = generate_pdf_report(lead, enriched_data)

        pdf_filename = os.path.basename(pdf_path)

        # Public report URL
        base_url = os.getenv(
            "RAILWAY_PUBLIC_DOMAIN",
            "simplifiiq-lead-automation-production.up.railway.app"
        )

        report_url = f"https://{base_url}/reports/{pdf_filename}"

        # Step 3: Email attempt
        logger.info("📧 Sending email...")
        email_result = send_email_with_pdf(
            to_email=lead.email,
            company=lead.company,
            pdf_path=pdf_path
        )

        if not email_result:
            logger.warning("⚠️ Email failed, but public PDF link is available.")

        # Step 4: Logging
        try:
            status = "completed" if email_result else "pdf_generated_email_failed"
            log_to_sheets(lead, status)
        except Exception as e:
            logger.warning(f"⚠️ Sheets logging failed: {e}")

        return {
            "status": "success",
            "company": lead.company,
            "pdf_path": pdf_path,
            "report_url": report_url,
            "email_sent": email_result,
            "message": (
                f"Professional report generated successfully. "
                f"Download here: {report_url}"
            )
        }

    except Exception as e:
        logger.error(f"❌ Error processing lead: {str(e)}")

        try:
            log_to_sheets(lead, f"failed: {str(e)}")
        except Exception:
            pass

        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )