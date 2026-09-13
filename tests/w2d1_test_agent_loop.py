

from mini_agent import agent
from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import calculator,ToolRegistry
llm=DeepSeekLLM()
registry=ToolRegistry()
registry.register("calculator",calculator)
agent=Agent(llm,registry)
messages=[
    {
        "role":"user",
        "content":"你好，介绍一下自己"
    }
]
response=agent.run(messages)
print(response)