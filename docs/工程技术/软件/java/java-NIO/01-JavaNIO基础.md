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

```java
import java.io.*;

public class NIOExample {

    public static void main(String[] args) throws Exception {
        File file = new File("test.txt");
        FileOutputStream fos = new FileOutputStream(file);
        BufferedOutputStream bos = new BufferedOutputStream(fos);
        bos.write("Hello World!".getBytes());
        bos.close();
        System.out.println("文件已写入");

        FileInputStream fis = new FileInputStream(file);
        BufferedInputStream bis = new BufferedInputStream(fis);
        byte[] buffer = new byte[1024];
        int length = bis.read(buffer);
        while (length != -1) {
            System.out.println(new String(buffer, 0, length));
            length = bis.read(buffer);
        }
        bis.close();
        file.delete();
        System.out.println("文件已删除");
    }
}
```

## 选择器示例

### 客户端

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

public class NIOExampleClient {

    public static void main(String[] args) throws IOException {
        SocketChannel socketChannel = SocketChannel.open();
        socketChannel.configureBlocking(false);

        boolean isConnected = socketChannel.connect(new InetSocketAddress("localhost", 8080));
        while (!isConnected) {
            Selector selector = Selector.open();
            socketChannel.register(selector, SelectionKey.OP_CONNECT);
            selector.select();
            Iterator<SelectionKey> keys = selector.selectedKeys().iterator();
            while (keys.hasNext()) {
                SelectionKey key = keys.next();
                keys.remove();
                if (key.isConnectable()) {
                    SocketChannel channel = (SocketChannel) key.channel();
                    isConnected = channel.finishConnect();
                }
            }
        }

        System.out.println("已连接到服务器");

        while (true) {
            System.out.print("请输入消息：");
            String message = new java.util.Scanner(System.in).nextLine();

            ByteBuffer buffer = ByteBuffer.wrap(message.getBytes());
            socketChannel.write(buffer);
            System.out.println("已发送消息：" + message);

            ByteBuffer readBuffer = ByteBuffer.allocate(1024);
            int bytesRead = socketChannel.read(readBuffer);
            if (bytesRead > 0) {
                readBuffer.flip();
                byte[] bytes = new byte[readBuffer.remaining()];
                readBuffer.get(bytes);
                String receivedMessage = new String(bytes);
                System.out.println("收到服务器消息：" + receivedMessage);
            }

            if (message.equals("exit")) {
                break;
            }
        }
    }
}
```

### 服务端

```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.Iterator;

public class NIOExampleServer {

    public static void main(String[] args) throws IOException {
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
        serverSocketChannel.configureBlocking(false);
        serverSocketChannel.bind(new InetSocketAddress(8080));

        Selector selector = Selector.open();
        serverSocketChannel.register(selector, SelectionKey.OP_ACCEPT);
        System.out.println("服务器已启动，等待连接...");

        while (true) {
            selector.select();
            Iterator<SelectionKey> iterator = selector.selectedKeys().iterator();

            while (iterator.hasNext()) {
                SelectionKey key = iterator.next();
                iterator.remove();

                if (key.isAcceptable()) {
                    ServerSocketChannel server = (ServerSocketChannel) key.channel();
                    SocketChannel client = server.accept();
                    client.configureBlocking(false);
                    client.register(selector, SelectionKey.OP_READ);
                    System.out.println("新客户端连接: " + client);
                } else if (key.isReadable()) {
                    readData(key);
                }
            }
        }
    }

    private static void readData(SelectionKey key) throws IOException {
        SocketChannel client = (SocketChannel) key.channel();
        ByteBuffer buffer = ByteBuffer.allocate(1024);
        int readBytes = client.read(buffer);

        if (readBytes > 0) {
            buffer.flip();
            String data = new String(buffer.array(), 0, readBytes);
            System.out.println("接收到消息: " + data);

            ByteBuffer outBuffer;
            switch (data) {
                case "你好":
                    outBuffer = ByteBuffer.wrap("你好".getBytes());
                    break;
                case "你好吗":
                    outBuffer = ByteBuffer.wrap("我很好".getBytes());
                    break;
                case "你叫什么名字":
                    outBuffer = ByteBuffer.wrap("我叫小明".getBytes());
                    break;
                default:
                    outBuffer = ByteBuffer.wrap("我不明白".getBytes());
            }
            client.write(outBuffer);
        }
    }
}
```

