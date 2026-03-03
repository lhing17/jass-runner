"""HandleManager特效生命周期管理测试。

此模块测试HandleManager中的特效创建和销毁功能。
"""

import logging

import pytest

from src.jass_runner.natives.manager import HandleManager
from src.jass_runner.natives.handle import Unit, Effect


class TestHandleManagerEffect:
    """测试HandleManager的特效管理功能。"""

    def test_create_effect(self, caplog):
        """测试在指定坐标创建特效。"""
        caplog.set_level(logging.INFO)
        manager = HandleManager()

        effect = manager.create_effect("Abilities\\Spells\\Human\\Heal\\HealTarget.mdl", 100.0, 200.0, 50.0)

        # 验证返回类型
        assert isinstance(effect, Effect)
        assert effect.is_alive()
        assert effect.type_name == "effect"
        assert effect.model_path == "Abilities\\Spells\\Human\\Heal\\HealTarget.mdl"

        # 验证日志输出
        assert "[特效] 在 (100.0, 200.0, 50.0) 创建特效:" in caplog.text
        assert "HealTarget.mdl" in caplog.text
        assert f"(ID: {effect.id})" in caplog.text

    def test_create_effect_target(self, caplog):
        """测试在目标上创建特效。"""
        caplog.set_level(logging.INFO)
        manager = HandleManager()

        # 先创建一个单位作为目标
        unit = manager.create_unit("hfoo", 0, 500.0, 600.0, 0.0)

        effect = manager.create_effect_target(
            "Abilities\\Weapons\\FireBall\\FireBall.mdl",
            unit,
            "hand"
        )

        # 验证返回类型
        assert isinstance(effect, Effect)
        assert effect.is_alive()
        assert effect.type_name == "effect"
        assert effect.model_path == "Abilities\\Weapons\\FireBall\\FireBall.mdl"
        assert effect.target == unit
        assert effect.attach_point == "hand"

        # 验证日志输出 - 新版日志格式
        assert "[特效] 在 [unit#" in caplog.text
        assert "] 的附着点 [hand] 创建特效:" in caplog.text
        assert "FireBall.mdl" in caplog.text
        assert f"(ID: {effect.id})" in caplog.text

    def test_destroy_effect(self, caplog):
        """测试销毁特效。"""
        caplog.set_level(logging.INFO)
        manager = HandleManager()

        # 先创建特效
        effect = manager.create_effect("Abilities\\Spells\\Orc\\HealingWave\\HealingWave.mdl", 0.0, 0.0, 0.0)
        effect_id = effect.id

        # 清空日志以便只验证销毁的日志
        caplog.clear()

        # 销毁特效
        result = manager.destroy_effect(effect)

        # 验证返回结果
        assert result is True
        assert not effect.is_alive()

        # 验证日志输出
        assert f"[特效] 销毁特效 (ID: {effect_id})" in caplog.text

    def test_destroy_effect_already_dead(self, caplog):
        """测试销毁已经死亡的特效返回False。"""
        caplog.set_level(logging.INFO)
        manager = HandleManager()

        # 创建并立即销毁特效
        effect = manager.create_effect("test.mdl", 0.0, 0.0, 0.0)
        manager.destroy_effect(effect)

        # 再次销毁应该返回False
        result = manager.destroy_effect(effect)
        assert result is False

    def test_get_effect(self):
        """测试通过ID获取特效对象。"""
        manager = HandleManager()

        effect = manager.create_effect("test.mdl", 100.0, 200.0, 0.0)
        effect_id = effect.id

        # 通过ID获取特效
        retrieved = manager.get_effect(effect_id)

        assert isinstance(retrieved, Effect)
        assert retrieved.id == effect_id
        assert retrieved == effect

    def test_get_effect_not_found(self):
        """测试获取不存在的特效返回None。"""
        manager = HandleManager()

        result = manager.get_effect("effect_9999")
        assert result is None

    def test_create_effect_with_item_target(self, caplog):
        """测试在物品上创建特效。"""
        caplog.set_level(logging.INFO)
        manager = HandleManager()

        # 先创建一个物品作为目标
        item = manager.create_item("ratf", 300.0, 400.0)

        effect = manager.create_effect_target(
            "effect.mdl",
            item,
            "origin"
        )

        assert isinstance(effect, Effect)
        assert effect.target == item
        assert effect.attach_point == "origin"

        # 验证日志输出包含物品类型
        assert "[item#" in caplog.text
