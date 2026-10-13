import sys
from pathlib import Path

from mini_agent.mcp.client import MCPClient

ROOT = Path(__file__).resolve().parents[1]
server_command = [sys.executable, str(ROOT / "mcp_servers" / "calculator_server.py")]

client = MCPClient(server_command)
# ── 1. 启动 + 握手 ──
client.start()
info = client.initialize()
print("握手完成:")
print("  服务器信息:", client.server_info)
print("  协议版本:", info.get("protocolVersion"))
print()

# ── 2. 工具发现 ──
tools = client.list_tools()
print("发现工具:")
for tool in tools:
    print("  -", tool["name"], "|", tool["description"])
print()
# ── 3. 工具调用 ──
result = client.call_tool("calculator", {"a": 123, "b": 456, "operation": "multiply"})
print("调用结果:", result["content"][0]["text"])
assert result["content"][0]["text"] == "56088"

# ── 4. 业务错误（isError 正常返回）──
result = client.call_tool("calculator", {"a": 5, "b": 0, "operation": "divide"})
print("除零结果:", result["content"][0]["text"], "| isError:", result["isError"])
assert result["isError"] is True

# ── 5. 协议错误（未知工具 → 抛异常）──
try:
    client.call_tool("weather", {})
    print("没有抛出异常，异常！")
except RuntimeError as error:
    print("协议错误已捕获:", error)
print()

# ── 收尾 ──
client.close()
print("✓ MCPClient 全部场景通过")