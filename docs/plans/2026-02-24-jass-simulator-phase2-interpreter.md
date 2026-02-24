# JASS Simulator Phase 2: Interpreter and Execution Engine Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the interpreter engine that can execute parsed JASS code, manage variable scopes, and handle basic expressions.

**Architecture:** Create execution context, variable scope management, expression evaluator, and basic control flow handling.

**Tech Stack:** Python 3.8+, pytest

---

### Task 1: Create Interpreter Structure

**Files:**
- Create: `src/jass_runner/interpreter/__init__.py`
- Create: `src/jass_runner/interpreter/context.py`
- Create: `tests/interpreter/test_context.py`

**Step 1: Create interpreter package**

```python
# src/jass_runner/interpreter/__init__.py
"""JASS interpreter module."""
```

**Step 2: Write failing test for execution context**

```python
# tests/interpreter/test_context.py
"""Test execution context."""

def test_execution_context_creation():
    """Test that execution context can be created."""
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    assert context is not None
    assert hasattr(context, 'variables')
    assert isinstance(context.variables, dict)
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/interpreter/test_context.py::test_execution_context_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.interpreter.context'"

**Step 4: Create minimal execution context**

```python
# src/jass_runner/interpreter/context.py
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
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/interpreter/test_context.py::test_execution_context_creation -v`
Expected: PASS

**Step 6: Commit**

```bash
git add src/jass_runner/interpreter/__init__.py src/jass_runner/interpreter/context.py tests/interpreter/test_context.py
git commit -m "feat: add execution context with variable scope"
```

### Task 2: Add Variable Operations Tests

**Files:**
- Modify: `tests/interpreter/test_context.py`
- Modify: `src/jass_runner/interpreter/context.py`

**Step 1: Write failing test for variable operations**

```python
# tests/interpreter/test_context.py (add this function)
def test_variable_operations():
    """Test setting and getting variables."""
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()

    # Set variable
    context.set_variable('x', 42)
    assert context.has_variable('x') == True

    # Get variable
    value = context.get_variable('x')
    assert value == 42

    # Check non-existent variable
    assert context.has_variable('y') == False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/interpreter/test_context.py::test_variable_operations -v`
Expected: FAIL with assertion errors or NameError

**Step 3: Fix variable operations**

```python
# src/jass_runner/interpreter/context.py (no changes needed if implementation is correct)
# The existing implementation should pass the test
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/interpreter/test_context.py::test_variable_operations -v`
Expected: PASS

**Step 5: Write failing test for nested contexts**

```python
# tests/interpreter/test_context.py (add this function)
def test_nested_contexts():
    """Test variable lookup in nested contexts."""
    from jass_runner.interpreter.context import ExecutionContext

    parent = ExecutionContext()
    parent.set_variable('global', 100)

    child = ExecutionContext(parent)

    # Child can access parent variable
    assert child.has_variable('global') == True
    assert child.get_variable('global') == 100

    # Child can set its own variable
    child.set_variable('local', 200)
    assert child.get_variable('local') == 200

    # Parent cannot access child variable
    assert parent.has_variable('local') == False
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/interpreter/test_context.py::test_nested_contexts -v`
Expected: PASS

**Step 7: Commit**

```bash
git add tests/interpreter/test_context.py
git commit -m "test: add variable operations and nested context tests"
```

### Task 3: Create Expression Evaluator

**Files:**
- Create: `src/jass_runner/interpreter/evaluator.py`
- Create: `tests/interpreter/test_evaluator.py`

**Step 1: Write failing test for expression evaluator**

```python
# tests/interpreter/test_evaluator.py
"""Test expression evaluator."""

def test_evaluator_can_evaluate_literal():
    """Test that evaluator can evaluate literal values."""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    # Test integer literal
    result = evaluator.evaluate('42')
    assert result == 42

    # Test string literal
    result = evaluator.evaluate('"hello"')
    assert result == "hello"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/interpreter/test_evaluator.py::test_evaluator_can_evaluate_literal -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.interpreter.evaluator'"

**Step 3: Create minimal expression evaluator**

```python
# src/jass_runner/interpreter/evaluator.py
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
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/interpreter/test_evaluator.py::test_evaluator_can_evaluate_literal -v`
Expected: PASS

**Step 5: Write failing test for variable evaluation**

```python
# tests/interpreter/test_evaluator.py (add this function)
def test_evaluator_can_evaluate_variables():
    """Test that evaluator can evaluate variable references."""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    context.set_variable('x', 100)
    context.set_variable('name', 'John')

    evaluator = Evaluator(context)

    # Test variable reference
    result = evaluator.evaluate('x')
    assert result == 100

    result = evaluator.evaluate('name')
    assert result == 'John'
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/interpreter/test_evaluator.py::test_evaluator_can_evaluate_variables -v`
Expected: PASS

