"""JASS Group单位组类。

此模块包含JASS单位组handle的实现。
"""

from typing import Optional, Set

from .handle_base import Handle
from .unit import Unit


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

    def add_unit(self, unit: Unit) -> bool:
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

    def remove_unit(self, unit: Unit) -> bool:
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

    def contains(self, unit: Unit) -> bool:
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
