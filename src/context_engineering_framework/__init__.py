"""Context Engineering Framework - A framework for building context-aware AI agents."""

from context_engineering_framework.core.agent import BaseAgent, Message
from context_engineering_framework.core.context import ContextManager, ContextSource
from context_engineering_framework.core.tools import BaseTool, ToolInput, ToolOutput

__version__ = "0.1.0"
__all__ = [
    'BaseAgent',
    'Message',
    'ContextManager',
    'ContextSource',
    'BaseTool',
    'ToolInput',
    'ToolOutput',
]
