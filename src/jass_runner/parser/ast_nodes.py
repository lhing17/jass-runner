"""AST节点定义。

此模块包含JASS解析器的抽象语法树节点定义。
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class Parameter:
    """函数参数节点。"""
    name: str
    type: str
    line: int  # 来自标记的行号
    column: int  # 来自标记的列号


@dataclass
class GlobalDecl:
    """全局变量声明节点。"""
    name: str
    type: str
    value: Any  # 初始值，可能为None
    is_constant: bool = False  # 是否为常量


@dataclass
class LocalDecl:
    """表示局部变量声明。"""
    name: str
    type: str
    value: Any


@dataclass
class FunctionDecl:
    """函数声明节点。"""
    name: str
    parameters: List[Parameter]
    return_type: str
    line: int
    column: int
    body: Optional[List[Any]] = None  # 现在将包含语句


@dataclass
class AST:
    """抽象语法树根节点。"""
    functions: List[FunctionDecl]
    globals: List[GlobalDecl] = None  # 全局变量声明列表

    def __post_init__(self):
        """初始化默认值。"""
        if self.globals is None:
            self.globals = []


@dataclass
class NativeCallNode:
    """原生函数调用节点。"""
    func_name: str
    args: List[Any]


@dataclass
class SetStmt:
    """变量赋值语句节点。"""
    var_name: str
    value: Any  # 可以是字面量或函数调用节点


@dataclass
class IfStmt:
    """if语句节点。"""
    condition: str  # 条件表达式
    then_body: List[Any]  # then分支的语句列表
    elseif_branches: List[dict] = field(default_factory=list)  # elseif分支列表
    else_body: List[Any] = field(default_factory=list)  # else分支的语句列表

    def __post_init__(self):
        """初始化默认值。"""
        if self.elseif_branches is None:
            self.elseif_branches = []
        if self.else_body is None:
            self.else_body = []


@dataclass
class LoopStmt:
    """loop循环语句节点。"""
    body: List[Any]  # 循环体内的语句列表


@dataclass
class ExitWhenStmt:
    """exitwhen循环退出语句节点。"""
    condition: str  # 退出条件表达式


@dataclass
class ReturnStmt:
    """return返回语句节点。"""
    value: Optional[Any]  # 返回值，如果是return nothing则为None
