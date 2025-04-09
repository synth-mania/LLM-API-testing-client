"""
Token usage tracking and cost calculation utilities.
"""

from typing import Dict, Any, Tuple
from openrouter_client.config.settings import config

class TokenUsage:
    """Track token usage and calculate costs."""
    
    def __init__(self):
        """Initialize token usage counters."""
        self.input_tokens = 0
        self.output_tokens = 0
        self.call_count = 0
    
    def update(self, prompt_tokens: int, completion_tokens: int) -> None:
        """
        Update token counts with new usage.
        
        Args:
            prompt_tokens: Number of tokens in the prompt
            completion_tokens: Number of tokens in the completion
        """
        self.input_tokens += prompt_tokens
        self.output_tokens += completion_tokens
        self.call_count += 1
    
    def calculate_cost(self) -> float:
        """
        Calculate the total cost based on current token usage.
        
        Returns:
            float: Total cost in dollars
        """
        input_cost = self.input_tokens / 1_000_000 * config.get('input_price_per_million')
        output_cost = self.output_tokens / 1_000_000 * config.get('output_price_per_million')
        return input_cost + output_cost
    
    def get_usage_summary(self) -> str:
        """
        Return a formatted string with usage statistics.
        
        Returns:
            str: Formatted usage summary
        """
        return (
            f"TOTAL TOKENS: INPUT {self.input_tokens}    OUTPUT {self.output_tokens}\n"
            f"COST ${round(self.calculate_cost(), 2)}"
        )
    
    def get_usage_dict(self) -> Dict[str, Any]:
        """
        Return usage statistics as a dictionary.
        
        Returns:
            Dict[str, Any]: Usage statistics
        """
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.input_tokens + self.output_tokens,
            "call_count": self.call_count,
            "cost": round(self.calculate_cost(), 2)
        }
    
    def reset(self) -> None:
        """Reset all counters to zero."""
        self.input_tokens = 0
        self.output_tokens = 0
        self.call_count = 0
