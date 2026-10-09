from mini_agent.context import estimate_messages_tokens
from mini_agent.memory import MemoryManager
from mock_llm import MockLLM
print("== MemoryManager 基本接口 ==")
mock = MockLLM([{"role": "assistant", "content": "【模拟摘要】"}])
memory = MemoryManager(mock, max_tokens=2000)

memory.add({"role": "system", "content": "你是 MiniAgent。"})
memory.add({"role": "user", "content": "我叫小明。"})
memory.add({"role": "assistant", "content": "记住了。"})
for i in range(1, 11):
    memory.add({"role": "user", "content": f"闲聊 {i}：" + "内容" * 100})
    memory.add({"role": "assistant", "content": f"回应 {i}：" + "回应" * 100})

print("压缩前:", memory.stats())
ok = memory.compress()
print("compress() →", ok, "| 压缩次数:", memory.compress_count)
print("压缩后:", memory.stats())
print("视图首三条:", [m["role"] for m in memory.context()[:3]])
assert ok is True
assert memory.compress_count == 1

ok2 = memory.compress()      # 已经低于预算，不该再压
assert ok2 is False
assert memory.compress_count == 1
print("✓ 接口正确，且不会重复压缩")
print()
# ── 2. 接入 Agent 循环（mock 全链路）──
print("== Agent + MemoryManager 集成 ==")
from mini_agent.agent import Agent
from mini_agent.tools import ToolRegistry, CalculatorTool

loop_responses = [
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [{"id": "c1", "type": "function",
                        "function": {"name": "calculator",
                                     "arguments": '{"a": 6, "b": 7, "operation": "multiply"}'}}],
    },
    {"role": "assistant", "content": "6 × 7 = 42"},
]
mock2 = MockLLM(loop_responses)
registry = ToolRegistry()
registry.register(CalculatorTool())
agent = Agent(mock2, registry)
memory2 = MemoryManager(mock2, max_tokens=100000)
memory2.add({"role": "user", "content": "6*7 等于几？"})
final = agent.run(memory2)
print("回答:", final["content"])
print("存储结构:", [m["role"] for m in memory2.messages])
assert final["content"] == "6 × 7 = 42"
assert mock2.call_count == 2
print("✓ Agent 循环走通，消息全落在 memory 里")
print()
# ── 3. 真实 API：完整流程（和 chat.py 同款组装）──
print("== 真实流程冒烟 ==")
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import CurrentTimeTool

llm = DeepSeekLLM()
registry2 = ToolRegistry()
registry2.register(CalculatorTool())
registry2.register(CurrentTimeTool())
agent2 = Agent(llm, registry2)
memory3 = MemoryManager(llm)
memory3.add({"role": "system", "content": "你是 MiniAgent，一个可以使用工具的 AI 助手。"})
memory3.add({"role": "user", "content": "帮我算 12*34，然后告诉我现在几点"})
final3 = agent2.run(memory3)
print("回答:", final3["content"])
print("油表:", memory3.stats())