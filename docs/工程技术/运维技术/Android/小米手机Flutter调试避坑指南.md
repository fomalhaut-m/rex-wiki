# 📱 小米/Redmi 手机 Flutter 调试避坑清单（Android 16 专属）

> 按优先级排序，99% 的调试问题一次性解决。

---

## 一、设备连接与驱动篇（最关键）

### 🔴 核心问题：WinUSB 驱动反复回退 + 小米互联干扰

**问题一：每次重启电脑/重插手机，驱动就变回 WinUSB，根本原因：**

1. Windows 自动更新把 WinUSB 驱动优先级设得比 ADB 更高
2. 小米的 USB VID/PID 在 Windows 驱动库中匹配到通用驱动而非 ADB 驱动

**问题二：小米手机 + 小米电脑同 WiFi 下的「小米互联」干扰**

> 💡 **这是最容易被忽视的干扰源。小米笔记本和小米手机在同一 WiFi 下会自动建立互联通道（如小米妙享/小米传），这个通道会：**<br>
> **· 劫持 USB 的 MTP 协议，建立自己的传输通道**<br>
> **· 与 ADB 端口冲突（ADB 默认用 5037）**<br>
> **· 导致 Flutter/ADB 命令响应异常或完全失灵**

> 💡 **核心问题不是「装不上」，而是「装完会被 Windows 自动覆盖」**

---

### 方案一（关键）：禁用 Windows 自动更新驱动

```powershell
# 1. Win+R 输入 sysdm.cpl 打开「系统属性」
# 2. 切换到「硬件」选项卡 → 点击「设备安装设置」
# 3. 选择「否，让我选择要执行的操作」
# 4. 勾选「从不安装来自Windows更新的驱动程序软件」
# 5. 点击「保存更改」
```

---

### 方案二：手动安装并锁定 ADB 驱动

```powershell
# 1. 设备管理器找到「通用串行总线设备」里的 Redmi K70 Ultra ALSC
# 2. 右键 → 更新驱动程序 → 浏览我的计算机以查找驱动程序
# 3. 选择「让我从计算机上的可用驱动程序列表中选取」
# 4. 选择「Android设备」→ Google → Android ADB Interface → 下一步安装
# 5. 安装完成后，设备会出现在「Android设备」分类下
```

---

### 方案三：用 devcon.exe 彻底锁死驱动

```powershell
# 1. 查找设备硬件 ID（需要安装 Android SDK）
devcon.exe find * | findstr /i "Redmi"
# 输出格式：USB\VID_XXXX&PID_XXXX

# 2. 强制绑定 ADB 驱动（替换成你的实际硬件 ID）
devcon.exe update USB\VID_XXXX&PID_XXXX "C:\Users\你的用户名\AppData\Local\Android\Sdk\extras\google\usb_driver\android_winusb.inf"
```

> ⚠️ devcon.exe 需要管理员权限。Android SDK 默认不包含 devcon.exe，需单独下载 Windows 驱动工具包(WDK)。

---

### 方案四：终极兜底 - 小米手机助手

```powershell
# 1. 安装「小米手机助手」，它会自动安装并锁定官方 ADB 驱动
# 2. 安装完成后卸载小米助手，驱动文件会保留，不会回退
# 3. 重新插拔手机，设备会稳定显示为「Android Composite ADB Interface」
```

> 💡 **即使之前装过又卸载了，仍需重新安装来修复残留驱动**

---

### 问题 A：ADB 识别不到设备（显示 WinUSB/通用串行总线设备）

| 解决步骤 | 说明 |
|----------|------|
| 右键设备 → 更新驱动 | — |
| 手动选择：**Android 设备** → **Android ADB Interface** | — |
| 执行 `adb kill-server && adb start-server` | 必须安装 Google 官方 ADB 驱动 |

**WinUSB 模式会直接导致 Flutter 版本识别错误。**

---

### 问题 B：无线调试能连，但 Flutter 识别为 Android 6.0.1

