from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ToolRegistry, calculator, calculator_schema

llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register("calculator", calculator, calculator_schema)
agent = Agent(llm, registry)

messages = [{"role": "user", "content": "帮我算 5 除以 0"}]
final = agent.run(messages)

print("最终回答:", final["content"])
print()
print("完整消息历史:")
for message in messages:
    print(message)