#!/bin/bash

# OpenRouter GUI Client Run Script for Linux/macOS
echo "Starting OpenRouter GUI Client..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py

# Deactivate virtual environment on exit
deactivate
