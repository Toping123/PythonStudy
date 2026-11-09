
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

# 检索向量库
search_result = vector_store.similarity_search(input_text, 2)
reference_text = "["
for doc in search_result:
    reference_text += doc.page_content
reference_text += "]"


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
chain = prompt | print_prompt | model | StrOutputParser()
res = chain.invoke({"input": input_text, "context": reference_text})
print(res)
