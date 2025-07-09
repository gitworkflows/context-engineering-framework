"""
Custom Tools Example

This script demonstrates how to create and use custom tools with the Context Engineering Framework.
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from context_engineering_framework import BaseTool, BaseAgent


# Define input and output models for our tools
class CalculatorInput(BaseModel):
    """Input model for the calculator tool."""
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")
    operation: str = Field(
        ...,
        description="Operation to perform",
        regex="^(add|subtract|multiply|divide)$"
    )


class CalculatorOutput(BaseModel):
    """Output model for the calculator tool."""
    result: float
    operation: str


class WeatherInput(BaseModel):
    """Input model for the weather tool."""
    location: str = Field(..., description="City name or coordinates")
    date: Optional[str] = Field(
        None,
        description="Date in YYYY-MM-DD format (default: today)",
        regex="^\d{4}-\d{2}-\d{2}$"
    )


class WeatherOutput(BaseModel):
    """Output model for the weather tool."""
    location: str
    date: str
    temperature: float
    condition: str
    humidity: float


# Create custom tools
class CalculatorTool(BaseTool):
    """A simple calculator tool that performs basic arithmetic operations."""
    name = "calculator"
    description = "Perform basic arithmetic calculations"
    input_model = CalculatorInput
    output_model = CalculatorOutput
    
    async def execute(self, input_data: CalculatorInput) -> CalculatorOutput:
        """Execute the calculator operation."""
        operations = {
            "add": lambda a, b: a + b,
            "subtract": lambda a, b: a - b,
            "multiply": lambda a, b: a * b,
            "divide": lambda a, b: a / b if b != 0 else float('inf')
        }
        
        operation_func = operations.get(input_data.operation)
        if not operation_func:
            raise ValueError(f"Unsupported operation: {input_data.operation}")
            
        result = operation_func(input_data.a, input_data.b)
        return CalculatorOutput(
            result=result,
            operation=f"{input_data.a} {input_data.operation} {input_data.b}"
        )


class WeatherTool(BaseTool):
    """A mock weather tool that simulates weather data retrieval."""
    name = "get_weather"
    description = "Get weather information for a location"
    input_model = WeatherInput
    output_model = WeatherOutput
    
    # Mock weather data (in a real app, this would call a weather API)
    _mock_weather_data = {
        "New York": {
            "temperature": 22.5,
            "condition": "Sunny",
            "humidity": 0.65
        },
        "London": {
            "temperature": 15.0,
            "condition": "Cloudy",
            "humidity": 0.75
        },
        "Tokyo": {
            "temperature": 28.0,
            "condition": "Rainy",
            "humidity": 0.85
        }
    }
    
    async def execute(self, input_data: WeatherInput) -> WeatherOutput:
        """Get weather information for the specified location."""
        # In a real implementation, this would call a weather API
        location = input_data.location.title()
        date = input_data.date or datetime.now().strftime("%Y-%m-%d")
        
        # Get mock data or use defaults
        weather = self._mock_weather_data.get(location, {
            "temperature": 20.0,
            "condition": "Clear",
            "humidity": 0.5
        })
        
        return WeatherOutput(
            location=location,
            date=date,
            temperature=weather["temperature"],
            condition=weather["condition"],
            humidity=weather["humidity"]
        )


class ToolUsingAgent(BaseAgent):
    """An agent that uses custom tools."""
    
    def __init__(self):
        super().__init__(
            name="ToolUser",
            description="An agent that demonstrates tool usage"
        )
        
        # Register tools
        self.add_tool(CalculatorTool())
        self.add_tool(WeatherTool())
    
    async def process(self, input_text: str, **kwargs) -> str:
        """Process input and use tools as needed."""
        # Simple command parsing (in a real app, use a proper parser)
        parts = input_text.lower().split()
        if not parts:
            return "Please provide a command. Type 'help' for available commands."
        
        command = parts[0]
        args = parts[1:]
        
        try:
            if command == "calculate":
                if len(args) != 3:
                    return "Usage: calculate <num1> <operation> <num2>"
                
                a, op, b = args
                result = await self.tools["calculator"].execute(
                    CalculatorInput(a=float(a), b=float(b), operation=op)
                )
                return f"Result: {result.operation} = {result.result}"
                
            elif command == "weather":
                if not args:
                    return "Usage: weather <location> [date]"
                
                location = args[0]
                date = args[1] if len(args) > 1 else None
                weather = await self.tools["get_weather"].execute(
                    WeatherInput(location=location, date=date)
                )
                return (
                    f"Weather in {weather.location} on {weather.date}:\n"
                    f"- Temperature: {weather.temperature}°C\n"
                    f"- Condition: {weather.condition}\n"
                    f"- Humidity: {weather.humidity*100}%"
                )
                
            elif command in ("help", "?"):
                return """
                Available commands:
                - calculate <num1> <operation> <num2> - Perform a calculation
                  (operations: add, subtract, multiply, divide)
                - weather <location> [date] - Get weather for a location
                - help - Show this help message
                """
                
            else:
                return f"Unknown command: {command}. Type 'help' for available commands."
                
        except Exception as e:
            return f"Error: {str(e)}"


async def main():
    """Run the custom tools example."""
    print("=== Custom Tools Example ===\n")
    
    # Create and run the agent
    agent = ToolUsingAgent()
    
    # Example interactions
    examples = [
        "help",
        "calculate 5 add 3",
        "calculate 10 multiply 7.5",
        "weather New York",
        "weather London 2025-07-15",
        "weather Tokyo",
        "calculate 10 divide 0",  # This will show infinity
        "invalid command"
    ]
    
    for example in examples:
        print(f"\nYou: {example}")
        response = await agent.process(example)
        print(f"Agent: {response}")


if __name__ == "__main__":
    asyncio.run(main())
