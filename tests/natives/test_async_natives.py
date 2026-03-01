"""异步 native 函数测试。"""


def test_trigger_sleep_action_raises_interrupt():
    """测试 TriggerSleepAction 抛出 SleepInterrupt 异常。"""
    from jass_runner.natives.async_natives import TriggerSleepAction
    from jass_runner.coroutine.exceptions import SleepInterrupt

    sleep_action = TriggerSleepAction()
    try:
        sleep_action.execute(None, 2.0)
        assert False, "应该抛出 SleepInterrupt"
    except SleepInterrupt as e:
        assert e.duration == 2.0
