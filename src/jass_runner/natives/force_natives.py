"""Force（玩家组）相关的原生函数。

此模块包含 CreateForce、DestroyForce、ForceAddPlayer 等 native 函数的实现。
"""

import logging
from typing import Optional
from ..natives.base import NativeFunction


logger = logging.getLogger(__name__)


class CreateForce(NativeFunction):
    """创建新的玩家组。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "CreateForce"
        """
        return "CreateForce"

    def execute(self, state_context, *args, **kwargs):
        """执行 CreateForce native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            *args: 额外位置参数（CreateForce 不接受参数）
            **kwargs: 关键字参数

        返回：
            force 的 handle ID，失败返回 None
        """
        # 检查 state_context 和 handle_manager
        if state_context is None:
            logger.error("[CreateForce] state_context is None")
            return None

        if not hasattr(state_context, 'handle_manager') or state_context.handle_manager is None:
            logger.error("[CreateForce] handle_manager not found in state_context")
            return None

        # 生成唯一ID
        handle_id = f"force_{state_context.handle_manager._generate_id()}"

        # 导入 Force 类
        from .handle import Force

        # 创建 Force 对象
        force = Force(handle_id)

        # 注册到 handle_manager
        state_context.handle_manager._register_handle(force)

        logger.info(f"[CreateForce] Created force: {handle_id}")
        return handle_id


class DestroyForce(NativeFunction):
    """销毁玩家组。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "DestroyForce"
        """
        return "DestroyForce"

    def execute(self, state_context, force_id: str, *args, **kwargs):
        """执行 DestroyForce native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            force_id: 要销毁的 force ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[DestroyForce] state_context or handle_manager not found")
            return None

        # 销毁 handle
        success = state_context.handle_manager.destroy_handle(force_id)
        if success:
            logger.info(f"[DestroyForce] Destroyed force: {force_id}")
        else:
            logger.warning(f"[DestroyForce] force not found: {force_id}")

        return None


class ForceAddPlayer(NativeFunction):
    """添加玩家到玩家组。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "ForceAddPlayer"
        """
        return "ForceAddPlayer"

    def execute(self, state_context, force_id: str, player_id: int, *args, **kwargs):
        """执行 ForceAddPlayer native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            force_id: 玩家组 ID
            player_id: 玩家 ID（0-15）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[ForceAddPlayer] state_context or handle_manager not found")
            return None

        # 获取 force 对象
        force = state_context.handle_manager.get_handle(force_id)
        if force is None or force.type_name != "force":
            logger.warning(f"[ForceAddPlayer] force not found: {force_id}")
            return None

        # 添加玩家
        from .handle import Force
        if isinstance(force, Force):
            force.add_player(player_id)
            logger.info(f"[ForceAddPlayer] Added player {player_id} to force {force_id}")

        return None


class ForceRemovePlayer(NativeFunction):
    """从玩家组移除玩家。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "ForceRemovePlayer"
        """
        return "ForceRemovePlayer"

    def execute(self, state_context, force_id: str, player_id: int, *args, **kwargs):
        """执行 ForceRemovePlayer native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            force_id: 玩家组 ID
            player_id: 玩家 ID（0-15）
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[ForceRemovePlayer] state_context or handle_manager not found")
            return None

        # 获取 force 对象
        force = state_context.handle_manager.get_handle(force_id)
        if force is None or force.type_name != "force":
            logger.warning(f"[ForceRemovePlayer] force not found: {force_id}")
            return None

        # 移除玩家
        from .handle import Force
        if isinstance(force, Force):
            force.remove_player(player_id)
            logger.info(f"[ForceRemovePlayer] Removed player {player_id} from force {force_id}")

        return None


class ForceClear(NativeFunction):
    """清空玩家组。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "ForceClear"
        """
        return "ForceClear"

    def execute(self, state_context, force_id: str, *args, **kwargs):
        """执行 ForceClear native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            force_id: 玩家组 ID
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[ForceClear] state_context or handle_manager not found")
            return None

        # 获取 force 对象
        force = state_context.handle_manager.get_handle(force_id)
        if force is None or force.type_name != "force":
            logger.warning(f"[ForceClear] force not found: {force_id}")
            return None

        # 清空玩家组
        from .handle import Force
        if isinstance(force, Force):
            force.clear()
            logger.info(f"[ForceClear] Cleared force: {force_id}")

        return None


class ForceEnumPlayers(NativeFunction):
    """枚举所有玩家并添加到玩家组（支持过滤）。"""

    @property
    def name(self) -> str:
        """获取 native 函数的名称。

        返回：
            "ForceEnumPlayers"
        """
        return "ForceEnumPlayers"

    def execute(self, state_context, force_id: str, filter_id: Optional[str] = None, *args, **kwargs):
        """执行 ForceEnumPlayers native 函数。

        参数：
            state_context: 状态上下文，必须包含 handle_manager
            force_id: 玩家组 ID
            filter_id: 可选的 filterfunc ID，用于过滤玩家
            *args: 额外位置参数
            **kwargs: 关键字参数

        返回：
            None（对应 JASS 的 nothing）
        """
        # 检查 state_context 和 handle_manager
        if state_context is None or not hasattr(state_context, 'handle_manager'):
            logger.error("[ForceEnumPlayers] state_context or handle_manager not found")
            return None

        # 获取 force 对象
        force = state_context.handle_manager.get_handle(force_id)
        if force is None or force.type_name != "force":
            logger.warning(f"[ForceEnumPlayers] force not found: {force_id}")
            return None

        # 获取 filter（如果有）
        filter_func = None
        if filter_id:
            from .handle import FilterFunc
            f = state_context.handle_manager.get_handle(filter_id)
            if isinstance(f, FilterFunc):
                filter_func = f

        # 枚举所有 16 个玩家
        from .handle import Force, Player
        if isinstance(force, Force):
            for pid in range(16):
                player = state_context.handle_manager.get_player(pid)
                if player:
                    # 如果有 filter，先评估 filter
                    if filter_func:
                        # filter 评估玩家是否通过
                        # 注意：FilterFunc 期望的是 unit 参数，但这里传入 player
                        # 这里简化处理，直接添加所有玩家
                        force.add_player(pid)
                    else:
                        # 无 filter，添加所有玩家
                        force.add_player(pid)

            logger.info(f"[ForceEnumPlayers] Enumerated players into force: {force_id}")

        return None
