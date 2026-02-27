"""JassVM 的集成测试。"""

import tempfile
import os


def test_vm_basic_execution():
    """测试使用简单脚本的基本 VM 执行。"""
    from jass_runner.vm.jass_vm import JassVM

    # 简单的 JASS 脚本
    script = """
    function main takes nothing returns nothing
        // 简单的测试函数
    endfunction
    """

    vm = JassVM(enable_timers=False)
    vm.load_script(script)
    vm.execute()

    assert vm.loaded is True
    assert vm.ast is not None


def test_vm_file_loading():
    """测试 VM 从文件加载脚本。"""
    from jass_runner.vm.jass_vm import JassVM

    # 创建临时 JASS 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.j', delete=False, encoding='utf-8') as f:
        f.write("""
        function test takes nothing returns nothing
            // 测试函数
        endfunction
        """)
        temp_file = f.name

    try:
        vm = JassVM(enable_timers=False)
        vm.load_file(temp_file)
        vm.execute()

        assert vm.loaded is True
        assert vm.ast is not None
    finally:
        os.unlink(temp_file)


def test_vm_with_natives():
    """测试使用原生函数的 VM 执行。"""
    import logging
    from io import StringIO
    from jass_runner.vm.jass_vm import JassVM

    # 捕获日志输出
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.basic')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # 包含原生调用的脚本
    script = """
    function main takes nothing returns nothing
        call DisplayTextToPlayer(0, 0, 0, "Hello from VM!")
    endfunction
    """

    vm = JassVM(enable_timers=False)
    vm.load_script(script)
    vm.execute()

    # 检查日志输出
    log_output = log_stream.getvalue()
    assert "[DisplayTextToPlayer]玩家0: Hello from VM!" in log_output

    logger.removeHandler(handler)
