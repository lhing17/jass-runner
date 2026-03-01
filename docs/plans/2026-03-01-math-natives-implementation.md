# JASS数学Native函数实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现common.j中定义的15个数学Native函数，分为核心数学函数（6个）和扩展数学函数（9个）。

**Architecture:** 创建两个新模块math_core.py和math_extended.py，每个函数继承NativeFunction基类，通过NativeFactory注册到系统中。使用Python标准库math和random实现计算逻辑。

**Tech Stack:** Python 3.8+, math模块, random模块, pytest

---

## 阶段1: 核心数学函数 (math_core.py)

### Task 1: 创建math_core.py模块和SquareRoot函数

**Files:**
- Create: `src/jass_runner/natives/math_core.py`
- Test: `tests/natives/test_math_core.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_math_core.py """

import pytest
from jass_runner.natives.math_core import SquareRoot


class TestSquareRoot:
    """测试SquareRoot函数。"""

    def test_square_root_of_positive_number(self):
        """测试正数的平方根。"""
        sqrt = SquareRoot()
        result = sqrt.execute(None, 16.0)
        assert result == 4.0

    def test_square_root_of_zero(self):
        """测试0的平方根。"""
        sqrt = SquareRoot()
        result = sqrt.execute(None, 0.0)
        assert result == 0.0

    def test_square_root_of_one(self):
        """测试1的平方根。"""
        sqrt = SquareRoot()
        result = sqrt.execute(None, 1.0)
        assert result == 1.0

    def test_square_root_of_negative_returns_zero(self):
        """测试负数的平方根返回0。"""
        sqrt = SquareRoot()
        result = sqrt.execute(None, -4.0)
        assert result == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_core.py::TestSquareRoot -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'jass_runner.natives.math_core'"

**Step 3: Write minimal implementation**

```python
"""创建 src/jass_runner/natives/math_core.py """

import math
import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class SquareRoot(NativeFunction):
    """计算平方根。

    对应JASS函数: SquareRoot(real r) -> real
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "SquareRoot"

    def execute(self, state_context, r: float) -> float:
        """执行平方根计算。

        参数:
            state_context: 状态上下文
            r: 输入实数

        返回:
            平方根结果，负数输入返回0
        """
        if r < 0:
            return 0.0
        return math.sqrt(r)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_core.py::TestSquareRoot -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_core.py src/jass_runner/natives/math_core.py
git commit -m "feat(math): add SquareRoot native function"
```

---

### Task 2: 实现Pow函数

**Files:**
- Modify: `src/jass_runner/natives/math_core.py`
- Test: `tests/natives/test_math_core.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_math_core.py """

from jass_runner.natives.math_core import Pow


class TestPow:
    """测试Pow函数。"""

    def test_pow_positive_base_positive_exponent(self):
        """测试正底数正指数。"""
        pow_func = Pow()
        result = pow_func.execute(None, 2.0, 3.0)
        assert result == 8.0

    def test_pow_zero_exponent(self):
        """测试0指数。"""
        pow_func = Pow()
        result = pow_func.execute(None, 5.0, 0.0)
        assert result == 1.0

    def test_pow_negative_exponent(self):
        """测试负指数。"""
        pow_func = Pow()
        result = pow_func.execute(None, 2.0, -1.0)
        assert result == 0.5

    def test_pow_fractional_exponent(self):
        """测试分数指数。"""
        pow_func = Pow()
        result = pow_func.execute(None, 4.0, 0.5)
        assert abs(result - 2.0) < 0.0001
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_core.py::TestPow -v`
Expected: FAIL with "ImportError: cannot import name 'Pow'"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/math_core.py """

class Pow(NativeFunction):
    """计算幂运算。

    对应JASS函数: Pow(real x, real power) -> real
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "Pow"

    def execute(self, state_context, x: float, power: float) -> float:
        """执行幂运算。

        参数:
            state_context: 状态上下文
            x: 底数
            power: 指数

        返回:
            x的power次方
        """
        return math.pow(x, power)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_core.py::TestPow -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_core.py src/jass_runner/natives/math_core.py
git commit -m "feat(math): add Pow native function"
```

---

### Task 3: 实现Cos和Sin函数

