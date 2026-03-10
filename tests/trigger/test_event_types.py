"""事件类型定义模块测试。

测试JASS触发器系统的事件类型常量定义。
"""

import pytest


class TestEventTypeConstants:
    """测试事件类型常量定义。"""

    def test_player_unit_events_exist(self):
        """测试玩家-单位事件常量存在且值为整数。"""
        from jass_runner.trigger.event_types import (
            EVENT_PLAYER_UNIT_DEATH,
            EVENT_PLAYER_UNIT_ATTACKED,
            EVENT_PLAYER_UNIT_SPELL_EFFECT,
            EVENT_PLAYER_UNIT_DAMAGED,
            EVENT_PLAYER_UNIT_PICKUP_ITEM,
            EVENT_PLAYER_UNIT_DROP_ITEM,
            EVENT_PLAYER_UNIT_USE_ITEM,
            EVENT_PLAYER_UNIT_ISSUED_ORDER,
        )

        # 验证所有常量都是整数类型
        assert isinstance(EVENT_PLAYER_UNIT_DEATH, int)
        assert isinstance(EVENT_PLAYER_UNIT_ATTACKED, int)
        assert isinstance(EVENT_PLAYER_UNIT_SPELL_EFFECT, int)
        assert isinstance(EVENT_PLAYER_UNIT_DAMAGED, int)
        assert isinstance(EVENT_PLAYER_UNIT_PICKUP_ITEM, int)
        assert isinstance(EVENT_PLAYER_UNIT_DROP_ITEM, int)
        assert isinstance(EVENT_PLAYER_UNIT_USE_ITEM, int)
        assert isinstance(EVENT_PLAYER_UNIT_ISSUED_ORDER, int)

        # 验证值符合预期 (与common.j保持一致)
        assert EVENT_PLAYER_UNIT_DEATH == 275
        assert EVENT_PLAYER_UNIT_ATTACKED == 276
        assert EVENT_PLAYER_UNIT_SPELL_EFFECT == 274
        assert EVENT_PLAYER_UNIT_DAMAGED == 277
        assert EVENT_PLAYER_UNIT_PICKUP_ITEM == 278
        assert EVENT_PLAYER_UNIT_DROP_ITEM == 279
        assert EVENT_PLAYER_UNIT_USE_ITEM == 280
        assert EVENT_PLAYER_UNIT_ISSUED_ORDER == 281

    def test_unit_events_exist(self):
        """测试通用单位事件常量存在且值为整数。"""
        from jass_runner.trigger.event_types import (
            EVENT_UNIT_DEATH,
            EVENT_UNIT_DAMAGED,
        )

        assert isinstance(EVENT_UNIT_DEATH, int)
        assert isinstance(EVENT_UNIT_DAMAGED, int)

        assert EVENT_UNIT_DEATH == 100
        assert EVENT_UNIT_DAMAGED == 101

    def test_player_events_exist(self):
        """测试玩家事件常量存在且值为整数。"""
        from jass_runner.trigger.event_types import (
            EVENT_PLAYER_DEFEAT,
            EVENT_PLAYER_VICTORY,
            EVENT_PLAYER_LEAVE,
            EVENT_PLAYER_CHAT,
        )

        assert isinstance(EVENT_PLAYER_DEFEAT, int)
        assert isinstance(EVENT_PLAYER_VICTORY, int)
        assert isinstance(EVENT_PLAYER_LEAVE, int)
        assert isinstance(EVENT_PLAYER_CHAT, int)

        assert EVENT_PLAYER_DEFEAT == 200
        assert EVENT_PLAYER_VICTORY == 201
        assert EVENT_PLAYER_LEAVE == 202
        assert EVENT_PLAYER_CHAT == 203

    def test_game_events_exist(self):
        """测试游戏事件常量存在且值为整数。"""
        from jass_runner.trigger.event_types import EVENT_GAME_TIMER_EXPIRED

        assert isinstance(EVENT_GAME_TIMER_EXPIRED, int)
        assert EVENT_GAME_TIMER_EXPIRED == 300

    def test_event_game_state_limit_exists(self):
        """测试EVENT_GAME_STATE_LIMIT事件常量存在且值正确。"""
        from jass_runner.trigger.event_types import EVENT_GAME_STATE_LIMIT

        assert isinstance(EVENT_GAME_STATE_LIMIT, int)
        assert EVENT_GAME_STATE_LIMIT == 301


