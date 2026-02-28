# Phase 4: 集成测试和示例脚本实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建完整的集成测试和示例JASS脚本，验证所有控制流特性协同工作

**Architecture:** 编写端到端测试和真实JASS示例脚本

**Tech Stack:** Python 3.8+, pytest, 现有JassVM框架

**Dependencies:** Phase 1、2、3完成

---

## Task 1: 创建完整控制流集成测试

**Files:**
- Create: `tests/integration/test_control_flow_integration.py`

**Step 1: 编写集成测试**

```python
"""控制流集成测试。

测试所有控制流特性在真实场景中的协同工作。
"""

from jass_runner.vm.jass_vm import JassVM


def test_fibonacci_with_control_flow():
    """测试使用控制流实现的斐波那契数列。"""
    code = """
    function fibonacci takes integer n returns integer
        if n <= 0 then
            return 0
        elseif n == 1 then
            return 1
        else
            return fibonacci(n - 1) + fibonacci(n - 2)
        endif
    endfunction

    function main takes nothing returns nothing
        local integer result = fibonacci(8)
        call DisplayTextToPlayer(Player(0), 0, 0, "Fibonacci(8) = " + I2S(result))
    endfunction
    """

    vm = JassVM()
    result = vm.execute(code)

    assert result.success


def test_sum_with_loop():
    """测试使用loop计算累加和。"""
    code = """
    function sum takes integer n returns integer
        local integer total = 0
        local integer i = 1
        loop
            exitwhen i > n
            set total = total + i
            set i = i + 1
        endloop
        return total
    endfunction

    function main takes nothing returns nothing
        local integer result = sum(10)
        call DisplayTextToPlayer(Player(0), 0, 0, "Sum(10) = " + I2S(result))
    endfunction
    """

    vm = JassVM()
    result = vm.execute(code)

    assert result.success


def test_prime_check():
    """测试素数判断，使用嵌套控制流。"""
    code = """
    function is_prime takes integer n returns boolean
        if n < 2 then
            return false
        endif
        if n == 2 then
            return true
        endif
        if n / 2 * 2 == n then
            return false
        endif

        local integer i = 3
        loop
            exitwhen i * i > n
            if n / i * i == n then
                return false
            endif
            set i = i + 2
        endloop
        return true
    endfunction

    function main takes nothing returns nothing
        local boolean r1 = is_prime(2)
        local boolean r2 = is_prime(17)
        local boolean r3 = is_prime(100)
        call DisplayTextToPlayer(Player(0), 0, 0, "Prime check done")
    endfunction
    """

    vm = JassVM()
    result = vm.execute(code)

    assert result.success


def test_gcd_with_loop():
    """测试使用loop计算最大公约数。"""
    code = """
    function gcd takes integer a, integer b returns integer
        loop
            exitwhen b == 0
            local integer temp = b
            set b = a - (a / b) * b
            set a = temp
        endloop
        return a
    endfunction

    function main takes nothing returns nothing
        local integer result = gcd(48, 18)
        call DisplayTextToPlayer(Player(0), 0, 0, "GCD(48, 18) = " + I2S(result))
    endfunction
    """

    vm = JassVM()
    result = vm.execute(code)

    assert result.success


def test_nested_loop_matrix():
    """测试嵌套循环（矩阵遍历场景）。"""
    code = """
    function main takes nothing returns nothing
        local integer rows = 3
        local integer cols = 4
        local integer total = 0
        local integer i = 0

        loop
            exitwhen i >= rows
            local integer j = 0
            loop
                exitwhen j >= cols
                set total = total + 1
                set j = j + 1
            endloop
            set i = i + 1
        endloop

        call DisplayTextToPlayer(Player(0), 0, 0, "Total cells = " + I2S(total))
    endfunction
    """

    vm = JassVM()
    result = vm.execute(code)

    assert result.success


def test_complex_control_flow():
    """测试复杂控制流组合。"""
    code = """
    function factorial takes integer n returns integer
        if n < 0 then
            return 0
        elseif n == 0 or n == 1 then
            return 1
        endif

        local integer result = 1
        local integer i = 2
        loop
            exitwhen i > n
            set result = result * i
            set i = i + 1
        endloop
        return result
    endfunction

    function main takes nothing returns nothing
        local integer i = 0
        loop
            exitwhen i > 5
            local integer f = factorial(i)
            call DisplayTextToPlayer(Player(0), 0, 0, "Factorial(" + I2S(i) + ") = " + I2S(f))
            set i = i + 1
        endloop
    endfunction
    """

    vm = JassVM()
    result = vm.execute(code)

    assert result.success
```

**Step 2: 运行测试**

```bash
pytest tests/integration/test_control_flow_integration.py -v
```
Expected: PASS

**Step 3: 提交**

