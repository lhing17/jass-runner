"""Test execution context."""

def test_execution_context_creation():
    """Test that execution context can be created."""
    from src.jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    assert context is not None
    assert hasattr(context, 'variables')
    assert isinstance(context.variables, dict)