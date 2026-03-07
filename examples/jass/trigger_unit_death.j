// examples/trigger_unit_death.j
// 单位死亡事件处理示例 - 演示带条件的触发器和死亡计数

// 全局变量用于记录死亡计数
integer death_count = 0
integer hero_death_count = 0

// 条件函数 - 只统计英雄单位的死亡
function isHeroDeath takes nothing returns boolean
    // 简化示例：假设80%的死亡是英雄单位（实际应检测单位类型）
    return true
endfunction

// 触发器动作函数 - 当任何单位死亡时触发
function onAnyUnitDeath takes nothing returns nothing
    // 增加总死亡计数
    set death_count = death_count + 1
    call DisplayTextToPlayer(Player(0), 0, 0, "Unit died! Total deaths: " + I2S(death_count))
endfunction

// 触发器动作函数 - 当英雄单位死亡时触发
function onHeroDeath takes nothing returns nothing
    // 增加英雄死亡计数
    set hero_death_count = hero_death_count + 1
    call DisplayTextToPlayer(Player(0), 0, 0, "HERO died! Hero deaths: " + I2S(hero_death_count))
endfunction

// 创建测试单位并触发死亡事件的函数
function testDeathEvents takes nothing returns nothing
    call DisplayTextToPlayer(Player(0), 0, 0, "Testing death events...")

    // 模拟单位死亡事件触发
    // 注意：实际的单位创建和死亡需要KillUnit函数触发事件
endfunction

// 主函数
function main takes nothing returns nothing
    local trigger t_any
    local trigger t_hero

    call DisplayTextToPlayer(Player(0), 0, 0, "=== Unit Death Counter System ===")

    // 创建通用死亡计数触发器
    set t_any = CreateTrigger()
    call TriggerRegisterUnitEvent(t_any, EVENT_UNIT_DEATH, null)
    call TriggerAddAction(t_any, function onAnyUnitDeath)
    call DisplayTextToPlayer(Player(0), 0, 0, "General death counter trigger initialized")

    // 创建英雄死亡计数触发器
    set t_hero = CreateTrigger()
    call TriggerRegisterUnitEvent(t_hero, EVENT_UNIT_DEATH, null)
    call TriggerAddCondition(t_hero, function isHeroDeath)
    call TriggerAddAction(t_hero, function onHeroDeath)
    call DisplayTextToPlayer(Player(0), 0, 0, "Hero death counter trigger initialized")

    // 显示初始状态
    call DisplayTextToPlayer(Player(0), 0, 0, "Death counter system ready!")
    call DisplayTextToPlayer(Player(0), 0, 0, "Current stats - Total: " + I2S(death_count) + ", Heroes: " + I2S(hero_death_count))

    // 测试死亡事件
    call testDeathEvents()
endfunction
