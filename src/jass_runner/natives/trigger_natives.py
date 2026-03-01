"""触发器生命周期相关的原生函数。

此模块包含JASS触发器系统中生命周期管理相关的native函数实现，
包括创建、销毁、启用和禁用触发器等功能。
"""

import logging
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class CreateTrigger(NativeFunction):
    """创建新触发器的原生函数。

    调用TriggerManager创建新触发器并返回触发器ID字符串。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "CreateTrigger"
        """
        return "CreateTrigger"

    def execute(self, state_context, *args, **kwargs):
        """执行 CreateTrigger 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            *args: 位置参数（此函数不接受额外参数）
            **kwargs: 关键字参数

        返回：
            触发器ID字符串，如果state_context或trigger_manager不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None:
            logger.error("[CreateTrigger] state_context is None")
            return None

        if not hasattr(state_context, 'trigger_manager') or state_context.trigger_manager is None:
            logger.error("[CreateTrigger] trigger_manager not found in state_context")
            return None

        # 创建新触发器
        trigger_id = state_context.trigger_manager.create_trigger()
        logger.info(f"[CreateTrigger] Created trigger: {trigger_id}")
        return trigger_id


class DestroyTrigger(NativeFunction):
    """销毁触发器的原生函数。

    调用TriggerManager销毁指定ID的触发器。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "DestroyTrigger"
        """
        return "DestroyTrigger"

    def execute(self, state_context, trigger_id: str, *args, **kwargs):
        """执行 DestroyTrigger 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要销毁的触发器ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应JASS的nothing返回类型）
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[DestroyTrigger] state_context or trigger_manager not found")
            return None

        # 销毁触发器
        success = state_context.trigger_manager.destroy_trigger(trigger_id)
        if success:
            logger.info(f"[DestroyTrigger] Destroyed trigger: {trigger_id}")
        else:
            logger.warning(f"[DestroyTrigger] Trigger not found: {trigger_id}")

        # 始终返回None（nothing）
        return None


class EnableTrigger(NativeFunction):
    """启用触发器的原生函数。

    调用TriggerManager启用指定ID的触发器。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "EnableTrigger"
        """
        return "EnableTrigger"

    def execute(self, state_context, trigger_id: str, *args, **kwargs):
        """执行 EnableTrigger 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要启用的触发器ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应JASS的nothing返回类型）
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[EnableTrigger] state_context or trigger_manager not found")
            return None

        # 启用触发器
        success = state_context.trigger_manager.enable_trigger(trigger_id)
        if success:
            logger.info(f"[EnableTrigger] Enabled trigger: {trigger_id}")
        else:
            logger.warning(f"[EnableTrigger] Trigger not found: {trigger_id}")

        # 始终返回None（nothing）
        return None


class DisableTrigger(NativeFunction):
    """禁用触发器的原生函数。

    调用TriggerManager禁用指定ID的触发器。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "DisableTrigger"
        """
        return "DisableTrigger"

    def execute(self, state_context, trigger_id: str, *args, **kwargs):
        """执行 DisableTrigger 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要禁用的触发器ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应JASS的nothing返回类型）
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[DisableTrigger] state_context or trigger_manager not found")
            return None

        # 禁用触发器
        success = state_context.trigger_manager.disable_trigger(trigger_id)
        if success:
            logger.info(f"[DisableTrigger] Disabled trigger: {trigger_id}")
        else:
            logger.warning(f"[DisableTrigger] Trigger not found: {trigger_id}")

        # 始终返回None（nothing）
        return None


class IsTriggerEnabled(NativeFunction):
    """检查触发器是否启用的原生函数。

    调用TriggerManager查询指定ID的触发器的启用状态。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "IsTriggerEnabled"
        """
        return "IsTriggerEnabled"

    def execute(self, state_context, trigger_id: str, *args, **kwargs) -> bool:
        """执行 IsTriggerEnabled 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要查询的触发器ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            bool: 触发器是否启用，触发器不存在返回False
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[IsTriggerEnabled] state_context or trigger_manager not found")
            return False

        # 查询触发器启用状态
        is_enabled = state_context.trigger_manager.is_trigger_enabled(trigger_id)
        logger.info(f"[IsTriggerEnabled] Trigger {trigger_id} enabled: {is_enabled}")
        return is_enabled


class TriggerAddAction(NativeFunction):
    """为触发器添加动作的原生函数。

    获取触发器并调用其add_action方法添加动作函数，返回动作handle。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerAddAction"
        """
        return "TriggerAddAction"

    def execute(self, state_context, trigger_id: str, action_func, *args, **kwargs):
        """执行 TriggerAddAction 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要添加动作的触发器ID
            action_func: 动作函数（可调用对象）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            动作handle字符串，如果触发器不存在则返回None
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerAddAction] state_context or trigger_manager not found")
            return None

        # 获取触发器
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if trigger is None:
            logger.warning(f"[TriggerAddAction] Trigger not found: {trigger_id}")
            return None

        # 添加动作
        action_handle = trigger.add_action(action_func)
        logger.info(f"[TriggerAddAction] Added action {action_handle} to trigger {trigger_id}")
        return action_handle


class TriggerRemoveAction(NativeFunction):
    """从触发器移除动作的原生函数。

    获取触发器并调用其remove_action方法移除指定动作。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerRemoveAction"
        """
        return "TriggerRemoveAction"

    def execute(self, state_context, trigger_id: str, action_handle: str, *args, **kwargs) -> bool:
        """执行 TriggerRemoveAction 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要移除动作的触发器ID
            action_handle: 要移除的动作handle
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            bool: 成功移除返回True，触发器或动作不存在返回False
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerRemoveAction] state_context or trigger_manager not found")
            return False

        # 获取触发器
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if trigger is None:
            logger.warning(f"[TriggerRemoveAction] Trigger not found: {trigger_id}")
            return False

        # 移除动作
        success = trigger.remove_action(action_handle)
        if success:
            logger.info(f"[TriggerRemoveAction] Removed action {action_handle} from trigger {trigger_id}")
        else:
            logger.warning(f"[TriggerRemoveAction] Action not found: {action_handle}")

        return success


class TriggerClearActions(NativeFunction):
    """清空触发器所有动作的原生函数。

    获取触发器并调用其clear_actions方法清空所有动作。
    """

    @property
    def name(self) -> str:
        """获取native函数的名称。

        返回：
            "TriggerClearActions"
        """
        return "TriggerClearActions"

    def execute(self, state_context, trigger_id: str, *args, **kwargs):
        """执行 TriggerClearActions 原生函数。

        参数：
            state_context: 状态上下文，必须包含trigger_manager
            trigger_id: 要清空动作的触发器ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应JASS的nothing返回类型）
        """
        # 检查state_context和trigger_manager存在性
        if state_context is None or not hasattr(state_context, 'trigger_manager'):
            logger.error("[TriggerClearActions] state_context or trigger_manager not found")
            return None

        # 获取触发器
        trigger = state_context.trigger_manager.get_trigger(trigger_id)
        if trigger is not None:
            # 清空动作
            trigger.clear_actions()
            logger.info(f"[TriggerClearActions] Cleared all actions from trigger {trigger_id}")
        else:
            logger.warning(f"[TriggerClearActions] Trigger not found: {trigger_id}")

        # 始终返回None（nothing）
        return None
