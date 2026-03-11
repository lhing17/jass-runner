"""Native函数注册表。

此模块实现了native函数的注册和管理系统，支持函数的注册、检索和查询。
支持装饰器自动注册和手动注册两种方式。
"""

import inspect
from typing import Dict, Optional, Callable, Type, Any


class NativeRegistry:
    """Native函数注册表。

    用于管理和注册JASS native函数，提供注册、检索和查询功能。
    支持装饰器自动注册和手动注册两种方式。
    """

    def __init__(self):
        """初始化native函数注册表。"""
        self._functions: Dict[str, object] = {}

    def register(self, native_function):
        """注册一个native函数。

        参数：
            native_function: 要注册的native函数实例
        """
        self._functions[native_function.name] = native_function

    def get(self, name: str) -> Optional[object]:
        """通过名称获取native函数。

        参数：
            name: native函数的名称

        返回：
            对应的native函数实例，如果不存在则返回None
        """
        return self._functions.get(name)

    def get_all(self) -> Dict[str, object]:
        """获取所有注册的native函数。

        返回：
            包含所有注册native函数的字典，键为函数名，值为函数实例
        """
        return self._functions.copy()

    def decorator(self, name: str) -> Callable:
        """创建用于自动注册native函数的装饰器。

        使用示例：
            registry = NativeRegistry()

            @registry.decorator("DisplayTextToPlayer")
            class DisplayTextToPlayer(NativeFunction):
                def execute(self, state_context, *args, **kwargs):
                    ...

        参数：
            name: native函数的名称

        返回：
            装饰器函数
        """
        def decorator_class(cls: Type[Any]) -> Type[Any]:
            """装饰器函数，注册类并返回类本身。"""
            # 创建实例并注册
            instance = cls()
            # 如果类没有name属性，设置装饰器提供的名称
            if not hasattr(instance, 'name') or instance.name is None:
                instance.name = name
            self.register(instance)
            return cls
        return decorator_class

    def auto_discover(self, module: Any) -> int:
        """自动发现并注册模块中的所有NativeFunction子类。

        扫描模块中的所有类，自动注册继承自NativeFunction且尚未注册的类。

        参数：
            module: 要扫描的模块对象

        返回：
            注册的native函数数量

        使用示例：
            from jass_runner.natives import basic
            registry.auto_discover(basic)
        """
        from .base import NativeFunction

        registered_count = 0
        for name, obj in inspect.getmembers(module):
            # 检查是否是类且继承自NativeFunction
            if (inspect.isclass(obj) and
                issubclass(obj, NativeFunction) and
                obj is not NativeFunction and
                not inspect.isabstract(obj)):

                # 尝试创建实例
                try:
                    instance = obj()
                    # 检查是否已注册（避免重复注册）
                    if instance.name not in self._functions:
                        self.register(instance)
                        registered_count += 1
                except (TypeError, NotImplementedError):
                    # 如果类需要参数或是抽象类，跳过
                    continue

        return registered_count