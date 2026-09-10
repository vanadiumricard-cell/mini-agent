from mini_agent.llm.client import DeepSeekLLM
llm=DeepSeekLLM()
messages=[]
messages.append({"role":"user","content":"我叫小明，记住我的名字"})
response=llm.chat(messages)
print("ai:",response)
messages.append({"role":"assistant","content":response})
messages.append({"role":"user","content":"我叫什么名字"})
response=llm.chat(messages)
print("ai:",response)