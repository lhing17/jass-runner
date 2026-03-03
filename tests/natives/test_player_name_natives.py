"""玩家名称相关 native 函数的测试。"""


def test_get_player_name():
    """测试 GetPlayerName native 函数。"""
    from src.jass_runner.natives.player_name_natives import GetPlayerName
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext()
    native = GetPlayerName()

    player = handle_manager.get_player(0)
    result = native.execute(state_context, player)

    assert result == "玩家0"
