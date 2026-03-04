"""JASS handle类体系。

此模块包含所有JASS handle的基类和具体实现。
"""

from typing import Set, Optional, Dict, List, Union, Tuple


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
        self.inventory: List[Optional['Item']] = [None] * 6  # 6槽位背包

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

    def add_item(self, item: 'Item', slot: int = -1) -> bool:
        """添加物品到背包，成功返回 True。

        参数：
            item: 要添加的物品
            slot: 目标槽位（-1表示自动找空槽，0-5表示指定槽位）

        返回：
            添加成功返回True，背包满或指定槽位被占返回False
        """
        if slot >= 0:
            if 0 <= slot < 6 and self.inventory[slot] is None:
                self.inventory[slot] = item
                return True
            return False
        # 自动找空槽
        for i in range(6):
            if self.inventory[i] is None:
                self.inventory[i] = item
                return True
        return False

    def remove_item(self, item: 'Item') -> bool:
        """从背包移除指定物品，成功返回 True。

        参数：
            item: 要移除的物品

        返回：
            移除成功返回True，物品不在背包中返回False
        """
        for i in range(6):
            if self.inventory[i] is item:
                self.inventory[i] = None
                return True
        return False

    def remove_item_from_slot(self, slot: int) -> bool:
        """从指定槽位移除物品，成功返回 True。

        参数：
            slot: 槽位索引（0-5）

        返回：
            移除成功返回True，槽位无效或为空返回False
        """
        if 0 <= slot < 6 and self.inventory[slot] is not None:
            self.inventory[slot] = None
            return True
        return False

    def get_item_in_slot(self, slot: int) -> Optional['Item']:
        """获取指定槽位的物品。

        参数：
            slot: 槽位索引（0-5）

        返回：
            该槽位的物品，无效槽位或空槽返回None
        """
        if 0 <= slot < 6:
            return self.inventory[slot]
        return None

    def find_item(self, item: 'Item') -> int:
        """查找物品所在槽位。

        参数：
            item: 要查找的物品

        返回：
            物品所在槽位索引（0-5），未找到返回-1
        """
        for i in range(6):
            if self.inventory[i] is item:
                return i
        return -1


