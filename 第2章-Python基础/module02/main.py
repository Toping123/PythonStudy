# 导入整个模块（模块.属性/方法）
from os import utime

import my_fun

# 使用模块中的属性
print(my_fun.PI)
print(my_fun.NAME)

# 调用模块中的方法
my_fun.log_operate1()
my_fun.log_operate2()
my_fun.log_operate3()

# 第二种导入方式（直接使用属性或调用方法）
from my_fun import PI, log_operate1, log_operate3

print(PI)

log_operate1()
# log_operate2() # 未导入无法调用
log_operate3()

# 第三种导入方式
from my_fun import *

print(NAME)
log_operate2()