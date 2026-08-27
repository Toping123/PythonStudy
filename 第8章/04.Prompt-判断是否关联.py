from openai import OpenAI

client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-x5b9qid1ay6dscki.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 示例数据
examples_data = {
    "是": [("公司ABC发布了季度财报,显示盘利增长。", "财报披露,公司ABC利润上升"),
           ("公司ITCAST发布了年度财报,显示盈利大幅度增长。", "财报披露,公司ITCAST更赚钱了。")],
    "不是": [("黄金价格下跌,投资者抛售。", "外汇市场文易额创下新高。"),
             ("央行降息,刺激经济增长。", "新能源技术的创新。")]
}

questions = [
    ("利率上升,影响房地产市场。", "高利率对房地产有一定的冲击。"),
    ("油价大幅度下联,能源公司面临挑战。", "未来智能城市的建设趋势越加明显。"),
    ("股票市场今日大涨,投资者乐观。", "持续上涨的市场让投资者恶到满意。")
]

messages = [{"role": "system",
             "content": "你帮我完成文本匹配,我给你2个句子,被()包围,你判断它们是否匹配,回答是或不是,请参考如下示例:"}]

for key,value in examples_data.items():
    for example in value:
        messages.append({"role": "user", "content": f"{example}"})
        messages.append({"role": "assistant", "content": key})

for question in questions:
    messages.append({"role": "user", "content": f"{question}"})

print(messages)

completion = client.chat.completions.create(
    model="qwen3.7-plus",
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
