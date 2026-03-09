"""Hashtable 集成测试"""

import pytest
from jass_runner.vm.jass_vm import JassVM


class TestHashtableIntegration:
    """测试 Hashtable 完整工作流程"""

    def test_hashtable_basic_workflow(self):
        """测试 hashtable 基础工作流程"""
        script = '''
function testHashtable takes nothing returns nothing
    local hashtable ht = InitHashtable()

    call SaveInteger(ht, 0, 0, 42)
    call SaveReal(ht, 0, 0, 3.14)
    call SaveBoolean(ht, 0, 1, true)
    call SaveStr(ht, 0, 2, "hello")

    call DisplayTextToPlayer(Player(0), 0, 0, I2S(LoadInteger(ht, 0, 0)))
    call DisplayTextToPlayer(Player(0), 0, 0, R2S(LoadReal(ht, 0, 0)))
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

    def test_hashtable_with_unit(self):
        """测试 hashtable 存储单位"""
        script = '''
function testHashtableWithUnit takes nothing returns nothing
    local hashtable ht = InitHashtable()
    local unit u = CreateUnit(Player(0), 'Hpal', 0, 0, 0)

    call SaveUnitHandle(ht, 0, 0, u)

    local unit loaded = LoadUnitHandle(ht, 0, 0)
    if loaded != null then
        call DisplayTextToPlayer(Player(0), 0, 0, "Unit loaded successfully")
    endif
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

    def test_hashtable_flush(self):
        """测试 hashtable 清空"""
        script = '''
function testHashtableFlush takes nothing returns nothing
    local hashtable ht = InitHashtable()

    call SaveInteger(ht, 0, 0, 42)
    call FlushParentHashtable(ht)

    if LoadInteger(ht, 0, 0) == 0 then
        call DisplayTextToPlayer(Player(0), 0, 0, "Flush successful")
    endif
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

    def test_hashtable_have_saved(self):
        """测试 HaveSaved 函数"""
        script = '''
function testHaveSaved takes nothing returns nothing
    local hashtable ht = InitHashtable()

    call SaveInteger(ht, 0, 0, 42)

    if HaveSavedInteger(ht, 0, 0) then
        call DisplayTextToPlayer(Player(0), 0, 0, "Integer exists")
    endif

    if not HaveSavedReal(ht, 0, 0) then
        call DisplayTextToPlayer(Player(0), 0, 0, "Real does not exist")
    endif
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)

    def test_hashtable_multiple_types_same_key(self):
        """测试同一键下存储不同类型"""
        script = '''
function testMultipleTypes takes nothing returns nothing
    local hashtable ht = InitHashtable()

    call SaveInteger(ht, 0, 0, 42)
    call SaveReal(ht, 0, 0, 3.14)
    call SaveBoolean(ht, 0, 0, true)

    if LoadInteger(ht, 0, 0) == 42 then
        call DisplayTextToPlayer(Player(0), 0, 0, "Integer OK")
    endif
    if LoadReal(ht, 0, 0) == 3.14 then
        call DisplayTextToPlayer(Player(0), 0, 0, "Real OK")
    endif
    if LoadBoolean(ht, 0, 0) then
        call DisplayTextToPlayer(Player(0), 0, 0, "Boolean OK")
    endif
endfunction
'''
        vm = JassVM(enable_timers=False)
        vm.run(script, load_blizzard=False)
