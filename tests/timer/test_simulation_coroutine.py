"""测试模拟循环协程集成。"""

import pytest
from unittest.mock import Mock, patch, MagicMock


def test_simulation_loop_has_coroutine_runner():
    """测试 SimulationLoop 有 coroutine_runner 和 timer_system 属性。"""
    from jass_runner.timer.simulation import SimulationLoop
    loop = SimulationLoop()
    assert loop.coroutine_runner is not None
    assert loop.timer_system is not None


def test_simulation_loop_init_with_fps():
    """测试 SimulationLoop 使用 fps 参数初始化。"""
    from jass_runner.timer.simulation import SimulationLoop
    loop = SimulationLoop(fps=60.0)
    assert loop.fps == 60.0
    assert loop.frame_duration == 1.0 / 60.0


def test_simulation_loop_run():
    """测试 SimulationLoop.run 方法。"""
    from jass_runner.timer.simulation import SimulationLoop
    loop = SimulationLoop()
    interpreter = Mock()
    ast = Mock()
    ast.globals = []
    ast.functions = []

    # 直接修补 _start_main 方法，不创建任何协程
    with patch.object(loop, '_start_main'):
        # 模拟 is_finished 在第一次调用后返回 True
        call_count = [0]
        def is_finished_side_effect():
            call_count[0] += 1
            return call_count[0] > 1  # 第一次返回 False，后续返回 True

        with patch.object(loop.coroutine_runner, 'is_finished', side_effect=is_finished_side_effect):
            result = loop.run(interpreter, ast, max_frames=10)

    assert 'frames' in result
    assert 'time' in result
    assert 'success' in result


def test_simulation_loop_run_with_main_function():
    """测试 SimulationLoop.run 能处理包含 main 函数的 AST。"""
    from jass_runner.timer.simulation import SimulationLoop
    loop = SimulationLoop()
    interpreter = Mock()

    # 创建模拟的 main 函数
    main_func = Mock()
    main_func.name = 'main'
    main_func.body = []

    ast = Mock()
    ast.globals = []
    ast.functions = [main_func]

    # 模拟 interpreter.functions.get 返回 main 函数
    interpreter.functions = {'main': main_func}
    interpreter.execute_global_declaration = Mock()

    result = loop.run(interpreter, ast, max_frames=5)
    assert 'frames' in result
    assert 'time' in result
    assert 'success' in result


def test_update_frame():
    """测试 _update_frame 方法。"""
    from jass_runner.timer.simulation import SimulationLoop
    loop = SimulationLoop(fps=30.0)

    initial_time = loop.current_time
    initial_frame = loop.frame_count

    loop._update_frame()

    assert loop.frame_count == initial_frame + 1
    assert loop.current_time == initial_time + loop.frame_duration
