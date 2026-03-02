"""单位组Native函数集成测试。"""

from jass_runner.vm.jass_vm import JassVM


class TestGroupNativesIntegration:
    """测试单位组native函数完整工作流。"""

    def test_group_lifecycle_workflow(self):
        """测试单位组完整生命周期。"""
        code = '''
        function main takes nothing returns nothing
            local group g
            local unit u1
            local unit u2

            // 创建单位组
            set g = CreateGroup()

            // 创建单位
            set u1 = CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0)
            set u2 = CreateUnit(Player(0), 1213484355, 150.0, 250.0, 0.0)

            // 添加单位到组
            call GroupAddUnit(g, u1)
            call GroupAddUnit(g, u2)

            // 验证单位在组中
            // (实际JASS中会用条件判断，这里仅测试native函数调用)

            // 清空组
            call GroupClear(g)

            // 销毁组
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()

    def test_group_with_nested_calls(self):
        """测试嵌套调用创建单位和组操作。"""
        code = '''
        function main takes nothing returns nothing
            local group g
            local unit first

            // 创建组并添加单位（使用嵌套调用）
            set g = CreateGroup()
            call GroupAddUnit(g, CreateUnit(Player(0), 1213484355, 100.0, 200.0, 0.0))

            // 获取第一个单位
            set first = FirstOfGroup(g)

            // 清理
            call GroupClear(g)
            call DestroyGroup(g)
        endfunction
        '''

        vm = JassVM()
        vm.load_script(code)
        vm.execute()
