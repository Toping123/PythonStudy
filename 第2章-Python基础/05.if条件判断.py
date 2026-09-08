score = int(input("请输入高考分数："))
if score >= 650:
    print("去清华")
elif score >= 600:
    print("去武大")
elif score >= 550:
    print("武汉理工")
elif score >= 300:
    print("普通大学")
else:
    print("家里蹲")

print("------------- 1.判断奇数偶数-------")
num = int(input("请输入一个整数："))
if num % 2 == 0:
    print(f"{num}是偶数")
else:
    print(f"{num}是奇数")

print("----------- 2.判断正负数-----------")
num1 = int(input("请输入一个数："))
if num1 > 0:
    print(f"{num}是正数")
elif num1 < 0:
    print(f"{num}是负数")
else:
    print("0既不是正数也不是负数")

print("----------- 3.判断考试成绩-----------")
score1 = int(input("请输入一个分数："))
if score1 > 85:
    print(f"{score1}是优秀")
elif score1 >= 60:
    print(f"{score1}是及格")
else:
    print(f"{score1}是不及格")

print("------------ 4.判断三角形-----------")
a = int(input("请输入第一条边的长度："))
b = int(input("请输入第二条边的长度："))
c = int(input("请输入第三条边的长度："))
if a + b < c or a + c < b or b + c < a:
    print("无法构成三角形")
elif a == b == c:
    print("等边三角形")
elif a == b or b == c or c == a:
    print("等腰三角形")
else:
    print("普通三角形")

print("------------ 5.计算区间电费-----------")
spend = int(input("请输入当月使用的电量："))
if spend > 4800:
    print("单价为0.7883")
elif spend >= 2880:
    print("单价为0.5383")
else:
    print("单价为0.4883")
