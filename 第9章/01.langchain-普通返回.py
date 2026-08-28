from langchain_community.llms.tongyi import Tongyi
from langchain_community.llms.ollama import Ollama

# 构造通义千问模型
tongyi_model = Tongyi(model="qwen-max")

# 调用invoke进行提问（非流式）
tongyi_resp = tongyi_model.invoke(input="你是谁，你能干什么？")
print(f"通义千问回复：{tongyi_resp}")

# 构造Ollama本地模型
ollama_model = Ollama(model="deepseek-r1:8b")
ollama_resp = ollama_model.invoke(input="你是谁，你能干什么？")
print(f"Ollama本地模型回复：{ollama_resp}")
