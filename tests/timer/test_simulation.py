"""测试模拟循环。"""

def test_simulation_loop_creation():
    """测试 SimulationLoop 可以被创建。"""
    from jass_runner.timer.simulation import SimulationLoop

    loop = SimulationLoop()
    assert loop is not None
    assert hasattr(loop, 'run_frames')
    assert hasattr(loop, 'frame_count')
    assert loop.timer_system is not None
    assert loop.coroutine_runner is not None
