"""JASS解释器。"""

from typing import Any
from .context import ExecutionContext
from .evaluator import Evaluator
from ..parser.parser import AST, FunctionDecl, LocalDecl, NativeCallNode
from ..natives.state import StateContext


class Interpreter:
    """解释和执行JASS AST。"""

    def __init__(self, native_registry=None):
        self.state_context = StateContext()
        self.global_context = ExecutionContext(native_registry=native_registry, state_context=self.state_context)
        self.current_context = self.global_context
        self.functions = {}
        self.evaluator = Evaluator(self.current_context)

    def execute(self, ast: AST):
        """执行AST。"""
        # 注册所有函数
        for func in ast.functions:
            self.functions[func.name] = func

        # 查找并执行main函数
        if 'main' in self.functions:
            self.execute_function(self.functions['main'])

    def execute_function(self, func: FunctionDecl):
        """执行一个函数。"""
        # 为函数执行创建新上下文，继承state_context
        func_context = ExecutionContext(self.global_context, state_context=self.state_context)
        self.current_context = func_context

        # 执行函数体
        if func.body:
            for statement in func.body:
                self.execute_statement(statement)

        # 恢复之前的上下文
        self.current_context = self.global_context

    def execute_statement(self, statement: Any):
        """执行单个语句。"""
        if isinstance(statement, LocalDecl):
            self.execute_local_declaration(statement)
        elif isinstance(statement, NativeCallNode):
            self.execute_native_call(statement)

    def execute_local_declaration(self, decl: LocalDecl):
        """执行局部变量声明。"""
        # 在当前上下文中设置变量
        self.current_context.set_variable(decl.name, decl.value)

    def execute_native_call(self, node: NativeCallNode):
        """执行原生函数调用。"""
        # 使用求值器求值原生调用
        self.evaluator.evaluate(node)