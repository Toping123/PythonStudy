myStr = "Toping study Python"
# 1.获取
print(myStr[1])
print(myStr[-3])

# 2.遍历
for item in myStr:
    print(item, end="\t")
print()

# 3.切片
print(myStr[:5:])
print(myStr[:5])
print(myStr[2:5])
print(myStr[2:8:3])
print(myStr[-1:8:-1])  # 步长为负数表示从末尾到开头

# 4.常见方法
print(myStr.find("Py"))  # find():查找指定字符串第一次出现的位置
print(myStr.count("n"))  # count():查找指定字符串出现的次数
print(myStr.upper())  # upper():转为大写（生成新的字符串）
print(myStr.lower())  # lower():转为小写（生成新的字符串）
print(myStr.split("n"))  # split():从指定字符串位置切割成list
print(myStr.strip("n"))  # strip(str):去除两端的字符串，默认str为" "即去除空格
print(myStr.replace("n", "m"))  # replace:字符串替换
print(myStr.startswith("n"))  # startswith(str):是否以指定字符串开始
print(myStr.endswith("n"))  # endswith(str):是否以指定字符串结尾

# 5.案例：简单验证邮箱（包含一个@和至少一个.）
email = input("请输入要验证的邮箱：")
if "." in email and email.count("@") == 1:
    print("合法")
else:
    print("非法")

# 6.判断字符串是否是回文串
str1 = "Py1thon"
# str1 = "上海自来水来自海上"
for i in range(0, len(str1) // 2):
    print(str1[i], str1[-i - 1])
    if str1[i] != str1[-i - 1]:
        print("不是回文串")
        break
else:
    print("是回文串")
