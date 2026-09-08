class Animal:
    def __init__(self, name):
        """
        构造
        :param name: 名称
        """
        self.name = name

    def sleep(self):
        print(self.name + "正在睡觉")

    def call(self):
        print(self.name + "正在发出叫声")


class Dog(Animal):

    def __init__(self):
        # 下面两种均可
        super().__init__("狗")
        # Animal.__init__(self,"狗")

    # 重写父类的方法
    def call(self):
        print(self.name + "正在发出汪汪汪的叫声")


class Cat(Animal):
    def __init__(self):
        Animal.__init__(self, "猫")

    def call(self):
        print(self.name + "正在发出喵喵喵的叫声")


if __name__ == '__main__':
    # 多态：父类的引用指向子类的对象
    animal = Dog()
    animal.sleep()
    animal.call()

    animal = Cat()
    animal.sleep()
    animal.call()
