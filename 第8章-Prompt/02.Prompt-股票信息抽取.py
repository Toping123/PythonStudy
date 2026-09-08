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
        "content": "2023-01-10,股市震荡。殷票强大科技A股今日开盘价100人民币,一度飙升至105人民币,随后回落至98人民币,最终以102人民币收盘,成交量达到5205000",
        "answers": {
            "日期": "2023-01-10",
            "股票名称": "强大科技A股",
            "开盘价": "100人民币",
            "收盘价": "102人民币",
            "成交量": "520000"
        }
    },
    {
        "content": "2024-05-16,股市利好。殷票英伟达美股今日开盘价105美元,一度飙升升至109美元,随后回落至100美元,最终以116美元收盘,成交量达到3560000。",
        "answers": {
            "日期": "2024-05-16",
            "股票名称": "英伟达美股",
            "开盘价": "105美元",
            "收盘价": "116美元",
            "成交量": "3560000"
        }
    }
]

# 提问问题
questions = [
    "2025-06-16,股市利好。股票传智教育A股今日开盘价66人民币,一度飙升至70人民币,随后回落至65人民币,最终以68人民币收盘,成交量达到123000。",
    "2025-06-06,股市利好。股票黑马程序员A股今日开盘价200人民币, 一度变飙升至211人民币, 随后回落至201人民币, 最终以206人民币收盘"
]

messages = [{"role": "system",
             "content": "你帮我完成信息抽取,我给你句子,你抽取信息,按JSON字符串输出,如果某些信息不存在,用]原文未提及"}]

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