**Files:**
- Modify: `src/jass_runner/natives/math_core.py`
- Test: `tests/natives/test_math_core.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_math_core.py """

import math as pymath
from jass_runner.natives.math_core import Cos, Sin


class TestCos:
    """测试Cos函数。"""

    def test_cos_zero(self):
        """测试cos(0)。"""
        cos = Cos()
        result = cos.execute(None, 0.0)
        assert abs(result - 1.0) < 0.0001

    def test_cos_pi(self):
        """测试cos(pi)。"""
        cos = Cos()
        result = cos.execute(None, pymath.pi)
        assert abs(result - (-1.0)) < 0.0001

    def test_cos_pi_over_2(self):
        """测试cos(pi/2)。"""
        cos = Cos()
        result = cos.execute(None, pymath.pi / 2)
        assert abs(result - 0.0) < 0.0001


class TestSin:
    """测试Sin函数。"""

    def test_sin_zero(self):
        """测试sin(0)。"""
        sin = Sin()
        result = sin.execute(None, 0.0)
        assert abs(result - 0.0) < 0.0001

    def test_sin_pi_over_2(self):
        """测试sin(pi/2)。"""
        sin = Sin()
        result = sin.execute(None, pymath.pi / 2)
        assert abs(result - 1.0) < 0.0001

    def test_sin_pi(self):
        """测试sin(pi)。"""
        sin = Sin()
        result = sin.execute(None, pymath.pi)
        assert abs(result - 0.0) < 0.0001
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_core.py::TestCos tests/natives/test_math_core.py::TestSin -v`
Expected: FAIL with "ImportError"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/math_core.py """

class Cos(NativeFunction):
    """计算余弦值。

    对应JASS函数: Cos(real r) -> real
    JASS使用弧度制。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "Cos"

    def execute(self, state_context, r: float) -> float:
        """执行余弦计算。

        参数:
            state_context: 状态上下文
            r: 弧度值

        返回:
            余弦值
        """
        return math.cos(r)


class Sin(NativeFunction):
    """计算正弦值。

    对应JASS函数: Sin(real r) -> real
    JASS使用弧度制。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "Sin"

    def execute(self, state_context, r: float) -> float:
        """执行正弦计算。

        参数:
            state_context: 状态上下文
            r: 弧度值

        返回:
            正弦值
        """
        return math.sin(r)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_core.py::TestCos tests/natives/test_math_core.py::TestSin -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_core.py src/jass_runner/natives/math_core.py
git commit -m "feat(math): add Cos and Sin native functions"
```

---

### Task 4: 实现R2I和I2R函数

**Files:**
- Modify: `src/jass_runner/natives/math_core.py`
- Test: `tests/natives/test_math_core.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_math_core.py """

from jass_runner.natives.math_core import R2I, I2R


class TestR2I:
    """测试R2I函数（实数转整数）。"""

    def test_r2i_positive(self):
        """测试正实数转换。"""
        r2i = R2I()
        result = r2i.execute(None, 3.7)
        assert result == 3

    def test_r2i_negative(self):
        """测试负实数转换（向零截断）。"""
        r2i = R2I()
        result = r2i.execute(None, -3.7)
        assert result == -3

    def test_r2i_exact(self):
        """测试整数实数转换。"""
        r2i = R2I()
        result = r2i.execute(None, 5.0)
        assert result == 5


class TestI2R:
    """测试I2R函数（整数转实数）。"""

    def test_i2r_positive(self):
        """测试正整数转换。"""
        i2r = I2R()
        result = i2r.execute(None, 42)
        assert result == 42.0
        assert isinstance(result, float)

    def test_i2r_negative(self):
        """测试负整数转换。"""
        i2r = I2R()
        result = i2r.execute(None, -10)
        assert result == -10.0

    def test_i2r_zero(self):
        """测试零转换。"""
        i2r = I2R()
        result = i2r.execute(None, 0)
        assert result == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_core.py::TestR2I tests/natives/test_math_core.py::TestI2R -v`
Expected: FAIL with "ImportError"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/math_core.py """

class R2I(NativeFunction):
    """实数转整数。

    对应JASS函数: R2I(real r) -> integer
    向零截断（与Python int()行为一致）。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "R2I"

    def execute(self, state_context, r: float) -> int:
        """执行实数转整数。

        参数:
            state_context: 状态上下文
            r: 实数值

        返回:
            整数（向零截断）
        """
        return int(r)


class I2R(NativeFunction):
    """整数转实数。

    对应JASS函数: I2R(integer i) -> real
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "I2R"

    def execute(self, state_context, i: int) -> float:
        """执行整数转实数。

        参数:
            state_context: 状态上下文
            i: 整数值

        返回:
            实数值
        """
        return float(i)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_core.py::TestR2I tests/natives/test_math_core.py::TestI2R -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_core.py src/jass_runner/natives/math_core.py
git commit -m "feat(math): add R2I and I2R native functions"
```

