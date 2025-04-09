"""
GUI theming and styling utilities.
"""

import customtkinter as ctk
from typing import Dict, Any, Tuple, Optional

class AppTheme:
    """Theme management for the application."""
    
    # Color schemes
    DARK = {
        "bg_primary": "#1a1a1a",
        "bg_secondary": "#2d2d2d",
        "fg_primary": "#ffffff",
        "fg_secondary": "#cccccc",
        "accent": "#3a7ebf",
        "accent_hover": "#2b5f8e",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545",
        "border": "#444444",
    }
    
    LIGHT = {
        "bg_primary": "#f5f5f5",
        "bg_secondary": "#e0e0e0",
        "fg_primary": "#000000",
        "fg_secondary": "#555555",
        "accent": "#007bff",
        "accent_hover": "#0056b3",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545",
        "border": "#cccccc",
    }
    
    # Font configurations
    FONTS = {
        "heading": ("Helvetica", 16, "bold"),
        "subheading": ("Helvetica", 14, "bold"),
        "body": ("Helvetica", 12),
        "small": ("Helvetica", 10),
        "monospace": ("Courier", 12),
    }
    
    # Padding and spacing
    PADDING = {
        "small": 5,
        "medium": 10,
        "large": 20,
    }
    
    @classmethod
    def setup_theme(cls, mode: str = "dark") -> None:
        """
        Set up the application theme.
        
        Args:
            mode: Theme mode, either "dark" or "light"
        """
        # Set appearance mode
        ctk.set_appearance_mode(mode)
        
        # Set default color theme
        ctk.set_default_color_theme("blue")
    
    @classmethod
    def get_colors(cls, mode: str = "dark") -> Dict[str, str]:
        """
        Get the color scheme for the specified mode.
        
        Args:
            mode: Theme mode, either "dark" or "light"
            
        Returns:
            Dict[str, str]: Color scheme dictionary
        """
        return cls.DARK if mode.lower() == "dark" else cls.LIGHT
    
    @classmethod
    def apply_widget_styling(cls, widget, widget_type: str, mode: str = "dark") -> None:
        """
        Apply styling to a widget based on its type.
        
        Args:
            widget: The widget to style
            widget_type: Type of widget (e.g., "button", "entry", "frame")
            mode: Theme mode, either "dark" or "light"
        """
        colors = cls.get_colors(mode)
        
        if widget_type == "button":
            widget.configure(
                fg_color=colors["accent"],
                hover_color=colors["accent_hover"],
                text_color=colors["fg_primary"],
                corner_radius=6
            )
        elif widget_type == "entry":
            widget.configure(
                fg_color=colors["bg_secondary"],
                text_color=colors["fg_primary"],
                border_color=colors["border"],
                corner_radius=6
            )
        elif widget_type == "frame":
            widget.configure(
                fg_color=colors["bg_primary"],
                corner_radius=8
            )
        elif widget_type == "label":
            widget.configure(
                text_color=colors["fg_primary"]
            )
        elif widget_type == "textbox":
            widget.configure(
                fg_color=colors["bg_secondary"],
                text_color=colors["fg_primary"],
                border_color=colors["border"],
                corner_radius=6
            )
