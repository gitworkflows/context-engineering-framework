"""
Context Management Example

This script demonstrates how to use the ContextManager to manage and merge context
from multiple sources with different priorities.
"""
import asyncio
import json
from pathlib import Path
from typing import Dict, Any

from context_engineering_framework import ContextManager


async def main():
    """Run the context management example."""
    print("=== Context Management Example ===\n")
    
    # Initialize the context manager
    context_manager = ContextManager()
    
    # Example 1: Add context from a dictionary
    user_context = {
        "user": {
            "id": "user123",
            "name": "John Doe",
            "preferences": {
                "theme": "dark",
                "notifications": True
            }
        }
    }
    
    # Add the context with a priority of 10 (lower priority)
    context_manager.add_context(user_context, priority=10, source="user_profile")
    print("Added user context:")
    print(json.dumps(context_manager.get_context(), indent=2))
    
    # Example 2: Add higher priority context
    session_context = {
        "user": {
            "preferences": {
                "theme": "light"  # Override the theme
            },
            "session": {
                "id": "session_xyz",
                "start_time": "2025-07-08T12:00:00Z"
            }
        }
    }
    
    # Add with higher priority (will override the theme)
    context_manager.add_context(session_context, priority=20, source="session")
    print("\nAfter adding session context (higher priority):")
    print(json.dumps(context_manager.get_context(), indent=2))
    
    # Example 3: Load context from a file
    def load_context_from_file(file_path: str) -> Dict[str, Any]:
        """Load context from a JSON file."""
        with open(file_path, 'r') as f:
            return json.load(f)
    
    # Create a sample config file
    config_path = Path("example_config.json")
    config_data = {
        "app": {
            "version": "1.0.0",
            "environment": "development"
        }
    }
    
    with open(config_path, 'w') as f:
        json.dump(config_data, f)
    
    # Load context from the file
    config_context = load_context_from_file(config_path)
    context_manager.add_context(config_context, priority=5, source="config_file")
    
    print("\nAfter adding config context (lowest priority):")
    print(json.dumps(context_manager.get_context(), indent=2))
    
    # Example 4: Get specific context values
    print("\nGetting specific values:")
    print(f"User name: {context_manager.get('user.name')}")
    print(f"Theme: {context_manager.get('user.preferences.theme')}")
    print(f"Environment: {context_manager.get('app.environment')}")
    
    # Example 5: Remove context by source
    context_manager.remove_source("session")
    print("\nAfter removing session context:")
    print(f"Theme reverted to: {context_manager.get('user.preferences.theme')}")
    
    # Clean up
    config_path.unlink()


if __name__ == "__main__":
    asyncio.run(main())
