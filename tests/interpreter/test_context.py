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