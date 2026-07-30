# 1.打印10遍 “人生苦短，我用Python”
i = 0
while i < 10:
    print("人生苦短，我用Python")
    i += 1
else:
    print("跳出了循环的执行体")

# 2.计算1..100的偶数累加和
total = 0
i = 0
while i <= 100:
    if i % 2 == 0:
        total += i
    i += 1
print(f"1..100的偶数累加和={total}")
