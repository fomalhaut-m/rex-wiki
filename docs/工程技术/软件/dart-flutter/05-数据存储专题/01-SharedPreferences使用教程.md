# SharedPreferences 使用教程

> SharedPreferences 是 Flutter 官方推荐的轻量级键值对存储，适用于简单配置和用户偏好设置。

---

## 一、简介

### 1.1 什么是 SharedPreferences？

SharedPreferences 是轻量级数据持久化方案：
- **键值对存储**：String, int, double, bool, List<String>
- **同步读写**：无需回调，直接读取
- **持久化**：应用关闭后数据依然保留
- **全平台支持**：Android/iOS/Windows/macOS/Linux/Web

### 1.2 适用场景

- 用户偏好设置（主题、语言）
- 开关状态（首次使用标识、通知开关）
- 简单配置（服务器地址、分页大小）
- 登录状态 Token
- 应用内评分/收藏

**不适场景**：大量数据、结构化数据、复杂查询

### 1.3 官方资源

| 资源 | 链接 |
|---|---|
| Pub 页面 | https://pub.dev/packages/shared_preferences |
| 官方文档 | https://api.flutter.dev/flutter/shared_preferences/shared_preferences-library.html |

---

## 二、安装

```yaml
# pubspec.yaml
dependencies:
  shared_preferences: ^2.2.2
```

```bash
flutter pub get
```

---

## 三、基础用法

### 3.1 写入数据

```dart
import 'package:shared_preferences/shared_preferences.dart';

// 存储字符串
await SharedPreferences.getInstance().then((prefs) {
  prefs.setString('username', 'Luke');
});

// 存储数字
prefs.setInt('age', 25);
prefs.setDouble('height', 175.5);

// 存储布尔值
prefs.setBool('isDarkMode', true);

// 存储列表
prefs.setStringList('tags', ['flutter', 'dart', 'getx']);
```

### 3.2 读取数据

```dart
final prefs = await SharedPreferences.getInstance();

// 读取字符串，默认值 ''
String username = prefs.getString('username') ?? '';

// 读取数字，默认值 0
int age = prefs.getInt('age') ?? 0;
double height = prefs.getDouble('height') ?? 0.0;

// 读取布尔值，默认值 false
bool isDarkMode = prefs.getBool('isDarkMode') ?? false;

// 读取列表，默认值 []
List<String> tags = prefs.getStringList('tags') ?? [];
```

### 3.3 删除数据

```dart
final prefs = await SharedPreferences.getInstance();

// 删除单个键
await prefs.remove('username');

// 清空所有数据
await prefs.clear();
```

### 3.4 检查键是否存在

```dart
bool exists = prefs.containsKey('username');
```

---

## 四、进阶用法

### 4.1 存储 JSON 对象

```dart
import 'dart:convert';

// 存储 Map
Map<String, dynamic> userInfo = {
  'id': 1,
  'name': 'Luke',
  'email': 'luke@example.com'
};
await prefs.setString('userInfo', jsonEncode(userInfo));

// 读取 Map
String? userInfoStr = prefs.getString('userInfo');
if (userInfoStr != null) {
  Map<String, dynamic> userInfo = jsonDecode(userInfoStr);
}
```

### 4.2 存储 DateTime

```dart
// 存储 DateTime（转为时间戳）
DateTime lastLogin = DateTime.now();
await prefs.setInt('lastLogin', lastLogin.millisecondsSinceEpoch);

// 读取 DateTime
int? lastLoginMs = prefs.getInt('lastLogin');
if (lastLoginMs != null) {
  DateTime lastLogin = DateTime.fromMillisecondsSinceEpoch(lastLoginMs);
}
```

### 4.3 批量操作

```dart
// 批量写入
Future<void> saveSettings({
  required String theme,
  required String language,
  required bool notifications,
}) async {
  final prefs = await SharedPreferences.getInstance();
  await Future.wait([
    prefs.setString('theme', theme),
    prefs.setString('language', language),
    prefs.setBool('notifications', notifications),
  ]);
}
```

