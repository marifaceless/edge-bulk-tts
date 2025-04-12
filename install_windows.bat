@echo off
echo ===============================================
echo Edge Bulk TTS - Easy Installer
echo ===============================================

cd /d "%~dp0"

echo Checking for Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    start https://www.python.org/downloads/
    echo Press any key to exit...
    pause > nul
    exit /b 1
)
echo [OK] Python is installed

echo Setting up virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install requirements
    echo Press any key to exit...
    pause > nul
    exit /b 1
)
echo [OK] All packages installed

echo.
echo ===============================================
echo Installation complete! Starting the app...
echo ===============================================
echo.
echo The app will open in your web browser shortly.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.

streamlit run edge_bulk.py

echo.
echo Application has been closed.
echo Press any key to exit...
pause > nul 