class Player(Handle):
    """玩家handle。

    属性：
        player_id: 玩家ID（0-15）
        name: 玩家名称
        race: 种族（如'human', 'orc', 'undead', 'nightelf'）
        color: 玩家颜色ID
        slot_state: 插槽状态（'empty', 'closed', 'player'）
        controller: 控制器类型（'user', 'computer', 'neutral', 'rescueable'）
        _gold, _lumber: 黄金和木材
        _food_cap, _food_used: 人口上限和已用人口
        _allies: 盟友玩家ID集合
        _enemies: 敌人玩家ID集合
    """

    # 玩家状态类型常量
    PLAYER_STATE_RESOURCE_GOLD = 1
    PLAYER_STATE_RESOURCE_LUMBER = 2
    PLAYER_STATE_RESOURCE_FOOD_CAP = 4
    PLAYER_STATE_RESOURCE_FOOD_USED = 5

    def __init__(self, handle_id: str, player_id: int):
        super().__init__(handle_id, "player")
        self.player_id = player_id
        self.name = f"玩家{player_id}"
        self.race = "human"  # 默认人类
        self.color = player_id  # 默认颜色等于ID
        self.slot_state = "player" if player_id < 12 else "empty"  # 0-11为玩家，12-15为空
        self.controller = "user" if player_id < 8 else "computer" if player_id < 12 else "neutral"
        self._allies: Set[int] = set()  # 盟友玩家ID集合
        self._enemies: Set[int] = set()  # 敌人玩家ID集合
        # 资源属性（最小集）
        self._gold: int = 500         # 黄金 0-1000000，初始500
        self._lumber: int = 0         # 木材 0-1000000，初始0
        self._food_cap: int = 100     # 人口上限 0-300，初始100
        self._food_used: int = 0      # 已用人口 0-food_cap，初始0
        # 通用状态存储字典（用于非资源类状态）
        self._state_data: Dict[int, int] = {}

    def _clamp_resource(self, value: int, min_val: int, max_val: int) -> int:
        """将值截断到有效范围。

        参数：
            value: 要截断的值
            min_val: 最小值
            max_val: 最大值

        返回：
            截断后的值
        """
        return max(min_val, min(value, max_val))

    def get_state(self, state_type: int) -> int:
        """获取玩家状态值。

        参数：
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）

        返回：
            状态值

        异常：
            ValueError: 无效的状态类型
        """
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            return self._gold
        elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
            return self._lumber
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
            return self._food_cap
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
            return self._food_used
        else:
            # 其他状态从字典读取，默认为 0
            return self._state_data.get(state_type, 0)

    def set_state(self, state_type: int, value: int) -> int:
        """设置玩家状态值。

        参数：
            state_type: 状态类型（PLAYER_STATE_RESOURCE_*）
            value: 要设置的值

        返回：
            实际设置的值（超出范围时自动截断到边界）

        异常：
            ValueError: 无效的状态类型
        """
        if state_type == Player.PLAYER_STATE_RESOURCE_GOLD:
            self._gold = self._clamp_resource(value, 0, 1000000)
            return self._gold
        elif state_type == Player.PLAYER_STATE_RESOURCE_LUMBER:
            self._lumber = self._clamp_resource(value, 0, 1000000)
            return self._lumber
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_CAP:
            self._food_cap = self._clamp_resource(value, 0, 300)
            return self._food_cap
        elif state_type == Player.PLAYER_STATE_RESOURCE_FOOD_USED:
            # 已用人口不能超过人口上限
            max_food = self._food_cap
            self._food_used = self._clamp_resource(value, 0, max_food)
            return self._food_used
        else:
            # 其他状态存入字典
            self._state_data[state_type] = value
            return value

    def set_alliance(self, other_player_id: int, is_ally: bool) -> None:
        """设置与其他玩家的关系。

        参数：
            other_player_id: 其他玩家ID
            is_ally: True表示设为盟友，False表示设为敌人
        """
        if is_ally:
            self._allies.add(other_player_id)
            self._enemies.discard(other_player_id)
        else:
            self._enemies.add(other_player_id)
            self._allies.discard(other_player_id)

    def is_ally(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的盟友。

        参数：
            other_player_id: 其他玩家ID

        返回：
            是盟友返回True，否则返回False
        """
        return other_player_id in self._allies

    def is_enemy(self, other_player_id: int) -> bool:
        """检查是否是指定玩家的敌人。

        参数：
            other_player_id: 其他玩家ID

        返回：
            是敌人返回True，否则返回False
        """
        return other_player_id in self._enemies


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


class Effect(Handle):
    """特效句柄，用于标识一个已创建的特效。"""

    def __init__(self, effect_id: int, model_path: str,
                 target: Optional[Union['Unit', 'Item', Tuple[float, float, float]]] = None,
                 attach_point: Optional[str] = None):
        """初始化特效句柄。

        参数：
            effect_id: 特效唯一标识符
            model_path: 模型路径（原样保存）
            target: 绑定目标，可以是单位、物品或坐标三元组
            attach_point: 附着点名称（如 "hand", "origin"）
        """
        super().__init__(effect_id, "effect")
        self.model_path = model_path
        self.target = target
        self.attach_point = attach_point


class BoolExpr(Handle):
    """布尔表达式基类，用于条件判断和过滤。

    属性：
        _func: 包装的函数（可为None）
    """

    def __init__(self, handle_id: str):
        """初始化布尔表达式。

        参数：
            handle_id: 唯一标识符
        """
        super().__init__(handle_id, "boolexpr")
        self._func = None

    def evaluate(self, *args, **kwargs) -> bool:
        """评估表达式，返回布尔值。

        参数：
            *args, **kwargs: 传递给包装函数的参数

        返回：
            评估结果，无函数时返回False
        """
        if self._func:
            return bool(self._func(*args, **kwargs))
        return False


class ConditionFunc(BoolExpr):
    """条件函数，用于触发器条件判断。

    继承自 BoolExpr，专门用于 TriggerAddCondition。
    包装的函数不接受参数，返回布尔值。
    """

    def __init__(self, handle_id: str, func=None):
        """初始化条件函数。

        参数：
            handle_id: 唯一标识符
            func: 条件函数（无参数，返回bool）
        """
        super().__init__(handle_id)
        self.type_name = "conditionfunc"
        self._func = func

    def evaluate(self) -> bool:
        """评估条件。

        返回：
            条件函数的执行结果，无函数时返回False
        """
        if self._func:
            return bool(self._func())
        return False


class FilterFunc(BoolExpr):
    """过滤函数，用于单位组枚举过滤。

    继承自 BoolExpr，专门用于 GroupEnumUnits 等函数。
    包装的函数接受一个单位参数，返回布尔值。
    """

    def __init__(self, handle_id: str, func=None):
        """初始化过滤函数。

        参数：
            handle_id: 唯一标识符
            func: 过滤函数（接受unit参数，返回bool）
        """
        super().__init__(handle_id)
        self.type_name = "filterfunc"
        self._func = func

    def evaluate(self, unit) -> bool:
        """评估单位是否符合过滤条件。

        参数：
            unit: 要评估的单位对象

        返回：
            过滤函数的执行结果，无函数时返回False
        """
        if self._func:
            return bool(self._func(unit))
        return False
