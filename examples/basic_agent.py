"""
Basic example of using the Context Engineering Framework.

This script demonstrates how to:
1. Create a custom agent
2. Add tools to the agent
3. Use the context manager
4. Process messages
"""
import asyncio
from pathlib import Path
from src import BaseAgent, ContextManager, Tool, Message

class GreetingAgent(BaseAgent):
    """A simple agent that can greet users and remember their names."""
    
    def __init__(self):
        super().__init__(
            name="GreetingAgent",
            description="An agent that greets users by name"
        )
        # Initialize context with default values
        self.context = {
            "users": {}
        }
        
        # Add a custom tool
        self.add_tool(
            self.remember_name,
            name="remember_name",
            description="Remember a user's name"
        )
    
    async def process(self, input_text: str, **kwargs) -> str:
        """Process a message and return a response."""
        # Add user message to conversation
        self.conversation.append(Message(role="user", content=input_text))
        
        # Simple command parsing
        parts = input_text.lower().split()
        if not parts:
            response = "Please provide a command. Say 'help' for available commands."
        else:
            cmd = parts[0]
            args = parts[1:]
            
            if cmd == "hello":
                name = args[0] if args else "there"
                response = f"Hello, {name}! How can I help you today?"
            elif cmd == "remember":
                if len(args) < 2:
                    response = "Usage: remember <user_id> <name>"
                else:
                    user_id, name = args[0], " ".join(args[1:])
                    # Use the tool to remember the name
                    result = await self.tools["remember_name"].execute(user_id=user_id, name=name)
                    response = result["message"]
            elif cmd == "recall":
                if not args:
                    response = "Usage: recall <user_id>"
                else:
                    user_id = args[0]
                    name = self.context["users"].get(user_id, "unknown")
                    response = f"I remember you, {name}!" if name != "unknown" else f"I don't know any {user_id}."
            elif cmd in ("help", "?"):
                response = """Available commands:
                hello [name] - Greet someone
                remember <user_id> <name> - Remember a user's name
                recall <user_id> - Recall a user's name
                help - Show this help message
                """
            else:
                response = f"I don't understand '{cmd}'. Type 'help' for available commands."
        
        # Add assistant response to conversation
        self.conversation.append(Message(role="assistant", content=response))
        return response
    
    async def remember_name(self, user_id: str, name: str) -> dict:
        """
        Remember a user's name.
        
        Args:
            user_id: The ID of the user
            name: The name to remember
            
        Returns:
            dict: A result dictionary with a success flag and message
        """
        self.context["users"][user_id] = name
        return {
            "success": True,
            "message": f"I'll remember that {user_id} is named {name}."
        }


async def main():
    """Run the example."""
    print("=== Context Engineering Framework Example ===\n")
    
    # Create an agent
    agent = GreetingAgent()
    
    # Example conversation
    messages = [
        "hello",
        "remember user123 John Doe",
        "recall user123",
        "hello John",
        "recall unknown",
        "help"
    ]
    
    # Process each message
    for msg in messages:
        print(f"You: {msg}")
        response = await agent.process(msg)
        print(f"Agent: {response}\n")
    
    # Show the agent's context
    print("\nAgent's context:")
    for user_id, name in agent.context["users"].items():
        print(f"- {user_id}: {name}")
    
    # Show conversation history
    print("\nConversation history:")
    for msg in agent.conversation:
        print(f"{msg.role.title()}: {msg.content}")


if __name__ == "__main__":
    asyncio.run(main())
