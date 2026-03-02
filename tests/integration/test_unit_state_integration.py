"""单位状态Native函数集成测试。

此模块包含单位状态相关native函数的集成测试。
"""

from jass_runner.vm.jass_vm import JassVM


class TestUnitStateIntegration:
    """测试单位状态native函数完整工作流。"""

    def test_widget_life_workflow(self):
        """测试widget生命值操作工作流。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            local real life

            // 创建单位
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)

            // 获取生命值
            set life = GetWidgetLife(u)
            // life 应该为 100.0

            // 设置生命值
            call SetWidgetLife(u, 50.0)

            // 再次获取
            set life = GetWidgetLife(u)
            // life 应该为 50.0
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_unit_damage_workflow(self):
        """测试单位伤害工作流。"""
        code = '''
        function main takes nothing returns nothing
            local unit attacker
            local unit target

            // 创建单位
            set attacker = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            set target = CreateUnit(Player(1), 1213484355, 150.0, 200.0, 0.0)

            // 造成伤害
            call UnitDamageTarget(attacker, target, 25.0, true, false, 0, 0, 0)

            // 目标生命值应该为 75.0
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
