@echo off
title EPTS Portal Automated DSR Generator
cd /d "%~dp0\.."
echo ========================================================
echo  e-Panchayat Telangana (EPTS) Automated DSR Downloader
echo  All data and reports are saved in automate_epts\
echo ========================================================
echo.

".venv\Scripts\python.exe" "automate_epts\dsr_auto_download.py"

echo.
pause
