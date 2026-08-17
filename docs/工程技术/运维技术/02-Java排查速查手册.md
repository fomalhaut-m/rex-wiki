# Java 单机服务器 CPU/内存/线程 排查命令速查手册（纯单机版）

**适用环境**：Linux 单机、物理机、虚拟机、非容器、标准 JDK 环境

**核心工具**：jps、jstat、jstack、jmap、top（JDK 原生，无需额外安装）

**核心区分（重中之重）**

- **jstat**：查GC、判CPU/内存异常根源（先定性）

- **jstack**：查线程、定位代码卡死、死循环、锁阻塞（后定位）

- **jmap**：查堆内存、大对象、内存泄漏、OOM

---

# 一、前置操作：获取 Java 进程 PID

```Plain Text
# 查看所有Java进程（最常用）
jps -l

# 配合系统命令查看进程资源占用
top
```

后续所有命令，替换 PID 为自己业务进程号即可

---

# 二、单机 CPU 飙高 完整排查流程（标准线上流程）

## 第一步：jstat 定性（判断是【代码问题】还是【GC问题】）

```Plain Text
# 每1秒打印一次GC状态，持续监控
jstat -gc PID 1000
```

**判断规则**：

- YGC/FGC 频繁暴涨、耗时高 → **CPU高是GC导致**（内存不合理、内存泄漏）

- GC次数正常、耗时低 → **CPU高是业务代码导致**（死循环、复杂计算）

## 第二步：top + jstack 精准定位代码行

```Plain Text
# 1. 查看该进程下所有线程CPU占用
top -H -p PID

# 2. 找出占用CPU最高的线程TID（十进制），转16进制
printf "%x" 线程TID

# 3. 连续导出3次线程快照（间隔2秒，对比波动，精准定位常驻热点）
jstack PID > thread_1.txt
sleep 2
jstack PID > thread_2.txt
sleep 2
jstack PID > thread_3.txt
```

**定位核心**：在快照文件中搜索 `0x十六进制TID`，持续处于 **RUNNABLE** 状态的线程堆栈，即为问题代码。

## CPU高频问题总结

- 代码问题：死循环、超大集合遍历、正则回溯、密集计算

- GC问题：新生代过小、老年代溢出、内存泄漏导致频繁GC

---

# 三、单机 内存泄漏 / OOM 排查流程

## 第一步：jstat 长期观测（判断是否内存泄漏）

```Plain Text
# 实时监控堆内存、GC变化
jstat -gc PID 1000
```

**泄漏判定标准**：

- OU（老年代使用内存）持续上涨，FullGC 后几乎不释放

- YGC 越来越频繁，系统响应逐渐变慢，最终触发OOM

## 第二步：jmap 分析对象占用 & 导出堆快照

```Plain Text
# 1. 查看堆整体配置、各区域内存占用
jmap -heap PID

# 2. 查看所有对象数量、内存占用（轻量、低影响）
jmap -histo PID | head -100

# 3. 生产安全导出堆文件（无FullGC、无强制STW，推荐）
jmap -dump:format=b,file=heap.hprof PID
```

**生产禁忌**：禁止高峰期执行 `jmap -dump:live`、`jmap -histo:live`，会触发FullGC，导致服务卡顿雪崩。

## 第三步：OOM 自动兜底配置（推荐永久开启）

JVM 启动参数添加，发生OOM自动留存堆快照，无需手动排查

```Plain Text
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/home/logs/heap.hprof
```

## 第四步：MAT 分析 hprof 文件

- Histogram：定位数量最多、占用内存最大的对象

- Dominator Tree：查找大对象、常驻内存对象的引用链

- Leak Suspects：工具自动识别内存泄漏可疑点

---

# 四、单机 线程异常 排查（卡死、超时、死锁、阻塞）

所有线程问题，统一使用 **jstack** 排查

## 1. 一键检测线程死锁（最实用）

```Plain Text
jstack PID | grep -i deadlock
```

有输出即为存在死锁，服务会永久卡死，必须重启+修复代码

## 2. 导出完整线程栈，分析阻塞/等待线程

```Plain Text
jstack PID > thread_all.txt
```

## 3. 线程状态问题定位规则

- **RUNNABLE 常驻**：代码死循环、CPU热点任务

- **BLOCKED 大量堆积**：锁竞争激烈、同步锁阻塞，接口大面积超时

- **WAITING/TIMED_WAITING 堆积**：线程池耗尽、IO等待、数据库/第三方接口阻塞

---

# 五、单机排查 最简标准流程（直接套用）

## 1. CPU 飙高

jstat 判GC状态 → top -H 找高CPU线程 → jstack 定位热点代码

## 2. 内存上涨/OOM

jstat 观测内存走势 → jmap 导出堆快照 → MAT 分析泄漏引用链

## 3. 服务卡顿/接口超时

jstack 查死锁 → 筛选 BLOCKED/WAITING 线程 → 定位锁/IO阻塞根因

---

# 六、单机命令避坑总结

- 优先用 **jstat** 定性问题，再用 jstack/jmap 定位，避免盲目排查

- 生产环境禁止使用带 `:live` 的 jmap 命令，防止FullGC雪崩

- CPU问题优先区分「GC导致」和「代码导致」，90%排查误区都是直接看jstack

- 线程问题必查死锁，死锁无法自动恢复，只能重启修复

> （注：部分内容可能由 AI 生成）