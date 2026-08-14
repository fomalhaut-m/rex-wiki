# GetStorage 使用教程

> GetStorage 是 GetX 官方配套的轻量级键值对存储，与 GetX 生态无缝集成，适合快速原型和轻量数据存储。

---

## 一、简介

### 1.1 什么是 GetStorage？

GetStorage 是 GetX 官方配套的轻量级存储：
- **同步 API**：无需回调，直接读写
- **无依赖**：轻量级，包体积小
- **GetX 集成**：与 GetX Service 完美结合
- **可选加密**：支持 AES 加密存储
- **全平台支持**：Android/iOS/Windows/macOS/Linux

### 1.2 适用场景

- 轻量配置存储
- 与 GetX 项目配合
- 快速原型开发
- 用户偏好设置
- Token/用户信息持久化

### 1.3 官方资源

| 资源 | 链接 |
|---|---|
| Pub 页面 | https://pub.dev/packages/get_storage |
| GetX Storage 官方文档 | https://github.com/jonataslaw/get_storage |
| GitHub | https://github.com/jonataslaw/get_storage |

---

## 二、安装

```yaml
# pubspec.yaml
dependencies:
  get_storage: ^2.1.1
```

```bash
flutter pub get
```

---

## 三、基础用法

### 3.1 初始化（App 入口）

```dart
import 'package:get_storage/get_storage.dart';

void main() async {
  await GetStorage.init();
  runApp(MyApp());
}
```

### 3.2 写入数据

```dart
final storage = GetStorage();

// 存储字符串
await storage.write('name', 'Luke');

// 存储数字
await storage.write('age', 25);

// 存储布尔值
await storage.write('isDark', true);

// 存储列表
await storage.write('tags', ['flutter', 'getx', 'dart']);

// 存储 Map
await storage.write('user', {
  'id': 1,
  'name': 'Luke',
  'email': 'luke@example.com'
});
```

### 3.3 读取数据

```dart
final storage = GetStorage();

// 读取字符串，默认值 ''
String name = storage.read('name') ?? 'default';

// 读取数字，默认值 0
int age = storage.read('age') ?? 0;

// 读取布尔值，默认值 false
bool isDark = storage.read('isDark') ?? false;

// 读取列表
List tags = storage.read('tags') ?? [];

// 读取 Map
Map? user = storage.read('user');
```

### 3.4 删除数据

```dart
final storage = GetStorage();

// 删除单个键
await storage.remove('name');

// 清空所有数据
await storage.erase();
```

### 3.5 检查键是否存在

```dart
bool exists = storage.hasData('name');
```

---

## 四、加密存储

### 4.1 初始化加密

```dart
void main() async {
  await GetStorage.init(
    encryptionCipher: HiveCipher.withPassphrase('your_secure_password'),
  );
  runApp(MyApp());
}
```

### 4.2 使用加密

```dart
// 初始化时设置加密密钥
await GetStorage.init(
  encryptionCipher: HiveAesCipher(Hive.generateSecureKey()),
);

// 所有存储自动加密
await storage.write('token', 'sensitive_data');
String token = storage.read('token');  // 自动解密
```

---

## 五、Service 封装

### 5.1 创建 StorageService

```dart
// lib/services/storage_service.dart
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

class StorageService extends GetxService {
  late final GetStorage _box;

  Future<StorageService> init() async {
    await GetStorage.init();
    _box = GetStorage();
    return this;
  }

  // 通用读写方法
  T? read<T>(String key) => _box.read<T>(key);

  Future<void> write(String key, dynamic value) async {
    await _box.write(key, value);
  }

  Future<void> remove(String key) async => _box.remove(key);

  Future<void> clear() async => _box.erase();

  bool hasData(String key) => _box.hasData(key);

  // 业务方法封装
  bool get isDarkMode => read<bool>('isDarkMode') ?? false;

  Future<void> setDarkMode(bool value) async {
    await write('isDarkMode', value);
  }

  String? get token => read<String>('token');

  Future<void> setToken(String token) async {
    await write('token', token);
  }

  Future<void> clearToken() async => remove('token');

  Map<String, dynamic>? get userInfo => read<Map<String, dynamic>>('userInfo');

  Future<void> setUserInfo(Map<String, dynamic> info) async {
    await write('userInfo', info);
  }

  Future<void> clearUserInfo() async => remove('userInfo');
}
```

