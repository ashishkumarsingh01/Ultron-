"""
Example: Developer agent for code generation.
"""

from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.control import DeveloperAgent


def main():
    """Run developer agent example."""
    config = UltronConfig(
        agent_name="Ultron Developer",
        enable_developer_agent=True,
        openai_api_key="your-api-key-here",  # Add your API key
    )
    
    agent = UltronAgent(config)
    developer = DeveloperAgent(agent)
    
    print("\n" + "="*60)
    print("Ultron - Developer Agent Example")
    print("="*60 + "\n")
    
    try:
        # Generate code
        print("Generating Python function...")
        print("-" * 60)
        code = developer.generate_code(
            "creates a function that checks if a number is prime",
            language="python"
        )
        print(code)
        
        # Generate tests
        print("\n" + "="*60)
        print("Generating tests...")
        print("-" * 60)
        tests = developer.generate_tests(code, language="python")
        print(tests)
        
        # Analyze code
        print("\n" + "="*60)
        print("Analyzing code...")
        print("-" * 60)
        analysis = developer.analyze_code(code)
        print(analysis["analysis"])
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Developer agent requires OpenAI API key")


if __name__ == "__main__":
    main()
