"""
Planner module - Agent loop and task planning for Ultron Agent Kernel.
"""

import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio
import uuid

from ultron.config import UltronConfig
from ultron.utils.errors import PlannerException, TaskTimeoutError
from ultron.utils.logger import setup_logger


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    PLANNING = "planning"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class Task:
    """Task definition."""
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    steps: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    result: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class Planner:
    """Planner module - Task planning and agent loop."""
    
    def __init__(self, config: UltronConfig, brain=None, memory=None):
        self.config = config
        self.brain = brain
        self.memory = memory
        
        self.logger = setup_logger(
            "ultron.planner",
            level=config.log_level,
            log_file=config.log_file,
            enable_file_logging=config.enable_file_logging
        )
        
        self.tasks: Dict[str, Task] = {}
        self.execution_history: List[Task] = []
        self.logger.info("Planner initialized")
    
    def create_task(self, description: str, task_id: Optional[str] = None, **metadata) -> Task:
        if task_id is None:
            task_id = str(uuid.uuid4())[:8]
        
        task = Task(
            id=task_id,
            description=description,
            metadata=metadata
        )
        
        self.tasks[task_id] = task
        self.logger.info(f"Created task: {task_id} - {description}")
        return task
    
    def plan_task(self, task: Task) -> List[str]:
        try:
            task.status = TaskStatus.PLANNING
            task.updated_at = datetime.now()
            
            if self.brain is None:
                task.steps = [task.description]
            else:
                planning_prompt = f"""Break down this task into specific steps:
                Task: {task.description}
                Provide 3-5 actionable steps."""
                
                response = self.brain.think(planning_prompt)
                task.steps = self._parse_steps(response)
            
            self.logger.info(f"Planned {len(task.steps)} steps for task {task.id}")
            return task.steps
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self.logger.error(f"Failed to plan task {task.id}: {str(e)}")
            raise PlannerException(f"Task planning failed: {str(e)}")
    
    async def execute_task(self, task: Task) -> str:
        try:
            task.status = TaskStatus.EXECUTING
            task.updated_at = datetime.now()
            
            steps = self.plan_task(task)
            results = []
            
            for i, step in enumerate(steps):
                self.logger.info(f"Executing step {i+1}/{len(steps)}: {step}")
                try:
                    step_result = await asyncio.wait_for(
                        self._execute_step(step),
                        timeout=self.config.timeout_seconds
                    )
                    results.append(step_result)
                except asyncio.TimeoutError:
                    raise TaskTimeoutError(f"Step {i} timed out")
            
            task.result = "\n".join(results)
            task.status = TaskStatus.COMPLETED
            task.updated_at = datetime.now()
            self.execution_history.append(task)
            
            self.logger.info(f"Task {task.id} completed successfully")
            return task.result
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self.logger.error(f"Task {task.id} execution failed: {str(e)}")
            raise
    
    async def _execute_step(self, step: str) -> str:
        await asyncio.sleep(0.1)
        return f"Completed: {step}"
    
    def _parse_steps(self, response: str) -> List[str]:
        lines = response.split('\n')
        steps = []
        for line in lines:
            line = line.strip()
            if line and any(line.startswith(f"{i}.") for i in range(1, 20)):
                step = line.split('.', 1)[1].strip() if '.' in line else line
                if step:
                    steps.append(step)
        return steps if steps else [response]
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_execution_history(self, limit: int = 10) -> List[Task]:
        return self.execution_history[-limit:]