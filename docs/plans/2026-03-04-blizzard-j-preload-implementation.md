# JassVM 前置加载 blizzard.j 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 JassVM 添加 `load_blizzard()` 方法，支持按需加载 blizzard.j 作为前置脚本

**Architecture:** 在 JassVM 中添加可选的 blizzard.j 加载机制，使用完整解析器解析 blizzard.j 内容，在执行用户脚本前优先执行。支持自动路径查找和自定义路径，失败仅记录警告。

**Tech Stack:** Python 3.8+, 现有 Jass 解析器、解释器

**设计文档:** `docs/plans/2026-03-04-blizzard-j-preload-design.md`

---

## Task 1: 添加 JassVM 状态变量支持 blizzard 脚本存储

**Files:**
- Create: 无
- Modify: `src/jass_runner/vm/jass_vm.py:45-47` (在 `__init__` 方法中添加新属性)
- Test: 无（后续任务一起测试）

**Step 1: 添加 blizzard_ast 和 blizzard_loaded 属性**

```python
self.ast = None
self.blizzard_ast = None  # 存储 blizzard.j 的 AST
self.loaded = False
self.blizzard_loaded = False  # blizzard.j 是否已加载
```

**Step 2: Commit**

```bash
git add src/jass_runner/vm/jass_vm.py
git commit -m "feat(vm): 添加 blizzard_ast 和 blizzard_loaded 状态变量"
```

---

## Task 2: 实现 load_blizzard 方法

**Files:**
- Create: 无
- Modify: `src/jass_runner/vm/jass_vm.py:60-63` 之后（在 load_file 方法之后）
- Test: `tests/vm/test_jass_vm.py`

**Step 1: 编写失败测试**

在 `tests/vm/test_jass_vm.py` 添加：

```python
class TestLoadBlizzard:
    """测试 load_blizzard 方法。"""

    def test_load_blizzard_auto_path_success(self):
        """测试自动路径加载 blizzard.j 成功。"""
        vm = JassVM()

        result = vm.load_blizzard()

        assert result is True
        assert vm.blizzard_loaded is True
        assert vm.blizzard_ast is not None

    def test_load_blizzard_custom_path_success(self):
        """测试自定义路径加载 blizzard.j 成功。"""
        vm = JassVM()
        path = 'resources/blizzard.j'

        result = vm.load_blizzard(path)

        assert result is True
        assert vm.blizzard_loaded is True

    def test_load_blizzard_invalid_path_returns_false(self):
        """测试无效路径返回 False 不抛出异常。"""
        vm = JassVM()

        result = vm.load_blizzard('nonexistent/path.j')

        assert result is False
        assert vm.blizzard_loaded is False
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/vm/test_jass_vm.py::TestLoadBlizzard -v
```

Expected: FAIL - AttributeError: 'JassVM' object has no attribute 'load_blizzard'

**Step 3: 实现 load_blizzard 方法**

在 `src/jass_runner/vm/jass_vm.py` 约 60-63 行（load_file 方法后）添加：

```python
def load_blizzard(self, path: str = None) -> bool:
    """
    加载 blizzard.j 作为前置脚本。

    参数:
        path: blizzard.j 的路径，None 则自动查找 resources/blizzard.j

    返回:
        bool: 加载成功返回 True，失败返回 False（仅记录警告）
    """
    # 自动查找路径
    if path is None:
        path = self._find_blizzard_path()
        if path is None:
            logger.warning("未找到 blizzard.j，已跳过加载")
            return False

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = Parser(content)
        self.blizzard_ast = parser.parse()
        self.blizzard_loaded = True
        logger.info(f"blizzard.j 已加载: {path}")
        return True

    except FileNotFoundError:
        logger.warning(f"blizzard.j 文件未找到: {path}")
        return False
    except Exception as e:
        logger.warning(f"blizzard.j 解析失败: {e}")
        return False

def _find_blizzard_path(self) -> Optional[str]:
    """自动查找 blizzard.j 的默认路径。"""
    possible_paths = [
        'resources/blizzard.j',
        os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'blizzard.j'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'resources', 'blizzard.j'),
    ]

    for p in possible_paths:
        normalized = os.path.normpath(p)
        if os.path.exists(normalized):
            return normalized
    return None
```

**Step 4: 运行测试确认通过**

```bash
pytest tests/vm/test_jass_vm.py::TestLoadBlizzard -v
```

Expected: PASS (3 passed)

**Step 5: Commit**

```bash
git add src/jass_runner/vm/jass_vm.py tests/vm/test_jass_vm.py
git commit -m "feat(vm): 实现 load_blizzard 方法，支持自动查找和自定义路径"
```

---

## Task 3: 执行时优先执行 blizzard 脚本

**Files:**
- Create: 无
- Modify: `src/jass_runner/vm/jass_vm.py:64-79` (execute 方法)
- Test: `tests/vm/test_jass_vm.py`

**Step 1: 编写失败测试**

在 `tests/vm/test_jass_vm.py` 添加：

```python
    def test_execute_with_blizzard_calls_blizzard_functions(self):
        """测试加载 blizzard 后能执行其中的函数。"""
        vm = JassVM()
        vm.load_blizzard()

        # 加载一个调用 blizzard.j 中 BJDebugMsg 函数的脚本
        vm.load_script('''
function main takes nothing returns nothing
    call BJDebugMsg("Hello from blizzard function")
endfunction
''')
        # 不应该抛出未定义函数的错误
        vm.execute()
```

**Step 2: 运行测试确认失败**