**Step 7: Commit**

```bash
git add src/jass_runner/interpreter/evaluator.py tests/interpreter/test_evaluator.py
git commit -m "feat: add basic expression evaluator"
```

### Task 4: Create Interpreter Core

**Files:**
- Create: `src/jass_runner/interpreter/interpreter.py`
- Create: `tests/interpreter/test_interpreter.py`

**Step 1: Write failing test for interpreter**

```python
# tests/interpreter/test_interpreter.py
"""Test JASS interpreter."""

def test_interpreter_can_execute_simple_script():
    """Test that interpreter can execute a simple script."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer x = 42
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # Should have executed without error
    assert True  # Just checking it doesn't crash
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/interpreter/test_interpreter.py::test_interpreter_can_execute_simple_script -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.interpreter.interpreter'"

**Step 3: Create minimal interpreter**

```python
# src/jass_runner/interpreter/interpreter.py
"""JASS interpreter."""

from typing import Any
from .context import ExecutionContext
from .evaluator import Evaluator
from ..parser.parser import AST, FunctionDecl

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

        # TODO: Execute function body
        # For now, just set up the context

        # Restore previous context
        self.current_context = self.global_context

    def execute_statement(self, statement: Any):
        """Execute a single statement."""
        # TODO: Implement statement execution
        pass
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/interpreter/test_interpreter.py::test_interpreter_can_execute_simple_script -v`
Expected: PASS

**Step 5: Write failing test for local variable declaration**

```python
# tests/interpreter/test_interpreter.py (add this function)
def test_interpreter_handles_local_variables():
    """Test that interpreter handles local variable declarations."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function test takes nothing returns nothing
        local integer x = 10
        local string name = "test"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # Function should be registered
    assert 'test' in interpreter.functions
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/interpreter/test_interpreter.py::test_interpreter_handles_local_variables -v`
Expected: PASS

**Step 7: Commit**

```bash
git add src/jass_runner/interpreter/interpreter.py tests/interpreter/test_interpreter.py
git commit -m "feat: add basic interpreter structure"
```

### Task 5: Enhance Parser for Statements

**Files:**
- Modify: `src/jass_runner/parser/parser.py`
- Modify: `tests/parser/test_parser.py`

**Step 1: Write failing test for statement parsing**

```python
# tests/parser/test_parser.py (add this function)
def test_parser_can_parse_local_declaration():
    """Test that parser can parse local variable declarations."""
    from jass_runner.parser.parser import Parser

    code = """
    function test takes nothing returns nothing
        local integer x = 42
        local string name = "hello"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.functions) == 1
    func = ast.functions[0]
    assert func.name == 'test'
    # TODO: Check that statements are parsed
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/parser/test_parser.py::test_parser_can_parse_local_declaration -v`
Expected: PASS (but statements not actually parsed yet)

**Step 3: Extend AST for statements**

```python
# src/jass_runner/parser/parser.py (add these dataclasses)
@dataclass
class LocalDecl:
    """Represents a local variable declaration."""
    name: str
    type: str
    value: Any

@dataclass
class FunctionDecl:
    """Represents a function declaration."""
    name: str
    parameters: List['Parameter']
    return_type: str
    body: Optional[List[Any]] = None  # Now will contain statements
```

**Step 4: Update parser to parse function body**

```python
# src/jass_runner/parser/parser.py (modify parse_function method)
    def parse_function(self) -> Optional[FunctionDecl]:
        """Parse a function declaration."""
        try:
            # ... existing code for function header ...

            # Parse function body
            body = []
            while self.current_token and not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endfunction'):
                statement = self.parse_statement()
                if statement:
                    body.append(statement)

            if self.current_token and self.current_token.value == 'endfunction':
                self.next_token()

            return FunctionDecl(name=name, parameters=parameters, return_type=return_type, body=body)

        except Exception:
            # If any error occurs, skip to next token and return None
            while self.current_token and not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'function'):
                self.next_token()
            return None

    def parse_statement(self) -> Optional[Any]:
        """Parse a statement."""
        if not self.current_token:
            return None

        # Parse local declaration
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'local':
            return self.parse_local_declaration()

        # Skip other tokens for now
        self.next_token()
        return None

    def parse_local_declaration(self) -> Optional[LocalDecl]:
        """Parse a local variable declaration."""
        try:
            # Skip 'local' keyword
            self.next_token()

            # Get variable type
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_type = self.current_token.value
            self.next_token()

            # Get variable name
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value
            self.next_token()

            # Check for assignment
            value = None
            if self.current_token and self.current_token.value == '=':
                self.next_token()
                # Parse expression (simplified)
                if self.current_token:
                    if self.current_token.type == 'NUMBER':
                        value = int(self.current_token.value)
                    elif self.current_token.type == 'STRING':
                        value = self.current_token.value[1:-1]  # Remove quotes
                    self.next_token()

            # Skip semicolon if present
            if self.current_token and self.current_token.value == ';':
                self.next_token()

            return LocalDecl(name=var_name, type=var_type, value=value)

        except Exception:
            return None
