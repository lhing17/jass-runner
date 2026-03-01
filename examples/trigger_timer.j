// examples/trigger_timer.j
// 计时器触发器示例 - 演示计时器事件注册和周期性触发

// 全局变量
integer tick_count = 0
integer trigger_id = 0

// 触发器动作函数 - 计时器到期时触发
function onTimerExpired takes nothing returns nothing
    set tick_count = tick_count + 1
    call DisplayTextToPlayer(Player(0), 0, 0, "Timer tick #" + I2S(tick_count))

    // 如果达到10次触发，显示完成信息
    if tick_count >= 10 then
        call DisplayTextToPlayer(Player(0), 0, 0, "Timer trigger completed 10 ticks!")
    endif
endfunction

// 一次性触发动作
function onOneTimeTimer takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "One-time timer triggered!")
endfunction

// 周期性报告动作
function onPeriodicReport takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "Periodic report: System running normally")
endfunction

// 主函数
function main takes nothing returns nothing
    local trigger t_periodic
    local trigger t_onetime
    local trigger t_report

    call DisplayTextToPlayer(Player(0), 0, 0, "=== Timer Trigger System Demo ===")

    // 1. 创建周期性计时器触发器（每2秒触发一次）
    set t_periodic = CreateTrigger()
    call TriggerRegisterTimerEvent(t_periodic, 2.0, true)
    call TriggerAddAction(t_periodic, function onTimerExpired)
    call DisplayTextToPlayer(Player(0), 0, 0, "Periodic trigger registered (2s interval)")

    // 2. 创建一次性计时器触发器（5秒后触发）
    set t_onetime = CreateTrigger()
    call TriggerRegisterTimerEvent(t_onetime, 5.0, false)
    call TriggerAddAction(t_onetime, function onOneTimeTimer)
    call DisplayTextToPlayer(Player(0), 0, 0, "One-time trigger registered (5s delay)")

    // 3. 创建周期性报告触发器（每1秒触发）
    set t_report = CreateTrigger()
    call TriggerRegisterTimerEvent(t_report, 1.0, true)
    call TriggerAddAction(t_report, function onPeriodicReport)
    call DisplayTextToPlayer(Player(0), 0, 0, "Report trigger registered (1s interval)")

    // 4. 禁用报告触发器（演示禁用功能）
    call DisableTrigger(t_report)
    call DisplayTextToPlayer(Player(0), 0, 0, "Report trigger disabled")

    // 5. 3秒后重新启用报告触发器
    // 注意：这里使用简化逻辑，实际实现需要第二个计时器触发器

    call DisplayTextToPlayer(Player(0), 0, 0, "All timer triggers set up!")
    call DisplayTextToPlayer(Player(0), 0, 0, "Running simulation...")
endfunction
