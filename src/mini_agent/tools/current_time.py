from datetime import datetime

def get_current_time()->str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
get_current_time_schema= {
    "type":"function",
    "function":{
        "name":"get_current_time",
        "description":"获得当前的日期和时间",
        "parameters":{
            "type":"object",
            "properties":{},
        },
    },
}