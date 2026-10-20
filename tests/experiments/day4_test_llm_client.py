from mini_agent.llm.client import DeepSeekLLM

llm = DeepSeekLLM()
message = llm.chat([{"role": "user", "content": "你好，请介绍一下你自己。"}])
print(message["content"])