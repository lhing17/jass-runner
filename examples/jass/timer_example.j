// examples/timer_example.j
// 演示计时器用法的示例 JASS 脚本

function timer_callback takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "Timer fired!")
endfunction

function periodic_callback takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "Periodic timer fired!")
endfunction

function main takes nothing returns nothing
    local timer t
    local timer p

    // 创建一次性计时器
    set t = CreateTimer()
    call TimerStart(t, 2.0, false, function timer_callback)

    // 创建周期性计时器
    set p = CreateTimer()
    call TimerStart(p, 1.0, true, function periodic_callback)

    call DisplayTextToPlayer(Player(0), 0, 0, "Timers started!")
endfunction
