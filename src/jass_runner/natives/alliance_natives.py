"""联盟相关 native 函数实现。

此模块包含 SetPlayerAlliance、GetPlayerAlliance 和 ConvertAllianceType
等联盟系统相关的 native 函数。
"""

import logging
from typing import TYPE_CHECKING

from .base import NativeFunction
from .alliance import get_alliance_name

if TYPE_CHECKING:
    from .manager import StateContext
    from .handle import Player

logger = logging.getLogger(__name__)


class ConvertAllianceType(NativeFunction):
    """将整数转换为联盟类型。

    在 Warcraft 3 中，这是一个类型转换函数，
    在我们的实现中直接返回传入的整数。
    """

    @property
    def name(self) -> str:
        return "ConvertAllianceType"

    def execute(self, state_context: 'StateContext', alliance_type: int) -> int:
        """执行 ConvertAllianceType。

        参数：
            state_context: 状态上下文
            alliance_type: 联盟类型整数

        返回：
            传入的联盟类型整数
        """
        logger.info(f"[ConvertAllianceType] 转换联盟类型: {alliance_type}")
        return alliance_type
