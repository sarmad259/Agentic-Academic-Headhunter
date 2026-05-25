@echo off
title Discover Professors
color 0B
cd /d "%~dp0"
echo.
echo  ============================================
echo   PROFESSOR DISCOVERY
echo   Scanning 216 universities x 10 research areas
echo   Includes rank 1-50 AND rank 100-300 universities
echo  ============================================
echo.
echo  Previous results saved as:
echo    targets_top50.json  (top-50 unis run)
echo.
echo  This run will scan mid-tier unis (rank 100-300)
echo  and MERGE results with existing targets.json
echo.
echo  Estimated time: 2-3 hours
echo  Leave this window open overnight.
echo.
python main.py discover
echo.
echo  Done! Check targets.json for results.
pause
