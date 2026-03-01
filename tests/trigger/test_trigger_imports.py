"""测试trigger模块的导出功能。

此模块测试从trigger包导入所有公共API的功能。
"""


class TestTriggerImports:
    """测试trigger模块的所有导出项。"""

    def test_trigger_class_import(self):
        """测试Trigger类可以从trigger包导入。"""
        from jass_runner.trigger import Trigger

        assert Trigger is not None
        assert callable(Trigger)

    def test_trigger_manager_import(self):
        """测试TriggerManager类可以从trigger包导入。"""
        from jass_runner.trigger import TriggerManager

        assert TriggerManager is not None
        assert callable(TriggerManager)

    def test_player_unit_events_import(self):
        """测试所有玩家-单位事件常量可以导入。"""
        from jass_runner.trigger import (
            EVENT_PLAYER_UNIT_DEATH,
            EVENT_PLAYER_UNIT_ATTACKED,
            EVENT_PLAYER_UNIT_SPELL_EFFECT,
            EVENT_PLAYER_UNIT_DAMAGED,
            EVENT_PLAYER_UNIT_PICKUP_ITEM,
            EVENT_PLAYER_UNIT_DROP_ITEM,
            EVENT_PLAYER_UNIT_USE_ITEM,
            EVENT_PLAYER_UNIT_ISSUED_ORDER,
        )

        # 验证所有常量都是字符串类型
        assert isinstance(EVENT_PLAYER_UNIT_DEATH, str)
        assert isinstance(EVENT_PLAYER_UNIT_ATTACKED, str)
        assert isinstance(EVENT_PLAYER_UNIT_SPELL_EFFECT, str)
        assert isinstance(EVENT_PLAYER_UNIT_DAMAGED, str)
        assert isinstance(EVENT_PLAYER_UNIT_PICKUP_ITEM, str)
        assert isinstance(EVENT_PLAYER_UNIT_DROP_ITEM, str)
        assert isinstance(EVENT_PLAYER_UNIT_USE_ITEM, str)
        assert isinstance(EVENT_PLAYER_UNIT_ISSUED_ORDER, str)

    def test_unit_events_import(self):
        """测试所有通用单位事件常量可以导入。"""
        from jass_runner.trigger import (
            EVENT_UNIT_DEATH,
            EVENT_UNIT_DAMAGED,
        )

        assert isinstance(EVENT_UNIT_DEATH, str)
        assert isinstance(EVENT_UNIT_DAMAGED, str)

    def test_player_events_import(self):
        """测试所有玩家事件常量可以导入。"""
        from jass_runner.trigger import (
            EVENT_PLAYER_DEFEAT,
            EVENT_PLAYER_VICTORY,
            EVENT_PLAYER_LEAVE,
            EVENT_PLAYER_CHAT,
        )

        assert isinstance(EVENT_PLAYER_DEFEAT, str)
        assert isinstance(EVENT_PLAYER_VICTORY, str)
        assert isinstance(EVENT_PLAYER_LEAVE, str)
        assert isinstance(EVENT_PLAYER_CHAT, str)

    def test_game_events_import(self):
        """测试所有游戏事件常量可以导入。"""
        from jass_runner.trigger import EVENT_GAME_TIMER_EXPIRED

        assert isinstance(EVENT_GAME_TIMER_EXPIRED, str)

    def test_event_categories_import(self):
        """测试所有事件分类列表可以导入。"""
        from jass_runner.trigger import (
            PLAYER_UNIT_EVENTS,
            UNIT_EVENTS,
            PLAYER_EVENTS,
            GAME_EVENTS,
            ALL_EVENTS,
        )

        # 验证所有分类都是列表类型
        assert isinstance(PLAYER_UNIT_EVENTS, list)
        assert isinstance(UNIT_EVENTS, list)
        assert isinstance(PLAYER_EVENTS, list)
        assert isinstance(GAME_EVENTS, list)
        assert isinstance(ALL_EVENTS, list)

        # 验证分类非空
        assert len(PLAYER_UNIT_EVENTS) > 0
        assert len(UNIT_EVENTS) > 0
        assert len(PLAYER_EVENTS) > 0
        assert len(GAME_EVENTS) > 0
        assert len(ALL_EVENTS) > 0

    def test_all_exports_in_all_list(self):
        """测试所有导出项都在__all__列表中。"""
        import jass_runner.trigger as trigger_module

        expected_exports = [
            # 玩家-单位事件
            "EVENT_PLAYER_UNIT_DEATH",
            "EVENT_PLAYER_UNIT_ATTACKED",
            "EVENT_PLAYER_UNIT_SPELL_EFFECT",
            "EVENT_PLAYER_UNIT_DAMAGED",
            "EVENT_PLAYER_UNIT_PICKUP_ITEM",
            "EVENT_PLAYER_UNIT_DROP_ITEM",
            "EVENT_PLAYER_UNIT_USE_ITEM",
            "EVENT_PLAYER_UNIT_ISSUED_ORDER",
            # 通用单位事件
            "EVENT_UNIT_DEATH",
            "EVENT_UNIT_DAMAGED",
            # 玩家事件
            "EVENT_PLAYER_DEFEAT",
            "EVENT_PLAYER_VICTORY",
            "EVENT_PLAYER_LEAVE",
            "EVENT_PLAYER_CHAT",
            # 游戏事件
            "EVENT_GAME_TIMER_EXPIRED",
            # 事件分类列表
            "PLAYER_UNIT_EVENTS",
            "UNIT_EVENTS",
            "PLAYER_EVENTS",
            "GAME_EVENTS",
            "ALL_EVENTS",
            # 触发器类
            "Trigger",
            "TriggerManager",
        ]

        for export in expected_exports:
            assert export in trigger_module.__all__, f"{export} 不在__all__列表中"

    def test_import_star_works(self):
        """测试使用from trigger import *可以导入所有项。"""
        # 使用exec来测试import *
        import importlib

        module = importlib.import_module("jass_runner.trigger")
        all_names = module.__all__

        # 验证__all__中的所有名称都可以在模块中找到
        for name in all_names:
            assert hasattr(module, name), f"{name} 不在模块中"

    def test_event_values_are_correct(self):
        """测试事件常量的值正确。"""
        from jass_runner.trigger import (
            EVENT_PLAYER_UNIT_DEATH,
            EVENT_UNIT_DEATH,
            EVENT_PLAYER_DEFEAT,
            EVENT_GAME_TIMER_EXPIRED,
        )

        assert EVENT_PLAYER_UNIT_DEATH == "player_unit_death"
        assert EVENT_UNIT_DEATH == "unit_death"
        assert EVENT_PLAYER_DEFEAT == "player_defeat"
        assert EVENT_GAME_TIMER_EXPIRED == "game_timer_expired"
