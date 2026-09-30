class Tool:
    name=""
    description=""
    parameters={}
    required=[]
    def run(self,**kwargs):
        raise NotImplementedError("子类必须重写run方法")
    def to_schema(self):
        return{
            "type":"function",
            "function":{
                "name":self.name,
                "description":self.description,
                "parameters":{
                    "type":"object",
                    "properties":self.parameters,
                    "required":self.required
                }
            }
        }