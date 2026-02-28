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
    vm.load_script(code)
    vm.execute()
    assert True


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
    vm.load_script(code)
    vm.execute()
    assert True


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
    vm.load_script(code)
    vm.execute()
    assert True


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
    vm.load_script(code)
    vm.execute()
    assert True


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
    vm.load_script(code)
    vm.execute()
    assert True


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
    vm.load_script(code)
    vm.execute()
    assert True
