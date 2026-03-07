// 控制流特性演示脚本
// 展示if/elseif/else/endif, loop/exitwhen/endloop, return等功能

function sum takes integer n returns integer
    // 使用loop计算1到n的累加和
    local integer total = 0
    local integer i = 1
    loop
        exitwhen i > n
        set total = total + i
        set i = i + 1
    endloop
    return total
endfunction

function multiply_table takes integer n returns nothing
    // 嵌套循环示例
    local integer i = 1
    loop
        exitwhen i > n

        local integer j = 1
        loop
            exitwhen j > n
            call DisplayTextToPlayer(Player(0), 0, 0, "Processing...")
            set j = j + 1
        endloop

        set i = i + 1
    endloop
endfunction

function find_value takes integer target returns integer
    // 使用if和loop查找值
    local integer i = 0
    loop
        exitwhen i > 100

        if i == target then
            return i
        endif

        set i = i + 1
    endloop
    return -1
endfunction

function max takes integer a, integer b returns integer
    // 简单条件判断
    if a > b then
        return a
    else
        return b
    endif
endfunction

function main takes nothing returns nothing
    // 主函数：展示所有控制流特性

    call DisplayTextToPlayer(Player(0), 0, 0, "=== Control Flow Demo ===")

    // 1. 累加和
    local integer s = sum(10)
    call DisplayTextToPlayer(Player(0), 0, 0, "Sum calculated")

    // 2. 乘法表
    call DisplayTextToPlayer(Player(0), 0, 0, "Multiplication table (1-3):")
    call multiply_table(3)

    // 3. 查找值
    local integer found = find_value(42)
    call DisplayTextToPlayer(Player(0), 0, 0, "Value found")

    // 4. 最大值
    local integer m = max(5, 3)
    call DisplayTextToPlayer(Player(0), 0, 0, "Max calculated")

    call DisplayTextToPlayer(Player(0), 0, 0, "=== Demo Complete ===")
endfunction
