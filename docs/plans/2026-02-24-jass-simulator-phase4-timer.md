# JASS Simulator Phase 4: Timer System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement frame-based timer system that simulates JASS timer functionality with discrete time steps for fast simulation of long-term game behavior.

**Architecture:** Create Timer class for individual timers, TimerSystem for managing multiple timers, and integrate with interpreter for timer-related native functions like CreateTimer, TimerStart, and TimerGetElapsed.

**Tech Stack:** Python 3.8+, pytest, time module for simulation

---

### Task 1: Create Timer Class

**Files:**
- Create: `src/jass_runner/timer/__init__.py`
- Create: `src/jass_runner/timer/timer.py`
- Create: `tests/timer/test_timer.py`

**Step 1: Create timer package**

```python
# src/jass_runner/timer/__init__.py
"""Timer system module."""
```

**Step 2: Write failing test for Timer class**

```python
# tests/timer/test_timer.py
"""Test Timer class."""

def test_timer_creation():
    """Test that Timer can be created."""
    from jass_runner.timer.timer import Timer

    timer = Timer(timer_id="timer_001")
    assert timer is not None
    assert timer.timer_id == "timer_001"
    assert timer.elapsed == 0.0
    assert timer.periodic is False
    assert timer.running is False
```

**Step 3: Run test to verify it fails**

Run: `pytest tests/timer/test_timer.py::test_timer_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.timer.timer'"

**Step 4: Create minimal Timer class**

```python
# src/jass_runner/timer/timer.py
"""Timer class for JASS timer simulation."""

from typing import Callable, Optional


class Timer:
    """Represents a JASS timer."""

    def __init__(self, timer_id: str):
        self.timer_id = timer_id
        self.elapsed: float = 0.0
        self.timeout: float = 0.0
        self.periodic: bool = False
        self.running: bool = False
        self.callback: Optional[Callable] = None
        self.callback_args = ()

    def start(self, timeout: float, periodic: bool, callback: Callable, *args):
        """Start the timer."""
        self.timeout = timeout
        self.periodic = periodic
        self.callback = callback
        self.callback_args = args
        self.running = True
        self.elapsed = 0.0

    def update(self, delta_time: float) -> bool:
        """Update timer with elapsed time. Returns True if timer fired."""
        if not self.running:
            return False

        self.elapsed += delta_time

        if self.elapsed >= self.timeout:
            if self.callback:
                self.callback(*self.callback_args)

            if self.periodic:
                self.elapsed = 0.0
                return True
            else:
                self.running = False
                return True

        return False

    def pause(self):
        """Pause the timer."""
        self.running = False

    def resume(self):
        """Resume the timer."""
        self.running = True

    def destroy(self):
        """Destroy the timer."""
        self.running = False
        self.callback = None
        self.callback_args = ()
```

**Step 5: Run test to verify it passes**

Run: `pytest tests/timer/test_timer.py::test_timer_creation -v`
Expected: PASS

**Step 6: Commit**

```bash
git add src/jass_runner/timer/__init__.py src/jass_runner/timer/timer.py tests/timer/test_timer.py
git commit -m "feat: add Timer class"
```

---

### Task 2: Create TimerSystem Class

**Files:**
- Create: `src/jass_runner/timer/system.py`
- Modify: `tests/timer/test_timer.py`

**Step 1: Write failing test for TimerSystem**

```python
# tests/timer/test_timer.py (add to existing file)

def test_timer_system_creation():
    """Test that TimerSystem can be created."""
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    assert system is not None
    assert hasattr(system, 'create_timer')
    assert hasattr(system, 'get_timer')
    assert hasattr(system, 'update')
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/timer/test_timer.py::test_timer_system_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.timer.system'"

**Step 3: Create TimerSystem class**

