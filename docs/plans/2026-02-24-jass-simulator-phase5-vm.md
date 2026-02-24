# JASS Simulator Phase 5: Virtual Machine Core Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the JassVM virtual machine that integrates parser, interpreter, native functions, and timer system into a complete JASS execution environment.

**Architecture:** Create JassVM class as the main entry point, integrate all components, add script loading and execution capabilities, and provide command-line interface for running JASS scripts.

**Tech Stack:** Python 3.8+, pytest, argparse for CLI, logging

---

### Task 1: Create JassVM Core Class

**Files:**
- Create: `src/jass_runner/vm/__init__.py`
- Create: `src/jass_runner/vm/jass_vm.py`
- Create: `tests/vm/test_jass_vm.py`

**Step 1: Create vm package**

```python
# src/jass_runner/vm/__init__.py
"""Virtual machine module."""
```

**Step 2: Write failing test for JassVM creation**

```python
# tests/vm/test_jass_vm.py
"""Test JassVM class."""

def test_jass_vm_creation():
    """Test that JassVM can be created."""
    from jass_runner.vm.jass_vm import JassVM

    vm = JassVM()
    assert vm is not None
    assert hasattr(vm, 'load_script')
    assert hasattr(vm, 'execute')
    assert hasattr(vm, 'run')
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/vm/test_jass_vm.py::test_jass_vm_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.vm.jass_vm'"

**Step 4: Create minimal JassVM class**

```python
# src/jass_runner/vm/jass_vm.py
"""JASS Virtual Machine."""

import logging
from typing import Optional

from ..parser.parser import JassParser
from ..interpreter.interpreter import JassInterpreter
from ..natives.factory import NativeFactory
from ..timer.system import TimerSystem
from ..timer.simulation import SimulationLoop


logger = logging.getLogger(__name__)


class JassVM:
    """JASS Virtual Machine - main entry point for JASS execution."""

    def __init__(self, enable_timers: bool = True):
        """
        Initialize JASS Virtual Machine.

        Args:
            enable_timers: Whether to enable timer system
        """
        self.enable_timers = enable_timers

        # Initialize components
        self.parser = JassParser()
        self.timer_system = TimerSystem() if enable_timers else None
        self.native_factory = NativeFactory(timer_system=self.timer_system)
        self.native_registry = self.native_factory.create_default_registry()
        self.interpreter = JassInterpreter(
            native_registry=self.native_registry,
            timer_system=self.timer_system
        )

        # Simulation loop for timers
        self.simulation_loop: Optional[SimulationLoop] = None
        if enable_timers and self.timer_system:
            self.simulation_loop = SimulationLoop(self.timer_system)

        self.ast = None
        self.loaded = False

    def load_script(self, script_content: str):
        """Load and parse JASS script."""
        self.ast = self.parser.parse(script_content)
        self.loaded = True
        logger.info(f"Loaded script with {len(self.ast.functions) if hasattr(self.ast, 'functions') else 0} functions")

    def load_file(self, filepath: str):
        """Load JASS script from file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            script_content = f.read()
        self.load_script(script_content)

    def execute(self):
        """Execute the loaded script."""
        if not self.loaded:
            raise RuntimeError("No script loaded. Call load_script() first.")

        logger.info("Starting script execution")
        self.interpreter.interpret(self.ast)

    def run_simulation(self, seconds: float = 10.0):
        """Run timer simulation for specified seconds."""
        if not self.enable_timers or not self.simulation_loop:
            logger.warning("Timer system not enabled")
            return

        logger.info(f"Running simulation for {seconds} seconds")
        self.simulation_loop.run_seconds(seconds)
        logger.info(f"Simulation complete. Simulated time: {self.simulation_loop.get_simulated_time():.2f}s")

    def run(self, script_content: str, simulate_seconds: float = 0.0):
        """Load and execute script, optionally run simulation."""
        self.load_script(script_content)
        self.execute()

        if simulate_seconds > 0 and self.enable_timers:
            self.run_simulation(simulate_seconds)
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/vm/test_jass_vm.py::test_jass_vm_creation -v`
Expected: PASS

**Step 6: Commit**

```bash
git add src/jass_runner/vm/__init__.py src/jass_runner/vm/jass_vm.py tests/vm/test_jass_vm.py
git commit -m "feat: add JassVM core class"
```

---

### Task 2: Create Command-Line Interface

**Files:**
- Create: `src/jass_runner/cli.py`
- Create: `tests/cli/test_cli.py`

**Step 1: Write failing test for CLI**

```python
# tests/cli/test_cli.py
"""Test command-line interface."""

def test_cli_parser_creation():
    """Test that CLI argument parser can be created."""
    from jass_runner.cli import create_parser

    parser = create_parser()
    assert parser is not None
    assert hasattr(parser, 'parse_args')
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_cli.py::test_cli_parser_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.cli'"

**Step 3: Create CLI module**

```python
# src/jass_runner/cli.py
"""Command-line interface for JASS runner."""

import argparse
import sys
import logging
from .vm.jass_vm import JassVM


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description='JASS Script Runner - Execute JASS scripts outside of Warcraft III',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s script.j          # Execute JASS script
  %(prog)s script.j --simulate 30  # Execute and simulate 30 seconds
  %(prog)s script.j --no-timers   # Execute without timer system
  %(prog)s --version         # Show version
        """
    )

    parser.add_argument(
        'script',
        help='JASS script file to execute'
    )

    parser.add_argument(
        '--simulate',
        type=float,
        default=0.0,
        help='Simulate timer execution for N seconds (default: 0, no simulation)'
    )

    parser.add_argument(
        '--no-timers',
        action='store_true',
        help='Disable timer system'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress all output except errors'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='JASS Runner 1.0.0'
    )

    return parser


