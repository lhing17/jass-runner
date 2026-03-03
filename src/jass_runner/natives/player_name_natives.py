"""玩家名称相关 native 函数实现。"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction

if TYPE_CHECKING:
    from .state import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class GetPlayerName(NativeFunction):
    """获取玩家名称。"""

    @property
    def name(self) -> str:
        return "GetPlayerName"

    def execute(self, state_context: 'StateContext', player: 'Player') -> str:
        """执行 GetPlayerName native 函数。"""
        return player.name
