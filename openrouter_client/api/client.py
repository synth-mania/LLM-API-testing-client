"""
OpenRouter API client implementation.
"""

import requests
import json
import time
import logging
from typing import Dict, Any, Tuple, Optional, Callable

from openrouter_client.config.settings import config
from openrouter_client.utils.token_tracker import TokenUsage

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("api_client")

class ApiClient:
    """Client for interacting with the OpenRouter API."""
    
    def __init__(self, token_usage: TokenUsage = None, status_callback: Callable[[str], None] = None):
        """
        Initialize the API client.
        
        Args:
            token_usage: TokenUsage instance for tracking token usage
            status_callback: Callback function for status updates
        """
        self.token_usage = token_usage or TokenUsage()
        self.status_callback = status_callback or (lambda x: None)
        self.is_running = False
        self.should_stop = False
    
    def _update_status(self, status: str) -> None:
        """Update status via callback."""
        if self.status_callback:
            self.status_callback(status)
        logger.info(status)
    
    def make_api_request(self, prompt: str) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Make a single call to the OpenRouter API.
        
        Args:
            prompt: The user prompt to send to the API
            
        Returns:
            Tuple containing:
            - bool: True if the request was successful, False otherwise
            - Optional[str]: The response content if successful, None otherwise
            - Optional[Dict[str, Any]]: Response metadata if successful, None otherwise
        """
        # Prepare the request payload
        payload = {
            "model": config.get("model"),
            "messages": [
                {"role": "system", "content": config.get("system_prompt")},
                {"role": "user", "content": prompt}
            ]
        }
        
        # Add max_tokens if configured
        max_tokens = config.get("max_tokens")
        if max_tokens > 0:
            payload["max_tokens"] = max_tokens
        
        self._update_status(f"Sending request to {config.get('model')}...")
        
        try:
            # Make the API request
            response = requests.post(
                config.get("api_endpoint"),
                headers=config.get_headers(),
                json=payload,
                timeout=config.get("request_timeout")
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse the response
            response_data = response.json()
            
            # Process successful response
            return self._handle_successful_response(response_data)
            
        except requests.exceptions.RequestException as e:
            return self._handle_request_exception(e)
        except json.JSONDecodeError:
            self._update_status("Failed to decode JSON response.")
            if 'response' in locals():
                logger.error(f"Raw response: {response.text}")
            return False, None, None
        except Exception as e:
            self._update_status(f"An unexpected error occurred: {e}")
            logger.exception("Unexpected error")
            return False, None, None
    
    def _handle_successful_response(self, response_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Process a successful API response.
        
        Args:
            response_data: The JSON response from the API
            
        Returns:
            Tuple containing:
            - bool: True if processing was successful
            - Optional[str]: The response content
            - Optional[Dict[str, Any]]: Response metadata
        """
        # Extract the response content
        if response_data.get("choices") and len(response_data["choices"]) > 0:
            message = response_data["choices"][0].get("message", {})
            content = message.get("content", "No content found in response.")
            usage = response_data.get("usage", {})
            
            self._update_status("Response received successfully.")
            
            # Update token usage
            self.token_usage.update(
                usage.get("prompt_tokens", 0),
                usage.get("completion_tokens", 0)
            )
            
            # Prepare metadata
            metadata = {
                "model": response_data.get("model", "unknown"),
                "usage": usage,
                "created": response_data.get("created", 0),
                "id": response_data.get("id", "")
            }
            
            return True, content, metadata
        else:
            self._update_status("Unexpected response format.")
            logger.error(f"Response data: {json.dumps(response_data, indent=2)}")
            
            # Handle specific error messages
            if "error" in response_data:
                err_message = response_data["error"].get("message", "")
                logger.error(f"API error: {err_message}")
                
                # Check for token limit errors
                if "afford" in err_message:
                    words = err_message.split()
                    for i, word in enumerate(words):
                        if word == "afford" and i + 1 < len(words):
                            try:
                                new_max_tokens = int(words[i+1].rstrip('.,:;'))
                                self._update_status(f"Updated max_tokens to {new_max_tokens}")
                                config.set("max_tokens", new_max_tokens)
                                config.save_config()
                            except (ValueError, IndexError):
                                pass
            
            return False, None, None
    
    def _handle_request_exception(self, e: requests.exceptions.RequestException) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Handle request exceptions.
        
        Args:
            e: The request exception
            
        Returns:
            Tuple containing:
            - bool: Always False as this handles errors
            - Optional[str]: Always None
            - Optional[Dict[str, Any]]: Always None
        """
        self._update_status(f"Request failed: {e}")
        
        # Check for specific error responses
        if hasattr(e, 'response') and e.response is not None:
            status_code = e.response.status_code
            logger.error(f"Status Code: {status_code}")
            logger.error(f"Response Body: {e.response.text}")
            
            # Handle payment required error
            if status_code == 402:
                refractory_seconds = config.get("refractory_seconds")
                self._update_status(f"API credits exhausted. Waiting {refractory_seconds / 60} minutes before trying again")
                self._update_status(f"Inflicted damage: ${round(self.token_usage.calculate_cost(), 2)}")
                config.set("max_tokens", 0)
                config.save_config()
                
                # In GUI we don't want to block, so we'll just report this
                return False, f"API credits exhausted (402). Please wait or try with a different API key.", None
            
            # Handle authentication errors
            if status_code in [401, 403]:
                self._update_status("Authentication/Authorization failed. The API key may be invalid or revoked.")
                return False, "Authentication failed. Please check your API key.", None
        
        return False, f"Request error: {str(e)}", None
    
    def start_continuous_requests(self, prompt: str, callback: Callable[[bool, Optional[str], Optional[Dict[str, Any]]], None]) -> None:
        """
        Start making continuous API requests.
        
        Args:
            prompt: The prompt to send
            callback: Function to call with results
        """
        if self.is_running:
            return
        
        self.is_running = True
        self.should_stop = False
        
        import threading
        
        def run_requests():
            call_count = 0
            while not self.should_stop:
                call_count += 1
                self._update_status(f"Making call #{call_count}")
                
                success, content, metadata = self.make_api_request(prompt)
                callback(success, content, metadata)
                
                if self.should_stop:
                    break
                
                # Wait before next request
                delay = config.get("request_delay_seconds")
                self._update_status(f"Waiting for {delay} seconds...")
                
                # Use a loop with small sleeps to allow for quicker stopping
                for _ in range(int(delay * 10)):
                    if self.should_stop:
                        break
                    time.sleep(0.1)
            
            self.is_running = False
            self._update_status("Continuous requests stopped.")
        
        # Start the thread
        thread = threading.Thread(target=run_requests)
        thread.daemon = True
        thread.start()
    
    def stop_continuous_requests(self) -> None:
        """Stop the continuous API requests."""
        self.should_stop = True
        self._update_status("Stopping continuous requests...")
