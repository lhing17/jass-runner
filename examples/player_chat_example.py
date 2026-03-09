"""玩家聊天事件示例。

此示例展示如何使用 TriggerRegisterPlayerChatEvent native函数
和simulate_player_chat方法来模拟玩家聊天输入。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from jass_runner.vm.jass_vm import JassVM

# 定义JASS脚本
jass_script = '''
function onAnyChat takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "收到聊天消息!")
endfunction

function onHelloChat takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "Hello! 欢迎使用JASS Runner!")
endfunction

function onStartGame takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "游戏开始!")
endfunction

function main takes nothing returns nothing
    local trigger t_any
    local trigger t_hello
    local trigger t_start

    // 触发器1: 监听玩家0的任何聊天消息（子字符串匹配""，匹配所有内容）
    set t_any = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t_any, Player(0), "", false)
    call TriggerAddAction(t_any, function onAnyChat)

    // 触发器2: 监听包含"hello"的消息（不区分大小写）
    set t_hello = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t_hello, Player(0), "hello", false)
    call TriggerAddAction(t_hello, function onHelloChat)

    // 触发器3: 精确匹配"-start"命令
    set t_start = CreateTrigger()
    call TriggerRegisterPlayerChatEvent(t_start, Player(0), "-start", true)
    call TriggerAddAction(t_start, function onStartGame)

    call DisplayTextToPlayer(Player(0), 0, 0, "聊天事件已注册，等待输入...")
endfunction
'''


def main():
    print("=" * 60)
    print("JASS Runner - 玩家聊天事件示例")
    print("=" * 60)

    # 创建虚拟机
    vm = JassVM(enable_timers=False)

    # 运行脚本
    vm.run(jass_script, load_blizzard=False)

    print("\n" + "-" * 60)
    print("模拟玩家聊天输入:")
    print("-" * 60 + "\n")

    # 模拟各种聊天输入
    print("1. 玩家0发送: 'hello world'")
    vm.simulate_player_chat(0, "hello world")

    print("\n2. 玩家0发送: 'hi there' (不应该触发hello)")
    vm.simulate_player_chat(0, "hi there")

    print("\n3. 玩家0发送: '-start' (精确匹配)")
    vm.simulate_player_chat(0, "-start")

    print("\n4. 玩家0发送: '-start game' (不匹配精确模式)")
    vm.simulate_player_chat(0, "-start game")

    print("\n5. 玩家1发送: 'hello' (不同玩家，不会触发)")
    vm.simulate_player_chat(1, "hello")

    print("\n" + "=" * 60)
    print("示例完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()
