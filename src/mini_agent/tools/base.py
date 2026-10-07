class Tool:
    name=""
    description=""
    parameters={}
    required=[]
    ALLOWED_PARAM_KEYS = {"type", "description", "enum"}
    def validate(self):
        if not self.name:
            raise ValueError("工具缺少 name")
        if not self.description:
            raise ValueError(f"工具 {self.name} 缺少 description")
        for param, spec in self.parameters.items():
            for key in spec:
                if key not in self.ALLOWED_PARAM_KEYS:
                    raise ValueError(
                        f"工具 {self.name} 的参数 {param} 含可疑键 '{key}'"
                        f"（允许：{self.ALLOWED_PARAM_KEYS}）"
                    )
        for param in self.required:
            if param not in self.parameters:
                raise ValueError(f"工具 {self.name} 的 required 含不存在的参数：{param}")
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