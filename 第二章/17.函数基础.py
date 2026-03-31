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
