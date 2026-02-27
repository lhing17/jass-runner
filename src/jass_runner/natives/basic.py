"""基础native函数实现。

此模块包含JASS基础native函数的实现，如DisplayTextToPlayer等。
"""

import logging
from .base import NativeFunction
from .handle import Unit, Item, Player
from ..utils import int_to_fourcc


logger = logging.getLogger(__name__)

# 单位状态常量
UNIT_STATE_LIFE = 0
UNIT_STATE_MAX_LIFE = 1
UNIT_STATE_MANA = 2
UNIT_STATE_MAX_MANA = 3


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

    def execute(self, state_context, player: Player, x: float, y: float, message: str):
        """执行DisplayTextToPlayer native函数。

        参数：
            state_context: 状态上下文
            player: Player对象
            x: X坐标（游戏中未使用，仅保持接口兼容）
            y: Y坐标（游戏中未使用，仅保持接口兼容）
            message: 要显示的文本消息

        返回：
            None
        """
        player_id = player.player_id if player else -1
        logger.info(f"[DisplayTextToPlayer]玩家{player_id}: {message}")
        return None


class KillUnit(NativeFunction):
    """杀死一个单位（通过状态管理系统）。

    此函数模拟JASS中的KillUnit native函数，通过HandleManager真正销毁单位。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"KillUnit"
        """
        return "KillUnit"

    def execute(self, state_context, unit: Unit):
        """执行KillUnit native函数。

        参数：
            state_context: 状态上下文
            unit: Unit对象（由CreateUnit返回）

        返回：
            bool: 成功杀死单位返回True，否则返回False
        """
        if unit is None:
            logger.warning("[KillUnit]尝试击杀None单位")
            return False

        # 通过HandleManager销毁单位
        handle_manager = state_context.handle_manager
        success = handle_manager.destroy_handle(unit.id)

        if success:
            logger.info(f"[KillUnit] 单位{unit.id}已被击杀")
        else:
            logger.warning(f"[KillUnit] 单位{unit.id}不存在或已被销毁")

        return success


class CreateUnit(NativeFunction):
    """创建一个单位（通过状态管理系统）。

    此函数模拟JASS中的CreateUnit native函数，通过HandleManager真正创建单位。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"CreateUnit"
        """
        return "CreateUnit"

    def execute(self, state_context, player: int, unit_type: int,
                x: float, y: float, facing: float) -> Unit:
        """执行CreateUnit native函数。

        参数：
            state_context: 状态上下文
            player: 玩家ID
            unit_type: 单位类型代码（fourcc整数格式，如1213484355代表'hfoo'）
            x: X坐标
            y: Y坐标
            facing: 面向角度

        返回：
            Unit: 生成的Unit对象
        """
        # 将fourcc整数转换为字符串（如1213484355 -> 'hfoo'）
        unit_type_str = int_to_fourcc(unit_type)

        # 通过HandleManager创建单位
        handle_manager = state_context.handle_manager
        unit = handle_manager.create_unit(unit_type_str, player, x, y, facing)

        logger.info(f"[CreateUnit] 为玩家{player}在({x}, {y})创建{unit_type_str}，单位ID: {unit.id}")
        return unit


class GetUnitState(NativeFunction):
    """获取单位状态（通过状态管理系统）。

    此函数模拟JASS中的GetUnitState native函数，从HandleManager查询真实单位状态。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"GetUnitState"
        """
        return "GetUnitState"

    def execute(self, state_context, unit: Unit, state_type: int) -> float:
        """执行GetUnitState native函数。

        参数：
            state_context: 状态上下文
            unit: Unit对象（由CreateUnit返回）
            state_type: 状态类型常量（如UNIT_STATE_LIFE=0表示生命值）

        返回：
            float: 单位状态值
        """
        if unit is None:
            return 0.0

        # 将整数状态类型转换为字符串
        state_map = {
            UNIT_STATE_LIFE: "UNIT_STATE_LIFE",
            UNIT_STATE_MAX_LIFE: "UNIT_STATE_MAX_LIFE",
            UNIT_STATE_MANA: "UNIT_STATE_MANA",
            UNIT_STATE_MAX_MANA: "UNIT_STATE_MAX_MANA",
        }

        state_str = state_map.get(state_type)
        if state_str is None:
            logger.warning(f"[GetUnitState] 未知状态类型: {state_type}")
            return 0.0

        # 通过HandleManager查询单位状态
        handle_manager = state_context.handle_manager
        value = handle_manager.get_unit_state(unit.id, state_str)

        return value


class CreateItem(NativeFunction):
    """创建一个物品（通过状态管理系统）。

    此函数模拟JASS中的CreateItem native函数，通过HandleManager真正创建物品。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"CreateItem"
        """
        return "CreateItem"

    def execute(self, state_context, item_type: int, x: float, y: float) -> Item:
        """执行CreateItem native函数。

        参数：
            state_context: 状态上下文
            item_type: 物品类型代码（fourcc整数格式）
            x: X坐标
            y: Y坐标

        返回：
            Item: 生成的Item对象
        """
        # 将fourcc整数转换为字符串
        item_type_str = int_to_fourcc(item_type)

        # 通过HandleManager创建物品
        handle_manager = state_context.handle_manager
        item = handle_manager.create_item(item_type_str, x, y)

        logger.info(f"[CreateItem] 在({x}, {y})创建{item_type_str}，物品ID: {item.id}")
        return item


class RemoveItem(NativeFunction):
    """移除一个物品（通过状态管理系统）。

    此函数模拟JASS中的RemoveItem native函数，通过HandleManager真正销毁物品。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"RemoveItem"
        """
        return "RemoveItem"

    def execute(self, state_context, item: Item):
        """执行RemoveItem native函数。

        参数：
            state_context: 状态上下文
            item: Item对象（由CreateItem返回）

        返回：
            None
        """
        if item is None:
            logger.warning("[RemoveItem] 尝试移除None物品")
            return

        # 通过HandleManager销毁物品
        handle_manager = state_context.handle_manager
        success = handle_manager.destroy_handle(item.id)

        if success:
            logger.info(f"[RemoveItem] 物品{item.id}已被移除")
        else:
            logger.warning(f"[RemoveItem] 物品{item.id}不存在或已被移除")


class PlayerNative(NativeFunction):
    """获取Player对象（通过player_id）。

    此函数模拟JASS中的Player native函数，通过HandleManager获取或创建Player对象。
    """

    @property
    def name(self) -> str:
        """获取函数名称。

        返回：
            函数名称"Player"
        """
        return "Player"

    def execute(self, state_context, player_id: int) -> Player:
        """执行Player native函数。

        参数：
            state_context: 状态上下文
            player_id: 玩家ID（0-15）

        返回：
            Player: Player对象
        """
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(player_id)
        return player
