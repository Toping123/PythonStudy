class Book:
    def __init__(self, book_id, name, total_num):
        """
        书
        :param book_id:    书id
        :param name:       书名称
        :param total_num:  书总量
        """
        self.book_id = book_id
        self.name = name
        self.__available_num = total_num

    def borrow_book(self) -> bool:
        """
        被借阅
        :return: 是否借阅成功
        """
        if self.__available_num > 0:
            self.__available_num -= 1
            return True
        else:
            return False

    def return_book(self):
        """被归还"""
        self.__available_num += 1

    def get_available_num(self) -> int:
        """
        获取可借阅的数量
        :return: 可借阅的数量
        """
        return self.__available_num

    def __str__(self) -> str:
        return f"书籍编号:{self.book_id},书名:{self.name},剩余数量:{self.__available_num}"
