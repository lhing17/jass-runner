"""测试触发器生命周期相关的原生函数。"""

import logging
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_state_context():
    """创建模拟的状态上下文。"""
    context = MagicMock()
    context.trigger_manager = MagicMock()
    return context


class TestCreateTrigger:
    """测试 CreateTrigger 原生函数。"""

    def test_create_trigger_returns_trigger_id(self, mock_state_context):
        """测试 CreateTrigger 返回触发器ID字符串。"""
        from jass_runner.natives.trigger_natives import CreateTrigger

        # 配置模拟的trigger_manager
        mock_state_context.trigger_manager.create_trigger.return_value = "trigger_0"

        native = CreateTrigger()
        assert native.name == "CreateTrigger"

        result = native.execute(mock_state_context)

        assert result == "trigger_0"
        mock_state_context.trigger_manager.create_trigger.assert_called_once()

    def test_create_trigger_without_trigger_manager_logs_error(self, mock_state_context, caplog):
        """测试没有trigger_manager时记录错误日志。"""
        from jass_runner.natives.trigger_natives import CreateTrigger

        # 移除trigger_manager
        delattr(mock_state_context, 'trigger_manager')

        native = CreateTrigger()

        with caplog.at_level(logging.ERROR):
            result = native.execute(mock_state_context)

        assert result is None
        assert "state_context" in caplog.text.lower() or "trigger_manager" in caplog.text.lower()


class TestDestroyTrigger:
    """测试 DestroyTrigger 原生函数。"""

    def test_destroy_trigger_returns_none(self, mock_state_context):
        """测试 DestroyTrigger 成功时返回None（nothing）。"""
        from jass_runner.natives.trigger_natives import DestroyTrigger

        mock_state_context.trigger_manager.destroy_trigger.return_value = True

        native = DestroyTrigger()
        assert native.name == "DestroyTrigger"

        result = native.execute(mock_state_context, "trigger_0")

        assert result is None
        mock_state_context.trigger_manager.destroy_trigger.assert_called_once_with("trigger_0")

    def test_destroy_trigger_invalid_trigger(self, mock_state_context):
        """测试销毁不存在的触发器。"""
        from jass_runner.natives.trigger_natives import DestroyTrigger

        mock_state_context.trigger_manager.destroy_trigger.return_value = False

        native = DestroyTrigger()
        result = native.execute(mock_state_context, "trigger_invalid")

        assert result is None


class TestEnableTrigger:
    """测试 EnableTrigger 原生函数。"""

    def test_enable_trigger_returns_none(self, mock_state_context):
        """测试 EnableTrigger 成功时返回None。"""
        from jass_runner.natives.trigger_natives import EnableTrigger

        mock_state_context.trigger_manager.enable_trigger.return_value = True

        native = EnableTrigger()
        assert native.name == "EnableTrigger"

        result = native.execute(mock_state_context, "trigger_0")

        assert result is None
        mock_state_context.trigger_manager.enable_trigger.assert_called_once_with("trigger_0")

    def test_enable_trigger_invalid_trigger(self, mock_state_context):
        """测试启用不存在的触发器。"""
        from jass_runner.natives.trigger_natives import EnableTrigger

        mock_state_context.trigger_manager.enable_trigger.return_value = False

        native = EnableTrigger()
        result = native.execute(mock_state_context, "trigger_invalid")

        assert result is None


class TestDisableTrigger:
    """测试 DisableTrigger 原生函数。"""

    def test_disable_trigger_returns_none(self, mock_state_context):
        """测试 DisableTrigger 成功时返回None。"""
        from jass_runner.natives.trigger_natives import DisableTrigger

        mock_state_context.trigger_manager.disable_trigger.return_value = True

        native = DisableTrigger()
        assert native.name == "DisableTrigger"

        result = native.execute(mock_state_context, "trigger_0")

        assert result is None
        mock_state_context.trigger_manager.disable_trigger.assert_called_once_with("trigger_0")

    def test_disable_trigger_invalid_trigger(self, mock_state_context):
        """测试禁用不存在的触发器。"""
        from jass_runner.natives.trigger_natives import DisableTrigger

        mock_state_context.trigger_manager.disable_trigger.return_value = False

        native = DisableTrigger()
        result = native.execute(mock_state_context, "trigger_invalid")

        assert result is None


class TestIsTriggerEnabled:
    """测试 IsTriggerEnabled 原生函数。"""

    def test_is_trigger_enabled_returns_true(self, mock_state_context):
        """测试 IsTriggerEnabled 返回True当触发器启用时。"""
        from jass_runner.natives.trigger_natives import IsTriggerEnabled

        mock_state_context.trigger_manager.is_trigger_enabled.return_value = True

        native = IsTriggerEnabled()
        assert native.name == "IsTriggerEnabled"

        result = native.execute(mock_state_context, "trigger_0")

        assert result is True
        mock_state_context.trigger_manager.is_trigger_enabled.assert_called_once_with("trigger_0")

    def test_is_trigger_enabled_returns_false(self, mock_state_context):
        """测试 IsTriggerEnabled 返回False当触发器禁用时。"""
        from jass_runner.natives.trigger_natives import IsTriggerEnabled

        mock_state_context.trigger_manager.is_trigger_enabled.return_value = False

        native = IsTriggerEnabled()
        result = native.execute(mock_state_context, "trigger_0")

        assert result is False

    def test_is_trigger_enabled_invalid_trigger(self, mock_state_context):
        """测试检查不存在的触发器返回False。"""
        from jass_runner.natives.trigger_natives import IsTriggerEnabled

        mock_state_context.trigger_manager.is_trigger_enabled.return_value = False

        native = IsTriggerEnabled()
        result = native.execute(mock_state_context, "trigger_invalid")

        assert result is False


