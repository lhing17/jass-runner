
import os
import sys
import logging
from jass_runner.vm.jass_vm import JassVM

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_war3map():
    """加载并执行 resources/war3map.j 文件"""
    
    # 确定文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    war3map_path = os.path.join(project_root, 'resources', 'war3map.j')
    
    if not os.path.exists(war3map_path):
        logger.error(f"找不到文件: {war3map_path}")
        return

    logger.info(f"正在加载脚本: {war3map_path}")
    
    try:
        # 创建虚拟机实例
        vm = JassVM(enable_timers=True)
        
        vm.load_blizzard()
        # 加载脚本文件
        vm.load_file(war3map_path)
        
        # 执行脚本 (默认执行 main 函数)
        logger.info("开始执行脚本...")
        vm.execute()
        
        # 运行模拟循环 (可选，如果脚本中有计时器)
        # 这里模拟运行 5 秒钟
        logger.info("开始模拟运行...")
        vm.run_simulation(seconds=5.0)
        
    except Exception as e:
        logger.error(f"执行过程中发生错误: {e}", exc_info=True)

if __name__ == "__main__":
    # 添加 src 目录到 Python 路径，以便能导入 jass_runner
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(os.path.dirname(current_dir), 'src')
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
        
    run_war3map()
