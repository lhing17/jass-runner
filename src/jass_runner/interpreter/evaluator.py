"""JASS表达式求值器。"""

from typing import Any
from .context import ExecutionContext


class Evaluator:
    """求值JASS表达式。"""

    def __init__(self, context: ExecutionContext):
        self.context = context

    def evaluate_native_call(self, node):
        """求值原生函数调用。"""
        func_name = node.func_name
        args = [self.evaluate(arg) for arg in node.args]

        # 从上下文中获取原生函数
        native_func = self.context.get_native_function(func_name)
        if native_func is None:
            raise RuntimeError(f"Native function not found: {func_name}")

        # 执行原生函数，传递state_context作为第一个参数
        return native_func.execute(self.context.state_context, *args)

    def evaluate(self, expression: Any) -> Any:
        """求值一个JASS表达式或AST节点。"""
        # 如果是字符串，按原逻辑处理
        if isinstance(expression, str):
            expression = expression.strip()

            # 处理字符串字面量
            if expression.startswith('"') and expression.endswith('"'):
                return expression[1:-1]

            # 处理整数字面量
            if expression.isdigit():
                return int(expression)

            # 处理浮点数字面量
            try:
                return float(expression)
            except ValueError:
                pass

            # 处理布尔值
            if expression == 'true':
                return True
            if expression == 'false':
                return False

            # 处理函数引用 (function:func_name)
            if expression.startswith('function:'):
                func_name = expression[9:]  # 去掉 'function:' 前缀
                # 返回一个可调用对象，用于回调
                interpreter = self.context.interpreter
                def callback_wrapper():
                    if interpreter and func_name in interpreter.functions:
                        from ..parser.parser import FunctionDecl
                        func = interpreter.functions[func_name]
                        if isinstance(func, FunctionDecl):
                            interpreter.execute_function(func)
                return callback_wrapper

            # 处理变量引用
            if self.context.has_variable(expression):
                return self.context.get_variable(expression)

            # 默认：作为字符串返回
            return expression

        # 如果是AST节点，检查节点类型
        node_type = type(expression).__name__

        if node_type == 'NativeCallNode':
            return self.evaluate_native_call(expression)

        # 其他节点类型将在后续添加
        raise NotImplementedError(f"Unsupported node type: {node_type}")