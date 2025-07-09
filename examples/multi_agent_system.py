"""
Multi-Agent System Example

This script demonstrates how to create and manage multiple agents that can
communicate and work together to solve problems.
"""
import asyncio
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from context_engineering_framework import BaseAgent, Message, Tool


# Define models for our tools and messages
class TaskRequest(BaseModel):
    """Model for task requests between agents."""
    task_id: str
    description: str
    priority: int = 1
    deadline: Optional[str] = None


class TaskResponse(BaseModel):
    """Model for task responses between agents."""
    task_id: str
    status: str  # "accepted", "rejected", "completed", "failed"
    result: Optional[Any] = None
    message: Optional[str] = None


# Define some tools for our agents
class TaskAssignmentTool(Tool):
    """Tool for assigning tasks to other agents."""
    name = "assign_task"
    description = "Assign a task to another agent"
    input_model = TaskRequest
    
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
    
    async def execute(self, input_data: TaskRequest) -> Dict[str, Any]:
        """Execute the task assignment."""
        # In a real implementation, this would send the task to another agent
        print(f"{self.agent.name} received task: {input_data.description}")
        return {
            "task_id": input_data.task_id,
            "status": "accepted",
            "message": f"Task {input_data.task_id} has been accepted by {self.agent.name}"
        }


class ResearchTool(Tool):
    """Tool for researching information."""
    name = "research"
    description = "Research information on a topic"
    
    async def execute(self, topic: str) -> Dict[str, Any]:
        """Execute the research."""
        # Simulate research by returning mock data
        research_data = {
            "topic": topic,
            "sources": [
                f"https://example.com/research/{topic.replace(' ', '_')}",
                f"https://en.wikipedia.org/wiki/{topic}"
            ],
            "summary": f"This is a summary of information about {topic}.",
            "key_points": [
                f"{topic} is an important topic in this field.",
                f"Recent developments in {topic} have been significant.",
                f"Experts agree that {topic} will continue to be relevant."
            ]
        }
        
        await asyncio.sleep(1)  # Simulate time to do research
        return research_data


class WritingTool(Tool):
    """Tool for writing content."""
    name = "write"
    description = "Write content based on provided information"
    
    async def execute(self, topic: str, points: List[str], style: str = "professional") -> Dict[str, Any]:
        """Write content based on the provided points."""
        # Simulate writing by formatting the points
        content = {
            "title": f"{topic.title()}: A Comprehensive Overview",
            "introduction": f"This document provides an overview of {topic}.",
            "sections": [
                {"heading": "Introduction", "content": f"{topic} is a fascinating subject that has many aspects to explore."},
                {"heading": "Key Points", "content": "\n- " + "\n- ".join(points)},
                {"heading": "Conclusion", "content": f"In conclusion, {topic} is an important area of study with many applications."}
            ],
            "style": style,
            "word_count": len(" ".join(points).split()) + 50  # Rough estimate
        }
        
        await asyncio.sleep(0.5)  # Simulate time to write
        return content


# Define our agent classes
class ManagerAgent(BaseAgent):
    """An agent that coordinates tasks between other agents."""
    
    def __init__(self, team: Dict[str, BaseAgent]):
        super().__init__(name="Manager", description="Coordinates the team")
        self.team = team
        self.add_tool(TaskAssignmentTool(self))
    
    async def process(self, input_text: str, **kwargs) -> str:
        """Process input and delegate tasks."""
        # Simple command parsing
        parts = input_text.split(" to ")
        if len(parts) < 2:
            return "Please specify a task and an agent. Example: 'research AI to researcher'"
        
        task = parts[0].strip()
        agent_name = parts[1].strip().lower()
        
        if agent_name not in self.team:
            return f"Unknown agent: {agent_name}. Available agents: {', '.join(self.team.keys())}"        
        # Create a task
        task_id = f"task_{len(self.conversation) + 1}"
        task_request = TaskRequest(
            task_id=task_id,
            description=task,
            priority=1
        )
        
        # Assign the task to the appropriate agent
        agent = self.team[agent_name]
        response = await agent.process(f"handle_task {task_request.json()}")
        
        return f"Task assigned to {agent_name}: {response}"


class ResearcherAgent(BaseAgent):
    """An agent that can research topics."""
    
    def __init__(self):
        super().__init__(name="Researcher", description="Researches information")
        self.add_tool(ResearchTool())
    
    async def process(self, input_text: str, **kwargs) -> str:
        """Process research requests."""
        if input_text.startswith("handle_task "):
            # Handle task assignment
            task_json = input_text[len("handle_task "):]
            task = TaskRequest.parse_raw(task_json)
            
            # Do the research
            research = await self.tools["research"].execute(task.description)
            
            # Format the response
            response = TaskResponse(
                task_id=task.task_id,
                status="completed",
                result={"research": research},
                message=f"Research on '{task.description}' completed successfully."
            )
            return response.json()
        
        return "I'm a researcher. Please assign me tasks through the manager."


class WriterAgent(BaseAgent):
    """An agent that can write content."""
    
    def __init__(self):
        super().__init__(name="Writer", description="Writes content")
        self.add_tool(WritingTool())
    
    async def process(self, input_text: str, **kwargs) -> str:
        """Process writing requests."""
        if input_text.startswith("handle_task "):
            # Handle task assignment
            task_json = input_text[len("handle_task "):]
            task = TaskRequest.parse_raw(task_json)
            
            # For simplicity, assume the task is to write about a topic with some points
            topic = task.description
            points = [
                f"{topic} has many interesting aspects.",
                f"The history of {topic} is fascinating.",
                f"There are many applications of {topic} in various fields."
            ]
            
            # Write the content
            content = await self.tools["write"].execute(
                topic=topic,
                points=points,
                style="professional"
            )
            
            # Format the response
            response = TaskResponse(
                task_id=task.task_id,
                status="completed",
                result={"content": content},
                message=f"Content about '{topic}' has been written."
            )
            return response.json()
        
        return "I'm a writer. Please assign me tasks through the manager."


async def main():
    """Run the multi-agent system example."""
    print("=== Multi-Agent System Example ===\n")
    
    # Create the agents
    researcher = ResearcherAgent()
    writer = WriterAgent()
    
    # Create the manager with the team
    manager = ManagerAgent({
        "researcher": researcher,
        "writer": writer
    })
    
    # Example interactions
    examples = [
        "research AI to researcher",
        "write a report on machine learning to writer",
        "analyze data to analyst"  # This agent doesn't exist
    ]
    
    for example in examples:
        print(f"\nYou: {example}")
        response = await manager.process(example)
        print(f"Manager: {response}")
    
    # Show how agents can be used directly
    print("\nDirect interaction with the researcher:")
    research = await researcher.tools["research"].execute("quantum computing")
    print(f"Research result: {research['summary']}")
    
    print("\nDirect interaction with the writer:")
    content = await writer.tools["write"].execute(
        topic="The Future of AI",
        points=[
            "AI is transforming industries.",
            "Ethical considerations are important.",
            "The future is full of possibilities."
        ]
    )
    print(f"Generated content: {content['title']}")
    print(f"Word count: {content['word_count']}")


if __name__ == "__main__":
    asyncio.run(main())
