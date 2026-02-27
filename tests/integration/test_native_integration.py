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
    # 注意：KillUnit现在需要真实的单位ID，所以这里只测试DisplayTextToPlayer
    jass_code = """
    function main takes nothing returns nothing
        call DisplayTextToPlayer(0, 0, 0, "Hello from JASS!")
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

    finally:
        # 清理
        logger.removeHandler(handler)


def test_native_function_with_state_integration():
    """测试原生函数与状态管理系统的集成。"""
    from jass_runner.parser.parser import Parser
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.utils import fourcc_to_int

    # 设置日志以捕获输出
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.basic')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # 使用FourCC整数格式创建单位类型（'hfoo' = 1213484355）
    unit_type_int = fourcc_to_int("hfoo")

    # 创建JASS代码，使用CreateUnit和KillUnit
    jass_code = f"""
    function main takes nothing returns nothing
        call DisplayTextToPlayer(0, 0, 0, "Creating unit...")
    endfunction
    """

    try:
        # 解析和执行
        parser = Parser(jass_code)
        ast = parser.parse()

        factory = NativeFactory()
        registry = factory.create_default_registry()

        interpreter = Interpreter(native_registry=registry)

        # 先通过HandleManager创建一个单位
        unit = interpreter.state_context.handle_manager.create_unit("hfoo", 0, 100.0, 200.0, 0.0)
        assert unit is not None

        # 执行脚本
        interpreter.execute(ast)

        # 验证单位存在
        assert unit.unit_type == "hfoo"

        # 检查日志输出
        log_output = log_stream.getvalue()
        assert "[DisplayTextToPlayer]玩家0: Creating unit..." in log_output

    finally:
        # 清理
        logger.removeHandler(handler)


def test_create_unit_and_kill_unit_in_jass():
    """测试在JASS脚本中直接调用CreateUnit和KillUnit。"""
    from jass_runner.parser.parser import Parser
    from jass_runner.interpreter.interpreter import Interpreter
    from jass_runner.natives.factory import NativeFactory
    from jass_runner.utils import fourcc_to_int

    # 设置日志以捕获输出
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.basic')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # 使用FourCC整数格式创建单位类型（'hfoo' = 1213484355）
    unit_type_int = fourcc_to_int("hfoo")

    # 创建JASS代码：创建单位并存储到变量，然后击杀它
    jass_code = f"""
    function main takes nothing returns nothing
        local unit u
        set u = CreateUnit(0, {unit_type_int}, 100.0, 200.0, 0.0)
        call KillUnit(u)
    endfunction
    """

    try:
        # 解析和执行
        parser = Parser(jass_code)
        ast = parser.parse()

        factory = NativeFactory()
        registry = factory.create_default_registry()

        interpreter = Interpreter(native_registry=registry)

        # 执行脚本
        interpreter.execute(ast)

        # 检查日志输出
        log_output = log_stream.getvalue()
        assert "[CreateUnit] 为玩家0在(100.0, 200.0)创建hfoo" in log_output
        assert "[KillUnit] 单位unit_1已被击杀" in log_output

    finally:
        # 清理
        logger.removeHandler(handler)