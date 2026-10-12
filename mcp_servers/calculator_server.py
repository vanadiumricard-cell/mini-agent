"""最小 MCP 服务器：把 CalculatorTool 按 MCP 协议暴露出去。

实现的 MCP 最小子集：
  initialize   → 握手（版本、能力、服务器信息）
  tools/list   → 工具发现
  tools/call   → 工具调用（执行并返回 content 块）

注意：stdout 是协议专线，任何调试信息只能走 stderr！
"""
import json
import sys
from mini_agent.tools import CalculatorTool, ToolRegistry
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
PROTOCOL_VERSION = "2026-10-12"
registry = ToolRegistry()
registry.register(CalculatorTool())
def ok(request_id, result):
    return {"jsonrpc": "2.0", "id": request_id, "result": result}
def error(request_id, code, message):
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}
def tool_to_mcp(tool):
    """把我们的 Tool 转成 MCP 格式（格式转换是服务器的职责，工具本身不知情）"""
    return {
        "name": tool.name,
        "description": tool.description,
        "inputSchema": {
            "type": "object",
            "properties": tool.parameters,
            "required": tool.required,
        },
    }
def handle(message):
    if "id" not in message:#通知，不需要响应
        return None
    request_id= message["id"]
    method=message.get("method")
    params=message.get("params",{})
    if method=="initialize":
        return ok(request_id,{"protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},     # 声明：我提供 tools 能力
            "serverInfo": {"name": "mini-agent-calculator", "version": "0.1.0"},})
    if method=="tools/list":
        tools=[tool_to_mcp(tool) for tool in registry.tools.values()]
        return ok (request_id,{"tools":tools})
    if method=="tools/call":
         name = params.get("name")
         arguments = params.get("arguments", {})
         tool = registry.get(name)
         if tool is None:
            # 协议层错误：请求本身不合法
            return error(request_id, -32602, f"未知工具: {name}")
         try:
            result = tool.run(**arguments)
            return ok(request_id, {"content": [{"type": "text", "text": str(result)}]})
         except Exception as err:
            # 业务层错误：执行失败，标记 isError 让调用方处理
            return ok(request_id, {
                "content": [{"type": "text", "text": f"工具执行错误: {err}"}],
                "isError": True,
            })
    return error(request_id, -32601, f"未知方法: {method}")
def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        response = handle(message)
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)
if __name__ == "__main__":
    main()