from mini_agent.tools import ToolRegistry
from mini_agent.llm.client import DeepSeekLLM
import json
class Agent:
   def __init__(self,llm,tool_registry):
         self.llm=llm
         self.tool_registry=tool_registry
   def run(self,messages):
        while True:
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
   def execute_tool_call(self,tool_call):
        name=tool_call["function"]["name"]
        arguments=json.loads(tool_call["function"]["arguments"])
        tool=self.tool_registry.get(name)
        if tool is None:
             raise ValueError(f"找不到工具{name}")
        return tool (**arguments)

          
  
                              
        

