"""
Example plugin for Ultron.
"""

from ultron.plugins.plugin_base import UltronPlugin


class CalculatorPlugin(UltronPlugin):
    """Simple calculator plugin."""
    
    def __init__(self):
        super().__init__("calculator", "1.0.0")
    
    def execute(self, operation: str, a: float, b: float) -> float:
        """Execute calculation.
        
        Args:
            operation: add, subtract, multiply, divide
            a: First number
            b: Second number
            
        Returns:
            Result
        """
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        else:
            raise ValueError(f"Unknown operation: {operation}")