```python
# src/jass_runner/timer/system.py
"""Timer system for managing multiple timers."""

import uuid
from typing import Dict, Optional
from .timer import Timer


class TimerSystem:
    """System for managing JASS timers."""

    def __init__(self):
        self._timers: Dict[str, Timer] = {}
        self._current_time: float = 0.0

    def create_timer(self) -> str:
        """Create a new timer and return its ID."""
        timer_id = f"timer_{uuid.uuid4().hex[:8]}"
        timer = Timer(timer_id)
        self._timers[timer_id] = timer
        return timer_id

    def get_timer(self, timer_id: str) -> Optional[Timer]:
        """Get a timer by ID."""
        return self._timers.get(timer_id)

    def destroy_timer(self, timer_id: str) -> bool:
        """Destroy a timer."""
        if timer_id in self._timers:
            timer = self._timers[timer_id]
            timer.destroy()
            del self._timers[timer_id]
            return True
        return False

    def update(self, delta_time: float):
        """Update all timers with elapsed time."""
        self._current_time += delta_time

        timers_to_remove = []
        for timer_id, timer in self._timers.items():
            fired = timer.update(delta_time)
            if fired and not timer.periodic and not timer.running:
                timers_to_remove.append(timer_id)

        # Remove one-shot timers that have fired
        for timer_id in timers_to_remove:
            del self._timers[timer_id]

    def get_elapsed_time(self, timer_id: str) -> Optional[float]:
        """Get elapsed time for a timer."""
        timer = self.get_timer(timer_id)
        if timer:
            return timer.elapsed
        return None

    def pause_timer(self, timer_id: str) -> bool:
        """Pause a timer."""
        timer = self.get_timer(timer_id)
        if timer:
            timer.pause()
            return True
        return False

    def resume_timer(self, timer_id: str) -> bool:
        """Resume a timer."""
        timer = self.get_timer(timer_id)
        if timer:
            timer.resume()
            return True
        return False
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/timer/test_timer.py::test_timer_system_creation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/timer/system.py tests/timer/test_timer.py
git commit -m "feat: add TimerSystem class"
```

---

### Task 3: Add Timer-Related Native Functions

**Files:**
- Create: `src/jass_runner/natives/timer_natives.py`
- Create: `tests/natives/test_timer_natives.py`

**Step 1: Write failing test for timer natives**

```python
# tests/natives/test_timer_natives.py
"""Test timer-related native functions."""

def test_create_timer_native():
    """Test CreateTimer native function."""
    from jass_runner.natives.timer_natives import CreateTimer
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    native = CreateTimer(timer_system=system)
    assert native.name == "CreateTimer"

    # Create a timer
    timer_id = native.execute()
    assert timer_id is not None
    assert timer_id.startswith("timer_")

    # Verify timer exists in system
    timer = system.get_timer(timer_id)
    assert timer is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_timer_natives.py::test_create_timer_native -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.timer_natives'"

**Step 3: Create timer native functions**

```python
# src/jass_runner/natives/timer_natives.py
"""Timer-related native functions."""

import logging
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class CreateTimer(NativeFunction):
    """Create a new timer."""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "CreateTimer"

    def execute(self):
        """Execute CreateTimer native function."""
        timer_id = self._timer_system.create_timer()
        logger.info(f"[CreateTimer] Created timer: {timer_id}")
        return timer_id


class TimerStart(NativeFunction):
    """Start a timer."""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "TimerStart"

    def execute(self, timer_id: str, timeout: float, periodic: bool, callback_func: str, *args):
        """Execute TimerStart native function."""
        timer = self._timer_system.get_timer(timer_id)
        if not timer:
            logger.warning(f"[TimerStart] Timer not found: {timer_id}")
            return False

        # In real implementation, callback_func would be a JASS function reference
        # For now, we'll create a simple callback that logs
        def callback_wrapper():
            logger.info(f"[TimerCallback] Timer {timer_id} fired with args: {args}")

        timer.start(timeout, periodic, callback_wrapper, *args)
        logger.info(f"[TimerStart] Started timer {timer_id}: timeout={timeout}, periodic={periodic}")
        return True


class TimerGetElapsed(NativeFunction):
    """Get elapsed time for a timer."""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "TimerGetElapsed"

    def execute(self, timer_id: str):
        """Execute TimerGetElapsed native function."""
        elapsed = self._timer_system.get_elapsed_time(timer_id)
        if elapsed is None:
            logger.warning(f"[TimerGetElapsed] Timer not found: {timer_id}")
            return 0.0

        logger.info(f"[TimerGetElapsed] Timer {timer_id} elapsed: {elapsed}")
        return elapsed
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_timer_natives.py::test_create_timer_native -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/timer_natives.py tests/natives/test_timer_natives.py
git commit -m "feat: add timer-related native functions"
```

---

### Task 4: Extend NativeFactory for Timer Natives

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Modify: `tests/natives/test_factory.py`

**Step 1: Write failing test for factory with timer natives**

```python
# tests/natives/test_factory.py (add to existing file)