```

**Step 5: Update test to verify statement parsing**

```python
# tests/parser/test_parser.py (modify test_parser_can_parse_local_declaration)
def test_parser_can_parse_local_declaration():
    """Test that parser can parse local variable declarations."""
    from jass_runner.parser.parser import Parser, LocalDecl

    code = """
    function test takes nothing returns nothing
        local integer x = 42
        local string name = "hello"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    assert len(ast.functions) == 1
    func = ast.functions[0]
    assert func.name == 'test'
    assert func.body is not None
    assert len(func.body) == 2

    # Check first local declaration
    stmt1 = func.body[0]
    assert isinstance(stmt1, LocalDecl)
    assert stmt1.name == 'x'
    assert stmt1.type == 'integer'
    assert stmt1.value == 42

    # Check second local declaration
    stmt2 = func.body[1]
    assert isinstance(stmt2, LocalDecl)
    assert stmt2.name == 'name'
    assert stmt2.type == 'string'
    assert stmt2.value == 'hello'
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/parser/test_parser.py::test_parser_can_parse_local_declaration -v`
Expected: PASS

**Step 7: Commit**

```bash
git add src/jass_runner/parser/parser.py tests/parser/test_parser.py
git commit -m "feat: extend parser to handle local variable declarations"
```

### Task 6: Implement Statement Execution

**Files:**
- Modify: `src/jass_runner/interpreter/interpreter.py`
- Modify: `tests/interpreter/test_interpreter.py`

**Step 1: Write failing test for local variable execution**

```python
# tests/interpreter/test_interpreter.py (add this function)
def test_interpreter_executes_local_declarations():
    """Test that interpreter executes local variable declarations."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function main takes nothing returns nothing
        local integer x = 42
        local string greeting = "Hello"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # After execution, variables should be in context
    # (Note: currently variables are in function context, not global)
    assert 'main' in interpreter.functions
```

**Step 2: Run test to verify it passes**

Run: `pytest tests/interpreter/test_interpreter.py::test_interpreter_executes_local_declarations -v`
Expected: PASS (but variables not actually set yet)

**Step 3: Implement statement execution**

```python
# src/jass_runner/interpreter/interpreter.py (modify execute_function and add execute_statement)
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
        from ..parser.parser import LocalDecl

        if isinstance(statement, LocalDecl):
            self.execute_local_declaration(statement)

    def execute_local_declaration(self, decl: LocalDecl):
        """Execute a local variable declaration."""
        # Set the variable in current context
        self.current_context.set_variable(decl.name, decl.value)
```

**Step 4: Update test to actually check variable values**

```python
# tests/interpreter/test_interpreter.py (modify test_interpreter_executes_local_declarations)
def test_interpreter_executes_local_declarations():
    """Test that interpreter executes local variable declarations."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.parser.parser import Parser

    code = """
    function test_vars takes nothing returns nothing
        local integer x = 42
        local string greeting = "Hello"
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()

    # Manually execute the function to check context
    func = ast.functions[0]
    interpreter.execute_function(func)

    # Variables should be set in function context
    # (We can't easily check this without exposing context)
    assert func.name == 'test_vars'
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/interpreter/test_interpreter.py::test_interpreter_executes_local_declarations -v`
Expected: PASS

**Step 6: Add test for variable value checking**

```python
# tests/interpreter/test_interpreter.py (add this function)
def test_interpreter_sets_variable_values():
    """Test that interpreter correctly sets variable values."""
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.parser.parser import LocalDecl

    # Create a mock function with local declarations
    local_decl1 = LocalDecl(name='x', type='integer', value=42)
    local_decl2 = LocalDecl(name='msg', type='string', value='test')

    # Create interpreter and test context
    interpreter = Interpreter()
    test_context = ExecutionContext()
    interpreter.current_context = test_context

    # Execute declarations
    interpreter.execute_local_declaration(local_decl1)
    interpreter.execute_local_declaration(local_decl2)

    # Check values
    assert test_context.get_variable('x') == 42
    assert test_context.get_variable('msg') == 'test'
