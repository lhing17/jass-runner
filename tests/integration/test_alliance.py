"""联盟系统集成测试。

测试完整的联盟设置和查询流程。
"""

import pytest
from jass_runner.vm.jass_vm import JassVM


class TestAllianceIntegration:
    """测试联盟系统端到端功能。"""

    def test_set_and_get_alliance(self):
        """测试设置和获取联盟关系的完整流程。"""
        jass_code = '''
function main takes nothing returns nothing
    local player p0 = Player(0)
    local player p1 = Player(1)
    local boolean result

    // 设置联盟
    call SetPlayerAlliance(p0, p1, ALLIANCE_PASSIVE, true)

    // 查询联盟
    set result = GetPlayerAlliance(p0, p1, ALLIANCE_PASSIVE)

    // 输出结果用于验证
    if result then
        call DisplayTextToPlayer(p0, 0, 0, "Alliance is active")
    else
        call DisplayTextToPlayer(p0, 0, 0, "Alliance is inactive")
    endif
endfunction
'''
        vm = JassVM()
        # 使用 run 方法执行脚本
        try:
            vm.run(jass_code)
            success = True
        except Exception:
            success = False

        assert success

    def test_alliance_constants_are_integers(self):
        """测试联盟类型常量被正确解析为整数。"""
        vm = JassVM()

        # 检查 ALLIANCE_PASSIVE 被解析为整数 0
        assert vm.interpreter.global_context.variables.get('ALLIANCE_PASSIVE') == 0

        # 检查其他联盟常量也被正确解析
        assert vm.interpreter.global_context.variables.get('ALLIANCE_SHARED_VISION') == 5
        assert vm.interpreter.global_context.variables.get('ALLIANCE_SHARED_CONTROL') == 6

    def test_convert_alliance_type(self):
        """测试 ConvertAllianceType 在脚本中的使用。"""
        jass_code = '''
function main takes nothing returns nothing
    local alliancetype at = ConvertAllianceType(0)
    local player p0 = Player(0)
    local player p1 = Player(1)

    call SetPlayerAlliance(p0, p1, at, true)
endfunction
'''
        vm = JassVM()
        try:
            vm.run(jass_code)
            success = True
        except Exception:
            success = False

        assert success
