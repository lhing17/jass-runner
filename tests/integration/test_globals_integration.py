"""全局变量集成测试。"""

from jass_runner.vm.jass_vm import JassVM


def test_globals_with_control_flow():
    """测试全局变量在控制流语句中使用。"""
    code = """
globals
    integer counter = 0
endglobals

function main takes nothing returns nothing
    loop
        exitwhen counter >= 5
        set counter = counter + 1
    endloop
endfunction
"""
    vm = JassVM()
    vm.load_script(code)
    vm.execute()

    # 验证循环结束后全局变量的值
    assert vm.interpreter.global_context.get_variable('counter') == 5


def test_globals_with_function_calls():
    """测试全局变量在函数间共享状态。"""
    code = """
globals
    integer total = 0
endglobals

function add_to_total takes integer value returns nothing
    set total = total + value
endfunction

function main takes nothing returns nothing
    call add_to_total(10)
    call add_to_total(20)
    call add_to_total(30)
endfunction
"""
    vm = JassVM()
    vm.load_script(code)
    vm.execute()

    # 验证全局变量累加结果
    assert vm.interpreter.global_context.get_variable('total') == 60


def test_globals_example_script():
    """测试完整示例脚本。"""
    code = """
globals
    integer game_score = 0
    boolean game_active = true
endglobals

function score_point takes integer points returns nothing
    if game_active then
        set game_score = game_score + points
    endif
endfunction

function main takes nothing returns nothing
    call score_point(10)
    call score_point(20)
    set game_active = false
    call score_point(30)
endfunction
"""
    vm = JassVM()
    vm.load_script(code)
    vm.execute()

    # 验证最终分数（game_active=false后不应再加分）
    assert vm.interpreter.global_context.get_variable('game_score') == 30
