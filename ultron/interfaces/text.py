"""
Text interface for Ultron Agent Kernel.
"""

import logging
from typing import Optional

from ultron.interfaces.base import BaseInterface
from ultron.utils.logger import setup_logger


class TextInterface(BaseInterface):
    """Text interface for text-based interaction."""
    
    def __init__(self, agent):
        super().__init__(agent)
        self.logger = setup_logger("ultron.interfaces.text")
    
    def process_input(self, text: str) -> str:
        """Process text input.
        
        Args:
            text: Input text
            
        Returns:
            Processed text
        """
        self.logger.debug(f"Processing input: {text[:50]}...")
        return text.strip()
    
    def process_output(self, output: str) -> str:
        """Process text output.
        
        Args:
            output: Output text
            
        Returns:
            Processed text
        """
        self.logger.debug(f"Processing output: {output[:50]}...")
        return output
    
    def chat(self, message: str) -> str:
        """Chat with the agent.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        self.logger.info(f"User: {message}")
        response = self.agent.think(message)
        self.logger.info(f"Agent: {response}")
        return response
    
    def ask(self, question: str) -> str:
        """Ask the agent a question.
        
        Args:
            question: Question to ask
            
        Returns:
            Agent response
        """
        return self.chat(question)
    
    def get_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Get response with optional system prompt.
        
        Args:
            prompt: User prompt
            system_prompt: System context
            
        Returns:
            Agent response
        """
        return self.agent.think(prompt, system_prompt)