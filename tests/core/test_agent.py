"""Tests for the core agent module."""
import pytest
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from context_engineering_framework.core.agent import BaseAgent, Message

class TestBaseAgent:
    """Test cases for BaseAgent class."""
    
    @pytest.fixture
    def agent(self):
        """Create a test agent instance."""
        return BaseAgent(name="test_agent", description="A test agent")
    
    def test_agent_initialization(self, agent):
        """Test agent initialization."""
        assert agent.name == "test_agent"
        assert agent.description == "A test agent"
        assert len(agent.conversation) == 0
    
    def test_add_message(self, agent):
        """Test adding a message to the conversation."""
        message = Message(role="user", content="Hello, agent!")
        agent.conversation.append(message)
        
        assert len(agent.conversation) == 1
        assert agent.conversation[0].role == "user"
        assert agent.conversation[0].content == "Hello, agent!"
