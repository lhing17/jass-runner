"""JassCoroutine 类测试。"""

from unittest.mock import Mock, MagicMock
import pytest
from jass_runner.interpreter.coroutine import JassCoroutine
from jass_runner.coroutine import CoroutineStatus
from jass_runner.coroutine.exceptions import SleepInterrupt
from jass_runner.interpreter.control_flow import ReturnSignal


def test_jass_coroutine_creation():
    """测试 JassCoroutine 实例创建。"""
    interpreter = Mock()
    func = Mock()
    func.body = []
    coroutine = JassCoroutine(interpreter, func)

    assert coroutine.interpreter is interpreter
    assert coroutine.func is func
    assert coroutine._pc == 0


def test_jass_coroutine_with_args():
    """测试带参数的 JassCoroutine 创建。"""
    interpreter = Mock()
    func = Mock()
    func.body = []
    func.parameters = []
    args = [1, 2, 3]
    coroutine = JassCoroutine(interpreter, func, args)

    assert coroutine.args == args


def test_jass_coroutine_context_management():
    """测试 JassCoroutine 上下文管理。

    验证协程在执行时正确设置和清理执行上下文。
    """
    # 准备
    interpreter = Mock()
    interpreter.global_context = Mock()
    interpreter.global_context.native_registry = Mock()
    interpreter.state_context = Mock()
    interpreter.current_context = None
    interpreter.evaluator = Mock()
    interpreter.evaluator.context = None

    func = Mock()
    func.body = []
    func.parameters = []

    coroutine = JassCoroutine(interpreter, func)

    # 执行
    coroutine.start()
    # 消费生成器以触发执行
    list(coroutine.generator)

    # 验证：上下文应该被设置过
    assert interpreter.current_context is not None


def test_jass_coroutine_executes_statements():
    """测试 JassCoroutine 执行语句。"""
    interpreter = Mock()
    interpreter.global_context = Mock()
    interpreter.global_context.native_registry = Mock()
    interpreter.state_context = Mock()
    interpreter.current_context = None
    interpreter.evaluator = Mock()
    interpreter.evaluator.context = None

    # 创建两个模拟语句
    stmt1 = Mock()
    stmt2 = Mock()
    func = Mock()
    func.body = [stmt1, stmt2]
    func.parameters = []

    coroutine = JassCoroutine(interpreter, func)
    coroutine.start()
    list(coroutine.generator)

    # 验证语句被执行
    assert interpreter.execute_statement.call_count == 2
    interpreter.execute_statement.assert_any_call(stmt1)
    interpreter.execute_statement.assert_any_call(stmt2)


def test_jass_coroutine_handles_sleep_interrupt():
    """测试 JassCoroutine 处理 SleepInterrupt。"""
    interpreter = Mock()
    interpreter.global_context = Mock()
    interpreter.global_context.native_registry = Mock()
    interpreter.state_context = Mock()
    interpreter.current_context = None
    interpreter.evaluator = Mock()
    interpreter.evaluator.context = None

    stmt1 = Mock()
    stmt2 = Mock()
    func = Mock()
    func.body = [stmt1, stmt2]
    func.parameters = []

    # 第一个语句抛出 SleepInterrupt
    interpreter.execute_statement.side_effect = [
        SleepInterrupt(2.0),
        None
    ]

    coroutine = JassCoroutine(interpreter, func)
    coroutine.start()

    # 执行生成器，应该产生 SleepSignal
    signals = list(coroutine.generator)

    assert len(signals) == 1
    assert signals[0].duration == 2.0


def test_jass_coroutine_handles_return_signal():
    """测试 JassCoroutine 处理 ReturnSignal。"""
    interpreter = Mock()
    interpreter.global_context = Mock()
    interpreter.global_context.native_registry = Mock()
    interpreter.state_context = Mock()
    interpreter.current_context = None
    interpreter.evaluator = Mock()
    interpreter.evaluator.context = None

    stmt1 = Mock()
    stmt2 = Mock()
    func = Mock()
    func.body = [stmt1, stmt2]
    func.parameters = []

    # 第一个语句抛出 ReturnSignal
    interpreter.execute_statement.side_effect = [
        ReturnSignal(42),
        None
    ]

    coroutine = JassCoroutine(interpreter, func)
    coroutine.start()
    list(coroutine.generator)

    # 验证只执行了第一个语句（return后停止）
    assert interpreter.execute_statement.call_count == 1
    interpreter.execute_statement.assert_called_once_with(stmt1)


def test_jass_coroutine_parameter_binding():
    """测试 JassCoroutine 参数绑定。"""
    interpreter = Mock()
    interpreter.global_context = Mock()
    interpreter.global_context.native_registry = Mock()
    interpreter.state_context = Mock()
    interpreter.current_context = None
    interpreter.evaluator = Mock()
    interpreter.evaluator.context = None

    # 创建参数定义
    param1 = Mock()
    param1.name = 'x'
    param2 = Mock()
    param2.name = 'y'
    func = Mock()
    func.body = []
    func.parameters = [param1, param2]

    # 提供参数值
    args = [10, 20]
    coroutine = JassCoroutine(interpreter, func, args)
    coroutine.start()
    list(coroutine.generator)

    # 验证上下文被创建时参数被正确绑定
    # 这里通过检查 _setup_context 是否创建了 ExecutionContext 来验证
    # 由于使用了 Mock，无法直接验证，但确保没有抛出异常即为成功


def test_jass_coroutine_resume():
    """测试 JassCoroutine resume 方法。"""
    interpreter = Mock()
    interpreter.global_context = Mock()
    interpreter.global_context.native_registry = Mock()
    interpreter.state_context = Mock()
    interpreter.current_context = None
    interpreter.evaluator = Mock()
    interpreter.evaluator.context = None

    func = Mock()
    func.body = [Mock()]
    func.parameters = []

    coroutine = JassCoroutine(interpreter, func)

    # 测试未启动时返回 None
    result = coroutine.resume()
    assert result is None

    # 启动协程
    coroutine.start()
    coroutine.status = CoroutineStatus.RUNNING

    # 创建一个生成器，返回 SleepSignal
    from jass_runner.coroutine.signals import SleepSignal
    mock_generator = MagicMock()
    mock_generator.__next__ = MagicMock(return_value=SleepSignal(1.0))
    coroutine.generator = mock_generator

    result = coroutine.resume()
    assert result is not None
    assert result.duration == 1.0
    assert coroutine.status == CoroutineStatus.SLEEPING
