from mini_agent.llm.base import demollm
llm=demollm()
response = llm.chat([{"role": "user", "content": "Hello, how are you?"}])
print(response["content"])
