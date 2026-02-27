"""Native函数工厂。

此模块包含NativeFactory类，用于创建预配置的native函数注册表。
"""

from .registry import NativeRegistry
from .basic import DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState, CreateItem, RemoveItem
from .timer_natives import CreateTimer, TimerStart, TimerGetElapsed


class NativeFactory:
    """Native函数工厂。

    此类负责创建预配置的native函数注册表，简化注册过程。
    """

    def __init__(self, timer_system=None):
        """初始化工厂。

        参数：
            timer_system: 可选的计时器系统实例
        """
        self._timer_system = timer_system

    def create_default_registry(self) -> NativeRegistry:
        """创建包含默认native函数的注册表。

        返回：
            NativeRegistry: 包含DisplayTextToPlayer、KillUnit、CreateUnit和GetUnitState的注册表
        """
        registry = NativeRegistry()

        # 注册基础native函数
        registry.register(DisplayTextToPlayer())
        registry.register(KillUnit())
        registry.register(CreateUnit())
        registry.register(GetUnitState())
        registry.register(CreateItem())
        registry.register(RemoveItem())

        # 如果计时器系统可用，注册计时器原生函数
        if self._timer_system:
            registry.register(CreateTimer(self._timer_system))
            registry.register(TimerStart(self._timer_system))
            registry.register(TimerGetElapsed(self._timer_system))

        return registry