from mini_agent.llm.client import DeepSeekLLM
llm=DeepSeekLLM()
response=llm.chat("你好，请介绍一下你自己。")
print(response)