"""事件类型转换 native 函数测试。

此模块包含 ConvertPlayerUnitEvent、ConvertPlayerEvent、ConvertGameEvent、ConvertUnitEvent
四个 native 函数的单元测试。
"""

import pytest
from jass_runner.natives.event_natives import (
    ConvertPlayerUnitEvent,
    ConvertPlayerEvent,
    ConvertGameEvent,
    ConvertUnitEvent
)
from jass_runner.natives.event_handles import (
    PlayerUnitEvent,
    PlayerEvent,
    GameEvent,
    UnitEvent
)
from jass_runner.natives.state import StateContext


@pytest.fixture
def state_context():
    """提供 StateContext fixture。"""
    return StateContext()


class TestConvertPlayerUnitEvent:
    """测试 ConvertPlayerUnitEvent native 函数。"""

    def test_creation(self, state_context):
        """测试创建 PlayerUnitEvent 对象。"""
        native = ConvertPlayerUnitEvent()
        event = native.execute(state_context, 274)

        assert isinstance(event, PlayerUnitEvent)
        assert event.event_id == 274
        assert event.type_name == "playerunitevent"
        assert event.is_alive()

    def test_different_event_ids(self, state_context):
        """测试不同的 event_id 值。"""
        native = ConvertPlayerUnitEvent()

        event1 = native.execute(state_context, 0)
        event2 = native.execute(state_context, 100)
        event3 = native.execute(state_context, 999)

        assert event1.event_id == 0
        assert event2.event_id == 100
        assert event3.event_id == 999

    def test_return_type(self, state_context):
        """测试返回类型正确。"""
        native = ConvertPlayerUnitEvent()
        event = native.execute(state_context, 274)

        assert type(event) is PlayerUnitEvent
        assert hasattr(event, 'id')
        assert hasattr(event, 'type_name')
        assert hasattr(event, 'event_id')
        assert hasattr(event, 'is_alive')

    def test_name_property(self):
        """测试 name 属性。"""
        native = ConvertPlayerUnitEvent()
        assert native.name == "ConvertPlayerUnitEvent"


class TestConvertPlayerEvent:
    """测试 ConvertPlayerEvent native 函数。"""

    def test_creation(self, state_context):
        """测试创建 PlayerEvent 对象。"""
        native = ConvertPlayerEvent()
        event = native.execute(state_context, 100)

        assert isinstance(event, PlayerEvent)
        assert event.event_id == 100
        assert event.type_name == "playerevent"
        assert event.is_alive()

    def test_different_event_ids(self, state_context):
        """测试不同的 event_id 值。"""
        native = ConvertPlayerEvent()

        event1 = native.execute(state_context, 0)
        event2 = native.execute(state_context, 50)
        event3 = native.execute(state_context, 255)

        assert event1.event_id == 0
        assert event2.event_id == 50
        assert event3.event_id == 255

    def test_return_type(self, state_context):
        """测试返回类型正确。"""
        native = ConvertPlayerEvent()
        event = native.execute(state_context, 100)

        assert type(event) is PlayerEvent
        assert hasattr(event, 'id')
        assert hasattr(event, 'type_name')
        assert hasattr(event, 'event_id')
        assert hasattr(event, 'is_alive')

    def test_name_property(self):
        """测试 name 属性。"""
        native = ConvertPlayerEvent()
        assert native.name == "ConvertPlayerEvent"


class TestConvertGameEvent:
    """测试 ConvertGameEvent native 函数。"""

    def test_creation(self, state_context):
        """测试创建 GameEvent 对象。"""
        native = ConvertGameEvent()
        event = native.execute(state_context, 10)

        assert isinstance(event, GameEvent)
        assert event.event_id == 10
        assert event.type_name == "gameevent"
        assert event.is_alive()

    def test_different_event_ids(self, state_context):
        """测试不同的 event_id 值。"""
        native = ConvertGameEvent()

        event1 = native.execute(state_context, 0)
        event2 = native.execute(state_context, 5)
        event3 = native.execute(state_context, 100)

        assert event1.event_id == 0
        assert event2.event_id == 5
        assert event3.event_id == 100

    def test_return_type(self, state_context):
        """测试返回类型正确。"""
        native = ConvertGameEvent()
        event = native.execute(state_context, 10)

        assert type(event) is GameEvent
        assert hasattr(event, 'id')
        assert hasattr(event, 'type_name')
        assert hasattr(event, 'event_id')
        assert hasattr(event, 'is_alive')

    def test_name_property(self):
        """测试 name 属性。"""
        native = ConvertGameEvent()
        assert native.name == "ConvertGameEvent"


class TestConvertUnitEvent:
    """测试 ConvertUnitEvent native 函数。"""

    def test_creation(self, state_context):
        """测试创建 UnitEvent 对象。"""
        native = ConvertUnitEvent()
        event = native.execute(state_context, 50)

        assert isinstance(event, UnitEvent)
        assert event.event_id == 50
        assert event.type_name == "unitevent"
        assert event.is_alive()

    def test_different_event_ids(self, state_context):
        """测试不同的 event_id 值。"""
        native = ConvertUnitEvent()

        event1 = native.execute(state_context, 0)
        event2 = native.execute(state_context, 25)
        event3 = native.execute(state_context, 200)

        assert event1.event_id == 0
        assert event2.event_id == 25
        assert event3.event_id == 200

    def test_return_type(self, state_context):
        """测试返回类型正确。"""
        native = ConvertUnitEvent()
        event = native.execute(state_context, 50)

        assert type(event) is UnitEvent
        assert hasattr(event, 'id')
        assert hasattr(event, 'type_name')
        assert hasattr(event, 'event_id')
        assert hasattr(event, 'is_alive')

    def test_name_property(self):
        """测试 name 属性。"""
        native = ConvertUnitEvent()
        assert native.name == "ConvertUnitEvent"


class TestEventNativesIntegration:
    """测试事件 native 函数的集成行为。"""

    def test_events_registered_in_handle_manager(self, state_context):
        """测试创建的事件被注册到 handle manager 中。"""
        native_pue = ConvertPlayerUnitEvent()
        native_pe = ConvertPlayerEvent()
        native_ge = ConvertGameEvent()
        native_ue = ConvertUnitEvent()

        event_pue = native_pue.execute(state_context, 1)
        event_pe = native_pe.execute(state_context, 2)
        event_ge = native_ge.execute(state_context, 3)
        event_ue = native_ue.execute(state_context, 4)

        # 验证可以通过 handle manager 获取到这些事件
        assert state_context.handle_manager.get_playerunit_event(event_pue.id) is not None
        assert state_context.handle_manager.get_playerevent(event_pe.id) is not None
        assert state_context.handle_manager.get_gameevent(event_ge.id) is not None
        assert state_context.handle_manager.get_unitevent(event_ue.id) is not None

    def test_multiple_events_have_unique_ids(self, state_context):
        """测试多次创建的事件具有唯一的 ID。"""
        native = ConvertPlayerUnitEvent()

        event1 = native.execute(state_context, 100)
        event2 = native.execute(state_context, 100)
        event3 = native.execute(state_context, 100)

        # 相同 event_id 但不同 handle id
        assert event1.id != event2.id
        assert event2.id != event3.id
        assert event1.event_id == event2.event_id == event3.event_id
