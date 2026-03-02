"""JASS类型系统错误类。"""


class JassTypeError(TypeError):
    """JASS类型错误异常。

    当类型检查失败时抛出，包含详细的类型和位置信息。

    属性：
        source_type: 源类型名称
        target_type: 目标类型名称
        line: 源代码行号（可选）
        column: 源代码列号（可选）
    """

    def __init__(self, message: str, source_type: str, target_type: str,
                 line: int = None, column: int = None):
        super().__init__(message)
        self.source_type = source_type
        self.target_type = target_type
        self.line = line
        self.column = column
