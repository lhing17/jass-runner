from typing import List, Optional, TYPE_CHECKING, Any, Union
from .ast_nodes import GlobalDecl, ArrayDecl
from .errors import ParseError

if TYPE_CHECKING:
    from .base_parser import BaseParser

class GlobalParserMixin:
    """提供全局变量解析功能。"""

    def parse_globals_block(self: 'BaseParser') -> List[Union[GlobalDecl, ArrayDecl]]:
        """解析可选的globals块。

        返回：
            如果存在globals块返回全局声明列表（GlobalDecl或ArrayDecl），否则返回空列表
        """
        globals_list = []

        # 检查是否存在 globals 关键字
        if not self.current_token or not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'globals'):
            return globals_list

        # 跳过 'globals' 关键字
        self.next_token()

        # 解析变量声明列表直到 endglobals
        while (self.current_token and
               not (self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals')):
            global_decl = self.parse_global_declaration()
            if global_decl:
                globals_list.append(global_decl)
            else:
                # 如果解析失败，跳过当前token以避免无限循环
                # 注意：这可能会跳过 endglobals，需要小心
                # 更好的策略可能是跳到下一行或者下一个分号，但在JASS中换行就是语句结束
                self.next_token()

        # 跳过 'endglobals' 关键字
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals':
            self.next_token()

        return globals_list

    def parse_global_declaration(self: 'BaseParser') -> Optional[Union[GlobalDecl, ArrayDecl]]:
        """解析单个全局变量声明。

        格式: [constant] <type> [array] <name> [= <initial_value>]
        注意: array声明不支持初始化

        返回：
            GlobalDecl节点、ArrayDecl节点或None（如果解析失败）
        """
        # 获取变量类型
        if not self.current_token:
            return None

        # 检查是否是 constant 声明
        is_constant = False
        if self.current_token.value == 'constant':
            is_constant = True
            self.next_token()
            if not self.current_token:
                return None

        var_type = self.current_token.value
        # 允许 TYPE_KEYWORDS 或 其他标识符（自定义类型/handle类型）
        # JASS 中所有 handle 类型本质上都是标识符
        # 这里为了简单，如果不是关键字，也假设是类型
        if var_type not in self.TYPE_KEYWORDS and self.current_token.type != 'IDENTIFIER':
             # 实际上 JASS 类型必须是预定义的或者是 handle 子类型
             # 严格检查可以在语义分析阶段做，这里放宽
             pass

        self.next_token()

        # 检查是否是数组声明
        is_array = False
        if self.current_token and self.current_token.type == 'KEYWORD' and \
           self.current_token.value == 'array':
            is_array = True
            self.next_token()

        # 获取变量名
        if not self.current_token or self.current_token.type != 'IDENTIFIER':
            return None
        var_name = self.current_token.value
        self.next_token()

        # 数组声明不支持初始化
        if is_array:
            if self.current_token and self.current_token.value == '=':
                self.errors.append(ParseError(
                    message="数组声明不支持初始化",
                    line=self.current_token.line if self.current_token else 0,
                    column=self.current_token.column if self.current_token else 0
                ))
                return None
            return ArrayDecl(
                name=var_name,
                element_type=var_type,
                is_global=True,
                is_constant=is_constant
            )

        # 检查可选的初始值（普通变量）
        value = None
        if self.current_token and self.current_token.value == '=':
            self.next_token()
            
            # 使用 ExpressionParserMixin 提供的 parse_expression 解析初始值
            # 假设 BaseParser 混入了 ExpressionParserMixin
            if hasattr(self, 'parse_expression'):
                value = self.parse_expression()
                
                # GlobalDecl value 期望的是字符串、bool 或 NativeCallNode
                # parse_expression 返回的可能是字符串或 NativeCallNode
                # 如果返回字符串，它可能包含引号（如果是字符串字面量）
                # 为了保持与 GlobalDecl 的兼容性（它期望去引号的字符串值），我们需要处理一下
                # 但 GlobalDecl 的 value 字段类型定义比较模糊 (Any)，通常是运行时求值用的
                # 现在的实现中，GlobalDecl.value 如果是字符串，通常是原始值
                # 我们需要确保 parse_expression 返回的值适合 GlobalDecl
                
                # 在 JASS 中，全局变量初始化只能是常量表达式或 Native 调用
                # parse_expression 能够处理这些
                
                # 特殊处理：如果 parse_expression 返回的是带引号的字符串，我们需要去掉引号吗？
                # 如果是 ExpressionParser 解析出来的，它是带引号的 '"foo"'
                # 而对于数字，ExpressionParser 返回字符串 '0' 或 '3.14'。
                # 测试失败原因：test_globals.py 期望 value 是 int(0) 和 float(3.14159)
                # 而 parse_expression 返回的是字符串 '0' 和 '3.14159'
                # 旧的 GlobalParser 在 L104-L108 会保留 Token value (int/float)，
                # 但 Lexer 可能已经把它们转成了 int/float (如果 Lexer 足够聪明)，或者保留为 str
                # 让我们检查 Lexer 的行为。通常 Lexer 会保留原始值。
                # 但 expression_parser._parse_atom 显式把它们转成了 str (L136, L140)
                # 这就是问题所在！
                
                # 修复方案：尝试将 value 转回 int/float
                if isinstance(value, str):
                    if value.isdigit():
                        value = int(value)
                    elif value == 'true':
                        value = True
                    elif value == 'false':
                        value = False
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            # 字符串字面量处理
                            # 如果是 '"foo"'，去掉引号
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            pass
            else:
                # 降级处理或者报错
                return None

        elif is_constant:
            # constant 必须有初始值
            self.errors.append(ParseError(
                message=f"常量 '{var_name}' 必须指定初始值",
                line=self.current_token.line if self.current_token else 0,
                column=self.current_token.column if self.current_token else 0
            ))
            return None

        # 这里的 value 如果是字符串字面量，是否应该包含引号？
        # 如果是 ExpressionParser 解析出来的，它是带引号的 '"foo"'
        # 原来的 parser 是去掉引号的 'foo'
        # 我们需要确认 GlobalDecl 的消费者（Interpreter）期望什么
        # 假设 Interpreter 直接使用 value，如果是字符串，它需要知道这是一个字符串值还是变量名
        # 在 GlobalDecl 中，value 可能是 NativeCallNode，也可能是字面量
        # 如果是 'foo'，解释器怎么知道它是字符串 "foo" 还是变量 foo？
        # 通常 AST 中字面量应该有专门的节点，或者保留引号。
        # 让我们查看 Interpreter.visit_GlobalDecl 或相关逻辑
        
        # 修正：原来的 parser 在 L110 确实去掉了引号。
        # 让我们看看 Evaluator 对 GlobalDecl 的处理。
        # 搜索 Interpreter 逻辑...
        
        return GlobalDecl(name=var_name, type=var_type, value=value, is_constant=is_constant)
