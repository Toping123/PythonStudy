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

is_answering = False  # 是否进入回复阶段
print("\n" + "=" * 20 + "思考过程" + "=" * 20)
for chunk in response:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
    if hasattr(delta, "content") and delta.content:
        if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
        print(delta.content, end="", flush=True)
