"""
## 什么是 lambda

`lambda` 用来创建**小型匿名函数**（不需要用 `def` 定义名字）

- `def`：适合复杂多行逻辑，有函数名
- `lambda`：只能写**单行表达式**，适合临时、简短逻辑

### 语法模板

```
lambda 参数列表 : 返回值表达式
```

1. 关键字：`lambda`
2. 冒号前：**形参**，多个逗号隔开，可以无参数
3. 冒号后：**只能是一条表达式**，表达式结果自动作为返回值，**不能写 return**
4. lambda 本身是一个函数对象
"""
# 无参
f = lambda: "Hello"
print(f())

# 参数（多参数,隔开）
add = lambda a, b: a + b
print(add(1, 2))

# 带默认参数
add2 = lambda a, b=1: a + b
print(add2(1))

# 可以是简单的表达式，通常为三元判断
abs_func = lambda a: a if a > 0 else -a
print(abs_func(2))
print(abs_func(-3))