### 5.2 初始化

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Get.putAsync(() => StorageService().init());
  runApp(MyApp());
}
```

---

## 六、结合 GetX 响应式

### 6.1 创建响应式 Controller

```dart
// lib/controllers/theme_controller.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../services/storage_service.dart';

class ThemeController extends GetxController {
  final StorageService _storage = Get.find();

  final _isDark = false.obs;

  bool get isDark => _isDark.value;

  ThemeMode get themeMode => _isDark.value ? ThemeMode.dark : ThemeMode.light;

  @override
  void onInit() {
    super.onInit();
    _isDark.value = _storage.isDarkMode;
  }

  Future<void> toggleTheme() async {
    _isDark.value = !_isDark.value;
    await _storage.setDarkMode(_isDark.value);
    Get.changeThemeMode(themeMode);
  }
}
```

### 6.2 页面使用

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
            subtitle: Text(_isDark.value ? '已开启' : '已关闭'),
            value: themeCtrl.isDark,
            onChanged: (_) => themeCtrl.toggleTheme(),
          )),
        ],
      ),
    );
  }
}
```

---

## 七、实战示例：用户登录状态持久化

### 7.1 AuthService

```dart
// lib/services/auth_service.dart
import 'dart:convert';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

class AuthService extends GetxService {
  late final GetStorage _box;
  static const String _tokenKey = 'auth_token';
  static const String _userKey = 'user_info';

  Future<AuthService> init() async {
    _box = GetStorage();
    return this;
  }

  bool get isLoggedIn => _box.hasData(_tokenKey);

  String? get token => _box.read<String>(_tokenKey);

  Map<String, dynamic>? get userInfo {
    final str = _box.read<String>(_userKey);
    return str != null ? jsonDecode(str) : null;
  }

  Future<void> login(String token, Map<String, dynamic> user) async {
    await _box.write(_tokenKey, token);
    await _box.write(_userKey, jsonEncode(user));
    // 通知控制器更新
    Get.find<AuthController>().updateUser(user);
  }

  Future<void> logout() async {
    await _box.remove(_tokenKey);
    await _box.remove(_userKey);
    Get.find<AuthController>().clearUser();
  }
}

// lib/controllers/auth_controller.dart
class AuthController extends GetxController {
  final RxMap<String, dynamic> user = RxMap();

  void updateUser(Map<String, dynamic> info) {
    user.value = info;
  }

  void clearUser() {
    user.clear();
  }

  bool get isLoggedIn => user.isNotEmpty;
}
```

### 7.2 初始化和服务

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 初始化 Storage 和 Auth 服务
  final storageService = await Get.putAsync(() => StorageService().init());
  Get.put(AuthController());

  // 检查登录状态
  if (storageService.token != null) {
    final userInfo = storageService.userInfo;
    if (userInfo != null) {
      Get.find<AuthController>().updateUser(userInfo);
    }
  }

  runApp(MyApp());
}
```

### 7.3 登录页面

```dart
// lib/pages/login_page.dart
class LoginPage extends StatelessWidget {
  final AuthController _authCtrl = Get.find();
  final AuthService _authService = Get.find();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('登录')),
      body: Center(
        child: ElevatedButton(
          onPressed: () async {
            // 模拟登录
            const token = 'mock_token_123';
            final user = {
              'id': 1,
              'name': 'Luke',
              'email': 'luke@example.com'
            };

            await _authService.login(token, user);

            Get.offAll(() => HomePage());
          },
          child: Text('模拟登录'),
        ),
      ),
    );
  }
}
```

---

## 八、完整示例：应用配置管理

```dart
// lib/services/app_settings_service.dart
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:get_storage/get_storage.dart';

class AppSettingsService extends GetxService {
  late final GetStorage _box;

  Future<AppSettingsService> init() async {
    _box = GetStorage();
    return this;
  }

  // 主题设置
  bool get isDarkMode => _box.read<bool>('darkMode') ?? false;

  ThemeMode get themeMode => isDarkMode ? ThemeMode.dark : ThemeMode.light;

