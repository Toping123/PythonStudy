from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="data/test.pdf",
    mode="page"  # 默认page，可设置single
)

documents = loader.lazy_load()
page_count = 0
for document in documents:
    page_count += 1
    print(document)
    print("-" * 100)
print(f"总数量{page_count}")