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


def test_execute_func_creates_coroutine():
    """测试 ExecuteFunc 创建新协程执行指定函数。"""
    from jass_runner.natives.async_natives import ExecuteFunc
    from unittest.mock import Mock

    execute_func = ExecuteFunc()
    mock_interpreter = Mock()
    mock_func = Mock()
    mock_func.body = []
    mock_interpreter.functions = {"test_func": mock_func}
    mock_interpreter.coroutine_runner = Mock()

    execute_func.interpreter = mock_interpreter
    execute_func.execute(None, "test_func")

    mock_interpreter.coroutine_runner.execute_func.assert_called_once()

