"""测试与计时器相关的原生函数。"""

def test_create_timer_native():
    """测试 CreateTimer 原生函数。"""
    from jass_runner.natives.timer_natives import CreateTimer
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    native = CreateTimer(timer_system=system)
    assert native.name == "CreateTimer"

    # 创建计时器（测试时传递 None 作为 state_context）
    timer_id = native.execute(None)
    assert timer_id is not None
    assert timer_id.startswith("timer_")

    # 验证计时器存在于系统中
    timer = system.get_timer(timer_id)
    assert timer is not None


def test_destroy_timer_native():
    """测试 DestroyTimer 原生函数。"""
    from jass_runner.natives.timer_natives import DestroyTimer
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    native = DestroyTimer(timer_system=system)

    # 首先创建一个计时器
    timer_id = system.create_timer()
    assert system.get_timer(timer_id) is not None

    # 销毁计时器
    result = native.execute(None, timer_id)
    assert result is True
    assert system.get_timer(timer_id) is None


def test_pause_timer_native():
    """测试 PauseTimer 原生函数。"""
    from jass_runner.natives.timer_natives import PauseTimer
    from jass_runner.timer.system import TimerSystem

    system = TimerSystem()
    native = PauseTimer(timer_system=system)

    timer_id = system.create_timer()
    result = native.execute(None, timer_id)
    assert result is True
