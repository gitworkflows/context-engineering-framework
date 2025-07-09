"""
Base agent class for the Context Engineering Framework.
Provides core functionality for all agents in the system.
"""
from typing import Dict, Any, List, Optional, Callable, Type, TypeVar, Union
from pydantic import BaseModel, Field, validator
from dataclasses import dataclass
import inspect
import logging

# Type variable for agent subclasses
T = TypeVar('T', bound='BaseAgent')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Tool(BaseModel):
    """Represents a tool that can be used by an agent."""
    name: str
    description: str
    func: Callable
    input_schema: Optional[Type[BaseModel]] = None
    output_schema: Optional[Type[BaseModel]] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def __call__(self, *args, **kwargs) -> Any:
        """Execute the tool with the given arguments."""
        try:
            # Validate input if schema is provided
            if self.input_schema:
                if inspect.isclass(self.input_schema) and issubclass(self.input_schema, BaseModel):
                    validated_input = self.input_schema(**kwargs)
                    kwargs = validated_input.dict()
            
            # Execute the function
            result = self.func(*args, **kwargs)
            
            # Validate output if schema is provided
            if self.output_schema:
                if inspect.isclass(self.output_schema) and issubclass(self.output_schema, BaseModel):
                    if isinstance(result, dict):
                        result = self.output_schema(**result)
                    elif not isinstance(result, self.output_schema):
                        result = self.output_schema(result=result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {str(e)}")
            raise


@dataclass
class Message:
    """A message in the agent's conversation."""
    role: str  # 'user', 'assistant', 'system', 'tool'
    content: str
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self, name: str, description: str = ""):
        """Initialize the agent with a name and optional description."""
        self.name = name
        self.description = description
        self.tools: Dict[str, Tool] = {}
        self.conversation: List[Message] = []
        self.context: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"agent.{self.name}")
    
    def add_tool(self, tool: Union[Tool, Callable], 
                name: str = None, 
                description: str = None,
                input_schema: Type[BaseModel] = None,
                output_schema: Type[BaseModel] = None) -> None:
        """Add a tool to the agent's toolkit.
        
        Args:
            tool: Either a Tool instance or a callable
            name: Name of the tool (required if tool is callable)
            description: Description of the tool (required if tool is callable)
            input_schema: Pydantic model for input validation
            output_schema: Pydantic model for output validation
        """
        if isinstance(tool, Tool):
            self.tools[tool.name] = tool
        elif callable(tool):
            if not name:
                name = tool.__name__
            if not description:
                description = tool.__doc__ or ""
                
            self.tools[name] = Tool(
                name=name,
                description=description,
                func=tool,
                input_schema=input_schema,
                output_schema=output_schema
            )
        else:
            raise ValueError("Tool must be either a Tool instance or a callable")
    
    def remove_tool(self, name: str) -> bool:
        """Remove a tool from the agent's toolkit."""
        if name in self.tools:
            del self.tools[name]
            return True
        return False
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools with their descriptions."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema.schema() if tool.input_schema else None,
                "output_schema": tool.output_schema.schema() if tool.output_schema else None
            }
            for tool in self.tools.values()
        ]
    
    async def process(self, input_text: str, **kwargs) -> str:
        """Process an input message and return a response.
        
        This is the main entry point for the agent. Subclasses should override
        this method to implement their specific behavior.
        """
        # Add user message to conversation
        self.conversation.append(Message(role="user", content=input_text))
        
        # Default implementation just echoes the input
        response = f"{self.name} received: {input_text}"
        
        # Add assistant response to conversation
        self.conversation.append(Message(role="assistant", content=response))
        
        return response
    
    def set_context(self, context: Dict[str, Any]) -> None:
        """Set the agent's context."""
        self.context = context
    
    def get_context(self, key: str = None, default: Any = None) -> Any:
        """Get a value from the agent's context."""
        if key is None:
            return self.context
        return self.context.get(key, default)
    
    def reset(self) -> None:
        """Reset the agent's conversation and state."""
        self.conversation = []
        # Don't reset tools or context, just conversation


# Example usage
if __name__ == "__main__":
    # Create a simple agent
    agent = BaseAgent(name="EchoAgent", description="An agent that echoes back input")
    
    # Process a message
    response = agent.process("Hello, world!")
    print(response)  # Output: EchoAgent received: Hello, world!
