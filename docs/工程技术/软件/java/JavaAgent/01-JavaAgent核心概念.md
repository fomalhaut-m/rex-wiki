# JavaAgent核心概念

## 什么是JavaAgent

JavaAgent是JVM提供的一种 instrumentation 能力，允许在JVM运行时动态修改字节码，从而在不修改源代码的情况下增强或监控应用程序的行为。它是Java SE 5引入的重要特性，为字节码操作提供了标准化的入口。

## 核心作用

| 作用 | 说明 |
|------|------|
| 字节码增强 | 在类加载前或加载时修改类的字节码 |
| 运行时注入 | 无需重启应用即可动态加载代理逻辑 |
| 功能扩展 | 实现APM、性能监控、热修复等功能的基础 |

## 工作机制

### JVM启动参数

JavaAgent通过JVM启动参数 `-javaagent` 加载：

```bash
java -javaagent:agent.jar -jar your-app.jar
```

### 两种加载模式

#### 1. Premain模式（启动时加载）

```java
public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        // 在应用启动前执行
    }
}
```

- 在主应用 main 方法之前执行
- 通过 MANIFEST.MF 配置 Agent-Class
- 适合监控初始化、类转换

#### 2. AgentMain模式（运行时加载）

```java
public class MyAgent {
    public static void agentmain(String args, Instrumentation inst) {
        // 在应用运行中动态加载
    }
}
```

- 允许在应用运行时动态Attach
- 适合热修复、动态监控切换

## 核心接口：Instrumentation

`java.lang.instrument.Instrumentation` 是JavaAgent的核心接口，提供以下关键能力：

### 类转换器注册

```java
public static void premain(String args, Instrumentation inst) {
    inst.addTransformer(new MyClassFileTransformer());
}
```

### 类重定义与重转换

```java
inst.retransformClasses(targetClass);
inst.redefineClasses(definition);
```

### 类增强器

```java
public interface ClassFileTransformer {
    byte[] transform(
        ClassLoader loader,
        String className,
        Class<?> classBeingRedefined,
        ProtectionDomain protectionDomain,
        byte[] classfileBuffer
    );
}
```

## MANIFEST配置

Agent JAR 必须包含正确的 MANIFEST.MF 配置：

```properties
Manifest-Version: 1.0
Premain-Class: com.example.MyAgent
Agent-Class: com.example.MyAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true
```

## 技术优势

| 优势 | 说明 |
|------|------|
| 无侵入 | 不需要修改业务代码 |
| 动态性 | 支持运行时动态加载 |
| 标准化 | JVM原生支持，API稳定 |
| 灵活性 | 支持任意字节码操作 |

## 应用场景

- **APM监控**：SkyWalking、Pinpoint 等工具的核心技术
- **热修复**：无需重启应用即可修复线上问题
- **性能分析**：JProfiler、Async-profiler 等工具的基础
- **AOP框架**：Spring AOP、AspectJ 等的实现机制
- **安全监控**：应用安全防护、漏洞检测

## 与ASM、javassist的关系

| 工具 | 说明 |
|------|------|
| JavaAgent | 提供运行时注入的入口和机制 |
| ASM | 低-level字节码操作库，性能最优 |
| javassist | 高-level字节码操作库，使用更简单 |

JavaAgent定义了「在哪里」进行字节码操作，而ASM和javassist定义了「如何」操作字节码。