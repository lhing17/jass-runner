"""Expression evaluator for JASS."""

from typing import Any
from .context import ExecutionContext


class Evaluator:
    """Evaluates JASS expressions."""

    def __init__(self, context: ExecutionContext):
        self.context = context

    def evaluate(self, expression: str) -> Any:
        """Evaluate a JASS expression."""
        expression = expression.strip()

        # Handle string literals
        if expression.startswith('"') and expression.endswith('"'):
            return expression[1:-1]

        # Handle integer literals
        if expression.isdigit():
            return int(expression)

        # Handle float literals
        try:
            return float(expression)
        except ValueError:
            pass

        # Handle variable references
        if self.context.has_variable(expression):
            return self.context.get_variable(expression)

        # Default: return as string
        return expression