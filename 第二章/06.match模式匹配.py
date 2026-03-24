# match....case...模式匹配
weekday = input("请输入今天星期几：")
match weekday:
    case '1':
        print("周一会议日")
    case '2':
        print("周二评审日")
    case '3':
        print("周三开发日")
    case '4':
        print("周四测试日")
    case '5':
        print("周五发版日")
    case '6' | '7':  # 匹配多项的方式
        print("周末休息日")
    case _:
        print("非法输入")

# 简单计算器案例
print("------------简单计算器案例----------")
num1 = float(input("请输入第一个数："))
num2 = float(input("请输入第二个数："))
oper = input("请输入计算类型(+-*/)：")
match oper:
    case '+':
        print(f"{num1} + {num2} = ", num1 + num2)
    case '-':
        print(f"{num1} - {num2} = ", num1 - num2)
    case '*':
        print(f"{num1} * {num2} = ", num1 * num2)
    case '/' if num2 != 0: # case中可附加条件，只有符合该条件，才匹配case
        print(f"{num1} / {num2} = ", num1 / num2)
    case _:
        print("不支持的操作!!!")
