# JASS 运行器用户指南

## 安装

```bash
# 从本地源码安装
pip install -e .

# 或直接运行而不安装
python -m jass_runner --help
```

## 基本用法

### 执行 JASS 脚本

```bash
jass-runner script.j
```

### 执行并带计时器模拟

```bash
jass-runner script.j --simulate 30
```

### 禁用计时器系统

```bash
jass-runner script.j --no-timers
```

### 详细输出

```bash
jass-runner script.j --verbose
```

## JASS 语言支持

运行器支持 JASS 语法的子集：

- 函数声明：`function name takes nothing returns nothing`
- 局部变量：`local type name`
- 原生函数调用：`call NativeFunction(args)`
- 基本控制流（if/else、循环）
- 计时器操作

## 原生函数模拟

原生函数通过控制台输出模拟：

- `DisplayTextToPlayer(player, x, y, message)` - 输出消息到控制台
- `KillUnit(unit)` - 记录单位死亡
- `CreateTimer()`、`TimerStart()` 等 - 模拟计时器操作

## 计时器系统

计时器系统使用基于帧的模拟：

- 默认：30 FPS（每帧 0.033 秒）
- 允许快速推进长时间模拟
- 支持一次性计时器和周期性计时器
- 计时器可以暂停和恢复

## 示例

创建文件 `test.j`：

```jass
function main takes nothing returns nothing
    call DisplayTextToPlayer(0, 0, 0, "Hello from JASS!")

    local timer t = CreateTimer()
    call TimerStart(t, 2.0, false, function main)
endfunction
```

运行它：

```bash
jass-runner test.j --simulate 5
```

## 扩展

有关扩展原生函数的信息，请参阅 [docs/natives/README.md](docs/natives/README.md)。
有关计时器系统的详细信息，请参阅 [docs/timer/README.md](docs/timer/README.md)。
