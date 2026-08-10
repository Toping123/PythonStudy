import json
from 第6章.model.Book import Book
from 第6章.model.Member import Member


class BookManager:
    def __init__(self, version="1.0.0"):
        self.version = version
        self.book_list = []
        self.member_list = []
        self.load_book_data()
        self.load_member_data()

    def load_book_data(self):
        """加载书籍数据"""
        with open("./data/book_list.json", "r", encoding="utf-8") as f:
            book_list = json.load(f)
        self.book_list = []
        for book in book_list:
            self.book_list.append(
                Book(book["book_id"], book["name"], book["total_num"]))
        print("加载书籍数据成功")

    def load_member_data(self):
        """加载会员数据"""
        with open("./data/member_list.json", "r", encoding="utf-8") as f:
            member_list = json.load(f)
        self.member_list = []
        for member in member_list:
            self.member_list.append(
                Member(member["member_id"], member["name"], member["sex"],
                       member["age"], member["password"], member["vip_grade"]))
        print("加载会员数据成功")

    def login(self, member_id, password) -> Member | None:
        """
        登录
        :param member_id: 登录用户id
        :param password:  登录密码
        :return:  是否登录成功
        """
        member = self.get_member_by_id(member_id)
        if member is None:
            print(f"用户{member_id}不存在")
            return None
        elif member.password != password:
            print(f"密码错误")
            return None
        else:
            print(f"登录成功,欢迎{member.name}")
            return member

    def get_member_by_id(self, member_id) -> Member | None:
        """
        根据会员id获取会员信息
        :param member_id: 指定member_id
        :return: 会员信息
        """
        for member in self.member_list:
            if str(member.member_id) == member_id:
                return member
        return None

    def get_book_by_id(self, book_id) -> Book | None:
        """
        根据书籍id获取书籍信息
        :param book_id: 指定book_id
        :return: 书籍信息
        """
        for book in self.book_list:
            if str(book.book_id) == book_id:
                return book
        return None

    def run(self):
        """运行"""
        while True:
            member_id = input("请输入用户id:")
            password = input("请输入登录密码:")
            member = self.login(member_id, password)
            if member is None:
                continue
            else:
                break
        if member is not None:
            print("欢迎使用图书馆管理系统")
            while True:
                print("---------------------------------------------")
                operate_type = input("请输入操作类型:\n1.借阅书籍\n2.归还书籍\n3.查询已借阅书籍\n4.退出系统\n")
                match operate_type:
                    case "1":
                        print("---------------------------------------------")
                        print(f"当前书籍数据:\n{"\n".join(book.__str__() for book in self.book_list)}")
                        book_id = input("请输入要借阅的书籍id：")
                        book = self.get_book_by_id(book_id)
                        if book is None:
                            print(f"当前无{book_id}的书籍")
                            continue
                        member.borrow_book(book)
                        book.borrow_book()
                    case "2":
                        print("---------------------------------------------")
                        print("当前已借阅的书:")
                        for borrowed_book in member.get_current_book_list():
                            print(f"{borrowed_book.book_id}:{borrowed_book.name}")
                        book_id = input("请输入要还的书籍id：")
                        book = self.get_book_by_id(book_id)
                        if book is None:
                            print(f"当前无{book_id}的书籍")
                            continue
                        member.return_book(book)
                        book.return_book()
                    case "3":
                        print("---------------------------------------------")
                        print("当前已借阅书籍:")
                        for borrowed_book in member.get_current_book_list():
                            print(f"{borrowed_book.book_id}:{borrowed_book.name}")
                    case "4":
                        print("---------------------------------------------")
                        print("欢迎下次光临")
                        return


if __name__ == '__main__':
    manager = BookManager()
    manager.run()
