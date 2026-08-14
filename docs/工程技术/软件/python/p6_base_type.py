#!/usr/bin/python3

counter = 100  # 整型变量
miles = 1000.0  # 浮点型变量
name = "leiming"  # 字符串

print(counter)
print(miles)
print(name)

# 变量定义
x = 10  # 整数
y = 3.14  # 浮点数
name = "Alice"  # 字符串
is_active = True  # 布尔值

# 多变量赋值
a, b, c = 1, 2, "three"

# 查看数据类型
print(type(x))  # <class 'int'>
print(type(y))  # <class 'float'>
print(type(name))  # <class 'str'>
print(type(is_active))  # <class 'bool'>

print('print(isinstance(x, int)) : ')
print(isinstance(x, int))
print('print(isinstance(y, float)) : ')
print(isinstance(y, float))
print('print(isinstance(name, str)) : ')
print(isinstance(name, str))
print('print(isinstance(is_active, bool)) : ')
print(isinstance(is_active, bool))
print('print(isinstance(a, int)) : ')
print(isinstance(a, int))
print('print(isinstance(b, int)) : ')
print(isinstance(b, int))
print('print(isinstance(c, str)) : ')
print(isinstance(c, str))

# 加法
print('# 加法 print(1+3) : ')
print(1 + 3)
# 减法
print(' # 减法 print(3-1) : ')
print(3 - 1)
# 乘法
print('# 乘法 print(3*2) : ')
print(3 * 2)
# 除法，得到一个浮点数
print('# 除法，得到一个浮点数 print(4/2) : ')
print(4 / 2)
# 除法，得到一个整数
print('# 除法，得到一个整数 print(4//2) : ')
print(4 // 2)
# 取余
print('# 取余 print(4%2) : ')
print(4 % 2)
# 乘方
print('# 乘方 print(2**3) : ')
print(2 ** 3)

## 逻辑运算符
a = 1
b = 2
if a > b:
    print("a > b")
elif a < b:
    print("a < b")
else:
    print("a == b")

# bool
print('bool(0) : ')
print(bool(0))
print('bool(1) : ')
print(bool(1))
print('bool(None) : ')
print(bool(None))
print('bool("") : ')
print(bool(""))
print('bool([]) : ')
print(bool([]))
print('bool({}) : ')
print(bool({}))
print('bool(()) : ')
print(bool(()))

# and or not
print('True and False : ')
print(True and False)
print('True or False : ')
print(True or False)
print('not True : ')
print(not True)
print('not False : ')
print(not False)
print('not 0 : ')
print(not 0)

# > <
print('1 > 2 : ')
print(1 > 2)
print('1 < 2 : ')
print(1 < 2)
print('1 >= 2 : ')
print(1 >= 2)
print('1 <= 2 : ')
print(1 <= 2)
print('1 == 2 : ')
print(1 == 2)
print('1 != 2 : ')
print(1 != 2)
print('1 is 2 : ')
print(1 is 2)
print('1 is not 2 : ')
print(1 is not 2)
print('1 is None : ')
print(1 is None)
print('1 is not None : ')
print(1 is not None)

# 列表
list1 = [1, 2, 3, 4, 5];

print('list1')
print(list1)
print('list1[0]')
print(list1[0])
print('list1[1:2]')
print(list1[1:2])
print('list1[1:]')
print(list1[1:])
print('list1[:2]')
print(list1[:2])
print('list1[-1]')
print(list1[-1])
print('list1[-2]')
print(list1[-2])

print('合并列表')
list2 = [6, 7, 8, 9, 10]
list3 = list1 + list2
print(list3)

# list 的方法
print('追加')
list1.append(11)
print(list1)
print('删除')
list1.remove(11)
print(list1)
print('插入')
list1.insert(0, 11)
print(list1)
print('删除')
list1.pop(0)
print(list1)
print('排序')
list1.sort()
print(list1)
print('反转')
list1.reverse()
print(list1)
print('长度')
print(len(list1))
print('索引')
print(list1.index(2))
print('计数')
print(list1.count(2))
print('清空')
list1.clear()
print(list1)


# 元组 写在小括号里的是元组
tuple1 = (1, 2, 3, 4, 5)
print('元组')
print(tuple1)
print('元组索引')
print(tuple1[0])
print('元组切片')
print(tuple1[1:2])
print('元组长度')
print(len(tuple1))

# set 集合 {} 是set
set1 = {1, 2, 3, 4, 5}
print('集合')
print(set1)
print('集合长度')
print(len(set1))
print('集合方法')
print('添加')
set1.add(6)
print(set1)
print('删除')
set1.remove(6)
print(set1)
print('清空')
set1.clear()
print(set1)
print('集合运算')
set2 = {1, 2, 3, 4, 5}
set3 = {4, 5, 6, 7, 8}
print('交集 &')
print(set2 & set3)
print('并集 |')
print(set2 | set3)
print('差集 -')
print(set2 - set3)
print('对称差集 ^')
print(set2 ^ set3)
print('子集 <=')
print(set2 <= set3)
print('超集 >=')
print(set2 >= set3)
print('子集 issubset')
print(set2.issubset(set3))
print('超集 isuperset')
print(set2.issuperset(set3))
print('相等 ==')
print(set2 == set3)
print('不相等 !=')
print(set2 != set3)
print('交集 intersection')
print(set2.intersection(set3))
print('并集 union')
print(set2.union(set3))
print('差集 difference')
print(set2.difference(set3))

# 枚举字典
dict1 = {'name': 'leiming', 'age': 18, 'gender': 'male'}
for key, value in dict1.items():
    print(key, value)

# bytes
bytes1 = b'hello world'
print("b'hello world")
print(bytes1)
print('bytes1[0]')
print(bytes1[0])

bytes2 = bytes('hello world', 'utf-8');
print("bytes('hello world', 'utf-8')")
