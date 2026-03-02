"""单位组枚举Native函数集成测试。

此模块包含单位组枚举native函数的集成测试，验证完整工作流。
"""

from jass_runner.vm.jass_vm import JassVM


class TestGroupEnumIntegration:
    """测试单位组枚举native函数完整工作流。"""

    def test_group_enum_units_of_player_workflow(self):
        """测试按玩家枚举单位工作流。"""
        code = '''
        function main takes nothing returns nothing
            local group g
            local player p

            // 创建单位组
            set g = CreateGroup()
            set p = Player(0)

            // 创建一些单位
            call CreateUnit(p, 1213484355, 100.0, 200.0, 0.0)
            call CreateUnit(p, 1213484355, 150.0, 250.0, 0.0)

            // 枚举玩家0的单位到组
            call GroupEnumUnitsOfPlayer(g, p, null)

            // 验证组大小
            // (实际JASS中会用条件判断，这里仅测试native函数调用)

            // 清理
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_group_enum_units_in_range_workflow(self):
        """测试范围内枚举单位工作流。"""
        code = '''
        function main takes nothing returns nothing
            local group g

            // 创建单位组
            set g = CreateGroup()

            // 创建一些单位
            call CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            call CreateUnit(Player(0), 1213484355, 150.0, 200.0, 0.0)

            // 枚举范围内的单位
            call GroupEnumUnitsInRange(g, 100.0, 200.0, 100.0, null)

            // 清理
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
