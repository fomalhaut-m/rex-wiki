# 原子操作类

## 概述

原子操作类位于 `java.util.concurrent.atomic` 包下，提供了基于 CAS 机制的无锁并发操作能力。

### 分类

| 类型 | 类 |
|------|-----|
| 基础 | AtomicBoolean、AtomicInteger、AtomicLong |
| 数组 | AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray |
| 引用 | AtomicReference、AtomicMarkableReference、AtomicStampedReference |
| 对象字段 | AtomicIntegerFieldUpdater、AtomicLongFieldUpdater、AtomicReferenceFieldUpdater |
| 累加器 | DoubleAccumulator、DoubleAdder、LongAccumulator、LongAdder |

## 基础原子类

### 底层原理

```java
// Unsafe 底层实现
private static final Unsafe U = Unsafe.getUnsafe();
// 可见性
private volatile int value;

// cas 机制
public final native boolean compareAndSwapInt(Object o, long offset, int expected, int x);
```

### AtomicBoolean

```java
private static final VarHandle VALUE;
```

> VarHandle 是 JDK 9 提供的方法，用于对变量进行动态强类型引用，支持读/写、volatile 读/写和 CAS 操作。

### 使用示例

```java
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

public class AtomicBasicTest {

    public static void main(String[] args) {
        AtomicInteger atomicInteger = new AtomicInteger();
        atomicInteger.addAndGet(1);
        System.out.println(atomicInteger);

        AtomicLong atomicLong = new AtomicLong();
        // = 0, 没有修改
        atomicLong.compareAndSet(0, 2);
        System.out.println(atomicLong);
        // = 1, 修改了
        atomicLong.compareAndSet(1, 2);
        System.out.println(atomicLong);

        AtomicBoolean atomicBoolean = new AtomicBoolean();
        atomicBoolean.compareAndSet(true, true);
        System.out.println(atomicBoolean); // = false
        atomicBoolean.compareAndSet(false, true);
        System.out.println(atomicBoolean); // true
    }
}
```

## 数组原子类

### 使用示例

```java
import java.util.concurrent.atomic.AtomicReferenceArray;

public class AtomicArrayTest {

    public static void main(String[] args) {
        String[] names = {"leiming", "wangrui", "leiwen"};
        AtomicReferenceArray<String> array = new AtomicReferenceArray<>(names);

        System.out.println("[当前内容] :" + array);

        array.set(2, "zhaodongyan");
        System.out.println("[当前内容] :" + array);

        // CAS方法，元数据不正确不会被修改
        array.compareAndSet(1, "?", "yaojing");
        System.out.println("[当前内容] :" + array);

        array.compareAndSet(1, "wangrui", "leiming2");
        System.out.println("[当前内容] :" + array);
    }
}
```

## 引用原子类

### AtomicReference

用于对象的原子引用更新，对比的是内存引用地址。

```java
import java.util.concurrent.atomic.AtomicReference;

public class AtomicReferenceTest {

    public static void testAtomicReference() {
        Book juc = new Book("学习juc", 20L);
        Book java = new Book("java基础", 21L);

        AtomicReference atomicReference = new AtomicReference(juc);
        atomicReference.compareAndSet(juc, java);
        System.out.println("[更换结果] :" + atomicReference);

        // 注意：重写hash和eq也无法更换，因为对比的是内存地址
        atomicReference.compareAndSet(new Book("学习juc", 20L), java);
        System.out.println("[未更换:重写hash和eq无法更换] :" + atomicReference);
    }
}
```

### AtomicStampedReference（版本号引用）

解决 ABA 问题，记录每次修改的版本号。

```java
import java.util.concurrent.atomic.AtomicStampedReference;

public class AtomicReferenceTest {

    public static void testAtomicStampedReference() {
        Book juc1 = new Book("juc第一版", 1L);
        Book juc2 = new Book("juc第贰版", 2L);

        AtomicStampedReference<Book> asr
                = new AtomicStampedReference<>(juc1, 1);

        // 错误示例：版本号不匹配
        boolean b = asr.compareAndSet(juc1, juc2, 2, 2);
        System.err.println("[错误示例] " + b);

        // 正确示例：版本号匹配
        b = asr.compareAndSet(juc1, juc2, 1, 2);
        System.out.println("[正确示例] " + b);
    }
}
```

### AtomicMarkableReference（标记引用）

类似版本号，但只有 true/false 两个状态。

```java
import java.util.concurrent.atomic.AtomicMarkableReference;

public class AtomicReferenceTest {

    public static void testAtomicMarkableReference() {
        Book juc1 = new Book("juc第一版", 1L);
        Book juc2 = new Book("juc第贰版", 2L);

        AtomicMarkableReference<Book> asr
                = new AtomicMarkableReference<>(juc1, true);

        boolean b = asr.compareAndSet(juc1, juc2, false, true);
        System.err.println("[错误示例] " + b);

        b = asr.compareAndSet(juc1, juc2, true, true);
        System.out.println("[正确示例] " + b);
    }
}
```

## 对象字段原子类

### AtomicLongFieldUpdater

对对象字段进行原子更新，字段必须使用 `volatile` 修饰。

```java
import java.util.concurrent.atomic.AtomicLongFieldUpdater;

public class AtomicReferenceUpdaterTest {

    public static void testLongUpdaterIsVolatile() {
        AtomicLongFieldUpdater<Book> updater
                = AtomicLongFieldUpdater.newUpdater(Book.class, "price");
        System.out.println(updater);
    }

    public static void testLongUpdater() {
        Book book = new Book("longUpdater", 100L);
        System.out.println("修改之前: " + book);

        book.setPrice(99L);
        System.out.println("修改之后: " + book);

        AtomicLongFieldUpdater<Book> updater
                = AtomicLongFieldUpdater.newUpdater(Book.class, "price");
        updater.set(book, 88L);
        System.out.println("第二次修改后: " + book);
    }

    public static class Book {
        private String name;
        private volatile long price; // 必须使用volatile

        public void setPrice(long price) {
            AtomicLongFieldUpdater<Book> fieldUpdater
                    = AtomicLongFieldUpdater.newUpdater(Book.class, "price");
            fieldUpdater.set(this, price);
        }
    }
}
```

> 注意：字段必须使用 `volatile` 关键字定义，否则会抛出 `IllegalArgumentException: Must be volatile type`

## 累加器

### DoubleAccumulator / LongAccumulator

支持自定义累加函数。

```java
import java.util.concurrent.atomic.DoubleAccumulator;
import java.util.concurrent.atomic.DoubleAdder;

public class AtomicAddTest {

    public static void main(String[] args) {
        DoubleAccumulator da = new DoubleAccumulator(
                (x, y) -> x + y, // 累加函数
                0d                // 初始值
        );

        da.accumulate(1.0);
        System.out.println("结果: " + da);
        da.accumulate(3);
        System.out.println("结果: " + da);
        da.accumulate(5.0);
        System.out.println("结果: " + da);

        DoubleAdder adder = new DoubleAdder();
        adder.add(2.0);
        System.out.println("add = " + adder);
        adder.add(2.0);
        System.out.println("add = " + adder);
    }
}
```

## CAS 机制说明

CAS (Compare-And-Swap) 是原子操作的核心：

1. **读取**：获取当前值
2. **比较**：将当前值与期望值比较
3. **交换**：相等时更新为新值

如果多线程同时修改，只有第一个线程能成功，其他线程会失败并重试。
