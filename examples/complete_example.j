// examples/complete_example.j
// 演示所有 JASS 运行器功能的完整示例

function unit_died takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "A unit has died!")
endfunction

function periodic_report takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Periodic report: All systems operational")
endfunction

function main takes nothing returns nothing
    local timer death_timer
    local timer report_timer
    local string unit_name

    call DisplayTextToPlayer(0, 0, 0, "Starting simulation...")

    // 创建一个单位
    set unit_name = "Hero_001"
    call DisplayTextToPlayer(0, 0, 0, "Creating unit: " + unit_name)

    // 创建死亡计时器（一次性，3 秒）
    set death_timer = CreateTimer()
    call TimerStart(death_timer, 3.0, false, function unit_died)

    // 创建周期性报告计时器（每 2 秒）
    set report_timer = CreateTimer()
    call TimerStart(report_timer, 2.0, true, function periodic_report)

    call DisplayTextToPlayer(0, 0, 0, "Timers started. Simulation running...")
endfunction
