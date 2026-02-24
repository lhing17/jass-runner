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