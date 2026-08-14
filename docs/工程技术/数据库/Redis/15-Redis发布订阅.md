# Redis 发布和订阅

## 定义

进程间的一种消息通信模式：发送者（pub）发送消息，订阅者（sub）接收消息。

## 订阅/发布消息图

1. 下图展示了频道 channel1，以及订阅这个频道的三个客户端之间的关系：
   - client1
   - client2
   - client5

2. 当有新消息通过 PUBLISH 命令发送给频道 channel1 时，这个消息就会被发送给订阅它的所有客户端。

## 常用命令

### PUBLISH

将信息发送到指定的频道。

```cmd
# 对没有订阅者的频道发送信息
redis> PUBLISH bad_channel "can any body hear me?"
(integer) 0

# 向有一个订阅者的频道发送信息
redis> PUBLISH msg "good morning"
(integer) 1

# 向有多个订阅者的频道发送信息
redis> PUBLISH chat_room "hello~ everyone"
(integer) 3
```

### SUBSCRIBE

订阅一个或多个频道。

```cmd
redis> SUBSCRIBE channel1 channel2 channel3
```

### UNSUBSCRIBE

退订频道。

```cmd
redis> UNSUBSCRIBE channel1
```

### PSUBSCRIBE

按模式订阅频道。

```cmd
redis> PSUBSCRIBE news.*
```

## 工作原理

1. 客户端订阅频道后，会与 Redis 服务器建立长连接
2. 当有消息发布到频道时，Redis 服务器会推送给所有订阅者
3. 如果订阅者不在线，消息会丢失（不同于消息队列）

## 应用场景

- 实时聊天系统
- 消息通知
- 订阅/关注系统
- 缓存失效通知
