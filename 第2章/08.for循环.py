# 1.遍历输入的字符串
myStr = input("请输入你要遍历的字符串：")
for i in myStr:
    print(i, end="\t")
print()

# 2.计算1..100的所有奇数和
total = 0
for i in range(1, 101):
    if i % 2 == 0:
        total += i
print(f"1..100的所有奇数和为：{total}")

# 3.计算1..100的所有奇数和简化
total2 = 0
for i in range(1, 101, 2):
    total2 += i
print(f"1..100的所有奇数和为：{total2}")

# 4.输出一个长度为10，宽度为5的长方形*
for i in range(1, 6):
    for j in range(1, 11):
        print("*", end="\t")
    print()

# 5.打印99乘法表
for i in range(1, 10):
    for j in range(i, 10):
        print(f"{i} * {j} = {i * j}", end="\t")
    print()

# 6.打印直角边为5的等腰三角形
for i in range(1, 6):
    for j in range(1, i + 1):
        print("*", end="\t")
    print()

# 7.根据输入的数字打印对应的数字金字塔
num = int(input("请输入数字金字塔的高度："))
for i in range(1, num + 1):
    for j in range(1, i + 1):
        print(f"{j}", end="\t")
    print()
