"""KK对战平台扩展API native函数实现。

此模块包含KK对战平台（KKAPI.j）扩展的native函数实现。
这些函数在标准JASS基础上提供了额外的功能。
"""

import logging
from .base import NativeFunction


logger = logging.getLogger(__name__)


class DzUnlockOpCodeLimit(NativeFunction):
    """解锁JASS字节码限制。

    此函数是KK对战平台的扩展API，用于解除JASS字节码的执行限制。
    在模拟环境中仅记录日志，不做实际操作。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"DzUnlockOpCodeLimit"
        """
        return "DzUnlockOpCodeLimit"

    @property
    def source(self) -> str:
        """获取native函数来源。

        返回：
            "KKAPI.j" 表示这是KK对战平台扩展API
        """
        return "KKAPI.j"

    def execute(self, state_context, enable: bool):
        """执行DzUnlockOpCodeLimit native函数。

        参数：
            state_context: 状态上下文
            enable: 是否启用解锁（True为解锁，False为关闭）

        返回：
            None
        """
        status = "启用" if enable else "禁用"
        logger.info(f"[DzUnlockOpCodeLimit] {status}JASS字节码限制解锁（KK平台扩展API）")
        return None
