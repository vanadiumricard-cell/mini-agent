"""MiniAgent 命令行入口：只做"解析参数 + 分发子命令"，业务在 chat.py。

用法：
  mini-agent chat                 启动交互式对话
  mini-agent chat --no-mcp        降级模式（只用本地工具）
  mini-agent chat --budget 4000   自定义 context 预算
  mini-agent --version            查看版本
"""
import argparse
def build_parser():
    parser = argparse.ArgumentParser(
        prog="mini-agent",
        description="MiniAgent —— 一个可以使用工具的 AI Agent",
    )
    parser.add_argument("-V", "--version", action="version", version="mini-agent 1.0.0")

    subparsers = parser.add_subparsers(dest="command")

    chat_parser = subparsers.add_parser("chat", help="启动交互式对话")
    chat_parser.add_argument(
        "--budget", type=int, default=None,
        help="context 预算（token），默认取模型窗口的 75%%",
    )
    chat_parser.add_argument(
        "--no-mcp", action="store_true",
        help="不挂载 MCP 服务器（降级：只用本地工具）",
    )
    return parser
def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "chat":
        from mini_agent.chat import main as chat_main   # 按需导入：看 --help 时不用加载整个栈
        chat_main(budget=args.budget, use_mcp=not args.no_mcp)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()