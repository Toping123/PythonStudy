from 第6章.model.Book import Book


class Member:
    def __init__(self, member_id, name, sex, age,password, vip_grade):
        """
        用户
        :param member_id: 用户id
        :param name:      用户名
        :param sex        性别
        :param age:       用户年龄
        :param password:  登录密码
        :param vip_grade vip等级（0-3）
        """
        self.member_id = member_id
        self.name = name
        self.sex = sex
        self.age = age
        self.password = password
        self.vip_grade = vip_grade
        # 已借阅书籍，字典列表，key为book_id,value为book
        self.__borrow_book_list = []

    def borrow_limit_num(self) -> int:
        """
        总共可借阅的书籍数量
        :return: 可借阅的书籍数量
        """
        return 3 + self.vip_grade

    def get_current_book_list(self) -> list[Book]:
        """
        获取当前借阅的书籍
        :return: 当前借阅的书籍list
        """
        return self.__borrow_book_list

    def borrow_book(self, book: Book) -> bool:
        """
        借阅书籍
        :param book: 书籍
        :return:  是否可借阅
        """
        if book.get_available_num() <= 0:
            print(f"书籍《{book.name}》已无库存")
            return False
        elif len(self.__borrow_book_list) >= self.borrow_limit_num():
            print(f"您当前最多可借{self.borrow_limit_num()},当前已借满!")
            return False
        else:
            print(f"借阅《{book.name}》成功")
            self.__borrow_book_list.append(book)
            return True

    def return_book(self, book: Book) -> bool:
        """
        还书
        :param book: 书籍
        :return: 是否可还
        """
        if book not in self.__borrow_book_list:
            print(f"你当前未借《{book.name}》")
            return False
        else:
            self.__borrow_book_list.remove(book)
            print(f"还书籍《{book.name}》成功")
            return True

    def __str__(self):
        print(f"书籍id:{self.member_id},书名:{self.name}")
