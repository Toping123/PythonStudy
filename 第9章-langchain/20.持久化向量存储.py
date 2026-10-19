from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

# 向量存储模型，Chroma向量数据库（轻量级）
vector_store = Chroma(
    collection_name="vectors",  # 当前向量存储起个名，类似数据库表名
    embedding_function=DashScopeEmbeddings(),
    persist_directory="./chroma_db"
)

# CSV加载器加载源数据
loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column="source"
)

documents = loader.load()

# 向量存储的添加
vector_store.add_documents(
    documents=documents,  # 添加的数据源
    ids=[f"id{str(i)}" for i in range(1, len(documents) + 1)]  # 给添加的文档添加id
)

# 删除，传入[id, id...]
vector_store.delete(["id1", "id2"])

# 检索，k表示需要匹配的最接近的数量
result = vector_store.similarity_search("Python简单易学", 2)
print(result)
