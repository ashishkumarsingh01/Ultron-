"""
Web application entry point for Ultron.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
from typing import Optional, Dict, Any
import json

from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.utils.logger import setup_logger

# Initialize logging
logger = setup_logger("ultron.app")

# Create FastAPI app
app = FastAPI(
    title="Ultron Agent API",
    description="Advanced AI Agent Kernel Web API",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize configuration and agent
try:
    config = UltronConfig.from_env()
    agent = UltronAgent(config)
    logger.info("Ultron Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize agent: {str(e)}")
    agent = None

# Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Ultron Agent API", "version": "0.1.0"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/dashboard.html")
async def dashboard():
    """Serve dashboard."""
    try:
        return FileResponse("ultron/web/dashboard.html", media_type="text/html")
    except Exception as e:
        logger.error(f"Failed to serve dashboard: {str(e)}")
        return {"error": "Dashboard not found"}

@app.get("/api/info")
async def get_info():
    """Get agent information."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        return agent.get_info()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/config")
async def get_config():
    """Get configuration."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        return agent.config.to_dict()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/think")
async def think(prompt: str, system_prompt: Optional[str] = None):
    """Process a prompt through the brain."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        response = agent.think(prompt, system_prompt)
        return {"prompt": prompt, "response": response, "status": "success"}
    except Exception as e:
        logger.error(f"Think error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/execute")
async def execute(task: str):
    """Execute a task."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        result = agent.execute(task)
        return {"task": task, "result": result, "status": "completed"}
    except Exception as e:
        logger.error(f"Execute error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/api/remember")
async def remember(content: str, metadata: Optional[Dict[str, Any]] = None):
    """Store in memory."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        memory_id = agent.remember(content, metadata)
        return {"memory_id": memory_id, "content": content, "status": "success"}
    except Exception as e:
        logger.error(f"Remember error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/recall")
async def recall(query: str, k: int = 5):
    """Retrieve from memory."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        results = agent.recall(query, k)
        return {"query": query, "results": results, "status": "success"}
    except Exception as e:
        logger.error(f"Recall error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/history")
async def get_history(limit: int = 10):
    """Get execution history."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        tasks = agent.get_execution_history(limit)
        return {"tasks": [task.__dict__ for task in tasks], "status": "success"}
    except Exception as e:
        logger.error(f"History error: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.get("/api/conversation")
async def get_conversation():
    """Get conversation history."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        history = agent.brain.get_history()
        return {"history": history, "status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/conversation/clear")
async def clear_conversation():
    """Clear conversation history."""
    if agent is None:
        return {"status": "error", "message": "Agent not initialized"}
    try:
        agent.clear_conversation()
        return {"status": "cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
