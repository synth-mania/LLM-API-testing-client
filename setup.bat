@echo off
:: OpenRouter GUI Client Setup Script for Windows
echo Setting up OpenRouter GUI Client...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH. Please install Python and try again.
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment. Please make sure venv module is installed.
        echo You can install it with: pip install virtualenv
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup completed successfully!
echo.
echo To run the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the application: python main.py
echo.
echo You can also run the application directly with: run.bat
echo.

pause
