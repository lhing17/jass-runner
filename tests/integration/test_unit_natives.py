"""单位操作 native 函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestUnitNativesIntegration:
    """测试单位 native 函数完整工作流。"""

    def test_unit_lifecycle_workflow(self):
        """测试单位完整生命周期。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            // 创建单位
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)

            // 获取并设置状态
            call SetUnitState(u, 0, 80.0)

            // 获取位置
            local real x = GetUnitX(u)
            local real y = GetUnitY(u)

            // 设置新位置
            call SetUnitPosition(u, 300.0, 400.0)

            // 设置朝向
            call SetUnitFacing(u, 90.0)
            local real facing = GetUnitFacing(u)

            // 获取单位信息
            local integer type_id = GetUnitTypeId(u)
            local string name = GetUnitName(u)

            // 杀死单位
            call KillUnit(u)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_create_unit_at_loc_workflow(self):
        """测试使用 Location 创建单位。"""
        code = '''
        function main takes nothing returns nothing
            local location loc = Location(500.0, 600.0)
            local unit u = CreateUnitAtLoc(Player(0), 1213484355, loc, 45.0)

            // 验证位置
            local real x = GetUnitX(u)
            local real y = GetUnitY(u)

            // 清理
            call RemoveLocation(loc)
            call KillUnit(u)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
