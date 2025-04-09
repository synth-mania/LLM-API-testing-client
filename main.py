#!/usr/bin/env python3
"""
OpenRouter GUI Client

Main entry point for the OpenRouter GUI application.
"""

import sys
import os
from openrouter_client.gui.app import App

def main():
    """Initialize and run the application."""
    app = App()
    app.run()

if __name__ == "__main__":
    main()
