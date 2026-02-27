"""计时器系统的集成测试。"""

import logging
from io import StringIO


def test_timer_system_integration():
    """测试计时器系统与原生函数的集成。"""
    from jass_runner.timer.system import TimerSystem
    from jass_runner.timer.simulation import SimulationLoop
    from jass_runner.natives.factory import NativeFactory

    # 设置日志以捕获输出
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('jass_runner.natives.timer_natives')
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # 创建计时器系统和模拟
    timer_system = TimerSystem()
    factory = NativeFactory(timer_system=timer_system)
    registry = factory.create_default_registry()

    # 获取计时器原生函数
    create_timer = registry.get("CreateTimer")
    timer_start = registry.get("TimerStart")
    timer_get_elapsed = registry.get("TimerGetElapsed")

    # 创建并启动计时器
    timer_id = create_timer.execute(None)
    assert timer_id is not None

    # 跟踪回调调用
    callback_calls = []

    def test_callback():
        callback_calls.append("called")

    # 启动计时器（1秒超时，一次性）
    timer_start.execute(None, timer_id, 1.0, False, test_callback)

    # 创建模拟循环
    simulation = SimulationLoop(timer_system, frame_duration=0.05)  # 测试用20 FPS

    # 运行模拟0.5秒（不应触发回调）
    simulation.run_seconds(0.5)
    assert len(callback_calls) == 0

    # 检查经过时间
    elapsed = timer_get_elapsed.execute(None, timer_id)
    assert 0.4 <= elapsed <= 0.6  # 允许一定容差

    # 再运行模拟0.6秒（应触发回调）
    simulation.run_seconds(0.6)
    assert len(callback_calls) == 1

    # 清理
    logger.removeHandler(handler)

    # 检查日志输出
    log_output = log_stream.getvalue()
    assert f"[CreateTimer] Created timer: {timer_id}" in log_output
    assert f"[TimerStart] Started timer {timer_id}" in log_output
