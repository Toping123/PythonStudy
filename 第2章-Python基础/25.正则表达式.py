import re

str1 = "18807143567的手机号,你记住了吗,QQ号码是1768598567"
str2 = "手机号是18807143567,你记住了吗,QQ号码是1768598567"

# match: 从字符串的开头匹配，匹配第一个匹配项 -> Match对象
result = re.match(r"1[3-9]\d{9}", str1)
if result:
    print(result.group())  # 获取匹配的结果
    print(result.span())
    print(result.start())
    print(result.end())
else:
    print("match未获取到")

# search: 从任意位置开始匹配，匹配第一个匹配项 -> Match对象
result = re.search(r"1[3-9]\d{9}", str2)
if result:
    print(result.group())  # 获取匹配的结果
    print(result.span())
    print(result.start())
    print(result.end())
else:
    print("search未获取到")

# findAll: 从字符串的开头匹配，匹配所有的匹配项 -> list
result = re.findall(r"1[3-9]\d{9}", str1)
print(result)
