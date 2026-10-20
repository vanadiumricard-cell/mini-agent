import json
import sys
from pathlib import Path

from mini_agent.mcp import MCPClient, register_mcp_tools
from mini_agent.tools import CalculatorTool, ToolRegistry

ROOT = Path(__file__).resolve().parents[1]
server_command = [sys.executable, str(ROOT / "mcp_servers" / "calculator_server.py")]

client = MCPClient(server_command)
client.start()
client.initialize()

# ── 1. 把远程工具接进注册表 ──
registry = ToolRegistry()
count = register_mcp_tools(registry, client)
print(f"从 MCP 接入了 {count} 个工具")
print("注册表内容:", list(registry.tools.keys()))
print()

# ── 2. 远程工具在注册表里"长得和本地工具一模一样" ──
remote_schema = registry.get_schemas()[0]
print("它的 schema（Registry 视角）:")
print(json.dumps(remote_schema, ensure_ascii=False, indent=2))
print()

# ── 3. 绕场一周的无损证明！──
local_schema = CalculatorTool().to_schema()
print("远程工具的 schema == 本地 CalculatorTool 的 schema ?", remote_schema == local_schema)
assert remote_schema == local_schema
print()

# ── 4. 直接执行（走适配器 → MCP 协议 → 另一个进程）──
tool = registry.get("calculator")
result = tool.run(a=123, b=456, operation="multiply")
print("远程执行结果:", result)
assert result == "56088"
print()

# ── 5. 业务错误：isError 文本作为数据返回 ──
result = tool.run(a=5, b=0, operation="divide")
print("远程执行（除零）:", result)
assert "除数不能为零" in result
print()

client.close()
print("✓ MCPTool 适配器全部场景通过")