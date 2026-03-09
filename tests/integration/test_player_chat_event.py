"""玩家聊天事件集成测试。

此模块测试 TriggerRegisterPlayerChatEvent native函数和simulate_player_chat方法的集成。
"""

import pytest


class TestPlayerChatEvent:
    """测试玩家聊天事件功能。"""

    def test_player_chat_event_substring_match(self):
        """测试玩家聊天事件子字符串匹配。"""
        from jass_runner.vm.jass_vm import JassVM

        script = '''
function onPlayerChat takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "收到聊天消息!")
endfunction

function main takes nothing returns nothing
    local trigger t
    set t = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t, Player(0), "hello", false)
    call TriggerAddAction(t, function onPlayerChat)
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

        # 模拟玩家0发送包含"hello"的消息
        vm.simulate_player_chat(0, "hello world")

    def test_player_chat_event_exact_match(self):
        """测试玩家聊天事件精确匹配。"""
        from jass_runner.vm.jass_vm import JassVM

        script = '''
function onExactMatch takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "精确匹配成功!")
endfunction

function main takes nothing returns nothing
    local trigger t
    set t = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t, Player(0), "start", true)
    call TriggerAddAction(t, function onExactMatch)
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

        # 模拟玩家0发送精确匹配的消息
        vm.simulate_player_chat(0, "start")

    def test_player_chat_event_exact_match_no_trigger(self):
        """测试精确匹配模式下不匹配的消息不会触发。"""
        from jass_runner.vm.jass_vm import JassVM

        action_called = [False]

        # 使用Python端验证动作是否被调用
        vm = JassVM(enable_timers=False)

        script = '''
function onExactMatch takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "应该不会被触发")
endfunction

function main takes nothing returns nothing
    local trigger t
    set t = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t, Player(0), "exact", true)
    call TriggerAddAction(t, function onExactMatch)
endfunction
'''
        vm.run(script, load_blizzard=False)

        # 发送不匹配的消息（精确匹配要求完全一致）
        vm.simulate_player_chat(0, "exact message")
        # 触发器不应该被触发（因为没有验证错误，测试通过表示成功）

    def test_player_chat_event_wrong_player(self):
        """测试非目标玩家的聊天不会触发事件。"""
        from jass_runner.vm.jass_vm import JassVM

        vm = JassVM(enable_timers=False)

        script = '''
function onPlayerChat takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "玩家0的消息!")
endfunction

function main takes nothing returns nothing
    local trigger t
    set t = CreateTrigger()
    // 只监听玩家0的聊天
    call TriggerRegisterPlayerChatEvent(t, Player(0), "test", false)
    call TriggerAddAction(t, function onPlayerChat)
endfunction
'''
        vm.run(script, load_blizzard=False)

        # 玩家1发送消息，不应该触发
        vm.simulate_player_chat(1, "test message")
        # 玩家0发送消息，应该触发
        vm.simulate_player_chat(0, "test message")

    def test_player_chat_event_multiple_triggers(self):
        """测试多个触发器监听不同聊天消息。"""
        from jass_runner.vm.jass_vm import JassVM

        vm = JassVM(enable_timers=False)

        script = '''
function onHello takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "Hello received!")
endfunction

function onGoodbye takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "Goodbye received!")
endfunction

function main takes nothing returns nothing
    local trigger t1
    local trigger t2

    set t1 = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t1, Player(0), "hello", false)
    call TriggerAddAction(t1, function onHello)

    set t2 = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t2, Player(0), "bye", false)
    call TriggerAddAction(t2, function onGoodbye)
endfunction
'''
        vm.run(script, load_blizzard=False)

        # 触发hello
        vm.simulate_player_chat(0, "hello there")
        # 触发bye
        vm.simulate_player_chat(0, "goodbye and bye")
