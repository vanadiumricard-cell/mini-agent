


from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import calculator,ToolRegistry,calculator_schema
llm=DeepSeekLLM()
registry=ToolRegistry()
registry.register("calculator",calculator,calculator_schema)
agent=Agent(llm,registry)
print()
print("第一次")
messages=[{"role":"user","content":"计算5+0"}]
final=agent.run(messages)
print("最终回答",final["content"])
print()
print("完整历史")
for message in messages:
    print(message)
print()
print("第二次")
messages2=[
    {"role": "user", "content": "先帮我算 123*456，再把结果加 789"}
]
final2 = agent.run(messages2)
print("最终回答:", final2["content"])
print()
print("完整消息历史:")
for message in messages2:
    print(message)