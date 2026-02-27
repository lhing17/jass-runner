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


def test_evaluator_can_evaluate_native_call():
    """测试求值器可以求值原生函数调用。"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext
    from jass_runner.natives.base import NativeFunction
    from jass_runner.natives.registry import NativeRegistry
    from jass_runner.parser.parser import NativeCallNode

    # 创建一个模拟的原生函数
    class MockNativeFunction(NativeFunction):
        name = "DisplayTextToPlayer"

        def execute(self, state_context, *args):
            return f"Called {self.name} with args: {args}"

    # 设置带有原生函数的上下文
    registry = NativeRegistry()
    registry.register(MockNativeFunction())
    context = ExecutionContext(native_registry=registry)

    evaluator = Evaluator(context)

    # 创建一个原生调用节点
    node = NativeCallNode(
        func_name="DisplayTextToPlayer",
        args=["player", "message"]
    )

    # 测试原生调用求值
    result = evaluator.evaluate(node)
    assert result == "Called DisplayTextToPlayer with args: ('player', 'message')"