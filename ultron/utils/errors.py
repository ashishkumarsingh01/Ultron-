"""
Custom exceptions for Ultron Agent Kernel.
"""


class UltronException(Exception):
    """Base exception for Ultron."""
    pass


class BrainException(UltronException):
    """Exception raised by Brain/LLM module."""
    pass


class MemoryException(UltronException):
    """Exception raised by Memory module."""
    pass


class PlannerException(UltronException):
    """Exception raised by Planner module."""
    pass


class InterfaceException(UltronException):
    """Exception raised by Interface modules."""
    pass


class ControlException(UltronException):
    """Exception raised by Control modules."""
    pass


class VoiceProcessingError(InterfaceException):
    """Error during voice processing."""
    pass


class VisionProcessingError(InterfaceException):
    """Error during vision processing."""
    pass


class TaskTimeoutError(PlannerException):
    """Task execution timeout."""
    pass