def test_factory_with_timer_system():
    """Test factory with timer system integration."""
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.timer.system import TimerSystem

    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    # Check timer natives are registered
    create_timer_func = registry.get("CreateTimer")
    timer_start_func = registry.get("TimerStart")
    timer_elapsed_func = registry.get("TimerGetElapsed")

    assert create_timer_func is not None
    assert create_timer_func.name == "CreateTimer"

    assert timer_start_func is not None
    assert timer_start_func.name == "TimerStart"

    assert timer_elapsed_func is not None
    assert timer_elapsed_func.name == "TimerGetElapsed"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_factory.py::test_factory_with_timer_system -v`
Expected: FAIL with "TypeError: __init__() got an unexpected keyword argument 'timer_system'"

**Step 3: Update NativeFactory to support timer system**

```python
# src/jass_runner/natives/factory.py (update existing class)

from .timer_natives import CreateTimer, TimerStart, TimerGetElapsed


class NativeFactory:
    """Factory for creating native function registries."""

    def __init__(self, timer_system=None):
        self._timer_system = timer_system

    def create_default_registry(self) -> NativeRegistry:
        """Create a registry with default native functions."""
        registry = NativeRegistry()

        # Register basic native functions
        from .basic import DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState
        registry.register(DisplayTextToPlayer())
        registry.register(KillUnit())
        registry.register(CreateUnit())
        registry.register(GetUnitState())

        # Register timer natives if timer system is available
        if self._timer_system:
            registry.register(CreateTimer(self._timer_system))
            registry.register(TimerStart(self._timer_system))
            registry.register(TimerGetElapsed(self._timer_system))

        return registry
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_factory.py::test_factory_with_timer_system -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/natives/factory.py tests/natives/test_factory.py
git commit -m "feat: extend NativeFactory for timer natives"
```

---

### Task 5: Add Frame-Based Simulation Loop

**Files:**
- Create: `src/jass_runner/timer/simulation.py`
- Create: `tests/timer/test_simulation.py`

**Step 1: Write failing test for simulation loop**

```python
# tests/timer/test_simulation.py
"""Test simulation loop."""

def test_simulation_loop_creation():
    """Test that SimulationLoop can be created."""
    from jass_runner.timer.simulation import SimulationLoop
    from jass_runner.timer.system import TimerSystem

    timer_system = TimerSystem()
    loop = SimulationLoop(timer_system=timer_system)
    assert loop is not None
    assert hasattr(loop, 'run_frames')
    assert hasattr(loop, 'current_frame')
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/timer/test_simulation.py::test_simulation_loop_creation -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.timer.simulation'"

**Step 3: Create SimulationLoop class**

```python
# src/jass_runner/timer/simulation.py
"""Frame-based simulation loop."""

import time
from typing import Callable, Optional
from .system import TimerSystem


class SimulationLoop:
    """Frame-based simulation loop for JASS timer system."""

    def __init__(self, timer_system: TimerSystem, frame_duration: float = 0.033):
        """
        Initialize simulation loop.

        Args:
            timer_system: TimerSystem instance
            frame_duration: Duration of each frame in seconds (default: 0.033 = ~30 FPS)
        """
        self.timer_system = timer_system
        self.frame_duration = frame_duration
        self.current_frame: int = 0
        self.running: bool = False
        self._frame_callback: Optional[Callable] = None

    def run_frames(self, num_frames: int):
        """Run simulation for specified number of frames."""
        self.running = True

        for frame in range(num_frames):
            self.current_frame = frame

            # Call frame callback if set
            if self._frame_callback:
                self._frame_callback(frame)

            # Update timer system with frame duration
            self.timer_system.update(self.frame_duration)

            # Simulate frame delay (in real simulation, this would be actual time)
            # For fast simulation, we don't actually sleep

        self.running = False

    def run_seconds(self, seconds: float):
        """Run simulation for specified number of seconds."""
        num_frames = int(seconds / self.frame_duration)
        self.run_frames(num_frames)

    def set_frame_callback(self, callback: Callable):
        """Set callback to be called each frame."""
        self._frame_callback = callback

    def get_simulated_time(self) -> float:
        """Get total simulated time in seconds."""
        return self.current_frame * self.frame_duration
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/timer/test_simulation.py::test_simulation_loop_creation -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/timer/simulation.py tests/timer/test_simulation.py
git commit -m "feat: add frame-based simulation loop"
```

---

### Task 6: Integrate Timer System with Interpreter

