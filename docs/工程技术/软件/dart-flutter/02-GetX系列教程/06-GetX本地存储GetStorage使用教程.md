# GetStorage 轻量级本地存储

> GetStorage 是 GetX 官方配套的轻量级键值对存储方案，适合 Flutter 移动端数据持久化。

---

## 1. 为什么选择 GetStorage？

| 方案 | 适用场景 | 优点 | 缺点 |
|---|---|---|---|
| **GetStorage** | 轻量数据、简单键值对 | 轻量、无依赖、同步API | 不适合复杂结构 |
| **SharedPreferences** | 简单配置 | 原生支持 | 类型限制 |
| **Hive** | 复杂数据结构 | 高性能、支持加密 | 需要初始化 |
| **Sqflite** | 结构化数据 | SQL 查询能力 | 学习成本高 |

GetStorage 特点：**同步读写**、**无异步回调**、**轻量级**、**无需初始化**。

---

## 2. 安装

```yaml
# pubspec.yaml
dependencies:
  get_storage: ^2.1.1
```

```bash
flutter pub get
```

---

## 3. 初始化（App 入口）

在 `main.dart` 入口初始化：

```dart
import 'package:get_storage/get_storage.dart';

void main() async {
  await GetStorage.init();  // 必须异步初始化
  runApp(MyApp());
}
```

---

## 4. 基础用法

### 4.1 写入数据

```dart
// 存储字符串
GetStorage().write('name', 'Luke');

// 存储数字
GetStorage().write('age', 25);

// 存储布尔值
GetStorage().write('isDark', true);

// 存储列表
GetStorage().write('tags', ['flutter', 'getx', 'dart']);

// 存储 Map
GetStorage().write('user', {
  'id': 1,
  'name': 'Luke',
  'email': 'luke@example.com'
});
```

### 4.2 读取数据

```dart
// 读取字符串，默认值 ''
String name = GetStorage().read('name') ?? 'default';

// 读取数字，默认值 0
int age = GetStorage().read('age') ?? 0;

// 读取布尔值，默认值 false
bool isDark = GetStorage().read('isDark') ?? false;

// 读取列表
List tags = GetStorage().read('tags') ?? [];

// 读取 Map
Map? user = GetStorage().read('user');
```

### 4.3 删除数据

```dart
// 删除单个键
GetStorage().remove('name');

// 清空所有数据
GetStorage().erase();
```

### 4.4 检查键是否存在

```dart
bool exists = GetStorage().hasData('name');
```

---

## 5. 进阶用法：Service 封装

推荐封装为 GetxService，方便依赖注入：

```dart
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
}
```

使用方式：

```dart
// 初始化
await Get.putAsync(() => StorageService().init());

// 读取
final storage = Get.find<StorageService>();
bool isDark = storage.isDarkMode;

// 写入
await storage.setDarkMode(true);
```

---

## 6. 结合 GetX 响应式

配合 GetxController 实现响应式存储：

```dart
class ThemeController extends GetxController {
  final _isDark = false.obs;

  bool get isDark => _isDark.value;

  final StorageService _storage = Get.find<StorageService>();

  @override
  void onInit() {
    super.onInit();
    _isDark.value = _storage.isDarkMode;
  }

  void toggleTheme() async {
    _isDark.value = !_isDark.value;
    await _storage.setDarkMode(_isDark.value);
    Get.changeThemeMode(_isDark.value ? ThemeMode.dark : ThemeMode.light);
  }
}
```

在页面中使用：

```dart
class SettingsPage extends StatelessWidget {
  final ThemeController themeCtrl = Get.find();

  @override
  Widget build(BuildContext context) {
    return Obx(() => Switch(
      value: themeCtrl.isDark,
      onChanged: (_) => themeCtrl.toggleTheme(),
    ));
  }
}
```

---

## 7. 实际项目示例：用户登录状态持久化

```dart
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

  Future<void> login(String token, Map<String, dynamic> user) async {
    await _box.write(_tokenKey, token);
    await _box.write(_userKey, user);
    // 触发登录状态更新
    Get.find<AuthController>().updateUser(user);
  }

  Future<void> logout() async {
    await _box.remove(_tokenKey);
    await _box.remove(_userKey);
    Get.find<AuthController>().clearUser();
  }
}

// 使用
class AuthController extends GetxController {
  final RxMap<String, dynamic> user = RxMap();

  void updateUser(Map<String, dynamic> info) {
    user.value = info;
  }

  void clearUser() {
    user.clear();
  }
}
```

---

## 8. 注意事项

### 8.1 数据类型

GetStorage 存储时会丢失 Dart 类型信息，读取 Map 时需要注意：

```dart
// 写入
await storage.write('data', {'count': 10});

// 读取后需要强制转换类型
Map<String, dynamic> data = storage.read<Map<String, dynamic>>('data') ?? {};
int count = data['count'] as int;  // 需要强制转换
```

### 8.2 加密存储

如需加密存储敏感数据：

```dart
await GetStorage.init(
  encryptionCipher: HiveCipher.withPassphrase('your_secure_password'),
);
```

### 8.3 异常处理

建议配合 try-catch 使用：

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

## 9. 总结

- **GetStorage** 适合简单键值对存储，与 GetX 无缝集成
- 建议封装为 **Service** 统一管理存储逻辑
- 配合 **Obx** 或 **ObxBuilder** 实现响应式数据持久化
- 复杂数据结构建议使用 **Hive** 或 **Sqflite**

GetStorage 是 GetX 生态中最轻量的存储方案，非常适合快速原型和中小型项目。