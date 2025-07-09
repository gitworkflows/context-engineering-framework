"""
Command Line Interface for the Context Engineering Framework.
"""
import os
import sys
import asyncio
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import (
    BaseAgent, 
    ContextManager,
    FileReadTool,
    FileWriteTool
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CLIAgent(BaseAgent):
    """A simple CLI agent that can execute commands."""
    
    def __init__(self):
        super().__init__(
            name="CLIAgent",
            description="A command-line interface agent"
        )
        # Add some basic tools
        self.add_tool(FileReadTool())
        self.add_tool(FileWriteTool())
    
    async def process(self, command: str, **kwargs) -> str:
        """Process a command and return the result."""
        self.conversation.append(
            {"role": "user", "content": command, "kwargs": kwargs}
        )
        
        try:
            # Simple command routing
            parts = command.strip().split()
            if not parts:
                return "No command provided. Type 'help' for available commands."
                
            cmd = parts[0].lower()
            args = parts[1:]
            
            if cmd == "help":
                return self.help()
            elif cmd == "list":
                return self.list_tools()
            elif cmd == "read":
                if len(args) < 1:
                    return "Usage: read <file_path> [encoding=utf-8]"
                file_path = args[0]
                encoding = args[1] if len(args) > 1 else "utf-8"
                tool = self.get_tool("file_read")
                result = await tool.execute(file_path=file_path, encoding=encoding)
                return result["data"]["content"]
            elif cmd == "write":
                if len(args) < 2:
                    return "Usage: write <file_path> <content> [encoding=utf-8]"
                file_path = args[0]
                content = " ".join(args[1:])
                tool = self.get_tool("file_write")
                result = await tool.execute(file_path=file_path, content=content)
                return result["message"]
            else:
                return f"Unknown command: {cmd}. Type 'help' for available commands."
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def help(self) -> str:
        """Show help information."""
        return """Available commands:
  help                - Show this help message
  list                - List available tools
  read <file>         - Read a file
  write <file> <text> - Write text to a file
"""
    
    def list_tools(self) -> str:
        """List available tools."""
        tools = self.list_tools()
        if not tools:
            return "No tools available."
            
        result = ["Available tools:"]
        for tool in tools:
            result.append(f"- {tool['name']}: {tool['description']}")
            
        return "\n".join(result)


async def main():
    """Main entry point for the CLI."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Context Engineering Framework CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the interactive shell")
    
    # Read file command
    read_parser = subparsers.add_parser("read", help="Read a file")
    read_parser.add_argument("file", help="File to read")
    read_parser.add_argument("--encoding", default="utf-8", help="File encoding")
    
    # Write file command
    write_parser = subparsers.add_parser("write", help="Write to a file")
    write_parser.add_argument("file", help="File to write to")
    write_parser.add_argument("content", help="Content to write")
    write_parser.add_argument("--encoding", default="utf-8", help="File encoding")
    write_parser.add_argument("--append", action="store_true", help="Append to file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create agent
    agent = CLIAgent()
    
    # Execute command
    if args.command == "run":
        print("Context Engineering Framework - Interactive Shell")
        print("Type 'help' for available commands, 'exit' to quit")
        
        while True:
            try:
                # Get user input
                user_input = input("\ncef> ").strip()
                
                # Handle exit
                if user_input.lower() in ("exit", "quit"):
                    print("Goodbye!")
                    break
                    
                # Process command
                result = await agent.process(user_input)
                print(result)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to exit")
            except Exception as e:
                print(f"Error: {str(e)}")
                
    elif args.command == "read":
        tool = FileReadTool()
        result = await tool.execute(
            file_path=args.file,
            encoding=args.encoding
        )
        if result["success"]:
            print(result["data"]["content"])
        else:
            print(f"Error: {result['message']}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "write":
        tool = FileWriteTool()
        result = await tool.execute(
            file_path=args.file,
            content=args.content,
            encoding=args.encoding,
            append=args.append
        )
        if result["success"]:
            print(result["message"])
        else:
            print(f"Error: {result['message']}", file=sys.stderr)
            sys.exit(1)
            
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
