"""Camera 函数的集成测试。

验证 Camera 相关 native 函数与常量加载机制的完整工作流。
"""

import pytest
from src.jass_runner.vm.jass_vm import JassVM


class TestCameraWorkflow:
    """测试 Camera 相关函数的完整工作流。"""

    def test_get_camera_margin_with_constant(self):
        """测试使用常量调用 GetCameraMargin。"""
        vm = JassVM()

        # 从 common.j 加载的常量
        global_vars = vm.interpreter.global_context.variables
        margin_type = global_vars['CAMERA_MARGIN_LEFT']

        # 通过注册表获取 native
        get_margin = vm.native_registry.get('GetCameraMargin')

        # 使用常量值调用
        result = get_margin.execute(vm.interpreter.state_context, margin_type)

        assert result == 100.0

    def test_set_camera_bounds_stores_values(self):
        """测试 SetCameraBounds 存储边界值。"""
        vm = JassVM()

        set_bounds = vm.native_registry.get('SetCameraBounds')

        # 典型的魔兽3相机边界设置
        set_bounds.execute(
            vm.interpreter.state_context,
            -11520.0, -11776.0, 11520.0, 11264.0,
            -11520.0, 11264.0, 11520.0, -11776.0
        )

        bounds = vm.interpreter.state_context.camera_bounds
        assert bounds['x1'] == -11520.0
        assert bounds['y1'] == -11776.0
        assert bounds['x2'] == 11520.0
        assert bounds['y2'] == 11264.0
        assert bounds['x3'] == -11520.0
        assert bounds['y3'] == 11264.0
        assert bounds['x4'] == 11520.0
        assert bounds['y4'] == -11776.0
