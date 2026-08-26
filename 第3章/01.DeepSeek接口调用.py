import os

from openai import OpenAI

# 创建
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "你是一个助理"},
        {"role": "user", "content": "3个人分12个苹果，怎么均分？"},
        {"role": "assistant", "content": '将12个苹果平均分给3个人，每人分到 **4个** 苹果。\n\n如果苹果大小差异很大，想要绝对公平，也可以把所有苹果榨成汁，再用量杯平均分成3杯。'},
        {"role": "user", "content": "那四个人呢？"},
    ],
    model="deepseek-v4-pro",
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)
