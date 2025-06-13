"""
LLM wrapper to handle Bedrock-specific requirements
"""

from typing import Any, Dict, List, Optional
from litellm import completion
import os


class BedrockLLM:
    """Wrapper for Bedrock LLM that handles response cleaning"""
    
    def __init__(self, model: Optional[str] = None):
        self.model = model or os.getenv("CREWAI_LLM_MODEL", "bedrock/us.anthropic.claude-3-opus-20240229-v1:0")
    
    def call(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Call the LLM and clean the response"""
        try:
            response = completion(
                model=self.model,
                messages=messages,
                **kwargs
            )
            
            # Get the content and clean trailing whitespace
            content = response.choices[0].message.content
            if content:
                content = content.rstrip()  # Remove trailing whitespace
            
            return content
            
        except Exception as e:
            # If it's a trailing whitespace error, try to clean and retry
            if "trailing whitespace" in str(e):
                # Clean the last message if it's from assistant
                if messages and messages[-1].get("role") == "assistant":
                    messages[-1]["content"] = messages[-1]["content"].rstrip()
                    return self.call(messages, **kwargs)
            raise e


def get_bedrock_llm():
    """Factory function to get configured Bedrock LLM"""
    return BedrockLLM()