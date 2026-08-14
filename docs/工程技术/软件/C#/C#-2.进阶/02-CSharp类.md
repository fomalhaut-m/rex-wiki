# C# 类（Class）

当你定义一个类时，你定义了一个数据类型的蓝图。这实际上并没有定义任何的数据，但它定义了类的名称意味着什么，也就是说，类的对象由什么组成及在这个对象上可执行什么操作。对象是类的实例。构成类的方法和变量成为类的成员。

## 1. 类的定义

类的定义是以关键字 **class** 开始，后跟类的名称。类的主体，包含在一对花括号内。下面是类定义的一般形式：

```csharp
<access specifier> class class_name
{
    // member variables
    <access specifier> <data type> variable1;
    <access specifier> <data type> variable2;
    ...
    <access specifier> <data type> variableN;

    // member methods
    <access specifier> <return type> method1(parameter_list)
    {
        // method body
    }
    <access specifier> <return type> method2(parameter_list)
    {
        // method body
    }
    ...
    <access specifier> <return type> methodN(parameter_list)
    {
        // method body
    }
}
```

请注意：

- 访问标识符 `<access specifier>` 指定了对类及其成员的访问规则。如果没有指定，则使用默认的访问标识符。类的默认访问标识符是 **internal**，成员的默认访问标识符是 **private**。
- 数据类型 `<data type>` 指定了变量的类型，返回类型 `<return type>` 指定了方法返回的数据类型。
- 如果要访问类的成员，你要使用点（.）运算符。
- 点运算符链接了对象的名称和成员的名称。

下面的实例说明了目前为止所讨论的概念：

```csharp
using System;

namespace BoxApplication
{
    class Box
    {
       public double length;   // 长度
       public double breadth;  // 宽度
    }
}
```

## 2. 访问标识符

访问标识符指定了一个类或其成员的访问级别。

C# 中有以下几种访问标识符：

| 标识符 | 说明 |
|--------|------|
| `public` | 公有访问，不受限制 |
| `private` | 私有访问，仅限同类成员 |
| `protected` | 受保护访问，仅限同类及派生类 |
| `internal` | 内部访问，仅限当前程序集 |

## 3. 类的示例

```csharp
using System;

namespace BoxApplication
{
    class Box
    {
       private double length;      // 长度
       private double breadth;     // 宽度
       private double height;      // 高度

       public void setValues(double l, double b, double h)
       {
           length = l;
           breadth = b;
           height = h;
       }

       public double getVolume()
       {
           return length * breadth * height;
       }
    }

    class Boxtester
    {
       static void Main(string[] args)
       {
          Box box1 = new Box();
          box1.setValues(5.0, 6.0, 7.0);
          Console.WriteLine("体积：{0}", box1.getVolume());
       }
    }
}
```

运行结果：

```
体积：210
```
