# Android Gradle Wrapper 反人类设计

> Flutter/Android 项目 Gradle 下载失败的根因和根治方法
> 更新：2026-05-11

---

## 核心坑（超级反直觉）

### 1. 系统装的 Gradle = 摆设

Flutter/Android 项目**完全不用系统全局 Gradle**，系统装了什么、装对没装对，**项目完全不 care**。

### 2. 项目自带 gradlew，强制自己管理自己的 Gradle 版本

不管你电脑装没装、装对没对，它**必须自己下载一份对应版本**到 `~/.gradle/wrapper/dists/`。

### 3. 下载好了 zip 但没放进指定文件夹 = 死循环

你手动下载了 Gradle zip，但**没放进它指定的固定文件夹**，它就死循环一直下载、一直报错。

### 4. 一句话总结

**系统级安装 ≠ 项目使用**
Android/Flutter 就是这么设计的，故意隔离，**强制用 wrapper 自己下载**，特别反人类。

---

## 标准症状

```bash
flutter build apk --release
# 疯狂下载 Gradle，永远下不完
# 或者一直报错 Gradle not found / checksum mismatch
```

**系统 Gradle 明明装好了，Flutter 就是不用。**

---

## 根治方法（一步到位）

### Step 1：找出它期望的目录结构

```bash
ls ~/.gradle/wrapper/dists/gradle-8.14-all/
# 会显示一个类似 "xxxxxxxxxxxx/" 的随机 HASH 文件夹名
```

### Step 2：把下载好的 zip 复制进去

```bash
# 假设下载的是 gradle-8.14-all.zip
HASH=$(ls ~/.gradle/wrapper/dists/gradle-8.14-all/ 2>/dev/null | grep -v '\.lock' | head -1)
mkdir -p ~/.gradle/wrapper/dists/gradle-8.14-all/$HASH
cp ~/Downloads/gradle-8.14-all.zip ~/.gradle/wrapper/dists/gradle-8.14-all/$HASH/
```

### Step 3：直接打包（不下载）

```bash
flutter build apk --release
# 这次绝对不下载、直接编译
```

---

## 原理说明

```
Flutter 项目结构：
vexfy-app/
├── android/              ← 项目自己的 Gradle 配置
│   └── gradle/wrapper/
│       └── gradle-wrapper.properties  ← 指定了 Gradle 版本（如 8.14）
└── gradlew              ← Gradle Wrapper 脚本（强制用它）
```

当你运行 `flutter build apk --release`：

```
1. Flutter 调用 gradlew
2. gradlew 读取 gradle-wrapper.properties，发现需要 Gradle 8.14
3. gradlew 去 ~/.gradle/wrapper/dists/gradle-8.14-all/ 找
4. 找到 HASH 文件夹，检查 zip 是否存在 + checksum 是否正确
5. 不存在或不正确 → 开始下载 → 报错/死循环
6. zip 存在且正确 → 解压到 HASH 文件夹内 → 编译成功
```

**核心逻辑：它不看你系统装了什么，只看自己的 ~/.gradle/wrapper/dists/ 有没有正确放置的 zip。**

---

## 正确的下载流程（非根治，只是另一种方式）

### 方法1：让它自己下载（慢+容易失败）

```bash
flutter build apk --release
# 慢慢等它下载，经常失败
```

### 方法2：提前手动放 zip（根治）

```bash
# 1. 先让它尝试验证（触发创建目录结构）
flutter build apk --debug 2>&1 | head -5
# 会立即失败，但会在 ~/.gradle/wrapper/dists/ 创建目录

# 2. 找到它创建的 HASH 目录
ls ~/.gradle/wrapper/dists/gradle-8.14-all/

# 3. 下载 Gradle zip（去官网或镜像）
wget https://services.gradle.org/distributions/gradle-8.14-all.zip -O ~/Downloads/gradle-8.14-all.zip

# 4. 复制到它指定的目录
cp ~/Downloads/gradle-8.14-all.zip ~/.gradle/wrapper/dists/gradle-8.14-all/<HASH>/

# 5. 重新打包
flutter build apk --release
```

---

## 常用 Gradle 版本对应

| Flutter 版本 | Gradle 版本 | Android Gradle Plugin |
|-------------|------------|---------------------|
| Flutter 3.24+ | Gradle 8.14 | AGP 8.5+ |
| Flutter 3.22+ | Gradle 8.10 | AGP 8.3+ |
| Flutter 3.16+ | Gradle 8.4 | AGP 8.2+ |

查看当前项目使用的版本：

```bash
cat android/gradle/wrapper/gradle-wrapper.properties
```

---

## 其他相关命令

```bash
# 查看当前 Gradle 下载状态
ls -la ~/.gradle/wrapper/dists/

# 清除下载缓存（强制重新下载）
rm -rf ~/.gradle/wrapper/dists/gradle-8.14-all/

# 查看 Flutter 要求的 Gradle 版本
grep -r "gradle" android/settings.gradle
```

---

## 镜像加速（可选）

如果下载很慢，可以配置国内镜像：

```bash
# 在 ~/.gradle/gradle.properties 中添加
org.gradle.jvmargs=-Xmx4g -Xms512m
org.gradle.daemon=true
org.gradle.parallel=true
```

---

_最后更新：2026-05-11_
