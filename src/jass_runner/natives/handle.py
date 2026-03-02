"""JASS handle类体系。

此模块包含所有JASS handle的基类和具体实现。
"""

from typing import Set, Optional, Dict, List


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
        self.level = 1  # 单位等级，默认为1
        self._abilities: Dict[int, int] = {}  # 技能ID -> 技能等级
        self._permanent_abilities: Set[int] = set()  # 永久技能ID集合

    def destroy(self):
        """销毁单位，将生命值设为0。"""
        self.life = 0
        self._abilities.clear()
        self._permanent_abilities.clear()
        super().destroy()

    def add_ability(self, ability_id: int) -> bool:
        """给单位添加技能。

        参数：
            ability_id: 技能ID（fourcc整数格式）

        返回：
            添加成功返回True，技能已存在返回False
        """
        if ability_id in self._abilities:
            return False
        self._abilities[ability_id] = 1  # 默认等级1
        return True

    def remove_ability(self, ability_id: int) -> bool:
        """从单位移除技能。

        参数：
            ability_id: 技能ID

        返回：
            移除成功返回True，技能不存在返回False
        """
        if ability_id not in self._abilities:
            return False
        del self._abilities[ability_id]
        self._permanent_abilities.discard(ability_id)  # 移除永久标记
        return True

    def has_ability(self, ability_id: int) -> bool:
        """检查单位是否拥有指定技能。

        参数：
            ability_id: 技能ID

        返回：
            拥有技能返回True，否则返回False
        """
        return ability_id in self._abilities

    def get_ability_level(self, ability_id: int) -> int:
        """获取技能等级。

        参数：
            ability_id: 技能ID

        返回：
            技能等级，技能不存在返回0
        """
        return self._abilities.get(ability_id, 0)

    def set_ability_level(self, ability_id: int, level: int) -> bool:
        """设置技能等级。

        参数：
            ability_id: 技能ID
            level: 新等级（必须>0）

        返回：
            设置成功返回True，技能不存在或等级无效返回False
        """
        if ability_id not in self._abilities:
            return False
        if level <= 0:
            return False
        self._abilities[ability_id] = level
        return True

    def inc_ability_level(self, ability_id: int) -> bool:
        """增加技能等级。

        参数：
            ability_id: 技能ID

        返回：
            增加成功返回True，技能不存在返回False
        """
        if ability_id not in self._abilities:
            return False
        self._abilities[ability_id] += 1
        return True

    def dec_ability_level(self, ability_id: int) -> bool:
        """降低技能等级。

        参数：
            ability_id: 技能ID

        返回：
            降低成功返回True，技能不存在或等级已为1返回False
        """
        if ability_id not in self._abilities:
            return False
        if self._abilities[ability_id] <= 1:
            return False
        self._abilities[ability_id] -= 1
        return True

    def make_ability_permanent(self, ability_id: int, permanent: bool) -> bool:
        """设置技能是否为永久技能。

        参数：
            ability_id: 技能ID
            permanent: True表示设为永久，False表示取消永久

        返回：
            设置成功返回True，技能不存在返回False
        """
        if ability_id not in self._abilities:
            return False

        if permanent:
            self._permanent_abilities.add(ability_id)
        else:
            self._permanent_abilities.discard(ability_id)

        return True

    def is_ability_permanent(self, ability_id: int) -> bool:
        """检查技能是否为永久技能。

        参数：
            ability_id: 技能ID

        返回：
            是永久技能返回True，否则返回False
        """
        return ability_id in self._permanent_abilities


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

    def get_size(self) -> int:
        """获取组内单位数量。

        返回：
            单位数量
        """
        return len(self._units)

    def unit_at(self, index: int) -> Optional[str]:
        """获取指定索引位置的单位ID。

        注意: 由于set是无序的，索引位置不保证稳定。
        这个方法主要用于BlzGroupUnitAt的兼容性实现。

        参数：
            index: 索引位置（从0开始）

        返回：
            单位ID，如果索引无效返回None
        """
        if index < 0 or index >= len(self._units):
            return None

        # 将set转换为list进行索引访问
        # 注意: 顺序不保证稳定
        units_list = list(self._units)
        return units_list[index]

    def destroy(self):
        """销毁单位组，清理所有单位引用。"""
        self.clear()
        super().destroy()


class Rect(Handle):
    """矩形区域handle。

    属性：
        min_x: 最小X坐标（左边界）
        min_y: 最小Y坐标（下边界）
        max_x: 最大X坐标（右边界）
        max_y: 最大Y坐标（上边界）
    """

    def __init__(self, rect_id: str, min_x: float, min_y: float,
                 max_x: float, max_y: float):
        """初始化矩形区域。

        参数：
            rect_id: 矩形ID
            min_x: 最小X坐标
            min_y: 最小Y坐标
            max_x: 最大X坐标
            max_y: 最大Y坐标
        """
        super().__init__(rect_id, "rect")
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def contains(self, x: float, y: float) -> bool:
        """检查点是否在矩形内。

        参数：
            x: X坐标
            y: Y坐标

        返回：
            点在矩形内返回True
        """
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y)
