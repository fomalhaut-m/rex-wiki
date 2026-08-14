# Hive 数据库使用教程

> Hive 是高性能 NoSQL 键值对数据库，支持加密和 Web，适合离线缓存和复杂对象存储。

---

## 一、简介

### 1.1 什么是 Hive？

Hive 是轻量级 NoSQL 数据库：
- **高性能**：纯 Dart 实现，无需桥接
- **键值对存储**：类似 JSON 的文档数据库
- **类型安全**：支持 TypeAdapter 序列化
- **加密支持**：可选 AES 加密
- **Web 支持**：可在 Web 端使用

### 1.2 适用场景

- 离线数据缓存
- 复杂对象存储
- 需要加密的敏感数据
- 离线优先应用
- 快速原型开发

### 1.3 官方资源

| 资源 | 链接 |
|---|---|
| Pub 页面 | https://pub.dev/packages/hive |
| Flutter 封装 | https://pub.dev/packages/hive_flutter |
| 官方文档 | https://docs.hivedb.dev/ |
| GitHub | https://github.com/hivedb/hive |

---

## 二、安装配置

### 2.1 添加依赖

```yaml
# pubspec.yaml
dependencies:
  hive: ^2.2.3
  hive_flutter: ^1.1.0

dev_dependencies:
  hive_generator: ^2.0.1
  build_runner: ^2.4.7
```

### 2.2 安装命令

```bash
flutter pub get
```

---

## 三、基础用法

### 3.1 初始化

```dart
import 'package:hive_flutter/hive_flutter.dart';

void main() async {
  await Hive.initFlutter();
  runApp(MyApp());
}
```

### 3.2 打开 Box

```dart
// 打开普通 Box
var box = await Hive.openBox('myBox');

// 打开加密 Box
var encryptedBox = await Hive.openBox(
  'secureBox',
  encryptionCipher: HiveAesCipher(key),
);
```

### 3.3 写入数据

```dart
// 存储任何类型
box.put('name', 'Luke');
box.put('age', 25);
box.put('isActive', true);
box.put('scores', [100, 90, 85]);
box.put('metadata', {'theme': 'dark', 'lang': 'zh'});

// 存储日期
box.put('createdAt', DateTime.now());
```

### 3.4 读取数据

```dart
// 读取值
String name = box.get('name', defaultValue: 'default');
int age = box.get('age', defaultValue: 0);
bool isActive = box.get('isActive', defaultValue: false);

// 读取列表
List scores = box.get('scores', defaultValue: []);

// 读取 Map
Map metadata = box.get('metadata', defaultValue: {});
```

### 3.5 删除数据

```dart
// 删除单个
box.delete('name');

// 删除多个
box.deleteAll(['name', 'age']);

// 清空 Box
box.clear();
```

---

## 四、类型适配器（TypeAdapter）

### 4.1 简单模型

```dart
// 定义模型
@HiveType(typeId: 0)
class User {
  @HiveField(0)
  String name;

  @HiveField(1)
  int age;

  @HiveField(2)
  String? email;

  User({required this.name, required this.age, this.email});
}
```

### 4.2 生成适配器

```bash
dart run build_runner build
```

生成 `user.g.dart`：

```dart
@HiveType(typeId: 0)
class User extends HiveObject {
  @HiveField(0)
  String name;

  @HiveField(1)
  int age;

  @HiveField(2)
  String? email;

  User({required this.name, required this.age, this.email});
}

// 自动生成的适配器
class UserAdapter extends TypeAdapter<User> {
  @override
  final int typeId = 0;

  @override
  User read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };
    return User(
      name: fields[0] as String,
      age: fields[1] as int,
      email: fields[2] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, User obj) {
    writer
      ..writeByte(3)
      ..writeByte(0)
      ..write(obj.name)
      ..writeByte(1)
      ..write(obj.age)
      ..writeByte(2)
      ..write(obj.email);
  }

  @override
  int get hashCode => typeId.hashCode;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is UserAdapter &&
          runtimeType == other.runtimeType &&
          typeId == other.typeId;
}
```

### 4.3 注册适配器

```dart
void main() async {
  await Hive.initFlutter();

  // 注册适配器
  Hive.registerAdapter(UserAdapter());

  // 打开 Box（指定类型）
  var userBox = await Hive.openBox<User>('users');

  runApp(MyApp());
}
```

