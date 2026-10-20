import sys
import httpx
from pathlib import Path
from mini_agent.mcp import MCPClient,register_mcp_tools,MCPTool
from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import (
    ToolRegistry,
    CurrentTimeTool,
    ReadFileTool,ListFilesTool,WriteFileTool,CalculatorTool
)
from mini_agent.memory import MemoryManager
ROOT=Path(__file__).resolve().parents[2]
SERVER_COMMAND=[sys.executable,str(ROOT/"mcp_servers"/"calculator_server.py")]
def stream_print(piece):
    sys.stdout.write(piece)
    sys.stdout.flush()
def handle_command(text,memory,registry,llm):
    """处理 / 命令：只改本地状态，不与 LLM 对话"""
    command=text.split()[0].lower()
    if command=="/help":
        print("── 可用命令 ──")
        print("  /help     显示这个帮助")
        print("  /stats    会话统计（工具 / 消息 / token / usage）")
        print("  /tools    列出已注册的工具（含 MCP 标记）")
        print("  /clear    清空对话（保留 system 提示词）")
        print("  exit      退出")
    elif command=="/stats":
        print("── 会话统计 ──")
        print(f"  工具 ({len(registry.tools)}): {', '.join(registry.tools.keys())}")
        print(f"  消息: {len(memory.messages)} 条 | 压缩: {memory.compress_count} 次")
        print(f"  {memory.stats()}")
        usage=getattr(llm,"last_usage",None)
        print(f"  上次 API usage: {usage if usage else '（暂无）'}")
    elif command=="/tools":
        print(f"── 已注册工具（{len(registry.tools)}）──")
        for tool in registry.tools.values():
            tag="[MCP]" if isinstance(tool,MCPTool) else "[本地]"
            print(f"  {tag:<6} {tool.name:<16} {tool.description}")
    elif command=="/clear":
        keep=[m for m in memory.messages[:1] if m.get("role")=="system"]
        memory.messages[:]=keep
        memory.compress_count=0
        print("会话已清空（保留 system 提示词）")
    else:
        print(f"未知命令：{command}（试试 /help）")
def main(budget=None,use_mcp=True):
    llm=DeepSeekLLM()
    registry=ToolRegistry()
    registry.register(CurrentTimeTool())
    registry.register(ReadFileTool())
    registry.register(ListFilesTool())
    registry.register(WriteFileTool())

    mcp_client=None
    if use_mcp:
        mcp_client=MCPClient(SERVER_COMMAND)
        mcp_client.start()
        mcp_client.initialize()
        print(f"mcp已连接：{mcp_client.server_info}")
        count=register_mcp_tools(registry,mcp_client)
        print(f"已从 MCP 接入 {count} 个工具")
    else:
        # 降级模式：没有 MCP 时，本地 calculator 顶上（本尊回家）
        registry.register(CalculatorTool())
        print("未挂载 MCP（降级模式：本地工具）")
    print(f"注册表: {list(registry.tools.keys())}")
    agent=Agent(llm,registry)
    memory=MemoryManager(llm,max_tokens=budget) if budget else MemoryManager(llm)
    memory.add({
        "role":"system",
        "content":"你是 MiniAgent，一个可以使用工具的 AI 助手。"
                  "需要做数学计算时，必须调用 calculator 工具，不要自己心算；"
                  "需要知道当前时间时，必须调用 get_current_time 工具；"
                  "需要查看项目文件内容时，调用 read_file 工具，不要猜测；"
                  "需要浏览项目目录时，调用 list_files 工具；"
                  "需要创建或写入文件时，调用 write_file 工具（写入前会请求用户确认）。"
                  "回答要简洁但不遗漏：用户问了几个问题，就完整回答几个。",
    })

    print("agent已启动")
    print("输入 /help查看命令，输入exit退出")
    try:
       while True:
         user_input=input("\n用户:" ).strip()
         if user_input in ("exit","/exit"):
           print("agent已结束")
           break
         if user_input.startswith("/"):
             handle_command(user_input,memory,registry,llm)
             continue
         before = len(memory.messages)          # ← 注意：先记位置，再追加
         memory.add({"role":"user","content":user_input})
         print("agent:",end="",flush=True)
         try:
             message=agent.run(memory,on_token=stream_print)
         except (httpx.TimeoutException,httpx.NetworkError):
             print()
             print("  [网络问题] 超时或连接中断——这句没答完，重试一次吧")
             del memory.messages[before:]        # 回滚这轮，别留半截历史
             continue
         except httpx.HTTPStatusError as err:
             print()
             print(f"  [API 错误] HTTP {err.response.status_code}：{err.response.text[:200]}")
             del memory.messages[before:]
             continue
         print() 
         print("agent:",end="",flush=True)
         message=agent.run(memory,on_token=stream_print)
         print()
         for new_messages in memory.messages[before:]:
             tool_calls=new_messages.get("tool_calls")
             if tool_calls:
                 for tool_call in tool_calls:
                     print(f"  [调用工具] {tool_call['function']['name']}"
                          f" 参数: {tool_call['function']['arguments']}")
         print()   
         '''          
         for ever_messages in messages:
             print(ever_messages)
         '''
        
         print(f"  [{memory.stats()}]")
    finally:
       # try finally语法：无论try内代码怎么退出（报错，正常运行，包括 Ctrl+C），都会执行finally内代码：服务器进程都要回收
       if mcp_client is not None:
           mcp_client.close()
if __name__ == "__main__":
    main()
