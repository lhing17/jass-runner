# TimerDialog Native 函数实现设计文档

## 日期
2026-03-10

## 概述
实现 JASS 中的 timerdialog（计时器对话框）handle 类型和相关的 5 个核心 native 函数。

## 背景
在魔兽争霸 III 中，timerdialog 用于显示一个与计时器关联的对话框，常用于倒计时、游戏时间显示等场景。

## 设计目标
1. 实现 timerdialog handle 类型
2. 实现 5 个核心 native 函数
3. 所有操作记录日志（模拟行为，不实际显示 UI）

## 实现方案

### 1. TimerDialog Handle 类

**文件**: `src/jass_runner/natives/timerdialog.py`

```python
class TimerDialog(Handle):
    """计时器对话框 handle"""
    def __init__(self, handle_id: str, timer):
        super().__init__(handle_id, "timerdialog")
        self.timer = timer          # 关联的 timer
        self.title = ""             # 标题
        self.displayed = False      # 是否显示
```

### 2. Native 函数实现

**文件**: `src/jass_runner/natives/timerdialog_natives.py`

| 函数名 | 签名 | 功能 | 日志输出 |
|--------|------|------|----------|
| CreateTimerDialog | `takes timer t returns timerdialog` | 创建 timerdialog，关联指定 timer | `[CreateTimerDialog] 创建 timerdialog: {handle_id} (关联 timer: {timer_id})` |
| DestroyTimerDialog | `takes timerdialog whichDialog returns nothing` | 销毁 timerdialog | `[DestroyTimerDialog] 销毁 timerdialog: {handle_id}` |
| TimerDialogSetTitle | `takes timerdialog whichDialog, string title returns nothing` | 设置标题 | `[TimerDialogSetTitle] 设置 timerdialog {handle_id} 标题为: "{title}"` |
| TimerDialogDisplay | `takes timerdialog whichDialog, boolean display returns nothing` | 设置显示/隐藏 | `[TimerDialogDisplay] 显示 timerdialog: {handle_id}` 或 `[TimerDialogDisplay] 隐藏 timerdialog: {handle_id}` |
| IsTimerDialogDisplayed | `takes timerdialog whichDialog returns boolean` | 返回显示状态 | 无日志，返回布尔值 |

### 3. HandleManager 扩展

**文件**: `src/jass_runner/natives/manager.py`

添加方法：
- `create_timerdialog(timer)` - 创建 timerdialog，返回 handle id
- `get_timerdialog(handle_id)` - 根据 id 获取 TimerDialog 实例

### 4. NativeFactory 注册

**文件**: `src/jass_runner/natives/factory.py`

导入并注册 5 个 native 函数：
- CreateTimerDialog
- DestroyTimerDialog
- TimerDialogSetTitle
- TimerDialogDisplay
- IsTimerDialogDisplayed

### 5. 类型层级

`timerdialog` 继承自 `handle`，在类型系统中与其他 handle 类型同级。

## 测试策略

1. 单元测试：每个 native 函数的独立测试
2. 集成测试：创建 → 设置标题 → 显示 → 销毁 的完整流程测试

## 日志示例

```
[CreateTimerDialog] 创建 timerdialog: timerdialog_1 (关联 timer: timer_1)
[TimerDialogSetTitle] 设置 timerdialog timerdialog_1 标题为: "剩余时间"
[TimerDialogDisplay] 显示 timerdialog: timerdialog_1
[DestroyTimerDialog] 销毁 timerdialog: timerdialog_1
```

## 后续扩展（可选）

如需完整实现，可添加以下 native 函数：
- TimerDialogSetTitleColor
- TimerDialogSetTimeColor
- TimerDialogSetSpeed
- TimerDialogSetRealTimeRemaining
