"""
Context Engineering Framework - A framework for building and managing AI agents.

This package provides the core components for creating context-aware AI agents.
"""

__version__ = "0.1.0"

# Import core components
from .core.context import ContextManager, ContextSource
from .core.agent import BaseAgent, Tool, Message
from .core.tools import (
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
