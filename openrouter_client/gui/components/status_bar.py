"""
Status bar component for the OpenRouter GUI client.
"""

import customtkinter as ctk
from typing import Dict, Any
import time

from openrouter_client.gui.utils.theme import AppTheme
from openrouter_client.utils.token_tracker import TokenUsage

class StatusBar(ctk.CTkFrame):
    """Status bar for displaying application status and metrics."""
    
    def __init__(self, master, token_usage: TokenUsage, **kwargs):
        """
        Initialize the status bar.
        
        Args:
            master: Parent widget
            token_usage: TokenUsage instance for tracking token usage
            **kwargs: Additional keyword arguments for the frame
        """
        super().__init__(master, height=30, **kwargs)
        
        # Apply styling
        AppTheme.apply_widget_styling(self, "frame")
        
        # Store token usage reference
        self.token_usage = token_usage
        
        # Status variables
        self.status_text = "Ready"
        self.status_time = time.time()
        
        # Create widgets
        self._create_widgets()
        self._setup_layout()
        
        # Start update timer
        self._start_update_timer()
    
    def _create_widgets(self):
        """Create the status bar widgets."""
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Ready",
            font=AppTheme.FONTS["small"]
        )
        AppTheme.apply_widget_styling(self.status_label, "label")
        
        # Token usage label
        self.token_label = ctk.CTkLabel(
            self,
            text="Tokens: 0 in, 0 out",
            font=AppTheme.FONTS["small"]
        )
        AppTheme.apply_widget_styling(self.token_label, "label")
        
        # Cost label
        self.cost_label = ctk.CTkLabel(
            self,
            text="Cost: $0.00",
            font=AppTheme.FONTS["small"]
        )
        AppTheme.apply_widget_styling(self.cost_label, "label")
    
    def _setup_layout(self):
        """Set up the status bar layout."""
        # Configure grid
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # Place widgets
        self.status_label.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.token_label.grid(row=0, column=1, sticky="e", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.cost_label.grid(row=0, column=2, sticky="e", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
    
    def _start_update_timer(self):
        """Start the timer for updating the status bar."""
        self._update_status_bar()
        self.after(1000, self._start_update_timer)
    
    def _update_status_bar(self):
        """Update the status bar with current information."""
        # Update token usage
        self.token_label.configure(
            text=f"Tokens: {self.token_usage.input_tokens} in, {self.token_usage.output_tokens} out"
        )
        
        # Update cost
        self.cost_label.configure(
            text=f"Cost: ${self.token_usage.calculate_cost():.2f}"
        )
        
        # Clear status after 5 seconds
        if time.time() - self.status_time > 5 and self.status_text != "Ready":
            self.set_status("Ready")
    
    def set_status(self, status: str):
        """
        Set the status text.
        
        Args:
            status: The status text to display
        """
        self.status_text = status
        self.status_time = time.time()
        self.status_label.configure(text=f"Status: {status}")
