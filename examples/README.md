# Examples

This directory contains example code that demonstrates how to use the Context Engineering Framework.

## Getting Started

To run the examples, first install the package in development mode:

```bash
pip install -e .
```

Then navigate to the examples directory and run the Python scripts:

```bash
cd examples
python basic_agent.py
```

## Available Examples

### Basic Examples

- `basic_agent.py`: A simple example of creating and using a basic agent
- `context_management.py`: Demonstrates how to use the context manager
- `custom_tools.py`: Shows how to create and use custom tools
- `message_passing.py`: Example of message passing between agents

### Advanced Examples

- `multi_agent_system.py`: Demonstrates a system with multiple interacting agents
- `web_integration.py`: Shows how to integrate the framework with a web server
- `persistence.py`: Example of saving and loading agent state

## Running Tests for Examples

To run the example tests:

```bash
pytest tests/test_examples.py -v
```

## Contributing

If you'd like to contribute an example, please follow these guidelines:

1. Keep examples focused and simple
2. Include comments explaining the code
3. Add a brief description in this README
4. Ensure the example follows the project's coding standards
5. Add tests if appropriate

## Need Help?

If you have any questions about the examples or how to use the framework, please open an issue on GitHub.
