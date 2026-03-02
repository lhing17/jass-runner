"""单位位置操作 native 函数实现。

此模块包含单位位置设置和修改的 native 函数。
"""

import logging
from .base import NativeFunction
from .handle import Unit
from .location import Location
from ..utils import int_to_fourcc

logger = logging.getLogger(__name__)


class SetUnitPosition(NativeFunction):
    """设置单位位置（使用坐标）。"""

    @property
    def name(self) -> str:
        return "SetUnitPosition"

    def execute(self, state_context, unit: Unit, x: float, y: float):
        """执行 SetUnitPosition native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            x: 新的 X 坐标
            y: 新的 Y 坐标
        """
        if unit is None:
            logger.warning("[SetUnitPosition] 尝试设置 None 单位的位置")
            return

        unit.x = float(x)
        unit.y = float(y)

        logger.debug(f"[SetUnitPosition] 单位 {unit.id} 位置设置为 ({x}, {y})")


class SetUnitPositionLoc(NativeFunction):
    """设置单位位置（使用 Location）。"""

    @property
    def name(self) -> str:
        return "SetUnitPositionLoc"

    def execute(self, state_context, unit: Unit, loc: Location):
        """执行 SetUnitPositionLoc native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            loc: Location 位置对象
        """
        if unit is None:
            logger.warning("[SetUnitPositionLoc] 尝试设置 None 单位的位置")
            return

        if loc is None:
            logger.warning("[SetUnitPositionLoc] Location 为 None")
            return

        unit.x = loc.x
        unit.y = loc.y
        unit.z = loc.z

        logger.debug(f"[SetUnitPositionLoc] 单位 {unit.id} 位置设置为 ({loc.x}, {loc.y}, {loc.z})")


class CreateUnitAtLoc(NativeFunction):
    """在指定位置创建单位（使用 Location）。"""

    @property
    def name(self) -> str:
        return "CreateUnitAtLoc"

    def execute(self, state_context, player_id: int, unit_type: int,
                loc: Location, facing: float):
        """执行 CreateUnitAtLoc native 函数。

        参数：
            state_context: 状态上下文
            player_id: 玩家 ID
            unit_type: 单位类型代码（fourcc 整数格式）
            loc: Location 位置对象
            facing: 面向角度

        返回：
            Unit: 创建的单位对象
        """
        if loc is None:
            logger.warning("[CreateUnitAtLoc] Location 为 None")
            return None

        # 将 fourcc 整数转换为字符串
        unit_type_str = int_to_fourcc(unit_type)

        # 通过 HandleManager 创建单位
        handle_manager = state_context.handle_manager
        unit = handle_manager.create_unit(unit_type_str, player_id,
                                          loc.x, loc.y, facing)

        # 设置 z 坐标
        unit.z = loc.z

        logger.info(f"[CreateUnitAtLoc] 为玩家 {player_id} 在 {loc} 创建 {unit_type_str}，单位 ID: {unit.id}")
        return unit


class GetUnitFacing(NativeFunction):
    """获取单位朝向角度。"""

    @property
    def name(self) -> str:
        return "GetUnitFacing"

    def execute(self, state_context, unit: Unit) -> float:
        """执行 GetUnitFacing native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象

        返回：
            float: 单位朝向角度（度）
        """
        if unit is None:
            return 0.0
        return unit.facing


class SetUnitFacing(NativeFunction):
    """设置单位朝向角度。"""

    @property
    def name(self) -> str:
        return "SetUnitFacing"

    def execute(self, state_context, unit: Unit, facing_angle: float):
        """执行 SetUnitFacing native 函数。

        参数：
            state_context: 状态上下文
            unit: 单位对象
            facing_angle: 新的朝向角度（度）
        """
        if unit is None:
            logger.warning("[SetUnitFacing] 尝试设置 None 单位的朝向")
            return

        unit.facing = float(facing_angle)
        logger.debug(f"[SetUnitFacing] 单位 {unit.id} 朝向设置为 {facing_angle}")


class CreateUnitAtLocByName(NativeFunction):
    """在指定位置按名称创建单位。"""

    @property
    def name(self) -> str:
        return "CreateUnitAtLocByName"

    def execute(self, state_context, player_id: int, unit_name: str,
                loc: Location, facing: float):
        """执行 CreateUnitAtLocByName native 函数。

        参数：
            state_context: 状态上下文
            player_id: 玩家 ID
            unit_name: 单位名称（如 "footman"）
            loc: Location 位置对象
            facing: 面向角度

        返回：
            Unit: 创建的单位对象
        """
        if loc is None:
            logger.warning("[CreateUnitAtLocByName] Location 为 None")
            return None

        if not unit_name:
            logger.warning("[CreateUnitAtLocByName] 单位名称为空")
            return None

        # 名称到单位类型的映射（简化实现）
        name_to_type = {
            "footman": "hfoo",
            "peasant": "hpea",
            "knight": "hkni",
            "archer": "earc",
            "grunt": "ogru",
        }

        unit_type = name_to_type.get(unit_name.lower(), unit_name[:4].lower())

        # 通过 HandleManager 创建单位
        handle_manager = state_context.handle_manager
        unit = handle_manager.create_unit(unit_type, player_id,
                                          loc.x, loc.y, facing)

        # 设置 z 坐标和名称
        unit.z = loc.z
        unit.name = unit_name

        logger.info(f"[CreateUnitAtLocByName] 为玩家 {player_id} 在 {loc} 创建 {unit_name} ({unit_type})，单位 ID: {unit.id}")
        return unit
