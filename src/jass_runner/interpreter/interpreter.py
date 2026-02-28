"""JASS解释器。"""

from typing import Any
from .context import ExecutionContext
from .evaluator import Evaluator
from ..parser.parser import AST, FunctionDecl, LocalDecl, NativeCallNode, SetStmt, IfStmt, LoopStmt, ExitWhenStmt, ReturnStmt, GlobalDecl
from ..parser.ast_nodes import ArrayDecl, SetArrayStmt
from ..natives.state import StateContext
from .control_flow import ExitLoopSignal, ReturnSignal


class Interpreter:
    """解释和执行JASS AST。"""

    def __init__(self, native_registry=None):
        self.state_context = StateContext()
        self.global_context = ExecutionContext(native_registry=native_registry, state_context=self.state_context, interpreter=self)
        self.current_context = self.global_context
        self.functions = {}
        self.evaluator = Evaluator(self.current_context)

    def execute(self, ast: AST):
        """执行AST。"""
        # 初始化全局变量
        if ast.globals:
            for global_decl in ast.globals:
                self.execute_global_declaration(global_decl)

        # 注册所有函数
        for func in ast.functions:
            self.functions[func.name] = func

        # 查找并执行main函数
        if 'main' in self.functions:
            self.execute_function(self.functions['main'])

    def execute_global_declaration(self, decl: GlobalDecl):
        """执行全局变量声明。

        参数：
            decl: GlobalDecl节点，包含变量名、类型和初始值
        """
        # 如果值是函数调用节点，先执行它并获取返回值
        if isinstance(decl.value, NativeCallNode):
            result = self.evaluator.evaluate(decl.value)
            self.global_context.set_variable(decl.name, result)
        else:
            # 直接赋值字面量或None
            self.global_context.set_variable(decl.name, decl.value)

    def execute_function(self, func: FunctionDecl):
        """执行一个函数。"""
        # 保存当前上下文以便后续恢复
        previous_context = self.current_context

        # 为函数执行创建新上下文，继承global_context的native_registry和state_context
        func_context = ExecutionContext(
            self.global_context,
            native_registry=self.global_context.native_registry,
            state_context=self.state_context,
            interpreter=self
        )
        self.current_context = func_context

        # 更新求值器的上下文
        self.evaluator.context = func_context

        # 执行函数体
        return_value = None
        try:
            if func.body:
                for statement in func.body:
                    self.execute_statement(statement)
        except ReturnSignal as signal:
            return_value = signal.value

        # 恢复之前的上下文
        self.current_context = previous_context
        self.evaluator.context = previous_context

        return return_value

    def execute_statement(self, statement: Any):
        """执行单个语句。"""
        if isinstance(statement, ArrayDecl):
            self.execute_array_declaration(statement)
        elif isinstance(statement, LocalDecl):
            self.execute_local_declaration(statement)
        elif isinstance(statement, NativeCallNode):
            self.execute_native_call(statement)
        elif isinstance(statement, SetStmt):
            self.execute_set_statement(statement)
        elif isinstance(statement, SetArrayStmt):
            self.execute_set_array_statement(statement)
        elif isinstance(statement, IfStmt):
            self.execute_if_statement(statement)
        elif isinstance(statement, LoopStmt):
            self.execute_loop_statement(statement)
        elif isinstance(statement, ExitWhenStmt):
            self.execute_exitwhen_statement(statement)
        elif isinstance(statement, ReturnStmt):
            self.execute_return_statement(statement)

    def execute_array_declaration(self, decl: ArrayDecl):
        """执行数组声明。

        参数：
            decl: 数组声明节点
        """
        self.current_context.declare_array(decl.name, decl.element_type)

    def execute_local_declaration(self, decl: LocalDecl):
        """执行局部变量声明。"""
        # 如果值是函数调用节点，先执行它并获取返回值
        if isinstance(decl.value, NativeCallNode):
            result = self.evaluator.evaluate(decl.value)
            self.current_context.set_variable(decl.name, result)
        else:
            # 直接赋值字面量或None
            self.current_context.set_variable(decl.name, decl.value)

    def execute_native_call(self, node: NativeCallNode):
        """执行原生函数调用。"""
        # 使用求值器求值原生调用
        self.evaluator.evaluate(node)

    def execute_set_statement(self, stmt: SetStmt):
        """执行变量赋值语句。"""
        # 如果值是函数调用节点，先执行它并获取返回值
        if isinstance(stmt.value, NativeCallNode):
            result = self.evaluator.evaluate(stmt.value)
            self.current_context.set_variable_recursive(stmt.var_name, result)
        elif isinstance(stmt.value, str):
            # 如果是字符串，可能是表达式，需要求值
            result = self.evaluator.evaluate(stmt.value)
            self.current_context.set_variable_recursive(stmt.var_name, result)
        else:
            # 直接赋值字面量
            self.current_context.set_variable_recursive(stmt.var_name, stmt.value)

    def execute_set_array_statement(self, stmt: SetArrayStmt):
        """执行数组元素赋值。

        参数：
            stmt: 数组赋值语句节点
        """
        # 求值索引表达式
        index = self.evaluator.evaluate(stmt.index)
        # 求值右侧值
        value = self.evaluator.evaluate(stmt.value)
        # 设置数组元素
        self.current_context.set_array_element(stmt.array_name, int(index), value)

    def execute_if_statement(self, stmt: IfStmt):
        """执行if语句。

        参数：
            stmt: IfStmt节点，包含condition、then_body、elseif_branches和else_body
        """
        # 求值条件表达式
        condition_result = self.evaluator.evaluate_condition(stmt.condition)

        if condition_result:
            # 执行then分支
            for statement in stmt.then_body:
                self.execute_statement(statement)
        else:
            # 检查elseif分支
            executed = False
            for elseif in stmt.elseif_branches:
                elseif_condition = self.evaluator.evaluate_condition(elseif['condition'])
                if elseif_condition:
                    for statement in elseif['body']:
                        self.execute_statement(statement)
                    executed = True
                    break

            # 如果没有执行任何elseif分支，执行else分支
            if not executed and stmt.else_body:
                for statement in stmt.else_body:
                    self.execute_statement(statement)

    def execute_loop_statement(self, stmt: LoopStmt):
        """执行loop循环语句。

        参数：
            stmt: LoopStmt节点，包含循环体内的语句列表
        """
        while True:
            try:
                # 执行循环体内的所有语句
                for statement in stmt.body:
                    self.execute_statement(statement)
            except ExitLoopSignal:
                # 当exitwhen条件满足时，退出循环
                break

    def execute_exitwhen_statement(self, stmt: ExitWhenStmt):
        """执行exitwhen退出循环语句。

        参数：
            stmt: ExitWhenStmt节点，包含退出条件表达式
        """
        # 求值条件表达式
        condition_result = self.evaluator.evaluate_condition(stmt.condition)

        # 如果条件为真，抛出ExitLoopSignal退出循环
        if condition_result:
            raise ExitLoopSignal()

    def execute_return_statement(self, stmt: ReturnStmt):
        """执行return语句。

        参数：
            stmt: ReturnStmt节点，包含返回值表达式（可为None）
        """
        # 求值返回值（如果有）
        value = None
        if stmt.value:
            value = self.evaluator.evaluate(stmt.value)

        # 抛出ReturnSignal，携带返回值
        raise ReturnSignal(value)

    def _call_function_with_args(self, func: FunctionDecl, args: list):
        """使用指定参数调用函数。

        参数：
            func: 函数定义节点
            args: 参数值列表

        返回：
            函数返回值
        """
        # 保存当前上下文以便后续恢复
        previous_context = self.current_context

        # 创建新上下文
        func_context = ExecutionContext(
            self.global_context,
            native_registry=self.global_context.native_registry,
            state_context=self.state_context,
            interpreter=self
        )

        # 设置参数值
        for param, arg_value in zip(func.parameters, args):
            func_context.set_variable(param.name, arg_value)

        self.current_context = func_context
        self.evaluator.context = func_context

        # 执行函数体
        return_value = None
        try:
            if func.body:
                for statement in func.body:
                    self.execute_statement(statement)
        except ReturnSignal as signal:
            return_value = signal.value

        # 恢复上下文
        self.current_context = previous_context
        self.evaluator.context = previous_context

        return return_value
