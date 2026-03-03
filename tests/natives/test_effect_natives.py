"""特效 Native 函数单元测试。"""

import pytest

from jass_runner.natives.handle import Unit
from jass_runner.natives.effect_natives import (
    AddSpecialEffect,
    AddSpecialEffectTarget,
    DestroyEffect,
    SetSpecialEffectScale,
    SetSpecialEffectColor,
)
from jass_runner.natives.state import StateContext
from jass_runner.natives.handle import Effect


class TestAddSpecialEffect:
    """测试 AddSpecialEffect 函数。"""

    def test_add_special_effect(self):
        """测试在指定坐标创建特效。"""
        # 准备
        state_context = StateContext()
        native = AddSpecialEffect()

        # 执行
        effect = native.execute(
            state_context,
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0,
            200.0
        )

        # 验证
        assert isinstance(effect, Effect)
        assert effect.model_path == "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl"
        assert effect.target == (100.0, 200.0, 0.0)
        assert effect.alive is True


class TestAddSpecialEffectTarget:
    """测试 AddSpecialEffectTarget 函数。"""

    def test_add_special_effect_target_unit(self):
        """测试在单位附着点创建特效。"""
        # 准备
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        player = handle_manager.get_player(0)
        unit = handle_manager.create_unit(0, player, 0.0, 0.0, 0.0)
        native = AddSpecialEffectTarget()

        # 执行
        effect = native.execute(
            state_context,
            "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
            unit,
            "hand"
        )

        # 验证
        assert isinstance(effect, Effect)
        assert effect.model_path == "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl"
        assert effect.target == unit
        assert effect.attach_point == "hand"
        assert effect.alive is True


class TestDestroyEffect:
    """测试 DestroyEffect 函数。"""

    def test_destroy_effect_success(self):
        """测试成功销毁特效。"""
        # 准备
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        effect = handle_manager.create_effect(
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0,
            200.0,
            0.0
        )
        native = DestroyEffect()

        # 执行
        result = native.execute(state_context, effect)

        # 验证
        assert result is True
        assert effect.alive is False

    def test_destroy_already_destroyed_effect(self):
        """测试销毁已销毁的特效返回 False。"""
        # 准备
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        effect = handle_manager.create_effect(
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0,
            200.0,
            0.0
        )
        effect.destroy()
        native = DestroyEffect()

        # 执行
        result = native.execute(state_context, effect)

        # 验证
        assert result is False


class TestSetSpecialEffectScale:
    """测试 SetSpecialEffectScale 函数。"""

    def test_set_special_effect_scale(self):
        """测试设置特效缩放。"""
        # 准备
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        effect = handle_manager.create_effect(
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0,
            200.0,
            0.0
        )
        native = SetSpecialEffectScale()

        # 执行（应该不抛异常）
        result = native.execute(state_context, effect, 2.5)

        # 验证
        assert result is None


class TestSetSpecialEffectColor:
    """测试 SetSpecialEffectColor 函数。"""

    def test_set_special_effect_color(self):
        """测试设置特效颜色。"""
        # 准备
        state_context = StateContext()
        handle_manager = state_context.handle_manager
        effect = handle_manager.create_effect(
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0,
            200.0,
            0.0
        )
        native = SetSpecialEffectColor()

        # 执行（应该不抛异常）
        result = native.execute(state_context, effect, 255, 128, 64, 200)

        # 验证
        assert result is None
