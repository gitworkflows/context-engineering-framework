"""Pytest configuration and fixtures for tests."""
import pytest
from pathlib import Path
import sys

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Common fixtures can be defined here
@pytest.fixture
def sample_context():
    """Return a sample context dictionary for testing."""
    return {
        "user": {"name": "Test User", "id": "123"},
        "session": {"id": "session_123", "start_time": "2023-01-01T00:00:00Z"}
    }
