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


def test_fog_enable_sets_state():
    """测试 FogEnable 设置战争迷雾状态。"""
    from jass_runner.natives.fog_natives import FogEnable, FogState

    state = FogState()
    native = FogEnable(state)

    # 禁用迷雾
    native.execute([False])
    assert state.fog_enabled is False

    # 启用迷雾
    native.execute([True])
    assert state.fog_enabled is True


def test_is_fog_mask_enabled_returns_state():
    """测试 IsFogMaskEnabled 返回黑色遮罩状态。"""
    from jass_runner.natives.fog_natives import IsFogMaskEnabled, FogState

    state = FogState()
    native = IsFogMaskEnabled(state)

    # 默认启用
    result = native.execute([])
    assert result is True

    # 禁用后查询
    state.mask_enabled = False
    result = native.execute([])
    assert result is False
