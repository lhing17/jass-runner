"""Fog native 函数测试。

此模块包含战争迷雾相关 native 函数的测试。
"""

import pytest


class TestFogState:
    """测试 FogState 类的功能。"""

    def test_fog_state_default_values(self):
        """测试 FogState 默认值为启用状态。"""
        from jass_runner.natives.fog_natives import FogState

        state = FogState()

        assert state.mask_enabled is True
        assert state.fog_enabled is True


def test_fog_mask_enable_sets_state():
    """测试 FogMaskEnable 设置黑色遮罩状态。"""
    from jass_runner.natives.fog_natives import FogMaskEnable, FogState

    state = FogState()
    native = FogMaskEnable(state)

    # 禁用遮罩
    native.execute([False])
    assert state.mask_enabled is False

    # 启用遮罩
    native.execute([True])
    assert state.mask_enabled is True
