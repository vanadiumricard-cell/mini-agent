import json
import sys

from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.memory import MemoryManager
from mini_agent.tools import CalculatorTool, CurrentTimeTool, ToolRegistry


def stream_print(piece):
    sys.stdout.write(piece)
    sys.stdout.flush()


llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register(CalculatorTool())
registry.register(CurrentTimeTool())
agent = Agent(llm, registry)

# ── 1. 底层验证：流式下 tool_calls 拼装是否完整 ──
print("=== 1. 流式 tool_calls 拼装 ===")
message = llm.chat(
    [{"role": "user", "content": "帮我算 12*34"}],
    tools=registry.get_schemas(),
    on_token=stream_print,
)
print()
print("拼装出的 message:")
print(json.dumps(message, ensure_ascii=False, indent=2))

tool_calls = message.get("tool_calls")
assert tool_calls, "没有拼出 tool_calls！（模型可能直接心算了，重跑一次）"
call = tool_calls[0]
assert call["function"]["name"] == "calculator"
args = json.loads(call["function"]["arguments"])     # 碎片必须拼成合法 JSON
print("拼装出的参数:", args)
print()
# ── 2. 全链路：多轮工具调用 + 打字机 ──
print("=== 2. Agent 全链路（流式打字机）===")
memory = MemoryManager(llm)
memory.add({"role": "user", "content": "帮我算 123*456，然后告诉我现在几点"})
final = agent.run(memory, on_token=stream_print)
print()
print()

tool_msgs = [m for m in memory.messages if m.get("role") == "tool"]
print("工具执行结果:", [m["content"] for m in tool_msgs])
assert any("56088" in str(m.get("content")) for m in tool_msgs)
assert final["content"]
print("✓ 流式 + 工具调用全链路通过")