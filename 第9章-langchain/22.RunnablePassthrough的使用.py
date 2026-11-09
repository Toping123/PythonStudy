from re import search
from xml.dom.minidom import Document

from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore

# 构建模型
model = ChatTongyi(model="qwen-plus")
prompt = ChatPromptTemplate.from_messages([
    ("system", "以我提供的参考资料为主，简介和专业地回答用户问题，参考资料：{context}"),
    ("user", "用户提问：{input}"),
])

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 准备向量库的数据
vector_store.add_texts(["减肥就要少吃多锻炼", "减肥期间饮食很重要，清单饮食控制卡路里", "跑步是很好的运动"])

input_text = "怎么减肥"

# 向量存储对应,通过as_retriever可返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k": 2})


def format_func(docs: list[Document]):
    """
    拼接向量数据
    :param docs:
    :return:
    """
    if not docs:
        return "无相关参考资料"
    formatted_str = "["
    for doc_item in docs:
        formatted_str += doc_item.page_content
    formatted_str += "]"
    return formatted_str


def print_prompt(prompt) -> str:
    """
    打印指令
    :param prompt:
    :return:
    """
    print(prompt.to_string())
    print("-" * 20)
    return prompt


# 调用链
chain = ({"input": RunnablePassthrough(),
          "context": retriever | format_func} | prompt | print_prompt | model | StrOutputParser())
res = chain.invoke(input_text)
print(res)

"""
retriever:
    - 输入: 用户的提问   str
    - 输出: 向量库的检索结果  list[Document]
prompt:
    - 输入: 用户的提问 + 向量库的检索结果  dict
    - 输出: 完整的提示词  PromptValue
"""