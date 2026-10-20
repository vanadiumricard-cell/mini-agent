import json

import pytest
from mock_llm import MockLLM

from mini_agent.agent import Agent
from mini_agent.memory import MemoryManager
from mini_agent.tools import CalculatorTool, ToolRegistry


def make_agent(responses):
    mock = MockLLM(responses)
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    agent = Agent(mock, registry)
    memory = MemoryManager(mock)
    return agent, memory, mock


def tool_call_response(name, arguments, call_id="c1"):
    return {"role": "assistant", "content": None,
            "tool_calls": [{"id": call_id, "type": "function",
                            "function": {"name": name,
                                         "arguments": json.dumps(arguments)}}]}


def test_agent_tool_loop():
    responses = [
        tool_call_response("calculator", {"a": 6, "b": 7, "operation": "multiply"}),
        {"role": "assistant", "content": "6 × 7 = 42"},
    ]
    agent, memory, mock = make_agent(responses)
    memory.add({"role": "user", "content": "6*7?"})
    final = agent.run(memory)

    assert final["content"] == "6 × 7 = 42"
    assert mock.call_count == 2
    tool_msgs = [m for m in memory.messages if m.get("role") == "tool"]
    assert tool_msgs[0]["content"] == "42"


def test_agent_unknown_tool_returns_error_text():
    responses = [
        tool_call_response("weather", {}),
        {"role": "assistant", "content": "没有天气工具"},
    ]
    agent, memory, _ = make_agent(responses)
    memory.add({"role": "user", "content": "天气？"})
    agent.run(memory)
    tool_msgs = [m for m in memory.messages if m.get("role") == "tool"]
    assert "找不到工具" in tool_msgs[0]["content"]


def test_agent_max_iterations():
    loop = tool_call_response("calculator", {"a": 1, "b": 1, "operation": "add"})
    agent, memory, _ = make_agent([loop, loop, loop])   # 永远想调工具
    memory.add({"role": "user", "content": "死循环"})
    with pytest.raises(RuntimeError):
        agent.run(memory, max_iterations=3)


def test_agent_callbacks():
    responses = [
        tool_call_response("calculator", {"a": 2, "b": 3, "operation": "add"}),
        {"role": "assistant", "content": "5"},
    ]
    agent, memory, _ = make_agent(responses)
    memory.add({"role": "user", "content": "2+3?"})

    tokens, tools = [], []
    agent.run(memory,
              on_token=tokens.append,
              on_tool=lambda tc: tools.append(tc["function"]["name"]))
    assert tools == ["calculator"]
    assert tokens == ["5"]        # MockLLM 模拟流式：content 一次性回调