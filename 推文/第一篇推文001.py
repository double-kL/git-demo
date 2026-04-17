"""
# 这是你的第一段Python代码 —— 假想AI日记

# 1. 顺序：定义一个变量（就像给盒子贴标签）
today = "2026-04-10"

# 2. 列表：存放多条日记（就像一排抽屉）
diary_entries = [
    "今天用户教我认识天气查询",
    "我还不会算加法，但马上就能学会"
]

# 3. 字典：一条日记的完整信息（像一张表格）
new_entry = {
    "date": today,
    "content": "我学会了用print()说话！",
    "mood": "excited"
}

# 4. 把新日记加入列表
diary_entries.append(new_entry)

# 5. 循环打印所有日记
print(f"========== AI日记 ({today}) ==========")
for entry in diary_entries:
    if isinstance(entry, dict):
        print(f"- {entry['content']} (心情: {entry['mood']})")
    else:
        print("- " + entry)
"""

"""
# 导入OpenAI库（大模型的电话机）
from openai import OpenAI

# 1. 配置你的Key（注意：不要直接写在代码里！用环境变量更安全）
#    临时测试可以写在这里，但不要上传到网上
client = OpenAI(
    api_key="sk-3NxpBwIclOVRqa4fiHe0usKMjXis5LBw6tpKAC0GDki9SlTR",   # 替换成AIO平台真实的Key
    base_url="https://api.aiearth.dev"   # 输入AIO平台的地址
)

# 2. 发起一次对话
response = client.chat.completions.create(
    model="deepseek-chat",   # 使用哪个模型
    messages=[
        {"role": "user", "content": "你好，请用一句话介绍你自己"}  # 用户说的话
    ]
)

# 3. 打印大模型的回答
answer = response.choices[0].message.content
print("大模型说：", answer)
"""