---

### Task 5: 运行阶段1完整测试

**Files:**
- Test: `tests/natives/test_math_core.py`

**Step 1: 运行所有核心数学函数测试**

Run: `pytest tests/natives/test_math_core.py -v`
Expected: 所有15个测试通过

**Step 2: 验证覆盖率**

Run: `pytest --cov=src/jass_runner.natives.math_core --cov-report=term-missing tests/natives/test_math_core.py`
Expected: 100%覆盖率

**Step 3: Commit阶段1完成**

```bash
git add .
git commit -m "feat(math): complete phase 1 - core math functions"
```

---

## 阶段2: 扩展数学函数 (math_extended.py)

### Task 6: 创建math_extended.py模块和Tan函数

**Files:**
- Create: `src/jass_runner/natives/math_extended.py`
- Test: `tests/natives/test_math_extended.py`

**Step 1: Write the failing test**

```python
"""创建 tests/natives/test_math_extended.py """

import pytest
import math as pymath
from jass_runner.natives.math_extended import Tan


class TestTan:
    """测试Tan函数。"""

    def test_tan_zero(self):
        """测试tan(0)。"""
        tan = Tan()
        result = tan.execute(None, 0.0)
        assert abs(result - 0.0) < 0.0001

    def test_tan_pi_over_4(self):
        """测试tan(pi/4)。"""
        tan = Tan()
        result = tan.execute(None, pymath.pi / 4)
        assert abs(result - 1.0) < 0.0001

    def test_tan_pi(self):
        """测试tan(pi)。"""
        tan = Tan()
        result = tan.execute(None, pymath.pi)
        assert abs(result - 0.0) < 0.0001
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_extended.py::TestTan -v`
Expected: FAIL with "ModuleNotFoundError"

**Step 3: Write minimal implementation**

```python
"""创建 src/jass_runner/natives/math_extended.py """

import math
import logging
from .base import NativeFunction

logger = logging.getLogger(__name__)


class Tan(NativeFunction):
    """计算正切值。

    对应JASS函数: Tan(real r) -> real
    JASS使用弧度制。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "Tan"

    def execute(self, state_context, r: float) -> float:
        """执行正切计算。

        参数:
            state_context: 状态上下文
            r: 弧度值

        返回:
            正切值
        """
        return math.tan(r)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_extended.py::TestTan -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_extended.py src/jass_runner/natives/math_extended.py
git commit -m "feat(math): add Tan native function"
```

---

### Task 7: 实现ModuloInteger和ModuloReal函数

**Files:**
- Modify: `src/jass_runner/natives/math_extended.py`
- Test: `tests/natives/test_math_extended.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_math_extended.py """

from jass_runner.natives.math_extended import ModuloInteger, ModuloReal


class TestModuloInteger:
    """测试ModuloInteger函数。"""

    def test_modulo_positive(self):
        """测试正数取模。"""
        mod = ModuloInteger()
        result = mod.execute(None, 10, 3)
        assert result == 1

    def test_modulo_exact_division(self):
        """测试整除取模。"""
        mod = ModuloInteger()
        result = mod.execute(None, 12, 3)
        assert result == 0

    def test_modulo_negative_dividend(self):
        """测试负被除数取模。"""
        mod = ModuloInteger()
        result = mod.execute(None, -10, 3)
        assert result == -1

    def test_modulo_by_zero(self):
        """测试除数为0返回0。"""
        mod = ModuloInteger()
        result = mod.execute(None, 10, 0)
        assert result == 0


class TestModuloReal:
    """测试ModuloReal函数。"""

    def test_modulo_real_positive(self):
        """测试正实数取模。"""
        mod = ModuloReal()
        result = mod.execute(None, 10.5, 3.0)
        assert abs(result - 1.5) < 0.0001

    def test_modulo_real_by_zero(self):
        """测试除数为0返回0。"""
        mod = ModuloReal()
        result = mod.execute(None, 10.0, 0.0)
        assert result == 0.0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_extended.py::TestModuloInteger tests/natives/test_math_extended.py::TestModuloReal -v`