---

## 五、结合 GetX 使用

### 5.1 创建 Service

```dart
// lib/services/preferences_service.dart
import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';

class PreferencesService extends GetxService {
  late final SharedPreferences _prefs;

  Future<PreferencesService> init() async {
    _prefs = await SharedPreferences.getInstance();
    return this;
  }

  // 通用方法
  String? getString(String key) => _prefs.getString(key);
  Future<bool> setString(String key, String value) => _prefs.setString(key, value);

  int? getInt(String key) => _prefs.getInt(key);
  Future<bool> setInt(String key, int value) => _prefs.setInt(key, value);

  bool? getBool(String key) => _prefs.getBool(key);
  Future<bool> setBool(String key, bool value) => _prefs.setBool(key, value);

  Future<bool> remove(String key) => _prefs.remove(key);
  Future<bool> clear() => _prefs.clear();

  // 业务方法
  bool get isDarkMode => _prefs.getBool('isDarkMode') ?? false;
  Future<void> setDarkMode(bool value) => _prefs.setBool('isDarkMode', value);

  String get language => _prefs.getString('language') ?? 'zh';
  Future<void> setLanguage(String lang) => _prefs.setString('language', lang);

  String? get token => _prefs.getString('token');
  Future<void> setToken(String? token) async {
    if (token != null) {
      await _prefs.setString('token', token);
    } else {
      await _prefs.remove('token');
    }
  }
}
```

### 5.2 初始化

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Get.putAsync(() => PreferencesService().init());
  runApp(MyApp());
}
```

### 5.3 创建 Controller

```dart
// lib/controllers/theme_controller.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../services/preferences_service.dart';

class ThemeController extends GetxController {
  final PreferencesService _prefs = Get.find();

  bool get isDarkMode => _prefs.isDarkMode;

  ThemeMode get themeMode => isDarkMode ? ThemeMode.dark : ThemeMode.light;

  Future<void> toggleTheme() async {
    await _prefs.setDarkMode(!isDarkMode);
    Get.changeThemeMode(themeMode);
    update();  // 通知 UI 更新
  }
}
```

### 5.4 页面使用

```dart
class SettingsPage extends StatelessWidget {
  final ThemeController themeCtrl = Get.find();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('设置')),
      body: ListView(
        children: [
          Obx(() => SwitchListTile(
            title: Text('深色模式'),
            subtitle: Text('开启深色主题'),
            value: themeCtrl.isDarkMode,
            onChanged: (_) => themeCtrl.toggleTheme(),
          )),
        ],
      ),
    );
  }
}
```

---

## 六、完整示例：用户设置页面

```dart
// lib/controllers/settings_controller.dart
import 'dart:convert';
import 'package:get/get.dart';
import 'package:flutter/material.dart';
import '../services/preferences_service.dart';

class SettingsController extends GetxController {
  final PreferencesService _prefs = Get.find();

  // 主题
  bool get isDarkMode => _prefs.isDarkMode;
  ThemeMode get themeMode => isDarkMode ? ThemeMode.dark : ThemeMode.light;

  // 语言
  String get language => _prefs.language;
  static const languages = ['zh', 'en', 'ja'];

  // 通知
  bool get notifications => _prefs.getBool('notifications') ?? true;

  // 用户信息
  Map<String, dynamic>? get userInfo {
    final str = _prefs.getString('userInfo');
    return str != null ? jsonDecode(str) : null;
  }

  // 修改主题
  Future<void> setDarkMode(bool value) async {
    await _prefs.setBool('isDarkMode', value);
    Get.changeThemeMode(themeMode);
    update();
  }

  // 修改语言
  Future<void> setLanguage(String lang) async {
    await _prefs.setString('language', lang);
    update();
  }

  // 修改通知设置
  Future<void> setNotifications(bool value) async {
    await _prefs.setBool('notifications', value);
    update();
  }

