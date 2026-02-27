# JASS Runner

A JASS script simulator for Warcraft III map testing and automation.

## Features

- JASS script parsing and interpretation
- Native function simulation with console output
- Frame-based timer system for fast simulation
- Extensible plugin architecture
- Command-line interface

## Project Status

### Completed
- ✅ Project requirements analysis and architecture design
- ✅ 5-phase detailed implementation plan documentation
- ✅ Phase 1: Project setup and core infrastructure (all tasks completed)
- ✅ Phase 2: Interpreter and execution engine (all tasks completed)
- ✅ Phase 3: Native function framework (all tasks completed)
- ✅ State Management System (all 5 phases completed)
  - Handle class system and HandleManager
  - Native function state sharing
  - Integration tests and performance benchmarks
  - Documentation and utilities
- ✅ Project documentation (CLAUDE.md, PROJECT_NOTES.md, docs/natives/README.md)

### In Progress
- ✅ Phase 4: Timer system (completed)
- ✅ Phase 5: Virtual machine core (completed)

## Technical Architecture

The project uses a five-layer architecture design:

1. **Parser Layer** (`src/jass_runner/parser/`) - JASS syntax parsing, generates AST
2. **Interpreter Layer** (`src/jass_runner/interpreter/`) - AST execution, variable scope management
3. **Native Function Framework** (`src/jass_runner/natives/`) - Plugin-based native function simulation
4. **Timer System** (`src/jass_runner/timer/`) - Frame-based timer simulation
5. **Virtual Machine Core** (`src/jass_runner/vm/`) - Component integration and command-line interface

## Installation

```bash
# Install development version
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Usage

### Using Python API

```python
from jass_runner import JassVM

# Create virtual machine instance
vm = JassVM()

# Load JASS script
vm.load_script("map_script.j")

# Execute script
vm.execute()

# Run timer simulation (optional)
vm.run_simulation(10.0)  # Simulate 10 seconds of game time
```

### Using Command Line Interface

```bash
# Execute JASS script
jass-runner script.j

# Execute with timer simulation (10 seconds)
jass-runner script.j --simulate 10

# Disable timer system
jass-runner script.j --no-timers

# Show verbose output
jass-runner script.j --verbose
```

## Development Guide

### Environment Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run specific tests
pytest tests/path/to/test_file.py
pytest tests/path/to/test_file.py::test_function_name -v

# Code linting
flake8 src tests
```

### Project Structure

```
jass-runner/
├── pyproject.toml          # Project configuration
├── README.md              # English documentation (this file)
├── README_zh.md           # Chinese documentation
├── CLAUDE.md              # Claude Code working guide
├── PROJECT_NOTES.md       # Project progress notes
├── src/jass_runner/       # Source code
│   ├── __init__.py        # Package entry point
│   ├── parser/           # Parser layer (JASS syntax parsing, AST generation)
│   ├── interpreter/      # Interpreter layer (AST execution, variable scope)
│   ├── natives/          # Native function framework (plugin-based simulation)
│   ├── timer/           # Timer system (to be implemented - Phase 4)
│   └── vm/              # Virtual machine core (to be implemented - Phase 5)
├── tests/                # Test code
│   └── __init__.py       # Test package
├── examples/             # Example scripts
│   └── hello_world.j     # Simple example
└── docs/plans/          # Implementation plan documents
    ├── 2026-02-24-jass-simulator-design.md
    ├── 2026-02-24-jass-simulator-phase1-setup.md
    ├── 2026-02-24-jass-simulator-phase2-interpreter.md
    ├── 2026-02-24-jass-simulator-phase3-natives.md
    ├── 2026-02-24-jass-simulator-phase4-timer.md
    └── 2026-02-24-jass-simulator-phase5-vm.md
```

### Implementation Plan

The project is implemented in 5 phases, detailed plans are in the `docs/plans/` directory:

1. **Phase 1**: Project setup and core infrastructure (completed)
2. **Phase 2**: Interpreter and execution engine (completed)
3. **Phase 3**: Native function framework (completed)
4. **Phase 4**: Timer system (in progress)
5. **Phase 5**: Virtual machine core (planned)

See [docs/natives/README.md](docs/natives/README.md) for native function framework documentation.

## State Management System

JASS Runner provides a complete state management system for maintaining JASS handle states in memory.

### Core Components

- **Handle**: Base class for all JASS handles
- **Unit**: Unit handle with life, mana, and other attributes
- **HandleManager**: Centralized handle lifecycle management
- **StateContext**: Global and local state management

### Quick Example

```python
from jass_runner.natives.manager import HandleManager

# Create manager
manager = HandleManager()

# Create a unit
unit = manager.create_unit("hfoo", 0, 100.0, 200.0, 270.0)

# Query state
life = manager.get_unit_state(unit.id, "UNIT_STATE_LIFE")
print(f"Life: {life}")

# Destroy unit
manager.destroy_handle(unit.id)
```

More examples in [examples/](examples/) directory.

### Documentation

- [User Guide](docs/user_guide.md) - How to use JASS Runner
- [Timer System](docs/timer/README.md) - Timer system details
- [Native Functions](docs/natives/README.md) - Extending native functions

## Examples

### Simple Example (examples/hello_world.j)

```jass
// examples/hello_world.j
// Simple JASS test script

function main takes nothing returns nothing
    call DisplayTextToPlayer(GetLocalPlayer(), 0, 0, "Hello, World!")
endfunction
```

### Running Examples

```bash
# Run via CLI
jass-runner examples/hello_world.j

# Or via Python script
python examples/run_complete_example.py
```

## Extending Development

### Adding New Native Functions

1. Create a class inheriting from `NativeFunction` base class
2. Implement `name` property and `execute` method
3. Register in `NativeFactory.create_default_registry()`

Example:
```python
from jass_runner.natives.base import NativeFunction

class MyNative(NativeFunction):
    @property
    def name(self) -> str:
        return "MyNative"

    def execute(self, *args):
        print(f"MyNative called with {args}")
        return None
```

## License

MIT

## Related Documentation

- [Project Design Document](docs/plans/2026-02-24-jass-simulator-design.md)
- [Implementation Plans](docs/plans/)
- [Project Notes](PROJECT_NOTES.md)
- [Claude Working Guide](CLAUDE.md)
- [Timer System Documentation](docs/timer/README.md)
- [Native Function Documentation](docs/natives/README.md)