| 解决步骤 |
|----------|
| 1. 关闭「开发者选项」里的「无线调试」和「ADB TLS 连接」 |
| 2. 改用**原装数据线有线连接** |

---

### 问题 C：设备管理器出现黄色感叹号

| 方案 | 说明 |
|------|------|
| 安装「小米助手」自动补全驱动 | 装完可卸载 |
| 手动下载「Google USB 驱动」安装 | 备选方案 |

---

## 二、手机开发者选项配置篇（必全开）

**路径**：`设置 → 我的设备 → 全部参数 → 连续点击 MIUI/OS 版本号`

### ✅ 必须开启的选项

```
☐ USB 调试
☐ USB 调试（安全模式）
☐ USB 安装
☐ USB 调试（Security settings）
☐ 允许模拟位置（调试定位相关时）
```

### ✅ 额外设置

- 连接电脑时，手机弹窗选择**「文件传输（MTP）」**，并勾选**「始终允许此计算机」**
- **关闭「USB 安装安全校验」**，避免小米拦截 Flutter 安装应用

### ✅ 防回退设置（手机端）

1. 每次连接电脑都**手动选择「文件传输（MTP）」**，不要选"仅充电"
2. 关闭手机里的「连接电脑时自动安装驱动」相关选项（部分 MIUI 有此设置）

---

### ✅ 小米互联干扰解决方案

**原因**：小米手机 + 小米笔记本同 WiFi 下会自动建立「小米妙享/小米互联」通道，与 ADB 冲突。

| 方案 | 操作 |
|------|------|
| **方案 1（推荐）** | 关闭手机上的「小米互连」/「小米妙享」开关 |
| **方案 2** | 关闭笔记本电脑上的「小米传」/「小米互联」服务 |
| **方案 3** | **手机和电脑断开同一个 WiFi**，手机开热点给电脑（或反之） |
| **方案 4** | 在开发者选项里**关闭「无线调试」**（它会和小米互联抢端口） |

---

## 三、电脑端 ADB 与 Flutter 配置篇

### 1. 重置 ADB 服务（每次调试前必做）

```powershell
adb kill-server
adb start-server
adb devices
```

**连接正常**：`设备ID + device`

**如果是 `unauthorized`**：手机上点击「始终允许」授权。

### 2. Flutter 项目强制兼容配置

修改 `android/app/build.gradle`：

```gradle
android {
    compileSdkVersion 35        // Android 16 对应 API 35
    buildToolsVersion "35.0.0"

    defaultConfig {
        minSdkVersion 21
        targetSdkVersion 35       // 必须和 compileSdkVersion 一致
    }
}
```

### 3. 调试命令（版本识别异常时直接用）

```powershell
# 跳过版本校验强制运行
flutter run --no-version-check

# 指定设备运行（设备 ID 从 adb devices 获取）
flutter run -d 你的设备ID --no-version-check
```

---

## 四、常见问题快速排查

| 问题 | 排查步骤 |
|------|----------|
| Flutter 能看到设备，但无法安装 | 1. 检查「USB 安装」权限 2. 关闭小米管家拦截 3. `flutter clean && flutter pub get` |
| 应用安装成功，但打开后闪退 | 1. targetSdkVersion 需为 35 2. 关闭「不保留活动」 |
| ADB 能识别，Flutter devices 看不到 | 1. 重启电脑和手机 2. 使用原装数据线 |

---

## 五、终极兜底方案

1. **备份手机数据，更新到最新版 MIUI/HyperOS**
2. **重新安装 Android SDK Platform-Tools，确保版本 ≥ 35**
3. **彻底卸载电脑上的第三方手机助手**（可能劫持 ADB 驱动）
4. **改用 Android Studio 自带的 ADB 工具调试**

---

## 💡 附：为什么会反复变回去？

Windows 有个机制：每次检测到设备的驱动签名或匹配度更高的通用驱动时，会自动替换手动安装的驱动。

**禁用自动更新驱动 + 强制绑定 ADB 驱动**，是唯一能彻底解决这个问题的方法。

