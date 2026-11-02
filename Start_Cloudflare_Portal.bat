@echo off
title Telangana Panchayat Raj - Cloudflare Online Gateway
cd /d "%~dp0"
echo ===================================================================
echo   Telangana Panchayat Raj - Automated DSR Portal
echo   Launching Public Cloudflare Tunnel (Hyderabad Edge)
echo ===================================================================
echo.
".venv\Scripts\python.exe" run_cloudflare_portal.py
pause
