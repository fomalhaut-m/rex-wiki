# 02-Flutter 项目结构速通

> 结合 Vexfy 项目实战学习 Flutter 项目结构，适合有 Java 基础的程序员快速上手

---

## 1. Vexfy 项目目录一览

```
vexfy/app/                    ← Flutter 项目根目录
├── lib/                      ← 所有 Dart 代码在这里
│   ├── main.dart             ← 【入口】App 启动的第一个文件
│   ├── app/                  ← 应用层
│   │   ├── core/             ← 核心配置（主题/常量/工具）
│   │   ├── routes/           ← 路由配置（页面跳转规则）
│   │   └── modules/          ← 【核心】功能模块（按页面划分）
│   ├── data/                 ← 数据层
│   │   ├── models/           ← 数据模型（对应 Java 的 Entity/DTO）
│   │   ├── database/         ← SQLite 数据库操作
│   │   ├── providers/        ← 数据源（从哪取数据）
│   │   └── repositories/     ← 数据仓库（封装数据操作）
│   ├── services/             ← 公共服务层
│   │   ├── player_service.dart      ← 播放器服务
│   │   ├── local_music_service.dart ← 本地音乐扫描
│   │   └── audio_handler_service.dart ← 后台播放+通知栏
│   └── widgets/              ← 通用组件（可复用的 UI）
│
├── android/                  ← Android 平台配置
├── ios/                      ← iOS 平台配置
└── pubspec.yaml              ← 【重要】依赖管理（类似 Maven pom.xml）
```

---

## 2. Flutter 对应 Java 概念速查

| Flutter | Java | 说明 |
|---------|------|------|
| `lib/` | `src/main/java/` | 源代码目录 |
| `main.dart` | `main(String[] args)` | 程序入口 |
| `modules/` | `controller/` + `service/` | 功能模块 |
| `models/` | `Entity` / `DTO` | 数据模型 |
| `services/` | `@Service` | 公共服务 |
| `pubspec.yaml` | `pom.xml` / `build.gradle` | 依赖管理 |
| `Widget` | `Component` | 界面组件 |
| `Scaffold` | `Activity` | 页面布局容器 |
| `GetX` | `Spring IOC` | 状态管理+依赖注入 |

---

## 3. 入口文件 main.dart

```dart
// 文件：app/lib/main.dart

void main() async {
    // async：异步初始化，Flutter 启动要做一些准备
    WidgetsFlutterBinding.ensureInitialized();
    
    // 初始化数据库
    await DatabaseHelper.instance.init();
    
    // 初始化音频服务（后台播放需要）
    await startAudioService();
    
    // 启动 App
    runApp(const VexfyApp());
}
```

**类似 Java Spring Boot 的启动：**

```java
// Java Spring Boot
public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
}
```

---

## 4. App 根 Widget

```dart
// Vexfy 的 App 入口 Widget
class VexfyApp extends StatelessWidget {
    const VexfyApp({super.key});

    @override
    Widget build(BuildContext context) {
        // build() = 类似 Java 的 render/Thymeleaf 模板
        return GetMaterialApp(
            // GetMaterialApp = GetX 的 MaterialApp，支持路由/状态管理
            title: 'Vexfy',
            theme: AppTheme.darkTheme,  // 暗色主题
            home: const HomePage(),     // 首页
        );
    }
}
```

---

## 5. 依赖管理 pubspec.yaml

```yaml
# 文件：app/pubspec.yaml（类似 Maven 的 pom.xml）

name: vexfy
description: Vexfy Music Player
version: 1.0.0+1

dependencies:
    # 【核心依赖】类似 Java 的 Maven 依赖
    flutter:
        sdk: flutter
    
    # 状态管理（我们用 GetX，类似 Spring 的 IOC 容器）
    get: ^4.6.6
    
    # 音频播放（类似 Java 的 JavaFX Media）
    just_audio: ^0.9.36
    
    # 后台播放 + 通知栏
    audio_service: ^0.18.12
    
    # 本地音乐扫描（查手机里的音频文件）
    on_audio_query: ^2.9.0
    
    # 本地数据库（类似 Java 的 JDBC / MyBatis）
    sqflite: ^2.3.2
    
    # 文件路径工具
    path_provider: ^2.1.2

dev_dependencies:
    flutter_test:
        sdk: flutter
    flutter_lints: ^3.0.1
```

**安装依赖命令：** `flutter pub get`（类似 `mvn compile`）

---

## 6. modules 目录结构（核心！）

```
app/lib/app/modules/
├── home/                    ← 首页（4个Tab的容器）
│   ├── home_page.dart       ← 首页主页面
│   └── home_binding.dart    ← 依赖注入（GetX）
│
├── player/                  ← Tab1 播放器页面
│   ├── player_page.dart     ← 播放器页面
│   ├── player_tab.dart      ← Tab内容
│   └── player.dart          ← 状态管理（Controller）
│
├── playlist/                ← Tab2 播放列表
│   ├── playlist_tab.dart
│   └── playlist.dart
│
├── stats/                   ← Tab3 播放统计
│   ├── stats_tab.dart
│   └── stats.dart
│
└── settings/               ← Tab4 设置
    ├── settings_tab.dart
    └── settings.dart
```

---

## 7. 一个真实的 Page 文件

```dart
// 文件：app/lib/app/modules/player/player_page.dart

class PlayerPage extends GetView<PlayerController> {
    // PlayerController：状态管理类
    // GetView<PlayerController>：自动获取 PlayerController 实例

    const PlayerPage({super.key});

    @override
    Widget build(BuildContext context) {
        // build() = 类似 Java 的 render/Thymeleaf 模板
        // 返回一个 Widget（界面组件）
        
        return Scaffold(
            // Scaffold = Android 的 Activity 布局容器
            // 提供了 AppBar / Body / BottomNav 等通用结构
            
            appBar: AppBar(
                title: const Text('播放器'),
                backgroundColor: Colors.black,
            ),
            
            body: Center(
                // Center = 居中布局
                child: Column(
                    // Column = 垂直布局，类似 div flex-direction:column
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                        Text(controller.currentSong.value.title),
                        Text(controller.currentSong.value.artist),
                        IconButton(
                            icon: Icon(controller.isPlaying.value 
                                ? Icons.pause 
                                : Icons.play_arrow),
                            onPressed: controller.playPause,
                        ),
                    ],
                ),
            ),
        );
    }
}
```

---

## 8. 运行 Flutter 项目

```bash
# 进入项目目录
cd /home/luke/workspace/vex/vexfy/app

# 查看可用设备
flutter devices

# 运行 App（debug模式，热重载）
flutter run

# 发布版本（性能更好）
flutter run --release
```

---

## 9. 目录结构速记图

```
main.dart  →  启动 App
     ↓
app/routes/  →  配置路由（去哪一页）
     ↓
app/modules/ →  每个功能模块（首页/播放器/列表/统计/设置）
     ↓
data/models/ + services/  →  数据层（存什么/怎么取）
     ↓
widgets/  →  通用组件（复用UI）
```

---

## 下一步

- [03-Widget基础](./03-Widget基础.md) — 写个简单界面