**Files:**
- Modify: `src/jass_runner/interpreter/context.py`
- Modify: `tests/interpreter/test_context.py`

**Step 1: Write failing test for interpreter with timer system**

```python
# tests/interpreter/test_context.py (add to existing file)

def test_execution_context_with_timer_system():
    """Test execution context with timer system."""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.timer.system import TimerSystem
    from jass_runner.natives.factory import NativeFactory

    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    context = ExecutionContext(native_registry=registry, timer_system=timer_system)

    # Check timer system is attached
    assert context.timer_system is timer_system

    # Check timer natives are available
    create_timer_func = context.get_native_function("CreateTimer")
    assert create_timer_func is not None
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/interpreter/test_context.py::test_execution_context_with_timer_system -v`
Expected: FAIL with "TypeError: __init__() got an unexpected keyword argument 'timer_system'"

**Step 3: Update ExecutionContext to support timer system**

```python
# src/jass_runner/interpreter/context.py (update existing class)

class ExecutionContext:
    """Execution context for JASS code."""

    def __init__(self, parent=None, native_registry=None, timer_system=None):
        self.parent = parent
        self.variables = {}
        self.native_registry = native_registry
        self.timer_system = timer_system

    def get_native_function(self, name: str):
        """Get a native function by name."""
        if self.native_registry:
            return self.native_registry.get(name)
        return None

    def get_timer_system(self):
        """Get the timer system."""
        return self.timer_system
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/interpreter/test_context.py::test_execution_context_with_timer_system -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/jass_runner/interpreter/context.py tests/interpreter/test_context.py
git commit -m "feat: integrate timer system with interpreter context"
```

---

### Task 7: Add More Timer Native Functions

**Files:**
- Modify: `src/jass_runner/natives/timer_natives.py`
- Modify: `tests/natives/test_timer_natives.py`

**Step 1: Write failing tests for additional timer natives**

```python
# tests/natives/test_timer_natives.py (add to existing file)

def test_destroy_timer_native():
    """Test DestroyTimer native function."""
    from jass_runner.natives.timer_natives import DestroyTimer
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    native = DestroyTimer(timer_system=system)

    # Create a timer first
    timer_id = system.create_timer()
    assert system.get_timer(timer_id) is not None

    # Destroy the timer
    result = native.execute(timer_id)
    assert result is True
    assert system.get_timer(timer_id) is None

def test_pause_timer_native():
    """Test PauseTimer native function."""
    from jass_runner.natives.timer_natives import PauseTimer
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    native = PauseTimer(timer_system=system)

    timer_id = system.create_timer()
    result = native.execute(timer_id)
    assert result is True
```

**Step 2: Run tests to verify they fail**

Run: `pytest tests/natives/test_timer_natives.py::test_destroy_timer_native tests/natives/test_timer_natives.py::test_pause_timer_native -v`
Expected: Both FAIL with "AttributeError: module 'jass_runner.natives.timer_natives' has no attribute 'DestroyTimer'"

**Step 3: Implement additional timer native functions**

```python
# src/jass_runner/natives/timer_natives.py (add to existing file)

class DestroyTimer(NativeFunction):
    """Destroy a timer."""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "DestroyTimer"

    def execute(self, timer_id: str):
        """Execute DestroyTimer native function."""
        success = self._timer_system.destroy_timer(timer_id)
        if success:
            logger.info(f"[DestroyTimer] Destroyed timer: {timer_id}")
        else:
            logger.warning(f"[DestroyTimer] Timer not found: {timer_id}")
        return success


class PauseTimer(NativeFunction):
    """Pause a timer."""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "PauseTimer"

    def execute(self, timer_id: str):
        """Execute PauseTimer native function."""
        success = self._timer_system.pause_timer(timer_id)
        if success:
            logger.info(f"[PauseTimer] Paused timer: {timer_id}")
        else:
            logger.warning(f"[PauseTimer] Timer not found: {timer_id}")
        return success


class ResumeTimer(NativeFunction):
    """Resume a timer."""

    def __init__(self, timer_system):
        self._timer_system = timer_system

    @property
    def name(self) -> str:
        return "ResumeTimer"

    def execute(self, timer_id: str):
        """Execute ResumeTimer native function."""
        success = self._timer_system.resume_timer(timer_id)
        if success:
            logger.info(f"[ResumeTimer] Resumed timer: {timer_id}")
        else:
            logger.warning(f"[ResumeTimer] Timer not found: {timer_id}")
        return success
```

