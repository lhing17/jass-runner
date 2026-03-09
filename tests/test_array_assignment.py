"""简化测试 - 验证数组赋值功能是否正常。

使用方法:
    python test_array_assignment.py

如果测试通过，会显示:
    udg_equip_count: 2
    udg_equip_item_type_id[1] = 1228025904
    udg_equip_item_type_id[2] = 1228025905
"""

import sys
sys.path.insert(0, 'src')

from jass_runner.vm.jass_vm import JassVM
from jass_runner.utils import fourcc_to_int

test_code = '''
globals
    integer array udg_equip_item_type_id
    integer udg_equip_count
endglobals

function AddEquipment takes integer item_type_id returns nothing
    local integer id
    set id = udg_equip_count + 1
    set udg_equip_count = id
    set udg_equip_item_type_id[id] = item_type_id
endfunction

function InitEquipmentData takes nothing returns nothing
    set udg_equip_count = 0
    call AddEquipment('I200')
    call AddEquipment('I201')
endfunction

function main takes nothing returns nothing
    call InitEquipmentData()
endfunction
'''

print("=" * 60)
print(fourcc_to_int('I202'))
print("数组赋值简化测试")
print("=" * 60)
print()

vm = JassVM(enable_timers=False)
vm.load_script(test_code)
vm.execute()

count = vm.interpreter.global_context.get_variable('udg_equip_count')
print(f'udg_equip_count: {count}')

success = True
for i in range(1, count + 1):
    val = vm.interpreter.global_context.get_array_element('udg_equip_item_type_id', i)
    expected = fourcc_to_int('I200' if i == 1 else 'I201')
    status = "OK" if val == expected else "FAIL"
    print(f'{status} udg_equip_item_type_id[{i}] = {val} (预期: {expected})')
    if val == 0:
        success = False
        print(f'  错误: udg_equip_item_type_id[{i}] 的值为0!')

print()
if success:
    print("测试通过!")
else:
    print("测试失败! 数组赋值为0的问题仍然存在。")
