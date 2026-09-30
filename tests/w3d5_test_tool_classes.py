import json

from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import (
    ToolRegistry,
    CalculatorTool, CurrentTimeTool,
    ReadFileTool, ListFilesTool, WriteFileTool,
)
from mock_llm import MockLLM
registry = ToolRegistry()
registry.register(CalculatorTool())
registry.register(CurrentTimeTool())
registry.register(ReadFileTool())
registry.register(ListFilesTool())
registry.register(WriteFileTool())
print("已注册工具:", list(registry.tools.keys()))
print()
print("calculator 的 schema（确认与旧格式一致）:")
print(json.dumps(registry.get_schemas()[0], ensure_ascii=False, indent=2))
print()
responses = [
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "id": "call_001",
                "type": "function",
                "function": {
                    "name": "calculator",
                    "arguments": '{"a": 7, "b": 6, "operation": "multiply"}',
                },
            }
        ],
    },
    {"role": "assistant", "content": "7 × 6 = 42"},
]
mock = MockLLM(responses)
agent = Agent(mock, registry)
messages = [{"role": "user", "content": "7*6"}]
final = agent.run(messages)
print("mock 回答:", final["content"])
print("工具结果:", messages[2]["content"])
assert final["content"] == "7 × 6 = 42"
assert messages[2]["content"] == "42"
print("mock 回归通过 ✓")
print()
llm = DeepSeekLLM()
agent2 = Agent(llm, registry)
messages2 = [{"role": "user", "content": "读一下 pyproject.toml，告诉我 Python 版本要求"}]
final2 = agent2.run(messages2)
print("真实回答:", final2["content"])