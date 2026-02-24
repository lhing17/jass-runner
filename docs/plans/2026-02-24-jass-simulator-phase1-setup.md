# JASS Simulator Phase 1: Project Setup and Core Infrastructure Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Set up the project structure, core infrastructure, and basic JASS parser.

**Architecture:** Create the directory structure, setup files, and basic parser that can parse simple JASS variable declarations and function definitions.

**Tech Stack:** Python 3.8+, pytest, setuptools, logging

---

### Task 1: Create Project Structure

**Files:**
- Create: `pyproject.toml`
- Create: `README.md`
- Create: `src/jass_runner/__init__.py`
- Create: `tests/__init__.py`
- Create: `examples/hello_world.j`

**Step 1: Create pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "jass-runner"
version = "0.1.0"
description = "JASS script simulator for Warcraft III map testing"
readme = "README.md"
authors = [{name = "Developer", email = "dev@example.com"}]
license = {text = "MIT"}
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Testing",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
requires-python = ">=3.8"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=22.0", "flake8>=5.0"]

[tool.setuptools.packages.find]
where = ["src"]
```

**Step 2: Run validation**

Run: `python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"`
Expected: No error

**Step 3: Create README.md**

```markdown
# JASS Runner

A JASS script simulator for Warcraft III map testing and automation.

## Features

- Execute JASS scripts outside of Warcraft III
- Simulate native functions with console output
- Frame-based timer system for fast simulation
- Extensible plugin architecture for custom natives

## Installation

```bash
pip install -e .
```

## Usage

```python
from jass_runner import JassVM

vm = JassVM()
vm.load_script("map_script.j")
vm.execute()
```

## Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
flake8 src tests
```

## License

MIT

**Step 4: Create package structure**

```python
# src/jass_runner/__init__.py
"""JASS Runner - JASS script simulator for Warcraft III."""

__version__ = "0.1.0"
```

```python
# tests/__init__.py
"""Test package for jass-runner."""
```

**Step 5: Create example JASS script**

```jass
// examples/hello_world.j
// Simple JASS script for testing

function main takes nothing returns nothing
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Hello, World!")
endfunction
```

**Step 6: Commit**

```bash
git add pyproject.toml README.md src/jass_runner/__init__.py tests/__init__.py examples/hello_world.j
git commit -m "feat: initial project setup"
```

### Task 2: Setup Testing Infrastructure

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_project_structure.py`

**Step 1: Create test configuration**

```python
# tests/conftest.py
"""Pytest configuration for jass-runner."""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

**Step 2: Write failing test for project structure**

```python
# tests/test_project_structure.py
"""Test project structure and basic imports."""

def test_package_can_be_imported():
    """Test that the jass_runner package can be imported."""
    import jass_runner
    assert jass_runner.__version__ == "0.1.0"
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/test_project_structure.py::test_package_can_be_imported -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner'"

**Step 4: Install package in development mode**

Run: `pip install -e .`
Expected: Success message "Successfully installed jass-runner-0.1.0"

**Step 5: Run test to verify it passes**

Run: `pytest tests/test_project_structure.py::test_package_can_be_imported -v`
Expected: PASS

**Step 6: Commit**

```bash
git add tests/conftest.py tests/test_project_structure.py
git commit -m "test: add basic test infrastructure"
```

### Task 3: Create Core Parser Structure

**Files:**
- Create: `src/jass_runner/parser/__init__.py`
- Create: `src/jass_runner/parser/lexer.py`
- Create: `tests/parser/test_lexer.py`

**Step 1: Create parser package**

```python
# src/jass_runner/parser/__init__.py
"""JASS parser module."""
```

**Step 2: Write failing test for lexer**

```python
# tests/parser/test_lexer.py
"""Test JASS lexer."""

def test_lexer_can_tokenize_simple_code():
    """Test that lexer can tokenize simple JASS code."""
    from jass_runner.parser.lexer import Lexer

    code = "function main takes nothing returns nothing"
    lexer = Lexer(code)
    tokens = list(lexer.tokenize())

    # Should have at least some tokens
    assert len(tokens) > 0
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/parser/test_lexer.py::test_lexer_can_tokenize_simple_code -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.parser.lexer'"

**Step 4: Create minimal lexer implementation**

