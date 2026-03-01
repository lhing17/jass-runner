"""TriggerManager类测试模块。

测试JASS触发器系统中TriggerManager类的功能，
包括触发器生命周期管理和事件分发机制。
"""

import pytest
from unittest.mock import Mock, patch


class TestTriggerManagerCreation:
    """测试TriggerManager类的创建和基本属性。"""

    def test_trigger_manager_creation(self):
        """测试TriggerManager创建时初始化属性。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        assert manager._triggers == {}
        assert manager._event_index == {}
        assert manager._global_enabled is True
        assert manager._next_id == 0

    def test_trigger_manager_global_enabled_default(self):
        """测试TriggerManager全局启用状态默认为True。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        assert manager._global_enabled is True


class TestTriggerIdGeneration:
    """测试触发器ID生成功能。"""

    def test_generate_trigger_id_format(self):
        """测试生成的trigger_id格式正确。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager._generate_trigger_id()

        assert trigger_id.startswith("trigger_")
        # 格式为 trigger_ + 数字
        parts = trigger_id.split("_")
        assert len(parts) == 2
        assert parts[1].isdigit()

    def test_generate_trigger_id_incremental(self):
        """测试生成的trigger_id自增。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        id1 = manager._generate_trigger_id()
        id2 = manager._generate_trigger_id()
        id3 = manager._generate_trigger_id()

        # ID应该按顺序递增
        num1 = int(id1.split("_")[1])
        num2 = int(id2.split("_")[1])
        num3 = int(id3.split("_")[1])

        assert num2 == num1 + 1
        assert num3 == num2 + 1


class TestTriggerLifecycle:
    """测试触发器生命周期管理。"""

    def test_create_trigger_returns_id(self):
        """测试创建触发器返回唯一ID。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        assert trigger_id.startswith("trigger_")
        assert trigger_id in manager._triggers

    def test_create_trigger_multiple(self):
        """测试创建多个触发器返回不同ID。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        id1 = manager.create_trigger()
        id2 = manager.create_trigger()

        assert id1 != id2
        assert len(manager._triggers) == 2

    def test_destroy_trigger_success(self):
        """测试销毁存在的触发器返回True。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        result = manager.destroy_trigger(trigger_id)

        assert result is True
        assert trigger_id not in manager._triggers

    def test_destroy_trigger_not_found(self):
        """测试销毁不存在的触发器返回False。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        result = manager.destroy_trigger("trigger_nonexistent")

        assert result is False

    def test_get_trigger_existing(self):
        """测试获取存在的触发器。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        trigger = manager.get_trigger(trigger_id)

        assert trigger is not None
        assert trigger.trigger_id == trigger_id

    def test_get_trigger_not_found(self):
        """测试获取不存在的触发器返回None。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        trigger = manager.get_trigger("trigger_nonexistent")

        assert trigger is None