### 4.4 使用模型

```dart
// 存储 User 对象
var user = User(name: 'Luke', age: 25, email: 'luke@example.com');
await userBox.put('user1', user);

// 读取 User 对象
User? user = userBox.get('user1');
print(user?.name);  // Luke

// 获取所有用户
List<User> allUsers = userBox.values.toList();
```

---

## 五、进阶用法

### 5.1 Box 监听

```dart
// 监听变化
box.listenable().addListener(() {
  print('Box 发生了变化');
});

// 或使用流
box.watch().listen((event) {
  print('Key: ${event.key}, Value: ${event.value}');
});
```

### 5.2 加密 Box

```dart
import 'dart:convert';
import 'dart:typed_data';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter/foundation.dart';

Future<void> initHive() async {
  await Hive.initFlutter();

  // 生成加密密钥
  final key = Hive.generateSecureKey();
  final cipher = HiveAesCipher(key);

  // 保存密钥（安全方式存储）
  // 实际应用中建议使用 flutter_secure_storage
  final secureBox = await Hive.openBox('secure_box');
  await secureBox.put('key', base64Encode(key));

  // 打开加密 Box
  final encryptedBox = await Hive.openBox(
    'encrypted_data',
    encryptionCipher: cipher,
  );
}
```

### 5.3 Lazy Box（延迟加载）

```dart
// Lazy Box 按需加载，性能更好
var lazyBox = await Hive.openLazyBox('lazyUsers');

// 实际读取时才加载
final user = await lazyBox.get('user1');

// 关闭不再需要的 Lazy Box
await lazyBox.close();
```

### 5.4 Box 嵌套

```dart
// 打开子 Box
var parentBox = await Hive.openBox('parent');
var childBox = await parentBox.openBox('child');

// 存储
await childBox.put('nested', 'value');

// 读取
final value = await parentBox.get('child.nested');
```

---

## 六、结合 GetX 使用

### 6.1 创建 Service

```dart
// lib/services/hive_service.dart
import 'package:get/get.dart';
import 'package:hive_flutter/hive_flutter.dart';

class HiveService extends GetxService {
  late final Box _settingsBox;
  late final Box _cacheBox;

  Box get settings => _settingsBox;
  Box get cache => _cacheBox;

  Future<HiveService> init() async {
    await Hive.initFlutter();

    // 打开设置 Box
    _settingsBox = await Hive.openBox('settings');

    // 打开缓存 Box
    _cacheBox = await Hive.openBox('cache');

    return this;
  }

  @override
  void onClose() {
    _settingsBox.close();
    _cacheBox.close();
    super.onClose();
  }
}
```

### 6.2 初始化

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Get.putAsync(() => HiveService().init());
  runApp(MyApp());
}
```

### 6.3 创建 Controller

```dart
// lib/controllers/user_controller.dart
import 'package:get/get.dart';
import '../models/user.dart';
import '../services/hive_service.dart';

class UserController extends GetxController {
  final HiveService _hive = Get.find();
  late final Box<User> _userBox;

  final RxList<User> users = <User>[].obs;
  final Rx<User?> currentUser = Rx<User?>(null);

  @override
  void onInit() {
    super.onInit();
    _initUserBox();
  }

  Future<void> _initUserBox() async {
    // 注册适配器
    if (!Hive.isAdapterRegistered(0)) {
      Hive.registerAdapter(UserAdapter());
    }
    _userBox = await Hive.openBox<User>('users');

    // 监听变化
    _userBox.listenable().addListener(_onUsersChanged);

    // 加载数据
    _loadUsers();
  }

  void _onUsersChanged() {
    users.value = _userBox.values.toList();
  }

  void _loadUsers() {
    users.value = _userBox.values.toList();
    final userId = _hive.settings.get('currentUserId');
    if (userId != null) {
      currentUser.value = _userBox.get(userId);
    }
  }

  Future<void> addUser(User user) async {
    await _userBox.put('user_${user.id}', user);
  }

  Future<void> updateUser(User user) async {
    await _userBox.put('user_${user.id}', user);
  }

  Future<void> deleteUser(int id) async {
    await _userBox.delete('user_$id');
  }

