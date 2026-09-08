import random

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