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
