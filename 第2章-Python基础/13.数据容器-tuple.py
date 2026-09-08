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

# 6.组包
t4 = (1, 2, 3, 4, 5)
t5 = 1, 2, 3, 4, 5  # 组包
print(t4)
print(t5)

# 7.解包
a, b, c, d, e = t5
print(a, b, c, d, e)
# *收集剩余的元素
a, *b, c = t5
print(a, c)
print(b)

# 8.案例，元素交换abc交换成cab
a = 1
b = 2
c = 3
c, a, b = a, b, c  # 左侧是解包，右侧为组包
# c, a, b = (a, b, c) # 相当于下面，只是少了组包
print(a, b, c)

# 9.案例：统计分数
students = (
    ("S001", "王一", 85, 92, 78),
    ("S002", "王二", 92, 88, 95),
    ("S003", "王三", 78, 85, 82),
    ("S004", "王四", 88, 79, 91),
    ("S005", "王五", 95, 96, 89),
    ("S006", "王六", 76, 82, 77),
    ("S007", "王七", 89, 91, 94),
    ("S008", "王八", 75, 69, 82),
    ("S009", "王九", 86, 89, 98),
    ("S010", "王十", 66, 59, 72),
)
# 9.1计算每个学生的总分、各科平均分
print("学号\t\t姓名\t\t语文\t\t数学\t\t英语\t\t总分\t\t平均分")
for no, name, chinese, math, english in students:
    scoreSum = chinese + math + english
    avg = scoreSum / 3
    # 数字保留一位有效数字的方式为   :.1f
    print(f"{no}\t{name}\t\t{chinese}\t\t{math}\t\t{english}\t\t{sum}\t\t{avg:.1f}")

# 9.2统计各科成绩的最高分最低分平均分
chineseList = []
mathList = []
englishList = []
for *content, chinese, math, english in students:
    chineseList.append(chinese)
    mathList.append(math)
    englishList.append(english)
print(f"语文最高分：{max(chineseList)},最低分：{min(chineseList)},平均分：{sum(chineseList) / len(chineseList)}")
print(f"数学最高分：{max(mathList)},最低分：{min(mathList)},平均分：{sum(mathList) / len(mathList)}")
print(f"英语最高分：{max(chineseList)},最低分：{min(englishList)},平均分：{sum(englishList) / len(englishList)}")

# 9.3 查找平均分>=90的学生
print("学号\t\t姓名\t\t语文\t\t数学\t\t英语\t\t总分\t\t平均分")
for no, name, chinese, math, english in students:
    scoreSum = chinese + math + english
    avg = scoreSum / 3
    # 数字保留一位有效数字的方式为   :.1f
    if avg >= 90:
        print(f"{no}\t{name}\t\t{chinese}\t\t{math}\t\t{english}\t\t{scoreSum}\t\t{avg:.1f}")