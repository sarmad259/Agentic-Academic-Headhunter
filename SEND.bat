@echo off
title Send Approved Emails
color 0C
cd /d "%~dp0"
echo.
echo  Sending approved emails via Gmail SMTP...
echo  (Only emails in /approved folder will be sent)
echo.
python main.py send
pause
