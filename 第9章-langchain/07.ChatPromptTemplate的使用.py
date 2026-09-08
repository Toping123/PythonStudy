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

prompt_data = chat_prompt_template.invoke({"history": history_messages}).to_string()
print(prompt_data)
model = ChatTongyi(model="qwen3-max")
res = model.invoke(prompt_data)
print(res.content)
print(type(res))  # AIMessage
