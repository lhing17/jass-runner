"""基础native函数实现。

此模块包含JASS基础native函数的实现，如DisplayTextToPlayer等。
"""

import logging
from .base import NativeFunction


logger = logging.getLogger(__name__)


class DisplayTextToPlayer(NativeFunction):
    """向玩家显示文本（通过控制台输出模拟）。

    此函数模拟JASS中的DisplayTextToPlayer native函数，将文本消息输出到日志。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"DisplayTextToPlayer"
        """
        return "DisplayTextToPlayer"

    def execute(self, player: int, x: float, y: float, message: str):
        """执行DisplayTextToPlayer native函数。

        参数：
            player: 玩家ID
            x: X坐标（游戏中未使用，仅保持接口兼容）
            y: Y坐标（游戏中未使用，仅保持接口兼容）
            message: 要显示的文本消息

        返回：
            None
        """
        logger.info(f"[DisplayTextToPlayer] Player {player}: {message}")
        return None


class KillUnit(NativeFunction):
    """杀死一个单位（通过控制台输出模拟）。

    此函数模拟JASS中的KillUnit native函数，将单位死亡信息输出到日志。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"KillUnit"
        """
        return "KillUnit"

    def execute(self, unit_identifier):
        """执行KillUnit native函数。

        参数：
            unit_identifier: 单位标识符

        返回：
            bool: 成功杀死单位返回True，否则返回False
        """
        if unit_identifier is None:
            logger.warning("[KillUnit] Attempted to kill None unit")
            return False

        logger.info(f"[KillUnit] Unit {unit_identifier} has been killed")
        return True