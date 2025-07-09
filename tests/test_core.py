"""
Tests for core functionality of the Context Engineering Framework.
"""
import pytest
import asyncio
from pathlib import Path
from src.core import (
    ContextManager,
    BaseAgent,
    Tool,
    Message,
    BaseTool,
    ToolInput,
    ToolOutput,
    ToolError
)

# Test data
TEST_CONTEXT = {
    "app": {
        "name": "TestApp",
        "version": "1.0.0"
    },
    "user": {
        "id": 123,
        "name": "Test User"
    }
}

# Fixtures
@pytest.fixture
def context_manager():
    """Create a context manager with test data."""
    cm = ContextManager()
    cm.add_source("test_source", TEST_CONTEXT)
    return cm

@pytest.fixture
def base_agent():
    """Create a base agent for testing."""
    return BaseAgent(name="TestAgent", description="A test agent")

# Test ContextManager
class TestContextManager:
    """Tests for the ContextManager class."""
    
    def test_add_source(self, context_manager):
        """Test adding a context source."""
        assert len(context_manager.sources) == 1
        assert context_manager.sources[0].name == "test_source"
    
    def test_merge_contexts(self, context_manager):
        """Test merging context sources."""
        # Add another source with higher priority
        context_manager.add_source(
            "override", 
            {"app": {"name": "OverriddenApp"}},
            priority=10
        )
        
        # Merge contexts
        merged = context_manager.merge_contexts()
        
        # Check that higher priority source overrides lower priority
        assert merged["app"]["name"] == "OverriddenApp"
        # Check that other values are still present
        assert merged["app"]["version"] == "1.0.0"
        assert merged["user"]["name"] == "Test User"
    
    def test_get_context(self, context_manager):
        """Test getting context values."""
        # Get entire context
        context = context_manager.get_context()
        assert context["app"]["name"] == "TestApp"
        
        # Get specific value
        app_name = context_manager.get_context("app.name")
        assert app_name == "TestApp"
        
        # Get non-existent value with default
        missing = context_manager.get_context("nonexistent.key", "default")
        assert missing == "default"
    
    def test_load_from_file(self, tmp_path):
        """Test loading context from a file."""
        # Create a test JSON file
        json_file = tmp_path / "test.json"
        json_file.write_text('{"test": "value"}')
        
        # Create a test YAML file
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text('test: value')
        
        # Test loading JSON
        cm = ContextManager()
        cm.load_from_file(str(json_file))
        assert cm.get_context("test") == "value"
        
        # Test loading YAML
        cm = ContextManager()
        cm.load_from_file(str(yaml_file))
        assert cm.get_context("test") == "value"
        
        # Test invalid file
        with pytest.raises(ValueError):
            cm.load_from_file("nonexistent.json")

# Test BaseAgent
class TestBaseAgent:
    """Tests for the BaseAgent class."""
    
    @pytest.mark.asyncio
    async def test_process(self, base_agent):
        """Test processing a message."""
        response = await base_agent.process("Test message")
        assert "TestAgent received: Test message" in response
        assert len(base_agent.conversation) == 2  # User + Assistant messages
    
    def test_add_tool(self, base_agent):
        """Test adding a tool to the agent."""
        # Define a test tool
        def test_tool():
            """Test tool."""
            return "test"
        
        # Add the tool
        base_agent.add_tool(test_tool)
        
        # Check that the tool was added
        assert "test_tool" in base_agent.tools
        assert base_agent.tools["test_tool"].description == "Test tool."
    
    def test_remove_tool(self, base_agent):
        """Test removing a tool from the agent."""
        # Add a tool
        base_agent.add_tool(lambda: None, name="test_tool")
        assert "test_tool" in base_agent.tools
        
        # Remove the tool
        assert base_agent.remove_tool("test_tool") is True
        assert "test_tool" not in base_agent.tools
        
        # Try to remove non-existent tool
        assert base_agent.remove_tool("nonexistent") is False
    
    def test_set_get_context(self, base_agent):
        """Test setting and getting context."""
        # Set context
        context = {"key": "value"}
        base_agent.set_context(context)
        
        # Get context
        assert base_agent.get_context() == context
        assert base_agent.get_context("key") == "value"
        assert base_agent.get_context("nonexistent", "default") == "default"
    
    def test_reset(self, base_agent):
        """Test resetting the agent."""
        # Add some state
        base_agent.conversation = ["message1", "message2"]
        base_agent.context = {"key": "value"}
        
        # Reset the agent
        base_agent.reset()
        
        # Check that state was reset
        assert base_agent.conversation == []
        assert base_agent.context == {}  # Context is not reset by default

# Test Tool System
class TestToolSystem:
    """Tests for the tool system."""
    
    def test_tool_creation(self):
        """Test creating a tool."""
        def test_func(arg1: str) -> str:
            """Test function."""
            return f"Hello, {arg1}!"
        
        # Create a tool from a function
        tool = Tool.from_callable(test_func)
        
        # Check tool properties
        assert tool.name == "test_func"
        assert "Test function" in tool.description
        assert tool.input_schema is not None
        assert tool.output_schema is not None
        
        # Execute the tool
        result = tool(arg1="world")
        assert result == "Hello, world!"
    
    @pytest.mark.asyncio
    async def test_base_tool(self):
        """Test the BaseTool class."""
        class TestTool(BaseTool):
            """Test tool."""
            name = "test_tool"
            description = "A test tool"
            
            class Input(ToolInput):
                """Input schema."""
                name: str = Field(..., description="Name to greet")
            
            class Output(ToolOutput):
                """Output schema."""
                greeting: str = Field(..., description="Greeting message")
            
            async def _execute(self, input_data: Input) -> Dict[str, Any]:
                """Execute the tool."""
                return {"greeting": f"Hello, {input_data.name}!"}
        
        # Create and use the tool
        tool = TestTool()
        result = await tool.execute(name="Test")
        
        # Check the result
        assert result.success is True
        assert result.greeting == "Hello, Test!"
        
        # Test validation
        with pytest.raises(ToolError):
            await tool.execute()  # Missing required argument

# Test Message
class TestMessage:
    """Tests for the Message class."""
    
    def test_message_creation(self):
        """Test creating a message."""
        # Test with required arguments
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.metadata is None
        
        # Test with metadata
        metadata = {"timestamp": "2023-01-01T00:00:00"}
        msg = Message(role="assistant", content="Hi there!", metadata=metadata)
        assert msg.role == "assistant"
        assert msg.content == "Hi there!"
        assert msg.metadata == metadata
    
    def test_message_validation(self):
        """Test message validation."""
        # Test valid roles
        for role in ["user", "assistant", "system", "tool"]:
            msg = Message(role=role, content="test")
            assert msg.role == role
        
        # Test invalid role
        with pytest.raises(ValueError):
            Message(role="invalid", content="test")
        
        # Test empty content
        with pytest.raises(ValueError):
            Message(role="user", content="")
