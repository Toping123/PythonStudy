# 集合set：无序、不可重复、可修改
s1 = {4, 3, 4, 35, 64, 2, 0, 10}
print(s1)

# 定义空集合
s2 = {}  # 这是字典
print(type(s2))
s3 = set()
print(type(s3))

# 常见方法add
s4 = {1, 32, 64, 88, 3, 5, 7}
s4.add(22)
print(s4)

# 常见方法remove，移除指定元素
s4.remove(3)
print("remove后：", s4)

# 常见方法pop，删除第一个排序后的（内部排序的第一个,非元素顺序）元素
s4.pop()
print("pop后：", s4)

# 常见方法清除clear
s4.clear()
print(s4)

s5 = {1, 22, 30, 64, 544, 55, 2}
s6 = {2, 30, 44, 5}
# 常见方法difference,差集，存在于前者不存在与后者
print(s5.difference(s6))
print(s6.difference(s5))

# 常见方法union:并集
print(s5.union(s6))

# 常见方法intersection:交集
print(s5.intersection(s6))

# 案例：选修课
# 选修足球的学生
football_set = {"王林", "曾牛", "徐立国", "遁天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}
# 选修篮球的学生
basketball_set = {"张铁", "墨居仁", "王林", "姜老道", "曾牛", "王蝉", "韩立", "天运子", "李化元", "厉飞雨", "云露"}
# 选修法语学生
french_set = {"许木", "王卓", "十三", "虎咆", "姜老道", "天运子", "红蝶", "厉飞雨", "韩立", "曾牛"}
# 选修艺术学生名单
art_set = {"遁天", "天运子", "韩立", "虎咆", "姜老道", "紫灵"}
# (1)找出同时选修法语和艺术的学生
print("同时选修法语和艺术的学生1:", french_set.intersection(art_set))
print("同时选修法语和艺术的学生2:", french_set & art_set)  # &符号此时与intersection等价
# (2)找出同时选修四门功课的学生
print("同时选修四门功课的学生:", football_set & basketball_set & french_set & art_set)
# (3)找出选择了足球未选择篮球的学生
print("选择了足球未选择篮球的学生1:", football_set.difference(basketball_set))
print("选择了足球未选择篮球的学生2:", football_set - basketball_set)  # 减号等价于difference
print("选择了足球未选择篮球的学生3:", {s for s in football_set if s not in basketball_set})  # 集合推导式
# (4)统计每个学生选择的课程数量
# 获取学生名单
all_students = football_set | basketball_set | french_set | art_set  # | 等价于union
print(all_students)
all_list = [*football_set, *basketball_set, *french_set, *art_set]
print(all_list)
for s in all_students:
    print(f"{s}共选择了{all_list.count(s)}门课程")