```python
# src/jass_runner/parser/lexer.py
"""Simple JASS lexer."""

from dataclasses import dataclass
from typing import List, Iterator
import re

@dataclass
class Token:
    """Represents a token in JASS code."""
    type: str
    value: str
    line: int
    column: int

class Lexer:
    """Simple lexer for JASS code."""

    # Basic token patterns
    TOKEN_PATTERNS = [
        ('WHITESPACE', r'\s+'),
        ('COMMENT', r'//.*'),
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('OPERATOR', r'[+\-*/=<>!&|^%~]+'),
        ('PUNCTUATION', r'[(),;.:{}]'),
    ]

    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> Iterator[Token]:
        """Generate tokens from the code."""
        while self.pos < len(self.code):
            matched = False

            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)

                if match:
                    value = match.group(0)
                    start_pos = self.pos

                    # Skip whitespace and comments
                    if token_type not in ('WHITESPACE', 'COMMENT'):
                        yield Token(
                            type=token_type,
                            value=value,
                            line=self.line,
                            column=self.column
                        )

                    # Update position
                    self.pos = match.end()

                    # Update line and column counters
                    lines = value.count('\n')
                    if lines > 0:
                        self.line += lines
                        self.column = 1 + len(value) - value.rfind('\n') - 1
                    else:
                        self.column += len(value)

                    matched = True
                    break

            if not matched:
                # No pattern matched, skip one character
                self.pos += 1
                self.column += 1
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/parser/test_lexer.py::test_lexer_can_tokenize_simple_code -v`
Expected: PASS

**Step 6: Commit**

```bash
git add src/jass_runner/parser/__init__.py src/jass_runner/parser/lexer.py tests/parser/test_lexer.py
git commit -m "feat: add basic JASS lexer"
```

### Task 4: Enhance Lexer with Specific Tests

**Files:**
- Modify: `tests/parser/test_lexer.py`
- Modify: `src/jass_runner/parser/lexer.py`

**Step 1: Write failing test for specific token types**

```python
# tests/parser/test_lexer.py (add this function)
def test_lexer_token_types():
    """Test that lexer correctly identifies token types."""
    from jass_runner.parser.lexer import Lexer

    code = 'function test takes integer x returns string'
    lexer = Lexer(code)
    tokens = [t for t in lexer.tokenize() if t.type != 'WHITESPACE']

    expected_types = ['IDENTIFIER', 'IDENTIFIER', 'IDENTIFIER', 'IDENTIFIER', 'IDENTIFIER', 'IDENTIFIER']
    actual_types = [t.type for t in tokens]

    assert actual_types == expected_types
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/parser/test_lexer.py::test_lexer_token_types -v`
Expected: FAIL with assertion error (wrong token types)

**Step 3: Update lexer to handle keywords**

```python
# src/jass_runner/parser/lexer.py (modify TOKEN_PATTERNS)
class Lexer:
    """Simple lexer for JASS code."""

    # JASS keywords
    KEYWORDS = {
        'function', 'takes', 'returns', 'nothing', 'integer', 'real',
        'string', 'boolean', 'code', 'handle', 'endfunction', 'call',
        'if', 'then', 'else', 'endif', 'loop', 'endloop', 'exitwhen',
        'set', 'local', 'constant', 'array', 'native', 'type', 'extends'
    }

    # Basic token patterns (update order for better matching)
    TOKEN_PATTERNS = [
        ('WHITESPACE', r'\s+'),
        ('COMMENT', r'//.*'),
        ('STRING', r'"[^"]*"'),
        ('NUMBER', r'\d+(\.\d+)?'),
        ('OPERATOR', r'[+\-*/=<>!&|^%~]+'),
        ('PUNCTUATION', r'[(),;.:{}]'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ]

    def tokenize(self) -> Iterator[Token]:
        """Generate tokens from the code."""
        while self.pos < len(self.code):
            matched = False

            for token_type, pattern in self.TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.code, self.pos)

                if match:
                    value = match.group(0)

                    # Skip whitespace and comments
                    if token_type not in ('WHITESPACE', 'COMMENT'):
                        # Check if identifier is a keyword
                        actual_type = token_type
                        if token_type == 'IDENTIFIER' and value in self.KEYWORDS:
                            actual_type = 'KEYWORD'

                        yield Token(
                            type=actual_type,
                            value=value,
                            line=self.line,
                            column=self.column
                        )

                    # Update position and line/column counters
                    self._update_position(value)
                    matched = True
                    break

            if not matched:
                # No pattern matched, skip one character
                self._update_position(self.code[self.pos])
                self.pos += 1

    def _update_position(self, text: str):
        """Update line and column counters based on text."""
        lines = text.count('\n')
        if lines > 0:
            self.line += lines
            self.column = 1 + len(text) - text.rfind('\n') - 1
        else:
            self.column += len(text)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/parser/test_lexer.py::test_lexer_token_types -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/parser/lexer.py tests/parser/test_lexer.py
git commit -m "feat: enhance lexer with keyword recognition"
```

### Task 5: Create Basic Parser

**Files:**
- Create: `src/jass_runner/parser/parser.py`
- Create: `tests/parser/test_parser.py`

**Step 1: Write failing test for parser**

