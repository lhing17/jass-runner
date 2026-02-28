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


def test_operator_precedence_multiplication_before_addition():
    """测试乘法优先级高于加法。"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)
    # 2 + 3 * 4 应该等于 14，不是 20
    result = evaluator.evaluate("2 + 3 * 4")
    assert result == 14


def test_operator_precedence_with_parentheses():
    """测试括号优先级。"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)
    # (2 + 3) * 4 应该等于 20
    result = evaluator.evaluate("(2 + 3) * 4")
    assert result == 20


def test_evaluate_comparison_operators():
    """测试比较运算符。"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate("5 == 5") is True
    assert evaluator.evaluate("5 != 3") is True
    assert evaluator.evaluate("5 > 3") is True
    assert evaluator.evaluate("3 < 5") is True
    assert evaluator.evaluate("5 >= 5") is True
    assert evaluator.evaluate("3 <= 5") is True


def test_evaluate_logical_operators():
    """测试逻辑运算符"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate("true and true") is True
    assert evaluator.evaluate("true and false") is False
    assert evaluator.evaluate("true or false") is True
    assert evaluator.evaluate("false or false") is False
    assert evaluator.evaluate("not true") is False
    assert evaluator.evaluate("not false") is True


def test_evaluate_complex_logical_expression():
    """测试复杂逻辑表达式"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    # (5 > 3) and (2 < 4)
    result = evaluator.evaluate("5 > 3 and 2 < 4")
    assert result is True


def test_evaluate_condition_simple():
    """测试条件求值"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate_condition("5 > 3") is True
    assert evaluator.evaluate_condition("5 < 3") is False
    assert evaluator.evaluate_condition("true") is True
    assert evaluator.evaluate_condition("false") is False


def test_evaluate_condition_complex():
    """测试复杂条件求值"""
    from jass_runner.interpreter.evaluator import Evaluator
    from jass_runner.interpreter.context import ExecutionContext

    context = ExecutionContext()
    evaluator = Evaluator(context)

    assert evaluator.evaluate_condition("5 > 3 and 2 < 4") is True
    assert evaluator.evaluate_condition("not false") is True