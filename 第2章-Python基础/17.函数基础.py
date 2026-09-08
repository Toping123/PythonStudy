import math


# 单个参数：求圆的面积
def circle_area(radius):
    """
    求圆的面积
    :param radius: 半径
    :return: 圆的面积
    """
    return math.pi * radius * radius


print(f"10米圆的面积为：{circle_area(10)}")


# 多个参数：求长方形的面积
def rectangle_area(width, height):
    """
    求长方形的面积
    :param width: 宽
    :param height: 高
    :return: 长方形的面积
    """
    return width * height


print(f"长20米宽10米的长方形面积为：{rectangle_area(10, 20)}")


# 多个返回值：求圆的面积和周长
def circle_area_len(radius):
    """
    求圆的面积和周长
    :param radius: 圆的半径
    :return: (圆的面积, 圆的周长)
    """
    return math.pi * radius * radius, math.pi * radius * 2  # 利用组包，返回的是元组


area, length = circle_area_len(10)
print(f"10米圆的面积为：{area}，周长为：{length}")


# 函数的嵌套调用
def function_a():
    print("调用function_a开始")
    function_b()
    print("调用function_a结束")


def function_b():
    print("调用function_b开始")
    function_c()
    print("调用function_b结束")


def function_c():
    print("调用function_c")


function_a()


# 案例1：统计元音个数
def count_vowel(letters):
    count = 0
    for s in letters:
        if s in "aeiouAEIOU":
            count += 1
    return count


letter = "uhiusahksajkhksajhjkkgUEA"
print(f"元音字母个数为{count_vowel(letter)}")


# 案例2：计算传入成绩的最高分，最低分，平均分（保留1位）
def count_score(*scores):
    """
    计算传入成绩的最高分，最低分，平均分（保留1位）
    :param scores: 成绩列表
    :return: 成绩的最高分，最低分，平均分（保留1位）
    """
    return max(scores), min(scores), round(sum(scores) / len(scores), 1)


print(count_score(88, 62, 93, 84, 55, 63))


# 案例3：判断回文串
def is_palindrome(s):
    for i in range(0, len(s)):
        if s[i] != s[-i - 1]:
            return False
    return True

print(is_palindrome("123321"))
