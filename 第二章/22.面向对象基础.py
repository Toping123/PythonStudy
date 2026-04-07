# 定义类
class Car:
    def __init__(self, brand, color, price):
        """
        初始化方法
        :param brand: 品牌
        :param color: 颜色
        :param price: 价格
        """
        self.brand = brand
        self.color = color
        self.price = price

    def price_count(self, discount, rate):
        """
        购车总价
        :param discount: 折扣
        :param rate: 税率
        :return: 总价
        """
        return self.price * (discount + rate)

    def __str__(self):
        return f"{self.brand} {self.color} {self.price}"

    def __eq__(self, other):
        return self.brand == other.brand and self.color == other.color and self.price == other.price

    def __lt__(self, other):
        """
        对象比较,复写后,对象可直接使用>,<对比
        :param other:
        :return:
        """
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price

    def __le__(self, other):
        return self.price <= other.price

    def __ge__(self, other):
        return self.price >= other.price


# 创建对象
car = Car("Xiaomi", "宝石绿", 259800)
print(car)  # 未复写__str__打印的内存地址
print(car.__dict__)  # 打印属性与值的字典键值对

print(f"购车总价:{car.price_count(discount=0.8, rate=0.1)}")

car2 = Car("XiaoPeng", "灰色", 229800)
print(car2)  # 复写__str__打印的是__str__中的实现

print(car > car2)
