"""Native function registry."""

from typing import Dict, Optional


class NativeRegistry:
    """Registry for native functions."""

    def __init__(self):
        self._functions: Dict[str, object] = {}

    def register(self, native_function):
        """Register a native function."""
        self._functions[native_function.name] = native_function

    def get(self, name: str) -> Optional[object]:
        """Get a native function by name."""
        return self._functions.get(name)

    def get_all(self) -> Dict[str, object]:
        """Get all registered native functions."""
        return self._functions.copy()