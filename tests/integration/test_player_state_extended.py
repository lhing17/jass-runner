"""玩家状态扩展集成测试。

测试 ConvertPlayerState 和所有 playerstate 常量的使用。
"""

from jass_runner.vm.jass_vm import JassVM


class TestPlayerStateExtended:
    """测试玩家状态扩展功能。"""

    def test_player_state_constants_are_integers(self):
        """测试 playerstate 常量被正确解析为整数。"""
        vm = JassVM()

        # 检查资源状态常量
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_RESOURCE_GOLD'
        ) == 1
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_RESOURCE_LUMBER'
        ) == 2

        # 检查非资源状态常量
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_NO_CREEP_SLEEP'
        ) == 25
        assert vm.interpreter.global_context.variables.get(
            'PLAYER_STATE_OBSERVER'
        ) == 11

    def test_convert_player_state_as_parameter(self):
        """测试 ConvertPlayerState 调用结果作为函数参数。

        这是关键测试：验证 ConvertPlayerState(25) 的返回值
        可以正确传递给 SetPlayerState 和 GetPlayerState。
        """
        jass_code = '''
function main takes nothing returns nothing
    local player p = Player(0)
    local integer val

    // 使用 ConvertPlayerState 返回值作为 SetPlayerState 参数
    call SetPlayerState(p, ConvertPlayerState(25), 1)

    // 使用 ConvertPlayerState 返回值作为 GetPlayerState 参数
    set val = GetPlayerState(p, ConvertPlayerState(25))

    call DisplayTextToPlayer(p, 0, 0, "Value: " + I2S(val))
endfunction
'''
        vm = JassVM()
        try:
            vm.run(jass_code)
            success = True
        except Exception as e:
            print(f"Error: {e}")
            success = False

        assert success

    def test_set_and_get_non_resource_state(self):
        """测试设置和获取非资源状态。"""
        jass_code = '''
function main takes nothing returns nothing
    local player p = Player(0)
    local integer val

    // 设置观察者状态
    call SetPlayerState(p, PLAYER_STATE_OBSERVER, 1)

    // 获取状态值
    set val = GetPlayerState(p, PLAYER_STATE_OBSERVER)

    call DisplayTextToPlayer(p, 0, 0, "Observer: " + I2S(val))
endfunction
'''
        vm = JassVM()
        try:
            vm.run(jass_code)
            success = True
        except Exception:
            success = False

        assert success

    def test_resource_states_still_work(self):
        """测试资源状态仍然正常工作。"""
        jass_code = '''
function main takes nothing returns nothing
    local player p = Player(0)
    local integer val

    // 设置金币
    call SetPlayerState(p, PLAYER_STATE_RESOURCE_GOLD, 1000)

    // 获取金币
    set val = GetPlayerState(p, PLAYER_STATE_RESOURCE_GOLD)

    call DisplayTextToPlayer(p, 0, 0, "Gold: " + I2S(val))
endfunction
'''
        vm = JassVM()
        try:
            vm.run(jass_code)
            success = True
        except Exception:
            success = False

        assert success