  Future<void> setDarkMode(bool value) async {
    await _box.write('darkMode', value);
    Get.changeThemeMode(themeMode);
  }

  // 语言设置
  String get locale => _box.read<String>('locale') ?? 'zh_CN';

  Locale get currentLocale {
    switch (locale) {
      case 'en': return Locale('en');
      case 'ja': return Locale('ja');
      default: return Locale('zh', 'CN');
    }
  }

  Future<void> setLocale(String locale) async {
    await _box.write('locale', locale);
    Get.updateLocale(currentLocale);
  }

  // 字体大小
  double get fontScale => _box.read<double>('fontScale') ?? 1.0;

  Future<void> setFontScale(double scale) async {
    await _box.write('fontScale', scale);
  }

  // 通知设置
  bool get notificationsEnabled => _box.read<bool>('notifications') ?? true;

  Future<void> setNotifications(bool value) async {
    await _box.write('notifications', value);
  }

  // 音乐质量
  String get musicQuality => _box.read<String>('musicQuality') ?? 'high';

  Future<void> setMusicQuality(String quality) async {
    await _box.write('musicQuality', quality);
  }

  // 清空设置
  Future<void> resetSettings() async {
    await _box.erase();
  }
}

// lib/controllers/settings_controller.dart
class SettingsController extends GetxController {
  final AppSettingsService _settings = Get.find();

  bool get isDarkMode => _settings.isDarkMode;
  String get locale => _settings.locale;
  double get fontScale => _settings.fontScale;
  bool get notificationsEnabled => _settings.notificationsEnabled;
  String get musicQuality => _settings.musicQuality;

  Future<void> toggleDarkMode() async {
    await _settings.setDarkMode(!isDarkMode);
    update();
  }

  Future<void> setLocale(String locale) async {
    await _settings.setLocale(locale);
    update();
  }

  Future<void> setFontScale(double scale) async {
    await _settings.setFontScale(scale);
    update();
  }
}
```

---

## 九、注意事项

### 9.1 数据类型丢失

GetStorage 存储时会丢失 Dart 类型，读取 Map 时需要处理：

```dart
// 写入
await storage.write('data', {'count': 10});

// 读取后强制转换
Map<String, dynamic>? data = storage.read<Map<String, dynamic>>('data');
if (data != null) {
  int count = data['count'] as int;  // 需要强制转换
}
```

### 9.2 异步初始化

```dart
// 确保在 main 中初始化
void main() async {
  await GetStorage.init();  // 必须先初始化
  await Get.putAsync(() => StorageService().init());
  runApp(MyApp());
}
```

### 9.3 异常处理

```dart
try {
  final data = _box.read<Map>('key');
  if (data != null) {
    // 处理数据
  }
} catch (e) {
  // 数据可能已损坏，清除并重新初始化
  await _box.remove('key');
}
```

---

## 十、与其他存储方案对比

| 特性 | GetStorage | SharedPreferences | Hive |
|---|---|---|---|
| 复杂度 | ⭐ 低 | ⭐ 低 | ⭐⭐ 中 |
| 性能 | ⭐⭐ 中 | ⭐⭐ 中 | ⭐⭐⭐ 高 |
| 类型安全 | ❌ | ❌ | ✅ |
| 加密支持 | ✅ | ❌ | ✅ |
| Web 支持 | ✅ | ✅ | ✅ |
| GetX 集成 | ✅✅ 最优 | ❌ | ✅ |
| 学习曲线 | 低 | 低 | 中 |

---

## 十一、总结

GetStorage 特点：

- ✅ **GetX 官方配套**：与 GetX 生态完美结合
- ✅ **简单易用**：同步 API，无需回调
- ✅ **轻量级**：包体积小
- ✅ **可选加密**：支持敏感数据存储
- ✅ **全平台支持**：所有 Flutter 平台

适用场景：
- GetX 项目中的存储
- 轻量配置和偏好设置
- 快速原型开发
- Token 和用户信息持久化

不适用场景：
- 复杂结构化数据（建议 drift/floor）
- 超大量数据（建议 Hive/drift）
- 需要复杂查询（建议 drift/sqflite）

GetStorage 是 GetX 项目中最推荐的轻量存储方案。