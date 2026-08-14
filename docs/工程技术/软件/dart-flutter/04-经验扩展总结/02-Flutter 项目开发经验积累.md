# Flutter 项目开发经验积累

> 开发过程中积累的经验教训，可直接复用于其他项目
> 更新：2026-05-12

---

## 一、健康检测机制（启动时自动检测）

### 核心理念

**项目启动后，自动检测各项功能是否可用，精确定位问题。**

```
App 启动
  ↓
[健康检测] 逐一检测各项功能
  ↓
检测结果全部打印日志
  ↓
有问题 → 友好提示 + 降级方案 → 不闪退
```

### 完整健康检测清单

| 功能 | 检测方式 | 异常兜底 |
|------|---------|----------|
| 音频播放 | 播放1秒测试音（最小音量）| 提示"播放器暂不可用" |
| 数据库 | 读写测试 | 切换内存模式 |
| 文件读写 | 读写测试文件 | 提示"文件功能异常" |
| 存储权限 | permission_handler 检查 | 提示授与权限 |
| 网络状态 | connectivity_plus 检测 | 切换离线模式 |
| 通知栏权限 | 检查通知权限 | 提示开启通知 |
| 后台播放权限 | 检查后台音频权限 | 提示开启后台播放 |
| 音频焦点 | 检查音频焦点 | 自动处理焦点抢占 |
| 耳机检测 | 检测耳机插拔状态 | 插拔时自动暂停 |
| 磁盘空间 | 检查剩余空间 | 提示空间不足，停止缓存 |
| OSS连接 | ping OSS endpoint | 离线模式，暂停同步 |
| 内存状态 | 检查剩余内存 | 低内存时清理缓存 |

### 健康检测日志示例

```
[Vexfy] ===== App 启动 =====
[Vexfy] [健康检测] 数据库: ✅ 正常
[Vexfy] [健康检测] 文件读写: ✅ 正常
[Vexfy] [健康检测] 存储权限: ✅ 已授权
[Vexfy] [健康检测] 网络状态: ✅ 在线
[Vexfy] [健康检测] 通知栏权限: ⚠️ 未授权，请开启以接收后台播放控制
[Vexfy] [健康检测] 音频播放: ✅ 正常
[Vexfy] [健康检测] 后台播放: ✅ 正常
[Vexfy] [健康检测] 磁盘空间: ✅ 剩余 2.3GB
[Vexfy] [健康检测] 内存状态: ✅ 剩余 1.2GB
[Vexfy] ===== App 启动完成 =====
```

**注意：健康检测失败不影响 App 启动，只是提示用户或降级处理。**

1. 每个检测都要 try-catch，失败不影响 App 启动
2. 检测结果全部打印日志，精确到哪个功能有问题
3. 日志格式统一：`[健康检测] 功能名: 状态 + 详情`
4. 任何功能检测失败，要有友好提示而不是闪退

### 代码示例

```dart
class HealthChecker {
  final Talker logger;

  /// 检测播放器
  Future<void> checkAudioPlayer() async {
    try {
      await playerService.playTestSound(); // 播放测试音
      logger.info('[健康检测] 音频播放: 正常');
    } catch (e, s) {
      logger.error('[健康检测] 音频播放: 失败', e, s);
      // 降级方案：不崩，显示提示
      showToast('播放器暂不可用');
    }
  }

  /// 检测数据库
  Future<void> checkDatabase() async {
    try {
      await db.write('test_key', 'test_value');
      final value = await db.read('test_key');
      if (value != 'test_value') throw Exception('数据不一致');
      logger.info('[健康检测] 数据库: 正常');
    } catch (e, s) {
      logger.error('[健康检测] 数据库: 失败', e, s);
      // 降级方案：切换内存模式
      useInMemoryMode();
    }
  }

  /// 检测文件读写
  Future<void> checkFileSystem() async {
    try {
      final file = File('${tempDir}/test_health.txt');
      await file.writeAsString('test');
      final content = await file.readAsString();
      if (content != 'test') throw Exception('读写内容不一致');
      await file.delete();
      logger.info('[健康检测] 文件读写: 正常');
    } catch (e, s) {
      logger.error('[健康检测] 文件读写: 失败', e, s);
      showToast('文件读写功能异常');
    }
  }
}
```

---

## 二、日志规范（保证只看日志可精确定位问题）

### 核心原则

**所有关键步骤都要有日志，关键逻辑要打印入参出参。**

### 日志分级

| 级别 | 标签 | 使用场景 |
|------|------|---------|
| Debug | `[DEBUG]` | 调试信息，开发时看 |
| Info | `[INFO]` | 正常流程，如函数入口 |
| Warning | `[WARN]` | 异常但可处理，如权限缺失 |
| Error | `[ERROR]` | 异常且未处理，需要修复 |

### 日志格式

```dart
// 格式：[级别] 模块名 消息
// 示例：
logger.info('[PlayerService] 播放歌曲: ${song.title}');
logger.debug('[PlayerService] 入参: filePath=$filePath');
logger.warn('[PlayerService] 文件不存在，降级为在线URL');
logger.error('[PlayerService] 播放失败', e, s);
```

### 必须打印日志的地方

1. **函数入口**：打印入参
2. **函数出口**：打印出参（重要返回值）
3. **分支判断**：打印条件判断的输入
4. **异常捕获**：打印异常信息 + 堆栈
5. **外部调用**：网络请求、数据库操作等

---

## 三、异常处理原则（不让任何异常裸奔）

### 核心原则

**每个 async 函数都要有 try-catch，异常兜底不能少。**

### 处理策略

| 场景 | 处理方式 |
|------|---------|
| 播放器初始化失败 | 显示"播放器暂不可用"，不闪退 |
| 数据库初始化失败 | 切换内存模式兜底 |
| 权限获取失败 | 提示用户，而不是崩溃 |
| 网络请求失败 | 降级到离线模式 |
| 文件读取失败 | 返回空数据，不抛异常 |

### 代码模板

```dart
Future<Something> fetchSomething() async {
  try {
    logger.debug('[Service] fetchSomething 入参: id=$id');
    final result = await _repository.fetch(id);
    logger.info('[Service] fetchSomething 出参: ${result.length}条');
    return result;
  } catch (e, s) {
    logger.error('[Service] fetchSomething 异常', e, s);
    // 降级方案：返回空数据
    return [];
  }
}
```

### 异常兜底原则

1. **最外层兜底**：main() 有 try-catch，App 不闪退
2. **模块级兜底**：每个 Provider/Service 有 try-catch
3. **功能级兜底**：关键函数有 try-catch
4. **降级方案**：失败时提供 fallback，不影响整体功能

---

## 四、Flutter Android 打包经验

### 核心规则

详见：[Flutter Android 打包核心配置](./Flutter Android 打包核心配置.md)

| 经验 | 说明 |
|------|------|
| jcenter 禁用 | 只用 google() + mavenCentral() |
| on_audio_query 用 3.x | 不要用 1.x，会报 namespace |
| AGP 固定 7.0.4 | 当前最稳定版本 |
| Kotlin 固定 1.8.10 | 配合 AGP 7.0.4 |
| 打包前必 clean | 清除缓存避免异常 |

### Gradle Wrapper 反人类设计

详见：[Gradle Wrapper 反人类设计](../../../运维技术/Android/Gradle Wrapper 反人类设计.md)

**核心：系统装的 Gradle = 摆设，wrapper 强制自己下载。**

---

_最后更新：2026-05-12_
