"""数组功能集成测试。"""

from jass_runner.parser.parser import Parser
from jass_runner.interpreter.interpreter import Interpreter


def test_complete_array_workflow():
    """测试完整的数组声明、赋值、访问流程。"""
    code = """
globals
    integer array scores
endglobals

function Test takes nothing returns nothing
    local integer array temp

    set scores[0] = 100
endfunction
"""

    # 解析
    parser = Parser(code)
    ast = parser.parse()
    assert len(parser.errors) == 0

    # 执行
    interpreter = Interpreter()
    interpreter.execute(ast)
    interpreter.execute_function(interpreter.functions['Test'])

    # 验证全局数组
    assert interpreter.global_context.get_array_element("scores", 0) == 100