**Step 4: Update factory to include new timer natives**

```python
# src/jass_runner/natives/factory.py (update create_default_registry method)

def create_default_registry(self) -> NativeRegistry:
    """Create a registry with default native functions."""
    registry = NativeRegistry()

    # Register basic native functions
    from .basic import DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState
    registry.register(DisplayTextToPlayer())
    registry.register(KillUnit())
    registry.register(CreateUnit())
    registry.register(GetUnitState())

    # Register timer natives if timer system is available
    if self._timer_system:
        registry.register(CreateTimer(self._timer_system))
        registry.register(TimerStart(self._timer_system))
        registry.register(TimerGetElapsed(self._timer_system))
        registry.register(DestroyTimer(self._timer_system))
        registry.register(PauseTimer(self._timer_system))
        registry.register(ResumeTimer(self._timer_system))

    return registry
```

**Step 5: Run tests to verify they pass**

Run: `pytest tests/natives/test_timer_natives.py::test_destroy_timer_native tests/natives/test_timer_natives.py::test_pause_timer_native -v`
Expected: Both PASS

**Step 6: Commit**

```bash
git add src/jass_runner/natives/timer_natives.py src/jass_runner/natives/factory.py tests/natives/test_timer_natives.py
git commit -m "feat: add DestroyTimer, PauseTimer, ResumeTimer native functions"
```

---

### Task 8: Create Timer Integration Test

**Files:**
- Create: `tests/integration/test_timer_integration.py`

**Step 1: Write timer integration test**

```python
# tests/integration/test_timer_integration.py
"""Integration tests for timer system."""

import logging
from io import StringIO

def test_timer_system_integration():
    """Test integration of timer system with native functions."""
    from jass_runner.timer.system import TimerSystem
    from jass_runner.timer.simulation import SimulationLoop
    from jass_runner.natives.factory import NativeFactory

    # Setup logging to capture output
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.timer_natives')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Create timer system and simulation
    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    # Get timer native functions
    create_timer = registry.get("CreateTimer")
    timer_start = registry.get("TimerStart")
    timer_get_elapsed = registry.get("TimerGetElapsed")

    # Create and start a timer
    timer_id = create_timer.execute()
    assert timer_id is not None

    # Track callback calls
    callback_calls = []

    def test_callback():
        callback_calls.append("called")

    # Start timer (1 second timeout, one-shot)
    timer_start.execute(timer_id, 1.0, False, test_callback)

    # Create simulation loop
    simulation = SimulationLoop(timer_system, frame_duration=0.1)  # 10 FPS for test

    # Run simulation for 0.5 seconds (should not trigger callback)
    simulation.run_seconds(0.5)
    assert len(callback_calls) == 0

    # Check elapsed time
    elapsed = timer_get_elapsed.execute(timer_id)
    assert 0.4 <= elapsed <= 0.6  # Allow some tolerance

    # Run simulation for another 0.6 seconds (should trigger callback)
    simulation.run_seconds(0.6)
    assert len(callback_calls) == 1

    # Cleanup
    logger.removeHandler(handler)

    # Check log output
    log_output = log_stream.getvalue()
    assert f"[CreateTimer] Created timer: {timer_id}" in log_output
    assert f"[TimerStart] Started timer {timer_id}" in log_output
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/integration/test_timer_integration.py::test_timer_system_integration -v`
Expected: FAIL (various errors depending on implementation)

**Step 3: Commit test file**

```bash
git add tests/integration/test_timer_integration.py
git commit -m "test: add timer system integration test"
```

---

### Task 9: Add Timer Documentation

**Files:**
- Create: `docs/timer/README.md`
- Modify: `README.md`

**Step 1: Create timer documentation**

```markdown
# Timer System

The timer system provides frame-based simulation of JASS timers for fast testing of long-term game behavior.

## Architecture

- **Timer**: Individual timer with elapsed time tracking and callback support
- **TimerSystem**: Manages multiple timers and provides CRUD operations
- **SimulationLoop**: Frame-based simulation loop for running timers
- **Timer Natives**: Native functions for timer operations (CreateTimer, TimerStart, etc.)

## Usage

```python
from jass_runner.timer.system import TimerSystem
from jass_runner.timer.simulation import SimulationLoop
from jass_runner.natives.factory import NativeFactory

# Create timer system
timer_system = TimerSystem()