class TestEventIdToNameMapping:
    """测试事件ID到名称的映射。"""

    def test_event_id_to_name_exists(self):
        """测试EVENT_ID_TO_NAME映射存在且包含所有事件。"""
        from jass_runner.trigger.event_types import (
            EVENT_ID_TO_NAME,
            EVENT_PLAYER_UNIT_DEATH,
            EVENT_PLAYER_UNIT_ATTACKED,
            EVENT_PLAYER_UNIT_SPELL_EFFECT,
            EVENT_PLAYER_UNIT_DAMAGED,
            EVENT_PLAYER_UNIT_PICKUP_ITEM,
            EVENT_PLAYER_UNIT_DROP_ITEM,
            EVENT_PLAYER_UNIT_USE_ITEM,
            EVENT_PLAYER_UNIT_ISSUED_ORDER,
            EVENT_UNIT_DEATH,
            EVENT_UNIT_DAMAGED,
            EVENT_PLAYER_DEFEAT,
            EVENT_PLAYER_VICTORY,
            EVENT_PLAYER_LEAVE,
            EVENT_PLAYER_CHAT,
            EVENT_GAME_TIMER_EXPIRED,
            EVENT_GAME_STATE_LIMIT,
        )

        # 验证映射包含所有16个事件
        assert len(EVENT_ID_TO_NAME) == 16

        # 验证玩家-单位事件映射
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_SPELL_EFFECT] == "player_unit_spell_effect"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_DEATH] == "player_unit_death"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_ATTACKED] == "player_unit_attacked"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_DAMAGED] == "player_unit_damaged"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_PICKUP_ITEM] == "player_unit_pickup_item"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_DROP_ITEM] == "player_unit_drop_item"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_USE_ITEM] == "player_unit_use_item"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_UNIT_ISSUED_ORDER] == "player_unit_issued_order"

        # 验证通用单位事件映射
        assert EVENT_ID_TO_NAME[EVENT_UNIT_DEATH] == "unit_death"
        assert EVENT_ID_TO_NAME[EVENT_UNIT_DAMAGED] == "unit_damaged"

        # 验证玩家事件映射
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_DEFEAT] == "player_defeat"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_VICTORY] == "player_victory"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_LEAVE] == "player_leave"
        assert EVENT_ID_TO_NAME[EVENT_PLAYER_CHAT] == "player_chat"

        # 验证游戏事件映射
        assert EVENT_ID_TO_NAME[EVENT_GAME_TIMER_EXPIRED] == "game_timer_expired"
        assert EVENT_ID_TO_NAME[EVENT_GAME_STATE_LIMIT] == "game_state_limit"


