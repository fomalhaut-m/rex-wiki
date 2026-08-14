# 控制语句

# if
if True:
    print('True')
elif False:
    print('False')
else:
    print('else')

# 循环 for
for i in range(10):
    print(i)

# while
while True:
    print('while')
    break

# for else
for i in range(10):
    print(i)
    if i == 5:
        break
else:
    print('for else')

# range(), 自动生成数列
for i in range(10):
    print(i)

# break 和 continue
for i in range(10):
    if i == 5:
        break
    print(i)

for i in range(10):
    if i == 5:
        continue
    print(i)


# 质数查找
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, '等于', x, '*', n//x)
            break
    else:
        # 循环中没有找到元素
        print(n, ' 是质数')


# pass 语句
"""
Python pass是空语句，是为了保持程序结构的完整性。

pass 不做任何事情，一般用做占位语句，如下实例
"""
for i in range(10):
    pass

