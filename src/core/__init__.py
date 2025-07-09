"""
Core components of the Context Engineering Framework.

This package contains the fundamental building blocks for creating and managing
AI agents, including the base agent class, context management, and core tools.
"""

# Import core components
from .context import ContextManager, ContextSource
from .agent import BaseAgent, Tool, Message
from .tools import (
    BaseTool, 
    ToolError, 
    ToolInput, 
    ToolOutput,
    FileReadTool,
    FileWriteTool
)

__all__ = [
    'ContextManager',
    'ContextSource',
    'BaseAgent',
    'Tool',
    'Message',
    'BaseTool',
    'ToolError',
    'ToolInput',
    'ToolOutput',
    'FileReadTool',
    'FileWriteTool'
]
