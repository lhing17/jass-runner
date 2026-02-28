"""测试表达式求值器。"""

def test_operator_precedence_constants():
    """测试运算符优先级常量定义。"""
    from jass_runner.interpreter.evaluator import Evaluator, OperatorPrecedence

    assert OperatorPrecedence.UNARY == 7
    assert OperatorPrecedence.MULTIPLICATIVE == 6
    assert OperatorPrecedence.ADDITIVE == 5
    assert OperatorPrecedence.RELATIONAL == 4
    assert OperatorPrecedence.EQUALITY == 3
    assert OperatorPrecedence.AND == 2
    assert OperatorPrecedence.OR == 1


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


def test_evaluate_arithmetic_addition():
    """测试加法运算。"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)
    result = evaluator.evaluate("5 + 3")
    assert result == 8


def test_evaluate_arithmetic_mixed_types():
    """测试混合类型运算。"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)
    result = evaluator.evaluate("5 + 3.5")
    assert result == 8.5
    assert isinstance(result, float)


def test_evaluate_arithmetic_all_operators():
    """测试所有算术运算符。"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)
    assert evaluator.evaluate("10 - 3") == 7
    assert evaluator.evaluate("4 * 5") == 20
    assert evaluator.evaluate("15 / 3") == 5.0