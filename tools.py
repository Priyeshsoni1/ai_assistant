from datetime import datetime

def get_time():
    return {
        "current_time":str(datetime.now())
    }

def calculator(a,b,operation):
    if operation=="+":
        return a+b
    if operation=='-':
        return a-b
    return None


TOOLS = {

    "get_time":
        get_time,

    "calculator":
        calculator
}