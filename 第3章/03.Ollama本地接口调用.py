import os

from openai import OpenAI

# 创建
client = OpenAI(
    base_url="http://localhost:11434/v1"
)

response = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "你是谁？"}
    ],
    model="deepseek-r1:8b",
    stream=True,
    extra_body={"enable_thinking": True},
)

for chunk in response:
    if not chunk.choices:
        delta = chunk.choices[0].delta
        if hasattr(delta, "content") and delta.content:
            print(delta.content, end="", flush=True)
