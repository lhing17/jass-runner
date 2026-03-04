"""JASS Force玩家组（队伍）类。

此模块包含JASS玩家组handle的实现。
"""

from typing import Set

from .handle_base import Handle


class Force(Handle):
    """玩家组（队伍）句柄。

    用于管理一组玩家，支持添加、移除玩家等操作。

    属性：
        _players: 玩家ID集合
    """

    def __init__(self, force_id: str):
        """初始化玩家组。

        参数：
            force_id: 玩家组唯一标识符
        """
        super().__init__(force_id, "force")
        self._players: Set[int] = set()  # 存储玩家ID集合

    def add_player(self, player_id: int) -> bool:
        """添加玩家到组。

        参数：
            player_id: 玩家ID

        返回：
            如果添加成功返回True，玩家已在组中返回False
        """
        if player_id in self._players:
            return False
        self._players.add(player_id)
        return True

    def remove_player(self, player_id: int) -> bool:
        """从组中移除玩家。

        参数：
            player_id: 玩家ID

        返回：
            如果移除成功返回True，玩家不在组中返回False
        """
        if player_id not in self._players:
            return False
        self._players.remove(player_id)
        return True

    def clear(self) -> None:
        """清空玩家组，移除所有玩家。"""
        self._players.clear()

    def contains(self, player_id: int) -> bool:
        """检查玩家是否在组中。

        参数：
            player_id: 玩家ID

        返回：
            如果玩家在组中返回True，否则返回False
        """
        return player_id in self._players

    def get_players(self) -> Set[int]:
        """获取组内所有玩家ID。

        返回：
            玩家ID集合的副本
        """
        return self._players.copy()
