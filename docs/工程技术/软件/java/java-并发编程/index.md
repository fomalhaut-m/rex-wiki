# Java并发编程

## 目录导航

| 文档 | 说明 |
|------|------|
| [01-线程安全性](01-线程安全性.md) | 线程安全概念 |
| [02-对象的共享](02-对象的共享.md) | 对象共享与可见性 |
| [03-对象的组合](03-对象的组合.md) | 线程安全组合 |
| [04-JDK并发包](04-JDK并发包.md) | 并发工具类 |

## 核心知识点

### 线程安全
- 原子性：AtomicInteger/CAS
- 可见性：volatile/synchronized
- 有序性：Happens-Before

### 并发工具
- CountDownLatch
- CyclicBarrier
- Semaphore
- Exchanger