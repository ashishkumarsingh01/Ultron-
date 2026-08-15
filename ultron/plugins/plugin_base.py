"""
Base plugin class for Ultron.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging


class UltronPlugin(ABC):
    """Base class for Ultron plugins."""
    
    def __init__(self, name: str, version: str = "1.0.0"):
        """Initialize plugin.
        
        Args:
            name: Plugin name
            version: Plugin version
        """
        self.name = name
        self.version = version
        self.logger = logging.getLogger(f"ultron.plugin.{name}")
        self.enabled = True
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute plugin functionality.
        
        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Plugin result
        """
        pass
    
    def initialize(self) -> None:
        """Initialize plugin."""
        self.logger.info(f"Initializing plugin: {self.name} v{self.version}")
    
    def shutdown(self) -> None:
        """Shutdown plugin."""
        self.logger.info(f"Shutting down plugin: {self.name}")
    
    def get_info(self) -> Dict[str, Any]:
        """Get plugin information.
        
        Returns:
            Plugin info
        """
        return {
            "name": self.name,
            "version": self.version,
            "enabled": self.enabled
        }
