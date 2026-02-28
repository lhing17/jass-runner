"""JASS表达式求值器。"""

import re
from typing import Any, List, Tuple
from .context import ExecutionContext


class OperatorPrecedence:
    """运算符优先级（数字越大优先级越高）。"""
    OR = 1
    AND = 2
    EQUALITY = 3
    RELATIONAL = 4
    ADDITIVE = 5
    MULTIPLICATIVE = 6
    UNARY = 7


class Evaluator:
    """求值JASS表达式。"""

    # 运算符优先级映射
    OPERATOR_PRECEDENCE = {
        '+': OperatorPrecedence.ADDITIVE,
        '-': OperatorPrecedence.ADDITIVE,
        '*': OperatorPrecedence.MULTIPLICATIVE,
        '/': OperatorPrecedence.MULTIPLICATIVE,
    }

    def __init__(self, context: ExecutionContext):
        self.context = context

    def _tokenize_expression(self, expression: str) -> List[str]:
        """将表达式分词为token列表。

        参数：
            expression: JASS表达式字符串

        返回：
            token列表
        """
        tokens = []
        i = 0
        while i < len(expression):
            # 跳过空白字符
            if expression[i].isspace():
                i += 1
                continue

            # 处理字符串字面量
            if expression[i] == '"':
                j = i + 1
                while j < len(expression) and expression[j] != '"':
                    j += 1
                tokens.append(expression[i:j+1])
                i = j + 1
                continue

            # 处理运算符和括号
            if expression[i] in '+-*/()':
                tokens.append(expression[i])
                i += 1
                continue

            # 处理数字（包括浮点数）
            if expression[i].isdigit() or expression[i] == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue

            # 处理标识符（变量名等）
            if expression[i].isalpha() or expression[i] == '_':
                j = i
                while j < len(expression) and (expression[j].isalnum() or expression[j] == '_'):
                    j += 1
                tokens.append(expression[i:j])
                i = j
                continue

            i += 1

        return tokens

    def _parse_value(self, token: Any) -> Any:
        """解析单个token为值。

        参数：
            token: 单个token（字符串或已解析的值）

        返回：
            解析后的值
        """
        # 如果token已经是解析后的值（如int、float等），直接返回
        if not isinstance(token, str):
            return token

        token = token.strip()

        # 处理字符串字面量
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]

        # 处理整数字面量
        if token.isdigit():
            return int(token)

        # 处理浮点数字面量
        try:
            return float(token)
        except ValueError:
            pass

        # 处理布尔值
        if token == 'true':
            return True
        if token == 'false':
            return False

        # 处理变量引用
        if self.context.has_variable(token):
            return self.context.get_variable(token)

        # 默认：作为字符串返回
        return token

    def _apply_operator(self, left: Any, operator: str, right: Any) -> Any:
        """应用二元运算符。

        参数：
            left: 左操作数
            operator: 运算符（+、-、*、/）
            right: 右操作数

        返回：
            运算结果
        """
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            # JASS中除法返回实数
            return left / right
        else:
            raise ValueError(f"不支持的运算符: {operator}")

    def _parse_and_evaluate(self, tokens: List[str]) -> Any:
        """解析并求值token列表（支持运算符优先级）。

        使用调度场算法处理运算符优先级。

        参数：
            tokens: token列表

        返回：
            求值结果
        """
        if not tokens:
            return None

        # 如果只有一个token，直接解析
        if len(tokens) == 1:
            return self._parse_value(tokens[0])

        # 转换为输出队列和运算符栈
        output_queue = []
        operator_stack = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            # 处理左括号：压入运算符栈
            if token == '(':
                operator_stack.append(token)
            # 处理右括号：弹出直到左括号
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                # 弹出左括号
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
            # 如果是运算符
            elif token in self.OPERATOR_PRECEDENCE:
                precedence = self.OPERATOR_PRECEDENCE[token]

                # 弹出优先级更高或相等的运算符
                while (operator_stack and
                       operator_stack[-1] in self.OPERATOR_PRECEDENCE and
                       self.OPERATOR_PRECEDENCE[operator_stack[-1]] >= precedence):
                    output_queue.append(operator_stack.pop())

                operator_stack.append(token)
            else:
                # 操作数直接入输出队列
                output_queue.append(token)

            i += 1

        # 弹出剩余的运算符
        while operator_stack:
            output_queue.append(operator_stack.pop())

        # 使用栈求值逆波兰表达式
        eval_stack = []
        for token in output_queue:
            if token in self.OPERATOR_PRECEDENCE:
                # 运算符：弹出两个操作数，计算结果
                right = self._parse_value(eval_stack.pop())
                left = self._parse_value(eval_stack.pop())
                result = self._apply_operator(left, token, right)
                eval_stack.append(result)
            else:
                eval_stack.append(token)

        return eval_stack[0] if eval_stack else None

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

            # 检查是否包含算术运算符
            if any(op in expression for op in '+-*/'):
                # 确保不是字符串字面量或函数引用
                if not (expression.startswith('"') and expression.endswith('"')) and \
                   not expression.startswith('function:'):
                    tokens = self._tokenize_expression(expression)
                    if len(tokens) >= 3:  # 至少需要 操作数 运算符 操作数
                        return self._parse_and_evaluate(tokens)

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