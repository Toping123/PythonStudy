from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个边塞诗人，可作诗"),
        MessagesPlaceholder("history"),
        ("human", "再来一首唐诗")
    ]
)

history_messages = [
    ("human", "你来写一首唐诗"),
    ("ai", "床前明月光,疑是地上霜,举头望明月,低头思故乡"),
    ("human", "好诗再来一个"),
    ("ai", "锄禾日当午,汗滴禾下锄,谁知盘中餐,粒粒皆辛苦")
]

model = ChatTongyi(model="qwen3-max", streaming=True)
# 组成链，要求每一个组件都是Runnable接口的实现类，可多次|，前者的返回值作为后者的传参
chain = chat_prompt_template | model
# chat_prompt_template的invoke作为第一个参数传入model进行调用
res = chain.invoke({"history": history_messages})
print(res.content)

print("----------------下面是流式输出----------")

for chunk in chain.stream({"history": history_messages}):
    print(chunk.content, end="", flush=True)
