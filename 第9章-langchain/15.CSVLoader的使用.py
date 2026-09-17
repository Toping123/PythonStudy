from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/student.csv",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        # 如果数据原本有表头，就不要下面的代码，如果没有可以使用
        # "fieldnames": ["name", "age", "gender", "hobby"]
    },
    encoding="utf-8"
)

# lazy_load()懒加载，load()为全部加载
for document in loader.lazy_load():
    print(document)
