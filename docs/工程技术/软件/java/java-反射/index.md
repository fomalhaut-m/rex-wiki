# Java反射

## 目录导航

| 文档 | 说明 |
|------|------|
| [01-反射机制与类操作](01-反射机制与类操作.md) | Class对象与反射 |
| [02-反射机制与简单Java类](02-反射机制与简单Java类.md) | 反射操作JavaBean |
| [03-ClassLoader类加载器](03-ClassLoader类加载器.md) | 类加载机制 |
| [04-反射与代理设计模式](04-反射与代理设计模式.md) | 动态代理 |
| [05-反射与Annotation](05-反射与Annotation.md) | 注解处理 |
| [06-反射检查类结构](06-反射检查类结构.md) | 类结构检查 |

## 核心知识点

### Class类常用方法
- getClassLoader()
- getDeclaredMethods()
- getDeclaredFields()

### 反射应用场景
- Spring IOC容器
- MyBatis映射
- JSON序列化
- 单元测试框架