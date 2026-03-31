# 案例：
"""
开发一个教务管理系统，维护学生成绩信息
1.增：提示分别录入学生名、语文、数学、英语成绩实现录入
2.删：提示输入要删除的学生名删除学生信息
3.改：提示输入要修改的学生名，修改各科分数
4.查：提示输入要查询的学生名，查询信息
5.列出所有：列出所有学生信息
6.统计：统计各科成绩的最高分、最低分、平均分以及各科最高最低分的学生名
5.退出系统
"""
tip = '''
####### 购物车系统 #######
#       1.添加学生信息   #
#       2.删除学生信息   #
#       3.修改学生信息   #
#       4.查询学生信息   #
#       5.查询所有学生   #
#       6.数据统计      #
#       7.退出系统      #
########################
'''
print(tip)
info = {}
while True:
    operate = int(input("请输入要操作的类型："))
    match operate:
        case 1:
            name = input("请输入要添加的学生名：")
            if name in info:
                print("该学生信息已存在，请重新输入")
                continue
            chinese = int(input("请输入语文分数："))
            math = int(input("请输入数学分数："))
            english = int(input("请输入英语分数："))
            info[name] = {"chinese": chinese, "math": math, "english": english}
            print(f"{name}添加成功,{info[name]}")
        case 2:
            name = input("请输入要删除的学生名：")
            if name not in info:
                print("该学生信息不存在，请重新输入")
                continue
            info.pop(name)
            print(f"{name}删除成功")
        case 3:
            name = input("请输入要修改的学生名：")
            if name not in info:
                print("该学生信息不存在，请重新输入")
                continue
            chinese = int(input("请输入语文分数："))
            math = int(input("请输入数学分数："))
            english = int(input("请输入英语分数："))
            info[name] = {"chinese": chinese, "math": math, "english": english}
            print(f"{name}修改成功,{info[name]}")
        case 4:
            name = input("请输入要查询的学生名：")
            if name not in info:
                print("该学生信息不存在，请重新输入")
                continue
            print(f"{name}信息为：{info[name]}")
        case 5:
            print(f"学生信息：{info}")
        case 6:
            chinese_list = []
            math_list = []
            english_list = []
            for i in info.values():
                chinese_list.append(i["chinese"])
                math_list.append(i["math"])
                english_list.append(i["english"])
            chinese_max_score = max(chinese_list)
            chinese_min_score = min(chinese_list)
            math_max_score = max(math_list)
            math_min_score = min(math_list)
            english_max_score = max(english_list)
            english_min_score = min(english_list)
            print(
                f"语文最高成绩为：{chinese_max_score},最低成绩为：{chinese_min_score},平均分为：{round(sum(chinese_list) / len(chinese_list), 1)}")
            print(
                f"数学最高成绩为：{math_max_score},最低成绩为：{math_min_score},平均分为：{round(sum(math_list) / len(math_list), 1)}")
            print(
                f"英语最高成绩为：{english_max_score},最低成绩为：{english_min_score},平均分为：{round(sum(english_list) / len(english_list), 1)}")
            chinese_max_name_set = set()
            chinese_min_name_set = set()
            math_max_name_set = set()
            math_min_name_set = set()
            english_max_name_set = set()
            english_min_name_set = set()
            for key, value in info.items():
                if value["chinese"] == chinese_max_score:
                    chinese_max_name_set.add(key)
                elif value["chinese"] == chinese_min_score:
                    chinese_min_name_set.add(key)
                if value["math"] == math_max_score:
                    math_max_name_set.add(key)
                elif value["math"] == math_min_score:
                    math_min_name_set.add(key)
                if value["english"] == english_max_score:
                    english_max_name_set.add(key)
                elif value["english"] == english_min_score:
                    english_min_name_set.add(key)
            print(f"语文最高分的学生是{chinese_max_name_set},最低分的学生是{chinese_min_name_set}")
            print(f"数学最高分的学生是{math_max_name_set},最低分的学生是{math_min_name_set}")
            print(f"英语最高分的学生是{english_max_name_set},最低分的学生是{english_min_name_set}")
        case 7:
            print("再见，欢迎下次体验")
            break
        case _:
            print("非法输入，请重新输入!!!")
