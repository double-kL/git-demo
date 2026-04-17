"""
import json
from openai import OpenAI

# ========== 配置 ==========
API_KEY = "sk-"
BASE_URL = "https://api.deepseek.com"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ========== 工具函数 ==========
def get_weather(city: str) -> str:
    # 这里可以替换成真实API，现在模拟
    return f"{city}天气：晴天，24-28℃，微风"

def calculate(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except:
        return "计算错误，请检查表达式"

def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取失败：{e}"

def write_file(path: str, content: str) -> str:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return "写入成功"
    except Exception as e:
        return f"写入失败：{e}"

available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
    "read_file": read_file,
    "write_file": write_file,
}

# ========== 工具定义（JSON） ==========
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "计算数学表达式，如 '3+5*2'",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取文件内容",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "写入内容到文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["path", "content"]
            }
        }
    }
]

# ========== Agent主循环 ==========
def run_agent(user_input):
    messages = [{"role": "user", "content": user_input}]
    
    while True:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools
        )
        msg = response.choices[0].message
        
        if not msg.tool_calls:
            print("\n🤖 智能体回答：", msg.content)
            break
        
        # 处理工具调用
        messages.append(msg)
        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"🔧 调用工具：{func_name}，参数：{args}")
            result = available_functions[func_name](**args)
            print(f"📦 工具返回：{result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

# ========== 测试 ==========
if __name__ == "__main__":
    print("=== 你的迷你AGI已启动 ===\n")
    while True:
        query = input("你：")
        if query.lower() in ["exit", "退出"]:
            break
        run_agent(query)
        print()
"""