Expected: FAIL with "ImportError"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/math_extended.py """

class ModuloInteger(NativeFunction):
    """整数取模。

    对应JASS函数: ModuloInteger(integer a, integer b) -> integer
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "ModuloInteger"

    def execute(self, state_context, a: int, b: int) -> int:
        """执行整数取模。

        参数:
            state_context: 状态上下文
            a: 被除数
            b: 除数

        返回:
            余数，除数为0时返回0
        """
        if b == 0:
            return 0
        return a % b


class ModuloReal(NativeFunction):
    """实数取模。

    对应JASS函数: ModuloReal(real a, real b) -> real
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "ModuloReal"

    def execute(self, state_context, a: float, b: float) -> float:
        """执行实数取模。

        参数:
            state_context: 状态上下文
            a: 被除数
            b: 除数

        返回:
            余数，除数为0时返回0
        """
        if b == 0.0:
            return 0.0
        return a % b
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_extended.py::TestModuloInteger tests/natives/test_math_extended.py::TestModuloReal -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_extended.py src/jass_runner/natives/math_extended.py
git commit -m "feat(math): add ModuloInteger and ModuloReal native functions"
```

---

### Task 8: 实现类型转换函数 (R2S, S2R, I2S, S2I)

**Files:**
- Modify: `src/jass_runner/natives/math_extended.py`
- Test: `tests/natives/test_math_extended.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_math_extended.py """

from jass_runner.natives.math_extended import R2S, S2R, I2S, S2I


class TestR2S:
    """测试R2S函数（实数转字符串）。"""

    def test_r2s_integer(self):
        """测试整数实数转换。"""
        r2s = R2S()
        result = r2s.execute(None, 42.0)
        assert result == "42.000"

    def test_r2s_decimal(self):
        """测试小数实数转换。"""
        r2s = R2S()
        result = r2s.execute(None, 3.14159)
        assert result == "3.142"

    def test_r2s_negative(self):
        """测试负数转换。"""
        r2s = R2S()
        result = r2s.execute(None, -5.5)
        assert result == "-5.500"


class TestS2R:
    """测试S2R函数（字符串转实数）。"""

    def test_s2r_valid(self):
        """测试有效字符串。"""
        s2r = S2R()
        result = s2r.execute(None, "3.14")
        assert abs(result - 3.14) < 0.0001

    def test_s2r_integer_string(self):
        """测试整数字符串。"""
        s2r = S2R()
        result = s2r.execute(None, "42")
        assert result == 42.0

    def test_s2r_invalid(self):
        """测试无效字符串返回0。"""
        s2r = S2R()
        result = s2r.execute(None, "not_a_number")
        assert result == 0.0

    def test_s2r_empty(self):
        """测试空字符串返回0。"""
        s2r = S2R()
        result = s2r.execute(None, "")
        assert result == 0.0


class TestI2S:
    """测试I2S函数（整数转字符串）。"""

    def test_i2s_positive(self):
        """测试正整数。"""
        i2s = I2S()
        result = i2s.execute(None, 42)
        assert result == "42"

    def test_i2s_negative(self):
        """测试负整数。"""
        i2s = I2S()
        result = i2s.execute(None, -10)
        assert result == "-10"

    def test_i2s_zero(self):
        """测试零。"""
        i2s = I2S()
        result = i2s.execute(None, 0)
        assert result == "0"


