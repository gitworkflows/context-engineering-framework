"""
Web Integration Example

This script demonstrates how to integrate the Context Engineering Framework
with a web server using FastAPI.
"""
import asyncio
import json
import uvicorn
from typing import Dict, Any, List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from context_engineering_framework import BaseAgent, Message, Tool

# Configure FastAPI app
app = FastAPI(
    title="Context Engineering Framework API",
    description="A web API for the Context Engineering Framework",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ChatMessage(BaseModel):
    """Model for chat messages."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: str = datetime.utcnow().isoformat()


class ChatRequest(BaseModel):
    """Model for chat requests."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Model for chat responses."""
    response: str
    conversation_id: str
    timestamp: str = datetime.utcnow().isoformat()


# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_message(self, message: str, client_id: str):
        """Send a message to a specific client."""
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
    
    async def broadcast(self, message: str):
        """Send a message to all connected clients."""
        for connection in self.active_connections.values():
            await connection.send_text(message)


# Create a simple agent for the web interface
class WebAgent(BaseAgent):
    """A simple agent for the web interface."""
    
    def __init__(self):
        super().__init__(name="WebAgent", description="Handles web requests")
        # Store conversation history by conversation ID
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        
        # Register some example tools
        self.add_tool(CalculatorTool())
        self.add_tool(DateTimeTool())
    
    async def process_chat(self, message: str, conversation_id: str = "default") -> str:
        """Process a chat message and return a response."""
        # Initialize conversation if it doesn't exist
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        # Add user message to conversation history
        self.conversations[conversation_id].append({"role": "user", "content": message})
        
        # Simple command parsing
        if message.lower().startswith("calculate "):
            try:
                # Simple calculation (in a real app, use a proper parser)
                expr = message[10:].strip()
                result = eval(expr, {"__builtins__": {}}, {})  # Safe eval with no builtins
                response = f"The result of {expr} is {result}"
            except Exception as e:
                response = f"Could not calculate: {str(e)}"
        elif "time" in message.lower():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = f"The current date and time is: {current_time}"
        elif "hello" in message.lower() or "hi " in message.lower():
            response = "Hello! How can I assist you today?"
        else:
            response = f"I received your message: {message}"
        
        # Add assistant response to conversation history
        self.conversations[conversation_id].append({"role": "assistant", "content": response})
        
        return response


# Example tools
class CalculatorTool(Tool):
    """A simple calculator tool."""
    name = "calculator"
    description = "Perform basic arithmetic calculations"
    
    async def execute(self, expression: str) -> Dict[str, Any]:
        """Evaluate a mathematical expression."""
        try:
            # Safe evaluation with limited operations
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Invalid characters in expression")
            
            result = eval(expression, {"__builtins__": {}}, {})
            return {"expression": expression, "result": result, "status": "success"}
        except Exception as e:
            return {"expression": expression, "error": str(e), "status": "error"}


class DateTimeTool(Tool):
    """A tool to get the current date and time."""
    name = "datetime"
    description = "Get the current date and time"
    
    async def execute(self, timezone: str = "UTC") -> Dict[str, str]:
        """Get the current date and time."""
        now = datetime.utcnow()
        return {
            "utc": now.isoformat(),
            "timezone": timezone,
            "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "success"
        }


# Initialize the agent and connection manager
agent = WebAgent()
manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """Handle WebSocket connections."""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process the message with the agent
            response = await agent.process_chat(
                message.get("content", ""),
                message.get("conversation_id", "default")
            )
            
            # Send the response back to the client
            await manager.send_message(
                json.dumps({
                    "type": "response",
                    "content": response,
                    "conversation_id": message.get("conversation_id", "default")
                }),
                client_id
            )
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")


# REST API endpoints
@app.post("/chat", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    """Handle chat requests."""
    try:
        response = await agent.process_chat(
            chat_request.message,
            chat_request.conversation_id or "default"
        )
        
        return ChatResponse(
            response=response,
            conversation_id=chat_request.conversation_id or "default"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/{conversation_id}", response_model=List[ChatMessage])
async def get_conversation(conversation_id: str):
    """Get the conversation history."""
    if conversation_id not in agent.conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return [
        ChatMessage(role=msg["role"], content=msg["content"])
        for msg in agent.conversations[conversation_id]
    ]


@app.get("/tools", response_model=List[Dict[str, str]])
async def list_tools():
    """List all available tools."""
    return [
        {"name": name, "description": tool.description}
        for name, tool in agent.tools.items()
    ]


@app.post("/tools/{tool_name}")
async def execute_tool(tool_name: str, params: Dict[str, Any]):
    """Execute a tool."""
    if tool_name not in agent.tools:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    try:
        result = await agent.tools[tool_name].execute(**params)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run(
        "web_integration:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
