"""Basic native function implementations."""

import logging
from .base import NativeFunction


logger = logging.getLogger(__name__)


class DisplayTextToPlayer(NativeFunction):
    """Display text to a player (simulated with console output)."""

    @property
    def name(self) -> str:
        return "DisplayTextToPlayer"

    def execute(self, player: int, x: float, y: float, message: str):
        """Execute DisplayTextToPlayer native function."""
        logger.info(f"[DisplayTextToPlayer] Player {player}: {message}")
        return None