```bash
pytest tests/vm/test_jass_vm.py::TestLoadBlizzard::test_execute_with_blizzard_calls_blizzard_functions -v
```

Expected: FAIL - 可能因为 blizzard.j 中有未知的 native 函数（这是预期的，我们需要验证它尝试加载）

**Step 3: 修改 execute 方法**

在 `src/jass_runner/vm/jass_vm.py:64-79` 修改 execute 方法：

```python
def execute(self):
    """执行已加载的脚本。"""
    if not self.loaded:
        raise RuntimeError("未加载脚本。请先调用 load_script()。")

    if self.ast is None:
        raise RuntimeError("解析脚本失败。没有可用的 AST。")

    logger.info("开始脚本执行")
    try:
        # 如果已加载 blizzard.j，先执行它
        if self.blizzard_loaded and self.blizzard_ast is not None:
            logger.debug("执行 blizzard.j")
            self.interpreter.execute(self.blizzard_ast)

        self.interpreter.execute(self.ast)
        logger.info("脚本执行成功完成")
    except Exception as e:
        logger.error(f"执行期间出错: {e}")
        raise
```

**Step 4: 运行测试**

```bash
pytest tests/vm/test_jass_vm.py::TestLoadBlizzard::test_execute_with_blizzard_calls_blizzard_functions -v
```

Expected: 可能部分失败（因为 blizzard.j 可能包含未实现的 native），但应正确执行流程

**Step 5: Commit**

```bash
git add src/jass_runner/vm/jass_vm.py tests/vm/test_jass_vm.py
git commit -m "feat(vm): execute 方法优先执行已加载的 blizzard.j 脚本"
```

---

## Task 4: 添加 run 方法支持 blizzard 参数（可选）

**Files:**
- Create: 无
- Modify: `src/jass_runner/vm/jass_vm.py:91-97` (run 方法)
- Test: `tests/vm/test_jass_vm.py`

**Step 1: 编写测试**

在 `tests/vm/test_jass_vm.py` 添加：

```python
    def test_run_with_load_blizzard_true(self):
        """测试 run 方法支持加载 blizzard。"""
        vm = JassVM()

        vm.run('function main takes nothing returns nothing endfunction',
               load_blizzard=True)

        assert vm.blizzard_loaded is True
```

**Step 2: 实现 run 方法扩展**

修改 `run` 方法签名：

```python
def run(self, script_content: str, simulate_seconds: float = 0.0,
        load_blizzard: bool = False, blizzard_path: str = None):
    """
    加载并执行脚本，可选运行模拟。

    参数:
        script_content: JASS 脚本内容
        simulate_seconds: 模拟秒数
        load_blizzard: 是否加载 blizzard.j
        blizzard_path: 自定义 blizzard.j 路径
    """
    if load_blizzard:
        self.load_blizzard(blizzard_path)

    self.load_script(script_content)
    self.execute()

    if simulate_seconds > 0 and self.enable_timers:
        self.run_simulation(simulate_seconds)
```

**Step 3: 运行测试并提交**

```bash
pytest tests/vm/test_jass_vm.py -v
git add src/jass_runner/vm/jass_vm.py tests/vm/test_jass_vm.py
git commit -m "feat(vm): run 方法支持自动加载 blizzard 参数"
```

---

## Task 5: 更新 CLI 支持 --blizzard 选项（可选）

**Files:**
- Modify: `src/jass_runner/cli.py`
- Modify: `src/jass_runner/vm/jass_vm.py` (如有需要)

**Step 1: 添加 CLI 参数**

在 `src/jass_runner/cli.py:24-60` 之间添加参数：

```python
parser.add_argument(
    '--blizzard', '-b',
    action='store_true',
    help='加载 blizzard.j 前置脚本'
)

parser.add_argument(
    '--blizzard-path',
    type=str,
    default=None,
    help='指定 blizzard.j 的路径（默认: resources/blizzard.j）'
)
```

**Step 2: 修改 main 函数逻辑**

在 `main()` 函数中，创建 VM 后如有需要则加载 blizzard：

```python
vm = JassVM(enable_timers=not args.no_timers)

# 如果指定了 --blizzard，加载 blizzard.j
if args.blizzard:
    success = vm.load_blizzard(args.blizzard_path)
    if not success:
        logger.warning("blizzard.j 加载失败，继续执行用户脚本")

vm.load_file(args.script)
# ...
```

**Step 3: Commit**

```bash
git add src/jass_runner/cli.py
git commit -m "feat(cli): 添加 --blizzard 选项支持加载前置脚本"
```

---

## Task 6: 运行所有测试

**Step 1: 运行全部测试**

```bash
pytest tests/ -v --tb=short
```

Expected: All pass

**Step 2: 运行示例验证**

```bash
python -m jass_runner examples/hello_world.j --blizzard
```

应成功加载并显示 blizzard.j 加载信息。

---

## 总结

本计划实现以下功能：

1. **JassVM.load_blizzard(path=None)** - 按需加载 blizzard.j
2. **自动路径查找** - 自动在 resources/ 目录查找
3. **执行顺序** - blizzard.j 优先于用户脚本执行
4. **错误处理** - 失败仅记录警告
5. **CLI 支持** - `--blizzard` 选项

**Files Modified:**
- `src/jass_runner/vm/jass_vm.py`
- `src/jass_runner/cli.py` (可选)
- `tests/vm/test_jass_vm.py`

**New Tests:**
- `TestLoadBlizzard` 类：4+ 个测试方法
