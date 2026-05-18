# SimplifiQ | AI Lead Automation System

An automated system that captures business leads, enriches company data with AI, generates personalized PDF reports, and sends them via email—all automatically.

## 🎯 What It Does

```
Lead Submits Form
       ↓
Website Scraping & AI Analysis
       ↓
Generate Personalized PDF Report
       ↓
Send Email with Report
       ↓
Log to Google Sheets (optional)
```

## 🚀 Quick Start (5 minutes)

### 1. Install Python & Dependencies

```bash
# Python 3.8 or higher required
python --version

# Clone/download this project
cd simplifiiq-lead-automation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials (see Setup Guides below)
```

### 3. Run the Server

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Visit: **http://localhost:8000** in your browser

---

## 🔧 Configuration Guides

### A. OpenAI API Setup (Required)

1. Go to https://platform.openai.com
2. Sign up or login
3. Click "API keys" in the left menu
4. Create a new secret key
5. Copy it and paste into `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

**Cost:** ~$0.50-$2.00 per lead (for web scraping + AI analysis)

---

### B. Gmail SMTP Setup (Required for Email)

Gmail now requires "App Passwords" instead of your regular password.

#### Step 1: Enable 2-Factor Authentication
1. Go to https://myaccount.google.com
2. Click "Security" on the left
3. Enable "2-Step Verification" (if not already enabled)

#### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or your device)
3. Google generates a 16-character password
4. Copy it to `.env`:
   ```
   SENDER_EMAIL=your-email@gmail.com
   SENDER_PASSWORD=xxxx xxxx xxxx xxxx
   ```

**Note:** Don't use your actual Gmail password. App passwords are more secure.

---

### C. Google Sheets Setup (Optional/Bonus)

To automatically log all leads to a Google Sheet:

#### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com
2. Click "Create Project"
3. Name it "SimplifiQ"
4. Wait for it to be created

#### Step 2: Enable APIs
1. Search for "Google Sheets API" in the search bar
2. Click "Enable"
3. Search for "Google Drive API"
4. Click "Enable"

#### Step 3: Create Service Account
1. Go to "Service Accounts" (search in top bar)
2. Click "Create Service Account"
3. Name: "simplifiiq-bot"
4. Click "Create and Continue"
5. Click "Create Key" → "JSON"
6. A JSON file downloads automatically
7. Move it to your project folder and name it `credentials.json`

#### Step 4: Create Google Sheet
1. Go to https://sheets.google.com
2. Create a new sheet, name it exactly: `SimplifiQ Leads`
3. Share it with the email from the JSON file (it's in `client_email`)

#### Step 5: Update .env
```
GOOGLE_CREDENTIALS_PATH=./credentials.json
GOOGLE_SHEET_NAME=SimplifiQ Leads
```

---

## 📁 Project Structure

```
simplifiiq-lead-automation/
├── main.py                 # FastAPI server (entry point)
├── enrichment.py           # Web scraping + AI logic
├── pdf_generator.py        # PDF report creation
├── email_sender.py         # Email sending logic
├── sheets_logger.py        # Google Sheets logging (bonus)
├── templates/
│   └── form.html          # Lead capture form
├── reports/               # Generated PDFs (created automatically)
├── requirements.txt        # Python dependencies
├── .env                   # Your credentials (create from .env.example)
├── .env.example           # Template
└── README.md              # This file
```

---

## 🧪 Testing

### 1. Test Email Setup
```python
from email_sender import test_email_connection
result = test_email_connection()
# Should return True
```

### 2. Test Google Sheets Setup
```python
from sheets_logger import test_sheets_connection
result = test_sheets_connection()
# Should return True
```

### 3. Test Full Flow
1. Open http://localhost:8000
2. Fill in the form with test data
3. Submit
4. Check your email for the report
5. Check Google Sheets for the log entry

---

## 📊 How It Works

### Form Submission
User fills out the form with:
- Name, Email, Company, Website

### Company Enrichment
The system:
1. **Scrapes** the company website
2. **Uses OpenAI** to analyze the content
3. **Generates** AI insights, use cases, and recommendations

### PDF Generation
Creates a professional report with:
- Company analysis
- AI opportunities
- Actionable next steps
- SimplifiQ branding

### Email Delivery
Sends a personalized email with:
- HTML-formatted message
- PDF report as attachment
- Call-to-action buttons

### Logging (Optional)
Records in Google Sheets:
- Timestamp
- Prospect name & email
- Company & website
- Processing status

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** to GitHub
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use App Passwords** for Gmail (not your real password)

3. **Limit API Key Permissions** on OpenAI dashboard

4. **Rotate Credentials Regularly**
   - Generate new API keys quarterly
   - Regenerate Gmail app passwords

5. **Use Environment Variables** (never hardcode secrets)

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "OpenAI API key not found"
**Solution:** Make sure `.env` file exists and has:
```
OPENAI_API_KEY=sk-your-actual-key
```

### Issue: "Gmail authentication failed"
**Solutions:**
1. Check you're using an App Password (not your real Gmail password)
2. Check 2FA is enabled
3. Ensure `SENDER_EMAIL` matches your Gmail account
4. Check for extra spaces in passwords

### Issue: "Failed to scrape website"
**Possible causes:**
- Website is down
- Website blocks scrapers
- Website structure is unusual

**Solution:** Website scraping is best-effort; the system falls back gracefully

### Issue: Google Sheets not logging
**Solutions:**
1. Make sure credentials.json is in the project folder
2. Make sure the sheet is named exactly `SimplifiQ Leads`
3. Make sure the sheet is shared with the service account email
4. Run: `from sheets_logger import test_sheets_connection`

---

## 📈 Scaling & Deployment

### Local Development
```bash
python main.py
```

### Production Deployment

#### Option 1: Heroku (Free tier available)
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-your-key
heroku config:set SENDER_EMAIL=your-email@gmail.com
heroku config:set SENDER_PASSWORD=your-password

# Deploy
git push heroku main
```

