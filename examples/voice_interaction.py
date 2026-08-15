"""
Example: Voice interaction with Ultron.
"""

from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.interfaces import VoiceInterface, TextInterface


def main():
    """Run voice interaction example."""
    # Create configuration
    config = UltronConfig(
        agent_name="Ultron Voice",
        enable_voice=True,
        enable_vision=False,
    )
    
    # Initialize agent
    agent = UltronAgent(config)
    
    print("\n" + "="*60)
    print("Ultron - Voice Interaction Example")
    print("="*60 + "\n")
    
    # Initialize interfaces
    voice = VoiceInterface(agent)
    text = TextInterface(agent)
    
    try:
        # Get voice input
        print("Please speak...")
        spoken_text = voice.process_input()
        print(f"You said: {spoken_text}\n")
        
        # Process with agent
        response = agent.think(spoken_text)
        print(f"Ultron thinks: {response}\n")
        
        # Speak response
        print("Speaking response...")
        voice.process_output(response)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Voice processing requires microphone and speech recognition library")


if __name__ == "__main__":
    main()
