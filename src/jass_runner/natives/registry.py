"""Native函数注册表。

此模块实现了native函数的注册和管理系统，支持函数的注册、检索和查询。
"""

from typing import Dict, Optional


class NativeRegistry:
    """Native函数注册表。

    用于管理和注册JASS native函数，提供注册、检索和查询功能。
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