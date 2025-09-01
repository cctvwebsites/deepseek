@echo off
echo Starting your AI Agent...
set "PROJECT_FOLDER=%USERPROFILE%\Desktop\deepseek-ai-coder"
cd /d "%PROJECT_FOLDER%"
call .\venv\Scripts\activate.bat
python desktop_agent.py
pause