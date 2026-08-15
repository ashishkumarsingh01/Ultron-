"""
Run Ultron web server.
"""

from ultron.web.server import UltronServer
from ultron.config import UltronConfig


def main():
    """Start the web server."""
    config = UltronConfig.from_env()
    server = UltronServer(config, host="0.0.0.0", port=8000)
    
    print("\n" + "="*60)
    print("Ultron Web Server")
    print("="*60)
    print(f"\n🌐 Starting server...")
    print(f"Dashboard: http://localhost:8000/dashboard")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"WebSocket: ws://localhost:8000/ws/chat")
    print(f"\nPress Ctrl+C to stop\n")
    
    try:
        server.run()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")


if __name__ == "__main__":
    main()
