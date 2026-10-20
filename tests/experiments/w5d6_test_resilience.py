import sys
from pathlib import Path

from mini_agent.mcp import MCPClient, MCPConnectionError, register_mcp_tools
from mini_agent.tools import ToolRegistry

ROOT = Path(__file__).resolve().parents[1]
server_command = [sys.executable, str(ROOT / "mcp_servers" / "calculator_server.py")]

client = MCPClient(server_command)
client.start()
client.initialize()
tools = client.list_tools()
print("服务器提供的工具:", [t["name"] for t in tools])
assert "roll_dice" in [t["name"] for t in tools]

dice = client.call_tool("roll_dice", {})
value = int(dice["content"][0]["text"])
print("掷骰子:", value)
assert 1 <= value <= 6
print() 
# ── 2. 服务器暴毙：报错清晰（连接层错误）──
client.process.kill()
client.process.wait()
try:
    client.call_tool("calculator", {"a": 1, "b": 2, "operation": "add"})
    print("没有报错，异常！")
except MCPConnectionError as error:
    print("连接层错误已捕获:", error)
print()
# ── 3. 手动重启：恢复服务 ──
client.restart()
result = client.call_tool("calculator", {"a": 1, "b": 2, "operation": "add"})
print("重启后调用:", result["content"][0]["text"])
assert result["content"][0]["text"] == "3"
print()
# ── 4. 适配器自愈：再杀一次，MCPTool 自己重连 ──
registry = ToolRegistry()
register_mcp_tools(registry, client)
tool = registry.get("calculator")

client.process.kill()
client.process.wait()
print("服务器再次被击杀；通过适配器调用（应自动自愈）…")
result = tool.run(a=10, b=20, operation="add")
print("适配器自愈后结果:", result)
assert result == "30"
print()
# ── 5. 启动失败：错误命令 → 握手时清晰报错 ──
bad_client = MCPClient([sys.executable, "no_such_server.py"])
bad_client.start()
try:
    bad_client.initialize()
    print("没有报错，异常！")
except MCPConnectionError as error:
    print("启动失败已捕获:", error)
bad_client.close()
print()

client.close()
print("✓ 韧性演练全部通过")