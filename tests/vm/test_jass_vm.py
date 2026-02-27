"""测试 JassVM 类。"""

def test_jass_vm_creation():
    """测试 JassVM 可以被创建。"""
    from jass_runner.vm.jass_vm import JassVM

    vm = JassVM()
    assert vm is not None
    assert hasattr(vm, 'load_script')
    assert hasattr(vm, 'execute')
    assert hasattr(vm, 'run')


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
