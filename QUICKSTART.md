# Quick Start Guide (TL;DR)

## Installation (2 minutes)

```bash
# Clone repo and enter directory
git clone <repo-url>
cd simplifiiq-lead-automation

# Setup (choose your OS)
# Windows:
setup.bat

# Mac/Linux:
bash setup.sh

# Or manual:
python -m venv venv
source venv/bin/activate  # or . venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Configuration (5 minutes)

### 1. Get OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create new secret key
- Add to `.env`: `OPENAI_API_KEY=sk-...`

### 2. Get Gmail App Password
- Go to https://myaccount.google.com/apppasswords (2FA must be enabled)
- Generate "Mail" password
- Add to `.env`:
  ```
  SENDER_EMAIL=your-email@gmail.com
  SENDER_PASSWORD=xxxx xxxx xxxx xxxx
  ```

### 3. (Optional) Google Sheets
- Create service account at https://console.cloud.google.com
- Download JSON key file
- Save as `credentials.json`
- Create Google Sheet named `SimplifiQ Leads`
- Share with service account email
- Add to `.env`:
  ```
  GOOGLE_CREDENTIALS_PATH=./credentials.json
  GOOGLE_SHEET_NAME=SimplifiQ Leads
  ```

## Run

```bash
python main.py
# Visit http://localhost:8000
```

## Test Everything Works

```bash
python test_setup.py
```

## Deploy

**Heroku:**
```bash
heroku create app-name
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set SENDER_EMAIL=...
heroku config:set SENDER_PASSWORD=...
git push heroku main
```

**Railway/DigitalOcean/Other:** Add env vars in dashboard, connect GitHub, deploy.

---

## Architecture

```
POST /submit (form data)
    ↓
main.py: validate input
    ↓
enrichment.py: scrape website + OpenAI analysis
    ↓
pdf_generator.py: create PDF
    ↓
email_sender.py: send to prospect
    ↓
sheets_logger.py: log to Google Sheets
    ↓
return success response
```

## Cost per Lead
- OpenAI: ~$0.50-$2.00
- Gmail: Free
- Google Sheets: Free
- Hosting: $0-$20/month

## Customization

- **Form fields**: `templates/form.html` + `main.py` Lead class
- **Email template**: `email_sender.py` → `create_email_body()`
- **PDF styling**: `pdf_generator.py` → `build_story()`
- **AI insights**: `enrichment.py` → prompts

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| OpenAI API error | Check `OPENAI_API_KEY` in .env |
| Gmail auth failed | Use App Password, not Gmail password |
| Sheets not logging | Share sheet with service account email |
| Website scrape fails | Website is down or blocks scrapers (graceful fallback) |

## Full Documentation

See **README.md** for complete setup, security, scaling, and troubleshooting guides.

---

**Ready to go!** Questions? Email: career@simplifiiq.com