class TestS2I:
    """测试S2I函数（字符串转整数）。"""

    def test_s2i_valid(self):
        """测试有效字符串。"""
        s2i = S2I()
        result = s2i.execute(None, "42")
        assert result == 42

    def test_s2i_negative(self):
        """测试负数字符串。"""
        s2i = S2I()
        result = s2i.execute(None, "-10")
        assert result == -10

    def test_s2i_invalid(self):
        """测试无效字符串返回0。"""
        s2i = S2I()
        result = s2i.execute(None, "not_a_number")
        assert result == 0

    def test_s2i_empty(self):
        """测试空字符串返回0。"""
        s2i = S2I()
        result = s2i.execute(None, "")
        assert result == 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_extended.py::TestR2S tests/natives/test_math_extended.py::TestS2R tests/natives/test_math_extended.py::TestI2S tests/natives/test_math_extended.py::TestS2I -v`
Expected: FAIL with "ImportError"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/math_extended.py """

class R2S(NativeFunction):
    """实数转字符串。

    对应JASS函数: R2S(real r) -> string
    格式化为3位小数。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "R2S"

    def execute(self, state_context, r: float) -> str:
        """执行实数转字符串。

        参数:
            state_context: 状态上下文
            r: 实数值

        返回:
            格式化字符串（3位小数）
        """
        return f"{r:.3f}"


class S2R(NativeFunction):
    """字符串转实数。

    对应JASS函数: S2R(string s) -> real
    无效字符串返回0。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "S2R"

    def execute(self, state_context, s: str) -> float:
        """执行字符串转实数。

        参数:
            state_context: 状态上下文
            s: 字符串

        返回:
            实数值，无效时返回0
        """
        try:
            return float(s)
        except (ValueError, TypeError):
            return 0.0


class I2S(NativeFunction):
    """整数转字符串。

    对应JASS函数: I2S(integer i) -> string
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "I2S"

    def execute(self, state_context, i: int) -> str:
        """执行整数转字符串。

        参数:
            state_context: 状态上下文
            i: 整数值

        返回:
            字符串
        """
        return str(i)


class S2I(NativeFunction):
    """字符串转整数。

    对应JASS函数: S2I(string s) -> integer
    无效字符串返回0。
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "S2I"

    def execute(self, state_context, s: str) -> int:
        """执行字符串转整数。

        参数:
            state_context: 状态上下文
            s: 字符串

        返回:
            整数值，无效时返回0
        """
        try:
            return int(float(s))
        except (ValueError, TypeError):
            return 0
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_extended.py::TestR2S tests/natives/test_math_extended.py::TestS2R tests/natives/test_math_extended.py::TestI2S tests/natives/test_math_extended.py::TestS2I -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_extended.py src/jass_runner/natives/math_extended.py
git commit -m "feat(math): add R2S, S2R, I2S, S2I native functions"
```

---

### Task 9: 实现随机数函数 (GetRandomInt, GetRandomReal)

**Files:**
- Modify: `src/jass_runner/natives/math_extended.py`
- Test: `tests/natives/test_math_extended.py`

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_math_extended.py """

import random
from unittest.mock import patch
from jass_runner.natives.math_extended import GetRandomInt, GetRandomReal


class TestGetRandomInt:
    """测试GetRandomInt函数。"""

    def test_random_int_in_range(self):
        """测试随机整数在范围内。"""
        get_random = GetRandomInt()
        result = get_random.execute(None, 1, 10)
        assert 1 <= result <= 10

    def test_random_int_same_min_max(self):
        """测试最小值等于最大值。"""
        get_random = GetRandomInt()
        result = get_random.execute(None, 5, 5)
        assert result == 5

    def test_random_int_negative_range(self):
        """测试负数范围。"""
        get_random = GetRandomInt()
        result = get_random.execute(None, -10, -1)
        assert -10 <= result <= -1

    def test_random_int_reversed_range(self):
        """测试反转范围（最大值<最小值）。"""
        get_random = GetRandomInt()
        result = get_random.execute(None, 10, 1)
        assert result == 1  # 应该返回low值


class TestGetRandomReal:
    """测试GetRandomReal函数。"""

    def test_random_real_in_range(self):
        """测试随机实数在范围内。"""
        get_random = GetRandomReal()
        result = get_random.execute(None, 0.0, 1.0)
        assert 0.0 <= result <= 1.0

    def test_random_real_same_min_max(self):
        """测试最小值等于最大值。"""
        get_random = GetRandomReal()
        result = get_random.execute(None, 5.0, 5.0)
        assert result == 5.0

    def test_random_real_reversed_range(self):
        """测试反转范围。"""
        get_random = GetRandomReal()
        result = get_random.execute(None, 10.0, 1.0)
        assert result == 10.0  # 应该返回low值
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_math_extended.py::TestGetRandomInt tests/natives/test_math_extended.py::TestGetRandomReal -v`
Expected: FAIL with "ImportError"

**Step 3: Write minimal implementation**

```python
"""添加到 src/jass_runner/natives/math_extended.py """

import random

class GetRandomInt(NativeFunction):
    """获取随机整数。

    对应JASS函数: GetRandomInt(integer low, integer high) -> integer
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetRandomInt"

    def execute(self, state_context, low: int, high: int) -> int:
        """执行获取随机整数。

        参数:
            state_context: 状态上下文
            low: 最小值
            high: 最大值

        返回:
            [low, high]范围内的随机整数
        """
        if high < low:
            return low
        return random.randint(low, high)


