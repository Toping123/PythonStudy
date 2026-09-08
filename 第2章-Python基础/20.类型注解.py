# 变量后不指定类型，编译器可自动类型推断
age = 18

# 变量后指定类型后，编译器会自动给出提示
# 注：python是解释型语言，仅为提示，不会报错，实际类型以类型推断为准主要目的是规范
score: int = 88.0
print(type(score))  # float

score_list: list[float] = [88.0, 78]
name_list: list[str | int] = ["Toping", 78]
