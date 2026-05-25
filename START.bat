@echo off
title Professor Outreach System
color 0A
cls

echo.
echo  ============================================
echo   PROFESSOR OUTREACH SYSTEM
echo   Muhammad Sarmad Khan
echo  ============================================
echo.

cd /d "%~dp0"

echo  [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found. Install Python 3.10+
    pause
    exit
)
echo  OK

echo  [2/3] Checking dependencies...
python -c "import flask, groq, crewai, langgraph" >nul 2>&1
if errorlevel 1 (
    echo  Installing dependencies...
    pip install -r requirements.txt -q
)
echo  OK

echo  [3/3] Starting dashboard...
echo.
echo  Dashboard will open at: http://localhost:5000
echo.
echo  ============================================
echo   COMMANDS (open a new terminal to run):
echo.
echo   python main.py discover     ^<-- Find professors
echo   python main.py draft --crew ^<-- Generate emails
echo   python main.py draft        ^<-- LangGraph mode
echo   python main.py send         ^<-- Send approved
echo   python main.py followup     ^<-- Check no-replies
echo   python main.py status       ^<-- View stats
echo  ============================================
echo.

:: Open browser after 2 seconds
start "" timeout /t 2 >nul
start "" "http://localhost:5000"

:: Start dashboard (keeps window open)
python dashboard/app.py

pause
