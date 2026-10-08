from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import (
    ToolRegistry,
    CalculatorTool,CurrentTimeTool,
    ReadFileTool,ListFilesTool,WriteFileTool,
)
from mini_agent.context import context_report,build_context
def main ():
    llm=DeepSeekLLM()
    registry=ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(CurrentTimeTool())
    registry.register(ReadFileTool())
    registry.register(ListFilesTool())
    registry.register(WriteFileTool())
    agent=Agent(llm,registry)
    messages=[
        {
            "role":"system",
            "content":"你是 MiniAgent，一个可以使用工具的 AI 助手。需要做数学计算时，必须调用 calculator 工具，不要自己心算；\
                需要知道当前时间时，必须调用 get_current_time 工具，\
                需要查看项目文件内容时，调用 read_file 工具,不要猜测。\
                需要浏览项目目录时，调用 list_files 工具。需要创建或写入文件时，调用 write_file 工具（写入前会请求用户确认）,\
                回答要简洁但不遗漏：用户问了几个问题，就完整回答几个。",
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
         '''
         for new_messages in messages[before:]:
             tool_calls=new_messages.get("tool_calls")
             if tool_calls:
                 for tool_call in tool_calls:
                     print(f"  [调用工具] {tool_call['function']['name']}"
                          f" 参数: {tool_call['function']['arguments']}")
         print()   
                    
         for ever_messages in messages:
             print(ever_messages)
         '''
         print(f"agent:{message['content']}")
         print(f"  [{context_report(build_context(messages))}]")
if __name__ == "__main__":
    main()
