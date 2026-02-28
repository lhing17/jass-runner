"""测试全局变量执行。"""

from jass_runner.interpreter.interpreter import Interpreter
from jass_runner.parser.parser import Parser


def test_execute_globals_initialization():
    """测试全局变量正确初始化。"""
    code = """
globals
    integer counter = 10
    real value = 3.14
endglobals

function main takes nothing returns nothing
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证全局变量已初始化
    assert interpreter.global_context.get_variable('counter') == 10
    assert interpreter.global_context.get_variable('value') == 3.14


def test_execute_globals_access_in_function():
    """测试函数内访问全局变量。"""
    code = """
globals
    integer global_x = 5
endglobals

function main takes nothing returns nothing
    local integer y = global_x + 1
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 函数执行成功即表示测试通过
    assert True


def test_execute_globals_modify_in_function():
    """测试函数内修改全局变量。"""
    code = """
globals
    integer counter = 0
endglobals

function main takes nothing returns nothing
    set counter = counter + 1
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证全局变量已被修改
    assert interpreter.global_context.get_variable('counter') == 1


def test_execute_globals_persistence():
    """测试全局变量在多次调用间保持状态。"""
    code = """
globals
    integer call_count = 0
endglobals

function increment takes nothing returns nothing
    set call_count = call_count + 1
endfunction

function main takes nothing returns nothing
    call increment()
    call increment()
    call increment()
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证全局变量保持状态
    assert interpreter.global_context.get_variable('call_count') == 3


def test_execute_constant_access():
    """测试在函数内访问 constant 常量。"""
    code = """
globals
    constant integer MAX_SIZE = 100
    constant real PI = 3.14159
    constant string APP_NAME = "TestApp"
    constant boolean DEBUG_MODE = true
endglobals

function main takes nothing returns nothing
    local integer size = MAX_SIZE
    local real pi_value = PI
    local string name = APP_NAME
    local boolean debug = DEBUG_MODE
endfunction
"""
    parser = Parser(code)
    ast = parser.parse()

    assert len(parser.errors) == 0, f"解析错误: {parser.errors}"

    interpreter = Interpreter()
    interpreter.execute(ast)

    # 验证常量已正确初始化
    assert interpreter.global_context.get_variable('MAX_SIZE') == 100
    assert interpreter.global_context.get_variable('PI') == 3.14159
    assert interpreter.global_context.get_variable('APP_NAME') == 'TestApp'
    assert interpreter.global_context.get_variable('DEBUG_MODE') is True
