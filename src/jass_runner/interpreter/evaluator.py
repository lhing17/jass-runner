"""JASS表达式求值器。"""

import re
from typing import Any, List, Tuple
from .context import ExecutionContext
from ..parser.ast_nodes import ArrayAccess, IntegerExpr, VariableExpr


class OperatorPrecedence:
    """运算符优先级（数字越大优先级越高）。"""
    OR = 1
    AND = 2
    EQUALITY = 3
    RELATIONAL = 4
    ADDITIVE = 5
    MULTIPLICATIVE = 6
    UNARY = 7


class FunctionResult:
    """包装函数调用结果，用于在表达式求值中传递对象。"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"FunctionResult({self.value!r})"


class Evaluator:
    """求值JASS表达式。"""

    # 运算符优先级映射
    OPERATOR_PRECEDENCE = {
        'or': OperatorPrecedence.OR,
        'and': OperatorPrecedence.AND,
        '==': OperatorPrecedence.EQUALITY,
        '!=': OperatorPrecedence.EQUALITY,
        '>': OperatorPrecedence.RELATIONAL,
        '<': OperatorPrecedence.RELATIONAL,
        '>=': OperatorPrecedence.RELATIONAL,
        '<=': OperatorPrecedence.RELATIONAL,
        '+': OperatorPrecedence.ADDITIVE,
        '-': OperatorPrecedence.ADDITIVE,
        '*': OperatorPrecedence.MULTIPLICATIVE,
        '/': OperatorPrecedence.MULTIPLICATIVE,
    }

    # 一元运算符集合（带优先级）
    UNARY_OPERATORS = {'not': OperatorPrecedence.UNARY}

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

            # 处理字符串字面量（双引号）
            if expression[i] == '"':
                j = i + 1
                while j < len(expression) and expression[j] != '"':
                    j += 1
                tokens.append(expression[i:j+1])
                i = j + 1
                continue

            # 处理单引号（四字符码）
            if expression[i] == "'":
                j = i + 1
                # 四字符码：'xxxx'，其中 xxxx 是恰好4个字符
                while j < len(expression) and expression[j] != "'":
                    j += 1
                # 包含首尾单引号
                tokens.append(expression[i:j+1])
                i = j + 1
                continue

            # 处理逗号（函数参数分隔符）
            if expression[i] == ',':
                tokens.append(',')
                i += 1
                continue

            # 处理运算符和括号
            if expression[i] in '+-*/()':
                tokens.append(expression[i])
                i += 1
                continue

            # 处理比较运算符 (==, !=, >=, <=, >, <)
            if expression[i] in '=!><':
                # 检查双字符运算符
                if i + 1 < len(expression) and expression[i + 1] == '=':
                    tokens.append(expression[i:i+2])
                    i += 2
                else:
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

            # 处理标识符（变量名、关键字如and/or/not等）
            if expression[i].isalpha() or expression[i] == '_':
                j = i
                while j < len(expression) and (expression[j].isalnum() or expression[j] == '_'):
                    j += 1
                word = expression[i:j]
                tokens.append(word)
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
        # 如果是 FunctionResult，解包值
        if isinstance(token, FunctionResult):
            return token.value

        # 如果token已经是解析后的值（如int、float等），直接返回
        if not isinstance(token, str):
            return token

        token = token.strip()

        # 处理字符串字面量（双引号）
        if token.startswith('"') and token.endswith('"'):
            return token[1:-1]

        # 处理四字符码（单引号，如 'Rhrt'）
        if token.startswith("'") and token.endswith("'"):
            from ..utils import fourcc_to_int
            return fourcc_to_int(token[1:-1])  # 去掉首尾单引号

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

        # 处理null值
        if token == 'null':
            return None

        # 处理变量引用
        if self.context.has_variable(token):
            return self.context.get_variable(token)

        # 默认：作为字符串返回
        return token

    def _apply_operator(self, left: Any, operator: str, right: Any) -> Any:
        """应用二元运算符。

        参数：
            left: 左操作数
            operator: 运算符（+、-、*、/、==、!=、>、<、>=、<=）
            right: 右操作数

        返回：
            运算结果
        """
        # 处理None值：将None视为0（向后兼容）
        if left is None:
            left = 0
        if right is None:
            right = 0

        # 算术运算符
        if operator == '+':
            # 处理字符串拼接：如果任一侧是字符串，都转为字符串拼接
            if isinstance(left, str) or isinstance(right, str):
                # JASS: string + any = string concatenation
                return str(left) + str(right)
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            # JASS中除法：如果两个操作数都是整数，返回整数（整除）
            # 如果任一操作数是实数，返回实数
            if isinstance(left, int) and isinstance(right, int):
                return left // right
            return left / right
        # 比较运算符
        elif operator == '==':
            return left == right
        elif operator == '!=':
            return left != right
        elif operator == '>':
            return left > right
        elif operator == '<':
            return left < right
        elif operator == '>=':
            return left >= right
        elif operator == '<=':
            return left <= right
        # 逻辑运算符
        elif operator == 'and':
            return left and right
        elif operator == 'or':
            return left or right
        else:
            raise ValueError(f"不支持的运算符: {operator}")

    def _apply_unary_operator(self, operator: str, operand: Any) -> Any:
        """应用一元运算符。

        参数：
            operator: 运算符（not）
            operand: 操作数

        返回：
            运算结果
        """
        if operator == 'not':
            return not operand
        else:
            raise ValueError(f"不支持的一元运算符: {operator}")

    def _parse_and_evaluate(self, tokens: List[str]) -> Any:
        """解析并求值token列表（支持运算符优先级和函数调用）。

        使用调度场算法处理运算符优先级，同时识别函数调用模式。

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

        # 第一步：处理函数调用模式（如 GetCameraMargin(0)）
        # 将函数调用转换为先求值函数，然后再参与表达式计算
        i = 0
        processed_tokens = []
        while i < len(tokens):
            token = tokens[i]

            # 检查是否是函数调用模式：标识符 + 左括号
            if (token not in self.OPERATOR_PRECEDENCE and
                token not in self.UNARY_OPERATORS and
                token not in ('+', '-', '*', '/', '(', ')') and
                i + 1 < len(tokens) and tokens[i + 1] == '('):

                # 这是一个函数调用
                func_name = token
                i += 2  # 跳过函数名和左括号

                # 收集函数参数直到匹配的右括号
                func_args = []
                paren_depth = 1
                arg_tokens = []

                while i < len(tokens) and paren_depth > 0:
                    if tokens[i] == '(':
                        paren_depth += 1
                        arg_tokens.append(tokens[i])
                        i += 1
                    elif tokens[i] == ')':
                        paren_depth -= 1
                        if paren_depth == 0:
                            # 参数结束
                            if arg_tokens:
                                # 递归求值参数表达式
                                arg_value = self._parse_and_evaluate(arg_tokens)
                                func_args.append(arg_value)
                            i += 1
                            break
                        else:
                            arg_tokens.append(tokens[i])
                            i += 1
                    elif tokens[i] == ',' and paren_depth == 1:
                        # 参数分隔符
                        if arg_tokens:
                            arg_value = self._parse_and_evaluate(arg_tokens)
                            func_args.append(arg_value)
                        arg_tokens = []
                        i += 1
                    else:
                        arg_tokens.append(tokens[i])
                        i += 1

                # 执行函数调用并获取结果
                from ..parser.ast_nodes import NativeCallNode
                call_node = NativeCallNode(func_name=func_name, args=func_args)
                func_result = self.evaluate_native_call(call_node)
                # 使用 FunctionResult 包装结果，避免转换为字符串
                processed_tokens.append(FunctionResult(func_result))
            else:
                processed_tokens.append(token)
                i += 1

        # 第二步：使用逆波兰算法处理表达式
        # 处理一元运算符（如 -11520.0）
        # 如果表达式以 - 开头且后面跟着数字，将其作为负数处理
        if (len(processed_tokens) >= 2 and
            processed_tokens[0] == '-' and
            processed_tokens[1] not in ('(', ')')):
            # 这是一元负号
            processed_tokens = ['0'] + processed_tokens[0:]  # 转换为 0 - X

        # 转换为输出队列和运算符栈
        output_queue = []
        operator_stack = []

        i = 0
        while i < len(processed_tokens):
            token = processed_tokens[i]

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
            # 如果是一元运算符
            elif token in self.UNARY_OPERATORS:
                precedence = self.UNARY_OPERATORS[token]
                # 弹出优先级更高或相等的运算符
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       ((operator_stack[-1] in self.OPERATOR_PRECEDENCE and
                         self.OPERATOR_PRECEDENCE[operator_stack[-1]] >= precedence) or
                        (operator_stack[-1] in self.UNARY_OPERATORS and
                         self.UNARY_OPERATORS[operator_stack[-1]] >= precedence))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            # 如果是二元运算符
            elif token in self.OPERATOR_PRECEDENCE:
                precedence = self.OPERATOR_PRECEDENCE[token]

                # 弹出优先级更高或相等的运算符
                while (operator_stack and
                       operator_stack[-1] != '(' and
                       ((operator_stack[-1] in self.OPERATOR_PRECEDENCE and
                         self.OPERATOR_PRECEDENCE[operator_stack[-1]] >= precedence) or
                        (operator_stack[-1] in self.UNARY_OPERATORS and
                         self.UNARY_OPERATORS[operator_stack[-1]] >= precedence))):
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
            if token in self.UNARY_OPERATORS:
                # 一元运算符：弹出一个操作数
                operand = self._parse_value(eval_stack.pop())
                result = self._apply_unary_operator(token, operand)
                eval_stack.append(result)
            elif token in self.OPERATOR_PRECEDENCE:
                # 二元运算符：弹出两个操作数，计算结果
                right = self._parse_value(eval_stack.pop())
                left = self._parse_value(eval_stack.pop())
                result = self._apply_operator(left, token, right)
                eval_stack.append(result)
            else:
                eval_stack.append(token)

        if not eval_stack:
            return None

        # 如果结果是 FunctionResult，解包它
        result = eval_stack[0]
        if isinstance(result, FunctionResult):
            return result.value
        return result

    def evaluate_native_call(self, node):
        """求值原生函数调用。"""
        func_name = node.func_name
        # 处理参数：如果是列表（混合参数）、字符串或节点则求值，否则直接使用已求值的参数
        args = []
        for arg in node.args:
            if isinstance(arg, (int, float, bool)):
                # 已经是基本类型值，直接使用
                args.append(arg)
            elif isinstance(arg, list):
                # 混合参数列表，需要求值为一个数值
                # 例如: ['11520.0', '-', NativeCallNode(...)]
                result = self._evaluate_mixed_list(arg)
                args.append(result)
            elif isinstance(arg, str):
                # 字符串需要求值
                args.append(self.evaluate(arg))
            elif hasattr(arg, 'func_name'):
                # NativeCallNode，递归求值
                args.append(self.evaluate_native_call(arg))
            else:
                # 其他类型（可能是 AST 节点如 ArrayAccess）
                # 尝试使用 evaluate 方法求值
                try:
                    result = self.evaluate(arg)
                    args.append(result)
                except Exception:
                    # 如果不能求值，直接使用
                    args.append(arg)

        # 从上下文中获取原生函数
        native_func = self.context.get_native_function(func_name)
        if native_func is not None:
            # 执行原生函数，传递state_context作为第一个参数
            return native_func.execute(self.context.state_context, *args)

        # 如果不是原生函数，检查是否是用户定义的函数
        interpreter = self.context.interpreter
        if interpreter and func_name in interpreter.functions:
            from ..parser.parser import FunctionDecl
            func = interpreter.functions[func_name]
            if isinstance(func, FunctionDecl):
                # 调用用户定义的函数
                return interpreter._call_function_with_args(func, args)

        raise RuntimeError(f"Native function not found: {func_name}")

    def _evaluate_mixed_list(self, tokens: list) -> Any:
        """求值混合列表（包含字符串、数字和NativeCallNode）。

        将混合列表转换为表达式并求值，例如：
        ['11520.0', '-', NativeCallNode(func_name='GetCameraMargin', args=[0])]
        转换为表达式 "11520.0 - 100.0" -> 11420.0

        参数：
            tokens: 混合token列表

        返回：
            求值后的数值结果
        """
        # 将列表转换为可求值的token列表
        processed_tokens = []
        for token in tokens:
            if hasattr(token, 'func_name'):
                # 是 NativeCallNode，求值并获取结果
                func_result = self.evaluate_native_call(token)
                processed_tokens.append(str(func_result))
            elif type(token).__name__ == 'ArrayAccess':
                # 是 ArrayAccess 节点，使用 evaluate 求值
                array_result = self.evaluate(token)
                processed_tokens.append(str(array_result))
            else:
                processed_tokens.append(str(token))

        # 使用 _parse_and_evaluate 求值表达式
        return self._parse_and_evaluate(processed_tokens)

    def evaluate_condition(self, condition: Any) -> bool:
        """求值条件表达式，返回布尔结果。

        参数：
            condition: 条件表达式字符串或已求值的结果

        返回：
            布尔结果
        """
        if isinstance(condition, str):
            result = self.evaluate(condition)
        else:
            result = condition

        # 转换结果为布尔值
        if isinstance(result, bool):
            return result
        elif isinstance(result, (int, float)):
            return result != 0
        elif isinstance(result, str):
            return result.lower() == "true"
        return bool(result)

    def evaluate(self, expression: Any) -> Any:
        """求值一个JASS表达式或AST节点。"""
        # 处理null值（None）
        if expression is None:
            return None

        # 如果是字符串，按原逻辑处理
        if isinstance(expression, str):
            expression = expression.strip()

            # 检查是否包含算术运算符、比较运算符、逻辑运算符或函数调用
            operators = ['+', '-', '*', '/', '==', '!=', '>', '<', '>=', '<=', 'and', 'or', 'not']
            has_operator = any(op in expression for op in operators)
            has_function_call = '(' in expression and ')' in expression

            if has_operator or has_function_call:
                # 确保不是字符串字面量或函数引用
                if not (expression.startswith('"') and expression.endswith('"')) and \
                   not expression.startswith('function:'):
                    tokens = self._tokenize_expression(expression)
                    # 检查是否包含一元运算符（如not true只有2个token）
                    has_unary = any(t in self.UNARY_OPERATORS for t in tokens)
                    # 对于函数调用（如Player(0)），只要有括号就处理
                    if has_function_call or len(tokens) >= 3 or (len(tokens) == 2 and has_unary):
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

            # 处理null值
            if expression == 'null':
                return None

            # 处理函数引用 (function:func_name)
            if expression.startswith('function:'):
                func_name = expression[9:]  # 去掉 'function:' 前缀
                # 返回一个可调用对象，用于回调
                interpreter = self.context.interpreter
                def callback_wrapper(*args, **kwargs):
                    if interpreter and func_name in interpreter.functions:
                        from ..parser.parser import FunctionDecl
                        func = interpreter.functions[func_name]
                        if isinstance(func, FunctionDecl):
                            interpreter.execute_function(func)
                # 设置函数名属性，便于日志记录
                callback_wrapper.__name__ = func_name
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

        if node_type == 'IntegerExpr':
            return expression.value

        if node_type == 'VariableExpr':
            return self.context.get_variable(expression.name)

        if node_type == 'ArrayAccess':
            # 递归求值索引表达式
            index = self.evaluate(expression.index)
            return self.context.get_array_element(expression.array_name, int(index))

        # 其他节点类型将在后续添加
        raise NotImplementedError(f"Unsupported node type: {node_type}")