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

 