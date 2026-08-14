---
title: Python基础语法
---

# Python基础语法

## 环境说明

```bash
# 运行Python脚本
python script.py
```

## 基本语法

### 1. 变量与数据类型

```python
# 变量定义
name = "Alice"
age = 25
is_student = True

# 基本数据类型
# str, int, float, bool, list, dict, tuple, set
```

### 2. 条件判断

```python
if age >= 18:
    print("成年")
elif age >= 6:
    print("青少年")
else:
    print("儿童")
```

### 3. 循环

```python
# for循环
for i in range(5):
    print(i)

# while循环
count = 0
while count < 5:
    print(count)
    count += 1
```

### 4. 函数

```python
def greet(name, greeting="Hello"):
    """问候函数"""
    return f"{greeting}, {name}!"

# 调用
message = greet("Alice")
print(message)
```

### 5. 装饰器

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```

## 常用模块

| 模块 | 用途 |
|------|------|
| `sys` | 系统相关功能 |
| `os` | 文件系统操作 |
| `json` | JSON序列化 |
| `datetime` | 日期时间处理 |