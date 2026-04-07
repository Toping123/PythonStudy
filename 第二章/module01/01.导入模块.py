import random # 1.导入整个模块，调用使用：模块.方法
import random as rd # 2.导入整个模块并使用别名，调用使用：别名.方法
from random import randint  # 2.导入模块中的某些方法/类，调用使用：方法
from random import randint as rint  # 2.导入模块中的某些方法/类并使用别名，调用使用：方法别名


print(random.randint(1, 100))
print(rd.randint(1, 100))
print(randint(1, 100))
print(rint(1, 100))