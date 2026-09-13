class ToolRegistry:
    def __init__(self):
        self.tools={}
    def register(self,name,function,schema):
        self.tools[name]={
            "function":function,
            "schema":schema,
        }
    def get(self,name):
       tool=self.tools.get(name)
       if tool is None:
           return None
       return tool ["function"]
    def get_schemas(self):
        return [tool["schema"] for tool in self.tools.values()]
    
       