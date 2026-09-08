from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate

# 提示词
prompt1 = PromptTemplate.from_template(
    "我的妹夫姓{lastname},刚生了{gender},帮取个名字，简单以key:value的json格式回答，key恒为name")
# 构造通义千问模型
model = ChatTongyi(model="qwen-max",streaming=True)
# 构造一个Str解析器，接受Json字符串转为Dict
json_parser = JsonOutputParser()
# 第二个提示词
prompt2 = PromptTemplate.from_template("请解析{name}这个名字的含义")
# 构造一个Str解析器，接受AIMessage转为Str
str_parser = StrOutputParser()

# 使用chain
chain = prompt1 | model | json_parser | prompt2 | model | str_parser
res = chain.stream(input={"lastname": "童", "gender": "儿子"})
for chunk in res:
    print(chunk, end="", flush=True)
