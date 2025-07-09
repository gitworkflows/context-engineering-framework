"""
Core tools and utilities for the Context Engineering Framework.
"""
from typing import Any, Dict, List, Optional, Callable, Type, TypeVar, Union
from pathlib import Path
import json
import yaml
import logging
from pydantic import BaseModel, Field, validator

# Configure logging
logger = logging.getLogger(__name__)

T = TypeVar('T', bound='BaseTool')

class ToolError(Exception):
    """Base exception for tool-related errors."""
    pass


class ToolInput(BaseModel):
    """Base class for tool input schemas."""
    pass


class ToolOutput(BaseModel):
    """Base class for tool output schemas."""
    success: bool = Field(..., description="Whether the tool executed successfully")
    message: str = Field("", description="Status message or error details")
    data: Optional[Dict[str, Any]] = Field(None, description="Result data from the tool")


class BaseTool:
    """Base class for all tools in the system."""
    
    name: str = "base_tool"
    description: str = "Base tool class"
    version: str = "0.1.0"
    
    # Schema definitions
    input_schema: Type[ToolInput] = ToolInput
    output_schema: Type[ToolOutput] = ToolOutput
    
    def __init__(self, **kwargs):
        """Initialize the tool with configuration."""
        self.config = kwargs
        self.logger = logging.getLogger(f"tool.{self.name}")
    
    def validate_input(self, input_data: Dict[str, Any]) -> ToolInput:
        """Validate input data against the tool's input schema."""
        try:
            return self.input_schema(**input_data)
        except Exception as e:
            self.logger.error(f"Input validation failed: {str(e)}")
            raise ToolError(f"Invalid input: {str(e)}")
    
    def validate_output(self, output_data: Dict[str, Any]) -> ToolOutput:
        """Validate output data against the tool's output schema."""
        try:
            return self.output_schema(**output_data)
        except Exception as e:
            self.logger.error(f"Output validation failed: {str(e)}")
            raise ToolError(f"Invalid output: {str(e)}")
    
    async def execute(self, **kwargs) -> ToolOutput:
        """Execute the tool with the given arguments.
        
        Subclasses should override this method to implement their specific functionality.
        """
        try:
            # Validate input
            input_data = self.validate_input(kwargs)
            
            # Execute tool logic (to be implemented by subclasses)
            result = await self._execute(input_data)
            
            # Validate and return output
            return self.validate_output({
                "success": True,
                "message": "Operation completed successfully",
                "data": result
            })
            
        except Exception as e:
            self.logger.error(f"Tool execution failed: {str(e)}", exc_info=True)
            return self.output_schema(
                success=False,
                message=f"Tool execution failed: {str(e)}",
                data={"error": str(e)}
            )
    
    async def _execute(self, input_data: ToolInput) -> Dict[str, Any]:
        """Internal implementation of the tool's functionality."""
        # Default implementation returns the input data
        return input_data.dict()
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the OpenAPI schema for this tool."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "input_schema": self.input_schema.schema() if self.input_schema else {},
            "output_schema": self.output_schema.schema() if self.output_schema else {}
        }


# Example tools

class FileReadInput(ToolInput):
    """Input schema for the FileReadTool."""
    file_path: str = Field(..., description="Path to the file to read")
    encoding: str = Field("utf-8", description="File encoding")


class FileReadOutput(ToolOutput):
    """Output schema for the FileReadTool."""
    content: str = Field(..., description="File contents")
    size: int = Field(..., description="File size in bytes")


class FileReadTool(BaseTool):
    """Tool for reading files from the filesystem."""
    
    name = "file_read"
    description = "Read content from a file"
    input_schema = FileReadInput
    output_schema = FileReadOutput
    
    async def _execute(self, input_data: FileReadInput) -> Dict[str, Any]:
        file_path = Path(input_data.file_path)
        if not file_path.exists():
            raise ToolError(f"File not found: {file_path}")
            
        content = file_path.read_text(encoding=input_data.encoding)
        return {
            "content": content,
            "size": len(content)
        }


class FileWriteInput(ToolInput):
    """Input schema for the FileWriteTool."""
    file_path: str = Field(..., description="Path to the file to write")
    content: str = Field(..., description="Content to write to the file")
    encoding: str = Field("utf-8", description="File encoding")
    append: bool = Field(False, description="Whether to append to the file")


class FileWriteTool(BaseTool):
    """Tool for writing files to the filesystem."""
    
    name = "file_write"
    description = "Write content to a file"
    input_schema = FileWriteInput
    
    async def _execute(self, input_data: FileWriteInput) -> Dict[str, Any]:
        file_path = Path(input_data.file_path)
        mode = "a" if input_data.append else "w"
        
        try:
            with open(file_path, mode, encoding=input_data.encoding) as f:
                f.write(input_data.content)
                
            return {"success": True, "message": f"Successfully wrote to {file_path}"}
            
        except Exception as e:
            raise ToolError(f"Failed to write to file: {str(e)}")


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def example():
        # Example: Using the file read tool
        reader = FileReadTool()
        result = await reader.execute(file_path=__file__)
        print(f"File content (first 100 chars): {result.data['content'][:100]}...")
        
        # Example: Using the file write tool
        writer = FileWriteTool()
        result = await writer.execute(
            file_path="example.txt",
            content="Hello, world!\nThis is a test.",
            encoding="utf-8"
        )
        print(f"Write result: {result.message}")
    
    asyncio.run(example())