  // 保存用户信息
  Future<void> setUserInfo(Map<String, dynamic> info) async {
    await _prefs.setString('userInfo', jsonEncode(info));
    update();
  }

  // 退出登录
  Future<void> logout() async {
    await _prefs.remove('token');
    await _prefs.remove('userInfo');
    // 跳转到登录页
    Get.offAllNamed('/login');
  }
}

// lib/pages/settings_page.dart
class SettingsPage extends StatelessWidget {
  final SettingsController ctrl = Get.put(SettingsController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('设置')),
      body: Obx(() => ListView(
        children: [
          // 主题设置
          SwitchListTile(
            title: Text('深色模式'),
            subtitle: Text('开启后使用深色主题'),
            value: ctrl.isDarkMode,
            onChanged: ctrl.setDarkMode,
          ),
          Divider(),

          // 语言设置
          ListTile(
            title: Text('语言'),
            subtitle: Text(_getLanguageName(ctrl.language)),
            trailing: Icon(Icons.chevron_right),
            onTap: () => _showLanguageDialog(),
          ),
          Divider(),

          // 通知设置
          SwitchListTile(
            title: Text('推送通知'),
            subtitle: Text('接收应用推送消息'),
            value: ctrl.notifications,
            onChanged: ctrl.setNotifications,
          ),
          Divider(),

          // 退出登录
          ListTile(
            title: Text('退出登录', style: TextStyle(color: Colors.red)),
            onTap: () => _confirmLogout(),
          ),
        ],
      )),
    );
  }

  String _getLanguageName(String code) {
    switch (code) {
      case 'zh': return '简体中文';
      case 'en': return 'English';
      case 'ja': return '日本語';
      default: return '未知';
    }
  }

  void _showLanguageDialog() {
    Get.dialog(AlertDialog(
      title: Text('选择语言'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: SettingsController.languages.map((lang) {
          return RadioListTile<String>(
            title: Text(_getLanguageName(lang)),
            value: lang,
            groupValue: ctrl.language,
            onChanged: (value) {
              if (value != null) {
                ctrl.setLanguage(value);
                Get.back();
              }
            },
          );
        }).toList(),
      ),
    ));
  }

  void _confirmLogout() {
    Get.dialog(AlertDialog(
      title: Text('确认退出'),
      content: Text('确定要退出登录吗？'),
      actions: [
        TextButton(onPressed: () => Get.back(), child: Text('取消')),
        ElevatedButton(
          onPressed: () {
            Get.back();
            ctrl.logout();
          },
          child: Text('退出'),
        ),
      ],
    ));
  }
}
```

---

## 七、常见问题

### 7.1 异步初始化

SharedPreferences 本身是异步的，建议在应用启动时初始化：

```dart
// 方式1：使用 FutureBuilder
FutureBuilder<SharedPreferences>(
  future: SharedPreferences.getInstance(),
  builder: (context, snapshot) {
    if (!snapshot.hasData) return CircularProgressIndicator();
    return MyApp(prefs: snapshot.data!);
  },
)

// 方式2：在 main 中等待
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  runApp(MyApp(prefs: prefs));
}
```

### 7.2 数据丢失

- 卸载应用会清除数据
- 清理应用缓存也会清除数据
- 敏感数据建议加密或使用其他存储方案

### 7.3 性能优化

```dart
// 不要频繁读写
// 不好：每次点击都保存
onChanged: (value) {
  prefs.setString('key', value);  // 频繁写入
}

// 推荐：批量或延迟保存
onChanged: (value) {
  _tempValue = value;
  Future.delayed(Duration(seconds: 1), () => prefs.setString('key', value));
}
```

---

## 八、总结

SharedPreferences 特点：

- ✅ **官方推荐**：Flutter 官方推荐
- ✅ **全平台支持**：所有平台通用
- ✅ **简单易用**：无需初始化
- ✅ **同步 API**：无需回调

适用场景：
- 轻量配置
- 用户偏好
- 简单状态

不适用场景：
- 大量数据
- 结构化数据
- 复杂查询