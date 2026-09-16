from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ToolRegistry,calculator,calculator_schema
def main ():
    llm=DeepSeekLLM()
    registry=ToolRegistry()
    registry.register("calculator",calculator,calculator_schema)
    agent=Agent(llm,registry)
    messages=[
        {
            "role":"system",
            "content":"你是 MiniAgent，一个可以使用工具的 AI 助手。需要做数学计算时，必须调用 calculator 工具，不要自己心算。回答尽量简洁。回答要简洁但不遗漏：用户问了几个问题，就完整回答几个",
        }
        
    ]
    print("agent已启动")
    print("输入exit退出")
    while True:
         user_input=input("\n用户:" )
         if user_input=="exit":
           print("agent已结束")
           break
         messages.append({"role":"user","content":user_input})
         before = len(messages)
         message=agent.run(messages)
         for new_messages in messages[before:]:
             tool_calls=new_messages.get("tool_calls")
             if tool_calls:
                 for tool_call in tool_calls:
                     print(f"  [调用工具] {tool_call['function']['name']}"
                          f" 参数: {tool_call['function']['arguments']}")
                        
             
         print(f"agent:{message['content']}")
if __name__ == "__main__":
    main()
