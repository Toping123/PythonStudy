import csv


def write_csv_by_file():
    """文件写入的方式写入csv"""
    with open("./csv_data/csv1.csv", "w", encoding="utf-8") as f:
        f.write("姓名,性别,年龄\n")
        f.write("Toping,男,18\n")


def write_csv_by_csv_writer():
    """使用csvWriter写csv"""
    with open("./csv_data/csv2.csv", "w", encoding="utf-8", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=["姓名", "性别", "年龄"])
        # 写入表头
        csv_writer.writeheader()
        csv_writer.writerow({"姓名": "Toping", "性别": "男", "年龄": "18"})

def read_csv():
    with open("./csv_data/csv1.csv", "r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            print(row)
            print(row["姓名"])


if __name__ == '__main__':
    # write_csv_by_file()
    # write_csv_by_csv_writer()
    read_csv()
