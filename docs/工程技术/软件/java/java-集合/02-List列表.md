# List 接口

List 是 Collection 的子接口，它是一种有序集合，可以存储重复元素。

## 主要与 Collection 不一样的方法

| 方法 | 描述 |
|------|------|
| `void add(int index, E element)` | 向集合指定索引加入元素 |
| `E get(int index)` | 获取集合中指定索引的元素 |
| `ListIterator<E> listIterator()` | 获取 ListIterator 接口的实例 |
| `static List<E> of(E... elements)` | 通过指定的内容创建 List（JDK 1.9+），创建不能修改的 List 集合 |
| `int indexOf(Object o)` | 获取该对象在 List 中的索引 |

## 常用子类

- ArrayList
- LinkedList
- Vector

## 一. ArrayList

ArrayList 是 List 接口最常用的实现类，它基于数组实现。

### 构造方法

```java
// 空参构造方法
public ArrayList() {
    this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
}

// 创建指定长度的数组
public ArrayList(int initialCapacity) {
    if (initialCapacity > 0) {
        this.elementData = new Object[initialCapacity];
    } else if (initialCapacity == 0) {
        this.elementData = EMPTY_ELEMENTDATA;
    } else {
        throw new IllegalArgumentException("Illegal Capacity: " + initialCapacity);
    }
}
```

### 常用方法

```java
// 添加元素
list.add("hello");

// 获取元素
String s = list.get(0);

// 修改元素
list.set(0, "world");

// 删除元素
list.remove(0);

// 获取大小
int size = list.size();
```

## 二. LinkedList

LinkedList 是 List 接口的实现类，基于双向链表实现。

### 特有方法

```java
// 添加到头部
linkedList.addFirst("first");

// 添加到尾部
linkedList.addLast("last");

// 获取头部
String first = linkedList.getFirst();

// 获取尾部
String last = linkedList.getLast();

// 移除头部
linkedList.removeFirst();

// 移除尾部
linkedList.removeLast();
```

## 三. Vector

Vector 是 List 接口的实现类，它是同步的（线程安全），但性能比 ArrayList 差。

```java
Vector<String> vector = new Vector<>();
vector.add("element");
```

## ArrayList vs LinkedList vs Vector

| 特性 | ArrayList | LinkedList | Vector |
|------|-----------|------------|--------|
| 底层实现 | 数组 | 双向链表 | 数组 |
| 随机访问 | O(1) | O(n) | O(1) |
| 插入/删除 | O(n) | O(1) | O(n) |
| 线程安全 | 否 | 否 | 是 |
| 初始容量 | 10 | 0 | 10 |
