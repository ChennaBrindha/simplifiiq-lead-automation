"""
Google Sheets Logger
Optional bonus feature - logs all lead submissions to a Google Sheet
"""

import logging
import os
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def log_to_sheets(lead, status: str) -> bool:
    """
    Log lead submission to Google Sheets
    
    Args:
        lead: Lead object with name, email, company, website
        status: Status of processing (completed, failed, etc.)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get credentials file path
        creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        sheet_name = os.getenv("GOOGLE_SHEET_NAME")
        
        if not creds_path or not sheet_name:
            logger.warning("⚠️ Google Sheets credentials not configured, skipping logging")
            return False
        
        # Check if credentials file exists
        if not os.path.exists(creds_path):
            logger.warning(f"⚠️ Credentials file not found: {creds_path}")
            return False
        
        # Authenticate
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Open spreadsheet
        sheet = client.open(sheet_name).sheet1
        
        # Prepare row data
        row_data = [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Timestamp
            lead.name,
            lead.email,
            lead.company,
            lead.website,
            status
        ]
        
        # Append row
        sheet.append_row(row_data)
        
        logger.info(f"✅ Lead logged to Google Sheets: {lead.company}")
        return True
    
    except Exception as e:
        logger.warning(f"⚠️ Failed to log to Google Sheets: {e}")
        return False

def setup_sheets_template(sheet_name: str) -> bool:
    """
    Create and setup a new Google Sheet with headers
    
    Args:
        sheet_name: Name of the sheet to create
    
    Returns:
        True if successful
    """
    try:
        creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        
        if not creds_path or not os.path.exists(creds_path):
            logger.error("Credentials file not found")
            return False
        
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Create new spreadsheet
        spreadsheet = client.create(sheet_name)
        sheet = spreadsheet.sheet1
        
        # Set headers
        headers = [
            "Timestamp",
            "Prospect Name",
            "Email",
            "Company",
            "Website",
            "Status"
        ]
        
        sheet.insert_row(headers, 1)
        
        # Format header row
        sheet.format_rows([1], {
            "backgroundColor": {
                "red": 0.99,
                "green": 0.41,
                "blue": 0.60
            },
            "textFormat": {
                "bold": True,
                "foregroundColor": {
                    "red": 1,
                    "green": 1,
                    "blue": 1
                }
            }
        })
        
        # Set column widths
        sheet.update_cells([gspread.models.CellNotation('A:F')])
        
        logger.info(f"✅ Google Sheet created: {sheet_name}")
        logger.info(f"📝 Spreadsheet URL: {spreadsheet.url}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Failed to create Google Sheet: {e}")
        return False

def test_sheets_connection() -> bool:
    """
    Test if Google Sheets credentials are valid
    """
    try:
        creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        sheet_name = os.getenv("GOOGLE_SHEET_NAME")
        
        if not creds_path or not sheet_name:
            logger.warning("Google Sheets not configured")
            return False
        
        if not os.path.exists(creds_path):
            logger.warning(f"Credentials file not found: {creds_path}")
            return False
        
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Try to open the sheet
        client.open(sheet_name)
        
        logger.info("✅ Google Sheets connection test passed")
        return True
    
    except Exception as e:
        logger.warning(f"⚠️ Google Sheets connection test failed: {e}")
        return False