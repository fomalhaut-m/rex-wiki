# Flutter Android 打包核心配置与常见坑

> Flutter Android 打包的标准配置和避坑指南，通用于所有 Flutter 项目
> 更新：2026-05-11

---

## 一、核心概念（必须理解）

### 1. Flutter Android 构建链

```
flutter build apk --release
     ↓
调用 gradlew
     ↓
下载对应版本 Gradle 
     ↓
Gradle 执行 build.gradle
     ↓
编译 Android 项目
```

### 2. 关键文件位置

| 文件 | 作用 | 注意 |
|------|------|------|
| `android/build.gradle` | 项目构建配置 | 不要手动改版本 |
| `android/app/build.gradle` | App 构建配置 | 主战场 |
| `android/gradle.properties` | Gradle 全局参数 | JVM 内存/编码 |

### 3. Flutter Gradle 与系统 Gradle 的关系

**系统装的 Gradle = 摆设**，Flutter 项目用 Gradle Wrapper 强制自己下载。

详见：[Gradle Wrapper 反人类设计](../../../运维技术/Android/Gradle Wrapper 反人类设计.md)

---

## 二、标准配置（直接复制使用）

### 1. android/build.gradle

```gradle
buildscript {
    ext.kotlin_version = '1.8.10'
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:7.0.4'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.buildDir = '../build'
subprojects {
    project.buildDir = "${rootProject.buildDir}/${project.name}"
}
subprojects {
    project.evaluationDependsOn(':app')
}

tasks.register("clean", Delete) {
    delete rootProject.layout.buildDirectory
}
```

### 2. android/gradle.properties

```properties
android.useAndroidX=true
android.enableJetifier=true
org.gradle.jvmargs=-Xmx2048M -Dfile.encoding=UTF-8
```

### 3. pubspec.yaml 核心依赖

```yaml
name: vexfy
description: "Vexfy - 个人音乐播放器"
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: ^3.11.5
  dart-native-assets: false

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.8
  get: ^4.6.6
  sqflite: ^2.3.3
  path_provider: ^2.1.3
  just_audio: ^0.9.40
  audio_service: ^0.18.15
  on_audio_query_pluse: ^3.0.6  # 必须用 3.x+，不要用 1.x
  uuid: ^4.4.2
  crypto: ^3.0.3
  path: ^1.9.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^6.0.0
  sqflite_common_ffi: ^2.4.0+3  # 桌面平台才需要

flutter:
  uses-material-design: true
```

---

## 三、常见坑与解决方案

### 坑1：jcenter 废弃导致依赖下载失败

**问题表现：**
```
Could not resolve xxx
> Could not get resource 'https://jcenter.bintray.com/...'
```

**原因：** jcenter 2021 年已废弃，新版 Gradle 不再支持。

**解决：** 仓库只保留 `google() + mavenCentral()`，不要加任何 jcenter 镜像。

```gradle
repositories {
    google()
    mavenCentral()
    // 不要加 jcenter()、aliyunjcenter()、maven.aliyun.com
}
```

---

### 坑2：Namespace not specified（AGP 7.1.0+）

**问题表现：**
```
Namespace not specified for plugin xxx
```

**原因：** AGP 7.1.0+ 强制要求 namespace，老插件不兼容。

**解决：**
1. 升级到支持 namespace 的插件版本（如 `on_audio_query_pluse: ^3.0.6`）
2. 或降级 AGP 到 7.0.4（治标不治本，不推荐）

---

### 坑3：构建内存不足 / 编码异常

**问题表现：**
```
OutOfMemoryError
Unsupported charset: "GBK"
```

**解决：** `gradle.properties` 配置：

```properties
org.gradle.jvmargs=-Xmx2048M -Dfile.encoding=UTF-8
```

---

### 坑4：Gradle 下载慢 / 失败

**原因：** Gradle 官网下载慢，或者没放到正确目录。

**解决：**
1. 配置国内镜像（可选）
2. 手动下载 zip 放到指定目录（根治）

详见：[Gradle Wrapper 反人类设计](../../../运维技术/Android/Gradle Wrapper 反人类设计.md)

---

## 四、固定打包命令

```bash
# 每次打包前清理缓存（必须）
flutter clean

# 安装依赖
flutter pub get

# 打包 Release APK
flutter build apk --release
```

**黄金规则：clean + pub get 后再打包，清缓存避免异常。**

---

## 五、版本对应表

| Flutter 版本 | AGP 版本 | Kotlin 版本 | Gradle 版本 |
|-------------|---------|------------|------------|
| 3.24+ | 8.5+ | 1.9+ | 8.14+ |
| 3.22+ | 8.3+ | 1.9+ | 8.10+ |
| 3.20+ | 8.2+ | 1.8+ | 8.4+ |
| 3.16+ | 8.2+ | 1.8+ | 8.4+ |

**AGP 7.0.4 + Kotlin 1.8.10 + Flutter 3.24+ 是当前最稳定组合。**

---

## 六、禁用规则（永久遵守）

1. ❌ 禁用 jcenter 及所有 jcenter 镜像
2. ❌ 禁用阿里云 maven 镜像（不稳定）
3. ❌ 禁止手动改 gradle-wrapper.properties 的 Gradle 版本
4. ❌ 禁止使用 1.x 版本的 `on_audio_query`（用 `on_audio_query_pluse`）

---

_最后更新：2026-05-11_