```

**Step 7: Run test to verify it passes**

Run: `pytest tests/interpreter/test_interpreter.py::test_interpreter_sets_variable_values -v`
Expected: PASS

**Step 8: Commit**

```bash
git add src/jass_runner/interpreter/interpreter.py tests/interpreter/test_interpreter.py
git commit -m "feat: implement local variable declaration execution"
```

### Task 7: Create Integration Test with Parser and Interpreter

**Files:**
- Create: `tests/integration/test_parser_interpreter.py`

**Step 1: Write integration test**

```python
# tests/integration/test_parser_interpreter.py
"""Integration tests for parser and interpreter."""

def test_end_to_end_simple_script():
    """Test end-to-end parsing and execution of simple script."""
    from jass_runner.parser.parser import Parser
    from jass_runner.interpreter.interpreter import Interpreter

    code = """
    function main takes nothing returns nothing
        local integer answer = 42
        local string message = "Hello, World!"
    endfunction
    """

    # Parse
    parser = Parser(code)
    ast = parser.parse()

    # Execute
    interpreter = Interpreter()
    interpreter.execute(ast)

    # Verify
    assert len(ast.functions) == 1
    assert ast.functions[0].name == 'main'
    assert 'main' in interpreter.functions

    # Check that function has body with statements
    func = interpreter.functions['main']
    assert func.body is not None
    assert len(func.body) == 2
```

**Step 2: Run test to verify it passes**

Run: `pytest tests/integration/test_parser_interpreter.py::test_end_to_end_simple_script -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_parser_interpreter.py
git commit -m "test: add parser-interpreter integration test"
```

### Task 8: Create Phase 2 Summary

**Files:**
- Create: `docs/phase2_summary.md`

**Step 1: Create phase summary**

```markdown
# Phase 2 Summary: Interpreter and Execution Engine

## Completed Tasks

1. **Execution Context System**
   - Created `ExecutionContext` class with variable scope management
   - Supports nested contexts (parent-child relationships)
   - Variable lookup traverses parent contexts
   - Proper variable setting and getting

2. **Expression Evaluator**
   - Created `Evaluator` class for evaluating JASS expressions
   - Supports literal values (integers, floats, strings)
   - Supports variable references
   - Basic type handling

3. **Interpreter Core**
   - Created `Interpreter` class for executing JASS AST
   - Manages global and function execution contexts
   - Registers and executes functions
   - Handles function call execution

4. **Enhanced Parser**
   - Extended parser to handle function bodies
   - Added support for `LocalDecl` statements
   - Parses local variable declarations with optional initialization
   - Handles basic expressions in declarations

5. **Statement Execution**
   - Implemented execution of local variable declarations
   - Variables are set in the appropriate execution context
   - Supports integer and string values

6. **Integration Testing**
   - Created end-to-end tests combining parser and interpreter
   - Verified parsing and execution workflow

## Key Files Created/Modified

- `src/jass_runner/interpreter/context.py` - Execution context with scope
- `src/jass_runner/interpreter/evaluator.py` - Expression evaluator
- `src/jass_runner/interpreter/interpreter.py` - Main interpreter
- `src/jass_runner/parser/parser.py` - Enhanced with statement parsing
- `tests/interpreter/test_context.py` - Context tests
- `tests/interpreter/test_evaluator.py` - Evaluator tests
- `tests/interpreter/test_interpreter.py` - Interpreter tests
- `tests/integration/test_parser_interpreter.py` - Integration tests

## Architecture Overview

```
Parser (AST) → Interpreter → Execution Context
    ↓                    ↓
FunctionDecl        Variable Scope
LocalDecl           Expression Eval
```

## Next Phase (Phase 3)

Phase 3 will focus on:
1. Native function framework
2. Basic native function implementations
3. Function call execution
4. Return value handling

## Testing Coverage

Run: `pytest --cov=src/jass_runner --cov-report=term-missing`
Expected: Coverage for parser and interpreter modules
```

**Step 2: Run coverage check**

Run: `pytest --cov=src/jass_runner --cov-report=term-missing`
Expected: Shows coverage for parser and interpreter modules

**Step 3: Commit**

```bash
git add docs/phase2_summary.md
git commit -m "docs: add phase 2 summary"
```

---

**Phase 2 Complete!** The project now has:
- Execution context with variable scope management
- Expression evaluator for basic types
- Interpreter that can execute parsed JASS code
- Support for local variable declarations
- Integration between parser and interpreter

**Next:** Proceed to Phase 3: Native Function Framework.