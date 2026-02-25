"""JASS interpreter."""

from typing import Any
from .context import ExecutionContext
from .evaluator import Evaluator
from ..parser.parser import AST, FunctionDecl, LocalDecl


class Interpreter:
    """Interprets and executes JASS AST."""

    def __init__(self):
        self.global_context = ExecutionContext()
        self.current_context = self.global_context
        self.functions = {}

    def execute(self, ast: AST):
        """Execute the AST."""
        # Register all functions
        for func in ast.functions:
            self.functions[func.name] = func

        # Find and execute main function
        if 'main' in self.functions:
            self.execute_function(self.functions['main'])

    def execute_function(self, func: FunctionDecl):
        """Execute a function."""
        # Create new context for function execution
        func_context = ExecutionContext(self.global_context)
        self.current_context = func_context

        # Execute function body
        if func.body:
            for statement in func.body:
                self.execute_statement(statement)

        # Restore previous context
        self.current_context = self.global_context

    def execute_statement(self, statement: Any):
        """Execute a single statement."""
        if isinstance(statement, LocalDecl):
            self.execute_local_declaration(statement)

    def execute_local_declaration(self, decl: LocalDecl):
        """Execute a local variable declaration."""
        # Set the variable in current context
        self.current_context.set_variable(decl.name, decl.value)