class GetRandomReal(NativeFunction):
    """获取随机实数。

    对应JASS函数: GetRandomReal(real low, real high) -> real
    """

    @property
    def name(self) -> str:
        """获取函数名称。"""
        return "GetRandomReal"

    def execute(self, state_context, low: float, high: float) -> float:
        """执行获取随机实数。

        参数:
            state_context: 状态上下文
            low: 最小值
            high: 最大值

        返回:
            [low, high]范围内的随机实数
        """
        if high < low:
            return low
        return random.uniform(low, high)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_math_extended.py::TestGetRandomInt tests/natives/test_math_extended.py::TestGetRandomReal -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_math_extended.py src/jass_runner/natives/math_extended.py
git commit -m "feat(math): add GetRandomInt and GetRandomReal native functions"
```

---

### Task 10: 运行阶段2完整测试

**Files:**
- Test: `tests/natives/test_math_extended.py`

**Step 1: 运行所有扩展数学函数测试**

Run: `pytest tests/natives/test_math_extended.py -v`
Expected: 所有21个测试通过

**Step 2: 验证覆盖率**

Run: `pytest --cov=src/jass_runner.natives.math_extended --cov-report=term-missing tests/natives/test_math_extended.py`
Expected: 100%覆盖率

**Step 3: Commit阶段2完成**

```bash
git add .
git commit -m "feat(math): complete phase 2 - extended math functions"
```

---

## 阶段3: 集成与注册

### Task 11: 注册数学函数到NativeFactory

**Files:**
- Modify: `src/jass_runner/natives/factory.py`
- Test: `tests/natives/test_factory.py` (已存在，需要更新)

**Step 1: Write the failing test**

```python
"""添加到 tests/natives/test_factory.py 或创建新测试 """

import pytest
from jass_runner.natives.factory import NativeFactory
from jass_runner.natives.math_core import SquareRoot, Pow, Cos, Sin, R2I, I2R
from jass_runner.natives.math_extended import Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal


class TestNativeFactoryMathFunctions:
    """测试NativeFactory包含数学函数。"""

    def test_factory_includes_square_root(self):
        """测试工厂包含SquareRoot。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("SquareRoot")
        assert isinstance(func, SquareRoot)

    def test_factory_includes_pow(self):
        """测试工厂包含Pow。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("Pow")
        assert isinstance(func, Pow)

    def test_factory_includes_cos(self):
        """测试工厂包含Cos。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("Cos")
        assert isinstance(func, Cos)

    def test_factory_includes_sin(self):
        """测试工厂包含Sin。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("Sin")
        assert isinstance(func, Sin)

    def test_factory_includes_r2i(self):
        """测试工厂包含R2I。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("R2I")
        assert isinstance(func, R2I)

    def test_factory_includes_i2r(self):
        """测试工厂包含I2R。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("I2R")
        assert isinstance(func, I2R)

    def test_factory_includes_tan(self):
        """测试工厂包含Tan。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("Tan")
        assert isinstance(func, Tan)

    def test_factory_includes_modulo_integer(self):
        """测试工厂包含ModuloInteger。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("ModuloInteger")
        assert isinstance(func, ModuloInteger)

    def test_factory_includes_modulo_real(self):
        """测试工厂包含ModuloReal。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("ModuloReal")
        assert isinstance(func, ModuloReal)

    def test_factory_includes_r2s(self):
        """测试工厂包含R2S。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("R2S")
        assert isinstance(func, R2S)

    def test_factory_includes_s2r(self):
        """测试工厂包含S2R。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("S2R")
        assert isinstance(func, S2R)

    def test_factory_includes_i2s(self):
        """测试工厂包含I2S。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("I2S")
        assert isinstance(func, I2S)

    def test_factory_includes_s2i(self):
        """测试工厂包含S2I。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("S2I")
        assert isinstance(func, S2I)

    def test_factory_includes_get_random_int(self):
        """测试工厂包含GetRandomInt。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("GetRandomInt")
        assert isinstance(func, GetRandomInt)

    def test_factory_includes_get_random_real(self):
        """测试工厂包含GetRandomReal。"""
        factory = NativeFactory()
        registry = factory.create_default_registry()
        func = registry.get("GetRandomReal")
        assert isinstance(func, GetRandomReal)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/natives/test_factory.py::TestNativeFactoryMathFunctions -v`
Expected: FAIL with "KeyError" (函数未注册)

**Step 3: Write minimal implementation**

```python
"""修改 src/jass_runner/natives/factory.py """

