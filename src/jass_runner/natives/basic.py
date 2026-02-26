"""基础native函数实现。

此模块包含JASS基础native函数的实现，如DisplayTextToPlayer等。
"""

import logging
import uuid
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
        logger.info(f"[DisplayTextToPlayer]玩家{player}: {message}")
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
            logger.warning("[KillUnit]尝试击杀None单位")
            return False

        logger.info(f"[KillUnit] 单位{unit_identifier}已被击杀")
        return True


class CreateUnit(NativeFunction):
    """创建一个单位（模拟）。

    此函数模拟JASS中的CreateUnit native函数，生成唯一的单位标识符并输出日志。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"CreateUnit"
        """
        return "CreateUnit"

    def execute(self, player: int, unit_type: str, x: float, y: float, facing: float):
        """执行CreateUnit native函数。

        参数：
            player: 玩家ID
            unit_type: 单位类型代码（如'hfoo'代表步兵）
            x: X坐标
            y: Y坐标
            facing: 面向角度

        返回：
            str: 生成的单位标识符
        """
        unit_id = f"unit_{uuid.uuid4().hex[:8]}"
        logger.info(f"[CreateUnit] 为玩家{player}在({x}, {y})创建{unit_type}，单位ID: {unit_id}")
        return unit_id


class GetUnitState(NativeFunction):
    """获取单位状态（模拟）。

    此函数模拟JASS中的GetUnitState native函数，返回模拟的单位状态值。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"GetUnitState"
        """
        return "GetUnitState"

    def execute(self, unit_identifier, state_type: str):
        """执行GetUnitState native函数。

        参数：
            unit_identifier: 单位标识符
            state_type: 状态类型（如"UNIT_STATE_LIFE"表示生命值）

        返回：
            float: 单位状态值
        """
        if state_type == "UNIT_STATE_LIFE":
            # 返回模拟生命值
            return 100.0
        elif state_type == "UNIT_STATE_MANA":
            # 返回模拟魔法值
            return 50.0
        else:
            logger.warning(f"[GetUnitState] 未知状态类型: {state_type}")
            return 0.0