from mini_agent.agent import Agent
from mini_agent.tools import ToolRegistry,calculator
registry =ToolRegistry()
registry.register("calculator",calculator)
agent=Agent(registry)
user_input="请帮我计算"
tool_name=agent.decide_tool(user_input)
print("用户:", user_input)
print("Agent 决定使用:", tool_name)
result=agent.run_tool(tool_name,10,40,"add")
print(f"工具 {tool_name},结果 {result}")