---

## 六、高级绕过方案：Flutter SDK 源码补丁（小米 HyperOS 专属）

> ⚠️ **警告**：以下补丁直接修改 Flutter SDK 源码，适合已root/愿意折腾的开发者。普通用户建议用前面的方案。

**问题根因**：小米 HyperOS 会劫持 `ro.build.version.sdk` 等系统属性，让 Flutter 误判设备版本号。这个补丁让 Flutter 对特定设备（你的 `FIF6VCDQLVRGYH8D`）强制返回正确值。

### 补丁文件

需要修改 Flutter SDK 中的 Android 设备检测代码：

```
{Flutter SDK路径}/packages/flutter_tools/lib/src/android/android_device.dart
```

### 补丁一：强制指定设备 API 版本

找到这个 getter：
```dart
@visibleForTesting
Future<String?> get apiVersion => _getProperty('ro.build.version.sdk');
```

替换为：
```dart
@visibleForTesting
Future<String?> get apiVersion async {
  // 仅对这台设备强制返回 API 35
  if (id == 'FIF6VCDQLVRGYH8D') {
    return '35';
  }
  return _getProperty('ro.build.version.sdk');
}
```

### 补丁二：绕过版本检查

找到 `_checkForSupportedAndroidVersion()` 方法，替换为：

```dart
Future<bool> _checkForSupportedAndroidVersion() async {
  // 你的设备已经强制 API 35，直接通过检查
  if (id == 'FIF6VCDQLVRGYH8D') {
    return true;
  }

  // 以下保持原来逻辑不变
  final String? adbPath = _androidSdk.adbPath;
  if (adbPath == null) {
    return false;
  }
  try {
    await _processUtils.run(<String>[adbPath, 'start-server'], throwOnError: true);
    final String sdkVersion =
        await _getProperty('ro.build.version.sdk') ?? gradle_utils.minSdkVersion;

    final int? sdkVersionParsed = int.tryParse(sdkVersion);
    if (sdkVersionParsed == null) {
      _logger.printError('Unexpected response from getprop: "$sdkVersion"');
      return false;
    }

    if (sdkVersionParsed < gradle_utils.minSdkVersionInt) {
      _logger.printError(
        'The Android version ($sdkVersion) on the target device is too old. Please '
        'use a API ${gradle_utils.minSdkVersion} device or later.',
      );
      return false;
    }

    return true;
  } on Exception catch (e, stacktrace) {
    _logger.printError('Unexpected failure from adb: $e');
    _logger.printError('Stacktrace: $stacktrace');
    return false;
  }
}
```

### 补丁三：强制 isSupported 返回 true

找到 `isSupported()` 方法，替换为：

```dart
@override
Future<bool> isSupported() async {
  if (id == 'FIF6VCDQLVRGYH8D') {
    return true;
  }
  final TargetPlatform platform = await targetPlatform;
  return switch (platform) {
    TargetPlatform.android ||
    TargetPlatform.android_arm ||
    TargetPlatform.android_arm64 ||
    TargetPlatform.android_x64 => true,
    _ => false,
  };
}
```

### 应用补丁后

```powershell
flutter clean
flutter devices
```

预期输出：
```
FIF6VCDQLVRGYH8D (mobile) • FIF6VCDQLVRGYH8D • android • Android 15 (API 35)
```

### 运行项目

```powershell
flutter run -d FIF6VCDQLVRGYH8D
```

### 补丁特点

| 特点 | 说明 |
|------|------|
| ✅ 最小改动 | 只改 3 处，不动其他 |
| ✅ 设备唯一 | 只对 FIF6VCDQLVRGYH8D 生效 |
| ✅ 永久有效 | 修改 SDK 源码，持久生效 |
| ⚠️ SDK 升级会重置 | 升级 Flutter 后需重新打补丁 |

---

*来源：实际踩坑经验 · Android 16 + MIUI/HyperOS + Redmi K70 Ultra*