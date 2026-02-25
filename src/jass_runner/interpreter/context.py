"""Execution context for JASS interpreter."""

from typing import Dict, Any, Optional


class ExecutionContext:
    """Represents an execution context with variable scope."""

    def __init__(self, parent: Optional['ExecutionContext'] = None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent

    def set_variable(self, name: str, value: Any):
        """Set a variable in this context."""
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """Get a variable from this context or parent contexts."""
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Variable '{name}' not found")

    def has_variable(self, name: str) -> bool:
        """Check if variable exists in this or parent contexts."""
        if name in self.variables:
            return True
        elif self.parent:
            return self.parent.has_variable(name)
        else:
            return False