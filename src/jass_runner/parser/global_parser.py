from typing import List, Optional, TYPE_CHECKING, Any
from .ast_nodes import GlobalDecl, ArrayDecl
from .errors import ParseError

if TYPE_CHECKING:
    from .base_parser import BaseParser

class GlobalParserMixin:
    """提供全局变量解析功能。"""

    def parse_globals_block(self: 'BaseParser') -> List[Any]:
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
                self.next_token()

        # 跳过 'endglobals' 关键字
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals':
            self.next_token()

        return globals_list

    def parse_global_declaration(self: 'BaseParser') -> Optional[Any]:
        """解析单个全局变量声明。

        格式: [constant] <type> [array] <name> [= <initial_value>]
        注意: array声明不支持初始化

        返回：
            GlobalDecl节点、ArrayDecl节点或None（如果解析失败）
        """
        try:
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
            if var_type not in self.TYPE_KEYWORDS:
                return None
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
                if self.current_token:
                    if self.current_token.type == 'INTEGER':
                        value = self.current_token.value
                        self.next_token()
                    elif self.current_token.type == 'REAL':
                        value = self.current_token.value
                        self.next_token()
                    elif self.current_token.type == 'STRING':
                        value = self.current_token.value[1:-1]  # 移除引号
                        self.next_token()
                    elif self.current_token.type == 'KEYWORD' and self.current_token.value in ('true', 'false'):
                        value = self.current_token.value == 'true'
                        self.next_token()
            elif is_constant:
                # constant 必须有初始值
                self.errors.append(ParseError(
                    message=f"常量 '{var_name}' 必须指定初始值",
                    line=self.current_token.line if self.current_token else 0,
                    column=self.current_token.column if self.current_token else 0
                ))
                return None

            return GlobalDecl(name=var_name, type=var_type, value=value, is_constant=is_constant)

        except Exception:
            return None
