# --------------------字面量-----------------------
# 字面量：程序中直接书写的固定值（数据）
print(100)  # 整型（int）
print(3.14)  # 浮点数/小数（float）
print(True)  # 布尔（bool）
print(False)  # 布尔（bool）
print("Hello World")  # 字符串（str）
print(None)  # 空值（NoneType）

# 布尔值本质也是整型（True:1, False:0）
print(True + 1)
print(False + 1)

# ----------------------变量--------------------------
#  变量可修改为不同的类型（通常不推荐）
num = 12
print(num)
num = "Hello Python"
print(num)

# 一行定义多个变量
a, b = 3.14, 2
print(a)
print(b)

# 三值交换：a=1, b=2 , c=3 将abc的值交换成cab
a = 1
b = 2
c = 3
temp = c
c = a
a = b
b = temp
print(a, b, c)