class TestTriggerEnableDisable:
    """测试触发器启用/禁用功能。"""

    def test_enable_trigger_success(self):
        """测试启用存在的触发器返回True。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        # 先禁用
        manager.disable_trigger(trigger_id)
        # 再启用
        result = manager.enable_trigger(trigger_id)

        assert result is True
        trigger = manager.get_trigger(trigger_id)
        assert trigger.enabled is True

    def test_enable_trigger_not_found(self):
        """测试启用不存在的触发器返回False。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        result = manager.enable_trigger("trigger_nonexistent")

        assert result is False

    def test_disable_trigger_success(self):
        """测试禁用存在的触发器返回True。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        result = manager.disable_trigger(trigger_id)

        assert result is True
        trigger = manager.get_trigger(trigger_id)
        assert trigger.enabled is False

    def test_disable_trigger_not_found(self):
        """测试禁用不存在的触发器返回False。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        result = manager.disable_trigger("trigger_nonexistent")

        assert result is False

    def test_is_trigger_enabled_true(self):
        """测试检查触发器启用状态返回True。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        result = manager.is_trigger_enabled(trigger_id)

        assert result is True

    def test_is_trigger_enabled_false(self):
        """测试检查禁用状态的触发器返回False。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.disable_trigger(trigger_id)

        result = manager.is_trigger_enabled(trigger_id)

        assert result is False

    def test_is_trigger_enabled_not_found(self):
        """测试检查不存在的触发器返回False。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        result = manager.is_trigger_enabled("trigger_nonexistent")

        assert result is False


class TestEventRegistration:
    """测试事件注册功能。"""

    def test_register_event_success(self):
        """测试为触发器注册事件返回event_handle。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        event_handle = manager.register_event(
            trigger_id, "unit_death", {"unit_id": 123}
        )

        assert event_handle is not None
        assert event_handle.startswith("event_")
        assert "unit_death" in manager._event_index
        assert trigger_id in manager._event_index["unit_death"]

    def test_register_event_trigger_not_found(self):
        """测试为不存在的触发器注册事件返回None。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        event_handle = manager.register_event(
            "trigger_nonexistent", "unit_death", None
        )

        assert event_handle is None

    def test_register_event_multiple_triggers(self):
        """测试多个触发器注册相同事件。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id1 = manager.create_trigger()
        trigger_id2 = manager.create_trigger()

        manager.register_event(trigger_id1, "unit_death", None)
        manager.register_event(trigger_id2, "unit_death", None)

        assert len(manager._event_index["unit_death"]) == 2
        assert trigger_id1 in manager._event_index["unit_death"]
        assert trigger_id2 in manager._event_index["unit_death"]

    def test_register_event_multiple_event_types(self):
        """测试一个触发器注册多个不同类型的事件。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()

        manager.register_event(trigger_id, "unit_death", None)
        manager.register_event(trigger_id, "unit_damaged", None)

        assert "unit_death" in manager._event_index
        assert "unit_damaged" in manager._event_index
        assert trigger_id in manager._event_index["unit_death"]
        assert trigger_id in manager._event_index["unit_damaged"]

    def test_clear_trigger_events_success(self):
        """测试清空触发器的事件成功。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.register_event(trigger_id, "unit_death", None)
        manager.register_event(trigger_id, "unit_damaged", None)

        result = manager.clear_trigger_events(trigger_id)

        assert result is True
        trigger = manager.get_trigger(trigger_id)
        assert len(trigger.events) == 0

    def test_clear_trigger_events_removes_from_index(self):
        """测试清空事件后从事件索引中移除。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.register_event(trigger_id, "unit_death", None)

        manager.clear_trigger_events(trigger_id)

        assert trigger_id not in manager._event_index.get("unit_death", [])

    def test_clear_trigger_events_not_found(self):
        """测试清空不存在触发器的事件返回False。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        result = manager.clear_trigger_events("trigger_nonexistent")

        assert result is False

    def test_destroy_trigger_removes_from_event_index(self):
        """测试销毁触发器时从事件索引中移除。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.register_event(trigger_id, "unit_death", None)

        manager.destroy_trigger(trigger_id)

        assert trigger_id not in manager._event_index.get("unit_death", [])


class TestEventDispatch:
    """测试事件分发功能。"""

    def test_fire_event_no_listeners(self):
        """测试没有监听器时fire_event不报错。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        # 应该不抛出异常
        manager.fire_event("unit_death", {"unit_id": 123})

    def test_fire_event_disabled_trigger_skipped(self):
        """测试禁用的触发器不会收到事件。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.register_event(trigger_id, "unit_death", None)
        manager.disable_trigger(trigger_id)

        mock_trigger = Mock()
        mock_trigger.enabled = False
        manager._triggers[trigger_id] = mock_trigger

        manager.fire_event("unit_death", {"unit_id": 123})

        mock_trigger.evaluate_conditions.assert_not_called()
        mock_trigger.execute_actions.assert_not_called()

    def test_fire_event_condition_fails(self):
        """测试条件失败时不执行动作。"""
        from jass_runner.trigger.manager import TriggerManager
        from jass_runner.trigger.trigger import Trigger

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.register_event(trigger_id, "unit_death", None)

        # 使用真实Trigger对象，但mock条件返回False
        trigger = manager.get_trigger(trigger_id)
        condition_mock = Mock(return_value=False)
        trigger.add_condition(condition_mock)
        action_mock = Mock()
        trigger.add_action(action_mock)

        manager.fire_event("unit_death", {"unit_id": 123})

        condition_mock.assert_called_once()
        action_mock.assert_not_called()

    def test_fire_event_condition_passes(self):
        """测试条件通过时执行动作。"""
        from jass_runner.trigger.manager import TriggerManager
        from jass_runner.trigger.trigger import Trigger

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.register_event(trigger_id, "unit_death", None)

        trigger = manager.get_trigger(trigger_id)
        condition_mock = Mock(return_value=True)
        trigger.add_condition(condition_mock)
        action_mock = Mock()
        trigger.add_action(action_mock)

        manager.fire_event("unit_death", {"unit_id": 123})

        condition_mock.assert_called_once()
        action_mock.assert_called_once()

    def test_fire_event_passes_context(self):
        """测试事件触发时传递正确的状态上下文。"""
        from jass_runner.trigger.manager import TriggerManager
        from jass_runner.trigger.trigger import Trigger

        manager = TriggerManager()
        trigger_id = manager.create_trigger()
        manager.register_event(trigger_id, "unit_death", None)

        trigger = manager.get_trigger(trigger_id)
        condition_mock = Mock(return_value=True)
        trigger.add_condition(condition_mock)
        action_mock = Mock()
        trigger.add_action(action_mock)

        event_data = {"unit_id": 123, "player_id": 1}
        manager.fire_event("unit_death", event_data)

        # 验证传递的state_context包含event_data
        call_args = condition_mock.call_args[0][0]
        assert call_args["event_data"]["unit_id"] == 123

    def test_fire_event_multiple_triggers(self):
        """测试事件触发多个触发器。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()
        trigger_id1 = manager.create_trigger()
        trigger_id2 = manager.create_trigger()
        manager.register_event(trigger_id1, "unit_death", None)
        manager.register_event(trigger_id2, "unit_death", None)

        mock_trigger1 = Mock()
        mock_trigger1.enabled = True
        mock_trigger1.evaluate_conditions.return_value = True

        mock_trigger2 = Mock()
        mock_trigger2.enabled = True
        mock_trigger2.evaluate_conditions.return_value = True

        manager._triggers[trigger_id1] = mock_trigger1
        manager._triggers[trigger_id2] = mock_trigger2

        manager.fire_event("unit_death", {"unit_id": 123})

        mock_trigger1.evaluate_conditions.assert_called_once()
        mock_trigger1.execute_actions.assert_called_once()
        mock_trigger2.evaluate_conditions.assert_called_once()
        mock_trigger2.execute_actions.assert_called_once()

    def test_fire_event_unknown_event_type(self):
        """测试触发未注册的事件类型不报错。"""
        from jass_runner.trigger.manager import TriggerManager

        manager = TriggerManager()

        # 应该不抛出异常
        manager.fire_event("unknown_event", {"data": "test"})

