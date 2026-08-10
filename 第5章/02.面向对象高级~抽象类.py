from abc import ABC, abstractmethod
# python通过标准库abc模块实现抽象类

class Animal(ABC):
    def __init__(self, name):
        """
        构造
        :param name: 名称
        """
        self.name = name

    def sleep(self):
        print(self.name + "正在睡觉")

    @abstractmethod
    def call(self):
        pass


class Dog(Animal):

    def __init__(self):
        # 下面两种均可
        super().__init__("狗")
        # Animal.__init__(self,"狗")

    # 重写父类的方法(强制重新，否则运行报错)
    # Can't instantiate abstract class Dog without an implementation for abstract method 'call'
    def call(self):
        print(self.name + "正在发出汪汪汪的叫声")


class Cat(Animal):
    def __init__(self):
        Animal.__init__(self, "猫")

    def call(self):
        print(self.name + "正在发出喵喵喵的叫声")


if __name__ == '__main__':
    dog = Dog()
    dog.sleep()
    dog.call()

    cat = Cat()
    cat.sleep()
    cat.call()
