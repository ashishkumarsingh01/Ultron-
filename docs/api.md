# Ultron API Reference

## UltronAgent

### Initialization

```python
from ultron.core import UltronAgent
from ultron.config import UltronConfig

config = UltronConfig()
agent = UltronAgent(config)
```

### Core Methods

#### `execute(task_description, task_id=None, **kwargs) -> str`
Execute a complex task with automatic planning and execution.

```python
result = agent.execute("Search for AI news and summarize")
```

#### `think(prompt, system_prompt=None, **kwargs) -> str`
Process a prompt through the LLM.

```python
response = agent.think("What is artificial intelligence?")
```

#### `remember(content, metadata=None) -> str`
Store content in memory.

```python
memory_id = agent.remember("Important fact", {"type": "fact"})
```

#### `recall(query, k=5) -> List[Dict]`
Retrieve relevant memories.

```python
results = agent.recall("artificial intelligence", k=10)
```

#### `get_task_status(task_id) -> TaskStatus`
Get the status of a task.

```python
status = agent.get_task_status("task-123")
```

#### `get_execution_history(limit=10) -> List[Task]`
Get execution history.

```python
history = agent.get_execution_history()
```

#### `clear_conversation() -> None`
Clear conversation history.

```python
agent.clear_conversation()
```

#### `get_info() -> Dict`
Get agent information.

```python
info = agent.get_info()
```

## Brain

```python
from ultron.core import Brain

brain = Brain(config)
response = brain.think("prompt", system_prompt="context")
```

## Memory

```python
from ultron.core import Memory

memory = Memory(config)
memory_id = memory.remember("content", {"key": "value"})
results = memory.recall("query", k=5)
```

## Planner

```python
from ultron.core import Planner

planner = Planner(config, brain, memory)
task = planner.create_task("Task description")
result = await planner.execute_task(task)
```

## Interfaces

### Voice Interface

```python
from ultron.interfaces import VoiceInterface

voice = VoiceInterface(agent)
text = voice.process_input()  # Capture from microphone
voice.process_output(response)  # Speak response
```

### Vision Interface

```python
from ultron.interfaces import VisionInterface

vision = VisionInterface(agent)
analysis = vision.analyze_image("image.jpg")
text = vision.extract_text("image.jpg")
```

### Web Interface

```python
from ultron.interfaces import WebInterface

web = WebInterface(agent)
results = web.search("query")
data = web.fetch_json("https://api.example.com")
```

### Text Interface

```python
from ultron.interfaces import TextInterface

text = TextInterface(agent)
response = text.chat("message")
```

## Control Systems

### Computer Control

```python
from ultron.control import ComputerControl

computer = ComputerControl(agent)
computer.move_mouse(100, 100)
computer.click(100, 100)
computer.type_text("Hello")
```

### Android Control

```python
from ultron.control import AndroidControl

android = AndroidControl(agent, device_id="device-id")
devices = android.get_devices()
android.tap(100, 100)
android.swipe(100, 100, 200, 200)
```

### Developer Agent

```python
from ultron.control import DeveloperAgent

dev = DeveloperAgent(agent)
code = dev.generate_code("create a sorting function")
tests = dev.generate_tests(code)
```

## Web API

### Endpoints

- `GET /` - Welcome message
- `GET /api/info` - Agent information
- `GET /api/config` - Configuration
- `POST /api/think` - Process prompt
- `POST /api/execute` - Execute task
- `POST /api/remember` - Store in memory
- `GET /api/recall` - Retrieve from memory
- `GET /api/history` - Execution history
- `GET /api/conversation` - Chat history
- `POST /api/conversation/clear` - Clear history
- `WS /ws/chat` - WebSocket chat

### Example API Call

```bash
curl -X POST "http://localhost:8000/api/think?prompt=Hello"
```

## Configuration Options

See `ultron/config.py` for all available configuration options.
