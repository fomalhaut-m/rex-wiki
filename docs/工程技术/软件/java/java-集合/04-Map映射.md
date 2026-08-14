# Map

集合根据数据存储的不同分为两种格式：单值集合、二元偶对象集合。在 Collection 中都是属于单值集合，而二元偶对象集合则是使用 `key=value` 的结构，在使用的时候根据 `key` 寻找 `value` 的值。所以 Collection 和 Map 存储数据的目的为：**Collection 是为了数据的输出而设计的，Map 是为了数据的查询而存在的**。

`java.util.Map` 是进行二元偶对象数据存储的最大父接口，里面的所有存储的数据都会按照 `key=value` 的形式进行保存，所以在数据存放时需要用到两个内容。

## 常用方法

| 方法 | 释义 |
|------|------|
| `V put(K key, V value)` | 向集合中保存数据 |
| `V get(Object key)` | 通过 key 查询对应内容 |
| `V remove(Object key)` | 根据 key 删除对应数据 |
| `int size()` | 获取集合长度 |
| `Collection values()` | 返回所有的内容 |
| `Set keySet()` | 获取所有的 key |
| `Set<Map.Entry> entrySet()` | 将所有的内容以 Map.Entry 形式返回 |

在 JDK1.9 之后，在 MAP 接口中有 `of` 方法，他可以创建一个 Map 集合：

```java
Map<String, Integer> map = Map.of("one", 1, "two", 2, "three", 3);
System.out.println(map);
```

结果：

```cmd
{three=3, two=2, one=1}
```

> 如果 `key` 重复则会抛出异常 `Exception in thread "main" java.lang.IllegalArgumentException: duplicate key: three`

因为 `key` 作为 Map 操作的核心控制点，所以这个内容的重复实际上对于整个 Map 而言就需要进行更新。如果想正确使用 MAP 的接口，就要使用 Map 的子类：

- HashMap
- LinkedHashMap
- TreeMap
- HashTable

## 1. HashMap

HashMap 是 Map 接口中最为常见的一个子类，也是主要使用的一个子类，此类采用 Hash 的方式进行存储，所以存储的时候都是无序的。
