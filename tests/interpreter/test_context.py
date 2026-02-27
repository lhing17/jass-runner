"""Test execution context."""

def test_execution_context_creation():
    """Test that execution context can be created."""
    from src.jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    assert context is not None
    assert hasattr(context, 'variables')
    assert isinstance(context.variables, dict)


def test_variable_operations():
    """Test setting and getting variables."""
    from src.jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()

    # Set variable
    context.set_variable('x', 42)
    assert context.has_variable('x') == True

    # Get variable
    value = context.get_variable('x')
    assert value == 42

    # Check non-existent variable
    assert context.has_variable('y') == False


def test_nested_contexts():
    """Test variable lookup in nested contexts."""
    from src.jass_runner.interpreter.context import ExecutionContext

    parent = ExecutionContext()
    parent.set_variable('global', 100)

    child = ExecutionContext(parent)

    # Child can access parent variable
    assert child.has_variable('global') == True
    assert child.get_variable('global') == 100

    # Child can set its own variable
    child.set_variable('local', 200)
    assert child.get_variable('local') == 200

    # Parent cannot access child variable
    assert parent.has_variable('local') == False


def test_execution_context_with_natives():
    """Test execution context with native functions."""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    registry = factory.create_default_registry()

    context = ExecutionContext(native_registry=registry)

    # Check native registry is attached
    assert context.native_registry is registry

    # Check we can get native functions
    display_func = context.get_native_function("DisplayTextToPlayer")
    assert display_func is not None
    assert display_func.name == "DisplayTextToPlayer"


def test_execution_context_with_timer_system():
    """测试带有计时器系统的执行上下文。"""
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.timer.system import TimerSystem
    from jass_runner.natives.factory import NativeFactory

    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    context = ExecutionContext(native_registry=registry, timer_system=timer_system)

    # 检查计时器系统已附加
    assert context.timer_system is timer_system

    # 检查计时器原生函数可用
    create_timer_func = context.get_native_function("CreateTimer")
    assert create_timer_func is not None