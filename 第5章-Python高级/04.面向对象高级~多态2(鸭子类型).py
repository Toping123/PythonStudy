class Dog:

    def __init__(self):
        self.name = "狗"

    def call(self):
        print(self.name + "正在发出汪汪汪的叫声")


class Cat:
    def __init__(self):
        self.name = "猫"

    def call(self):
        print(self.name + "正在发出喵喵喵的叫声")


class Duck:
    def __init__(self):
        self.name = "鸭子"

    def call(self):
        print(self.name + "正在发出嘎嘎嘎的叫声")


def handle_call(duck):
    duck.call()


if __name__ == '__main__':
    # 本质上也不能算多态，只能说是Python是解释型语言（非编译型）handle_call参数可以随意
    handle_call(Dog())
    handle_call(Cat())
    handle_call(Duck())
