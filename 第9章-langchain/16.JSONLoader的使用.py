from langchain_community.document_loaders import JSONLoader

loader = JSONLoader(
    file_path="./data/student.json",
    jq_schema=".[].name",
    text_content=False,
)

# lazy_load()懒加载，load()为全部加载
for document in loader.lazy_load():
    print(document)
