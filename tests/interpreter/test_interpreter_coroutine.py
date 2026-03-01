"""Interpreter 协程支持测试。"""

from unittest.mock import Mock
import pytest
from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.coroutine.exceptions import SleepInterrupt


def test_interpreter_create_main_coroutine_no_main():
    """测试创建主协程：当没有 main 函数时返回 None。"""
    interpreter = Interpreter()
    ast = Mock()
    ast.globals = []
    ast.functions = []
    coroutine = interpreter.create_main_coroutine(ast)
    assert coroutine is None


def test_interpreter_create_main_coroutine_with_main():
    """测试创建主协程：当存在 main 函数时返回 JassCoroutine。"""
    from jass_runner.interpreter.coroutine import JassCoroutine

    interpreter = Interpreter()
    ast = Mock()
    ast.globals = []

    main_func = Mock()
    main_func.name = 'main'
    main_func.body = []
    main_func.parameters = []
    ast.functions = [main_func]

    coroutine = interpreter.create_main_coroutine(ast)

    assert coroutine is not None
    assert isinstance(coroutine, JassCoroutine)
    assert coroutine.func is main_func


def test_interpreter_create_main_coroutine_registers_globals():
    """测试创建主协程时注册全局变量。"""
    interpreter = Interpreter()
    ast = Mock()

    global_decl = Mock()
    global_decl.name = 'global_var'
    global_decl.type = 'integer'
    global_decl.value = 100
    ast.globals = [global_decl]

    ast.functions = []

    interpreter.create_main_coroutine(ast)

    assert interpreter.global_context.has_variable('global_var')
    assert interpreter.global_context.get_variable('global_var') == 100


def test_interpreter_create_main_coroutine_registers_functions():
    """测试创建主协程时注册函数。"""
    interpreter = Interpreter()
    ast = Mock()
    ast.globals = []

    func = Mock()
    func.name = 'my_func'
    func.body = []
    func.parameters = []
    ast.functions = [func]

    coroutine = interpreter.create_main_coroutine(ast)

    assert 'my_func' in interpreter.functions
    assert interpreter.functions['my_func'] is func


def test_interpreter_create_main_coroutine_with_params():
    """测试创建 main 协程时 main 函数无参数。"""
    from jass_runner.interpreter.coroutine import JassCoroutine

    interpreter = Interpreter()
    ast = Mock()
    ast.globals = []

    main_func = Mock()
    main_func.name = 'main'
    main_func.body = []
    main_func.parameters = []
    ast.functions = [main_func]

    coroutine = interpreter.create_main_coroutine(ast)

    assert isinstance(coroutine, JassCoroutine)
    assert coroutine.args == []  # main 函数调用不需要参数
