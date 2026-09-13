def calculator(a:float,b:float,operation:str)->float:
   if operation == "add":
      return a+b
   elif operation == "subtract":
      return a-b
   elif operation == "multiply":
      return a*b
   elif operation =="divide":
      if b==0:
        raise ValueError("除数不能为零")
      return a/b
   raise ValueError("不支持的运算类型")
calculator_schema={
   "type":"function",
   "function":{
      "name":"calculator",
      "description":"进行基本数学运算",
      "parameters":{
         "type":"object",
         "properties":{
            "a":{"type":"number","description":"第一个数字"},
            "b":{"type":"number","description":"第二个数字"},
            "operation":{
               "type":"string",
               "enum":["add","subtract","multiply","divide"],
               "description":"计算类型",
            },
         },
         "required":["a","b","operation"],
      }
   }
}
 