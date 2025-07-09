"""Tests for the tools module."""
import pytest
import sys
from pathlib import Path
from pydantic import BaseModel, Field

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from context_engineering_framework.core.tools import BaseTool, ToolInput, ToolOutput

# Prevent these classes from being collected as tests by pytest
class _TestInput(ToolInput):
    """Test input schema."""
    name: str
    value: int = 42

class _TestOutput(ToolOutput):
    """Test output schema.
    
    This extends ToolOutput and adds specific fields to the data dictionary.
    The data dictionary will contain 'result' and 'status' fields.
    """
    data: dict = Field(
        default_factory=lambda: {"result": "", "status": False},
        description="Result data with 'result' and 'status' fields"
    )

class _TestTool(BaseTool):
    """Test tool implementation."""
    name = "test_tool"
    description = "A test tool"
    input_schema = _TestInput
    output_schema = _TestOutput
    
    async def _execute(self, input_data):
        # Return a dictionary that will be used as the 'data' field in the ToolOutput
        return {
            "result": f"Processed {input_data.name} with value {input_data.value}",
            "status": True
        }

class TestBaseTool:
    """Test cases for BaseTool class."""
    
    @pytest.fixture
    def tool(self):
        """Create a test tool instance."""
        return _TestTool()
    
    @pytest.mark.asyncio
    async def test_tool_execution(self, tool):
        """Test tool execution with valid input."""
        # Mock the _execute method to return data that will be used as the 'data' field
        async def mock_execute(self, input_data):
            return {
                "result": f"Processed {input_data.name} with value {input_data.value}",
                "status": True
            }
        
        # Replace the _execute method with our mock
        original_execute = tool._execute
        tool._execute = mock_execute.__get__(tool)
        
        try:
            # The execute method will wrap our mock result in a ToolOutput object
            result = await tool.execute(name="test", value=123)
            
            # The result should be a ToolOutput object with success, message, and data
            assert result.success is True
            assert result.message == "Operation completed successfully"
            
            # The data field should contain our mock result with result and status
            assert result.data is not None
            assert isinstance(result.data, dict)
            assert result.data["status"] is True
            assert "Processed test with value 123" in result.data["result"]
        finally:
            # Restore the original method
            tool._execute = original_execute
    
    @pytest.mark.asyncio
    async def test_input_validation(self, tool):
        """Test input validation."""
        # Call execute without required 'name' field
        result = await tool.execute()
        
        # Should return a ToolOutput with success=False and an error message
        assert result.success is False
        assert "Field required" in result.message
        assert "name" in result.message
    
    def test_get_schema(self, tool):
        """Test schema generation."""
        schema = tool.get_schema()
        
        assert schema["name"] == "test_tool"
        assert "description" in schema
        assert "input_schema" in schema
        assert "output_schema" in schema
        
        # Check input schema structure
        assert "properties" in schema["input_schema"]
        assert "name" in schema["input_schema"]["properties"]
        assert "value" in schema["input_schema"]["properties"]
        
        # Check output schema structure
        assert "properties" in schema["output_schema"]
        assert "data" in schema["output_schema"]["properties"]
        assert "message" in schema["output_schema"]["properties"]
        assert "success" in schema["output_schema"]["properties"]
