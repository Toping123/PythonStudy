# 默认属性，外部导入(from ... import *)时，指定对外可导入的属性和方法，未手动设置的话，会自动导入所有
__all__ = ["NAME", "log_operate2"]

PI = 3.1415926
NAME = "我是常量"


def log_operate1():
    print("log_operate1")


def log_operate2():
    print("log_operate2")


def log_operate3():
    print("log_operate3")


# 测试函数
# __name__ : Python中的内置变量,表示当前模块的名称(直接运行当前模块时,__name__为"__main__",其他模块导入则为当前模块名my_fun)
# 执行当前文件,则执行,被导入则不执行
if __name__ == "__main__":
    print("直接执行的当前模块")
else:
    print(f"被外部导入,__name__ = {__name__}")
