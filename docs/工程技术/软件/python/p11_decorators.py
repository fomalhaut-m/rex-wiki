#  装饰器
import random
import time


## 声明装饰器
def my_decorator(func):
    """
    装饰器函数，用于包裹目标函数并添加额外功能

    Args:
        func (callable): 被装饰的目标函数对象

    Returns:
        function: 返回封装后的wrapper函数，该函数会包裹原函数并添加前后打印逻辑
    """

    def wrapper(a, b):
        # 包裹函数核心逻辑：
        # 1. 先执行装饰器添加的前置操作
        # 2. 调用原始被装饰函数
        # 3. 执行装饰器添加的后置操作
        print("执行前")
        func(a, b)
        print('执行后')

    return wrapper


@my_decorator
def my_function(a, b):
    print("Hello World")


my_function('a,', 'b.')


# 耗时装饰器
def timer(func):
    """
    耗时装饰器，用于包裹目标函数并记录函数执行耗时

    Args:
        func (callable): 被装饰的目标函数对象

    Returns:
        function: 返回封装后的wrapper函数，该函数会包裹原函数并记录函数执行耗时
    """
    def wrapper(*args, **kwargs):  # 修正参数接收方式
        # 包裹函数核心逻辑：
        # 1. 记录函数开始执行时间
        # 2. 调用原始被装饰函数
        # 3. 记录函数结束执行时间
        start_time = time.time()
        result = func(*args, **kwargs)  # 正确传递所有参数
        end_time = time.time()
        print(f"函数{func.__name__}执行耗时：{end_time - start_time}秒")
        return result
    return wrapper  # ★★★ 必须返回包装函数 ★★★



# 随机延迟方法
@timer
def random_delay(name: str):
    ## 延迟随机毫秒
    delay = random.randint(1, 1000)
    time.sleep(delay / 1000)
    print(f"{name}执行完毕")


random_delay(name='l')
random_delay(name='o')
random_delay(name='v')
random_delay(name='e')


# 类装饰器
def class_decorator(cls):
    """
    类装饰器，用于包裹目标类并添加额外功能

    Args:
        cls (type): 被装饰的目标类对象

    Returns:
        class: 返回封装后的wrapper类，该类会包裹原类并添加前后打印逻辑
    """
    class Wrapper(cls):
        def __init__(self, *args, **kwargs):
            # 包裹类核心逻辑：
            # 1. 先执行装饰器添加的前置操作
            # 2. 调用原始被装饰类的__init__方法
            print("执行前")
            super().__init__(*args, **kwargs)
            print('执行后')
    return Wrapper # ★★★ 必须返回包装类 ★★★


@class_decorator
class MyClass:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello, {self.name}!")

# 使用
my_obj = MyClass("Alice")
my_obj.say_hello()


# 内置装饰器
# Python 提供了一些内置的装饰器，例如：
#
# @staticmethod: 将方法定义为静态方法，不需要实例化类即可调用。
#
# @classmethod: 将方法定义为类方法，第一个参数是类本身（通常命名为 cls）。
#
# @property: 将方法转换为属性，使其可以像属性一样访问。
class MyClass:
    @staticmethod
    def static_method():
        print("This is a static method.")

    @classmethod
    def class_method(cls):
        print(f"This is a class method of {cls.__name__}.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

# 使用
MyClass.static_method()
MyClass.class_method()

obj = MyClass()
obj.name = "Alice"
print(obj.name)