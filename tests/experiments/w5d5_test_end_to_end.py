import sys
from pathlib import Path

from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.mcp import MCPClient, register_mcp_tools
from mini_agent.memory import MemoryManager
from mini_agent.tools import ToolRegistry

ROOT = Path(__file__).resolve().parents[1]
server_command = [sys.executable, str(ROOT / "mcp_servers" / "calculator_server.py")]

client = MCPClient(server_command)
client.start()
client.initialize()

registry = ToolRegistry()
register_mcp_tools(registry, client)

llm = DeepSeekLLM()
agent = Agent(llm, registry)
memory = MemoryManager(llm)
memory.add({"role": "user", "content": "帮我算 123*456 等于多少"})

final = agent.run(memory)
print("回答:", final["content"])

tool_messages = [m for m in memory.messages if m.get("role") == "tool"]
print("工具结果:", tool_messages[0]["content"] if tool_messages else "（没有调用工具）")
assert tool_messages, "Agent 没有调用工具"
assert tool_messages[0]["content"] == "56088"

client.close()
print("✓ 端到端打通：Agent → 适配器 → MCP 协议 → 另一个进程 → 返回")