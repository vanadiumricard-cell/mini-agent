from mini_agent.llm.client import DeepSeekLLM
llm=DeepSeekLLM()
messages=[]
messages.append({"role":"user","content":"我叫小明，记住我的名字"})
message=llm.chat(messages)
print("ai:",message["content"])
messages.append(message)
messages.append({"role":"user","content":"我叫什么名字"})
response=llm.chat(messages)
print("ai:",response["content"])