# 📦 SimplifiQ - Complete File Manifest

## All Files You've Received

### 🔴 REQUIRED - Core Application Files

#### 1. **main.py** ⭐ START HERE
   - FastAPI server entry point
   - Orchestrates the entire workflow
   - Command: `python main.py`

#### 2. **enrichment.py** (Company Analysis)
   - Scrapes websites
   - Calls OpenAI for insights
   - Generates use cases & recommendations

#### 3. **pdf_generator.py** (Report Creation)
   - Creates professional PDF reports
   - Uses reportlab library
   - Customizable styling

#### 4. **email_sender.py** (Email Delivery)
   - Sends emails via Gmail SMTP
   - Includes HTML formatting
   - Attaches PDF files

#### 5. **sheets_logger.py** (Optional Tracking)
   - Logs leads to Google Sheets
   - Optional bonus feature
   - Auto-creates sheet structure

### 🟢 CONFIGURATION Files

#### 6. **.env.example** → Copy to **.env**
   ```bash
   cp .env.example .env
   # Then edit with your credentials
   ```
   Contains:
   - OPENAI_API_KEY (required)
   - SENDER_EMAIL (required)
   - SENDER_PASSWORD (required)
   - GOOGLE_CREDENTIALS_PATH (optional)

#### 7. **requirements.txt**
   - All Python dependencies
   - Install: `pip install -r requirements.txt`

### 🟡 FRONTEND Files

#### 8. **templates/form.html**
   - Lead capture form
   - Beautiful, responsive design
   - Auto-creates directory

### 🔵 DOCUMENTATION Files

#### 9. **README.md** 📖 COMPREHENSIVE GUIDE
   - Full setup instructions
   - Configuration guides for all services
   - Troubleshooting section
   - Cost estimates
   - Scaling guide

#### 10. **QUICKSTART.md** ⚡ FOR EXPERIENCED DEVS
   - TL;DR version
   - 5-minute setup
   - Quick reference

### 🟣 DEPLOYMENT Files

#### 11. **Procfile**
   - For Heroku deployment
   - One-click deploy ready

#### 12. **Dockerfile**
   - Container deployment
   - Works with Docker/Kubernetes

#### 13. **docker-compose.yml**
   - Local Docker development
   - Run: `docker-compose up`

### ⚪ SETUP Files

#### 14. **setup.sh** (Mac/Linux)
   - Automated setup script
   - Run: `bash setup.sh`

#### 15. **setup.bat** (Windows)
   - Automated setup script
   - Run: `setup.bat`

#### 16. **test_setup.py** ✅ VERIFY EVERYTHING
   - Tests all credentials
   - Checks dependencies
   - Run: `python test_setup.py`

### ⚫ SECURITY Files

#### 17. **.gitignore**
   - Prevents committing secrets
   - Add to git repo

---

## 🚀 QUICK START STEPS

### Step 1: Create .env File
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Step 2: Install Dependencies
```bash
# Option A: Automated
# Windows: setup.bat
# Mac/Linux: bash setup.sh

# Option B: Manual
python -m venv venv
source venv/bin/activate  # or: . venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Get Credentials

**OpenAI:**
- Go to https://platform.openai.com/api-keys
- Create key → Copy to OPENAI_API_KEY in .env

**Gmail:**
- Enable 2FA at https://myaccount.google.com
- Get App Password at https://myaccount.google.com/apppasswords
- Copy to SENDER_EMAIL & SENDER_PASSWORD

**Google Sheets (Optional):**
- Create service account at https://console.cloud.google.com
- Download credentials.json
- Save to project folder

### Step 4: Verify Setup
```bash
python test_setup.py
# Should show ✅ ALL TESTS PASSED
```

### Step 5: Run the Server
```bash
python main.py
# Open: http://localhost:8000
```

---

## 📁 Final Directory Structure

After setup, your folder should look like:
```
simplifiiq-lead-automation/
├── main.py                    # Entry point
├── enrichment.py
├── pdf_generator.py
├── email_sender.py
├── sheets_logger.py
├── test_setup.py
├── templates/
│   └── form.html
├── reports/                   # Created automatically
├── venv/                      # Created by setup
├── .env                       # COPY FROM .env.example
├── .env.example
├── .gitignore
├── requirements.txt
├── setup.sh
├── setup.bat
├── Procfile
├── Dockerfile
├── docker-compose.yml
├── README.md                  # Full documentation
├── QUICKSTART.md
└── credentials.json           # Optional (Google Sheets)
```

---

## 🎯 Which Files to Edit

| Task | File |
|------|------|
| Change credentials | `.env` |
| Customize form fields | `templates/form.html` + `main.py` |
| Change email message | `email_sender.py` |
| Modify PDF design | `pdf_generator.py` |
| Add AI insights | `enrichment.py` |
| Change business logic | `main.py` |

---

## 🚢 Deployment

### Heroku (Recommended for beginners)
1. Already have `Procfile`
2. Push to GitHub
3. Connect to Heroku
4. Add environment variables in Heroku dashboard
5. Deploy

### Docker (Recommended for production)
1. Already have `Dockerfile`
2. Run: `docker build -t simplifiiq .`
3. Run: `docker run -p 8000:8000 simplifiiq`

### Docker Compose (For local development)
1. Already have `docker-compose.yml`
2. Make sure `.env` exists
3. Run: `docker-compose up`

---

## 📞 File-Specific Help

### If main.py crashes:
1. Check `.env` file exists
2. Run: `python test_setup.py`
3. Check logs for error message

### If emails don't send:
1. Run: `python test_setup.py`
2. Check SENDER_EMAIL and SENDER_PASSWORD in .env
3. Make sure it's an App Password, not Gmail password

### If PDF doesn't generate:
1. Check `reports/` directory exists
2. Check for error in console logs
3. Verify disk space available

### If Google Sheets doesn't log:
1. Run: `python test_setup.py`
2. Check credentials.json is in project folder
3. Verify sheet is shared with service account email

---

## ✅ Checklist Before Deployment

- [ ] .env file created and filled
- [ ] `python test_setup.py` passes all tests
- [ ] Form loads at http://localhost:8000
- [ ] Can submit a test lead
- [ ] Email is received
- [ ] PDF looks good
- [ ] Google Sheets logs (if enabled)
- [ ] README.md reviewed
- [ ] Credentials are secure (not in git)
- [ ] Ready to deploy!

---

## 💡 Tips

1. **During Development**: Use `python test_setup.py` frequently
2. **Before Deploying**: Test everything locally first
3. **Security**: Never commit .env file to git
4. **Logging**: Check console output for detailed error messages
5. **Customization**: Start with small changes to one file
6. **Testing**: Always test locally before deploying

---

## 📚 Reading Order

1. **This File** (you are here) ← Overview
2. **QUICKSTART.md** ← 5-minute setup
3. **README.md** ← Complete details
4. **Source code files** ← When you want to customize

---

## 🎓 Learning Resources

- FastAPI docs: https://fastapi.tiangolo.com
- OpenAI API: https://platform.openai.com/docs
- reportlab: https://www.reportlab.com
- gspread: https://docs.gspread.org

---

**You're all set! Start with Step 1 above and you'll be done in 15 minutes. 🚀**

Questions? Email: career@simplifiiq.com