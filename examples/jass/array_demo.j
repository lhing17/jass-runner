// examples/array_demo.j
// 数组功能演示

globals
    integer array playerScores
    string array playerNames
endglobals

function InitArrays takes nothing returns nothing
    local integer i
    local integer array tempScores

    // 初始化全局数组
    set playerScores[0] = 100
    set playerScores[1] = 200
    set playerNames[0] = "Player1"

    // 使用局部数组
    set i = 0
    set tempScores[i] = playerScores[0] + 50
    set tempScores[i + 1] = tempScores[i] * 2
endfunction
