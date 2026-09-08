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
print(myList2[0:3:1])  # [1, 2, 3]
print(myList2[:3:])  # [1, 2, 3]
print(myList2[:5:2])  # [1, 3, 5]
print(myList2[1::])  # [2, 3, 4, 5, 6]
print(myList2[0:-1:])  # [1, 2, 3, 4, 5]

# 7.list.append(ele)添加方法
myList3 = [1, 2, 3, 4, 5, 6]
print(myList3)
myList3.append(7)
print(myList3)

# 8.list.insert(index,ele)插入方法
myList3.insert(3, 7)
print(myList3)

# 9.list.remove(ele)删除指定元素方法（只删除第一个匹配到的元素）
myList3.remove(4)
print(myList3)

# 10.list.pop(index)删除指定位置的元素方法（index默认为length)
myList3.pop(2)
print(myList3)

# 11.list.sort()排序
myList3.sort()
print(myList3)

# 12.list.reserve()反转
myList3.reverse()
print(myList3)

# 13.最大最小值
maxNum = max(myList3)
minNum = min(myList3)
averageNum = sum(myList3) / len(myList3)
print(f"最大值为:{maxNum},最小值为:{minNum},平均值:{averageNum}")

# 14.案例：合并两个list,并去重
list1 = [1, 2, 4, 9, 5, 8]
list2 = [1, 5, 6, 3, 7, 9]
# (1) 合并,用+和解包的方式均可
# 解包：将列表这一类容器解开为1个个单独的元素
# 组包：将多个值合并到一个容器
list3 = list1 + list2
print(list3)
list4 = [*list1, *list2]
print(list4)
# (2) 去重
newList = []
for item in list3:
    if item not in newList:
        newList.append(item)
print(newList)

# 15.案例：找出元素1~20列表中能被3或5整除的元素，并将这些元素对应的平方组成一个新数组
list5 = range(1, 21)
newList = []
for item in list5:
    if item % 3 == 0 or item % 5 == 0:
        newList.append(item ** 2)
print(newList)

# 列表推导式
newList2 = [i ** 2 for i in list5 if i % 3 == 0 or i % 5 == 0]
print(newList2)
