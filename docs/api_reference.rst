.. _api_reference:

API Reference
============

This document provides detailed documentation for the Context Engineering Framework's API.

Core Modules
------------

.. toctree::
   :maxdepth: 2

   api/agent
   api/context
   api/tools
   api/messages
   api/exceptions

Core Classes
------------

.. autosummary::
   :toctree: _autosummary
   :template: custom-module-template.rst
   :recursive:

   context_engineering_framework.agent
   context_engineering_framework.context
   context_engineering_framework.tools
   context_engineering_framework.messages

Base Classes
------------

.. autoclass:: context_engineering_framework.agent.BaseAgent
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: context_engineering_framework.context.ContextManager
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: context_engineering_framework.tools.BaseTool
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: context_engineering_framework.messages.Message
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
----------

.. autoexception:: context_engineering_framework.exceptions.ContextError
   :members:

.. autoexception:: context_engineering_framework.exceptions.ToolError
   :members:

.. autoexception:: context_engineering_framework.exceptions.ValidationError
   :members:

CLI Reference
-------------

The framework includes a command-line interface (CLI) for common tasks.

.. click:: context_engineering_framework.cli:main
   :prog: cef
   :nested: full

Utilities
---------

.. automodule:: context_engineering_framework.utils
   :members:
   :undoc-members:
   :show-inheritance:

Type Definitions
----------------

.. automodule:: context_engineering_framework.types
   :members:
   :undoc-members:
   :show-inheritance:

Constants
---------

.. automodule:: context_engineering_framework.constants
   :members:
   :undoc-members:
   :show-inheritance:

Version
-------

.. automodule:: context_engineering_framework.version
   :members:
   :undoc-members:
   :show-inheritance:
