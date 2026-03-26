# 1.简单登录系统
"""
1.用户名/密码为Toping1/111、Toping2/222、Toping3
2.输入错误进行提示，直到输入正确
3.最多尝试5次，超过5次锁定5分钟
"""
import random

maxTimes = 5
currentTime = 0
while currentTime < maxTimes:
    name = input("请输入用户名：")
    pwd = input("请输入密码：")
    if ((name == "Toping1" and pwd == "111") or
            (name == "Toping2" and pwd == "222") or
            (name == "Toping3" and pwd == "333")):
        print("登录成功!!!")
        break
    else:
        currentTime += 1
        if currentTime < maxTimes:
            print("用户名或者密码错误，请重新输入")
if currentTime == maxTimes:
    print("输入错误超过5次，锁定5分钟...")

# 2.统计字符串中有多少个a和k
myStr = "hsklhsakjhgdghjdsgjhajkhakljhklahk"
aCount = 0
kCount = 0
for char in myStr:
    if char == "a":
        aCount += 1
    elif char == "k":
        kCount += 1
print(f"a的数量为：{aCount}，k的数量为：{kCount}")

# 3.猜数字游戏
randomNum = random.randint(1,101)
while True:
    num = int(input("请输入一个1~100的数字："))
    if num == randomNum:
        print("恭喜你猜对了")
        break
    elif num > randomNum:
        print("你猜大了继续加油")
    else:
        print("你猜小了继续加油")