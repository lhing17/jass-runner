"""Native function base class."""

from abc import ABC, abstractmethod


class NativeFunction(ABC):
    """Abstract base class for JASS native functions."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the native function."""
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the native function with given arguments."""
        pass