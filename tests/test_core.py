"""
Tests for Ultron core components.
"""

import pytest
from ultron.core import UltronAgent
from ultron.config import UltronConfig
from ultron.utils.errors import BrainException, MemoryException


class TestUltronConfig:
    """Test configuration."""
    
    def test_config_defaults(self):
        """Test default configuration."""
        config = UltronConfig()
        assert config.agent_name == "Ultron"
        assert config.llm_model == "gpt-4"
        assert config.enable_voice is True
    
    def test_config_to_dict(self):
        """Test config to dict conversion."""
        config = UltronConfig(agent_name="TestAgent")
        config_dict = config.to_dict()
        assert config_dict["agent_name"] == "TestAgent"


class TestUltronAgent:
    """Test Ultron Agent."""
    
    @pytest.fixture
    def agent(self):
        """Create test agent."""
        config = UltronConfig(
            agent_name="TestUltron",
            enable_file_logging=False
        )
        return UltronAgent(config)
    
    def test_agent_initialization(self, agent):
        """Test agent initialization."""
        assert agent.config.agent_name == "TestUltron"
        assert agent.brain is not None
        assert agent.memory is not None
        assert agent.planner is not None
    
    def test_agent_info(self, agent):
        """Test get agent info."""
        info = agent.get_info()
        assert info["name"] == "TestUltron"
        assert "llm_model" in info
        assert "memory_backend" in info
    
    def test_memory_operations(self, agent):
        """Test memory operations."""
        # Remember
        memory_id = agent.remember("Test content", {"type": "test"})
        assert memory_id is not None
        
        # Recall
        results = agent.recall("Test content", k=5)
        assert isinstance(results, list)
    
    def test_clear_conversation(self, agent):
        """Test clear conversation."""
        agent.clear_conversation()
        history = agent.brain.get_history()
        assert len(history) == 0


class TestMemory:
    """Test Memory module."""
    
    @pytest.fixture
    def memory(self):
        """Create test memory."""
        from ultron.core.memory import Memory
        config = UltronConfig(enable_file_logging=False)
        return Memory(config)
    
    def test_remember(self, memory):
        """Test remember function."""
        memory_id = memory.remember("Test", {"tag": "test"})
        assert memory_id is not None
    
    def test_recall(self, memory):
        """Test recall function."""
        results = memory.recall("Test", k=5)
        assert isinstance(results, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
