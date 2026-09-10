from mini_agent.llm.base import demollm,BaseLLM
def ask(llm:BaseLLM,message:str)->str:
    return llm.chat(message)
demo_llm=demollm()
response=ask(demo_llm,"你好啊")
print(response)