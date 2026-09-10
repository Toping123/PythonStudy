from langchain_community.chat_models import ChatTongyi
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from utils.MyFileChatMessageHistory import MyFileChatMessageHistory

# llm
model = ChatTongyi(model="qwen3-max", streaming=True)
# 提示词
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史回答用户输入的问题，会话历史：{chat_history},用户提问：{input},请回答")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你需要根据会话历史回答用户输入的问题，会话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答如下问题：{input}")
    ]
)
# 字符串解析器
str_parser = StrOutputParser()


def print_prompt(prompt):
    print("-" * 20, prompt.to_string(), "-" * 20)
    return prompt


# 初始chain
origin_chain = prompt | print_prompt | model | str_parser


def get_history(session_id) -> InMemoryChatMessageHistory:
    """
    通过session_id获取历史会话消息InMemoryChatMessageHistory类对象
    :param session_id: 会话session_id
    :return: 会话消息InMemoryChatMessageHistory类对象
    """
    return MyFileChatMessageHistory(session_id, "./my_chat_history")


# 新的chain，对原始chain增强，附带历史消息
new_chain = RunnableWithMessageHistory(
    origin_chain,  # 需要增强的原始chain
    get_history,  # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key="input",  # 用户输入的key,对应prompt的输入模板
    history_messages_key="chat_history"  # 会话历史消息的key,对应prompt的输入模板
)

if __name__ == '__main__':
    # 固定格式，添加langchain配置，为当前程序配置所属的session_id
    session_config = {
        "configurable": {
            "session_id": "Toping"
        }
    }

    # res = new_chain.invoke({"input": "小明有3只猫"}, session_config)
    # print("第一次执行", res)
    #
    # res = new_chain.invoke({"input": "小芳有1条狗"}, session_config)
    # print("第二次执行", res)

    res = new_chain.invoke({"input": "他们总共有几只宠物"}, session_config)
    print("第三次执行", res)
