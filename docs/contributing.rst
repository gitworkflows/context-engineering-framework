.. _contributing:

Contributing
============

We welcome contributions from the community! This guide will help you get started with contributing to the Context Engineering Framework.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   contributing/code_of_conduct
   contributing/setup
   contributing/development_workflow
   contributing/coding_standards
   contributing/documentation
   contributing/testing
   contributing/pull_requests
   contributing/release_process

Ways to Contribute
------------------

There are many ways to contribute to the project:

- **Bug Reports**: File an issue on GitHub if you find a bug
- **Feature Requests**: Suggest new features or improvements
- **Documentation**: Improve documentation, fix typos, or add examples
- **Code**: Submit bug fixes, new features, or performance improvements
- **Testing**: Help improve test coverage or report edge cases
- **Community**: Help answer questions on GitHub Discussions or Stack Overflow

Getting Started
---------------

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. Set up a **development environment** (see :ref:`setup`)
4. Create a **branch** for your changes
5. Make your changes and **test** them
6. Submit a **pull request** (see :ref:`pull_requests`)

Development Workflow
--------------------

1. **Create an issue** describing the bug or feature
2. **Assign the issue** to yourself if you're working on it
3. **Create a branch** for your changes
4. **Make your changes** following the coding standards
5. **Write tests** for your changes
6. **Run the tests** and ensure they pass
7. **Update the documentation** if needed
8. **Commit your changes** with a clear message
9. **Push your changes** to your fork
10. **Open a pull request** against the main branch

Coding Standards
----------------

- Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ for Python code
- Use type hints for all function signatures
- Write docstrings following the Google style guide
- Keep lines under 88 characters (Black's default)
- Run the linters and formatters before committing

Testing
-------

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Run the full test suite before pushing changes
- Add tests for any new functionality

Documentation
-------------

- Update the documentation when adding new features or changing behavior
- Add docstrings for all public modules, classes, and functions
- Include examples in docstrings where appropriate
- Update the user guide and API reference as needed

Pull Requests
-------------

- Keep pull requests focused on a single feature or bug fix
- Write a clear description of the changes
- Reference any related issues
- Ensure all tests pass and code coverage remains high
- Request reviews from maintainers when ready

Code Review
-----------

All contributions go through code review. Here's what to expect:

1. A maintainer will review your pull request
2. They may request changes or suggest improvements
3. Once approved, your changes will be merged

Release Process
---------------

1. Update the version number in the appropriate files
2. Update the changelog with the new version
3. Create a release tag
4. Publish the package to PyPI
5. Update the documentation

Getting Help
------------

If you need help at any point:

1. Check the documentation
2. Search the GitHub issues
3. Open a new issue if your question hasn't been answered

Thank you for contributing to the Context Engineering Framework!
