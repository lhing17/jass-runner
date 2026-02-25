"""Test expression evaluator."""

def test_evaluator_can_evaluate_literal():
    """Test that evaluator can evaluate literal values."""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    # Test integer literal
    result = evaluator.evaluate('42')
    assert result == 42

    # Test string literal
    result = evaluator.evaluate('"hello"')
    assert result == "hello"


def test_evaluator_can_evaluate_variables():
    """Test that evaluator can evaluate variable references."""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    context.set_variable('x', 100)
    context.set_variable('name', 'John')

    evaluator = Evaluator(context)

    # Test variable reference
    result = evaluator.evaluate('x')
    assert result == 100

    result = evaluator.evaluate('name')
    assert result == 'John'