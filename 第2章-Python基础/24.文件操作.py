import json


def write_file():
    """相对路径写入文件"""
    with open("./Toping.txt", "w", encoding="UTF-8") as f:
        f.write("今天星期四\n")
        f.write("又是美好的一天")


def read_file():
    """相对路径读取文件"""
    with open("./Toping.txt", "r", encoding="UTF-8") as f:
        print(f.read())
        
def write_absolute_file():
    """绝对路径写入文件"""
    with open("C:/Users/luotaoping/Desktop/Toping.txt", "w", encoding="UTF-8") as f:
        f.write("今天星期四\n")
        f.write("又是美好的一天")


def read_absolute_file():
    """绝对路径读取文件"""
    with open("C:/Users/luotaoping/Desktop/Toping.txt", "r", encoding="UTF-8") as f:
        print(f.read())


def write_json_file():
    """
    写入Json数据到文件中
    :return:
    """
    user = {"name": "Toping", "sex": "男"}
    with open("./Toping.json", "w", encoding="UTF-8") as f:
        json.dump(user, f, ensure_ascii=False, indent=4)


def read_json_file():
    """
    读取文件并转为Json
    :return:
    """
    with open("./Toping.json", "r", encoding="UTF-8") as f:
        # print(f.read())
        user = json.load(f)
        print(user)
        print(type(user))


if __name__ == '__main__':
    # write_file()
    # read_file()
    write_absolute_file()
    read_absolute_file()
    # write_json_file()
    # read_json_file()
