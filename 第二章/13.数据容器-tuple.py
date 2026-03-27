# tuple:元组，只能访问不可修改，有序可重复
# 1.定义
t1 = (1, 2, 2, 3, 6, 5)
print(t1)
print(type(t1))

# 2.访问
print(t1[3])
print(t1[-2])

# 3.切片
print(t1[1:3])  # 生成新元组

# 4.常见方法
print(t1.count(2))  # 2
print(t1.index(2))  # 1

# 5.注意点
# 元组中只有单个元素时末尾需要加,
t2 = ()
print(type(t2))
t3 = (1)  # 会被当成括号
print(type(t3))
t3 = (1,)
print(type(t3))
