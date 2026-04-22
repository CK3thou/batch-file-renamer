@echo off
REM Batch File Renamer - Desktop Launcher
REM This script starts the Flask web application and opens it in your default browser

echo.
echo ========================================
echo  Batch File Renamer - Web Interface
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python and try again.
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install -r requirements.txt
)

REM Start the Flask app
echo Starting Flask application...
echo.
echo The app will open in your browser at http://localhost:5000
echo Press Ctrl+C to stop the server.
echo.

start http://localhost:5000
python app.py

pause
