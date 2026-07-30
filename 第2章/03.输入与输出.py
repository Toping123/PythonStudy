# 获取键盘上输入的数据  input()
name = input("请输入姓名:")
age = input("请输入年龄:")
print(f"您的姓名是:{name},年龄是{age}")

# 案例：ATM取钱
total = 10000
password = input("请输入密码：")
print("密码输入正确")
num = input("请输入你要取出的金额：")
print(f"取出后剩余的金额:{total - int(num)}")

# 计算输入的两个数字之和
num1 = input("请输入第一个数字：")
num2 = input("请输入第二个数字：")
print(f"两数之和为：{int(num1) + int(num2)}")
