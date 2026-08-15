"""
Web server and API for Ultron Agent.
"""

import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import json

from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.utils.logger import setup_logger


class UltronServer:
    """Web server for Ultron Agent."""
    
    def __init__(self, config: Optional[UltronConfig] = None, host: str = "0.0.0.0", port: int = 8000):
        self.config = config or UltronConfig.from_env()
        self.host = host
        self.port = port
        self.logger = setup_logger("ultron.server")
        
        # Initialize agent
        self.agent = UltronAgent(self.config)
        
        # Create FastAPI app
        self.app = FastAPI(
            title="Ultron Agent API",
            description="Advanced AI Agent Kernel Web API",
            version="0.1.0"
        )
        
        # Add CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Setup routes
        self._setup_routes()
        self.logger.info(f"Ultron Server initialized on {host}:{port}")
    
    def _setup_routes(self) -> None:
        """Setup API routes."""
        
        @self.app.get("/")
        async def root():
            return {"message": "Welcome to Ultron Agent API", "version": "0.1.0"}
        
        @self.app.get("/api/info")
        async def get_info():
            """Get agent information."""
            return self.agent.get_info()
        
        @self.app.get("/api/config")
        async def get_config():
            """Get current configuration."""
            return self.config.to_dict()
        
        @self.app.post("/api/think")
        async def think(prompt: str, system_prompt: Optional[str] = None):
            """Process a prompt through the brain."""
            try:
                response = self.agent.think(prompt, system_prompt)
                return {"prompt": prompt, "response": response}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/execute")
        async def execute(task: str):
            """Execute a task."""
            try:
                result = self.agent.execute(task)
                return {"task": task, "result": result, "status": "completed"}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/remember")
        async def remember(content: str, metadata: Optional[Dict[str, Any]] = None):
            """Store in memory."""
            try:
                memory_id = self.agent.remember(content, metadata)
                return {"memory_id": memory_id, "content": content}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/recall")
        async def recall(query: str, k: int = 5):
            """Retrieve from memory."""
            try:
                results = self.agent.recall(query, k)
                return {"query": query, "results": results}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/history")
        async def get_history(limit: int = 10):
            """Get execution history."""
            try:
                tasks = self.agent.get_execution_history(limit)
                return {"tasks": [task.__dict__ for task in tasks]}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/conversation")
        async def get_conversation():
            """Get conversation history."""
            return {"history": self.agent.brain.get_history()}
        
        @self.app.post("/api/conversation/clear")
        async def clear_conversation():
            """Clear conversation history."""
            self.agent.clear_conversation()
            return {"status": "cleared"}
        
        @self.app.websocket("/ws/chat")
        async def websocket_chat(websocket: WebSocket):
            """WebSocket endpoint for real-time chat."""
            await websocket.accept()
            try:
                while True:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Process message
                    response = self.agent.think(message.get("prompt", ""))
                    
                    # Send response
                    await websocket.send_json({
                        "prompt": message.get("prompt"),
                        "response": response
                    })
            except Exception as e:
                self.logger.error(f"WebSocket error: {str(e)}")
                await websocket.close()
    
    def run(self) -> None:
        """Run the server."""
        import uvicorn
        self.logger.info(f"Starting Ultron Server on {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
