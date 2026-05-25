@echo off
title Generate Email Drafts
color 0E
cd /d "%~dp0"
echo.
echo  Select draft mode:
echo  [1] CrewAI - Best quality, self-correcting agents
echo  [2] LangGraph - DeepSeek/Groq pipeline
echo  [3] Groq - Fastest
echo.
set /p choice="Enter 1, 2, or 3: "

if "%choice%"=="1" (
    echo  Running CrewAI pipeline...
    python main.py draft --crew
) else if "%choice%"=="2" (
    echo  Running LangGraph pipeline...
    python main.py draft
) else if "%choice%"=="3" (
    echo  Running Groq direct...
    python main.py draft --groq
) else (
    echo  Invalid choice. Running Groq...
    python main.py draft --groq
)

echo.
echo  Drafts saved to /drafts folder.
echo  Review them, then move approved ones to /approved
pause
