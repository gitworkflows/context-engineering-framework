# Contributing to Context Engineering Framework

Thank you for your interest in contributing to the Context Engineering Framework! We welcome contributions from everyone, whether you're a developer, designer, or just someone who wants to help improve the project.

## How to Contribute

### Reporting Bugs

1. **Check Existing Issues**: Before creating a new issue, please check if the bug has already been reported.
2. **Create a New Issue**: If you've found a new bug, please create a new issue with a clear title and description. Include steps to reproduce the bug, expected behavior, and actual behavior.
3. **Provide Details**: Include your Python version, operating system, and any relevant error messages or logs.

### Suggesting Enhancements

1. **Check Existing Enhancements**: Before suggesting a new feature or enhancement, please check if it has already been suggested.
2. **Create a New Issue**: If you have an idea for an enhancement, create a new issue with a clear title and description. Explain why you think this enhancement would be valuable.

### Submitting Code Changes

1. **Fork the Repository**: Click the "Fork" button in the top-right corner of the repository page.
2. **Create a Branch**: Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**: Make your changes following the project's coding standards.
4. **Run Tests**: Ensure all tests pass:
   ```bash
   pytest
   ```
5. **Commit Your Changes**: Write clear, concise commit messages:
   ```bash
   git commit -m "Add your commit message here"
   ```
6. **Push to Your Fork**: Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**: Open a pull request from your fork to the main repository.

## Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/context-engineering-framework.git
   cd context-engineering-framework
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -e .[dev]
   ```

4. **Run Tests**:
   ```bash
   pytest
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use type hints for all function and method signatures.
- Write docstrings for all public modules, classes, and functions following the Google style guide.
- Keep lines under 88 characters (Black's default).

## Testing

- Write tests for all new features and bug fixes.
- Ensure all tests pass before submitting a pull request.
- If you're fixing a bug, add a test that would have caught the bug.

## Documentation

- Update the documentation when adding new features or changing existing behavior.
- Ensure all public APIs are well-documented.
- Add examples where appropriate.

## Code Review Process

1. A maintainer will review your pull request.
2. The reviewer may request changes. Please address these promptly.
3. Once approved, a maintainer will merge your changes.

## Questions?

If you have any questions, feel free to open an issue or reach out to the maintainers.
