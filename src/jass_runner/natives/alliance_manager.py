"""联盟管理器实现。

此模块提供 AllianceManager 类，用于集中管理玩家之间的联盟关系。
"""

from typing import Dict, Set, Tuple


class AllianceManager:
    """管理玩家之间的联盟关系。

    使用字典存储联盟关系，键为 (source_id, other_id) 元组，
    值为该玩家对已启用的联盟类型集合。
    """

    def __init__(self):
        """初始化联盟管理器。"""
        # (source_player_id, other_player_id) -> Set[alliance_type]
        self._alliances: Dict[Tuple[int, int], Set[int]] = {}

    def set_alliance(self, source_id: int, other_id: int,
                     alliance_type: int, value: bool) -> None:
        """设置玩家之间的联盟关系。

        参数：
            source_id: 源玩家ID
            other_id: 目标玩家ID
            alliance_type: 联盟类型（0-9）
            value: True 启用，False 禁用
        """
        key = (source_id, other_id)

        if key not in self._alliances:
            self._alliances[key] = set()

        if value:
            self._alliances[key].add(alliance_type)
        else:
            self._alliances[key].discard(alliance_type)

            # 如果集合为空，删除该键
            if not self._alliances[key]:
                del self._alliances[key]

    def get_alliance(self, source_id: int, other_id: int,
                     alliance_type: int) -> bool:
        """获取玩家之间的特定联盟关系状态。

        参数：
            source_id: 源玩家ID
            other_id: 目标玩家ID
            alliance_type: 联盟类型

        返回：
            该联盟类型是否启用
        """
        key = (source_id, other_id)

        if key not in self._alliances:
            return False

        return alliance_type in self._alliances[key]

    def get_all_alliances(self, source_id: int, other_id: int) -> Set[int]:
        """获取两个玩家之间所有已启用的联盟类型。

        参数：
            source_id: 源玩家ID
            other_id: 目标玩家ID

        返回：
            已启用的联盟类型集合
        """
        key = (source_id, other_id)
        return self._alliances.get(key, set()).copy()
