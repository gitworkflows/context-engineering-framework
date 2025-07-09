.. _installation:

Installation
============

Prerequisites
------------

- Python 3.8 or higher
- pip (Python package installer)

Install from PyPI (Recommended)
------------------------------

.. code-block:: bash

    pip install context-engineering-framework

Install from source
-------------------

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/yourusername/context-engineering-framework.git
       cd context-engineering-framework

2. Install the package in development mode:

   .. code-block:: bash

       pip install -e .[dev]

   This will install all dependencies, including development tools.

Verify Installation
------------------

To verify that the package is installed correctly, you can run:

.. code-block:: bash

    python -c "import context_engineering_framework; print(context_engineering_framework.__version__)"

You should see the version number printed to the console.

Docker
------

You can also run the framework using Docker:

.. code-block:: bash

    # Build the Docker image
    docker-compose build

    # Run the application
    docker-compose up

Development Setup
----------------

If you plan to contribute to the project, you'll need to set up your development environment:

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up a virtual environment:

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # On Windows: venv\Scripts\activate

4. Install development dependencies:

   .. code-block:: bash

       pip install -e .[dev]
       pre-commit install

5. Run the tests to make sure everything is working:

   .. code-block:: bash

       pytest

Next Steps
----------

- :ref:`getting_started` - Get started with the framework
- :ref:`user_guide` - Learn how to use the framework
- :ref:`api_reference` - Detailed API documentation
