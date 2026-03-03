"""Effect Handle类测试。

此模块包含Effect Handle类的单元测试。
"""

import pytest
from src.jass_runner.natives.handle import Effect, Unit


class TestEffectHandle:
    """测试Effect Handle类的功能。"""

    def test_effect_creation(self):
        """测试Effect类创建。"""
        effect = Effect(1, "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl",
                        target=(100.0, 200.0, 0.0))

        assert effect.id == 1
        assert effect.type_name == "effect"
        assert effect.model_path == "Abilities\\Spells\\Human\\Thunderclap\\ThunderclapCaster.mdl"
        assert effect.target == (100.0, 200.0, 0.0)
        assert effect.attach_point is None
        assert effect.alive is True

    def test_effect_with_unit_target(self):
        """测试绑定到单位的特效。"""
        unit = Unit("unit_1", 'hfoo', 0, 0.0, 0.0, 0.0)
        effect = Effect(2, "Abilities\\Spells\\Orc\\Bloodlust\\BloodlustTarget.mdl",
                        target=unit, attach_point="hand")

        assert effect.target == unit
        assert effect.attach_point == "hand"
