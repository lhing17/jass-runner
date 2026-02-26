"""原生函数集成测试。"""

import logging
from io import StringIO


def test_native_function_integration():
    """测试原生函数与解释器的集成。"""
    from jass_runner.parser.parser import Parser
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.natives.factory import NativeFactory

    # 设置日志以捕获输出
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.basic')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # 包含原生函数调用的JASS代码
    jass_code = """
    function main takes nothing returns nothing
        call DisplayTextToPlayer(0, 0, 0, "Hello from JASS!")
        call KillUnit("footman_001")
    endfunction
    """

    try:
        # 解析和执行
        parser = Parser(jass_code)
        ast = parser.parse()

        factory = NativeFactory()
        registry = factory.create_default_registry()

        interpreter = Interpreter(native_registry=registry)
        interpreter.execute(ast)

        # 检查日志输出
        log_output = log_stream.getvalue()
        assert "[DisplayTextToPlayer]玩家0: Hello from JASS!" in log_output
        assert "[KillUnit] 单位footman_001已被击杀" in log_output

    finally:
        # 清理
        logger.removeHandler(handler)