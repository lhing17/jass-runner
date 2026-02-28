from typing import List, Optional, TYPE_CHECKING
from .ast_nodes import GlobalDecl

if TYPE_CHECKING:
    from .base_parser import BaseParser

class GlobalParserMixin:
    """提供全局变量解析功能。"""

    def parse_globals_block(self: 'BaseParser') -> List[GlobalDecl]:
        """解析可选的globals块。

        返回：
            如果存在globals块返回GlobalDecl列表，否则返回空列表
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

        # 跳过 'endglobals' 关键字
        if self.current_token and self.current_token.type == 'KEYWORD' and self.current_token.value == 'endglobals':
            self.next_token()

        return globals_list

    def parse_global_declaration(self: 'BaseParser') -> Optional[GlobalDecl]:
        """解析单个全局变量声明。

        格式: [constant] <type> <name> [= <initial_value>]

        返回：
            GlobalDecl节点或None（如果解析失败）
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

            # 获取变量名
            if not self.current_token or self.current_token.type != 'IDENTIFIER':
                return None
            var_name = self.current_token.value

            self.next_token()

            # 检查可选的初始值
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

            return GlobalDecl(name=var_name, type=var_type, value=value, is_constant=is_constant)

        except Exception:
            return None
