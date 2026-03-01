"""协程信号测试。"""


def test_sleep_signal_creation():
    """测试SleepSignal创建。"""
    from jass_runner.coroutine.signals import SleepSignal
    signal = SleepSignal(2.5)
    assert signal.duration == 2.5
