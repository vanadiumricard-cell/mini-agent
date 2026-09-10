from mini_agent.llm.base import demollm
llm=demollm()
response=llm.chat("Hello, how are you?")
print(response)
