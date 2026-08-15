"""
Main Ultron Agent class - Orchestrates all components.
"""

import logging
import asyncio
from typing import Optional, Dict, Any, List

from ultron.config import UltronConfig
from ultron.core.brain import Brain
from ultron.core.memory import Memory
from ultron.core.planner import Planner, Task, TaskStatus
from ultron.utils.errors import UltronException
from ultron.utils.logger import setup_logger


class UltronAgent:
    """Main Ultron Agent - Orchestrates Brain, Memory, and Planner."""
    
    def __init__(self, config: Optional[UltronConfig] = None):
        if config is None:
            config = UltronConfig.from_env()
        
        self.config = config
        self.logger = setup_logger(
            "ultron",
            level=config.log_level,
            log_file=config.log_file,
            enable_file_logging=config.enable_file_logging
        )
        
        self.brain = Brain(config)
        self.memory = Memory(config)
        self.planner = Planner(config, self.brain, self.memory)
        
        self.logger.info(f"Ultron Agent '{config.agent_name}' initialized")
    
    def execute(self, task_description: str, task_id: Optional[str] = None, **kwargs) -> str:
        """Execute a task synchronously."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.execute_async(task_description, task_id, **kwargs))
        finally:
            loop.close()
    
    async def execute_async(self, task_description: str, task_id: Optional[str] = None, **kwargs) -> str:
        """Execute a task asynchronously."""
        try:
            task = self.planner.create_task(task_description, task_id, **kwargs)
            
            self.memory.remember(
                f"Task created: {task_description}",
                {"task_id": task.id, "type": "task_creation"}
            )
            
            result = await self.planner.execute_task(task)
            
            self.memory.remember(
                f"Task completed: {result}",
                {"task_id": task.id, "type": "task_completion"}
            )
            
            return result
        except Exception as e:
            self.logger.error(f"Task execution failed: {str(e)}")
            raise
    
    def think(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Process a prompt through the brain."""
        return self.brain.think(prompt, system_prompt, **kwargs)
    
    def remember(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Store content in memory."""
        return self.memory.remember(content, metadata)
    
    def recall(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve memories."""
        return self.memory.recall(query, k)
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Get task status."""
        task = self.planner.get_task(task_id)
        return task.status if task else None
    
    def get_execution_history(self, limit: int = 10) -> List[Task]:
        """Get execution history."""
        return self.planner.get_execution_history(limit)
    
    def clear_conversation(self) -> None:
        """Clear conversation history."""
        self.brain.clear_history()
        self.logger.info("Conversation history cleared")
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": self.config.agent_name,
            "description": self.config.agent_description,
            "llm_model": self.config.llm_model,
            "memory_backend": self.config.memory_backend.value,
            "version": "0.1.0"
        }