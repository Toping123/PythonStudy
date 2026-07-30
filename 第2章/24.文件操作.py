def write_file() -> None:
    with open("./Toping.txt", "w", encoding="UTF-8") as f:
        f.write("今天星期四\n")
        f.write("又是美好的一天")
        f.close()


def read_file() -> None:
    with open("./Toping.txt", "r", encoding="UTF-8") as f:
        print(f.read())
        f.close()


if __name__ == '__main__':
    write_file()
    read_file()
