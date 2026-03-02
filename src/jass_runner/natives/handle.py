"""JASS handle类体系。

此模块包含所有JASS handle的基类和具体实现。
"""

from typing import Set, Optional


class Handle:
    """所有JASS handle的基类。

    属性：
        id: 唯一标识符（字符串）
        type_name: handle类型名称
        alive: 是否存活
    """

    def __init__(self, handle_id: str, type_name: str):
        self.id = handle_id
        self.type_name = type_name
        self.alive = True

    def destroy(self):
        """标记handle为销毁状态。"""
        self.alive = False

    def is_alive(self) -> bool:
        """检查handle是否存活。"""
        return self.alive


class Unit(Handle):
    """单位handle。

    属性：
        unit_type: 单位类型代码（如'hfoo'）
        player_id: 所属玩家ID
        x, y: 位置坐标
        facing: 面向角度
        life: 当前生命值
        max_life: 最大生命值
        mana: 当前魔法值
        max_mana: 最大魔法值
        name: 单位名称，默认为unit_type
    """

    def __init__(self, handle_id: str, unit_type: str, player_id: int,
                 x: float, y: float, facing: float, name: str = None):
        super().__init__(handle_id, "unit")
        self.unit_type = unit_type
        self.player_id = player_id
        self.x = x
        self.y = y
        self.z = 0.0  # Z轴高度，默认为0
        self.facing = facing
        self.life = 100.0
        self.max_life = 100.0
        self.mana = 50.0
        self.max_mana = 50.0
        self.name = name or unit_type  # 如果没有提供名称，使用单位类型

    def destroy(self):
        """销毁单位，将生命值设为0。"""
        self.life = 0
        super().destroy()


class Player(Handle):
    """玩家handle。

    属性：
        player_id: 玩家ID（0-15）
        name: 玩家名称
        race: 种族（如'human', 'orc', 'undead', 'nightelf'）
        color: 玩家颜色ID
        slot_state: 插槽状态（'empty', 'closed', 'player'）
        controller: 控制器类型（'user', 'computer', 'neutral', 'rescueable'）
    """

    def __init__(self, handle_id: str, player_id: int):
        super().__init__(handle_id, "player")
        self.player_id = player_id
        self.name = f"玩家{player_id}"
        self.race = "human"  # 默认人类
        self.color = player_id  # 默认颜色等于ID
        self.slot_state = "player" if player_id < 12 else "empty"  # 0-11为玩家，12-15为空
        self.controller = "user" if player_id < 8 else "computer" if player_id < 12 else "neutral"


class Item(Handle):
    """物品handle。

    属性：
        item_type: 物品类型代码（如'ratf'代表攻击之爪）
        x, y: 位置坐标
    """

    def __init__(self, handle_id: str, item_type: str, x: float, y: float):
        super().__init__(handle_id, "item")
        self.item_type = item_type
        self.x = x
        self.y = y


class Group(Handle):
    """单位组，包含一组单位的引用。

    用于管理一组相关单位，支持添加、移除、遍历等操作。
    """

    def __init__(self, group_id: str):
        """初始化单位组。

        参数：
            group_id: 组的唯一标识符
        """
        super().__init__(group_id, "group")
        self._units: Set[str] = set()  # 存储单位ID集合

    def add_unit(self, unit: 'Unit') -> bool:
        """添加单位到组。

        参数：
            unit: 要添加的单位

        返回：
            如果添加成功返回True，单位已在组中返回False
        """
        if not isinstance(unit, Unit):
            return False
        if not unit.is_alive():
            return False
        if unit.id in self._units:
            return False
        self._units.add(unit.id)
        return True

    def remove_unit(self, unit: 'Unit') -> bool:
        """从组中移除单位。

        参数：
            unit: 要移除的单位

        返回：
            如果移除成功返回True，单位不在组中返回False
        """
        if not unit:
            return False
        if unit.id not in self._units:
            return False
        self._units.remove(unit.id)
        return True

    def clear(self):
        """清空单位组，移除所有单位。"""
        self._units.clear()

    def first(self) -> Optional[str]:
        """获取组内第一个单位的ID。

        返回：
            第一个单位的ID，如果组为空返回None
        """
        if not self._units:
            return None
        return next(iter(self._units))

    def contains(self, unit: 'Unit') -> bool:
        """检查单位是否在组内。

        参数：
            unit: 要检查的单位

        返回：
            如果单位在组中返回True，否则返回False
        """
        if not unit:
            return False
        return unit.id in self._units

    def get_units(self) -> Set[str]:
        """获取组内所有单位的ID集合。

        返回：
            单位ID的集合副本
        """
        return self._units.copy()

    def size(self) -> int:
        """获取组内单位数量。

        返回：
            单位数量
        """
        return len(self._units)

    def destroy(self):
        """销毁单位组，清理所有单位引用。"""
        self.clear()
        super().destroy()
