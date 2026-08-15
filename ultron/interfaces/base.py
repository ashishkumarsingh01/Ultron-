"""
Base interface class for Ultron.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseInterface(ABC):
    """Base class for all interfaces."""
    
    def __init__(self, agent):
        """Initialize interface.
        
        Args:
            agent: UltronAgent instance
        """
        self.agent = agent
    
    @abstractmethod
    def process_input(self, input_data: Any) -> Any:
        """Process input data.
        
        Args:
            input_data: Input to process
            
        Returns:
            Processed result
        """
        pass
    
    @abstractmethod
    def process_output(self, output_data: Any) -> Any:
        """Process output data.
        
        Args:
            output_data: Output to process
            
        Returns:
            Processed result
        """
        pass