  Future<void> setCurrentUser(User? user) async {
    currentUser.value = user;
    if (user != null) {
      await _hive.settings.put('currentUserId', user.id);
    } else {
      await _hive.settings.remove('currentUserId');
    }
  }
}
```

---

## 七、实战示例：聊天消息缓存

```dart
// 定义消息模型
@HiveType(typeId: 1)
class ChatMessage {
  @HiveField(0)
  final String id;

  @HiveField(1)
  final String conversationId;

  @HiveField(2)
  final String content;

  @HiveField(3)
  final int senderId;

  @HiveField(4)
  final DateTime timestamp;

  @HiveField(5)
  final MessageType type;

  @HiveField(6)
  final bool isRead;

  ChatMessage({
    required this.id,
    required this.conversationId,
    required this.content,
    required this.senderId,
    required this.timestamp,
    required this.type,
    this.isRead = false,
  });
}

@HiveType(typeId: 2)
enum MessageType {
  @HiveField(0)
  text,
  @HiveField(1)
  image,
  @HiveField(2)
  file,
}

// 消息缓存服务
class MessageCacheService {
  static const String _boxName = 'messages';

  Future<Box<ChatMessage>> _getBox() async {
    if (!Hive.isAdapterRegistered(1)) {
      Hive.registerAdapter(ChatMessageAdapter());
    }
    if (!Hive.isAdapterRegistered(2)) {
      Hive.registerAdapter(MessageTypeAdapter());
    }
    return await Hive.openBox<ChatMessage>(_boxName);
  }

  Future<void> cacheMessages(List<ChatMessage> messages) async {
    final box = await _getBox();
    final Map<String, ChatMessage> entries = {
      for (var msg in messages) 'msg_${msg.id}': msg
    };
    await box.putAll(entries);
  }

  Future<List<ChatMessage>> getMessages(String conversationId) async {
    final box = await _getBox();
    return box.values
        .where((msg) => msg.conversationId == conversationId)
        .toList()
      ..sort((a, b) => a.timestamp.compareTo(b.timestamp));
  }

  Future<ChatMessage?> getLatestMessage(String conversationId) async {
    final messages = await getMessages(conversationId);
    return messages.isEmpty ? null : messages.last;
  }

  Future<void> clearConversation(String conversationId) async {
    final box = await _getBox();
    final keysToDelete = box.keys
        .where((key) => box.get(key)?.conversationId == conversationId)
        .toList();
    await box.deleteAll(keysToDelete);
  }
}
```

---

## 八、常见问题

### 8.1 适配器冲突

每个模型需要唯一的 `typeId`：

```dart
// 用户模型
@HiveType(typeId: 0)
class User { ... }

// 消息模型
@HiveType(typeId: 1)
class Message { ... }

// 确保 typeId 不重复
```

### 8.2 代码生成失败

```bash
# 清理并重新生成
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

### 8.3 Web 端不支持加密

```dart
// Web 端使用不同的加密方式
if (kIsWeb) {
  // Web 使用 IndexedDB，无需特殊处理
  box = await Hive.openBox('myBox');
} else {
  // 移动端使用加密
  box = await Hive.openBox(
    'myBox',
    encryptionCipher: HiveAesCipher(key),
  );
}
```

### 8.4 Box 已关闭

```dart
// 检查 Box 是否打开
if (box.isOpen) {
  // 安全操作
  await box.put('key', 'value');
}
```

---

## 九、性能优化

### 9.1 使用 Lazy Box

```dart
// 大数据量时使用 Lazy Box
var lazyBox = await Hive.openLazyBox('largeData');

// 按需加载
final item = await lazyBox.get('someKey');
```

### 9.2 批量写入

```dart
// 使用 putAll 批量写入，性能更好
await box.putAll({
  'key1': value1,
  'key2': value2,
  'key3': value3,
});
```

### 9.3 适当关闭 Box

```dart
// 不用时关闭，释放内存
await box.close();

// 需要时重新打开
box = await Hive.openBox('myBox');
```

---

## 十、总结

Hive 特点：

- ✅ **高性能**：纯 Dart 实现
- ✅ **类型安全**：TypeAdapter 序列化
- ✅ **加密支持**：可选 AES 加密
- ✅ **Web 支持**：可在 Web 使用
- ✅ **轻量**：无需复杂配置

适用场景：
- 离线缓存
- 复杂对象
- 需要加密
- 快速原型

不适用场景：
- 超大量数据（建议 drift）
- 复杂查询（建议 drift/floor）