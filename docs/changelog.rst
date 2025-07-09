.. _changelog:

Changelog
=========

All notable changes to the Context Engineering Framework will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. include:: ../CHANGELOG.md
   :start-line: 2

Older Versions
--------------

For changes in versions prior to 0.1.0, please see the `GitHub releases page <https://github.com/yourusername/context-engineering-framework/releases>`_.

Versioning Policy
-----------------

This project follows `Semantic Versioning 2.0.0 <https://semver.org/>`_.

- **MAJOR** version when you make incompatible API changes
- **MINOR** version when you add functionality in a backward-compatible manner
- **PATCH** version when you make backward-compatible bug fixes

Deprecation Policy
------------------

- The deprecation period will be at least one minor version
- Deprecated features will raise a `DeprecationWarning`
- The documentation will clearly mark deprecated features
- Migration guides will be provided when possible

Security Fixes
--------------

Security fixes will be backported to the last minor version and released as a patch update.

For security issues, please see our :ref:`security` policy.

Contributing to the Changelog
----------------------------

When making changes to the project, please update the changelog as part of your pull request. Follow these guidelines:

1. Add your changes to the "Unreleased" section if they're not yet in a release
2. Group changes by type (Added, Changed, Deprecated, Removed, Fixed, Security)
3. Include links to issues or pull requests when applicable
4. Follow the existing format and style

Example:

.. code-block:: markdown

   ## [Unreleased]
   
   ### Added
   - New feature that does something cool (#123)
   
   ### Fixed
   - Fixed a bug that caused crashes (#124)

When creating a new release, the "Unreleased" section will be moved to a new version number.
