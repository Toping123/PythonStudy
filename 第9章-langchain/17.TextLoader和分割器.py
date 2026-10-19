from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = TextLoader("./data/test.txt", encoding="utf-8")

doc = loader.load()
print(doc)
print(len(doc))

# 分段器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # 分段的最大字符数
    chunk_overlap=50,  # 分段之间允许重叠字符数
    separators=["\n\n", "\n", "!", "?", " "],
    length_function=len,  # 统计字符的依据函数
)

split_docs = splitter.split_documents(doc)
for split_doc in split_docs:
    print("-"*50)
    print(split_doc)
    print("-"*50)
print(len(split_docs))
