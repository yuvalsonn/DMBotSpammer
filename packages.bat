@echo off
title Installing Required Python Libraries
color 0a

echo ================================================
echo      Setup for DMBotSpammer
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo python isn't downloaded
    pause
    exit /b
)

echo installing requirements
echo.

REM Install all dependencies
pip install asyncio
pip install discord.py
pip install pystyle

echo.
echo finished.
echo.
pause
