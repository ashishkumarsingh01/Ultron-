"""
Example: Web search and scraping with Ultron.
"""

from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.interfaces import WebInterface


def main():
    """Run web search example."""
    # Create configuration
    config = UltronConfig(
        agent_name="Ultron Web",
        enable_web=True,
    )
    
    # Initialize agent
    agent = UltronAgent(config)
    
    print("\n" + "="*60)
    print("Ultron - Web Integration Example")
    print("="*60 + "\n")
    
    # Initialize web interface
    web = WebInterface(agent)
    
    try:
        # Search the web
        print("Searching for 'artificial intelligence'...")
        results = web.search("artificial intelligence")
        
        print(f"\nSearch Results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']}")
            print(f"     {result['url']}")
        
        # Fetch a webpage
        print("\nFetching example.com...")
        response = web.process_input("https://example.com")
        
        print(f"\nResponse:")
        for key, value in response.items():
            print(f"  {key}: {value}")
        
        # Fetch JSON from API
        print("\nFetching JSON data...")
        json_data = web.fetch_json("https://api.github.com/users/github")
        print(f"Retrieved {len(json_data)} fields from API")
    
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
