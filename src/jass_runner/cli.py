"""JASS 运行器的命令行接口。

此模块包含命令行接口实现，用于执行 JASS 脚本。
"""

import argparse
import sys
import logging
from .vm.jass_vm import JassVM


def create_parser():
    """创建参数解析器。"""
    parser = argparse.ArgumentParser(
        description='JASS 脚本运行器 - 在魔兽争霸 III 外部执行 JASS 脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s script.j          # 执行 JASS 脚本
  %(prog)s script.j --simulate 30  # 执行并模拟 30 秒
  %(prog)s script.j --no-timers   # 禁用计时器系统执行
  %(prog)s --version         # 显示版本
        """
    )

    parser.add_argument(
        'script',
        help='要执行的 JASS 脚本文件'
    )

    parser.add_argument(
        '--simulate',
        type=float,
        default=0.0,
        help='模拟计时器执行 N 秒（默认: 0，不模拟）'
    )

    parser.add_argument(
        '--no-timers',
        action='store_true',
        help='禁用计时器系统'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='启用详细日志'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='仅显示错误输出'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='JASS 运行器 1.0.0'
    )

    return parser


def setup_logging(verbose: bool, quiet: bool):
    """根据详细程度设置日志。"""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format='%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def main():
    """主 CLI 入口点。"""
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose, args.quiet)

    try:
        # 创建并运行虚拟机
        vm = JassVM(enable_timers=not args.no_timers)
        vm.load_file(args.script)
        vm.execute()

        if args.simulate > 0:
            vm.run_simulation(args.simulate)

        logging.info("执行成功完成")
        return 0

    except FileNotFoundError:
        logging.error(f"脚本文件未找到: {args.script}")
        return 1
    except Exception as e:
        logging.error(f"执行脚本时出错: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
