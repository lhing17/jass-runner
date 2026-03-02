"""技能系统Native函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestAbilityNativesIntegration:
    """测试技能系统native函数完整工作流。"""

    def test_ability_lifecycle_workflow(self):
        """测试技能完整生命周期。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            local integer ability_id

            // 创建单位
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)

            // 添加技能（使用技能ID）
            set ability_id = 1097699445  // 'AHhb' - 圣光术
            call UnitAddAbility(u, ability_id)

            // 设置技能等级
            call SetUnitAbilityLevel(u, ability_id, 3)

            // 增加等级
            call IncUnitAbilityLevel(u, ability_id)

            // 降低等级
            call DecUnitAbilityLevel(u, ability_id)

            // 设为永久技能
            call UnitMakeAbilityPermanent(u, ability_id, true)

            // 移除技能
            call UnitRemoveAbility(u, ability_id)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_ability_with_nested_calls(self):
        """测试嵌套调用和技能操作。"""
        code = '''
        function main takes nothing returns nothing
            local unit u
            local integer ability_id

            // 创建单位并添加技能
            set u = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            set ability_id = 1097699445

            // 添加技能
            call UnitAddAbility(u, ability_id)

            // 获取并验证等级
            // (实际JASS中会用条件判断，这里仅测试native函数调用)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
