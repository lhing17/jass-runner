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

    def execute(self, state_context, *args, **kwargs):
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

    def execute(self, state_context, timer_id: str, timeout: float, periodic: bool, callback_func: str, *args):
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

    def execute(self, state_context, timer_id: str):
        """Execute TimerGetElapsed native function."""
        elapsed = self._timer_system.get_elapsed_time(timer_id)
        if elapsed is None:
            logger.warning(f"[TimerGetElapsed] Timer not found: {timer_id}")
            return 0.0

        logger.info(f"[TimerGetElapsed] Timer {timer_id} elapsed: {elapsed}")
        return elapsed
