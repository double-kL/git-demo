from openai import OpenAI

client = OpenAI(
    api_key="sk-KYYgBZPYQC0Kc5bpLfL1sl32RTyjQA04VSlq3GsMALyOOm5j",
    base_url="https://api.aiearth.dev/v1"
)

print("ChatGPT CLI (输入 'exit' 退出)")
messages = []

while True:
    user_input = input("\n你: ")
    if user_input.lower() == 'exit':
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    print(f"\nGPT: {answer}")
