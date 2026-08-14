# Premain模式开发

## 基本概念

Premain模式是JavaAgent最常用的加载方式，在目标应用的主方法执行之前完成Agent的加载和初始化。通过在JVM启动参数中指定 `-javaagent` 参数，可以将Agent字节码注入到JVM中。

## 开发步骤

### 1. 创建Maven项目结构

```
agent-project/
├── pom.xml
└── src/main/java/
    └── com/example/
        └── MyAgent.java
```

### 2. 定义Agent类

```java
package com.example;

import java.lang.instrument.Instrumentation;

public class MyAgent {
    public static void premain(String args, Instrumentation inst) {
        System.out.println("[MyAgent] premain executed with args: " + args);
        inst.addTransformer(new MyTransformer());
    }
}
```

### 3. 创建类转换器

```java
package com.example;

import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.security.ProtectionDomain;

public class MyTransformer implements ClassFileTransformer {
    @Override
    public byte[] transform(
            ClassLoader loader,
            String className,
            Class<?> classBeingRedefined,
            ProtectionDomain protectionDomain,
            byte[] classfileBuffer) throws IllegalClassFormatException {
        System.out.println("[Transformer] Loading class: " + className);
        return null;
    }
}
```

## 完整示例：方法耗时统计

### 目标应用

```java
public class TargetApp {
    public void doSomething() {
        System.out.println("doing something...");
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        TargetApp app = new TargetApp();
        for (int i = 0; i < 5; i++) {
            app.doSomething();
        }
    }
}
```

### Agent实现

```java
import java.lang.instrument.Instrumentation;
import java.lang.instrument.ClassFileTransformer;
import java.security.ProtectionDomain;
import javassist.*;

public class TimingAgent {
    public static void premain(String args, Instrumentation inst) {
        System.out.println("[TimingAgent] Premain started");
        inst.addTransformer(new TimingTransformer());
    }

    static class TimingTransformer implements ClassFileTransformer {
        @Override
        public byte[] transform(
                ClassLoader loader,
                String className,
                Class<?> classBeingRedefined,
                ProtectionDomain protectionDomain,
                byte[] classfileBuffer) {
            if (!className.equals("TargetApp")) {
                return null;
            }

            try {
                ClassPool pool = ClassPool.getDefault();
                CtClass clazz = pool.get("TargetApp");

                for (CtMethod method : clazz.getDeclaredMethods()) {
                    method.addLocalVariable("startTime", CtClass.longType);
                    method.insertBefore("startTime = System.nanoTime();");
                    method.insertAfter(
                        "System.out.println(\"[Timing] " +
                        method.getName() + " cost: \" + " +
                        "(System.nanoTime() - startTime) / 1000000 + \"ms\");"
                    );
                }

                return clazz.toBytecode();
            } catch (Exception e) {
                e.printStackTrace();
                return null;
            }
        }
    }
}
```

## Maven配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>timing-agent</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.javassist</groupId>
            <artifactId>javassist</artifactId>
            <version>3.29.2-GA</version>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>com.example.TimingAgent</mainClass>
                            <addClasspath>true</addClasspath>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

## MANIFEST配置

如果使用普通Java项目（非Maven），需要手动创建 MANIFEST.MF：

```properties
Manifest-Version: 1.0
Premain-Class: com.example.TimingAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true
```

打包时确保 MANIFEST.MF 在 JAR 的 META-INF 目录下：

```bash
jar cfm timing-agent.jar META-INF/MANIFEST.MF com/example/*.class
```

## 运行Agent

### 打包Agent

```bash
mvn clean package
```

### 运行目标应用

```bash
java -javaagent:timing-agent.jar -jar target-app.jar
```

### 输出示例

```
[TimingAgent] Premain started
doing something...
[Timing] doSomething cost: 102ms
doing something...
[Timing] doSomething cost: 101ms
...
```

## 注意事项

| 注意事项 | 说明 |
|----------|------|
| 类名转换 | 返回 null 表示不修改类 |
| 异常处理 | transform方法异常会导致类加载失败 |
| 类加载器 | 注意要注入类的类加载器上下文 |
| 性能影响 | Agent本身会引入一定的性能开销 |
| 线程安全 | 多线程环境下注意并发安全 |

## 进阶技巧

### 1. 过滤目标类

```java
if (!className.startsWith("com/example/")) {
    return null;
}
```

### 2. 获取方法参数名

```java
CtMethod method = ...;
MethodInfo info = method.getMethodInfo();
LocalVariableAttribute attr = (LocalVariableAttribute)
    info.getCodeAttribute().getAttribute(LocalVariableAttribute.tag);
```

### 3. 注解驱动增强

```java
@interface Timed {
}

if (method.hasAnnotation("com.example.Timed")) {
    // 只增强带注解的方法
}
```