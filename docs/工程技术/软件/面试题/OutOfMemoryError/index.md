# 内存溢出分析

## 目录导航

| 文档 | 说明 |
|------|------|
| [01-栈溢出](01-栈溢出.md) | StackOverflowError |
| [02-堆溢出](02-堆溢出.md) | java heap space |
| [03-直接缓存溢出](03-直接缓存溢出.md) | Direct buffer memory |
| [04-线程超上限](04-线程超上限.md) | unable to create new native thread |
| [05-元空间溢出](05-元空间溢出.md) | Metaspace |

## OOM场景

- 栈溢出：递归调用、线程创建过多
- 堆溢出：大量对象、大文件加载
- 元空间：动态生成大量类