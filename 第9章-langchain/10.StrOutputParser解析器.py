from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# zero-shot
prompt = PromptTemplate.from_template("我的妹夫姓{lastname},刚生了{gender},帮取个名字，简单回答即可")
# 构造通义千问模型
model = ChatTongyi(model="qwen-max",streaming=True)
# 构造一个解析器，接受AIMessage转为Str
parser = StrOutputParser()

# 使用chain
chain = prompt | model | parser
res = chain.invoke(input={"lastname": "童", "gender": "儿子"})
print(res)
print(type(res))
