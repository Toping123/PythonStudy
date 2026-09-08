class Car:
    def __init__(self, brand, model, owner):
        """
        构造
        :param brand: 品牌
        :param model: 型号
        :param owner: 车主
        """
        self.brand = brand
        self.model = model
        # 私有属性使用__来表示
        self.__owner = owner

    def start(self):
        """启动"""
        print(f"{self.__owner}启动了{self.brand}{self.model}")

    def drive(self):
        """驾驶"""
        print(f"{self.__owner}正在驾驶{self.brand}{self.model}")
        self.__operate_electric()

    # __表示私有方法
    def __operate_electric(self):
        """踩电门"""
        print(f"{self.__owner}踩电门")

    def stop(self):
        """停止"""
        print(f"{self.__owner}停止了{self.brand}{self.model}")


if __name__ == '__main__':
    car = Car("小米", "su7", "张三")
    car.start()
    car.drive()
    car.stop()
    # 依然可以在私有属性/方法中添加_类名访问私有属性/方法（不推荐）
    # print(car._Car__owner)
    # print(car._Car__operate_electric())
