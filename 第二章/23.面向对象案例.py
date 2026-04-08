"""
采用面向对象的思想，完成教务管理系统的开发
1.增：提示分别录入学生名、语文、数学、英语成绩实现录入
2.删：提示输入要删除的学生名删除学生信息
3.改：提示输入要修改的学生名，修改各科分数
4.查：提示输入要查询的学生名，查询信息
5.列出所有：列出所有学生信息
6.退出系统
"""


class Student:
    def __init__(self, name, chinese_score, match_score, english_score):
        self.name = name
        self.chinese_score = chinese_score
        self.match_score = match_score
        self.english_score = english_score

    def __str__(self):
        return f"{self.name}的成绩为:语文({self.chinese_score}),数学({self.match_score}),英语({self.english_score})"

    def update_score(self, chinese_score=None, match_score=None, english_score=None):
        """
        更新成绩
        :param chinese_score: 语文成绩
        :param match_score: 数学成绩
        :param english_score: 英语成绩
        :return:
        """
        if chinese_score is not None:
            self.chinese_score = chinese_score
        if match_score is not None:
            self.match_score = match_score
        if english_score is not None:
            self.english_score = english_score


if __name__ == "__main__":
    tempStudent = Student("Toping", 88, 99, 90)
    print(tempStudent)
    tempStudent.update_score(english_score=95)
    print(tempStudent)


def input_and_check_score():
    chinese_score = int(input("请输入语文成绩："))
    if chinese_score not in range(0, 100):
        print("成绩输入有误,须在0~100之间")
        return None
    math_score = int(input("请输入数学成绩："))
    if math_score not in range(0, 100):
        print("成绩输入有误,须在0~100之间")
        return None
    english_score = int(input("请输入英语成绩："))
    if english_score not in range(0, 100):
        print("成绩输入有误,须在0~100之间")
        return None
    return chinese_score, math_score, english_score


class EducationManager:
    NAME = "教务管理系统"
    VERSION = "1.0.0"

    def __init__(self):
        self.student_list = []

    def add_student(self):
        name = input("请输入学生姓名：")
        for student in self.student_list:
            if student.name == name:
                print("该学生已存在，请重新输入")
                return False
        scores = input_and_check_score()
        if scores is not None:
            chinese_score, math_score, english_score = scores
            self.student_list.append(Student(name, chinese_score, math_score, english_score))
            print("学生信息添加成功")
            return True
        print("学生信息添加失败")
        return False

    def get_student(self):
        name = input("请输入学生姓名：")
        for student in self.student_list:
            if student.name == name:
                print(f"当前学生信息为{student}")
                return student
        return None

    def update_student(self):
        name = input("请输入要修改的学生：")
        for student in self.student_list:
            if student.name == name:
                scores = input_and_check_score()
                if scores is not None:
                    chinese_score, math_score, english_score = scores
                    self.student_list.append(Student(name, chinese_score, math_score, english_score))
                    print(f"学生{student.name}信息修改成功")
                    return True
                print("学生信息修改失败")
                return False
        print("未找到该学生")
        return False

    def delete_student(self):
        name = input("请输入要删除的学生：")
        for student in self.student_list:
            if student.name == name:
                self.student_list.remove(student)
                print(f"学生{student.name}信息删除成功！")
                return True
        print("未找到该学生")
        return False

    def show_students(self):
        for student in self.student_list:
            print(student)

    def run(self):
        print(f"欢迎使用{EducationManager.NAME}V{EducationManager.VERSION}")
        while True:
            print("##################")
            print("#1.添加学生、2.修改学生、3.删除学生、4.查询指定学生、5.查询所有学生、6.退出系统")
            print("##################")
            choice = input("请输入要操作的类型：")
            try:
                match choice:
                    case "1":
                        self.add_student()
                    case "2":
                        self.update_student()
                    case "3":
                        self.delete_student()
                    case "4":
                        self.get_student()
                    case "5":
                        self.show_students()
                    case "6":
                        break
                    case _:
                        print("非法操作类型")
            except ValueError:
                print("输入的数据有误，请检查")
            except Exception as e:
                print(f"非法操作，请重新输入", e)


if __name__ == "__main__":
    manager = EducationManager()
    manager.run()
