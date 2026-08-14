# 09-打包发布

> Flutter 支持跨平台打包，本章覆盖 Android APK、iOS App Store、Linux/macOS/Windows 分发，以及 CI/CD 自动化构建。

---

## 1. APK 签名：Debug vs Release

### 1.1 Debug 签名

Debug 构建自动使用 Android SDK 自带的调试密钥签名：
- 密钥位置：`~/.android/debug.keystore`
- 密码：`android`
- 用途：**仅用于开发测试**，不能发布到应用市场

```bash
flutter build apk --debug
# 输出：build/app/outputs/flutter-apk/app-debug.apk
```

### 1.2 Release 签名

Release 构建需要正式的签名密钥：

**Step 1：生成签名密钥**

```bash
# 用 keytool（JDK 自带）生成 RSA 密钥
keytool -genkey -v -keystore ~/vexfy-release.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias vexfy \
  -storepass <密码> -keypass <密码> \
  -dname "CN=Vexfy, OU=Vexfy, O=Vexfy, L=Beijing, ST=Beijing, C=CN"
```

**Step 2：在 `android/app/build.gradle` 配置签名**

```groovy
// android/app/build.gradle
android {
    // ...

    signingConfigs {
        // 定义一个 signingConfig
        release {
            // 密钥文件路径（不要提交到 Git！）
            storeFile file("~/vexfy-release.jks")
            storePassword "<密码>"
            keyAlias "vexfy"
            keyPassword "<密码>"
        }
    }

    buildTypes {
        release {
            // 使用刚才定义的签名配置
            signingConfig signingConfigs.release
            // 开启代码压缩和混淆
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
        debug {
            signingConfig signingConfigs.debug  // Debug 用调试密钥
        }
    }
}
```

**Step 3：构建 Release APK**

```bash
flutter build apk --release
# 输出：build/app/outputs/flutter-apk/app-release.apk
```

**Java 对比：** 类似 Java JAR 的 `jarsigner -keystore keystore.jars app.jar`。

### 1.3 AAB（Android App Bundle）— Google Play 推荐格式

Google Play 要求 AAB 格式（国内厂商通常还是用 APK）：

```bash
flutter build appbundle --release
# 输出：build/app/outputs/bundle/release/app-release.aab
```

---

## 2. Android 应用市场发布

### 2.1 国内应用市场

| 平台 | 注册地址 | 需要的材料 |
|---|---|---|
| 华为应用市场 | AppGallery Connect | 企业/个人开发者认证 + 软著 |
| 小米应用商店 | 小米开放平台 | 企业认证 |
| OPPO 软件商店 | OPPO 开放平台 | 企业/个人认证 |
| vivo 应用商店 | vivo 开放平台 | 企业认证 |
| 腾讯应用宝 | 腾讯开放平台 | 企业认证 |

**发布流程（通用）：**
1. 注册开发者账号 + 实名认证
2. 准备材料：应用图标（多种尺寸）、截图（手机/平板）、应用描述、隐私政策 URL
3. 上传签名后的 Release APK / AAB
4. 填写分类、年龄分级、权限说明
5. 提交审核（1~7 天不等）

### 2.2 Google Play

