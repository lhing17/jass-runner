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


class SetCameraBounds(NativeFunction):
    """设置相机边界。"""

    @property
    def name(self) -> str:
        return "SetCameraBounds"

    def execute(self, state_context, x1: float, y1: float, x2: float, y2: float,
                x3: float, y3: float, x4: float, y4: float) -> None:
        """执行设置相机边界。

        参数:
            state_context: 状态上下文
            x1, y1: 第一个角点坐标
            x2, y2: 第二个角点坐标
            x3, y3: 第三个角点坐标
            x4, y4: 第四个角点坐标
        """
        bounds = state_context.camera_bounds
        bounds['x1'] = x1
        bounds['y1'] = y1
        bounds['x2'] = x2
        bounds['y2'] = y2
        bounds['x3'] = x3
        bounds['y3'] = y3
        bounds['x4'] = x4
        bounds['y4'] = y4

        logger.info(
            f"[SetCameraBounds] 相机边界已设置: "
            f"({x1},{y1})-({x2},{y2})-({x3},{y3})-({x4},{y4})"
        )


class GetCameraBoundMinX(NativeFunction):
    """获取相机边界最小X坐标。"""

    @property
    def name(self) -> str:
        return "GetCameraBoundMinX"

    def execute(self, state_context) -> float:
        """执行获取相机边界最小X坐标。

        参数:
            state_context: 状态上下文

        返回:
            相机边界最小X坐标
        """
        bounds = state_context.camera_bounds
        x_coords = [bounds.get('x1', 0.0), bounds.get('x2', 0.0),
                    bounds.get('x3', 0.0), bounds.get('x4', 0.0)]
        min_x = min(x_coords)
        logger.info(f"[GetCameraBoundMinX] 返回最小X坐标: {min_x}")
        return min_x


class GetCameraBoundMaxX(NativeFunction):
    """获取相机边界最大X坐标。"""

    @property
    def name(self) -> str:
        return "GetCameraBoundMaxX"

    def execute(self, state_context) -> float:
        """执行获取相机边界最大X坐标。

        参数:
            state_context: 状态上下文

        返回:
            相机边界最大X坐标
        """
        bounds = state_context.camera_bounds
        x_coords = [bounds.get('x1', 0.0), bounds.get('x2', 0.0),
                    bounds.get('x3', 0.0), bounds.get('x4', 0.0)]
        max_x = max(x_coords)
        logger.info(f"[GetCameraBoundMaxX] 返回最大X坐标: {max_x}")
        return max_x


class GetCameraBoundMinY(NativeFunction):
    """获取相机边界最小Y坐标。"""

    @property
    def name(self) -> str:
        return "GetCameraBoundMinY"

    def execute(self, state_context) -> float:
        """执行获取相机边界最小Y坐标。

        参数:
            state_context: 状态上下文

        返回:
            相机边界最小Y坐标
        """
        bounds = state_context.camera_bounds
        y_coords = [bounds.get('y1', 0.0), bounds.get('y2', 0.0),
                    bounds.get('y3', 0.0), bounds.get('y4', 0.0)]
        min_y = min(y_coords)
        logger.info(f"[GetCameraBoundMinY] 返回最小Y坐标: {min_y}")
        return min_y


class GetCameraBoundMaxY(NativeFunction):
    """获取相机边界最大Y坐标。"""

    @property
    def name(self) -> str:
        return "GetCameraBoundMaxY"

    def execute(self, state_context) -> float:
        """执行获取相机边界最大Y坐标。

        参数:
            state_context: 状态上下文

        返回:
            相机边界最大Y坐标
        """
        bounds = state_context.camera_bounds
        y_coords = [bounds.get('y1', 0.0), bounds.get('y2', 0.0),
                    bounds.get('y3', 0.0), bounds.get('y4', 0.0)]
        max_y = max(y_coords)
        logger.info(f"[GetCameraBoundMaxY] 返回最大Y坐标: {max_y}")
        return max_y


class SetDayNightModels(NativeFunction):
    """设置昼夜模型路径。"""

    @property
    def name(self) -> str:
        return "SetDayNightModels"

    def execute(self, state_context, terrain_model: str, sky_model: str) -> None:
        """执行设置昼夜模型。

        参数:
            state_context: 状态上下文
            terrain_model: 地形模型文件路径
            sky_model: 天空模型文件路径
        """
        logger.info(
            f"[SetDayNightModels] 昼夜模型已设置: "
            f"地形模型={terrain_model}, 天空模型={sky_model}"
        )
