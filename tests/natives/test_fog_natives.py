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
    native.execute(None, False)
    assert state.mask_enabled is False

    # 启用遮罩
    native.execute(None, True)
    assert state.mask_enabled is True


def test_fog_enable_sets_state():
    """测试 FogEnable 设置战争迷雾状态。"""
    from jass_runner.natives.fog_natives import FogEnable, FogState

    state = FogState()
    native = FogEnable(state)

    # 禁用迷雾
    native.execute(None, False)
    assert state.fog_enabled is False

    # 启用迷雾
    native.execute(None, True)
    assert state.fog_enabled is True


def test_is_fog_mask_enabled_returns_state():
    """测试 IsFogMaskEnabled 返回黑色遮罩状态。"""
    from jass_runner.natives.fog_natives import IsFogMaskEnabled, FogState

    state = FogState()
    native = IsFogMaskEnabled(state)

    # 默认启用
    result = native.execute(None)
    assert result is True

    # 禁用后查询
    state.mask_enabled = False
    result = native.execute(None)
    assert result is False


def test_is_fog_enabled_returns_state():
    """测试 IsFogEnabled 返回战争迷雾状态。"""
    from jass_runner.natives.fog_natives import IsFogEnabled, FogState

    state = FogState()
    native = IsFogEnabled(state)

    # 默认启用
    result = native.execute(None)
    assert result is True

    # 禁用后查询
    state.fog_enabled = False
    result = native.execute(None)
    assert result is False


def test_fog_natives_registered_in_factory():
    """测试 Fog native 函数在工厂中被注册。"""
    from jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    registry = factory.create_default_registry()

    # 验证所有函数都被注册
    assert registry.get("FogMaskEnable") is not None
    assert registry.get("FogEnable") is not None
    assert registry.get("IsFogMaskEnabled") is not None
    assert registry.get("IsFogEnabled") is not None
