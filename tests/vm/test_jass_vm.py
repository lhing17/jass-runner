"""测试 JassVM 类。"""

def test_jass_vm_creation():
    """测试 JassVM 可以被创建。"""
    from jass_runner.vm.jass_vm import JassVM

    vm = JassVM()
    assert vm is not None
    assert hasattr(vm, 'load_script')
    assert hasattr(vm, 'execute')
    assert hasattr(vm, 'run')
