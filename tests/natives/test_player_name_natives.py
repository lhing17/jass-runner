"""玩家名称相关 native 函数的测试。"""


def test_all_player_name_natives_registered():
    """测试玩家名称 native 函数已注册。"""
    from src.jass_runner.natives.factory import NativeFactory

    factory = NativeFactory()
    registry = factory.create_default_registry()

    assert registry.get("GetPlayerName") is not None
    assert registry.get("SetPlayerName") is not None


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


def test_set_player_name():
    """测试 SetPlayerName native 函数。"""
    from src.jass_runner.natives.player_name_natives import SetPlayerName
    from src.jass_runner.natives.state import StateContext
    from src.jass_runner.natives.manager import HandleManager

    handle_manager = HandleManager()
    state_context = StateContext()
    native = SetPlayerName()

    player = handle_manager.get_player(0)
    native.execute(state_context, player, "张三")

    assert player.name == "张三"
