from langchain_core.prompts import PromptTemplate

"""
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable

区别           format                    invoke
功能         纯字符串替换           Runnable接口标准方法   
返回值         字符串                 PromptValue对象（可调用to_string()转为str）
调用方式     format(k=v,k=v...)     invoke({"k":v,"k":v,...})
解析         支持解析{}占位符        支持解析{}占位符和MessagesPlaceholder结构化占位符
"""

prompt_template = PromptTemplate.from_template("我的邻居是{name},最喜欢{hobby}")

prompt_data1 = prompt_template.format(name="张三", hobby="打篮球")
print(prompt_data1, type(prompt_data1))

prompt_data2 = prompt_template.invoke({"name": "张三", "hobby": "打篮球"})
print(prompt_data2, type(prompt_data2))
