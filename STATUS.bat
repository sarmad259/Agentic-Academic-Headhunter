@echo off
title Outreach Status
color 0D
cd /d "%~dp0"
echo.
python main.py status
echo.
python main.py followup
pause
