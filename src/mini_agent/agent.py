
import json
class Agent:
   def __init__(self,llm,tool_registry):
         self.llm=llm
         self.tool_registry=tool_registry
   def run(self,messages,max_iterations=10):
        for _ in range(max_iterations):
             message=self.llm.chat(messages,tools=self.tool_registry.get_schemas())
             messages.append(message)
             tool_calls=message.get("tool_calls")
             if not tool_calls:
                  return message
             for tool_call in tool_calls:
                  result=self.execute_tool_call(tool_call)
                  messages.append({
                       "role":"tool",
                       "tool_call_id":tool_call["id"],
                       "content":str(result),
                  })
        raise RuntimeError(f"Agent 达到最大循环次数（{max_iterations}）仍未结束")    
   def execute_tool_call(self,tool_call):
        name=tool_call["function"]["name"]
        try:
            arguments=json.loads(tool_call["function"]["arguments"])
            tool=self.tool_registry.get(name)
            if tool is None:
                 return f"找不到工具{name}"
            return tool (**arguments)
        except Exception as error:
             return f"错误{error}"

          
  
                              
        