def setup_logging(verbose: bool, quiet: bool):
    """Setup logging based on verbosity."""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format='%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    try:
        # Create and run VM
        vm = JassVM(enable_timers=not args.no_timers)
        vm.load_file(args.script)
        vm.execute()

        if args.simulate > 0:
            vm.run_simulation(args.simulate)

        logging.info("Execution completed successfully")
        return 0

    except FileNotFoundError:
        logging.error(f"Script file not found: {args.script}")
        return 1
    except Exception as e:
        logging.error(f"Error executing script: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_cli.py::test_cli_parser_creation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/cli.py tests/cli/test_cli.py
git commit -m "feat: add command-line interface"
```

---

### Task 3: Create Main Entry Point

**Files:**
- Create: `src/jass_runner/__main__.py`
- Modify: `pyproject.toml`

**Step 1: Create __main__ module**

```python
# src/jass_runner/__main__.py
"""Main entry point for package execution."""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
```

**Step 2: Update pyproject.toml with entry points**

```toml
# pyproject.toml (update existing file)
[project]
name = "jass-runner"
version = "1.0.0"
description = "JASS script simulation runner for Warcraft III"
readme = "README.md"
requires-python = ">=3.8"
dependencies = []

[project.scripts]
jass-runner = "jass_runner.cli:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

**Step 3: Test package execution**

```bash
# Test that package can be executed
python -m jass_runner --help
```

Expected: Should show help message

**Step 4: Commit**

```bash
git add src/jass_runner/__main__.py pyproject.toml
git commit -m "feat: add main entry point and package configuration"
```

---

### Task 4: Add VM Integration Tests

**Files:**
- Create: `tests/vm/test_integration.py`

**Step 1: Write VM integration test**

```python
# tests/vm/test_integration.py
"""Integration tests for JassVM."""

import tempfile
import os

def test_vm_basic_execution():
    """Test basic VM execution with simple script."""
    from jass_runner.vm.jass_vm import JassVM

    # Simple JASS script
    script = """
    function main takes nothing returns nothing
        // Simple test function
    endfunction
    """

    vm = JassVM(enable_timers=False)
    vm.load_script(script)
    vm.execute()

    assert vm.loaded is True
    assert vm.ast is not None

def test_vm_file_loading():
    """Test VM loading script from file."""
    from jass_runner.vm.jass_vm import JassVM

    # Create temporary JASS file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.j', delete=False) as f:
        f.write("""
        function test takes nothing returns nothing
            // Test function
        endfunction
        """)
        temp_file = f.name

    try:
        vm = JassVM(enable_timers=False)
        vm.load_file(temp_file)
        vm.execute()

        assert vm.loaded is True
        assert vm.ast is not None
    finally:
        os.unlink(temp_file)

def test_vm_with_natives():
    """Test VM execution with native functions."""
    import logging
    from io import StringIO
    from jass_runner.vm.jass_vm import JassVM

    # Capture log output
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.basic')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Script with native calls
    script = """
    function main takes nothing returns nothing
        call DisplayTextToPlayer(0, 0, 0, "Hello from VM!")
        call KillUnit("test_unit")
    endfunction
    """

    vm = JassVM(enable_timers=False)
    vm.load_script(script)
    vm.execute()

    # Check log output
    log_output = log_stream.getvalue()
    assert "[DisplayTextToPlayer] Player 0: Hello from VM!" in log_output
    assert "[KillUnit] Unit test_unit has been killed" in log_output

    logger.removeHandler(handler)
```

**Step 2: Run tests to verify they pass**

Run: `pytest tests/vm/test_integration.py -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add tests/vm/test_integration.py
git commit -m "test: add VM integration tests"
```

---

### Task 5: Add Timer Integration to VM

**Files:**
- Modify: `tests/vm/test_integration.py`

**Step 1: Write test for VM with timers**

```python
# tests/vm/test_integration.py (add to existing file)

def test_vm_with_timers():
    """Test VM execution with timer system."""
    import logging
    from io import StringIO
    from jass_runner.vm.jass_vm import JassVM

    # Capture log output
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.timer_natives')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Script with timer operations
    script = """
    function timer_callback takes nothing returns nothing
        call DisplayTextToPlayer(0, 0, 0, "Timer fired!")
    endfunction

    function main takes nothing returns nothing
        local timer t = CreateTimer()
        call TimerStart(t, 1.0, false, function timer_callback)
        call DisplayTextToPlayer(0, 0, 0, "Timer started!")
    endfunction
    """

    vm = JassVM(enable_timers=True)
    vm.load_script(script)
    vm.execute()

    # Run simulation
    vm.run_simulation(2.0)

    # Check log output
    log_output = log_stream.getvalue()
    assert "[CreateTimer] Created timer:" in log_output
    assert "[TimerStart] Started timer" in log_output

    logger.removeHandler(handler)
```

**Step 2: Run test to verify it passes**

Run: `pytest tests/vm/test_integration.py::test_vm_with_timers -v`
Expected: PASS

**Step 3: Commit**

```bash
git add tests/vm/test_integration.py
git commit -m "test: add VM timer integration test"
```

---

### Task 6: Create Complete Example Script

**Files:**
- Create: `examples/complete_example.j`
- Create: `examples/run_complete_example.py`

**Step 1: Create complete example JASS script**

```jass
// examples/complete_example.j
// Complete example demonstrating all JASS runner features

function unit_died takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "A unit has died!")
endfunction

function periodic_report takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Periodic report: All systems operational")
endfunction

function main takes nothing returns nothing
    local timer death_timer
    local timer report_timer
    local string unit_name

    call DisplayTextToPlayer(0, 0, 0, "Starting simulation...")

    // Create a unit
    set unit_name = "Hero_001"
    call DisplayTextToPlayer(0, 0, 0, "Creating unit: " + unit_name)

    // Create death timer (one-shot, 3 seconds)
    set death_timer = CreateTimer()
    call TimerStart(death_timer, 3.0, false, function unit_died)

    // Create periodic report timer (every 2 seconds)
    set report_timer = CreateTimer()
    call TimerStart(report_timer, 2.0, true, function periodic_report)

    call DisplayTextToPlayer(0, 0, 0, "Timers started. Simulation running...")
endfunction
```

**Step 2: Create Python script to run complete example**

```python
# examples/run_complete_example.py
"""Run complete JASS example."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logging
from jass_runner.vm.jass_vm import JassVM

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Read JASS script
    with open('examples/complete_example.j', 'r') as f:
        jass_code = f.read()

    # Create VM with timers enabled
    vm = JassVM(enable_timers=True)

    print("=" * 60)
    print("JASS Runner - Complete Example")
    print("=" * 60)

    # Load and execute
    vm.load_script(jass_code)
    vm.execute()

    # Run simulation for 10 seconds
    print("\n" + "=" * 60)
    print("Running simulation for 10 seconds...")
    print("=" * 60)
    vm.run_simulation(10.0)

    print("\n" + "=" * 60)
    print("Simulation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

**Step 3: Commit**

```bash
git add examples/complete_example.j examples/run_complete_example.py
git commit -m "example: add complete JASS example"
```

---

### Task 7: Add Error Handling and Validation

**Files:**
- Modify: `src/jass_runner/vm/jass_vm.py`
- Modify: `tests/vm/test_jass_vm.py`

**Step 1: Write failing test for error handling**

```python
# tests/vm/test_jass_vm.py (add to existing file)

def test_vm_error_handling():
    """Test VM error handling."""
    from jass_runner.vm.jass_vm import JassVM

    vm = JassVM()

    # Test executing without loading
    import pytest
    with pytest.raises(RuntimeError, match="No script loaded"):
        vm.execute()

    # Test loading invalid script
    vm.load_script("invalid jass code")
    # Should not raise immediately, but execution might fail
    # This tests that load_script doesn't crash on parse errors
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/vm/test_jass_vm.py::test_vm_error_handling -v`
Expected: PASS for first assertion, but test documents error handling

**Step 3: Enhance error handling in JassVM**

```python
# src/jass_runner/vm/jass_vm.py (update execute method)

def execute(self):
    """Execute the loaded script."""
    if not self.loaded:
        raise RuntimeError("No script loaded. Call load_script() first.")

    if self.ast is None:
        raise RuntimeError("Failed to parse script. No AST available.")

    logger.info("Starting script execution")
    try:
        self.interpreter.interpret(self.ast)
        logger.info("Script execution completed successfully")
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        raise
```

**Step 4: Add test for file not found**

```python
# tests/vm/test_jass_vm.py (add to existing file)

def test_vm_file_not_found():
    """Test VM handling of missing file."""
    from jass_runner.vm.jass_vm import JassVM
    import pytest

    vm = JassVM()

    with pytest.raises(FileNotFoundError):
        vm.load_file("non_existent_file.j")
```

**Step 5: Run tests to verify they pass**

Run: `pytest tests/vm/test_jass_vm.py::test_vm_error_handling tests/vm/test_jass_vm.py::test_vm_file_not_found -v`
Expected: Both PASS

**Step 6: Commit**

```bash
git add src/jass_runner/vm/jass_vm.py tests/vm/test_jass_vm.py
git commit -m "feat: enhance error handling in JassVM"
```

---

### Task 8: Create User Documentation

**Files:**
- Create: `docs/user_guide.md`
- Modify: `README.md`

**Step 1: Create user guide**

```markdown
# JASS Runner User Guide

## Installation

```bash
# Install from local source
pip install -e .

# Or run directly without installation
python -m jass_runner --help
```

## Basic Usage

### Execute a JASS script

```bash
jass-runner script.j
```

### Execute with timer simulation

```bash
jass-runner script.j --simulate 30
```

### Disable timer system

```bash
jass-runner script.j --no-timers
```

### Verbose output

```bash
jass-runner script.j --verbose
```

## JASS Language Support

The runner supports a subset of JASS syntax:

- Function declarations: `function name takes nothing returns nothing`
- Local variables: `local type name`
- Native function calls: `call NativeFunction(args)`
- Basic control flow (if/else, loops)
- Timer operations

## Native Function Simulation

Native functions are simulated with console output:

- `DisplayTextToPlayer(player, x, y, message)` - Outputs message to console
- `KillUnit(unit)` - Logs unit death
- `CreateTimer()`, `TimerStart()`, etc. - Simulated timer operations

## Timer System

The timer system uses frame-based simulation:

- Default: 30 FPS (0.033 seconds per frame)
- Allows fast-forwarding through long simulations
- Supports one-shot and periodic timers
- Timers can be paused and resumed

## Example

Create a file `test.j`:

```jass
function main takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Hello from JASS!")

    local timer t = CreateTimer()
    call TimerStart(t, 2.0, false, function main)
endfunction
```

Run it:

```bash
jass-runner test.j --simulate 5
```

## Extending

See [docs/natives/README.md](docs/natives/README.md) for extending native functions.
See [docs/timer/README.md](docs/timer/README.md) for timer system details.
```

**Step 2: Update main README**

```markdown
# JASS Runner

A JASS script simulation runner for Warcraft III map development.

## Features

- JASS script parsing and interpretation
- Native function simulation with console output
- Frame-based timer system for fast simulation
- Extensible plugin architecture
- Command-line interface

## Quick Start

```bash
# Install
pip install -e .

# Run a script
jass-runner examples/complete_example.j --simulate 10
```

## Documentation

- [User Guide](docs/user_guide.md) - How to use JASS Runner
- [Native Functions](docs/natives/README.md) - Extending native functions
- [Timer System](docs/timer/README.md) - Timer system details
- [Examples](examples/) - Example scripts

## Project Structure

- `src/jass_runner/parser/` - JASS parser and lexer
- `src/jass_runner/interpreter/` - Execution engine
- `src/jass_runner/natives/` - Native function framework
- `src/jass_runner/timer/` - Timer system
- `src/jass_runner/vm/` - Virtual machine (this phase)

## Development

See implementation plans in `docs/plans/` for detailed development steps.
```

**Step 3: Commit**

```bash
git add docs/user_guide.md README.md
git commit -m "docs: add user guide and update README"
```

---

### Task 9: Create Setup and Installation Script

**Files:**
- Create: `setup.py`
- Create: `requirements.txt`

**Step 1: Create setup.py for backward compatibility**

```python
# setup.py
"""Setup script for JASS Runner."""

from setuptools import setup, find_packages

setup(
    name="jass-runner",
    version="1.0.0",
    description="JASS script simulation runner for Warcraft III",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="JASS Runner Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "jass-runner=jass_runner.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
```

**Step 2: Create requirements.txt**

```txt
# requirements.txt
# JASS Runner dependencies
# No external dependencies required
```

**Step 3: Test installation**

```bash
# Test installation
pip install -e .
jass-runner --version
```

Expected: Shows "JASS Runner 1.0.0"

**Step 4: Commit**

```bash
git add setup.py requirements.txt
git commit -m "feat: add setup.py and requirements.txt"
```

---

### Task 10: Final Integration Test

**Files:**
- Create: `tests/integration/test_full_integration.py`

**Step 1: Write full integration test**

```python
# tests/integration/test_full_integration.py
"""Full integration test of JASS Runner."""

import tempfile
import os
import subprocess
import sys

def test_cli_execution():
    """Test CLI execution with a simple script."""
    # Create temporary JASS file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.j', delete=False) as f:
        f.write("""
        function main takes nothing returns nothing
            call DisplayTextToPlayer(0, 0, 0, "CLI test successful!")
        endfunction
        """)
        temp_file = f.name

    try:
        # Run via CLI
        result = subprocess.run(
            [sys.executable, "-m", "jass_runner.cli", temp_file],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Check execution
        assert result.returncode == 0
        assert "CLI test successful!" in result.stdout

    finally:
        os.unlink(temp_file)

def test_package_installation():
    """Test that package can be installed and run."""
    # This test assumes the package is already installed in development mode
    # We just verify the entry point exists
    import jass_runner.cli
    import jass_runner.vm.jass_vm

    # If we can import these, the package structure is correct
    assert jass_runner.cli is not None
    assert jass_runner.vm.jass_vm is not None

def test_example_scripts():
    """Test that example scripts work."""
    from jass_runner.vm.jass_vm import JassVM

    # Test complete example
    with open('examples/complete_example.j', 'r') as f:
        script = f.read()

    vm = JassVM(enable_timers=True)
    vm.load_script(script)
    vm.execute()

    # Should not raise exceptions
    assert vm.loaded is True
```

**Step 2: Run integration tests**

Run: `pytest tests/integration/test_full_integration.py -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add tests/integration/test_full_integration.py
git commit -m "test: add full integration tests"
```

---

## Phase 5 Completion

Phase 5 implements the complete JASS Virtual Machine with:

1. **JassVM class** - Main entry point integrating all components
2. **Command-line interface** - `jass-runner` command for script execution
3. **Package structure** - Proper Python package with entry points
4. **Error handling** - Robust error handling and validation
5. **User documentation** - Complete user guide and examples
6. **Installation support** - setup.py and requirements.txt

**Key Features:**
- Single entry point for JASS execution
- CLI with support for timer simulation
- Proper Python package structure
- Comprehensive error handling
- Complete documentation and examples
- Integration of all previous phases (parser, interpreter, natives, timer)

**Project Complete:** All 5 phases are now implemented:

1. **Phase 1**: Project Setup and Core Infrastructure
2. **Phase 2**: Interpreter and Execution Engine
3. **Phase 3**: Native Function Framework
4. **Phase 4**: Timer System
5. **Phase 5**: Virtual Machine Core (this phase)

The JASS Runner can now:
- Parse and interpret JASS scripts
- Simulate native functions with console output
- Execute frame-based timer simulations
- Be used via command-line interface
- Be extended with custom native functions

---

Plan complete and saved to `docs/plans/2026-02-24-jass-simulator-phase5-vm.md`.

Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**