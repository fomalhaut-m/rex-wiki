# 多线程面试题

## 目录导航

| 文档 | 说明 |
|------|------|
| [01-Volatile关键字](01-Volatile关键字.md) | Volatile保证可见性 |
| [02-CAS比较与交换](02-CAS比较与交换.md) | CAS无锁算法 |
| [03-集合类线程安全问题](03-集合类线程安全问题.md) | 并发集合 |
| [04-多线程锁](04-多线程锁.md) | synchronized/Lock |
| [05-线程控制类](05-线程控制类.md) | CountDownLatch等 |
| [06-阻塞队列](06-阻塞队列.md) | BlockingQueue |
| [07-线程通讯](07-线程通讯.md) | wait/notify |
| [08-线程池原理](08-线程池原理.md) | 线程池核心原理 |
| [09-死锁问题分析](09-死锁问题分析.md) | 死锁产生与排查 |

## 核心知识点

### 线程基础
- Thread创建方式
- 线程状态
- 线程优先级

### 同步机制
- synchronized
- ReentrantLock
- volatile

### 并发工具
- CountDownLatch
- CyclicBarrier
- Semaphore