class TestTriggerAddAction:
    """测试 TriggerAddAction 原生函数。"""

    def test_add_action_returns_handle(self, mock_state_context):
        """测试 TriggerAddAction 返回动作handle。"""
        from jass_runner.natives.trigger_natives import TriggerAddAction

        # 模拟触发器和trigger_manager
        mock_trigger = MagicMock()
        mock_trigger.add_action.return_value = "action_abc123"
        mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

        native = TriggerAddAction()
        assert native.name == "TriggerAddAction"

        action_func = lambda ctx: None
        result = native.execute(mock_state_context, "trigger_0", action_func)

        assert result == "action_abc123"
        mock_state_context.trigger_manager.get_trigger.assert_called_once_with("trigger_0")
        mock_trigger.add_action.assert_called_once_with(action_func)

    def test_add_action_invalid_trigger(self, mock_state_context):
        """测试对不存在的触发器添加动作返回None。"""
        from jass_runner.natives.trigger_natives import TriggerAddAction

        mock_state_context.trigger_manager.get_trigger.return_value = None

        native = TriggerAddAction()
        action_func = lambda ctx: None
        result = native.execute(mock_state_context, "trigger_invalid", action_func)

        assert result is None

    def test_add_action_without_trigger_manager(self, mock_state_context):
        """测试没有trigger_manager时添加动作返回None。"""
        from jass_runner.natives.trigger_natives import TriggerAddAction

        delattr(mock_state_context, 'trigger_manager')

        native = TriggerAddAction()
        action_func = lambda ctx: None
        result = native.execute(mock_state_context, "trigger_0", action_func)

        assert result is None


class TestTriggerRemoveAction:
    """测试 TriggerRemoveAction 原生函数。"""

    def test_remove_action_returns_true(self, mock_state_context):
        """测试 TriggerRemoveAction 成功时返回True。"""
        from jass_runner.natives.trigger_natives import TriggerRemoveAction

        mock_trigger = MagicMock()
        mock_trigger.remove_action.return_value = True
        mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

        native = TriggerRemoveAction()
        assert native.name == "TriggerRemoveAction"

        result = native.execute(mock_state_context, "trigger_0", "action_abc123")

        assert result is True
        mock_state_context.trigger_manager.get_trigger.assert_called_once_with("trigger_0")
        mock_trigger.remove_action.assert_called_once_with("action_abc123")

    def test_remove_action_invalid_action(self, mock_state_context):
        """测试移除不存在的动作返回False。"""
        from jass_runner.natives.trigger_natives import TriggerRemoveAction

        mock_trigger = MagicMock()
        mock_trigger.remove_action.return_value = False
        mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

        native = TriggerRemoveAction()
        result = native.execute(mock_state_context, "trigger_0", "action_invalid")

        assert result is False

    def test_remove_action_invalid_trigger(self, mock_state_context):
        """测试对不存在的触发器移除动作返回False。"""
        from jass_runner.natives.trigger_natives import TriggerRemoveAction

        mock_state_context.trigger_manager.get_trigger.return_value = None

        native = TriggerRemoveAction()
        result = native.execute(mock_state_context, "trigger_invalid", "action_abc123")

        assert result is False


class TestTriggerClearActions:
    """测试 TriggerClearActions 原生函数。"""

    def test_clear_actions_returns_none(self, mock_state_context):
        """测试 TriggerClearActions 成功时返回None。"""
        from jass_runner.natives.trigger_natives import TriggerClearActions

        mock_trigger = MagicMock()
        mock_state_context.trigger_manager.get_trigger.return_value = mock_trigger

        native = TriggerClearActions()
        assert native.name == "TriggerClearActions"

        result = native.execute(mock_state_context, "trigger_0")

        assert result is None
        mock_state_context.trigger_manager.get_trigger.assert_called_once_with("trigger_0")
        mock_trigger.clear_actions.assert_called_once()

    def test_clear_actions_invalid_trigger(self, mock_state_context):
        """测试清空不存在的触发器的动作返回None。"""
        from jass_runner.natives.trigger_natives import TriggerClearActions

        mock_state_context.trigger_manager.get_trigger.return_value = None

        native = TriggerClearActions()
        result = native.execute(mock_state_context, "trigger_invalid")

        assert result is None

    def test_clear_actions_without_trigger_manager(self, mock_state_context):
        """测试没有trigger_manager时清空动作返回None。"""
        from jass_runner.natives.trigger_natives import TriggerClearActions

        delattr(mock_state_context, 'trigger_manager')

        native = TriggerClearActions()
        result = native.execute(mock_state_context, "trigger_0")

        assert result is None
