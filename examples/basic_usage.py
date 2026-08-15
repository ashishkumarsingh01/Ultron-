"""
Basic example of using Ultron Agent.
"""

from ultron.core import UltronAgent
from ultron.config import UltronConfig


def main():
    """Run basic example."""
    # Create configuration
    config = UltronConfig(
        agent_name="Ultron",
        agent_description="Advanced AI Agent Kernel",
        enable_voice=False,  # Set to True to enable voice
        enable_vision=False,  # Set to True to enable vision
        enable_web=True,
    )
    
    # Initialize agent
    agent = UltronAgent(config)
    
    print(f"\n{'='*60}")
    print(f"Welcome to {agent.config.agent_name}")
    print(f"{agent.config.agent_description}")
    print(f"{'='*60}\n")
    
    # Get agent info
    info = agent.get_info()
    print(f"Agent Info:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Example: Chat with agent
    print(f"\n{'='*60}")
    print("Chat Mode")
    print(f"{'='*60}\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Think about the input
            response = agent.think(user_input)
            print(f"\nUltron: {response}\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
