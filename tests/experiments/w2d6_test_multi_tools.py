from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import (
    ToolRegistry,
    calculator, calculator_schema,
    get_current_time, get_current_time_schema,
)
llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register("calculator", calculator, calculator_schema)
registry.register("get_current_time", get_current_time, get_current_time_schema)

agent = Agent(llm, registry)

print("已注册工具:", list(registry.tools.keys()))
def show_tool_calls(messages):
    for message in messages:
        tool_calls = message.get("tool_calls")
        if tool_calls:
            for tool_call in tool_calls:
                print("  调用:", tool_call["function"]["name"],
                      tool_call["function"]["arguments"])
print("场景 1: 问时间")
messages1 = [{"role": "user", "content": "现在几点了？"}]
final1 = agent.run(messages1)
print("答:", final1["content"])
show_tool_calls(messages1)
print()
print("场景 2: 计算")
messages2 = [{"role": "user", "content": "帮我算 99*11"}]
final2 = agent.run(messages2)
print("答:", final2["content"])
show_tool_calls(messages2)
print()
print("场景 3: 时间和计算一起")
messages3 = [{"role": "user", "content": "现在几点了？顺便帮我算 12*34"}]
final3 = agent.run(messages3)
print("答:", final3["content"])
show_tool_calls(messages3)
