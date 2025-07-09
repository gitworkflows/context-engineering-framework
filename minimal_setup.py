from setuptools import setup, find_packages

setup(
    name="context-engineering-framework",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "typing-extensions>=4.0.0",
        "pyyaml>=6.0.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "mypy>=1.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.20.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "cef=cli.main:main",
        ],
    },
)