"""
# 导入OpenAI库（大模型的电话机）
from openai import OpenAI

# 1. 配置你的Key（注意：不要直接写在代码里！用环境变量更安全）
#    临时测试可以写在这里，但不要上传到网上
client = OpenAI(
    api_key="sk-3NxpBwIclOVRqa4fiHe0usKMjXis5LBw6tpKAC0GDki9SlTR",   # 替换成AIO平台真实的Key
    base_url="https://api.aiearth.dev"   # 输入AIO平台的地址
)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取某个城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名"}
                },
                "required": ["city"]
            }
        }
    }
]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "北京天气如何？"}],
    tools=tools
)

### 大模型会返回“工具名和参数”
"""
"""
### 定义两个简单函数
# 模拟获取天气（你可以换成真实API）
def get_weather(city):
    # 假装查到了温度
    weather_data = {"北京": 5, "上海": 18, "深圳": 25}
    temp = weather_data.get(city, 15)
#括号里面的是默认值，就是如果这个city没有找到的时候默认这个city为15度
    return f"{city}当前温度：{temp}摄氏度"

# 一个简单计算工具
def add(a, b):
    return a + b

### 写一个 `execute_tool()` 执行器
def execute_tool(tool_name, arguments):
    if tool_name == "get_weather":
        city = arguments.get("city")
        return get_weather(city)
    elif tool_name == "add":
        a = arguments.get("a")
        b = arguments.get("b")
        return add(a, b)
    else:
        return f"未知工具：{tool_name}"
# 模拟大模型返回的“点菜单”
tool_call = {"name": "get_weather", "arguments": {"city": "北京"}}
result = execute_tool(tool_call["name"], tool_call["arguments"])
print(result)   # 输出：北京当前温度:5摄氏度
"""
"""
from openai import OpenAI

# ---------- 1. 配置 ----------
client = OpenAI(api_key="sk-48a32a6a180d4a8fba7bbb6c86f2fdd2", base_url="https://api.deepseek.com")

# ---------- 2. 工具定义（同Day4）----------
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取城市温度",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

# ---------- 3. 工具执行函数 ----------
def get_weather(city):
    temps = {"北京": 5, "上海": 18, "深圳": 25}
    return temps.get(city, 15)

def execute_tool(tool_name, args):
    if tool_name == "get_weather":
        return get_weather(args["city"])
    return "未知工具"

# ---------- 4. ReAct循环 ----------
messages = [
    {"role": "user", "content": "北京天气如何？如果低于10度，提醒我穿外套"}
]

max_loops = 3   # 防止无限循环
for _ in range(max_loops):
    # 大模型“思考”：要不要用工具？
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"   # 让模型自己决定
    )
    
    message = response.choices[0].message
    messages.append(message)   # 保存助手的回复
    
    # 检查大模型是否想要调用工具
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = eval(tool_call.function.arguments)   # 把字符串转成字典
            result = execute_tool(tool_name, arguments)
            # 把工具结果“观察”放回对话中
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
    else:
        # 没有工具调用，直接输出最终答案
        print("最终回答：", message.content)
        break
else:
    print("达到最大循环次数，最后回答：", messages[-1].content)
"""
"""
迷你AGI —— 让大模型自己学会用工具
支持：天气查询、数学计算（可自行扩展）
"""
"""
import json
from openai import OpenAI

# ========== 配置 ==========
client = OpenAI(
    api_key="sk-48a32a6a180d4a8fba7bbb6c86f2fdd2",   # 替换！！！
    base_url="https://api.deepseek.com"
)

# ========== 1. 工具说明书（告诉大模型有哪些能力）==========
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取某个城市当前温度（摄氏度）",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如北京"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个数的和",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

# ========== 2. 工具的真正实现（Python函数）==========
def get_weather(city):
    模拟天气API,实际可替换为requests.get()
    data = {"北京": 5, "上海": 18, "深圳": 25}
    return data.get(city, 15)

def add(a, b):
    return a + b

def execute_tool(tool_name, arguments):
    ""根据大模型的选择,调用对应的Python函数""
    if tool_name == "get_weather":
        return get_weather(arguments["city"])
    elif tool_name == "add":
        return add(arguments["a"], arguments["b"])
    else:
        return f"错误：未定义工具 {tool_name}"

# ========== 3. ReAct循环（思考-行动-观察）==========
def run_agent(user_input):
    messages = [{"role": "user", "content": user_input}]
    max_steps = 5   # 防止死循环
    
    for step in range(max_steps):
        print(f"\n--- 第 {step+1} 次思考 ---")
        # 调用大模型，允许它使用工具
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        assistant_msg = response.choices[0].message
        messages.append(assistant_msg)   # 保存大模型的回复
        
        # 如果大模型想要调用工具
        if assistant_msg.tool_calls:
            for tc in assistant_msg.tool_calls:
                tool_name = tc.function.name
                # 将JSON字符串参数转为Python字典（例如 '{"city":"北京"}' -> {"city":"北京"}）
                args = json.loads(tc.function.arguments)
                print(f"🔧 调用工具：{tool_name}，参数：{args}")
                result = execute_tool(tool_name, args)
                print(f"📊 观察结果：{result}")
                # 把工具结果以“工具消息”形式放回对话
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": str(result)
                })
        else:
            # 没有工具调用 → 输出最终答案
            print("\n🤖 最终答案：")
            print(assistant_msg.content)
            return
    
    print("⚠️ 达到最大循环次数，可能未完成。")

# ========== 4. 启动 ==========
if __name__ == "__main__":
    run_agent("北京天气如何？如果低于10度，请提醒我穿外套。")
"""
"""
import requests

# 这里就填你刚找到的API密钥（私钥）
API_KEY = ""

def get_weather(city):
    """
    使用新版验证方式获取实时天气
    """
    url = "https://api.seniverse.com/v3/weather/now.json"
    params = {
        "key": API_KEY,          # 只需要一个key参数
        "location": city,
        "language": "zh-Hans",
        "unit": "c"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        temperature = data["results"][0]["now"]["temperature"]
        weather_text = data["results"][0]["now"]["text"]
        
        return f"{city}当前温度：{temperature}摄氏度，{weather_text}"
    
    except Exception as e:
        return f"请求出错: {e}"

if __name__ == "__main__":
    print(get_weather("北京"))
#################################################################################

from openai import OpenAI

# ---------- 1. 配置 ----------     # 替换成AIO平台真实的Key# 输入AIO平台的地址
client = OpenAI(api_key="sk-3NxpBwIclOVRqa4fiHe0usKMjXis5LBw6tpKAC0GDki9SlTR", base_url="https://api.aiearth.dev")

# ---------- 2. 工具定义（同Day4）----------
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取城市温度",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

# ---------- 3. 工具执行函数 ----------
def get_weather(city):
    temps = {"北京": 5, "上海": 18, "深圳": 25}
    return temps.get(city, 15)

def execute_tool(tool_name, args):
    if tool_name == "get_weather":
        return get_weather(args["city"])
    return "未知工具"

# ---------- 4. ReAct循环 ----------
messages = [
    {"role": "user", "content": "北京天气如何？如果低于10度，提醒我穿外套"}
]

max_loops = 3   # 防止无限循环
for _ in range(max_loops):
    # 大模型“思考”：要不要用工具？
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"   # 让模型自己决定
    )
    
    message = response.choices[0].message
    messages.append(message)   # 保存助手的回复
    
    # 检查大模型是否想要调用工具
    if message.tool_calls:
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            arguments = eval(tool_call.function.arguments)   # 把字符串转成字典
            result = execute_tool(tool_name, arguments)
            # 把工具结果“观察”放回对话中
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
    else:
        # 没有工具调用，直接输出最终答案
        print("最终回答：", message.content)
        break
else:
    print("达到最大循环次数，最后回答：", messages[-1].content)







import requests

# ========== 配置信息 ==========
# 请将下面两个值替换成你刚刚申请到的公钥和私钥
UID = "你的心知天气UID"        # 例如："S1234567890"
API_KEY = "你的心知天气API密钥"  # 例如："abcdefghijklmnop"

def get_weather(city):
    """
    真正联网获取指定城市的实时天气
    """
    # 心知天气的实时天气API地址
    url = "https://api.seniverse.com/v3/weather/now.json"
    
    # 请求参数
    params = {
        "key": API_KEY,      # 你的API密钥
        "location": city,    # 要查询的城市
        "unit": "c",         # 摄氏温度单位
        "language": "zh-Hans" # 返回中文天气描述
    }
    
    try:
        # 发送GET请求到心知天气服务器
        response = requests.get(url, params=params, timeout=10)
        # 检查HTTP状态码是否为200
        response.raise_for_status()
        # 将服务器返回的JSON字符串解析为Python字典
        data = response.json()
        
        # 从返回的数据中提取需要的天气信息
        # 心知天气返回的数据结构为: {"results": [{"now": {"temperature": "5", "text": "晴"}}]}
        now_temperature = data["results"][0]["now"]["temperature"]
        now_weather_text = data["results"][0]["now"]["text"]
        
        return f"{city}当前温度：{now_temperature}摄氏度，{now_weather_text}"
    
    except requests.exceptions.RequestException as e:
        # 捕获网络或API请求相关的错误
        return f"网络或API请求错误: {e}"
    except (KeyError, IndexError, ValueError) as e:
        # 捕获解析JSON数据时可能出现的错误
        return f"数据解析错误，请检查城市名或API返回格式: {e}"

# ========== 测试代码 ==========
if __name__ == "__main__":
    city_name = input("请输入城市名称：")
    weather_info = get_weather(city_name)
    print(weather_info)








import requests
import json
from openai import OpenAI

# ========== 配置 ==========
# 1. 心知天气API Key
WEATHER_API_KEY = "你的心知天气API密钥"

# 2. 大模型API Key（DeepSeek / OpenAI）
client = OpenAI(
    api_key="sk-3NxpBwIclOVRqa4fiHe0usKMjXis5LBw6tpKAC0GDki9SlTR";
     base_url="https://api.aiearth.dev"
)

# ========== 真实天气函数 ==========
def get_real_weather(city):
    url = "https://api.seniverse.com/v3/weather/now.json"
    params = {
        "key": WEATHER_API_KEY,
        "location": city,
        "unit": "c",
        "language": "zh-Hans"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        temp = data["results"][0]["now"]["temperature"]
        text = data["results"][0]["now"]["text"]
        return f"{city}当前{text}，{temp}摄氏度"
    except Exception as e:
        return f"天气查询失败：{e}"

# ========== 大模型智能建议 ==========
def get_advice_from_llm(weather_info):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个贴心的穿衣助手。根据用户提供的天气信息，给出简洁实用的穿衣建议。可以适当用emoji。"},
            {"role": "user", "content": f"天气信息：{weather_info}，请给出穿衣建议。"}
        ]
    )
    return response.choices[0].message.content

# ========== 主程序 ==========
def main():
    city = input("请输入城市名：").strip()
    print("正在查询天气...")
    weather_info = get_real_weather(city)
    print(f"\n🌤️ {weather_info}")
    
    print("\n🤖 大模型正在思考穿衣建议...\n")
    advice = get_advice_from_llm(weather_info)
    print(f"💡 {advice}")

if __name__ == "__main__":
    main()
"""