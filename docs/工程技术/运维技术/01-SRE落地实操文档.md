# SRE 全套落地技术实操文档（组件+插件+配置）

## 一、SRE 可观测整体落地架构

整套SRE可观测体系**零业务代码入侵**，可直接部署生产，完整实现SLI指标采集、SLO监控、故障告警、稳定性管控。

**整体技术链路**：Java服务 + JMX Exporter（JavaAgent探针插件） + Prometheus + Grafana + AlertManager

- **采集层**：JMX Exporter（JavaAgent探针，采集JVM核心SLI指标）

- **存储层**：Prometheus（时序数据库，存储所有监控指标）

- **可视化层**：Grafana（搭建SRE专属大盘，观测指标趋势）

- **告警层**：AlertManager（配置SLO阈值，实现分级故障告警）

## 二、核心采集插件：JMX Exporter 实操配置

### 2.1 插件核心作用

基于**JavaAgent探针机制**，无代码侵入，自动抓取Java服务所有SRE核心SLI指标：CPU使用率、堆/非堆内存、元空间、YGC/FGC次数、GC耗时、活跃线程、阻塞线程、类加载数。

### 2.2 插件基础信息

- 插件名称：jmx_prometheus_javaagent

- 稳定生产版本：1.3.0

- 加载方式：javaagent挂载（优先级高于业务代码，纯探针模式）

### 2.3 核心配置文件 jmx-config.yml（生产直接复用）

```Plain Text
lowercaseOutputName: true
lowercaseOutputLabelNames: true
rules:
  # 堆内存指标
  - pattern: 'java.lang<type=Memory><HeapMemoryUsage>(.*)'
    name: jvm_heap_$1
    type: GAUGE
  # 非堆内存
  - pattern: 'java.lang<type=Memory><NonHeapMemoryUsage>(.*)'
    name: jvm_nonheap_$1
    type: GAUGE
  # GC 采集次数/耗时
  - pattern: 'java.lang<type=GarbageCollector,name=.*>(CollectionCount|CollectionTime)'
    name: jvm_gc_$1
    type: COUNTER
  # 线程指标
  - pattern: 'java.lang<type=Threading>(ThreadCount|PeakThreadCount|DaemonThreadCount)'
    name: jvm_thread_$1
    type: GAUGE

```

### 2.4 Java服务挂载插件两种生产方案

#### 方案1：单机服务器启动命令（直接部署）

```Plain Text
java \
-javaagent:/opt/jmx/jmx_prometheus_javaagent-1.3.0.jar=9404:/opt/jmx/jmx-config.yml \
-jar app.jar

```

#### 方案2：Docker/ECS 零侵入部署（推荐）

通过环境变量全局注入，无需修改启动脚本、无需改镜像

```Plain Text
JAVA_TOOL_OPTIONS=-javaagent:/opt/jmx/jmx_prometheus_javaagent-1.3.0.jar=9404:/opt/jmx/jmx-config.yml
```

**挂载生效接口**：启动后自动暴露指标接口 `http://IP:9404/metrics`

## 三、Prometheus 指标采集配置

新增JVM监控任务，定时自动抓取所有服务SRE核心SLI指标，持久化存储

```Plain Text
scrape_configs:
  - job_name: 'sre-jvm-monitor'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['服务IP:9404']

```

## 四、Grafana 可视化大盘落地

- 快速模板ID：**8563**（通用成熟JVM SRE大盘）

- 覆盖核心指标：内存占用趋势、GC波动明细、线程数量变化、CPU使用率、服务抖动状态

- 落地价值：直观观测SLI指标走势，提前捕捉故障前兆，实现事前预判

**导入方式**：Grafana → Dashboards → Import → 输入模板ID → 绑定Prometheus数据源

## 五、SLO 分级告警规则（AlertManager 生产可用）

严格对齐SRE运维红线，区分预警/紧急级别，生产可直接启用

```Plain Text
# 1. 堆内存超75%（内存泄漏预警）
expr: jvm_heap_used / jvm_heap_max > 0.75
for: 5m
severity: warning

# 2. CPU持续超80%（性能击穿SLO，紧急告警）
expr: system_cpu_usage > 0.8
for: 2m
severity: critical

# 3. 出现FullGC（严重稳定性隐患）
expr: increase(jvm_gc_CollectionCount{name=~".*Old.*"}[10m]) > 0
severity: critical

# 4. 线程数暴涨（线程池耗尽前兆）
expr: jvm_thread_ThreadCount > 400
for: 3m
severity: warning

```

## 六、线上故障配套排查工具栈（SRE事中处置）

监控发现SLI指标异常后，配套原生工具快速定位根因，形成完整闭环

- **CPU异常**：top、jstat、Arthas profiler 热点采样

- **内存异常/泄漏**：jstat、jmap、MAT 堆文件分析

- **线程阻塞/卡死**：jstack、Arthas thread 线程检测

## 七、落地总结

- **核心技术栈**：JMX Exporter（JavaAgent探针） + Prometheus + Grafana + AlertManager

- **落地核心**：通过技术手段自动化采集SLI、监控SLO、管控ErrorBudget

- **最终效果**：实现线上稳定性可观测、可预判、可管控，达成SRE可持续运维目标

> （注：部分内容可能由 AI 生成）