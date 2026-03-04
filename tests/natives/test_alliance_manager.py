"""AllianceManager 测试。"""

from src.jass_runner.natives.alliance_manager import AllianceManager
from src.jass_runner.natives.alliance import (
    ALLIANCE_PASSIVE,
    ALLIANCE_SHARED_VISION,
)


class TestAllianceManager:
    """测试 AllianceManager 的功能。"""

    def test_set_and_get_alliance(self):
        """测试设置和获取联盟关系。"""
        manager = AllianceManager()

        # 初始状态应为 False
        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is False

        # 设置联盟
        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)
        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is True

        # 取消联盟
        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, False)
        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is False

    def test_multiple_alliance_types(self):
        """测试同一对玩家可以设置多个联盟类型。"""
        manager = AllianceManager()

        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)
        manager.set_alliance(0, 1, ALLIANCE_SHARED_VISION, True)

        assert manager.get_alliance(0, 1, ALLIANCE_PASSIVE) is True
        assert manager.get_alliance(0, 1, ALLIANCE_SHARED_VISION) is True

    def test_alliance_independence(self):
        """测试不同玩家对之间的联盟关系相互独立。"""
        manager = AllianceManager()

        # 设置玩家0对玩家1的联盟
        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)

        # 玩家0对玩家2应该没有联盟
        assert manager.get_alliance(0, 2, ALLIANCE_PASSIVE) is False

        # 玩家1对玩家0应该没有联盟（单向）
        assert manager.get_alliance(1, 0, ALLIANCE_PASSIVE) is False

    def test_get_all_alliances(self):
        """测试获取所有联盟类型。"""
        manager = AllianceManager()

        manager.set_alliance(0, 1, ALLIANCE_PASSIVE, True)
        manager.set_alliance(0, 1, ALLIANCE_SHARED_VISION, True)

        alliances = manager.get_all_alliances(0, 1)
        assert ALLIANCE_PASSIVE in alliances
        assert ALLIANCE_SHARED_VISION in alliances
