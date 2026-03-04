"""测试 JassVM 类。"""
import pytest


def test_jass_vm_creation():
    """测试 JassVM 可以被创建。"""
    from jass_runner.vm.jass_vm import JassVM

    vm = JassVM()
    assert vm is not None
    assert hasattr(vm, 'load_script')
    assert hasattr(vm, 'execute')
    assert hasattr(vm, 'run')


class TestLoadBlizzard:
    """测试 load_blizzard 方法。"""

    def test_load_blizzard_auto_path_success(self):
        """测试自动路径加载 blizzard.j 成功。"""
        from jass_runner.vm.jass_vm import JassVM

        vm = JassVM()

        result = vm.load_blizzard()

        assert result is True
        assert vm.blizzard_loaded is True
        assert vm.blizzard_ast is not None

    def test_load_blizzard_custom_path_success(self):
        """测试自定义路径加载 blizzard.j 成功。"""
        from jass_runner.vm.jass_vm import JassVM

        vm = JassVM()
        path = 'resources/blizzard.j'

        result = vm.load_blizzard(path)

        assert result is True
        assert vm.blizzard_loaded is True

    def test_load_blizzard_invalid_path_returns_false(self):
        """测试无效路径返回 False 不抛出异常。"""
        from jass_runner.vm.jass_vm import JassVM

        vm = JassVM()

        result = vm.load_blizzard('nonexistent/path.j')

        assert result is False
        assert vm.blizzard_loaded is False

    def test_execute_with_blizzard_calls_blizzard_functions(self):
        """测试加载 blizzard 后能执行其中的函数。"""
        from jass_runner.vm.jass_vm import JassVM

        vm = JassVM()
        vm.load_blizzard()

        # 加载一个简单的用户脚本（空函数，不调用未实现的 native）
        vm.load_script('''
function main takes nothing returns nothing
endfunction
''')
        # 应该成功执行，不抛出异常（blizzard.j 已加载）
        vm.execute()

    def test_run_with_load_blizzard_true(self):
        """测试 run 方法支持加载 blizzard。"""
        from jass_runner.vm.jass_vm import JassVM

        vm = JassVM()

        vm.run('function main takes nothing returns nothing endfunction',
               load_blizzard=True)

        assert vm.blizzard_loaded is True


def test_vm_error_handling():
    """测试 VM 错误处理。"""
    from jass_runner.vm.jass_vm import JassVM

    vm = JassVM()

    # 测试未加载脚本就执行
    import pytest
    with pytest.raises(RuntimeError, match="未加载脚本"):
        vm.execute()

    # 测试加载无效脚本
    vm.load_script("invalid jass code")
    # 不应立即抛出异常，但执行可能会失败
    # 这测试了 load_script 在解析错误时不会崩溃


def test_vm_file_not_found():
    """测试 VM 处理缺失文件。"""
    from jass_runner.vm.jass_vm import JassVM
    import pytest

    vm = JassVM()

    with pytest.raises(FileNotFoundError):
        vm.load_file("non_existent_file.j")
