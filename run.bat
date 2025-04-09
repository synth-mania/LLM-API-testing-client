@echo off
:: OpenRouter GUI Client Run Script for Windows
echo Starting OpenRouter GUI Client...

:: Check if virtual environment exists
if not exist venv (
    echo Error: Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the application
python main.py

:: Deactivate virtual environment on exit
deactivate
