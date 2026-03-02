"""JASS运行时类型检查器。"""

from typing import Any
from .errors import JassTypeError
from .hierarchy import TypeHierarchy


class TypeChecker:
    """JASS运行时类型检查器。

    负责验证类型兼容性并执行允许的隐式类型转换。

    支持的隐式转换：
    - integer -> real
    - handle子类型 -> handle
    """

    # 允许的隐式转换规则: {目标类型: [允许的来源类型列表]}
    _ALLOWED_IMPLICIT_CONVERSIONS = {
        'real': ['integer'],
    }

    def is_compatible(self, source_type: str, target_type: str) -> bool:
        """判断源类型是否可以隐式赋值给目标类型。

        规则：
        1. 类型完全相同：允许
        2. 目标类型在转换规则中且源类型在允许列表中：允许
        3. handle子类型可赋值给handle父类型：允许

        参数：
            source_type: 源类型名称
            target_type: 目标类型名称

        返回：
            如果兼容返回True，否则返回False
        """
        # 类型完全相同
        if source_type == target_type:
            return True

        # 检查handle子类型协变
        if target_type == 'handle':
            return TypeHierarchy.is_subtype(source_type, 'handle')

        # 检查隐式转换规则
        if target_type in self._ALLOWED_IMPLICIT_CONVERSIONS:
            allowed_sources = self._ALLOWED_IMPLICIT_CONVERSIONS[target_type]
            if source_type in allowed_sources:
                return True

        return False

    def check_assignment(self, target_type: str, value: Any,
                        value_type: str, line: int = None,
                        column: int = None) -> Any:
        """检查赋值操作是否合法，返回转换后的值。

        参数：
            target_type: 目标变量声明类型
            value: 要赋的值
            value_type: 值的实际类型
            line: 源代码行号（用于错误报告）
            column: 源代码列号（用于错误报告）

        返回：
            转换后的值

        抛出：
            JassTypeError: 类型不兼容
        """
        if not self.is_compatible(value_type, target_type):
            raise JassTypeError(
                message=f"类型错误：不能将'{value_type}'类型的值赋值给'{target_type}'类型的变量",
                source_type=value_type,
                target_type=target_type,
                line=line,
                column=column
            )

        # 执行转换
        if value_type == 'integer' and target_type == 'real':
            return float(value)

        return value

    def check_function_arg(self, param_type: str, arg_value: Any,
                          arg_type: str, line: int = None,
                          column: int = None) -> Any:
        """检查函数参数类型是否匹配。

        参数：
            param_type: 形参声明类型
            arg_value: 实参值
            arg_type: 实参类型
            line: 源代码行号
            column: 源代码列号

        返回：
            转换后的值

        抛出：
            JassTypeError: 类型不兼容
        """
        if not self.is_compatible(arg_type, param_type):
            raise JassTypeError(
                message=f"类型错误：参数类型不匹配，期望'{param_type}'，实际得到'{arg_type}'",
                source_type=arg_type,
                target_type=param_type,
                line=line,
                column=column
            )

        # 执行转换
        if arg_type == 'integer' and param_type == 'real':
            return float(arg_value)

        return arg_value

    def check_return_value(self, return_type: str, value: Any,
                          value_type: str, line: int = None,
                          column: int = None) -> Any:
        """检查返回值类型是否匹配。

        参数：
            return_type: 函数声明的返回类型
            value: 返回值
            value_type: 返回值类型
            line: 源代码行号
            column: 源代码列号

        返回：
            转换后的值

        抛出：
            JassTypeError: 类型不兼容
        """
        if return_type == 'nothing':
            return value

        if not self.is_compatible(value_type, return_type):
            raise JassTypeError(
                message=f"类型错误：返回值类型不匹配，期望'{return_type}'，实际得到'{value_type}'",
                source_type=value_type,
                target_type=return_type,
                line=line,
                column=column
            )

        # 执行转换
        if value_type == 'integer' and return_type == 'real':
            return float(value)

        return value
