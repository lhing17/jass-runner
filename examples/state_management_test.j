// 状态管理系统测试脚本
function main takes nothing returns nothing
    local integer player = 0
    local string unitType = "hfoo"
    local real x = 100.0
    local real y = 200.0
    local real facing = 270.0

    // 创建单位
    local unit u = CreateUnit(player, 'hfoo', x, y, facing)

    // 查询单位状态
    local real life = GetUnitState(u, "UNIT_STATE_LIFE")
    local real maxLife = GetUnitState(u, "UNIT_STATE_MAX_LIFE")

    // 显示信息
    call DisplayTextToPlayer(player, 0, 0, "创建单位: " + unitType)
    call DisplayTextToPlayer(player, 0, 0, "单位ID: " + u)
    call DisplayTextToPlayer(player, 0, 0, "生命值: " + R2S(life) + "/" + R2S(maxLife))

    // 杀死单位
    call KillUnit(u)

    // 再次查询（应返回0）
    local real lifeAfterKill = GetUnitState(u, "UNIT_STATE_LIFE")
    call DisplayTextToPlayer(player, 0, 0, "杀死后生命值: " + R2S(lifeAfterKill))

    call DisplayTextToPlayer(player, 0, 0, "测试完成")
endfunction
