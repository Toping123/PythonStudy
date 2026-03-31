# dict:字典，key-value型存储容器，key不可重复(重复时后面会覆盖前面)，数据可修改
# key必须时不可变类型（str,int,float,tuple）
dict1 = {"王林": 670, "李慕婉": 608, "徐立国": 580, "韩立": 700}
print(dict1)
print(type(dict1))

# 获取
print(dict1["李慕婉"])
print(dict1.get("李慕婉"))
print(dict1.keys())  # 获取所有的key
print(dict1.values())  # 获取所有的value
print(dict1.items())  # 获取所有的item,即(key,value)

# 修改/添加，存在该键就是修改，不存在则是添加
dict1["王林"] = 688
print(dict1)

# 删除
del_item = dict1.pop("徐立国")  # 删除指定key所在的item,返回值为value
print(del_item)  # 580
print(dict1)

del dict1["韩立"]  # 使用del关键字也可删除
print(dict1)

# 遍历
for key, value in dict1.items():
    print(key, value)

# 案例：
'''
开发一个购物车管理系统，实现增删改查
1.增：提示分别录入商品名称、价格、数量实现录入
2.删：提示输入要删除的商品名称删除商品
3.改：提示输入要修改的商品名称，修改价格和数量
4.查：将商品信息展示出来
5.退出系统
'''
tip = '''
####### 购物车系统 #######
#       1.添加购物车     #
#       2.删除购物车     #
#       3.修改购物车     #
#       4.查询购物车     #
#       5.退出系统       #
########################
'''
print(tip)
shopping_cart = {}
while True:
    operate = int(input("请输入要操作的类型："))
    match operate:
        case 1:
            name = input("请输入要添加的商品名称：")
            if name in shopping_cart:
                print("该商品已存在，请重新输入")
                continue
            price = float(input("请输入商品单价："))
            num = int(input("请输入商品数量："))
            shopping_cart[name] = {"name": name, "price": price, "num": num}
            print(f"{name}添加成功,{shopping_cart[name]}")
        case 2:
            name = input("请输入要删除的商品名称：")
            if name not in shopping_cart:
                print("该商品不存在，请重新输入")
                continue
            shopping_cart.pop(name)
            print(f"{name}删除成功")
        case 3:
            name = input("请输入要修改的商品名称：")
            if name not in shopping_cart:
                print("该商品不存在，请重新输入")
                continue
            price = float(input("请输入商品单价:"))
            num = int(input("请输入商品数量:"))
            shopping_cart[name] = {"name": name, "price": price, "num": num}
            print(f"{name}修改成功,{shopping_cart[name]}")
        case 4:
            print(f"购物车信息：{shopping_cart}")
        case 5:
            print("再见，欢迎下次体验")
            break
        case _:
            print("非法输入，请重新输入!!!")
