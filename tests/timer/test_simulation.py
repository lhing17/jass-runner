"""测试模拟循环。"""

def test_simulation_loop_creation():
    """测试 SimulationLoop 可以被创建。"""
    from jass_runner.timer.simulation import SimulationLoop
    from jass_runner.timer.system import TimerSystem

    timer_system = TimerSystem()
    loop = SimulationLoop(timer_system=timer_system)
    assert loop is not None
    assert hasattr(loop, 'run_frames')
    assert hasattr(loop, 'current_frame')
