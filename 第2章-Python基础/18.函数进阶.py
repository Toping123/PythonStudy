# 1.global关键字：表示访问的是全局变量
num = 1


def change_num1():
    num = 10  # 函数内部的局部变量
    return num


def change_num2():
    global num  # 使用global后表明下面修改的num是全局变量
    num = 10
    return num


change_num1()
print(num)
change_num2()
print(num)


# 2.函数传参
def reg_account(name, age, gender, city):
    print(f"注册成功,姓名:{name},年龄:{age},性别:{gender},城市:{city}")
    return {"name": name, "age": age, "gender": gender, "city": city}


# (1) 严格按顺序传参
reg_account("Toping", 18, "男", "深圳")
# (2) 关键字传参（不要求顺序，只要求个数）
reg_account(age=18, name="Toping", city="深圳", gender="男")
# (3)混合传参数(关键字参数必须放后面)
reg_account("Toping", 18, gender="男", city="深圳")


# 2.函数默认参数
def reg_account(name, age, gender, city="深圳"):
    print(f"注册成功,姓名:{name},年龄:{age},性别:{gender},城市:{city}")
    return {"name": name, "age": age, "gender": gender, "city": city}


# city参数未传，采用默认值
reg_account("Toping", 18, "男")
# 传了city参数，采用传参值
reg_account("Toping", 18, gender="男", city="湖北")


# 不定长参数
def count_score(*score, **score_args):
    """
    根据传入的分数列表计算最大值、最小值、平均值
    :param score: 分数，采用不定长位置参数
    :param score_args:  不定长关键字参数
        round: 保留的小数位数
        print: 是否打印输出
    :return: 最大值、最小值、平均值
    """
    max_score = max(score)
    min_score = min(score)
    avg_score = sum(score) / len(score)
    if score_args.get("round") is not None:
        avg_score = round(avg_score, score_args.get("round"))
    if score_args.get("print") is not None:
        print(f"计算的最大值:{max_score},最小值:{min_score},平均值:{avg_score}")
    return max_score, min_score, avg_score


count_score(88, 78, 99, 76, 65, 59, 87, round=1, print=True)
