// examples/trigger_basic.j
// 基础触发器示例 - 演示触发器系统的基本用法

// 触发器动作函数 - 当单位死亡时触发
function onUnitDeath takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "A unit has died!")
endfunction

// 主函数
function main takes nothing returns nothing
    local trigger t

    // 创建新触发器
    set t = CreateTrigger()
    call DisplayTextToPlayer(Player(0), 0, 0, "Trigger created: " + t)

    // 注册单位死亡事件到触发器
    call TriggerRegisterUnitEvent(t, EVENT_UNIT_DEATH, null)
    call DisplayTextToPlayer(Player(0), 0, 0, "Unit death event registered")

    // 添加动作函数到触发器
    call TriggerAddAction(t, function onUnitDeath)
    call DisplayTextToPlayer(Player(0), 0, 0, "Action added to trigger")

    // 触发器系统初始化完成
    call DisplayTextToPlayer(Player(0), 0, 0, "Trigger system initialized!")
    call DisplayTextToPlayer(Player(0), 0, 0, "Create a unit and kill it to test the trigger.")
endfunction
