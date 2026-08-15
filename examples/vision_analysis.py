"""
Example: Vision and image analysis with Ultron.
"""

from pathlib import Path
from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.interfaces import VisionInterface


def main():
    """Run vision example."""
    # Create configuration
    config = UltronConfig(
        agent_name="Ultron Vision",
        enable_vision=True,
    )
    
    # Initialize agent
    agent = UltronAgent(config)
    
    print("\n" + "="*60)
    print("Ultron - Vision Analysis Example")
    print("="*60 + "\n")
    
    # Initialize vision interface
    vision = VisionInterface(agent)
    
    # Example image path
    image_path = "example.jpg"
    
    if not Path(image_path).exists():
        print(f"No image found at {image_path}")
        print("To use this example:")
        print("1. Add an image file named 'example.jpg'")
        print("2. Run this script again")
        return
    
    try:
        # Analyze image
        analysis = vision.analyze_image(image_path)
        print(f"Image Analysis:")
        for key, value in analysis.items():
            print(f"  {key}: {value}")
        
        # Extract text from image
        print("\nExtracting text...")
        text = vision.extract_text(image_path)
        if text:
            print(f"Extracted Text:\n{text}")
        else:
            print("No text found in image")
        
        # Detect objects
        print("\nDetecting objects...")
        objects = vision.detect_objects(image_path)
        if objects:
            print(f"Objects found: {objects}")
        else:
            print("No objects detected")
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
