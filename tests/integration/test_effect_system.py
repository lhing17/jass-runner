"""特效系统集成测试。

此模块包含特效系统的完整流程测试，验证特效创建、属性设置和销毁功能。
"""

import pytest
from src.jass_runner.natives.factory import NativeFactory
from src.jass_runner.natives.state import StateContext
from src.jass_runner.natives.manager import HandleManager


class TestEffectSystem:
    """测试特效系统完整流程。"""

    def test_create_and_destroy_effect(self):
        """测试创建并销毁特效的完整流程。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        # 创建特效
        add_effect = registry.get("AddSpecialEffect")
        effect = add_effect.execute(
            state_context,
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0, 200.0
        )

        assert effect is not None
        assert effect.alive is True

        # 设置属性
        set_scale = registry.get("SetSpecialEffectScale")
        set_scale.execute(state_context, effect, 1.5)

        set_color = registry.get("SetSpecialEffectColor")
        set_color.execute(state_context, effect, 255, 0, 0, 255)

        # 销毁特效
        destroy = registry.get("DestroyEffect")
        result = destroy.execute(state_context, effect)

        assert result is True
        assert effect.alive is False

    def test_effect_on_unit(self):
        """测试在单位上创建特效。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        # 创建单位
        unit = handle_manager.create_unit('hfoo', 0, 0.0, 0.0, 0.0)

        # 在单位上创建特效
        add_effect_target = registry.get("AddSpecialEffectTarget")
        effect = add_effect_target.execute(
            state_context,
            "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
            unit,
            "hand"
        )

        assert effect.target == unit
        assert effect.attach_point == "hand"

    def test_destroy_already_dead_effect(self):
        """测试销毁已死亡的特效返回False。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        # 创建特效
        add_effect = registry.get("AddSpecialEffect")
        effect = add_effect.execute(
            state_context,
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            0.0, 0.0
        )

        # 第一次销毁
        destroy = registry.get("DestroyEffect")
        result1 = destroy.execute(state_context, effect)
        assert result1 is True

        # 第二次销毁（已死亡）
        result2 = destroy.execute(state_context, effect)
        assert result2 is False

    def test_effect_factory_registration(self):
        """测试特效函数在工厂中正确注册。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()

        # 验证所有特效函数已注册
        assert registry.get("AddSpecialEffect") is not None
        assert registry.get("AddSpecialEffectTarget") is not None
        assert registry.get("DestroyEffect") is not None
        assert registry.get("SetSpecialEffectScale") is not None
        assert registry.get("SetSpecialEffectColor") is not None

    def test_effect_properties(self):
        """测试特效对象属性正确设置。"""
        state_context = StateContext()
        handle_manager = state_context.handle_manager

        # 创建坐标特效
        effect1 = handle_manager.create_effect(
            "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
            100.0, 200.0, 50.0
        )

        assert effect1.model_path == "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl"
        assert effect1.target == (100.0, 200.0, 50.0)
        assert effect1.attach_point is None
        assert effect1.type_name == "effect"

        # 创建目标特效
        unit = handle_manager.create_unit('hfoo', 0, 0.0, 0.0, 0.0)
        effect2 = handle_manager.create_effect_target(
            "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
            unit,
            "origin"
        )

        assert effect2.model_path == "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl"
        assert effect2.target == unit
        assert effect2.attach_point == "origin"