```bash
git add tests/integration/test_control_flow_integration.py
git commit -m "test(integration): 添加控制流集成测试

- 斐波那契数列测试
- 累加和测试
- 素数判断测试
- 最大公约数测试
- 嵌套循环矩阵测试
- 复杂控制流组合测试

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 2: 创建控制流示例JASS脚本

**Files:**
- Create: `examples/control_flow_demo.j`

**Step 1: 创建示例脚本**

```jass
// 控制流特性演示脚本
// 展示if/elseif/else/endif, loop/exitwhen/endloop, return等功能

function fibonacci takes integer n returns integer
    // 使用递归和条件语句实现斐波那契数列
    if n <= 0 then
        return 0
    elseif n == 1 then
        return 1
    else
        return fibonacci(n - 1) + fibonacci(n - 2)
    endif
endfunction

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

function is_even takes integer n returns boolean
    // 简单条件判断
    if n / 2 * 2 == n then
        return true
    else
        return false
    endif
endfunction

function print_numbers takes integer max returns nothing
    // 使用loop和if嵌套
    local integer i = 0
    loop
        exitwhen i > max

        if is_even(i) then
            call DisplayTextToPlayer(Player(0), 0, 0, I2S(i) + " is even")
        else
            call DisplayTextToPlayer(Player(0), 0, 0, I2S(i) + " is odd")
        endif

        set i = i + 1
    endloop
endfunction

function multiply_table takes integer n returns nothing
    // 嵌套循环示例
    local integer i = 1
    loop
        exitwhen i > n

        local integer j = 1
        loop
            exitwhen j > n

            local integer product = i * j
            call DisplayTextToPlayer(Player(0), 0, 0, I2S(i) + " x " + I2S(j) + " = " + I2S(product))

            set j = j + 1
        endloop

        set i = i + 1
    endloop
endfunction

function find_first_divisible takes integer start, integer divisor returns integer
    // 使用exitwhen提前退出循环
    local integer i = start
    loop
        exitwhen i > 100

        if i / divisor * divisor == i then
            return i
        endif

        set i = i + 1
    endloop
    return -1
endfunction

function main takes nothing returns nothing
    // 主函数：展示所有控制流特性

    call DisplayTextToPlayer(Player(0), 0, 0, "=== Control Flow Demo ===")

    // 1. 斐波那契数列
    local integer fib = fibonacci(10)
    call DisplayTextToPlayer(Player(0), 0, 0, "Fibonacci(10) = " + I2S(fib))

    // 2. 累加和
    local integer s = sum(10)
    call DisplayTextToPlayer(Player(0), 0, 0, "Sum(1 to 10) = " + I2S(s))

    // 3. 奇偶判断
    call DisplayTextToPlayer(Player(0), 0, 0, "Numbers 0-5:")
    call print_numbers(5)

    // 4. 乘法表
    call DisplayTextToPlayer(Player(0), 0, 0, "Multiplication table (1-3):")
    call multiply_table(3)

    // 5. 查找第一个可被整除的数
    local integer first = find_first_divisible(10, 7)
    call DisplayTextToPlayer(Player(0), 0, 0, "First number >= 10 divisible by 7: " + I2S(first))

    call DisplayTextToPlayer(Player(0), 0, 0, "=== Demo Complete ===")
endfunction
```

**Step 2: 测试示例脚本执行**

```bash
python -m jass_runner examples/control_flow_demo.j
```
Expected: 成功执行，输出演示内容

**Step 3: 提交**

```bash
git add examples/control_flow_demo.j
git commit -m "feat(examples): 添加控制流演示脚本

- 斐波那契数列
- 累加和计算
- 奇偶判断
- 嵌套循环乘法表
- 提前return示例

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Task 3: 运行完整测试套件

**Step 1: 运行所有测试**

```bash
pytest --tb=short
```
Expected: 所有测试通过

**Step 2: 生成覆盖率报告**

```bash
pytest --cov=src/jass_runner --cov-report=term-missing
```
Expected: 核心模块覆盖率>90%

**Step 3: 最终提交**

```bash
git add -A
git commit -m "feat: 完成控制流语句扩展实现

- Parser层: IfStmt, LoopStmt, ExitWhenStmt, ReturnStmt
- Evaluator层: 完整运算符支持(+,-,*,/,==,!=,<,>,<=,>=,and,or,not)
- Interpreter层: if/elseif/else, loop/exitwhen, return执行
- 完整测试覆盖: 单元测试+集成测试
- 示例脚本: control_flow_demo.j

Co-Authored-By: Claude (kimi-k2.5) <noreply@anthropic.com>"
```

---

## Phase 4 完成检查清单

- [x] 控制流集成测试（斐波那契、累加和、素数、GCD、嵌套循环）
- [x] 控制流演示脚本
- [x] 完整测试套件通过
- [x] 覆盖率报告

**项目完成！**
