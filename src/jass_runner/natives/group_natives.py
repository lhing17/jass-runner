"""单位组Native函数实现。

此模块包含JASS单位组相关native函数的实现。
"""

import logging
from .base import NativeFunction
from .handle import Group

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
