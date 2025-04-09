"""
Response panel component for the OpenRouter GUI client.
"""

import customtkinter as ctk
from typing import Callable, Optional, Dict, Any
import tkinter as tk

from openrouter_client.gui.utils.theme import AppTheme

class ResponsePanel(ctk.CTkFrame):
    """Panel for displaying API responses."""
    
    def __init__(self, master, **kwargs):
        """
        Initialize the response panel.
        
        Args:
            master: Parent widget
            **kwargs: Additional keyword arguments for the frame
        """
        super().__init__(master, **kwargs)
        
        # Apply styling
        AppTheme.apply_widget_styling(self, "frame")
        
        # Create widgets
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create the panel widgets."""
        # Response label
        self.response_label = ctk.CTkLabel(
            self, 
            text="Response:",
            font=AppTheme.FONTS["subheading"]
        )
        AppTheme.apply_widget_styling(self.response_label, "label")
        
        # Response text area
        self.response_text = ctk.CTkTextbox(
            self,
            height=200,
            wrap="word"
        )
        self.response_text.configure(state="disabled")
        AppTheme.apply_widget_styling(self.response_text, "textbox")
        
        # Metadata frame
        self.metadata_frame = ctk.CTkFrame(self)
        AppTheme.apply_widget_styling(self.metadata_frame, "frame")
        
        # Metadata label
        self.metadata_label = ctk.CTkLabel(
            self.metadata_frame,
            text="Metadata:",
            font=AppTheme.FONTS["small"]
        )
        AppTheme.apply_widget_styling(self.metadata_label, "label")
        
        # Metadata text
        self.metadata_text = ctk.CTkTextbox(
            self.metadata_frame,
            height=60,
            font=AppTheme.FONTS["small"]
        )
        self.metadata_text.configure(state="disabled")
        AppTheme.apply_widget_styling(self.metadata_text, "textbox")
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self)
        AppTheme.apply_widget_styling(self.button_frame, "frame")
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self._clear_response
        )
        AppTheme.apply_widget_styling(self.clear_button, "button")
        
        # Copy button
        self.copy_button = ctk.CTkButton(
            self.button_frame,
            text="Copy",
            command=self._copy_response
        )
        AppTheme.apply_widget_styling(self.copy_button, "button")
    
    def _setup_layout(self):
        """Set up the panel layout."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Place widgets
        self.response_label.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=(AppTheme.PADDING["medium"], AppTheme.PADDING["small"]))
        self.response_text.grid(row=1, column=0, sticky="nsew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        # Metadata frame layout
        self.metadata_frame.grid(row=2, column=0, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.metadata_frame.grid_columnconfigure(0, weight=1)
        
        self.metadata_label.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["small"], pady=(AppTheme.PADDING["small"], 0))
        self.metadata_text.grid(row=1, column=0, sticky="ew", padx=AppTheme.PADDING["small"], pady=AppTheme.PADDING["small"])
        
        # Button frame layout
        self.button_frame.grid(row=3, column=0, sticky="e", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["medium"])
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.clear_button.grid(row=0, column=0, padx=AppTheme.PADDING["small"])
        self.copy_button.grid(row=0, column=1, padx=AppTheme.PADDING["small"])
    
    def _clear_response(self):
        """Clear the response text area."""
        self.response_text.configure(state="normal")
        self.response_text.delete("0.0", "end")
        self.response_text.configure(state="disabled")
        
        self.metadata_text.configure(state="normal")
        self.metadata_text.delete("0.0", "end")
        self.metadata_text.configure(state="disabled")
    
    def _copy_response(self):
        """Copy the response text to clipboard."""
        text = self.response_text.get("0.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
    
    def set_response(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Set the response content and metadata.
        
        Args:
            content: The response content
            metadata: Optional response metadata
        """
        # Update response text
        self.response_text.configure(state="normal")
        self.response_text.delete("0.0", "end")
        self.response_text.insert("0.0", content)
        self.response_text.configure(state="disabled")
        
        # Update metadata text if provided
        if metadata:
            metadata_str = ""
            if "model" in metadata:
                metadata_str += f"Model: {metadata['model']}\n"
            
            if "usage" in metadata:
                usage = metadata["usage"]
                metadata_str += f"Tokens: {usage.get('prompt_tokens', 0)} in, {usage.get('completion_tokens', 0)} out\n"
            
            if "created" in metadata:
                metadata_str += f"Created: {metadata['created']}\n"
            
            if "id" in metadata:
                metadata_str += f"ID: {metadata['id']}"
            
            self.metadata_text.configure(state="normal")
            self.metadata_text.delete("0.0", "end")
            self.metadata_text.insert("0.0", metadata_str)
            self.metadata_text.configure(state="disabled")
    
    def set_error(self, error_message: str):
        """
        Set an error message in the response area.
        
        Args:
            error_message: The error message to display
        """
        self.response_text.configure(state="normal")
        self.response_text.delete("0.0", "end")
        self.response_text.insert("0.0", f"ERROR: {error_message}")
        self.response_text.configure(state="disabled")
        
        # Clear metadata
        self.metadata_text.configure(state="normal")
        self.metadata_text.delete("0.0", "end")
        self.metadata_text.configure(state="disabled")
