class ToolRegistry:
    def __init__(self):
        self.tools={}
    def register(self,name,function):
        self.tools[name]=function
    def get(self,name):
        return self.tools.get(name) 
       