class TestEventCategoryLists:
    """测试事件分类列表。"""

    def test_player_unit_events_list(self):
        """测试PLAYER_UNIT_EVENTS列表包含所有玩家-单位事件。"""
        from jass_runner.trigger.event_types import (
            PLAYER_UNIT_EVENTS,
            EVENT_PLAYER_UNIT_DEATH,
            EVENT_PLAYER_UNIT_ATTACKED,
            EVENT_PLAYER_UNIT_SPELL_EFFECT,
            EVENT_PLAYER_UNIT_DAMAGED,
            EVENT_PLAYER_UNIT_PICKUP_ITEM,
            EVENT_PLAYER_UNIT_DROP_ITEM,
            EVENT_PLAYER_UNIT_USE_ITEM,
            EVENT_PLAYER_UNIT_ISSUED_ORDER,
        )

        assert len(PLAYER_UNIT_EVENTS) == 8
        assert EVENT_PLAYER_UNIT_DEATH in PLAYER_UNIT_EVENTS
        assert EVENT_PLAYER_UNIT_ATTACKED in PLAYER_UNIT_EVENTS
        assert EVENT_PLAYER_UNIT_SPELL_EFFECT in PLAYER_UNIT_EVENTS
        assert EVENT_PLAYER_UNIT_DAMAGED in PLAYER_UNIT_EVENTS
        assert EVENT_PLAYER_UNIT_PICKUP_ITEM in PLAYER_UNIT_EVENTS
        assert EVENT_PLAYER_UNIT_DROP_ITEM in PLAYER_UNIT_EVENTS
        assert EVENT_PLAYER_UNIT_USE_ITEM in PLAYER_UNIT_EVENTS
        assert EVENT_PLAYER_UNIT_ISSUED_ORDER in PLAYER_UNIT_EVENTS

    def test_unit_events_list(self):
        """测试UNIT_EVENTS列表包含所有单位事件。"""
        from jass_runner.trigger.event_types import (
            UNIT_EVENTS,
            EVENT_UNIT_DEATH,
            EVENT_UNIT_DAMAGED,
        )

        assert len(UNIT_EVENTS) == 2
        assert EVENT_UNIT_DEATH in UNIT_EVENTS
        assert EVENT_UNIT_DAMAGED in UNIT_EVENTS

    def test_player_events_list(self):
        """测试PLAYER_EVENTS列表包含所有玩家事件。"""
        from jass_runner.trigger.event_types import (
            PLAYER_EVENTS,
            EVENT_PLAYER_DEFEAT,
            EVENT_PLAYER_VICTORY,
            EVENT_PLAYER_LEAVE,
            EVENT_PLAYER_CHAT,
        )

        assert len(PLAYER_EVENTS) == 4
        assert EVENT_PLAYER_DEFEAT in PLAYER_EVENTS
        assert EVENT_PLAYER_VICTORY in PLAYER_EVENTS
        assert EVENT_PLAYER_LEAVE in PLAYER_EVENTS
        assert EVENT_PLAYER_CHAT in PLAYER_EVENTS

    def test_game_events_list(self):
        """测试GAME_EVENTS列表包含所有游戏事件。"""
        from jass_runner.trigger.event_types import (
            GAME_EVENTS,
            EVENT_GAME_TIMER_EXPIRED,
            EVENT_GAME_STATE_LIMIT,
        )

        assert len(GAME_EVENTS) == 2
        assert EVENT_GAME_TIMER_EXPIRED in GAME_EVENTS
        assert EVENT_GAME_STATE_LIMIT in GAME_EVENTS

    def test_all_events_includes_game_state_limit(self):
        """测试ALL_EVENTS列表包含EVENT_GAME_STATE_LIMIT事件。"""
        from jass_runner.trigger.event_types import (
            ALL_EVENTS,
            EVENT_GAME_STATE_LIMIT,
            PLAYER_UNIT_EVENTS,
            UNIT_EVENTS,
            PLAYER_EVENTS,
            GAME_EVENTS,
        )

        # 验证总数正确 (8 + 2 + 4 + 2 = 16)
        assert len(ALL_EVENTS) == 16

        # 验证EVENT_GAME_STATE_LIMIT在ALL_EVENTS中
        assert EVENT_GAME_STATE_LIMIT in ALL_EVENTS

        # 验证所有分类都在ALL_EVENTS中
        for event in PLAYER_UNIT_EVENTS:
            assert event in ALL_EVENTS
        for event in UNIT_EVENTS:
            assert event in ALL_EVENTS
        for event in PLAYER_EVENTS:
            assert event in ALL_EVENTS
        for event in GAME_EVENTS:
            assert event in ALL_EVENTS

    def test_all_events_list(self):
        """测试ALL_EVENTS列表包含所有事件。"""
        from jass_runner.trigger.event_types import (
            ALL_EVENTS,
            PLAYER_UNIT_EVENTS,
            UNIT_EVENTS,
            PLAYER_EVENTS,
            GAME_EVENTS,
        )

        # 验证总数正确 (8 + 2 + 4 + 2 = 16)
        assert len(ALL_EVENTS) == 16

        # 验证所有分类都在ALL_EVENTS中
        for event in PLAYER_UNIT_EVENTS:
            assert event in ALL_EVENTS
        for event in UNIT_EVENTS:
            assert event in ALL_EVENTS
        for event in PLAYER_EVENTS:
            assert event in ALL_EVENTS
        for event in GAME_EVENTS:
            assert event in ALL_EVENTS
