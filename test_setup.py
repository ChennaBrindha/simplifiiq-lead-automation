"""
SimplifiQ Setup Verification Script
Tests all credentials and dependencies
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print("\n" + "="*50)
print("SimplifiQ Setup Verification")
print("="*50 + "\n")

# Load environment variables
load_dotenv()

def test_result(name: str, passed: bool, details: str = ""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {name}")
    if details:
        print(f"       {details}\n")
    else:
        print()
    return passed

all_passed = True

# Test 1: Python version
print("1️⃣  PYTHON & DEPENDENCIES")
print("-" * 50)
try:
    import fastapi
    import openai
    import reportlab
    test_result("Python dependencies", True, f"FastAPI {fastapi.__version__}")
except ImportError as e:
    all_passed = False
    test_result("Python dependencies", False, f"Missing: {e}")

# Test 2: .env file
print("\n2️⃣  ENVIRONMENT VARIABLES")
print("-" * 50)
env_exists = Path(".env").exists()
test_result(".env file", env_exists, "File found" if env_exists else "Create from .env.example")

# Test 3: OpenAI API
print("\n3️⃣  OPENAI API")
print("-" * 50)
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key and openai_key.startswith("sk-"):
    try:
        import openai
        openai.api_key = openai_key
        # Don't actually call the API, just check the key format
        test_result("OpenAI API Key", True, f"Key found (****{openai_key[-4:]})")
    except Exception as e:
        all_passed = False
        test_result("OpenAI API Key", False, str(e))
else:
    all_passed = False
    test_result("OpenAI API Key", False, "Not set or invalid format (should start with 'sk-')")

# Test 4: Gmail SMTP
print("\n4️⃣  GMAIL SMTP")
print("-" * 50)
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

if sender_email and sender_password:
    try:
        import smtplib
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5)
        server.login(sender_email, sender_password)
        server.quit()
        test_result("Gmail Authentication", True, f"Connected as {sender_email}")
    except smtplib.SMTPAuthenticationError:
        all_passed = False
        test_result("Gmail Authentication", False, 
                   "Login failed. Check credentials or use App Password")
    except Exception as e:
        all_passed = False
        test_result("Gmail Authentication", False, f"Connection error: {e}")
else:
    all_passed = False
    if not sender_email:
        test_result("Gmail Configuration", False, "SENDER_EMAIL not set")
    if not sender_password:
        test_result("Gmail Configuration", False, "SENDER_PASSWORD not set")

# Test 5: Google Sheets (optional)
print("\n5️⃣  GOOGLE SHEETS (OPTIONAL)")
print("-" * 50)
creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
sheet_name = os.getenv("GOOGLE_SHEET_NAME")

if creds_path and Path(creds_path).exists():
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        creds = Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        client = gspread.authorize(creds)
        
        if sheet_name:
            try:
                sheet = client.open(sheet_name)
                test_result("Google Sheets", True, f"Connected to '{sheet_name}'")
            except Exception as e:
                test_result("Google Sheets", False, 
                           f"Sheet '{sheet_name}' not found or not shared with service account")
        else:
            test_result("Google Sheets Configuration", False, "GOOGLE_SHEET_NAME not set")
    except Exception as e:
        test_result("Google Sheets", False, f"Authentication error: {e}")
else:
    test_result("Google Sheets (Optional)", True, "Not configured (optional feature)")

# Test 6: Directory structure
print("\n6️⃣  DIRECTORY STRUCTURE")
print("-" * 50)
templates_dir = Path("templates")
reports_dir = Path("reports")

test_result("templates/ directory", templates_dir.exists() or templates_dir.mkdir(exist_ok=True))
test_result("reports/ directory", reports_dir.exists() or reports_dir.mkdir(exist_ok=True))

# Test 7: Key files
print("\n7️⃣  KEY FILES")
print("-" * 50)
test_result("main.py", Path("main.py").exists())
test_result("enrichment.py", Path("enrichment.py").exists())
test_result("pdf_generator.py", Path("pdf_generator.py").exists())
test_result("email_sender.py", Path("email_sender.py").exists())
test_result("templates/form.html", Path("templates/form.html").exists())

# Summary
print("\n" + "="*50)
if all_passed:
    print("✅ ALL TESTS PASSED!")
    print("="*50)
    print("\n🚀 You're ready to run the server:")
    print("   python main.py")
    print("\n📖 Then visit: http://localhost:8000")
    sys.exit(0)
else:
    print("❌ SOME TESTS FAILED")
    print("="*50)
    print("\n📖 Check the README.md for setup instructions:")
    print("   https://github.com/simplifiiq/lead-automation")
    print("\n💬 Need help? Email: career@simplifiiq.com")
    sys.exit(1)