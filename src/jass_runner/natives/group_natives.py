"""单位组Native函数实现。

此模块包含JASS单位组相关native函数的实现。
"""

import logging
from typing import Optional, Callable
from .base import NativeFunction
from .handle import Group, Unit

logger = logging.getLogger(__name__)


class CreateGroup(NativeFunction):
    """创建一个新的单位组。

    对应JASS native函数: group CreateGroup()
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "CreateGroup"

    def execute(self, state_context) -> Group:
        """执行CreateGroup native函数。

        参数：
            state_context: 状态上下文

        返回：
            新创建的Group对象
        """
        handle_manager = state_context.handle_manager
        group = handle_manager.create_group()

        logger.info(f"[CreateGroup] 创建单位组，ID: {group.id}")
        return group


class DestroyGroup(NativeFunction):
    """销毁一个单位组。

    对应JASS native函数: void DestroyGroup(group whichGroup)

    注意: 销毁组不会销毁组内的单位，只是解散组。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "DestroyGroup"

    def execute(self, state_context, group: Group) -> bool:
        """执行DestroyGroup native函数。

        参数：
            state_context: 状态上下文
            group: 要销毁的单位组

        返回：
            成功销毁返回True，否则返回False
        """
        if group is None:
            logger.warning("[DestroyGroup] 尝试销毁None组")
            return False

        handle_manager = state_context.handle_manager
        success = handle_manager.destroy_handle(group.id)

        if success:
            logger.info(f"[DestroyGroup] 单位组{group.id}已销毁")
        else:
            logger.warning(f"[DestroyGroup] 单位组{group.id}不存在或已被销毁")

        return success


class GroupAddUnit(NativeFunction):
    """添加单位到单位组。

    对应JASS native函数: boolean GroupAddUnit(group whichGroup, unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupAddUnit"

    def execute(self, state_context, group: Group, unit: Unit) -> bool:
        """执行GroupAddUnit native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            unit: 要添加的单位

        返回：
            添加成功返回True，单位已在组中返回False
        """
        if group is None or unit is None:
            logger.warning("[GroupAddUnit] 组或单位为None")
            return False

        result = group.add_unit(unit)

        if result:
            logger.debug(f"[GroupAddUnit] 单位{unit.id}添加到组{group.id}")

        return result


class GroupRemoveUnit(NativeFunction):
    """从单位组移除单位。

    对应JASS native函数: boolean GroupRemoveUnit(group whichGroup, unit whichUnit)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupRemoveUnit"

    def execute(self, state_context, group: Group, unit: Unit) -> bool:
        """执行GroupRemoveUnit native函数。

        参数：
            state_context: 状态上下文
            group: 目标单位组
            unit: 要移除的单位

        返回：
            移除成功返回True，单位不在组中返回False
        """
        if group is None or unit is None:
            logger.warning("[GroupRemoveUnit] 组或单位为None")
            return False

        result = group.remove_unit(unit)

        if result:
            logger.debug(f"[GroupRemoveUnit] 单位{unit.id}从组{group.id}移除")

        return result


class GroupClear(NativeFunction):
    """清空单位组，移除所有单位。

    对应JASS native函数: void GroupClear(group whichGroup)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GroupClear"

    def execute(self, state_context, group: Group) -> bool:
        """执行GroupClear native函数。

        参数：
            state_context: 状态上下文
            group: 要清空的单位组

        返回：
            清空成功返回True
        """
        if group is None:
            logger.warning("[GroupClear] 组为None")
            return False

        group.clear()
        logger.debug(f"[GroupClear] 组{group.id}已清空")

        return True


class FirstOfGroup(NativeFunction):
    """获取单位组中的第一个单位。

    对应JASS native函数: unit FirstOfGroup(group whichGroup)

    注意: 由于Python的set是无序的，"第一个"是任意的。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "FirstOfGroup"

    def execute(self, state_context, group: Group) -> Optional[Unit]:
        """执行FirstOfGroup native函数。

        参数：
            state_context: 状态上下文
            group: 单位组

        返回：
            组内第一个单位，如果组为空返回None
        """
        if group is None:
            logger.warning("[FirstOfGroup] 组为None")
            return None

        first_unit_id = group.first()
        if first_unit_id is None:
            return None

        # 通过HandleManager获取单位对象
        handle_manager = state_context.handle_manager
        unit = handle_manager.get_unit(first_unit_id)

        return unit


class IsUnitInGroup(NativeFunction):
    """检查单位是否在单位组中。

    对应JASS native函数: boolean IsUnitInGroup(unit whichUnit, group whichGroup)
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "IsUnitInGroup"

    def execute(self, state_context, unit: Unit, group: Group) -> bool:
        """执行IsUnitInGroup native函数。

        参数：
            state_context: 状态上下文
            unit: 要检查的单位
            group: 单位组

        返回：
            单位在组中返回True，否则返回False
        """
        if group is None or unit is None:
            return False

        return group.contains(unit)


class ForGroup(NativeFunction):
    """遍历单位组中的每个单位并执行回调函数。

    对应JASS native函数: void ForGroup(group whichGroup, code callback)

    注意: 在真实JASS中，callback是code类型（函数引用）。
    这里我们使用Python的Callable来模拟。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "ForGroup"

    def execute(self, state_context, group: Group, callback: Callable[[Unit], None]):
        """执行ForGroup native函数。

        参数：
            state_context: 状态上下文
            group: 要遍历的单位组
            callback: 对每个单位执行的回调函数，接收unit参数
        """
        if group is None:
            logger.warning("[ForGroup] 组为None")
            return

        if callback is None:
            logger.warning("[ForGroup] 回调为None")
            return

        handle_manager = state_context.handle_manager
        unit_ids = group.get_units()

        for unit_id in unit_ids:
            unit = handle_manager.get_unit(unit_id)
            if unit and unit.is_alive():
                try:
                    callback(unit)
                except Exception as e:
                    logger.error(f"[ForGroup] 回调执行错误: {e}")

        logger.debug(f"[ForGroup] 遍历组{group.id}完成，处理了{len(unit_ids)}个单位")


class BlzGroupGetSize(NativeFunction):
    """获取单位组的大小（单位数量）。

    对应JASS native函数: integer BlzGroupGetSize(group whichGroup)

    这是暴雪扩展函数（Blz前缀），用于获取组内单位数量。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "BlzGroupGetSize"

    def execute(self, state_context, group: Group) -> int:
        """执行BlzGroupGetSize native函数。

        参数：
            state_context: 状态上下文
            group: 单位组

        返回：
            组内单位数量，如果组为None返回0
        """
        if group is None:
            return 0

        return group.get_size()


class BlzGroupUnitAt(NativeFunction):
    """获取单位组中指定索引的单位。

    对应JASS native函数: unit BlzGroupUnitAt(group whichGroup, integer index)

    这是暴雪扩展函数（Blz前缀），用于按索引访问组内单位。
    注意: 由于set是无序的，索引位置不保证稳定。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "BlzGroupUnitAt"

    def execute(self, state_context, group: Group, index: int) -> Optional[Unit]:
        """执行BlzGroupUnitAt native函数。

        参数：
            state_context: 状态上下文
            group: 单位组
            index: 索引位置（从0开始）

        返回：
            单位对象，如果索引无效或组为None返回None
        """
        if group is None:
            return None

        unit_id = group.unit_at(index)
        if unit_id is None:
            return None

        # 通过HandleManager获取单位对象
        handle_manager = state_context.handle_manager
        unit = handle_manager.get_unit(unit_id)

        return unit
