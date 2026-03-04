# JassVM 前置加载 blizzard.j 设计文档

**日期**: 2026-03-04
**主题**: JassVM Blizzard.j 前置加载设计

## 概述

为 JassVM 添加按需加载 blizzard.j 的能力，让用户脚本可以使用其中定义的 923+ 个常量、函数和配置。

## 背景

- `blizzard.j` 位于 `resources/` 目录，包含 10229 行代码和 923+ 个 JASS 函数
- 它是魔兽争霸 III 地图脚本的基础设施，用户脚本可能依赖其中的函数
- 与 `common.j` 不同：
  - `common.j`：只包含常量定义和 native 函数声明，当前已通过 `_load_constants()` 加载常量
  - `blizzard.j`：包含大量自定义函数实现，需要完整 JASS 解析器解析

## 设计决策

### 1. 加载策略：按需显式加载

用户主动调用加载，非自动。API：

```python
vm.load_blizzard()  # 自动查找 resources/blizzard.j
# 或
vm.load_blizzard('custom/path/blizzard.j')  # 指定路径
```

### 2. 路径策略：两者结合

- 默认 `path=None`：自动查找 `resources/blizzard.j`
- 支持自定义路径：显式指定完整路径

### 3. 错误处理：仅记录警告

- 加载失败时记录警告日志
- 不抛出异常
- 继续执行用户脚本

### 4. 加载顺序

```
1. vm.load_blizzard()      # 可选，按需
2. vm.load_script(user.j)  # 用户脚本
3. vm.execute()            # 先执行 blizzard.j，再执行用户脚本
```

## 实现细节

### API 定义

```python
class JassVM:
    def load_blizzard(self, path: str = None) -> bool:
        """
        加载 blizzard.j 作为前置脚本。

        参数:
            path: blizzard.j 的路径，None 则自动查找 resources/blizzard.j

        返回:
            bool: 加载成功返回 True，失败返回 False（仅记录警告）
        """
```

### 内部状态管理

- 添加 `self.blizzard_ast` 存储解析后的 blizzard.j AST
- 添加 `self.blizzard_loaded` 标志位
- `execute()` 方法调整：
  - 如果 blizzard 已加载，先执行 blizzard AST
  - 然后执行用户脚本 AST

### 路径查找逻辑

```python
default_paths = [
    'resources/blizzard.j',
    os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'blizzard.j')
]
```

### 错误处理

```python
try:
    # 加载并解析 blizzard.j
    self._load_blizzard_script(path)
    return True
except Exception as e:
    logger.warning(f"blizzard.j 加载失败: {e}")
    return False
```

## 与现有代码的关系

### 与 _load_constants() 的对比

| 功能 | _load_constants() | load_blizzard() |
|------|------------------|-----------------|
| 目标文件 | common.j | blizzard.j |
| 解析方式 | 正则提取常量 | 完整 JASS 解析器 |
| 解析内容 | 常量名和值 | 函数、变量、配置等 |
| 自动/手动 | 自动（初始化时） | 手动（按需） |
| 错误处理 | 静默失败 | 记录警告 |

### 修改文件

1. `src/jass_runner/vm/jass_vm.py` - 添加 `load_blizzard()` 方法和相关逻辑
3. `tests/vm/test_jass_vm.py` - 添加加载测试

## 测试场景

1. **正常加载**：`vm.load_blizzard()` 成功加载
2. **自定义路径**：`vm.load_blizzard('path/to/blizzard.j')` 成功加载
3. **加载失败**：文件不存在，记录警告，返回 False，不中断
4. **执行顺序**：blizzard.j 函数可在用户脚本中调用
5. **不加载也能运行**：不调用 load_blizzard() 时，用户脚本独立运行

## 使用示例

```python
from jass_runner.vm.jass_vm import JassVM

vm = JassVM()

# 加载 blizzard.j（可选）
vm.load_blizzard()

# 加载用户脚本
vm.load_script("""
function main takes nothing returns nothing
    // 使用 blizzard.j 中的函数
    call BJDebugMsg("Hello")
endfunction
""")

# 执行
vm.execute()
```

## CLI 支持（可选扩展）

未来可考虑添加命令行选项：

```bash
python -m jass_runner script.j --blizzard    # 自动加载 blizzard.j
python -m jass_runner script.j --blizzard path/to/custom.j  # 指定路径
```

此设计待实现。
