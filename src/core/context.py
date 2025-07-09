"""
Core context management for the Context Engineering Framework.
Handles loading, merging, and validating context from multiple sources.
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import yaml
from pydantic import BaseModel, Field, ValidationError


class ContextSource(BaseModel):
    """Represents a single source of context."""
    name: str
    content: Dict[str, Any]
    priority: int = 0
    source_type: str = "unknown"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ContextManager:
    """Manages context from multiple sources with priority-based merging."""
    
    def __init__(self):
        self.sources: List[ContextSource] = []
        self.context: Dict[str, Any] = {}
    
    def add_source(self, name: str, content: Dict[str, Any], 
                 priority: int = 0, source_type: str = "unknown",
                 metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add a new context source.
        
        Args:
            name: Unique identifier for the source
            content: Dictionary containing the context data
            priority: Higher priority sources override lower ones
            source_type: Type/category of the source
            metadata: Additional metadata about the source
        """
        if metadata is None:
            metadata = {}
            
        self.sources.append(
            ContextSource(
                name=name,
                content=content,
                priority=priority,
                source_type=source_type,
                metadata=metadata
            )
        )
    
    def load_from_file(self, file_path: str, priority: int = 0) -> None:
        """Load context from a JSON or YAML file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Context file not found: {file_path}")
            
        try:
            if path.suffix.lower() in ('.json',):
                with open(path, 'r') as f:
                    content = json.load(f)
            elif path.suffix.lower() in ('.yaml', '.yml'):
                with open(path, 'r') as f:
                    content = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
                
            self.add_source(
                name=path.name,
                content=content,
                priority=priority,
                source_type="file",
                metadata={"path": str(path.absolute())}
            )
        except Exception as e:
            raise ValueError(f"Failed to load context from {file_path}: {str(e)}")
    
    def merge_contexts(self) -> Dict[str, Any]:
        """Merge all context sources based on priority."""
        # Sort sources by priority (highest first)
        sorted_sources = sorted(
            self.sources, 
            key=lambda x: x.priority, 
            reverse=True
        )
        
        # Merge contexts, with higher priority sources overriding lower ones
        merged = {}
        for source in sorted_sources:
            self._deep_merge(merged, source.content)
            
        self.context = merged
        return self.context
    
    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Recursively merge source dictionary into target."""
        for key, value in source.items():
            if (key in target and 
                isinstance(target[key], dict) and 
                isinstance(value, dict)):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def get_context(self, key: str = None, default: Any = None) -> Any:
        """Get context value by dot-notation key."""
        if not self.context:
            self.merge_contexts()
            
        if key is None:
            return self.context
            
        keys = key.split('.')
        value = self.context
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def validate_context(self, schema: Dict[str, Any]) -> bool:
        """Validate the current context against a schema."""
        # This is a placeholder for schema validation logic
        # In a real implementation, this would use JSON Schema or similar
        return True  # Simplified for now


# Example usage
if __name__ == "__main__":
    # Create a context manager
    ctx_mgr = ContextManager()
    
    # Add some context sources
    ctx_mgr.add_source(
        name="defaults",
        content={"app": {"name": "ContextEngine", "version": "0.1.0"}},
        priority=0
    )
    
    ctx_mgr.add_source(
        name="user_prefs",
        content={"app": {"theme": "dark", "notifications": True}},
        priority=10
    )
    
    # Merge and get context
    context = ctx_mgr.merge_contexts()
    print("Merged context:", context)
    
    # Get specific value
    print("App name:", ctx_mgr.get_context("app.name"))
