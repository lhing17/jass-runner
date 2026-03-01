"""协程类测试。"""

from jass_runner.coroutine.coroutine import Coroutine
from jass_runner.coroutine import CoroutineStatus


def test_coroutine_creation():
    """测试协程创建。"""
    # Mock interpreter and function
    interpreter = object()
    func = object()

    coroutine = Coroutine(interpreter, func)

    assert coroutine.interpreter is interpreter
    assert coroutine.func is func
    assert coroutine.status == CoroutineStatus.PENDING
    assert coroutine.args == []
    assert coroutine.generator is None
    assert coroutine.wake_time == 0.0
