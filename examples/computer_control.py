"""
Example: Computer automation with Ultron.
"""

from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.control import ComputerControl


def main():
    """Run computer control example."""
    config = UltronConfig(
        agent_name="Ultron Computer Control",
        enable_computer_control=True,
    )
    
    agent = UltronAgent(config)
    computer = ComputerControl(agent)
    
    print("\n" + "="*60)
    print("Ultron - Computer Control Example")
    print("="*60 + "\n")
    
    try:
        # Get screen size
        width, height = computer.get_screen_size()
        print(f"Screen size: {width}x{height}")
        
        # Move mouse
        print(f"\nMoving mouse to center...")
        center_x, center_y = width // 2, height // 2
        computer.move_mouse(center_x, center_y)
        
        # Take screenshot
        print("Taking screenshot...")
        screenshot = computer.screenshot("ultron_screenshot.png")
        print("Screenshot saved as 'ultron_screenshot.png'")
        
        # Type text
        print("\nExample: Type 'Hello Ultron' (click a text field first)")
        # Uncomment to use:
        # computer.type_text("Hello Ultron")
        
        print("\nComputer control examples completed!")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Computer control requires appropriate OS permissions")


if __name__ == "__main__":
    main()
