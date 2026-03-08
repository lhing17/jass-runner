"""GetLocalPlayer native函数测试。

此模块包含GetLocalPlayer native函数的测试用例。
"""

import pytest
from jass_runner.natives.basic import PlayerNative, GetLocalPlayer
from jass_runner.natives.state import StateContext
from jass_runner.natives.handle import Player


class TestGetLocalPlayer:
    """GetLocalPlayer native函数的测试类。"""

    def setup_method(self):
        """设置测试环境。"""
        self.state_context = StateContext()
        self.get_local_player_native = GetLocalPlayer()
        self.player_native = PlayerNative()

    def test_get_local_player_returns_valid_player(self):
        """测试GetLocalPlayer返回有效的Player对象。

        验证：
        - 返回对象不为None
        - 返回对象是Player类型
        - handle_type为"player"
        """
        result = self.get_local_player_native.execute(self.state_context)

        # 验证返回对象不为None
        assert result is not None, "GetLocalPlayer返回None"

        # 验证返回对象是Player类型
        assert isinstance(result, Player), f"期望返回Player对象，实际返回{type(result)}"

        # 验证type_name为"player"
        assert result.type_name == "player", f"期望type_name为'player'，实际为'{result.type_name}'"

    def test_get_local_player_returns_player_id_zero(self):
        """测试GetLocalPlayer返回玩家ID为0。

        验证：
        - 返回的Player对象的player_id为0
        """
        result = self.get_local_player_native.execute(self.state_context)

        # 验证玩家ID为0
        assert result.player_id == 0, f"期望玩家ID为0，实际为{result.player_id}"

    def test_get_local_player_returns_same_as_player_zero(self):
        """测试GetLocalPlayer返回的对象与Player(0)相同。

        验证：
        - GetLocalPlayer返回的对象与Player(0)是同一个对象
        """
        local_player = self.get_local_player_native.execute(self.state_context)
        player_zero = self.player_native.execute(self.state_context, 0)

        # 验证两个对象是同一个对象
        assert local_player is player_zero, "GetLocalPlayer返回的对象与Player(0)不是同一个对象"
