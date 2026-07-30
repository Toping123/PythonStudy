# 获取字面量或变量数据类型 type()
print(type(1))  # int <class 'int'>
print(type(3.14))  # float <class 'float'>
print(type(True))  # bool <class 'bool'>
print(type("Toping"))  # str <class 'str'>
print(type(None))  # NoneType <class 'NoneType'>
print("------------------------------------------------")

# 获取数据类型是否是对应的类型 isInstance(数据, 类型) = bool
print(isinstance(1, int))
print(isinstance(1, float))  # False
print(isinstance(3.14, float))
print(isinstance(True, bool))
print(isinstance("true", str))
print("------------------------------------------------")

# 字符串
# 1.定义方式，"Python" , 'Python', '''Python''', """Python""" 单引号等效于双引号
my_str1 = "Python"
print(my_str1)
my_str2 = 'Python'
print(my_str2)
my_str3 = '''第一行
我随意换行单引号第二行
第三行'''
print(my_str3)
my_str3 = """第一行
我随意换行双引号第二行
第三行"""
print(my_str3)
print("------------------------------------------------")

# 2. 转义字符 \' 、\"、  \n 、\t \
print('123\'')
print("123'")
print("123\"")
print('123"')
print('123\n转行展示')
print('123\tTab空格展示"')
print("----------------------------------------------")

# 3. 字符串拼接
jointStr1 = "我要" "学习" "Python"
print(jointStr1)
jointStr2 = "我要" + "学习" + "Python"
print(jointStr2)
jointStr3 = "我要" + "学习" + str(10) + "天Python"  # str(int)将int转成str
print(jointStr3)

# 4. 字符串格式化
str1, str2, str3 = "好", "习", "上"
print(f"好{str1}学{str2}, 天天向{str3}")  # f表示format，推荐方式
print("好%s学%s, 天天向%s" % (str1, str2, str3))  # 用得少，几乎不用
