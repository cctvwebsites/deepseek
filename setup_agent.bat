@echo off
echo ====================================
echo    DeepSeek AI Agent Setup Script
echo ====================================
echo.
echo [1/6] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python is installed.
echo.
echo [2/6] Creating project folder...
set "PROJECT_FOLDER=%USERPROFILE%\Desktop\deepseek-ai-coder"
if not exist "%PROJECT_FOLDER%" (
    mkdir "%PROJECT_FOLDER%"
    echo ✓ Created folder: %PROJECT_FOLDER%
) else (
    echo ✓ Folder already exists: %PROJECT_FOLDER%
)
cd /d "%PROJECT_FOLDER%"
echo.
echo [3/6] Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created.
) else (
    echo ✓ Virtual environment already exists.
)
echo.
echo [4/6] Activating the virtual environment...
call .\venv\Scripts\activate.bat
echo ✓ Virtual environment is now ACTIVE.
echo.
echo [5/6] Installing required libraries...
pip install openai python-dotenv PyGithub
echo ✓ Libraries installed successfully.
echo.
echo [6/6] Creating the project file structure...
if not exist "auth" mkdir auth
if not exist "tools" mkdir tools
echo venv/>.gitignore
echo auth/>>.gitignore
echo __pycache__/>>.gitignore
echo *.pyc>>.gitignore
echo ✓ Project structure created.
echo.
echo ====================================
echo       SETUP COMPLETE!
echo ====================================
echo.
echo Next: Edit the auth\.env file with your API keys.
echo.
pause