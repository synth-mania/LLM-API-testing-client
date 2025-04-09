"""
Configuration settings for the OpenRouter API client.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

class Config:
    """Configuration settings for the OpenRouter API client."""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        # API Configuration
        "api_key": "",
        "api_endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "model": "openai/o1-pro",
        
        # Request Configuration
        "max_tokens": 0,  # 0 means no limit
        "request_delay_seconds": 1,
        "refractory_seconds": 300,  # 5 minutes
        "request_timeout": 30,  # seconds
        
        # Cost Tracking
        "input_price_per_million": 150,  # $150 per million tokens
        "output_price_per_million": 600,  # $600 per million tokens
        
        # HTTP Headers
        "http_referer": "https://llm-api-testing-client.github.io",
        "x_title": "LLM API Testing Client",
        
        # System prompt
        "system_prompt": "You are a helpful assistant.",
        
        # Default user prompt
        "default_user_prompt": "Write an essay on why API keys should be kept private."
    }
    
    def __init__(self):
        """Initialize configuration with default values."""
        self._config = self.DEFAULT_CONFIG.copy()
        self._config_file = self._get_config_file_path()
        self.load_config()
    
    def _get_config_file_path(self) -> Path:
        """Get the path to the configuration file."""
        # Use user's home directory for configuration
        config_dir = Path.home() / ".openrouter_client"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.json"
    
    def load_config(self) -> None:
        """Load configuration from file if it exists."""
        if self._config_file.exists():
            try:
                with open(self._config_file, "r") as f:
                    loaded_config = json.load(f)
                    # Update only keys that exist in DEFAULT_CONFIG
                    for key in self.DEFAULT_CONFIG:
                        if key in loaded_config:
                            self._config[key] = loaded_config[key]
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading configuration: {e}")
    
    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self._config_file, "w") as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            print(f"Error saving configuration: {e}")
    
    def get(self, key: str) -> Any:
        """Get a configuration value."""
        return self._config.get(key, self.DEFAULT_CONFIG.get(key))
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        if key in self.DEFAULT_CONFIG:
            self._config[key] = value
    
    def get_headers(self) -> Dict[str, str]:
        """Return the HTTP headers for API requests."""
        return {
            "Authorization": f"Bearer {self.get('api_key')}",
            "HTTP-Referer": self.get('http_referer'),
            "X-Title": self.get('x_title'),
            "Content-Type": "application/json"
        }
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save_config()


# Create a singleton instance
config = Config()
