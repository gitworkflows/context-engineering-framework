# Context Engineering Framework

A powerful framework for building and managing AI agents with context awareness. This framework provides the foundation for creating intelligent agents that can understand, process, and act upon contextual information.

> **Context is the key to building truly intelligent AI systems.**

## 🚀 Quick Start

1. **Install the package** (in development mode):
   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/context-engineering-framework.git
   cd context-engineering-framework
   
   # Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install the package in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```

2. **Run the CLI**:
   ```bash
   # Start the interactive shell
   cef run
   
   # Or use individual commands
   cef read README.md
   cef write example.txt "Hello, world!"
   ```

## 📚 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Development](#development)
  - [Setting Up](#setting-up)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
  - [CI/CD](#cicd)
- [Usage](#usage)
  - [Core Concepts](#core-concepts)
  - [Creating an Agent](#creating-an-agent)
  - [Using Tools](#using-tools)
  - [Context Management](#context-management)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

```
context-engineering-framework/
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
├── docs/                       # Documentation
├── examples/                   # Example usage
├── src/                        # Source code
│   ├── context_engineering_framework/
│   │   ├── core/              # Core framework components
│   │   │   ├── __init__.py
│   │   │   ├── agent.py       # Base agent implementation
│   │   │   ├── context.py     # Context management
│   │   │   └── tools.py       # Tool system
│   │   └── cli/               # Command-line interface
│   │       ├── __init__.py
│   │       └── main.py
│   └── tests/                 # Test suite
│       ├── core/              # Tests for core components
│       │   ├── test_agent.py
│       │   ├── test_context.py
│       │   └── test_tools.py
│       └── conftest.py        # Test configuration
├── .pre-commit-config.yaml    # Pre-commit hooks
├── Makefile                   # Common development tasks
├── pyproject.toml            # Project metadata and dependencies
└── README.md                 # This file
```

## Development

### Setting Up

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/context-engineering-framework.git
   cd context-engineering-framework
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package in development mode with all dependencies:
   ```bash
   pip install -e '.[dev]'
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

Run all tests with coverage:
```bash
make test
```

Run a specific test file:
```bash
pytest tests/core/test_agent.py -v
```

### Code Quality

Format code:
```bash
make format
```

Run linters:
```bash
make lint
```

### CI/CD

The project uses GitHub Actions for continuous integration. The workflow includes:
- Running tests on multiple Python versions
- Code coverage reporting
- Linting and type checking

## Features

- **Agent Framework**: Create and manage AI agents with custom behaviors
- **Tool System**: Build and use tools with input/output validation
- **Context Management**: Handle and merge context from multiple sources
- **CLI Interface**: Interact with the framework through a command-line interface
- **Extensible**: Easily add new agents, tools, and functionality
- **Type Annotations**: Full type hints for better development experience

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/context-engineering-framework.git
   cd context-engineering-framework
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

### Development Setup

For development, install the development dependencies:

```bash
pip install -e ".[dev]"
```

## Usage

### Core Concepts

The framework is built around several key concepts:

- **Agents**: Autonomous entities that can process information and perform actions
- **Tools**: Functions that agents can use to interact with the world
- **Context**: Information that agents use to make decisions
- **Messages**: Communication between agents and users

### Creating an Agent

```python
from src import BaseAgent

# Create a simple agent
agent = BaseAgent(name="DemoAgent", description="A demonstration agent")

# Process a message
response = await agent.process("Hello, world!")
print(response)
```

### Using Tools

```python
from src import BaseAgent, Tool

# Define a tool
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"

# Create an agent and add the tool
agent = BaseAgent(name="GreetingAgent")
agent.add_tool(greet)

# The agent can now use the tool
response = await agent.process("Greet Alice")
print(response)
```

### Context Management

```python
from src import ContextManager

# Create a context manager
ctx_mgr = ContextManager()

# Add context from different sources
ctx_mgr.add_source("defaults", {"app": {"name": "DemoApp", "version": "1.0.0"}})
ctx_mgr.add_source("user_prefs", {"theme": "dark", "notifications": True}, priority=10)

# Merge contexts
context = ctx_mgr.merge_contexts()
print(context)
```

## API Reference

### BaseAgent

The core agent class that provides the foundation for all agents.

#### Methods

- `process(input_text: str, **kwargs) -> str`: Process an input message and return a response
- `add_tool(tool: Union[Tool, Callable], **kwargs)`: Add a tool to the agent
- `remove_tool(name: str) -> bool`: Remove a tool by name
- `get_tool(name: str) -> Optional[Tool]`: Get a tool by name
- `list_tools() -> List[Dict[str, Any]]`: List all available tools
- `set_context(context: Dict[str, Any])`: Set the agent's context
- `get_context(key: str = None, default: Any = None)`: Get a value from the agent's context
- `reset()`: Reset the agent's conversation and state

### ContextManager

Manages context from multiple sources with priority-based merging.

#### Methods

- `add_source(name: str, content: Dict[str, Any], **kwargs)`: Add a context source
- `load_from_file(file_path: str, **kwargs)`: Load context from a JSON or YAML file
- `merge_contexts() -> Dict[str, Any]`: Merge all context sources based on priority
- `get_context(key: str = None, default: Any = None)`: Get a value from the merged context
- `validate_context(schema: Dict[str, Any]) -> bool`: Validate the context against a schema

### Tool

Base class for all tools.

#### Methods

- `validate_input(input_data: Dict[str, Any]) -> ToolInput`: Validate input data
- `validate_output(output_data: Dict[str, Any]) -> ToolOutput`: Validate output data
- `execute(**kwargs) -> ToolOutput`: Execute the tool with the given arguments
- `get_schema() -> Dict[str, Any]`: Get the OpenAPI schema for the tool

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes and add tests
4. Run the tests: `pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
- Like giving someone a sticky note

**Context Engineering:**
- A complete system for providing comprehensive context
- Includes documentation, examples, rules, patterns, and validation
- Like writing a full screenplay with all the details

### Why Context Engineering Matters

1. **Reduces AI Failures**: Most agent failures aren't model failures - they're context failures
2. **Ensures Consistency**: AI follows your project patterns and conventions
3. **Enables Complex Features**: AI can handle multi-step implementations with proper context
4. **Self-Correcting**: Validation loops allow AI to fix its own mistakes

## Template Structure

```
context-engineering-intro/
├── .claude/
│   ├── commands/
│   │   ├── generate-prp.md    # Generates comprehensive PRPs
│   │   └── execute-prp.md     # Executes PRPs to implement features
│   └── settings.local.json    # Claude Code permissions
├── PRPs/
│   ├── templates/
│   │   └── prp_base.md       # Base template for PRPs
│   └── EXAMPLE_multi_agent_prp.md  # Example of a complete PRP
├── examples/                  # Your code examples (critical!)
├── CLAUDE.md                 # Global rules for AI assistant
├── INITIAL.md               # Template for feature requests
├── INITIAL_EXAMPLE.md       # Example feature request
└── README.md                # This file
```

This template doesn't focus on RAG and tools with context engineering because I have a LOT more in store for that soon. ;)

## Step-by-Step Guide

### 1. Set Up Global Rules (CLAUDE.md)

The `CLAUDE.md` file contains project-wide rules that the AI assistant will follow in every conversation. The template includes:

- **Project awareness**: Reading planning docs, checking tasks
- **Code structure**: File size limits, module organization
- **Testing requirements**: Unit test patterns, coverage expectations
- **Style conventions**: Language preferences, formatting rules
- **Documentation standards**: Docstring formats, commenting practices

**You can use the provided template as-is or customize it for your project.**

### 2. Create Your Initial Feature Request

Edit `INITIAL.md` to describe what you want to build:

```markdown
## FEATURE:
[Describe what you want to build - be specific about functionality and requirements]

## EXAMPLES:
[List any example files in the examples/ folder and explain how they should be used]

## DOCUMENTATION:
[Include links to relevant documentation, APIs, or MCP server resources]

## OTHER CONSIDERATIONS:
[Mention any gotchas, specific requirements, or things AI assistants commonly miss]
```

**See `INITIAL_EXAMPLE.md` for a complete example.**

### 3. Generate the PRP

PRPs (Product Requirements Prompts) are comprehensive implementation blueprints that include:

- Complete context and documentation
- Implementation steps with validation
- Error handling patterns
- Test requirements

They are similar to PRDs (Product Requirements Documents) but are crafted more specifically to instruct an AI coding assistant.

Run in Claude Code:
```bash
/generate-prp INITIAL.md
```

**Note:** The slash commands are custom commands defined in `.claude/commands/`. You can view their implementation:
- `.claude/commands/generate-prp.md` - See how it researches and creates PRPs
- `.claude/commands/execute-prp.md` - See how it implements features from PRPs

The `$ARGUMENTS` variable in these commands receives whatever you pass after the command name (e.g., `INITIAL.md` or `PRPs/your-feature.md`).

This command will:
1. Read your feature request
2. Research the codebase for patterns
3. Search for relevant documentation
4. Create a comprehensive PRP in `PRPs/your-feature-name.md`

### 4. Execute the PRP

Once generated, execute the PRP to implement your feature:

```bash
/execute-prp PRPs/your-feature-name.md
```

The AI coding assistant will:
1. Read all context from the PRP
2. Create a detailed implementation plan
3. Execute each step with validation
4. Run tests and fix any issues
5. Ensure all success criteria are met

## Writing Effective INITIAL.md Files

### Key Sections Explained

**FEATURE**: Be specific and comprehensive
- ❌ "Build a web scraper"
- ✅ "Build an async web scraper using BeautifulSoup that extracts product data from e-commerce sites, handles rate limiting, and stores results in PostgreSQL"

**EXAMPLES**: Leverage the examples/ folder
- Place relevant code patterns in `examples/`
- Reference specific files and patterns to follow
- Explain what aspects should be mimicked

**DOCUMENTATION**: Include all relevant resources
- API documentation URLs
- Library guides
- MCP server documentation
- Database schemas

**OTHER CONSIDERATIONS**: Capture important details
- Authentication requirements
- Rate limits or quotas
- Common pitfalls
- Performance requirements

## The PRP Workflow

### How /generate-prp Works

The command follows this process:

1. **Research Phase**
   - Analyzes your codebase for patterns
   - Searches for similar implementations
   - Identifies conventions to follow

2. **Documentation Gathering**
   - Fetches relevant API docs
   - Includes library documentation
   - Adds gotchas and quirks

3. **Blueprint Creation**
   - Creates step-by-step implementation plan
   - Includes validation gates
   - Adds test requirements

4. **Quality Check**
   - Scores confidence level (1-10)
   - Ensures all context is included

### How /execute-prp Works

1. **Load Context**: Reads the entire PRP
2. **Plan**: Creates detailed task list using TodoWrite
3. **Execute**: Implements each component
4. **Validate**: Runs tests and linting
5. **Iterate**: Fixes any issues found
6. **Complete**: Ensures all requirements met

See `PRPs/EXAMPLE_multi_agent_prp.md` for a complete example of what gets generated.

## Using Examples Effectively

The `examples/` folder is **critical** for success. AI coding assistants perform much better when they can see patterns to follow.

### What to Include in Examples

1. **Code Structure Patterns**
   - How you organize modules
   - Import conventions
   - Class/function patterns

2. **Testing Patterns**
   - Test file structure
   - Mocking approaches
   - Assertion styles

3. **Integration Patterns**
   - API client implementations
   - Database connections
   - Authentication flows

4. **CLI Patterns**
   - Argument parsing
   - Output formatting
   - Error handling

### Example Structure

```
examples/
├── README.md           # Explains what each example demonstrates
├── cli.py             # CLI implementation pattern
├── agent/             # Agent architecture patterns
│   ├── agent.py      # Agent creation pattern
│   ├── tools.py      # Tool implementation pattern
│   └── providers.py  # Multi-provider pattern
└── tests/            # Testing patterns
    ├── test_agent.py # Unit test patterns
    └── conftest.py   # Pytest configuration
```

## Best Practices

### 1. Be Explicit in INITIAL.md
- Don't assume the AI knows your preferences
- Include specific requirements and constraints
- Reference examples liberally

### 2. Provide Comprehensive Examples
- More examples = better implementations
- Show both what to do AND what not to do
- Include error handling patterns

### 3. Use Validation Gates
- PRPs include test commands that must pass
- AI will iterate until all validations succeed
- This ensures working code on first try

### 4. Leverage Documentation
- Include official API docs
- Add MCP server resources
- Reference specific documentation sections

### 5. Customize CLAUDE.md
- Add your conventions
- Include project-specific rules
- Define coding standards

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Context Engineering Best Practices](https://www.philschmid.de/context-engineering)