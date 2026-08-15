"""
Configuration management for Ultron Agent Kernel.
"""

import os
from typing import Optional, Dict, Any
from enum import Enum

from pydantic_settings import BaseSettings
from pydantic import Field


class LLMProvider(str, Enum):
    """Available LLM providers."""
    OPENAI = "openai"
    CLAUDE = "claude"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"


class MemoryBackend(str, Enum):
    """Available memory backends."""
    PINECONE = "pinecone"
    WEAVIATE = "weaviate"
    CHROMA = "chroma"
    MILVUS = "milvus"


class UltronConfig(BaseSettings):
    """Main configuration for Ultron Agent."""
    
    # Agent Configuration
    agent_name: str = Field(default="Ultron", description="Agent name")
    agent_description: str = Field(default="Advanced AI Agent Kernel", description="Agent description")
    
    # LLM Configuration
    llm_provider: LLMProvider = Field(default=LLMProvider.OPENAI, description="LLM provider")
    llm_model: str = Field(default="gpt-4", description="LLM model name")
    llm_temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="LLM temperature")
    llm_max_tokens: int = Field(default=2048, description="Max tokens for LLM response")
    
    # API Keys
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    claude_api_key: Optional[str] = Field(default=None, description="Claude API key")
    huggingface_api_key: Optional[str] = Field(default=None, description="HuggingFace API key")
    google_cloud_key: Optional[str] = Field(default=None, description="Google Cloud API key")
    pinecone_api_key: Optional[str] = Field(default=None, description="Pinecone API key")
    
    # Memory Configuration
    memory_backend: MemoryBackend = Field(default=MemoryBackend.CHROMA, description="Memory backend")
    memory_dimension: int = Field(default=1536, description="Vector embedding dimension")
    pinecone_index: str = Field(default="ultron", description="Pinecone index name")
    memory_retention_days: int = Field(default=30, description="Memory retention in days")
    
    # Interface Configuration
    enable_voice: bool = Field(default=True, description="Enable voice interface")
    enable_vision: bool = Field(default=True, description="Enable vision interface")
    enable_web: bool = Field(default=True, description="Enable web interface")
    voice_language: str = Field(default="en-US", description="Voice language")
    
    # Control Configuration
    enable_computer_control: bool = Field(default=True, description="Enable computer control")
    enable_android_control: bool = Field(default=True, description="Enable Android control")
    enable_developer_agent: bool = Field(default=True, description="Enable developer agent")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="logs/ultron.log", description="Log file path")
    enable_file_logging: bool = Field(default=True, description="Enable file logging")
    
    # Planner Configuration
    max_planning_steps: int = Field(default=10, description="Max planning steps")
    timeout_seconds: int = Field(default=300, description="Task timeout in seconds")
    
    # Plugin Configuration
    plugin_dir: str = Field(default="./plugins", description="Plugin directory")
    auto_load_plugins: bool = Field(default=True, description="Auto-load plugins")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @classmethod
    def from_env(cls) -> "UltronConfig":
        """Load configuration from environment variables."""
        return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return self.model_dump(exclude_none=True)