# Create native factory with timer system
factory = NativeFactory(timer_system=timer_system)
registry = factory.create_default_registry()

# Get timer native functions
create_timer = registry.get("CreateTimer")
timer_start = registry.get("TimerStart")

# Create and start a timer
timer_id = create_timer.execute()

def my_callback():
    print("Timer fired!")

timer_start.execute(timer_id, 2.5, False, my_callback)

# Run simulation
simulation = SimulationLoop(timer_system)
simulation.run_seconds(3.0)  # Run for 3 simulated seconds
```

## Frame-Based Simulation

The simulation uses discrete time steps (frames) instead of real-time:

- Default frame duration: 0.033 seconds (~30 FPS)
- Timers update each frame based on elapsed simulated time
- Allows fast-forwarding through long simulations
- No real-time delays during testing

## Timer Types

- **One-shot**: Fires once after timeout
- **Periodic**: Repeats at specified interval
- **Pausable**: Can be paused and resumed
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

## Project Structure

- `src/jass_runner/parser/` - JASS parser and lexer
- `src/jass_runner/interpreter/` - Execution engine
- `src/jass_runner/natives/` - Native function framework
- `src/jass_runner/timer/` - Timer system (Phase 4)
- `src/jass_runner/vm/` - Virtual machine (Phase 5)

## Getting Started

See [docs/timer/README.md](docs/timer/README.md) for timer system documentation.
See [docs/natives/README.md](docs/natives/README.md) for native function documentation.
```

**Step 3: Commit**

```bash
git add docs/timer/README.md README.md
git commit -m "docs: add timer system documentation"
```

---

### Task 10: Add Timer Example Script

**Files:**
- Create: `examples/timer_example.j`
- Create: `examples/run_timer_example.py`

**Step 1: Create timer example JASS script**

```jass
// examples/timer_example.j
// Example JASS script demonstrating timer usage

function timer_callback takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Timer fired!")
endfunction

function periodic_callback takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Periodic timer fired!")
endfunction

function main takes nothing returns nothing
    local timer t
    local timer p

    // Create one-shot timer
    set t = CreateTimer()
    call TimerStart(t, 2.0, false, function timer_callback)

    // Create periodic timer
    set p = CreateTimer()
    call TimerStart(p, 1.0, true, function periodic_callback)

    call DisplayTextToPlayer(0, 0, 0, "Timers started!")
endfunction
```

**Step 2: Create Python script to run timer example**

```python
# examples/run_timer_example.py
"""Run timer example JASS script."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import logging
from jass_runner.parser.parser import JassParser
from jass_runner.interpreter.interpreter import JassInterpreter
from jass_runner.timer.system import TimerSystem
from jass_runner.timer.simulation import SimulationLoop
from jass_runner.natives.factory import NativeFactory

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Read JASS script
    with open('examples/timer_example.j', 'r') as f:
        jass_code = f.read()

    # Create systems
    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    # Parse and interpret
    parser = JassParser()
    ast = parser.parse(jass_code)

    interpreter = JassInterpreter(native_registry=registry, timer_system=timer_system)
    interpreter.interpret(ast)

    # Run simulation
    simulation = SimulationLoop(timer_system)
    print(f"Running simulation for 5 seconds...")
    simulation.run_seconds(5.0)
    print(f"Simulation complete. Simulated time: {simulation.get_simulated_time():.2f}s")

if __name__ == "__main__":
    main()
```

**Step 3: Commit**

```bash
git add examples/timer_example.j examples/run_timer_example.py
git commit -m "example: add timer usage example"
```

---

## Phase 4 Completion

Phase 4 implements the timer system with:

1. **Timer class** - Individual timer with elapsed time tracking
2. **TimerSystem** - Management of multiple timers
3. **Timer native functions** - CreateTimer, TimerStart, TimerGetElapsed, DestroyTimer, PauseTimer, ResumeTimer
4. **SimulationLoop** - Frame-based simulation for fast testing
5. **Interpreter integration** - Timer system available in execution context
6. **Documentation and examples** - Usage guide and example scripts

**Key Features:**
- Frame-based simulation (not real-time)
- Support for one-shot and periodic timers
- Pause/resume functionality
- Fast-forward simulation for testing long-term behavior
- Integration with native function framework

**Next Phase:** Phase 5 will implement the virtual machine integration and finalize the JASS runner.

---

Plan complete and saved to `docs/plans/2026-02-24-jass-simulator-phase4-timer.md`.

Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**