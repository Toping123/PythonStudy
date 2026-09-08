import json

from openai import OpenAI

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-x5b9qid1ay6dscki.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 示例数据
examples_data = [
    {
        "content": "2023年第88期,有2注一等奖,中奖的号码为: 红球1、3、8、7,蓝球12",
        "answers": {
            "期数": "202388",
            "中奖号码": [1,3,8,7,12],
            "一等奖": "2注"
        }
    },
    {
        "content": "2024102期,中奖的号码为：红球6、32、88、75,蓝球66，共有3注一等奖",
        "answers": {
            "期数": "2024102",
            "中奖号码": [6, 32, 88, 75],
            "一等奖": "3注"
        }
    },
]

# 提问问题
questions = [
    "2025年第100期,开好红球22 21 06 01 03 11 篮球07,一等奖中奖为2注。",
    "2025101期,有3注1等奖,10注2等奖,开号篮球11,中奖红球3、5、7、11、12、16。"
]

messages = [{"role": "system",
             "content": "你帮我完成信息抽取,我给你句子和回答示例,你抽取信息,按我示例中的JSON字符串属性进行输出，禁止输出其他属性,如果某些信息不存在,用原文未提及"}]

for example in examples_data:
    messages.append({"role": "user", "content": example["content"]})
    messages.append({"role": "assistant", "content": json.dumps(example["answers"], ensure_ascii=False)})

for question in questions:
    messages.append({"role": "user", "content": question})

completion = client.chat.completions.create(
    model="qwen3.7-plus",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": True},
    stream=True
)

is_answering = False  # 是否进入回复阶段
for chunk in completion:
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
