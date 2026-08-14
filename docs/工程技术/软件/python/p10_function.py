# 函数定义与调用
def hello():
    print("hello world")  # 定义一个简单的函数，打印 "hello world"

hello();  # 调用函数 hello()

# 意义：演示如何定义和调用一个基本函数。



# 比较两个数并返回较大值
def max(a, b):
    if a > b:  # 如果 a 大于 b
        return a  # 返回 a
    else:
        return b  # 否则返回 b

max(1, 2);  # 调用函数 max()，传入参数 1 和 2，返回较大的值 2

# 意义：演示如何通过条件判断实现一个简单的比较函数。



# 计算矩形面积
def area(width, height):
    return width * height  # 返回宽度乘以高度的结果

area(10, 20);  # 调用函数 area()，传入参数 10 和 20，返回面积 200

# 意义：演示如何定义一个带有参数的函数，并返回计算结果。



# 变量作用域 - 基本类型不会受到影响
def change(a, b):
    a = 100  # 修改局部变量 a 的值为 100
    b = 200  # 修改局部变量 b 的值为 200
    print("a = ", a, "b = ", b)  # 打印修改后的局部变量 a 和 b

a = 1; b = 2;  # 定义全局变量 a 和 b
change(a, b)  # 调用函数 change()，传入全局变量 a 和 b
print(a)  # 打印全局变量 a，未受影响
print(b)  # 打印全局变量 b，未受影响

# 意义：演示函数内部对基本类型变量的修改不会影响外部变量。



# 变量作用域 - 可变类型会受到影响
def change_all(list):
    id(list)  # 获取列表对象的内存地址
    print(list)  # 打印原始列表
    list[0] = 100  # 修改列表的第一个元素
    print(list)  # 打印修改后的列表

list = [1, 2, 3]  # 定义一个列表
change_all(list)  # 调用函数 change_all()，传入列表
print(list)  # 打印修改后的列表

# 意义：演示函数内部对可变类型（如列表）的修改会影响外部变量。



# 关键字参数
def print_identity(name, age, sex):
    print("name = ", name, "age = ", age, "sex = ", sex)  # 打印传入的参数

print_identity(age=18, name="leiming", sex="male")  # 使用关键字参数调用函数

# 意义：演示如何使用关键字参数调用函数，参数顺序可以调整。



# 默认参数
def print_identity_default(name, age=18, sex="male"):
    print("name = ", name, "age = ", age, "sex = ", sex)  # 打印传入的参数，默认值为 age=18, sex="male"

print_identity_default("leiming")  # 调用函数时仅传入 name 参数
print_identity_default("leiming", 20)  # 调用函数时传入 name 和 age 参数

# 意义：演示如何定义带有默认值的参数，简化函数调用。



# 不定长度参数 (*args)
def print_agrs(*args):
    print(args)  # 打印所有传入的参数，作为元组存储

print_agrs(1, 2, 3, 4, 5)  # 调用函数时传入多个参数
print_agrs(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)  # 调用函数时传入更多参数

# 意义：演示如何定义接受不定数量位置参数的函数。



# 不定长度关键字参数 (**kwargs)
def print_agrs_default(arg1, **kwargs):
    print(arg1, kwargs)  # 打印第一个位置参数和所有关键字参数

print_agrs_default(1)  # 调用函数时仅传入位置参数
print_agrs_default(1, name="leiming", age=18, sex="male")  # 调用函数时传入位置参数和关键字参数

# 意义：演示如何定义接受不定数量关键字参数的函数。


# 混合不定长度参数 (*args 和 **kwargs)
def print_agrs_default2(arg1, *args, **kwargs):
    print("arg1", arg1)  # 打印第一个位置参数
    print("args", args)  # 打印所有位置参数
    print("kwargs", kwargs)  # 打印所有关键字参数

print_agrs_default2(1, 2, 3, 4, 5, name="leiming", age=18, sex="male", height=180)
print_agrs_default2(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, name="leiming", age=18, sex="male", height=180)

# 意义：演示如何同时处理位置参数、不定长度位置参数和不定长度关键字参数。


# 强制关键字参数
def print_agrs_default3(args, *, A):
    print("A", A)  # 打印强制关键字参数 A
    print("args", args)  # 打印位置参数

print_agrs_default3(1, A=100)  # 调用函数时必须使用关键字传递参数 A

# 意义：演示如何强制某些参数必须通过关键字传递。


# 匿名函数 lambda
add = lambda a, b: a + b  # 定义一个匿名函数，返回两个参数的和

print(add(1, 2))  # 调用匿名函数，传入参数 1 和 2，返回结果 3

# 意义：演示如何使用 lambda 表达式定义匿名函数。


# return
def add(a, b):
    return a + b  # 返回两个参数的和

print(add(1, 2))  # 调用函数 add()，传入参数 1 和 2，返回结果 3

# Python3.8 新增了一个函数形参语法 / 用来指明函数形参必须使用指定位置参数，不能使用关键字参数的形式。
def add(a, b, /, c):
    return a + b + c

print(add(1, 2, 3))
print(add(1, 2, c=3))
