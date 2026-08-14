# Java8 Optional 容器类

用于尽量避免空指针异常。

## 1. 静态方法

| 方法名 | 描述 |
|--------|------|
| `static Optional empty()` | 返回空的 Optional 实例 |
| `static Optional of(T value)` | 返回具有指定非空值的 Optional，如果为空则发生异常 |
| `static Optional ofNullable(T value)` | 返回指定值的 Optional，如果为 null 则返回空 Optional，不会发生异常 |

## 2. 实例方法

### 2.1 获取值的方法

| 方法 | 描述 |
|------|------|
| `get()` | 返回包含的值，如果为空则抛出异常 |
| `orElse(T other)` | 返回包含的值，如果为空则返回指定的默认值 |
| `orElseGet(Supplier supplier)` | 返回包含的值，如果为空则返回 supplier 生成的值 |
| `orElseThrow(Supplier exceptionSupplier)` | 返回包含的值，如果为空则抛出 supplier 生成的异常 |

### 2.2 判断方法

| 方法 | 描述 |
|------|------|
| `isPresent()` | 返回值是否存在 |
| `ifPresent(Consumer consumer)` | 如果值存在则执行 consumer |

### 2.3 转换方法

| 方法 | 描述 |
|------|------|
| `map(Function mapper)` | 如果值存在则进行转换 |
| `flatMap(Function mapper)` | 如果值存在则进行转换，返回值为 Optional |

## 3. 示例代码

```java
// of 获取一个非 null 的对象，如果为 null 则发生异常
Optional<Employee> employee = Optional.of(new Employee());
System.out.println(employee);

// empty 获取一个空的 Optional
Optional<Employee> empty = Optional.empty();
System.out.println(empty);

// ofNullable 允许获取一个 null 对象，不会发生异常
Optional<Employee> employee1 = Optional.ofNullable(new Employee());
Optional<Employee> employee2 = Optional.ofNullable(null);
System.out.println(employee1);
System.out.println(employee2);

// orElse 使用默认值
String name = Optional.ofNullable(user)
    .map(User::getName)
    .orElse("匿名用户");

// ifPresent 如果存在则执行
Optional.ofNullable(email)
    .ifPresent(e -> System.out.println("发送邮件到: " + e));
```