```python
# tests/parser/test_parser.py
"""Test JASS parser."""

def test_parser_can_parse_function_declaration():
    """Test that parser can parse a simple function declaration."""
    from jass_runner.parser.parser import Parser

    code = """
    function test takes integer x returns string
    endfunction
    """

    parser = Parser(code)
    ast = parser.parse()

    # Should have at least one function
    assert hasattr(ast, 'functions')
    assert len(ast.functions) == 1
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/parser/test_parser.py::test_parser_can_parse_function_declaration -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.parser.parser'"

**Step 3: Create minimal parser implementation**

```python
# src/jass_runner/parser/parser.py
"""Simple JASS parser."""

from dataclasses import dataclass
from typing import List, Optional, Any
from .lexer import Lexer, Token

@dataclass
class FunctionDecl:
    """Represents a function declaration."""
    name: str
    parameters: List['Parameter']
    return_type: str
    body: Optional[List[Any]] = None

@dataclass
class Parameter:
    """Represents a function parameter."""
    name: str
    type: str

@dataclass
class AST:
    """Abstract Syntax Tree for JASS code."""
    functions: List[FunctionDecl]

class Parser:
    """Parser for JASS code."""

    def __init__(self, code: str):
        self.lexer = Lexer(code)
        self.tokens = list(self.lexer.tokenize())
        self.pos = 0
        self.current_token = None
        self.next_token()

    def next_token(self):
        """Advance to the next token."""
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            self.pos += 1
        else:
            self.current_token = None

    def parse(self) -> AST:
        """Parse the code and return AST."""
        functions = []

        while self.current_token:
            if self.current_token.type == 'KEYWORD' and self.current_token.value == 'function':
                func = self.parse_function()
                if func:
                    functions.append(func)
            else:
                self.next_token()

        return AST(functions=functions)

    def parse_function(self) -> Optional[FunctionDecl]:
        """Parse a function declaration."""
        # Skip 'function' keyword
        self.next_token()

        # Get function name
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None
        name = self.current_token.value
        self.next_token()

        # Skip 'takes' keyword
        if not self.current_token or self.current_token.value != 'takes':
            return None
        self.next_token()

        # Parse parameters
        parameters = []
        if self.current_token and self.current_token.value == 'nothing':
            # No parameters
            self.next_token()
        else:
            # Parse parameter list
            while self.current_token and self.current_token.value != 'returns':
                if self.current_token.type == 'IDENTIFIER':
                    param_type = self.current_token.value
                    self.next_token()

                    if self.current_token and self.current_token.type == 'IDENTIFIER':
                        param_name = self.current_token.value
                        self.next_token()
                        parameters.append(Parameter(name=param_name, type=param_type))

                # Skip comma if present
                if self.current_token and self.current_token.value == ',':
                    self.next_token()

        # Skip 'returns' keyword
        if not self.current_token or self.current_token.value != 'returns':
            return None
        self.next_token()

        # Get return type
        if not self.current_token or self.current_token.type not in ('IDENTIFIER', 'KEYWORD'):
            return None
        return_type = self.current_token.value
        self.next_token()

        # Skip to endfunction (for now)
        while self.current_token and not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endfunction'):
            self.next_token()

        if self.current_token and self.current_token.value == 'endfunction':
            self.next_token()

        return FunctionDecl(name=name, parameters=parameters, return_type=return_type)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/parser/test_parser.py::test_parser_can_parse_function_declaration -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/parser/parser.py tests/parser/test_parser.py