#### Option 2: Railway.app
1. Connect your GitHub repo
2. Add environment variables in dashboard
3. Deploy with one click

#### Option 3: DigitalOcean App Platform
1. Connect GitHub
2. Add environment variables
3. Deploy

---

## 💰 Cost Estimate

| Service | Cost | Notes |
|---------|------|-------|
| OpenAI API | $0.50-$2/lead | Web scraping + AI analysis |
| Gmail SMTP | Free | (with Gmail account) |
| Google Sheets | Free | (with Google account) |
| Hosting | $0-$20/month | Depends on platform |
| **Total** | **$0.50-$2 per lead** | + hosting |

100 leads/month = ~$50-$200 + hosting

---

## 🎨 Customization

### Change Email Template
Edit the HTML in `email_sender.py` → `create_email_body()`

### Change PDF Styling
Edit `pdf_generator.py` → `build_story()`

### Change Form Fields
1. Edit `templates/form.html` (HTML)
2. Update `Lead` class in `main.py` (Python model)
3. Update enrichment logic in `enrichment.py`

### Add More AI Insights
Edit `enrichment.py` → Add new functions like `generate_recommendations()`

---

## 📞 Support

- **OpenAI Help:** https://help.openai.com
- **Gmail Issues:** https://support.google.com/mail
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **This Project Issues:** Check logs in console

---

## 📝 Next Steps

1. ✅ Install dependencies
2. ✅ Set up OpenAI API
3. ✅ Set up Gmail
4. ✅ (Optional) Set up Google Sheets
5. ✅ Run the server
6. ✅ Test the form
7. ✅ Customize branding
8. ✅ Deploy to production

---

## 📄 License

MIT License - Use freely for personal and commercial projects.

---

## 🙌 Acknowledgments

- **SimplifiQ** - For the original assessment
- **OpenAI** - For GPT-based insights
- **FastAPI** - For the web framework
- **reportlab** - For PDF generation

---

**Made with ❤️ for modern businesses adopting AI**

Questions? Issues? Want to contribute? Reach out to career@simplifiiq.com