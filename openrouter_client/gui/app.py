"""
Main application window for the OpenRouter GUI client.
"""

import customtkinter as ctk
import tkinter as tk
from typing import Dict, Any, Optional
import threading
import time

from openrouter_client.config.settings import config
from openrouter_client.api.client import ApiClient
from openrouter_client.utils.token_tracker import TokenUsage
from openrouter_client.gui.utils.theme import AppTheme
from openrouter_client.gui.components.input_panel import InputPanel
from openrouter_client.gui.components.response_panel import ResponsePanel
from openrouter_client.gui.components.status_bar import StatusBar

class SettingsDialog(ctk.CTkToplevel):
    """Dialog for configuring application settings."""
    
    def __init__(self, parent, **kwargs):
        """
        Initialize the settings dialog.
        
        Args:
            parent: Parent widget
            **kwargs: Additional keyword arguments for the toplevel window
        """
        super().__init__(parent, **kwargs)
        
        self.title("Settings")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Apply styling
        AppTheme.apply_widget_styling(self, "frame")
        
        # Create widgets
        self._create_widgets()
        self._setup_layout()
        
        # Load current settings
        self._load_settings()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        self.focus_set()
    
    def _create_widgets(self):
        """Create the dialog widgets."""
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="OpenRouter API Settings",
            font=AppTheme.FONTS["heading"]
        )
        AppTheme.apply_widget_styling(self.title_label, "label")
        
        # Create notebook for settings categories
        self.notebook = ctk.CTkTabview(self)
        
        # API Settings tab
        self.api_tab = self.notebook.add("API Settings")
        self.api_tab.grid_columnconfigure(1, weight=1)
        
        # API Key
        self.api_key_label = ctk.CTkLabel(
            self.api_tab,
            text="API Key:",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.api_key_label, "label")
        
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ctk.CTkEntry(
            self.api_tab,
            textvariable=self.api_key_var,
            width=300,
            show="*"
        )
        AppTheme.apply_widget_styling(self.api_key_entry, "entry")
        
        self.show_key_var = tk.BooleanVar(value=False)
        self.show_key_checkbox = ctk.CTkCheckBox(
            self.api_tab,
            text="Show Key",
            variable=self.show_key_var,
            command=self._toggle_key_visibility
        )
        
        # API Endpoint
        self.endpoint_label = ctk.CTkLabel(
            self.api_tab,
            text="API Endpoint:",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.endpoint_label, "label")
        
        self.endpoint_var = tk.StringVar()
        self.endpoint_entry = ctk.CTkEntry(
            self.api_tab,
            textvariable=self.endpoint_var,
            width=300
        )
        AppTheme.apply_widget_styling(self.endpoint_entry, "entry")
        
        # Model
        self.model_label = ctk.CTkLabel(
            self.api_tab,
            text="Model:",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.model_label, "label")
        
        self.model_var = tk.StringVar()
        self.model_entry = ctk.CTkEntry(
            self.api_tab,
            textvariable=self.model_var,
            width=300
        )
        AppTheme.apply_widget_styling(self.model_entry, "entry")
        
        # Request Settings tab
        self.request_tab = self.notebook.add("Request Settings")
        self.request_tab.grid_columnconfigure(1, weight=1)
        
        # Max Tokens
        self.max_tokens_label = ctk.CTkLabel(
            self.request_tab,
            text="Max Tokens:",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.max_tokens_label, "label")
        
        self.max_tokens_var = tk.IntVar()
        self.max_tokens_entry = ctk.CTkEntry(
            self.request_tab,
            textvariable=self.max_tokens_var,
            width=100
        )
        AppTheme.apply_widget_styling(self.max_tokens_entry, "entry")
        
        # Request Delay
        self.delay_label = ctk.CTkLabel(
            self.request_tab,
            text="Request Delay (seconds):",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.delay_label, "label")
        
        self.delay_var = tk.DoubleVar()
        self.delay_entry = ctk.CTkEntry(
            self.request_tab,
            textvariable=self.delay_var,
            width=100
        )
        AppTheme.apply_widget_styling(self.delay_entry, "entry")
        
        # System Prompt
        self.system_prompt_label = ctk.CTkLabel(
            self.request_tab,
            text="System Prompt:",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.system_prompt_label, "label")
        
        self.system_prompt_text = ctk.CTkTextbox(
            self.request_tab,
            height=100,
            width=300
        )
        AppTheme.apply_widget_styling(self.system_prompt_text, "textbox")
        
        # Default User Prompt
        self.default_prompt_label = ctk.CTkLabel(
            self.request_tab,
            text="Default User Prompt:",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.default_prompt_label, "label")
        
        self.default_prompt_text = ctk.CTkTextbox(
            self.request_tab,
            height=100,
            width=300
        )
        AppTheme.apply_widget_styling(self.default_prompt_text, "textbox")
        
        # Cost Settings tab
        self.cost_tab = self.notebook.add("Cost Settings")
        self.cost_tab.grid_columnconfigure(1, weight=1)
        
        # Input Price
        self.input_price_label = ctk.CTkLabel(
            self.cost_tab,
            text="Input Price (per million tokens):",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.input_price_label, "label")
        
        self.input_price_var = tk.DoubleVar()
        self.input_price_entry = ctk.CTkEntry(
            self.cost_tab,
            textvariable=self.input_price_var,
            width=100
        )
        AppTheme.apply_widget_styling(self.input_price_entry, "entry")
        
        # Output Price
        self.output_price_label = ctk.CTkLabel(
            self.cost_tab,
            text="Output Price (per million tokens):",
            font=AppTheme.FONTS["body"]
        )
        AppTheme.apply_widget_styling(self.output_price_label, "label")
        
        self.output_price_var = tk.DoubleVar()
        self.output_price_entry = ctk.CTkEntry(
            self.cost_tab,
            textvariable=self.output_price_var,
            width=100
        )
        AppTheme.apply_widget_styling(self.output_price_entry, "entry")
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self)
        AppTheme.apply_widget_styling(self.button_frame, "frame")
        
        # Save button
        self.save_button = ctk.CTkButton(
            self.button_frame,
            text="Save",
            command=self._save_settings
        )
        AppTheme.apply_widget_styling(self.save_button, "button")
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy
        )
        AppTheme.apply_widget_styling(self.cancel_button, "button")
        
        # Reset button
        self.reset_button = ctk.CTkButton(
            self.button_frame,
            text="Reset to Defaults",
            command=self._reset_settings
        )
        AppTheme.apply_widget_styling(self.reset_button, "button")
    
    def _setup_layout(self):
        """Set up the dialog layout."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Place widgets
        self.title_label.grid(row=0, column=0, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["medium"])
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        # API Settings tab layout
        self.api_key_label.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.api_key_entry.grid(row=0, column=1, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.show_key_checkbox.grid(row=1, column=1, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        self.endpoint_label.grid(row=2, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.endpoint_entry.grid(row=2, column=1, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        self.model_label.grid(row=3, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.model_entry.grid(row=3, column=1, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        # Request Settings tab layout
        self.max_tokens_label.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.max_tokens_entry.grid(row=0, column=1, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        self.delay_label.grid(row=1, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.delay_entry.grid(row=1, column=1, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        self.system_prompt_label.grid(row=2, column=0, sticky="nw", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.system_prompt_text.grid(row=2, column=1, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        self.default_prompt_label.grid(row=3, column=0, sticky="nw", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.default_prompt_text.grid(row=3, column=1, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        # Cost Settings tab layout
        self.input_price_label.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.input_price_entry.grid(row=0, column=1, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        self.output_price_label.grid(row=1, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.output_price_entry.grid(row=1, column=1, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        # Button frame layout
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["medium"])
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.save_button.grid(row=0, column=0, padx=AppTheme.PADDING["small"])
        self.cancel_button.grid(row=0, column=1, padx=AppTheme.PADDING["small"])
        self.reset_button.grid(row=0, column=2, padx=AppTheme.PADDING["small"])
    
    def _toggle_key_visibility(self):
        """Toggle the visibility of the API key."""
        if self.show_key_var.get():
            self.api_key_entry.configure(show="")
        else:
            self.api_key_entry.configure(show="*")
    
    def _load_settings(self):
        """Load current settings into the dialog."""
        # API Settings
        self.api_key_var.set(config.get("api_key"))
        self.endpoint_var.set(config.get("api_endpoint"))
        self.model_var.set(config.get("model"))
        
        # Request Settings
        self.max_tokens_var.set(config.get("max_tokens"))
        self.delay_var.set(config.get("request_delay_seconds"))
        
        self.system_prompt_text.delete("0.0", "end")
        self.system_prompt_text.insert("0.0", config.get("system_prompt"))
        
        self.default_prompt_text.delete("0.0", "end")
        self.default_prompt_text.insert("0.0", config.get("default_user_prompt"))
        
        # Cost Settings
        self.input_price_var.set(config.get("input_price_per_million"))
        self.output_price_var.set(config.get("output_price_per_million"))
    
    def _save_settings(self):
        """Save settings and close the dialog."""
        # API Settings
        config.set("api_key", self.api_key_var.get())
        config.set("api_endpoint", self.endpoint_var.get())
        config.set("model", self.model_var.get())
        
        # Request Settings
        config.set("max_tokens", self.max_tokens_var.get())
        config.set("request_delay_seconds", self.delay_var.get())
        
        config.set("system_prompt", self.system_prompt_text.get("0.0", "end").strip())
        config.set("default_user_prompt", self.default_prompt_text.get("0.0", "end").strip())
        
        # Cost Settings
        config.set("input_price_per_million", self.input_price_var.get())
        config.set("output_price_per_million", self.output_price_var.get())
        
        # Save to file
        config.save_config()
        
        # Close dialog
        self.destroy()
    
    def _reset_settings(self):
        """Reset settings to defaults."""
        if tk.messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            config.reset_to_defaults()
            self._load_settings()


class App:
    """Main application window."""
    
    def __init__(self):
        """Initialize the application."""
        # Set up theme
        AppTheme.setup_theme("dark")
        
        # Create token usage tracker
        self.token_usage = TokenUsage()
        
        # Create API client
        self.api_client = ApiClient(
            token_usage=self.token_usage,
            status_callback=self._update_status
        )
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("OpenRouter GUI Client")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Create menu
        self._create_menu()
        
        # Create widgets
        self._create_widgets()
        self._setup_layout()
    
    def _create_menu(self):
        """Create the application menu."""
        # Create menu bar
        self.menu = tk.Menu(self.root)
        self.root.configure(menu=self.menu)
        
        # File menu
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Settings", command=self._open_settings)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create the application widgets."""
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        AppTheme.apply_widget_styling(self.main_frame, "frame")
        
        # Create panels
        self.input_panel = InputPanel(
            self.main_frame,
            send_callback=self._handle_send
        )
        
        self.response_panel = ResponsePanel(
            self.main_frame
        )
        
        # Control frame
        self.control_frame = ctk.CTkFrame(self.main_frame)
        AppTheme.apply_widget_styling(self.control_frame, "frame")
        
        # Continuous mode checkbox
        self.continuous_var = ctk.BooleanVar(value=False)
        self.continuous_checkbox = ctk.CTkCheckBox(
            self.control_frame,
            text="Continuous Mode",
            variable=self.continuous_var,
            command=self._toggle_continuous_mode
        )
        
        # Start/Stop button
        self.start_stop_button = ctk.CTkButton(
            self.control_frame,
            text="Start",
            command=self._toggle_continuous_requests,
            state="disabled"
        )
        AppTheme.apply_widget_styling(self.start_stop_button, "button")
        
        # Status bar
        self.status_bar = StatusBar(
            self.root,
            token_usage=self.token_usage
        )
    
    def _setup_layout(self):
        """Set up the application layout."""
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Place main frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Place panels
        self.input_panel.grid(row=0, column=0, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["medium"])
        self.response_panel.grid(row=1, column=0, sticky="nsew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["medium"])
        
        # Control frame layout
        self.control_frame.grid(row=2, column=0, sticky="ew", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["medium"])
        self.control_frame.grid_columnconfigure(1, weight=1)
        
        self.continuous_checkbox.grid(row=0, column=0, sticky="w", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        self.start_stop_button.grid(row=0, column=1, sticky="e", padx=AppTheme.PADDING["medium"], pady=AppTheme.PADDING["small"])
        
        # Place status bar
        self.status_bar.grid(row=1, column=0, sticky="ew", padx=0, pady=0)
    
    def _open_settings(self):
        """Open the settings dialog."""
        SettingsDialog(self.root)
    
    def _show_about(self):
        """Show the about dialog."""
        tk.messagebox.showinfo(
            "About",
            "OpenRouter GUI Client\n\n"
            "A graphical user interface for interacting with the OpenRouter API.\n\n"
            "WARNING: This application is provided for EDUCATIONAL PURPOSES ONLY.\n"
            "Using API keys that you found exposed is unethical and potentially illegal."
        )
    
    def _update_status(self, status: str):
        """
        Update the status bar.
        
        Args:
            status: The status text to display
        """
        if self.status_bar:
            self.status_bar.set_status(status)
    
    def _handle_send(self, prompt: str):
        """
        Handle sending a prompt to the API.
        
        Args:
            prompt: The prompt to send
        """
        # Use default prompt if None
        if prompt is None:
            prompt = config.get("default_user_prompt")
        
        # Check if prompt is empty
        if not prompt.strip():
            self._update_status("Error: Prompt cannot be empty")
            return
        
        # Check if API key is set
        if not config.get("api_key"):
            self._update_status("Error: API key not set")
            tk.messagebox.showerror("Error", "API key not set. Please configure in Settings.")
            return
        
        # Disable send button during request
        self.input_panel.send_button.configure(state="disabled")
        
        # Update status
        self._update_status("Sending request...")
        
        # Make request in a separate thread
        threading.Thread(
            target=self._make_request,
            args=(prompt,),
            daemon=True
        ).start()
    
    def _make_request(self, prompt: str):
        """
        Make an API request in a background thread.
        
        Args:
            prompt: The prompt to send
        """
        # Make the request
        success, content, metadata = self.api_client.make_api_request(prompt)
        
        # Update UI in main thread
        self.root.after(0, lambda: self._handle_response(success, content, metadata))
    
    def _handle_response(self, success: bool, content: Optional[str], metadata: Optional[Dict[str, Any]]):
        """
        Handle the API response.
        
        Args:
            success: Whether the request was successful
            content: The response content
            metadata: The response metadata
        """
        if success:
            self.response_panel.set_response(content, metadata)
            self._update_status("Response received")
        else:
            self.response_panel.set_error(content or "Unknown error")
            self._update_status("Error: Request failed")
        
        # Re-enable send button
        self.input_panel.send_button.configure(state="normal")
    
    def _toggle_continuous_mode(self):
        """Toggle continuous mode."""
        if self.continuous_var.get():
            self.start_stop_button.configure(state="normal")
        else:
            self.start_stop_button.configure(state="disabled")
            if self.api_client.is_running:
                self._stop_continuous_requests()
    
    def _toggle_continuous_requests(self):
        """Toggle continuous API requests."""
        if self.api_client.is_running:
            self._stop_continuous_requests()
        else:
            self._start_continuous_requests()
    
    def _start_continuous_requests(self):
        """Start continuous API requests."""
        # Get prompt
        prompt = self.input_panel.get_prompt()
        if prompt is None:
            prompt = config.get("default_user_prompt")
        
        # Check if prompt is empty
        if not prompt.strip():
            self._update_status("Error: Prompt cannot be empty")
            return
        
        # Check if API key is set
        if not config.get("api_key"):
            self._update_status("Error: API key not set")
            tk.messagebox.showerror("Error", "API key not set. Please configure in Settings.")
            return
        
        # Update UI
        self.start_stop_button.configure(text="Stop")
        self.input_panel.send_button.configure(state="disabled")
        
        # Start continuous requests
        self.api_client.start_continuous_requests(prompt, self._handle_response)
    
    def _stop_continuous_requests(self):
        """Stop continuous API requests."""
        # Update UI
        self.start_stop_button.configure(text="Start")
        self.input_panel.send_button.configure(state="normal")
        
        # Stop continuous requests
        self.api_client.stop_continuous_requests()
    
    def run(self):
        """Run the application."""
        self.root.mainloop()