1. 注册 [Google Play Console](https://play.google.com/console)（$25 一次性注册费）
2. 创建应用 → 填写商店信息 → 上传 AAB
3. 选择国家/地区 → 定价 → 内容分级（问卷）
4. 提交审核（通常 1~3 天）

**国内开发者注意事项：**
- Google Play 在国内无法访问，但海外用户必须通过 Google Play 安装
- 建议同时发布 Google Play 和国内渠道

---

## 3. iOS App Store 发布

### 3.1 准备工作

| 材料 | 说明 |
|---|---|
| Apple Developer 账号 | $99/年，企业账号 $299/年 |
| Mac + Xcode | 必须用 Mac 构建 |
| App Store Connect 账号 | 上传 App 需要 |
| 应用图标 | 1024x1024 PNG（App Store 用） |
| 截图 | iPhone 6.5" / iPhone 5.5" / iPad Pro 12.9" |

### 3.2 打包步骤

**Step 1：在 Xcode 配置签名**

- 打开 `ios/Runner.xcworkspace`
- Signing & Capabilities → Team 选择你的开发者账号
- Bundle Identifier 必须唯一（如 `com.vexfy.vexfy`）

**Step 2：Archive**

```bash
# 在 Mac 上执行
flutter build ipa --release
```

或在 Xcode 中：
- Product → Archive → 选择分发方式 → App Store Connect

**Step 3：上传到 App Store Connect**

```bash
# 使用 xcrun altool 上传
xcrun altool --upload-app \
  -type ios \
  -file build/ios/ipa/vexfy.ipa \
  -u <Apple ID> \
  -p <App 专用密码>
```

或使用 Xcode 的 Organizer 直接分发。

**Step 4：在 App Store Connect 填写信息**

- 应用名称、描述、关键词
- 上传截图（6.5" / 5.5" / iPad）
- 选择分类、年龄分级
- 提交审核（通常 1~3 天）

### 3.3 TestFlight 内测

在上架前，可以用 TestFlight 邀请外部测试用户：

1. Xcode → Product → Archive → 选择 TestFlight 分发
2. 在 App Store Connect 添加内部测试员（直接通过）或外部测试员（需要 Beta 审核）
3. 测试用户下载 TestFlight App，输入邀请码或访问链接即可安装

---

## 4. Linux / macOS / Windows 分发

### 4.1 Linux

```bash
flutter build linux --release
# 输出：build/linux/x64/release/bundle/vexfy（可执行文件 + so 库）
```

**分发方式：**
- 直接打包 `bundle` 目录（Linux 用户自己解压运行）
- Snapcraft（Linux 软件商店）
- Flatpak（跨发行版）
- AUR（Arch Linux 用户）

### 4.2 macOS

```bash
flutter build macos --release
# 输出：build/macos/Build/Products/Release/vexfy.app
```

**分发方式：**
- 直接分发 `.app` 目录（或压缩成 `.zip`）
- 上传到 App Store（需要签名 + 公证）
- Homebrew Cask（开源社区分发）

**macOS 代码签名 + 公证（ notarization）：**

```bash
# 签名
codesign --force --sign "Developer ID Application: Your Name" \
  --deep --options runtime \
  vexfy.app

#  notarization（Apple 验证应用安全性）
xcrun notarytool submit vexfy.app \
  --apple-id <Apple ID> \
  --password <App 专用密码> \
  --team-id <Team ID>
```

### 4.3 Windows

```bash
flutter build windows --release
# 输出：build/windows/runner/Release/vexfy.exe
```

**分发方式：**
- 直接分发 exe + DLL（需要 Visual C++ Runtime）
- MSIX / AppX（Windows Store）
- Inno Setup / NSIS 打包成安装程序（推荐，傻瓜式安装）

**Inno Setup 打包示例（脚本 `installer.iss`）：**

```iss
[Setup]
AppName=Vexfy
AppVersion=1.0.0
DefaultDirName={autopf}\Vexfy
OutputBaseFilename=vexfy-setup-1.0.0

[Files]
Source: "build\windows\runner\Release\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
```

---

## 5. CI/CD 自动化构建

### 5.1 GitHub Actions（推荐，免费）

在仓库根目录创建 `.github/workflows/flutter.yml`：

```yaml
name: Flutter CI/CD

on:
  push:
    branches: [main, release/*]
  pull_request:
    branches: [main]

jobs:
  # ========== Android 构建 ==========
  android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.27.0'   # 指定 Flutter 版本
          channel: 'stable'

      - run: flutter pub get

      - run: flutter build apk --release
        env:
          # 如果用到 Google Play 服务等，需要凭据
          GOOGLE_SERVICES_JSON: ${{ secrets.GOOGLE_SERVICES_JSON }}

      # 上传 APK 作为构建产物
      - uses: actions/upload-artifact@v4
        with:
          name: vexfy-android-apk
          path: build/app/outputs/flutter-apk/app-release.apk

  # ========== iOS 构建（仅 macOS Runner） ==========
  ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.27.0'
          channel: 'stable'

      - run: flutter pub get

      - run: flutter build ipa --release
        env:
          # iOS 发布签名需要证书和 Provisioning Profile
          FLUTTER_BUILD_IOS_CODE_SIGNINGIdentity: ${{ secrets.IOS_CODE_SIGNING_IDENTITY }}
          BUILD_PROVISIONING_PROFILE: ${{ secrets.IOS_PROVISIONING_PROFILE }}

      - uses: actions/upload-artifact@v4
        with:
          name: vexfy-ios-ipa
          path: build/ios/ipa/vexfy.ipa

  # ========== Linux 构建 ==========
  linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.27.0'
      - run: flutter pub get
      - run: flutter build linux --release
      - uses: actions/upload-artifact@v4
        with:
          name: vexfy-linux
          path: build/linux/x64/release/bundle
```

**在 GitHub 仓库 Settings → Secrets 中添加敏感信息：**
- `GOOGLE_SERVICES_JSON`（Android Firebase 配置）
- `IOS_CODE_SIGNING_IDENTITY`（iOS 签名证书）
- `IOS_PROVISIONING_PROFILE`（Provisioning Profile）

### 5.2 多平台触发条件

```yaml
on:
  push:
    tags:
      - 'v*'    # 打 Tag 时触发正式发布构建
```

### 5.3 自动发布到 GitHub Release

```yaml
  - name: Create GitHub Release
    if: startsWith(github.ref, 'refs/tags/v')
    uses: softprops/action-gh-release@v1
    with:
      files: |
        build/app/outputs/flutter-apk/app-release.apk
        build/ios/ipa/vexfy.ipa
        build/linux/x64/release/bundle/vexfy
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 6. 小结

| 平台 | 构建命令 | 产物 | 分发渠道 |
|---|---|---|---|
| Android Debug | `flutter build apk --debug` | `.apk` | 内部测试 |
| Android Release | `flutter build apk --release` | `.apk` / `.aab` | 应用市场 / 直接下载 |
| iOS | `flutter build ipa --release` | `.ipa` | App Store / TestFlight |
| Linux | `flutter build linux --release` | `bundle/` 目录 | 官网 / Snap / Flatpak |
| macOS | `flutter build macos --release` | `.app` | 官网 / App Store / Homebrew |
| Windows | `flutter build windows --release` | `.exe` | 官网 / Microsoft Store |

---

## 下一步

恭喜你完成 Dart 语言全部 9 章学习！ 🎉

结合 Vexfy 项目，继续探索：
- 完整的项目代码：[github.com/fomalhaut-m/vexfy](https://github.com/fomalhaut-m/vexfy.git)
- 音频处理：`audio_service` + `just_audio` 高级用法
- 状态持久化：GetX 状态保存到本地
- 歌词解析：LRC 格式解析 + 逐字高亮