git commit -m "feat: add basic JASS parser"
```

### Task 6: Add Error Handling to Parser

**Files:**
- Modify: `tests/parser/test_parser.py`
- Modify: `src/jass_runner/parser/parser.py`

**Step 1: Write failing test for error handling**

```python
# tests/parser/test_parser.py (add this function)
def test_parser_handles_invalid_syntax():
    """Test that parser handles invalid syntax gracefully."""
    from jass_runner.parser.parser import Parser

    code = "function invalid syntax"

    parser = Parser(code)
    ast = parser.parse()

    # Should return empty AST or handle error
    assert len(ast.functions) == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/parser/test_parser.py::test_parser_handles_invalid_syntax -v`
Expected: FAIL (parser might crash or return wrong result)

**Step 3: Add error handling to parser**

```python
# src/jass_runner/parser/parser.py (modify parse_function method)
    def parse_function(self) -> Optional[FunctionDecl]:
        """Parse a function declaration."""
        try:
            # Skip 'function' keyword
            self.next_token()

            # Get function name
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            name = self.current_token.value
            self.next_token()

            # Skip 'takes' keyword
            if not self.current_token or self.current_token.value != 'takes':
                return None
            self.next_token()

            # Parse parameters
            parameters = []
            if self.current_token and self.current_token.value == 'nothing':
                # No parameters
                self.next_token()
            else:
                # Parse parameter list
                while self.current_token and self.current_token.value != 'returns':
                    if self.current_token and self.current_token.type == 'IDENTIFIER':
                        param_type = self.current_token.value
                        self.next_token()

                        if self.current_token and self.current_token.type == 'IDENTIFIER':
                            param_name = self.current_token.value
                            self.next_token()
                            parameters.append(Parameter(name=param_name, type=param_type))

                    # Skip comma if present
                    if self.current_token and self.current_token.value == ',':
                        self.next_token()

            # Skip 'returns' keyword
            if not self.current_token or self.current_token.value != 'returns':
                return None
            self.next_token()

            # Get return type
            if not self.current_token or self.current_token.type not in ('IDENTIFIER', 'KEYWORD'):
                return None
            return_type = self.current_token.value
            self.next_token()

            # Skip to endfunction (for now)
            while self.current_token and not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endfunction'):
                self.next_token()

            if self.current_token and self.current_token.value == 'endfunction':
                self.next_token()

            return FunctionDecl(name=name, parameters=parameters, return_type=return_type)

        except Exception:
            # If any error occurs, skip to next token and return None
            while self.current_token and not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'function'):
                self.next_token()
            return None
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/parser/test_parser.py::test_parser_handles_invalid_syntax -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/parser/parser.py tests/parser/test_parser.py
git commit -m "feat: add error handling to parser"
```

### Task 7: Create Integration Test

**Files:**
- Create: `tests/integration/test_basic_parsing.py`

**Step 1: Write integration test**

```python
# tests/integration/test_basic_parsing.py
"""Integration tests for basic parsing."""

def test_parse_example_script():
    """Test parsing the example script."""
    from jass_runner.parser.parser import Parser

    with open('examples/hello_world.j', 'r', encoding='utf-8') as f:
        code = f.read()

    parser = Parser(code)
    ast = parser.parse()

    # Should find the main function
    assert len(ast.functions) == 1
    assert ast.functions[0].name == 'main'
    assert ast.functions[0].return_type == 'nothing'
    assert len(ast.functions[0].parameters) == 0
```

**Step 2: Run test to verify it passes**

Run: `pytest tests/integration/test_basic_parsing.py::test_parse_example_script -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/integration/test_basic_parsing.py
git commit -m "test: add integration test for parsing"
```

### Task 8: Create Phase 1 Summary

**Files:**
- Create: `docs/phase1_summary.md`

**Step 1: Create phase summary**

```markdown
# Phase 1 Summary: Project Setup and Core Infrastructure

## Completed Tasks

1. **Project Structure Setup**
   - Created `pyproject.toml` with proper metadata
   - Created `README.md` with documentation
   - Set up package structure in `src/jass_runner/`
   - Created example JASS script

2. **Testing Infrastructure**
   - Set up pytest configuration
   - Created basic test for package import
   - Installed package in development mode

3. **Lexer Implementation**
   - Created tokenizer for JASS code
   - Supports keywords, identifiers, strings, numbers, operators, punctuation
   - Handles whitespace and comments
   - Proper line/column tracking

4. **Parser Implementation**
   - Created basic parser for function declarations
   - Supports function name, parameters, return type
   - Error handling for invalid syntax
   - Produces AST with FunctionDecl and Parameter objects

5. **Integration Testing**
   - Tested parsing of example script
   - Verified end-to-end functionality

## Key Files Created

- `pyproject.toml` - Project configuration
- `README.md` - Documentation
- `src/jass_runner/parser/lexer.py` - JASS lexer
- `src/jass_runner/parser/parser.py` - JASS parser
- `tests/parser/test_lexer.py` - Lexer tests
- `tests/parser/test_parser.py` - Parser tests
- `tests/integration/test_basic_parsing.py` - Integration tests

## Next Phase (Phase 2)

Phase 2 will focus on:
1. Interpreter implementation
2. Variable scope management
3. Basic expression evaluation
4. Function call execution

## Testing Coverage

Run: `pytest --cov=src/jass_runner --cov-report=term-missing`
Expected: Basic coverage of parser module
```

**Step 2: Run coverage check**

Run: `pytest --cov=src/jass_runner --cov-report=term-missing`
Expected: Shows coverage for parser module

**Step 3: Commit**

```bash
git add docs/phase1_summary.md
git commit -m "docs: add phase 1 summary"
```

---

**Phase 1 Complete!** The project now has:
- Proper Python package structure
- Basic JASS lexer and parser
- Testing infrastructure
- Example script
- Documentation

**Next:** Proceed to Phase 2: Interpreter and Execution Engine.