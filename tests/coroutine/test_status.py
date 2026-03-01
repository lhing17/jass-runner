"""协程状态测试。"""

from jass_runner.coroutine import CoroutineStatus


def test_coroutine_status_values():
    """测试协程状态枚举值。"""
    assert CoroutineStatus.PENDING.value == "pending"
    assert CoroutineStatus.RUNNING.value == "running"
    assert CoroutineStatus.SLEEPING.value == "sleeping"
    assert CoroutineStatus.FINISHED.value == "finished"
