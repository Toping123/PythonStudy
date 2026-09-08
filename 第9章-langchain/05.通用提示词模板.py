from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

# zero-shot
prompt_template = PromptTemplate.from_template("我的妹夫姓{lastname},刚生了{gender},帮取个名字，简单回答即可")

# 构造通义千问模型
model = Tongyi(model="qwen-max")

# 方式1：调用format方法注入信息
prompt_data = prompt_template.format(lastname = "童",gender="女儿")
print(model.invoke(prompt_data))

# 方式2：使用chain
chain = prompt_template | model
print(chain.invoke(input={"lastname":"童","gender":"儿子"}))
