from mini_agent.agent import Agent
from mini_agent.tools import ToolRegistry, calculator, calculator_schema
from mock_llm import MockLLM

registry = ToolRegistry()
registry.register("calculator", calculator, calculator_schema)
'''
print("场景 1: 回放工具调用")
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
                    "arguments": '{"a": 123, "b": 456, "operation": "multiply"}',
                },
            }
        ],
    },
    {"role": "assistant", "content": "计算完成，结果是 56088。"},
]

mock = MockLLM(responses)
agent = Agent(mock, registry)

messages = [{"role": "user", "content": "帮我算 123*456"}]
final = agent.run(messages)
print("最终回答:", final["content"])
print("LLM 被调用次数:", mock.call_count)
print("消息条数:", len(messages))
for message in messages:
    print(message)
print()

assert final["content"] == "计算完成，结果是 56088。"
assert mock.call_count == 2
assert len(messages) == 4
assert messages[2]["role"] == "tool"
assert messages[2]["content"] == "56088"
print("场景 1 通过 ✓")
print()

print("场景 2: 未知工具")

responses = [
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {"id": "call_002", "type": "function",
             "function": {"name": "weather", "arguments": "{}"}},
        ],
    },
    {"role": "assistant", "content": "抱歉，我没有天气工具。"},
]

mock = MockLLM(responses)
agent = Agent(mock, registry)
messages = [{"role": "user", "content": "北京天气怎么样"}]
final = agent.run(messages)
for message in messages:
    print(message)
print("工具消息:", messages[2]["content"])
#assert "错误" in messages[2]["content"]
assert "找不到工具" in messages[2]["content"]

print("场景 2 通过 ✓")

print()

print("场景 3: 坏 JSON 参数")

responses = [
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {"id": "call_003", "type": "function",
             "function": {"name": "calculator", "arguments": "{a: 123???"}},
        ],
    },
    {"role": "assistant", "content": "参数格式有误。"},
]

mock = MockLLM(responses)
agent = Agent(mock, registry)
messages = [{"role": "user", "content": "随便"}]
final = agent.run(messages)
for message in messages:
    print(message)
print("工具消息:", messages[2]["content"])
assert "错误" in messages[2]["content"]
print("场景 3 通过 ✓")
print()
'''
print("场景 4: 死循环保护")

tool_call_response = {
    "role": "assistant",
    "content": None,
    "tool_calls": [
        {"id": "call_loop", "type": "function",
         "function": {"name": "calculator",
                      "arguments": '{"a": 1, "b": 1, "operation": "add"}'}},
    ],
}

mock = MockLLM([tool_call_response] * 5)
agent = Agent(mock, registry)
messages = [{"role": "user", "content": "死循环测试"}]

try:
    agent.run(messages, max_iterations=3)
    print("没有触发保护 ✗")
except RuntimeError as error:
    print("成功拦截:", error)
    print("场景 4 通过 ✓")