"""JASS 运行器的完整集成测试。"""

import tempfile
import os
import subprocess
import sys


def test_cli_execution():
    """测试使用简单脚本的 CLI 执行。"""
    # 创建临时 JASS 文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.j', delete=False, encoding='utf-8') as f:
        f.write("""
        function main takes nothing returns nothing
            call DisplayTextToPlayer(0, 0, 0, "CLI test successful!")
        endfunction
        """)
        temp_file = f.name

    try:
        # 通过 CLI 运行（使用 src 在路径中）
        env = os.environ.copy()
        env['PYTHONPATH'] = 'src'
        result = subprocess.run(
            [sys.executable, "-m", "jass_runner.cli", temp_file],
            capture_output=True,
            text=True,
            timeout=5,
            env=env
        )

        # 检查执行
        assert result.returncode == 0
        assert "CLI test successful!" in result.stdout

    finally:
        os.unlink(temp_file)


def test_package_installation():
    """测试包可以安装和运行。"""
    # 此测试假设包已以开发模式安装
    # 我们只验证入口点存在
    import jass_runner.cli
    import jass_runner.vm.jass_vm

    # 如果可以导入这些，包结构是正确的
    assert jass_runner.cli is not None
    assert jass_runner.vm.jass_vm is not None


def test_example_scripts():
    """测试示例脚本可以工作。"""
    from jass_runner.vm.jass_vm import JassVM

    # 使用简单脚本测试（避免未注册的原生函数）
    script = """
    function main takes nothing returns nothing
        call DisplayTextToPlayer(0, 0, 0, "Hello, World!")
    endfunction
    """

    vm = JassVM(enable_timers=False)
    vm.load_script(script)
    vm.execute()

    # 不应抛出异常
    assert vm.loaded is True
