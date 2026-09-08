# 1.普通运算符
print("10 + 4 = ", 10 + 4)  # 加 14
print("10 - 4 = ", 10 - 4)  # 减 6
print("10 * 4 = ", 10 * 4)  # 乘 40
print("10 / 4 = ", 10 / 4)  # 除 2.5
print("10 // 4 = ", 10 // 4)  # 整除 2
print("10 % 4 = ", 10 % 4)  # 取余/求模 2
print("10 ** 4 = ", 10 ** 4)  # 幂指数 10000

print("0.5 - 0.4 = ", 0.5 - 0.4)  # 结果为0.09999999999999998 float运算可能存在精度损失

# 2.赋值运算符
print("---------------- 2.赋值运算符---------------")
num = 85
num += 10
print(f"执行 num += 10后,num={num}")  # 95
num -= 10
print(f"执行 num -= 10后,num={num}")  # 85
num *= 10
print(f"执行 num *= 10后,num={num}")  # 850
num /= 10
print(f"执行 num /= 10后,num={num}")  # 85.0
num //= 10
print(f"执行 num //= 10后,num={num}")  # 8.0
num %= 10
print(f"执行 num %= 10后,num={num}")  # 8.0
num **= 2
print(f"执行 num **= 2后,num={num}")  # 64.0

# 3.比较运算符 ==、>=、<=、!=
print("------------------ 3.比较运算符---------------")
print(13 == 13)  # True
print(13 == 14)  # False
print(13 >= 14)  # False
print(13 <= 14)  # True
print(13 != 14)  # True

print("------------------ 4. 逻辑运算符---------------")
# 4. 逻辑运算符 and or not
print(1 > 3 and 4 > 2)  # False
print(1 > 3 or 4 > 2)   # True
print(not 1 > 3)        # True
