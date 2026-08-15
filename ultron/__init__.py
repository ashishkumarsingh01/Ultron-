"""
ULTRON - Advanced AI Agent Kernel

A comprehensive, modular AI agent system with multi-modal capabilities,
intelligent planning, and integrated tool ecosystem.
"""

__version__ = "0.1.0"
__author__ = "Ultron Team"
__license__ = "MIT"

from ultron.core.agent import UltronAgent
from ultron.config import UltronConfig
from ultron.utils.logger import setup_logger

__all__ = [
    "UltronAgent",
    "UltronConfig",
    "setup_logger",
]