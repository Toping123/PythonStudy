import json
import os

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, BaseMessage, messages_from_dict


class MyFileChatMessageHistory(BaseChatMessageHistory):

    def __init__(self, session_id, store_path):
        self.session_id = session_id
        self.store_path = store_path
        # 存储会话信息的完整路径
        self.file_path = os.path.join(self.store_path, self.session_id)
        # 创建文件
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages) -> None:
        """
        将消息添加进文件
        :param messages: 消息体
        :return: None
        """
        # 将旧的消息记录和当前消息合并
        all_messages = self.messages
        all_messages.extend(messages)

        # 将消息实体转为dict存入new_message_dicts
        new_message_dicts = []
        for message in all_messages:
            d = message_to_dict(message)
            new_message_dicts.append(d)

        # 与上面四行等价
        # new_messages = [message_to_dict(message) for message in all_messages]

        # 写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_message_dicts, f, ensure_ascii=False, indent=4)

    @property
    def messages(self) -> list[BaseMessage]:
        """
        从文件获取历史消息
        :return: 历史消息
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                message_data = json.load(f)
                return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
