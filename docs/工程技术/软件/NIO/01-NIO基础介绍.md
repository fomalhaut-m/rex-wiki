# Java NIO - 基础详解

> 新的输入/输出 (NIO) 库是在 JDK 1.4 中引入的，弥补了原来的 I/O 的不足，提供了高速的、面向块的 I/O。

而NIO把IO抽象成块每次IO操作的单位都是一个块，块被读入内存之后就是一个byte[]，NIO一次可以读或写多个字节。

## 通道与缓冲区

### 通道(Channel)

用于源节点与目标节点的连接。在 Java NIO 中，通道用于传输数据。Channel 本身不存储数据，因此需要配合缓冲区进行传输。

### 缓冲区（Buffer）

在 Java NIO 中，负责数据的存取。缓冲区就是数组。用于存储不同数据类型的数据，如：int、char、double、float、long等。缓冲区在创建时，不包含任何数据。需要利用 put() 方法添加数据，使用 get() 方法获取数据。

### 选择器（Selector）

选择器（Selector）是 SelectableChannel 对象的多路复用器。Selector 仅用于处理 SelectableChannel，因此可以理解为是多个通道的选择器。

## 文件NIO示例

[NIOExample.java](NIOExample.java)


## 选择器示例