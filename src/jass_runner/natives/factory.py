"""Native函数工厂。

此模块包含NativeFactory类，用于创建预配置的native函数注册表。
"""

from .registry import NativeRegistry
from .basic import DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState


class NativeFactory:
    """Native函数工厂。

    此类负责创建预配置的native函数注册表，简化注册过程。
    """

    @staticmethod
    def create_default_registry() -> NativeRegistry:
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

        return registry