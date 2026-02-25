"""JASS解释器的执行上下文。"""

from typing import Dict, Any, Optional


class ExecutionContext:
    """表示具有变量作用域的执行上下文。"""

    def __init__(self, parent: Optional['ExecutionContext'] = None, native_registry=None):
        self.variables: Dict[str, Any] = {}
        self.parent = parent
        self.native_registry = native_registry

    def set_variable(self, name: str, value: Any):
        """在此上下文中设置变量。"""
        self.variables[name] = value

    def get_variable(self, name: str) -> Any:
        """从此上下文或父上下文获取变量。"""
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            raise NameError(f"Variable '{name}' not found")

    def has_variable(self, name: str) -> bool:
        """检查变量是否在此上下文或父上下文中存在。"""
        if name in self.variables:
            return True
        elif self.parent:
            return self.parent.has_variable(name)
        else:
            return False

    def get_native_function(self, name: str):
        """通过名称获取native函数。

        参数：
            name: native函数名称

        返回：
            NativeFunction实例或None（如果未找到）
        """
        if self.native_registry:
            return self.native_registry.get(name)
        return None