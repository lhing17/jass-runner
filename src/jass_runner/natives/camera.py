"""Camera 相关 native 函数实现。

此模块包含与相机相关的 JASS native 函数，如 GetCameraMargin、SetCameraBounds 等。
"""

import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class GetCameraMargin(NativeFunction):
    """获取相机边距值。"""

    @property
    def name(self) -> str:
        return "GetCameraMargin"

    def execute(self, state_context, which_margin: int) -> float:
        """执行获取相机边距。

        参数:
            state_context: 状态上下文
            which_margin: 边距类型 (0=LEFT, 1=RIGHT, 2=TOP, 3=BOTTOM)

        返回:
            边距值 (固定 100.0 表示有效范围，其他返回 0.0)
        """
        if 0 <= which_margin <= 3:
            logger.info(f"[GetCameraMargin] 边距类型={which_margin}, 返回值=100.0")
            return 100.0
        return 0.0
