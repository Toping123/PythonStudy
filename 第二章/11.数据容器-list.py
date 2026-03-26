# 1.list定义(可存储不同的数据类型)
myList = [1, 2, "3", "hello", True]
print(type(myList))

# 2.访问（负数是从尾向头数）
print(myList[1])  # 2
print(myList[-1])  # True

# 3.修改
myList[2] = 3
print(myList)

# 4.删除
del myList[1]
print(myList)

# 5.遍历
for item in myList:
    print(item, end="\t")
print()

# 6.切片 list[开始索引:结束索引:步长]
# 开始索引默认值=0、结束索引默认值=length、步长默认值=1
myList2 = [1, 2, 3, 4, 5, 6]
print(myList2[0:3:1]) # [1, 2, 3]
print(myList2[:3:])   # [1, 2, 3]
print(myList2[:5:2])  # [1, 3, 5]
print(myList2[1::])   # [2, 3, 4, 5, 6]
print(myList2[0:-1:]) # [1, 2, 3, 4, 5]
