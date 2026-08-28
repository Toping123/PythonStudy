from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 构造通义千问模型
tongyi_model = ChatTongyi(model="qwen3-max")

messages = [
    SystemMessage(content="你是一位诗人"),
    HumanMessage(content="帮我作一首诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦"),
    HumanMessage(content="请参照上一个回复的格式写一首新的诗")
]

# 简写方式
messages2 = [
    ("system","你是一位诗人"),
    ("human","帮我作一首诗"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦"),
    ("human","请参照上一个回复的格式写一首新的诗"),
]

# 调用invoke进行提问（非流式）
# tongyi_resp = tongyi_model.stream(input=messages)
tongyi_resp = tongyi_model.stream(input=messages2)
print("通义千问回复:")
for item in tongyi_resp:
    print(item.content, end="", flush=True)

