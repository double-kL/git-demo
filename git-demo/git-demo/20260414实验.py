# 导入OpenAI库（大模型的电话机）
from openai import OpenAI

# 1. 配置你的Key（注意：不要直接写在代码里！用环境变量更安全）
#    临时测试可以写在这里，但不要上传到网上
client = OpenAI(
    api_key="sk-o1hs9pFfjCF43eL4ZAg6mFxe78ctJOABs7km4brvO5Nc1jud",   # 替换成真实的Key
    base_url="https://api.aiearth.dev/v1"   # DeepSeek的地址
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