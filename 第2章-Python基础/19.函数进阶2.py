# 1.函数作为参数
def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def operate(a, b, operator_func):
    """
    简易计算器
    :param a: 第一个数据
    :param b: 第二个数据
    :param operator_func: 操作类型
    :return: 计算结果
    """
    return operator_func(a, b)


print(operate(1, 2, add))
print(operate(1, 2, sub))
print(operate(1, 2, mul))


# 2.匿名函数
def print_line1():
    print("--------------------------")


print_line1()

# 格式为lambda:函数体，使用变量接收
print_line2 = lambda: print("------------------")
print_line2()

# 3.匿名函数案例
str_list = ["Python", "Java", "Kotlin", "JavaScript", "dart"]
print(str_list)
str_list.sort(key=lambda item: len(item))  # 排序的方式为字符串的长度
print(str_list)
print(str_list)
print(str_list)


# 4.函数递归：函数调用本身（必须有终结条件）
def jc(n):
    if n == 1:
        return 1
    return n + jc(n - 1)


print(jc(10))


# 5.案例：定义一个用于根据传入的商品信息（商品名、价格、数量）,优惠信息（优惠券、积分）,运费自计算价格的函数
# 要求：优惠券和积分都需金额满5000才可用，优惠券金额不可超过商品总金额，100积分抵1元(需要整百抵)，也不能超过总金额
def cal_total(*goods, coupon: float, integral: int, fare: float = 0):
    total = 0
    for good in goods:
        total += good["price"] * good["num"]
    if total >= 5000:
        total = total - coupon - integral // 100
    total += fare
    return total


print(cal_total({"name": "小米13", "price": 2000, "num": 1},
                {"name": "小米牙刷", "price": 199, "num": 3},
                {"name": "小米电池", "price": 9.9, "num": 10},
                {"name": "小米笔记本", "price": 4000, "num": 1}, coupon=88, integral=4510, fare=9.9))
