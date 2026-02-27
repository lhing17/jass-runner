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
