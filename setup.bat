@echo off
REM SimplifiQ Setup Script for Windows

echo.
echo ==========================================
echo SimplifiQ AI Lead Automation - Setup
echo ==========================================
echo.

REM Check Python
echo [*] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python not found. Please install Python 3.8 or higher.
    echo     Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo     Found Python %PYTHON_VERSION%
echo.

REM Create virtual environment
echo [*] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo     Virtual environment created
) else (
    echo     Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
echo     Virtual environment activated
echo.

REM Install dependencies
echo [*] Installing Python dependencies...
pip install -q -r requirements.txt
echo     All dependencies installed
echo.

REM Create .env file if it doesn't exist
echo [*] Setting up configuration...
if not exist ".env" (
    copy .env.example .env
    echo     Created .env file (edit with your credentials)
) else (
    echo     .env file already exists
)
echo.

REM Create directories
if not exist "reports" mkdir reports
if not exist "templates" mkdir templates

echo ==========================================
echo [OK] Setup Complete!
echo ==========================================
echo.
echo [*] Next Steps:
echo     1. Edit .env file with your credentials:
echo        - OPENAI_API_KEY
echo        - SENDER_EMAIL ^& SENDER_PASSWORD
echo.
echo     2. Start the server:
echo        python main.py
echo.
echo     3. Open your browser:
echo        http://localhost:8000
echo.
echo [*] For detailed setup instructions, see README.md
echo.
pause