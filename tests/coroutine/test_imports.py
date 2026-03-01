"""测试协程模块导出。"""


def test_coroutine_module_exports():
    """测试协程模块导出。"""
    from jass_runner.coroutine import (
        CoroutineStatus,
        SleepSignal,
        SleepInterrupt,
        Coroutine,
        SleepScheduler,
        CoroutineRunner,
        CoroutineError,
        CoroutineStackOverflow,
    )

    assert CoroutineStatus is not None
    assert SleepSignal is not None
    assert SleepInterrupt is not None
    assert Coroutine is not None
    assert SleepScheduler is not None
    assert CoroutineRunner is not None
    assert CoroutineError is not None
    assert CoroutineStackOverflow is not None
