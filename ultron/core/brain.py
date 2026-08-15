"""
Brain module - LLM integration for Ultron Agent Kernel.
"""

import logging
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod

from ultron.config import UltronConfig, LLMProvider
from ultron.utils.errors import BrainException
from ultron.utils.logger import setup_logger


class LLMProvider_(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate response from LLM."""
        pass


class OpenAIProvider(LLMProvider_):
    """OpenAI LLM provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise BrainException("openai package not installed")
    
    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048, **kwargs) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise BrainException(f"OpenAI API error: {str(e)}")


class Brain:
    """Brain module - LLM integration."""
    
    def __init__(self, config: UltronConfig):
        self.config = config
        self.logger = setup_logger(
            "ultron.brain",
            level=config.log_level,
            log_file=config.log_file,
            enable_file_logging=config.enable_file_logging
        )
        
        self._initialize_provider()
        self.conversation_history: List[Dict[str, str]] = []
        self.logger.info(f"Brain initialized with {config.llm_provider.value} provider")
    
    def _initialize_provider(self) -> None:
        if self.config.llm_provider == LLMProvider.OPENAI:
            if not self.config.openai_api_key:
                raise BrainException("OpenAI API key not provided")
            self.provider = OpenAIProvider(
                api_key=self.config.openai_api_key,
                model=self.config.llm_model
            )
        else:
            raise BrainException(f"Provider {self.config.llm_provider} not yet implemented")
    
    def think(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        try:
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = self.provider.generate(
                full_prompt,
                temperature=self.config.llm_temperature,
                max_tokens=self.config.llm_max_tokens,
                **kwargs
            )
            
            self.conversation_history.append({"role": "user", "content": prompt})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            self.logger.debug(f"Think result: {response[:100]}...")
            return response
        except Exception as e:
            self.logger.error(f"Think failed: {str(e)}")
            raise BrainException(f"Failed to process prompt: {str(e)}")
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.conversation_history = []
        self.logger.info("Conversation history cleared")
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.conversation_history.copy()