from typing import List, Optional, Set
from .lexer import Lexer, Token
from .errors import ParseError

class BaseParser:
    """JASS解析器基础类，提供词法分析器接口和基本辅助方法。"""

    # 可能出现在参数列表中的JASS类型关键词
    TYPE_KEYWORDS = {
        'integer', 'real', 'string', 'boolean', 'code', 'handle', 'nothing'
    }

    def __init__(self, code: str):
        """使用JASS代码初始化解析器。

        参数：
            code: 要解析的JASS源代码
        """
        self.lexer = Lexer(code)
        self.tokens: List[Token] = []
        self.current_token: Optional[Token] = None
        self.token_index = 0
        self.errors: List[ParseError] = []
        # 存储全局变量名用于冲突检查
        self.global_names: Set[str] = set()

    def add_error(self, error: ParseError) -> None:
        """添加错误到错误列表。"""
        self.errors.append(error)

    def match_keyword(self, keyword: str) -> bool:
        """检查当前标记是否匹配给定的关键词。

        参数：
            keyword: 要匹配的关键词

        返回：
            如果匹配返回True，否则返回False
        """
        if (self.current_token is not None and
                self.current_token.type == 'KEYWORD' and
                self.current_token.value == keyword):
            self.next_token()
            return True
        return False

    def next_token(self) -> None:
        """前进到下一个标记。"""
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def skip_to_next_function(self) -> None:
        """跳过标记直到下一个函数声明或标记结束。"""
        while self.current_token is not None:
            if (self.current_token.type == 'KEYWORD'
                    and self.current_token.value == 'function'):
                return
            self.next_token()