from .registry import NativeRegistry
from .basic import DisplayTextToPlayer, KillUnit, CreateUnit, GetUnitState, CreateItem, RemoveItem, PlayerNative
from .timer_natives import CreateTimer, TimerStart, TimerGetElapsed, DestroyTimer, PauseTimer, ResumeTimer
from .trigger_natives import (
    CreateTrigger,
    DestroyTrigger,
    EnableTrigger,
    DisableTrigger,
    IsTriggerEnabled,
    TriggerAddAction,
    TriggerRemoveAction,
    TriggerClearActions,
    TriggerAddCondition,
    TriggerRemoveCondition,
    TriggerClearConditions,
    TriggerEvaluate,
    TriggerClearEvents,
)
from .trigger_register_event_natives import (
    TriggerRegisterTimerEvent,
    TriggerRegisterTimerExpireEvent,
    TriggerRegisterPlayerUnitEvent,
    TriggerRegisterUnitEvent,
    TriggerRegisterPlayerEvent,
    TriggerRegisterGameEvent,
)
from .math_core import SquareRoot, Pow, Cos, Sin, R2I, I2R
from .math_extended import Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal


class NativeFactory:
    """Native函数工厂。

    此类负责创建预配置的native函数注册表，简化注册过程。
    """

    def __init__(self, timer_system=None):
        """初始化工厂。

        参数：
            timer_system: 可选的计时器系统实例
        """
        self._timer_system = timer_system

    def create_default_registry(self) -> NativeRegistry:
        """创建包含默认native函数的注册表。

        返回：
            NativeRegistry: 包含DisplayTextToPlayer、KillUnit、CreateUnit和GetUnitState的注册表
        """
        registry = NativeRegistry()

        # 注册基础native函数
        registry.register(DisplayTextToPlayer())
        registry.register(KillUnit())
        registry.register(CreateUnit())
        registry.register(GetUnitState())
        registry.register(CreateItem())
        registry.register(RemoveItem())
        registry.register(PlayerNative())

        # 注册触发器生命周期native函数
        registry.register(CreateTrigger())
        registry.register(DestroyTrigger())
        registry.register(EnableTrigger())
        registry.register(DisableTrigger())
        registry.register(IsTriggerEnabled())

        # 注册触发器动作管理native函数
        registry.register(TriggerAddAction())
        registry.register(TriggerRemoveAction())
        registry.register(TriggerClearActions())

        # 注册触发器条件管理native函数
        registry.register(TriggerAddCondition())
        registry.register(TriggerRemoveCondition())
        registry.register(TriggerClearConditions())
        registry.register(TriggerEvaluate())

        # 注册触发器事件管理native函数
        registry.register(TriggerClearEvents())

        # 注册触发器事件注册native函数
        registry.register(TriggerRegisterTimerEvent())
        registry.register(TriggerRegisterTimerExpireEvent())
        registry.register(TriggerRegisterPlayerUnitEvent())
        registry.register(TriggerRegisterUnitEvent())
        registry.register(TriggerRegisterPlayerEvent())
        registry.register(TriggerRegisterGameEvent())

        # 注册核心数学函数
        registry.register(SquareRoot())
        registry.register(Pow())
        registry.register(Cos())
        registry.register(Sin())
        registry.register(R2I())
        registry.register(I2R())

        # 注册扩展数学函数
        registry.register(Tan())
        registry.register(ModuloInteger())
        registry.register(ModuloReal())
        registry.register(R2S())
        registry.register(S2R())
        registry.register(I2S())
        registry.register(S2I())
        registry.register(GetRandomInt())
        registry.register(GetRandomReal())

        # 如果计时器系统可用，注册计时器原生函数
        if self._timer_system:
            registry.register(CreateTimer(self._timer_system))
            registry.register(TimerStart(self._timer_system))
            registry.register(TimerGetElapsed(self._timer_system))
            registry.register(DestroyTimer(self._timer_system))
            registry.register(PauseTimer(self._timer_system))
            registry.register(ResumeTimer(self._timer_system))

        return registry
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/natives/test_factory.py::TestNativeFactoryMathFunctions -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/natives/test_factory.py src/jass_runner/natives/factory.py
git commit -m "feat(math): register all math functions in NativeFactory"
```

---

### Task 12: 更新natives/__init__.py导出数学函数

**Files:**
- Modify: `src/jass_runner/natives/__init__.py`

**Step 1: Write the update**

```python
"""修改 src/jass_runner/natives/__init__.py """

