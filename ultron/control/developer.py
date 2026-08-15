"""
Developer agent for Ultron - Code generation and automation.

Uses free, open-source tools and APIs.
"""

import logging
from typing import Optional, List, Dict, Any

from ultron.utils.errors import ControlException
from ultron.utils.logger import setup_logger


class DeveloperAgent:
    """Developer automation and code generation."""
    
    def __init__(self, agent=None):
        self.agent = agent
        self.logger = setup_logger("ultron.control.developer")
        self.generated_code = []
    
    def generate_code(self, description: str, language: str = "python") -> str:
        """Generate code from description.
        
        Args:
            description: What code to generate
            language: Programming language
            
        Returns:
            Generated code
        """
        try:
            if self.agent is None:
                raise ControlException("Agent not available")
            
            prompt = f"""Generate {language} code that {description}
            
            Provide only the code without explanations.
            Use proper formatting and best practices."""
            
            code = self.agent.think(prompt)
            self.generated_code.append({"language": language, "code": code})
            self.logger.info(f"Generated {language} code")
            return code
        except Exception as e:
            self.logger.error(f"Code generation failed: {str(e)}")
            raise ControlException(f"Failed to generate code: {str(e)}")
    
    def generate_tests(self, code: str, language: str = "python") -> str:
        """Generate tests for code.
        
        Args:
            code: Code to test
            language: Programming language
            
        Returns:
            Generated test code
        """
        try:
            if self.agent is None:
                raise ControlException("Agent not available")
            
            framework = "pytest" if language == "python" else "jest"
            
            prompt = f"""Generate {framework} tests for this {language} code:
            
            ```{language}
            {code}
            ```
            
            Provide comprehensive test cases."""
            
            tests = self.agent.think(prompt)
            self.logger.info(f"Generated {framework} tests")
            return tests
        except Exception as e:
            self.logger.error(f"Test generation failed: {str(e)}")
            raise ControlException(f"Failed to generate tests: {str(e)}")
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code for issues.
        
        Args:
            code: Code to analyze
            
        Returns:
            Analysis results
        """
        try:
            if self.agent is None:
                raise ControlException("Agent not available")
            
            prompt = f"""Analyze this code for:
            1. Security issues
            2. Performance problems
            3. Code quality issues
            4. Best practice violations
            
            Code:
            ```
            {code}
            ```
            
            Provide a structured analysis."""
            
            analysis = self.agent.think(prompt)
            self.logger.info("Code analysis completed")
            return {"code": code, "analysis": analysis}
        except Exception as e:
            self.logger.error(f"Code analysis failed: {str(e)}")
            raise ControlException(f"Failed to analyze code: {str(e)}")
    
    def document_code(self, code: str) -> str:
        """Generate documentation for code.
        
        Args:
            code: Code to document
            
        Returns:
            Documentation
        """
        try:
            if self.agent is None:
                raise ControlException("Agent not available")
            
            prompt = f"""Generate comprehensive documentation for this code:
            
            ```
            {code}
            ```
            
            Include:
            - Function descriptions
            - Parameter explanations
            - Return value descriptions
            - Usage examples"""
            
            docs = self.agent.think(prompt)
            self.logger.info("Documentation generated")
            return docs
        except Exception as e:
            self.logger.error(f"Documentation generation failed: {str(e)}")
            raise ControlException(f"Failed to generate documentation: {str(e)}")
    
    def refactor_code(self, code: str, improvements: Optional[List[str]] = None) -> str:
        """Refactor code.
        
        Args:
            code: Code to refactor
            improvements: List of improvements to make
            
        Returns:
            Refactored code
        """
        try:
            if self.agent is None:
                raise ControlException("Agent not available")
            
            improvements_text = ", ".join(improvements) if improvements else "best practices"
            
            prompt = f"""Refactor this code for {improvements_text}:
            
            ```
            {code}
            ```
            
            Provide only the refactored code."""
            
            refactored = self.agent.think(prompt)
            self.logger.info("Code refactored")
            return refactored
        except Exception as e:
            self.logger.error(f"Code refactoring failed: {str(e)}")
            raise ControlException(f"Failed to refactor code: {str(e)}")
    
    def get_generated_code(self) -> List[Dict[str, str]]:
        """Get all generated code.
        
        Returns:
            List of generated code snippets
        """
        return self.generated_code.copy()
