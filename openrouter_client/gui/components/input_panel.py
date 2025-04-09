"""
Input panel component for the OpenRouter GUI client.
"""

import customtkinter as ctk
from typing import Callable, Optional

from openrouter_client.gui.utils.theme import AppTheme

class InputPanel(ctk.CTkFrame):
    """Panel for user input and prompt controls."""
    
    def __init__(self, master, send_callback: Callable[[str], None], **kwargs):
        """
        Initialize the input panel.
        
        Args:
            master: Parent widget
            send_callback: Callback function for when the send button is clicked
            **kwargs: Additional keyword arguments for the frame
        """
        super().__init__(master, **kwargs)
        
        # Apply styling
        AppTheme.apply_widget_styling(self, "frame")
        
        # Store callback
        self.send_callback = send_callback
        
        # Create widgets
        self._create_widgets()
        self._setup_layout()
    
    def _create_widgets(self):
        """Create the panel widgets."""
        # Prompt label
        self.prompt_label = ctk.CTkLabel(
            self, 
            text="Enter your prompt:",
            font=AppTheme.FONTS["subheading"]
        )
        AppTheme.apply_widget_styling(self.prompt_label, "label")
        
        # Prompt text area
        self.prompt_text = ctk.CTkTextbox(
            self,
            height=100,
            wrap="word"
        )
        AppTheme.apply_widget_styling(self.prompt_text, "textbox")
        
        # Default prompt checkbox
        self.use_default_var = ctk.BooleanVar(value=False)
        self.use_default_checkbox = ctk.CTkCheckBox(
            self,
            text="Use default prompt",
            variable=self.use_default_var,
            command=self._toggle_default_prompt
        )
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self)
        AppTheme.apply_widget_styling(self.button_frame, "frame")
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command=self._clear_prompt
        )
        AppTheme.apply_widget_styling(self.clear_button, "button")
        
        # Send button
        self.send_button = ctk.CTkButton(
            self.button_frame,
            text="Send",
            command=self._send_prompt
        )
        AppTheme.apply_widget_styling(self.send_button, "button")
    
    def _setup_layout(self):
        """Set up the panel layout."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Place widgets
        self.prompt_label.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=(AppTheme.PADDING["medium"], AppTheme.PADDING["small"]))
        self.prompt_text.grid(row=1, column=0, sticky="nsew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.use_default_checkbox.grid(row=2, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        # Button frame layout
        self.button_frame.grid(row=3, column=0, sticky="e", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["medium"])
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.clear_button.grid(row=0, column=0, padx=AppTheme.PADDING["small"])
        self.send_button.grid(row=0, column=1, padx=AppTheme.PADDING["small"])
    
    def _send_prompt(self):
        """Send the current prompt."""
        prompt = self.get_prompt()
        if prompt:
            self.send_callback(prompt)
    
    def _clear_prompt(self):
        """Clear the prompt text area."""
        self.prompt_text.delete("0.0", "end")
    
    def _toggle_default_prompt(self):
        """Toggle between default prompt and custom prompt."""
        if self.use_default_var.get():
            self.prompt_text.configure(state="disabled")
        else:
            self.prompt_text.configure(state="normal")
    
    def get_prompt(self) -> str:
        """
        Get the current prompt text.
        
        Returns:
            str: The prompt text
        """
        if self.use_default_var.get():
            # Return None to signal using the default prompt
            return None
        
        return self.prompt_text.get("0.0", "end").strip()
    
    def set_prompt(self, prompt: str):
        """
        Set the prompt text.
        
        Args:
            prompt: The prompt text to set
        """
        self.prompt_text.delete("0.0", "end")
        self.prompt_text.insert("0.0", prompt)
