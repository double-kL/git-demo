import requests
import json
from openai import OpenAI

# ========== 配置 ==========
# 1. 心知天气API Key
WEATHER_API_KEY = "输入天气密钥"

# 2. 大模型API Key（DeepSeek / OpenAI）
client = OpenAI(
    api_key=""#输入AIO平台密钥
    base_url="https://api.deepseek.com"
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