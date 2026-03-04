"""JASS Unit单位类。

此模块包含JASS单位handle的实现。
"""

from typing import Dict, List, Optional, Set

from .handle_base import Handle


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
