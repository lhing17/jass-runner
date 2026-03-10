"""事件类型 handle 类测试。

此模块包含 PlayerUnitEvent、PlayerEvent、GameEvent、UnitEvent 四个类的单元测试。
"""

import pytest
from jass_runner.natives.event_handles import PlayerUnitEvent, PlayerEvent, GameEvent, UnitEvent


class TestPlayerUnitEvent:
    """测试 PlayerUnitEvent 类。"""

    def test_creation(self):
        """测试创建 PlayerUnitEvent 对象。"""
        event = PlayerUnitEvent("playerunitevent_1", 274)
        assert event.id == "playerunitevent_1"
        assert event.type_name == "playerunitevent"
        assert event.event_id == 274
        assert event.is_alive()

    def test_is_alive(self):
        """测试 is_alive() 方法。"""
        event = PlayerUnitEvent("playerunitevent_2", 275)
        assert event.is_alive() is True

        event.destroy()
        assert event.is_alive() is False

    def test_different_event_ids(self):
        """测试不同 event_id 值。"""
        event1 = PlayerUnitEvent("playerunitevent_3", 0)
        event2 = PlayerUnitEvent("playerunitevent_4", 999)
        event3 = PlayerUnitEvent("playerunitevent_5", -1)

        assert event1.event_id == 0
        assert event2.event_id == 999
        assert event3.event_id == -1


class TestPlayerEvent:
    """测试 PlayerEvent 类。"""

    def test_creation(self):
        """测试创建 PlayerEvent 对象。"""
        event = PlayerEvent("playerevent_1", 100)
        assert event.id == "playerevent_1"
        assert event.type_name == "playerevent"
        assert event.event_id == 100
        assert event.is_alive()

    def test_is_alive(self):
        """测试 is_alive() 方法。"""
        event = PlayerEvent("playerevent_2", 101)
        assert event.is_alive() is True

        event.destroy()
        assert event.is_alive() is False

    def test_different_event_ids(self):
        """测试不同 event_id 值。"""
        event1 = PlayerEvent("playerevent_3", 0)
        event2 = PlayerEvent("playerevent_4", 255)
        event3 = PlayerEvent("playerevent_5", -100)

        assert event1.event_id == 0
        assert event2.event_id == 255
        assert event3.event_id == -100


class TestGameEvent:
    """测试 GameEvent 类。"""

    def test_creation(self):
        """测试创建 GameEvent 对象。"""
        event = GameEvent("gameevent_1", 10)
        assert event.id == "gameevent_1"
        assert event.type_name == "gameevent"
        assert event.event_id == 10
        assert event.is_alive()

    def test_is_alive(self):
        """测试 is_alive() 方法。"""
        event = GameEvent("gameevent_2", 11)
        assert event.is_alive() is True

        event.destroy()
        assert event.is_alive() is False

    def test_different_event_ids(self):
        """测试不同 event_id 值。"""
        event1 = GameEvent("gameevent_3", 0)
        event2 = GameEvent("gameevent_4", 5)
        event3 = GameEvent("gameevent_5", 1000)

        assert event1.event_id == 0
        assert event2.event_id == 5
        assert event3.event_id == 1000


class TestUnitEvent:
    """测试 UnitEvent 类。"""

    def test_creation(self):
        """测试创建 UnitEvent 对象。"""
        event = UnitEvent("unitevent_1", 50)
        assert event.id == "unitevent_1"
        assert event.type_name == "unitevent"
        assert event.event_id == 50
        assert event.is_alive()

    def test_is_alive(self):
        """测试 is_alive() 方法。"""
        event = UnitEvent("unitevent_2", 51)
        assert event.is_alive() is True

        event.destroy()
        assert event.is_alive() is False

    def test_different_event_ids(self):
        """测试不同 event_id 值。"""
        event1 = UnitEvent("unitevent_3", 0)
        event2 = UnitEvent("unitevent_4", 123)
        event3 = UnitEvent("unitevent_5", -50)

        assert event1.event_id == 0
        assert event2.event_id == 123
        assert event3.event_id == -50


class TestEventHandleInheritance:
    """测试事件 handle 类的继承关系。"""

    def test_all_events_are_handles(self):
        """测试所有事件类都继承自 Handle。"""
        from jass_runner.natives.handle_base import Handle

        player_unit_event = PlayerUnitEvent("pue_1", 1)
        player_event = PlayerEvent("pe_1", 2)
        game_event = GameEvent("ge_1", 3)
        unit_event = UnitEvent("ue_1", 4)

        assert isinstance(player_unit_event, Handle)
        assert isinstance(player_event, Handle)
        assert isinstance(game_event, Handle)
        assert isinstance(unit_event, Handle)