"""JASS native函数框架。

此包包含JASS native函数的模拟实现和状态管理系统。
"""

from .base import NativeFunction
from .registry import NativeRegistry
from .factory import NativeFactory
from .handle import Handle, Unit, Player
from .manager import HandleManager
from .state import StateContext
from .trigger_natives import (
    CreateTrigger, DestroyTrigger, EnableTrigger, DisableTrigger,
    IsTriggerEnabled, TriggerAddAction, TriggerRemoveAction, TriggerClearActions,
    TriggerAddCondition, TriggerRemoveCondition, TriggerClearConditions,
    TriggerEvaluate, TriggerClearEvents,
)
from .trigger_register_event_natives import (
    TriggerRegisterTimerEvent, TriggerRegisterTimerExpireEvent,
    TriggerRegisterPlayerUnitEvent, TriggerRegisterUnitEvent,
    TriggerRegisterPlayerEvent, TriggerRegisterGameEvent,
)
from .math_core import SquareRoot, Pow, Cos, Sin, R2I, I2R
from .math_extended import Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal

__all__ = [
    "NativeFunction",
    "NativeRegistry",
    "NativeFactory",
    "Handle",
    "Unit",
    "Player",
    "HandleManager",
    "StateContext",
    # 触发器生命周期管理
    "CreateTrigger",
    "DestroyTrigger",
    "EnableTrigger",
    "DisableTrigger",
    "IsTriggerEnabled",
    # 触发器动作管理
    "TriggerAddAction",
    "TriggerRemoveAction",
    "TriggerClearActions",
    # 触发器条件管理
    "TriggerAddCondition",
    "TriggerRemoveCondition",
    "TriggerClearConditions",
    "TriggerEvaluate",
    # 触发器事件管理
    "TriggerClearEvents",
    # 触发器事件注册
    "TriggerRegisterTimerEvent",
    "TriggerRegisterTimerExpireEvent",
    "TriggerRegisterPlayerUnitEvent",
    "TriggerRegisterUnitEvent",
    "TriggerRegisterPlayerEvent",
    "TriggerRegisterGameEvent",
    # 核心数学函数
    "SquareRoot",
    "Pow",
    "Cos",
    "Sin",
    "R2I",
    "I2R",
    # 扩展数学函数
    "Tan",
    "ModuloInteger",
    "ModuloReal",
    "R2S",
    "S2R",
    "I2S",
    "S2I",
    "GetRandomInt",
    "GetRandomReal",
]
```

**Step 2: Run test to verify imports work**

Run: `python -c "from jass_runner.natives import SquareRoot, Pow, Tan, GetRandomInt; print('Imports OK')"`
Expected: "Imports OK"

**Step 3: Commit**

```bash
git add src/jass_runner/natives/__init__.py
git commit -m "feat(math): export math functions from natives package"
```

---

### Task 13: 运行完整测试套件验证无回归

**Files:**
- Test: 所有测试文件

**Step 1: 运行所有测试**

Run: `pytest tests/ -v`
Expected: 所有现有测试通过 + 36个新数学函数测试通过

**Step 2: 验证覆盖率**

Run: `pytest --cov=src/jass_runner --cov-report=term-missing tests/`
Expected: 显示覆盖率报告，数学模块100%覆盖

**Step 3: 最终提交**

```bash
git add .
git commit -m "feat(math): complete math natives implementation - 15 functions"
```

---

## 实施完成标准

1. **核心数学函数**: 6个函数全部实现并通过测试
   - SquareRoot, Pow, Cos, Sin, R2I, I2R

2. **扩展数学函数**: 9个函数全部实现并通过测试
   - Tan, ModuloInteger, ModuloReal, R2S, S2R, I2S, S2I, GetRandomInt, GetRandomReal

3. **集成完成**:
   - 所有函数注册到NativeFactory
   - 从natives包正确导出

4. **测试覆盖**:
   - 36个单元测试全部通过
   - 100%代码覆盖率
   - 无回归（所有现有测试通过）

5. **文档更新**:
   - PROJECT_NOTES.md更新
   - TODO.md更新

---

## 执行选项

**计划已完成并保存到 `docs/plans/2026-03-01-math-natives-implementation.md`。两种执行方式：**

**1. Subagent-Driven (本会话)** - 我为每个任务派遣新的子代理，任务间进行审查，快速迭代

**2. Parallel Session (单独会话)** - 在新会话中打开并执行计划，批量执行带检查点

**选择哪种方式？**
