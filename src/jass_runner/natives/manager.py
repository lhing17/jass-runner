"""Handle管理器。

此模块包含HandleManager类，负责所有handle的生命周期管理。
"""

from typing import Dict, List, Optional
from .handle import Handle, Unit, Player, Item, Group, Rect


class HandleManager:
    """集中式handle管理器。

    负责所有handle的生命周期管理。
    """

    def __init__(self):
        self._handles: Dict[str, Handle] = {}  # id -> handle对象
        self._type_index: Dict[str, List[str]] = {}  # 类型索引
        self._next_id = 1
        self._trigger_manager = None  # 触发器管理器引用
        # 初始化16个玩家（ID 0-15）
        self._init_players()

    def _init_players(self):
        """初始化16个玩家（ID 0-15）。"""
        for player_id in range(16):
            handle_id = f"player_{player_id}"
            player = Player(handle_id, player_id)
            self._register_handle(player)

    def _generate_id(self) -> int:
        """生成下一个ID。"""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def _register_handle(self, handle: Handle):
        """注册handle到管理器中。"""
        self._handles[handle.id] = handle

        # 更新类型索引
        if handle.type_name not in self._type_index:
            self._type_index[handle.type_name] = []
        self._type_index[handle.type_name].append(handle.id)

    def create_unit(self, unit_type: str, player_id: int,
                    x: float, y: float, facing: float) -> Unit:
        """创建一个单位并返回Unit对象。"""
        handle_id = f"unit_{self._generate_id()}"
        unit = Unit(handle_id, unit_type, player_id, x, y, facing)
        self._register_handle(unit)
        return unit

    def get_handle(self, handle_id: str) -> Optional[Handle]:
        """通过ID获取handle对象。"""
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive():
            return handle
        return None

    def get_unit(self, unit_id: str) -> Optional[Unit]:
        """获取单位对象，进行类型检查。"""
        handle = self.get_handle(unit_id)
        if isinstance(handle, Unit):
            return handle
        return None

    def create_item(self, item_type: str, x: float, y: float) -> Item:
        """创建一个物品并返回Item对象。"""
        handle_id = f"item_{self._generate_id()}"
        item = Item(handle_id, item_type, x, y)
        self._register_handle(item)
        return item

    def get_item(self, item_id: str) -> Optional[Item]:
        """获取物品对象，进行类型检查。"""
        handle = self.get_handle(item_id)
        if isinstance(handle, Item):
            return handle
        return None

    def get_player(self, player_id: int) -> Optional[Player]:
        """通过玩家ID获取玩家对象。

        参数：
            player_id: 玩家ID（0-15）

        返回：
            Player对象，如果ID无效则返回None
        """
        if not 0 <= player_id <= 15:
            return None
        handle_id = f"player_{player_id}"
        handle = self.get_handle(handle_id)
        if isinstance(handle, Player):
            return handle
        return None

    def get_player_by_handle(self, handle_id: str) -> Optional[Player]:
        """通过handle ID获取玩家对象。"""
        handle = self.get_handle(handle_id)
        if isinstance(handle, Player):
            return handle
        return None

    def destroy_handle(self, handle_id: str) -> bool:
        """销毁指定的handle。"""
        handle = self._handles.get(handle_id)
        if handle and handle.is_alive():
            handle.destroy()
            return True
        return False

    def get_unit_state(self, unit_id: str, state_type: str) -> float:
        """获取单位状态值。"""
        unit = self.get_unit(unit_id)
        if not unit:
            return 0.0

        if state_type == "UNIT_STATE_LIFE":
            return unit.life
        elif state_type == "UNIT_STATE_MAX_LIFE":
            return unit.max_life
        elif state_type == "UNIT_STATE_MANA":
            return unit.mana
        elif state_type == "UNIT_STATE_MAX_MANA":
            return unit.max_mana
        else:
            return 0.0

    def set_unit_state(self, unit_id: str, state_type: str, value: float) -> bool:
        """设置单位状态值。"""
        unit = self.get_unit(unit_id)
        if not unit:
            return False

        if state_type == "UNIT_STATE_LIFE":
            unit.life = value
            return True
        elif state_type == "UNIT_STATE_MAX_LIFE":
            unit.max_life = value
            return True
        elif state_type == "UNIT_STATE_MANA":
            unit.mana = value
            return True
        elif state_type == "UNIT_STATE_MAX_MANA":
            unit.max_mana = value
            return True
        else:
            return False

    def get_total_handles(self) -> int:
        """获取总handle数量。"""
        return len(self._handles)

    def get_alive_handles(self) -> int:
        """获取存活handle数量。"""
        count = 0
        for handle in self._handles.values():
            if handle.is_alive():
                count += 1
        return count

    def get_handle_type_count(self, type_name: str) -> int:
        """获取指定类型的handle数量。"""
        if type_name not in self._type_index:
            return 0
        return len(self._type_index[type_name])

    def set_trigger_manager(self, trigger_manager):
        """设置触发器管理器。

        参数：
            trigger_manager: TriggerManager实例
        """
        self._trigger_manager = trigger_manager

    def kill_unit(self, unit_id: str) -> bool:
        """杀死单位并触发死亡事件。

        参数：
            unit_id: 单位ID

        返回：
            成功杀死返回True，单位不存在返回False
        """
        # 获取单位
        unit = self.get_unit(unit_id)
        if not unit:
            return False

        # 保存单位类型
        unit_type = unit.unit_type

        # 销毁单位
        unit.destroy()

        # 触发单位死亡事件
        if self._trigger_manager:
            from ..trigger.event_types import EVENT_UNIT_DEATH
            self._trigger_manager.fire_event(EVENT_UNIT_DEATH, {
                "unit_id": unit_id,
                "unit_type": unit_type
            })

        return True

    def create_group(self) -> Group:
        """创建一个新的单位组。"""
        handle_id = f"group_{self._generate_id()}"
        group = Group(handle_id)
        self._register_handle(group)
        return group

    def get_group(self, group_id: str) -> Optional[Group]:
        """获取单位组对象，进行类型检查。"""
        handle = self.get_handle(group_id)
        if isinstance(handle, Group):
            return handle
        return None

    def enum_units_of_player(self, player_id: int) -> List[str]:
        """枚举指定玩家的所有单位。

        参数：
            player_id: 玩家ID

        返回：
            单位ID列表
        """
        result = []
        type_name = "unit"

        if type_name not in self._type_index:
            return result

        for handle_id in self._type_index[type_name]:
            handle = self._handles.get(handle_id)
            if handle and handle.is_alive() and isinstance(handle, Unit):
                if handle.player_id == player_id:
                    result.append(handle_id)

        return result

    def enum_units_in_range(self, x: float, y: float, radius: float) -> List[str]:
        """枚举指定范围内的所有单位。

        参数：
            x: 中心X坐标
            y: 中心Y坐标
            radius: 半径

        返回：
            单位ID列表
        """
        result = []
        type_name = "unit"

        if type_name not in self._type_index:
            return result

        radius_sq = radius * radius

        for handle_id in self._type_index[type_name]:
            handle = self._handles.get(handle_id)
            if handle and handle.is_alive() and isinstance(handle, Unit):
                # 计算距离平方（避免开方）
                dx = handle.x - x
                dy = handle.y - y
                dist_sq = dx * dx + dy * dy

                if dist_sq <= radius_sq:
                    result.append(handle_id)

        return result

    def enum_units_of_type(self, unit_type: str) -> List[str]:
        """枚举指定类型的所有单位。

        参数：
            unit_type: 单位类型代码（如'hfoo'）

        返回：
            单位ID列表
        """
        result = []
        type_name = "unit"

        if type_name not in self._type_index:
            return result

        for handle_id in self._type_index[type_name]:
            handle = self._handles.get(handle_id)
            if handle and handle.is_alive() and isinstance(handle, Unit):
                if handle.unit_type == unit_type:
                    result.append(handle_id)

        return result

    def create_rect(self, min_x: float, min_y: float, max_x: float, max_y: float) -> Rect:
        """创建一个新的矩形区域。"""
        handle_id = f"rect_{self._generate_id()}"
        rect = Rect(handle_id, min_x, min_y, max_x, max_y)
        self._register_handle(rect)
        return rect

    def get_rect(self, rect_id: str) -> Optional[Rect]:
        """获取矩形区域对象，进行类型检查。"""
        handle = self.get_handle(rect_id)
        if isinstance(handle, Rect):
            return handle
        return None

    def enum_units_in_rect(self, rect: Rect) -> List[str]:
        """枚举矩形区域内的所有单位。

        参数：
            rect: 矩形区域

        返回：
            单位ID列表
        """
        result = []
        type_name = "unit"

        if type_name not in self._type_index:
            return result

        for handle_id in self._type_index[type_name]:
            handle = self._handles.get(handle_id)
            if handle and handle.is_alive() and isinstance(handle, Unit):
                if rect.contains(handle.x, handle.y):
                    result.append(handle_id)

        return result
