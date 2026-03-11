from typing import Optional, TYPE_CHECKING, Any, List
from .ast_nodes import NativeCallNode

if TYPE_CHECKING:
    from .base_parser import BaseParser
    from .lexer import Token

class ExpressionParserMixin:
    """提供表达式解析功能。"""

    def parse_condition(self: 'BaseParser') -> Optional[str]:
        """解析条件表达式。

        返回：
            条件表达式字符串，如果解析失败返回None
        """
        # 条件表达式本质上就是普通表达式
        return self.parse_expression()

    def parse_expression(self: 'BaseParser', min_precedence: int = 0) -> Optional[Any]:
        """解析表达式。
        
        支持：
        - 字面量 (整数, 实数, 字符串, 布尔值)
        - 变量引用
        - 函数调用
        - 数组访问
        - 一元运算符 (not, -)
        - 二元运算符 (+, -, *, /, and, or, ==, !=, <, >, <=, >=)
        - 括号

        参数:
            min_precedence: 最小优先级

        返回:
            AST节点(NativeCallNode等) 或 字符串形式的表达式
        """
        if not self.current_token:
            return None

        # 解析左操作数
        left = self._parse_atom()
        if left is None:
            return None

        # 解析二元运算符
        while True:
            op = self._get_binary_operator()
            if not op:
                break
            
            precedence = self._get_precedence(op)
            if precedence < min_precedence:
                break
            
            self.next_token() # 消耗运算符
            
            # 解析右操作数
            right = self.parse_expression(precedence + 1)
            if right is None:
                # 这是一个错误，但为了保持简单，我们可能需要处理它
                # 这里简单返回左操作数，或者抛出错误
                break
                
            # 组合表达式 (目前简化为字符串拼接，理想情况下应构建AST)
            # 注意：NativeCallNode 需要特殊处理转为字符串
            left_str = self._node_to_string(left)
            right_str = self._node_to_string(right)
            left = f"{left_str} {op} {right_str}"
            
        return left

    def parse_function_call(self: 'BaseParser') -> Optional[NativeCallNode]:
        """解析函数调用。
        
        格式: name(arg1, arg2, ...)
        
        返回:
            NativeCallNode 或 None
        """
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None
        
        func_name = self.current_token.value
        self.next_token() # 消耗函数名
        
        if not self.current_token or self.current_token.value != '(':
            return None
        
        self.next_token() # 消耗 '('
        
        args = []
        if self.current_token and self.current_token.value != ')':
            while True:
                arg = self.parse_expression()
                if arg is not None:
                    # 将参数转换为字符串或保留 NativeCallNode
                    # 为了兼容现有的 AST 结构（NativeCallNode.args 期望是字符串列表，或者包含嵌套调用）
                    # 现有的 NativeCallNode 定义允许 args 包含 NativeCallNode
                    args.append(self._node_to_arg(arg))
                
                if self.current_token and self.current_token.value == ',':
                    self.next_token()
                else:
                    break
        
        if self.current_token and self.current_token.value == ')':
            self.next_token() # 消耗 ')'
            
        return NativeCallNode(func_name=func_name, args=args)

    def _parse_atom(self: 'BaseParser') -> Optional[Any]:
        """解析原子表达式（字面量、标识符、括号表达式、前缀运算符）。"""
        if not self.current_token:
            return None

        token = self.current_token

        # 括号
        if token.value == '(':
            self.next_token()
            expr = self.parse_expression()
            if self.current_token and self.current_token.value == ')':
                self.next_token()
            return f"({expr})"

        # 一元运算符
        if token.value == '-' or (token.type == 'KEYWORD' and token.value == 'not'):
            op = token.value
            self.next_token()
            operand = self.parse_expression(self._get_unary_precedence()) # 解析高优先级操作数
            return f"{op} {self._node_to_string(operand)}"

        # 字面量
        if token.type == 'INTEGER':
            val = str(token.value)
            self.next_token()
            return val
        elif token.type == 'REAL':
            val = str(token.value)
            self.next_token()
            return val
        elif token.type == 'STRING':
            val = str(token.value) 
            # 修正：这里不再去除引号。GlobalParserMixin 会期望一个原始字符串。
            # Evaluator 期望字面量带有引号，变量名不带引号。
            # 所以我们必须返回带引号的字符串。
            self.next_token()
            return val
        elif token.type == 'KEYWORD' and token.value in ('true', 'false', 'null'):
            val = token.value
            self.next_token()
            return val
        elif token.type == 'KEYWORD' and token.value == 'function':
            # function func_name
            self.next_token()
            if self.current_token and self.current_token.type == 'IDENTIFIER':
                func_name = self.current_token.value
                self.next_token()
                return f"function {func_name}"
            return None

        # 标识符 (变量、数组访问、函数调用)
        if token.type == 'IDENTIFIER':
            name = token.value
            
            # 预读下一个 token 判断类型
            next_token = self._peek_token()
            
            if next_token == '(':
                # 函数调用
                # 回退指针或者直接调用 parse_function_call (它会重新检查 identifier)
                # 这里我们已经获取了 name，直接调用 parse_function_call 会重复
                # 所以我们手动处理
                return self.parse_function_call()
                
            self.next_token() # 消耗 name
            
            if self.current_token and self.current_token.value == '[':
                # 数组访问
                self.next_token()
                index = self.parse_expression()
                if self.current_token and self.current_token.value == ']':
                    self.next_token()
                return f"{name}[{self._node_to_string(index)}]"
            
            return name

        return None

    def _get_binary_operator(self: 'BaseParser') -> Optional[str]:
        """获取当前二元运算符。"""
        if not self.current_token:
            return None
        
        token = self.current_token
        if token.type == 'OPERATOR':
            return token.value
        if token.type == 'KEYWORD' and token.value in ('and', 'or'):
            return token.value
        return None

    def _get_precedence(self, op: str) -> int:
        """获取运算符优先级。"""
        precedences = {
            'or': 1,
            'and': 2,
            '==': 3, '!=': 3,
            '<': 4, '>': 4, '<=': 4, '>=': 4,
            '+': 5, '-': 5,
            '*': 6, '/': 6
        }
        return precedences.get(op, 0)

    def _get_unary_precedence(self) -> int:
        return 7 # 高于所有二元运算符

    def _peek_token(self: 'BaseParser') -> Optional[str]:
        """查看下一个token的值。"""
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1].value
        return None

    def _node_to_string(self, node: Any) -> str:
        """将节点转换为字符串表示（用于构建表达式字符串）。"""
        if isinstance(node, NativeCallNode):
            args_str = ", ".join([self._node_to_string(arg) for arg in node.args])
            return f"{node.func_name}({args_str})"
        return str(node)

    def _node_to_arg(self, node: Any) -> Any:
        """将节点转换为参数列表需要的格式。
        如果是 NativeCallNode，保持对象以便 AST 处理。
        如果是字符串（字面量、表达式），保持字符串。
        """
        if isinstance(node, NativeCallNode):
            return node
        # 去除字符串字面量的引号，如果它只是一个简单的字符串值
        # 但如果是复杂表达式，可能需要保留结构。
        # 这里为了兼容 GlobalParser 的逻辑：
        # string args 应去除引号
        s = str(node)
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        return s
