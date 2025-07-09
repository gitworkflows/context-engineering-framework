.. _getting_started:

Getting Started
==============

This guide will help you get started with the Context Engineering Framework.

Quick Start
-----------

Here's a simple example to get you started:

.. code-block:: python

    from context_engineering_framework import ContextManager, BaseAgent

    # Initialize the context manager
    context_manager = ContextManager()
    
    # Create a simple agent
    class MyAgent(BaseAgent):
        def __init__(self):
            super().__init__(name="MyAgent", description="A simple agent")
        
        async def process(self, input_text: str, **kwargs) -> str:
            return f"You said: {input_text}"
    
    # Create and run the agent
    agent = MyAgent()
    response = await agent.process("Hello, World!")
    print(response)  # Output: You said: Hello, World!

Core Concepts
-------------

Agents
~~~~~~
Agents are the main building blocks of the framework. They can process input, maintain state, and interact with other agents.

Context
~~~~~~~
Context provides agents with information about their environment and the current state of the system.

Tools
~~~~~
Tools are functions that agents can use to perform specific tasks. They can be registered with agents to extend their capabilities.

Messages
~~~~~~~~
Messages are used for communication between agents. They can contain text, data, or any other type of information.

Basic Usage
-----------

Creating an Agent
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from context_engineering_framework import BaseAgent

    class MyAgent(BaseAgent):
        def __init__(self):
            super().__init__(name="MyAgent", description="My custom agent")
        
        async def process(self, input_text: str, **kwargs) -> str:
            # Process the input and return a response
            return f"Processed: {input_text}"

Using the Context Manager
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from context_engineering_framework import ContextManager

    # Initialize the context manager
    context_manager = ContextManager()
    
    # Add some context
    context_manager.add_context({"user": {"name": "John", "role": "admin"}})
    
    # Get the current context
    context = context_manager.get_context()
    print(context["user"]["name"])  # Output: John

Creating and Using Tools
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from context_engineering_framework import BaseTool, BaseAgent
    from pydantic import BaseModel

    # Define input and output models
    class GreetInput(BaseModel):
        name: str

    class GreetOutput(BaseModel):
        greeting: str

    # Create a custom tool
    class GreetTool(BaseTool):
        name = "greet"
        description = "Generate a greeting"
        input_model = GreetInput
        output_model = GreetOutput
        
        async def execute(self, input_data: GreetInput) -> GreetOutput:
            return GreetOutput(greeting=f"Hello, {input_data.name}!")
    
    # Create an agent and register the tool
    agent = BaseAgent(name="Greeter")
    greet_tool = GreetTool()
    agent.add_tool(greet_tool)
    
    # Use the tool
    result = await agent.tools["greet"].execute(GreetInput(name="Alice"))
    print(result.greeting)  # Output: Hello, Alice!

Next Steps
----------

- Learn more about :ref:`user_guide`
- Explore the :ref:`api_reference`
- Check out the :ref:`examples` for more advanced usage
