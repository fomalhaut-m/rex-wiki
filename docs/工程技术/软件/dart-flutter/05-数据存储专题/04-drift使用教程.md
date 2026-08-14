# drift 数据库使用教程

> drift 是 Flutter 官方推荐的 SQLite ORM，功能最强大、最稳定，适合大型应用。

---

## 一、drift 简介

### 1.1 什么是 drift？

drift（原名 moor）是 Flutter 最强大的 SQLite ORM：
- **类型安全**：编译时检查 SQL 错误
- **声明式**：用 Dart 代码定义表结构
- **响应式**：支持流式查询更新 UI
- **全平台**：支持 Android/iOS/Windows/macOS/Linux/Web

### 1.2 官方资源

| 资源 | 链接 |
|---|---|
| Pub 页面 | https://pub.dev/packages/drift |
| 官方文档 | https://drift.simonbinder.eu/ |
| GitHub | https://github.com/simonb97/drift |
| 示例项目 | https://github.com/simonb97/drift-examples |

### 1.3 drift vs 其他方案

| 特性 | drift | floor | sqflite |
|---|---|---|---|
| 类型安全 | ✅ 完整 | ✅ 完整 | ❌ |
| 代码生成 | ✅ 自动 | ✅ 自动 | ❌ |
| 流式查询 | ✅ | ✅ | ❌ |
| Web 支持 | ✅ | ❌ | ❌ |
| 迁移支持 | ✅ 完整 | ✅ | ❌ |
| 学习曲线 | 中高 | 中 | 高 |

---

## 二、安装配置

### 2.1 添加依赖

```yaml
# pubspec.yaml
dependencies:
  drift: ^2.14.0
  sqlite3_flutter_libs: ^0.5.18
  path_provider: ^2.1.1
  path: ^1.8.3

dev_dependencies:
  drift_dev: ^2.14.0
  build_runner: ^2.4.7
```

### 2.2 桌面平台额外配置

```yaml
# 如果需要 Windows/macOS/Linux 支持
dependencies:
  drift: ^2.14.0
  sqlite3_flutter_libs: ^0.5.18
  drift_flutter: ^0.0.1  # 简化桌面集成

dev_dependencies:
  drift_dev: ^2.14.0
  build_runner: ^2.4.7
```

### 2.3 安装命令

```bash
flutter pub get
```

---

## 三、创建数据库

### 3.1 定义表（Models）

```dart
// lib/database/tables/users.dart
import 'package:drift/drift.dart';

class Users extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text().withLength(min: 1, max: 100)();
  TextColumn get email => text().unique()();
  IntColumn get age => integer().nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}
```

### 3.2 定义数据库类

```dart
// lib/database/database.dart
import 'dart:io';
import 'package:drift/drift.dart';
import 'package:drift_flutter/drift_flutter.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import 'tables/users.dart';

part 'database.g.dart';

@DriftDatabase(tables: [Users])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  // 查询所有用户
  Future<List<User>> getAllUsers() => select(users).get();

  // 流式查询（实时更新）
  Stream<List<User>> watchAllUsers() => select(users).watch();

  // 插入用户
  Future<int> insertUser(UsersCompanion user) =>
      into(users).insert(user);

  // 更新用户
  Future<bool> updateUser(User user) => update(users).replace(user);

  // 删除用户
  Future<int> deleteUser(int id) =>
      (delete(users)..where((t) => t.id.equals(id))).go();
}

LazyDatabase _openConnection() {
  return driftDatabase(name: 'my_database');
}
```

### 3.3 生成代码

```bash
dart run build_runner build
```

生成后会产生 `database.g.dart` 文件。

---

## 四、进阶查询

### 4.1 条件查询

```dart
// 查询单个用户
Future<User?> getUserById(int id) =>
    (select(users)..where((t) => t.id.equals(id))).getSingleOrNull();

// 模糊查询
Future<List<User>> searchUsers(String keyword) =>
    (select(users)..where((t) => t.name.like('%$keyword%'))).get();

// 多条件查询
Future<List<User>> getAdultUsers() =>
    (select(users)
      ..where((t) => t.age.isNotNull() & t.age.isBiggerOrEqualValue(18))
      ..orderBy([(t) => OrderingTerm.desc(t.createdAt)]))
    .get();
```

### 4.2 分页查询

```dart
Future<List<User>> getUsersPaginated(int page, int pageSize) {
  final offset = page * pageSize;
  return (select(users)
    ..limit(pageSize, offset: offset)
    ..orderBy([(t) => OrderingTerm.desc(t.createdAt)]))
    .get();
}
```

### 4.3 聚合查询

```dart
// 统计用户数量
Future<int> getUserCount() async {
  final count = users.id.count();
  final query = selectOnly(users)..addColumns([count]);
  final result = await query.getSingle();
  return result.read(count) ?? 0;
}

// 统计平均年龄
Future<double?> getAverageAge() async {
  final avg = users.age.avg();
  final query = selectOnly(users)..addColumns([avg]);
  final result = await query.getSingle();
  return result.read(avg);
}
```

---

## 五、数据迁移

### 5.1 添加新表

```dart
@DriftDatabase(tables: [Users, Posts])
class AppDatabase extends _$AppDatabase {
  @override
  int get schemaVersion => 2;  // 版本号+1

  @override
  MigrationStrategy get migration {
    return MigrationStrategy(
      onCreate: (Migrator m) async {
        await m.createAll();
      },
      onUpgrade: (Migrator m, int from, int to) async {
        // 处理迁移
        if (from < 2) {
          // 从 v1 升级到 v2
          await m.createTable(posts);
        }
      },
    );
  }
}
```

### 5.2 添加/修改列

```dart
// 添加新列
onUpgrade: (Migrator m, int from, int to) async {
  if (from < 3) {
    await m.addColumn(users, users.phoneNumber);
  }
},
```

### 5.3 数据迁移示例

```dart
@override
MigrationStrategy get migration {
  return MigrationStrategy(
    onCreate: (Migrator m) async {
      await m.createAll();
    },
    onUpgrade: (Migrator m, int from, int to) async {
      if (from == 1) {
        // v1 -> v2
        await m.addColumn(users, users.avatar);
      }
      if (from < 3) {
        // 所有小于 v3 的版本都需要这个迁移
        await m.addColumn(users, users.bio);
      }
    },
    beforeOpen: (details) async {
      // 每次打开数据库时执行
      if (details.wasCreated) {
        // 数据库刚创建，插入初始数据
        await _insertDefaultData();
      }
    },
  );
}
```

---

## 六、结合 GetX 使用

### 6.1 创建 Service

```dart
// lib/services/database_service.dart
import 'package:get/get.dart';
import 'package:path_provider/path_provider.dart';
import '../database/database.dart';

class DatabaseService extends GetxService {
  late final AppDatabase _db;

  AppDatabase get db => _db;

  Future<DatabaseService> init() async {
    final dir = await getApplicationDocumentsDirectory();
    _db = AppDatabase(LazyDatabase(() => SqliteDatabase.file(
      File(p.join(dir.path, 'my_database.sqlite')),
    )));
    return this;
  }

  @override
  void onClose() {
    _db.close();
    super.onClose();
  }
}
```

### 6.2 初始化数据库

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 初始化数据库
  await Get.putAsync(() => DatabaseService().init());

  runApp(MyApp());
}
```

### 6.3 创建 GetxController

```dart
// lib/controllers/user_controller.dart
import 'package:get/get.dart';
import '../database/database.dart';
import '../services/database_service.dart';

class UserController extends GetxController {
  final DatabaseService _dbService = Get.find<DatabaseService>();

  final RxList<User> users = <User>[].obs;
  final RxBool isLoading = false.obs;

  @override
  void onInit() {
    super.onInit();
    _watchUsers();
  }

  void _watchUsers() {
    _dbService.db.watchAllUsers().listen((userList) {
      users.value = userList;
    });
  }

  Future<void> addUser(String name, String email, int? age) async {
    await _dbService.db.insertUser(UsersCompanion(
      name: Value(name),
      email: Value(email),
      age: Value(age),
    ));
  }

  Future<void> deleteUser(int id) async {
    await _dbService.db.deleteUser(id);
  }
}
```

### 6.4 页面使用

```dart
class UserListPage extends StatelessWidget {
  final UserController ctrl = Get.put(UserController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('用户列表')),
      body: Obx(() {
        if (ctrl.isLoading.value) {
          return Center(child: CircularProgressIndicator());
        }
        return ListView.builder(
          itemCount: ctrl.users.length,
          itemBuilder: (context, index) {
            final user = ctrl.users[index];
            return ListTile(
              title: Text(user.name),
              subtitle: Text(user.email),
              trailing: IconButton(
                icon: Icon(Icons.delete),
                onPressed: () => ctrl.deleteUser(user.id),
              ),
            );
          },
        );
      }),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddDialog(),
        child: Icon(Icons.add),
      ),
    );
  }

  void _showAddDialog() {
    Get.dialog(
      AlertDialog(
        title: Text('添加用户'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              decoration: InputDecoration(labelText: '姓名'),
              onChanged: (v) => name = v,
            ),
            TextField(
              decoration: InputDecoration(labelText: '邮箱'),
              onChanged: (v) => email = v,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back(),
            child: Text('取消'),
          ),
          ElevatedButton(
            onPressed: () {
              ctrl.addUser(name, email, null);
              Get.back();
            },
            child: Text('添加'),
          ),
        ],
      ),
    );
  }
}
```

---

## 七、实战示例：聊天消息存储

```dart
// 定义消息表
class Messages extends Table {
  IntColumn get id => integer().autoIncrement()();
  IntColumn get conversationId => integer()();
  TextColumn get content => text()();
  IntColumn get senderId => integer()();
  BoolColumn get isRead => boolean().withDefault(const Constant(false))();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

@DriftDatabase(tables: [Messages])
class AppDatabase extends _$AppDatabase {
  // 查询会话消息
  Stream<List<Message>> watchConversationMessages(int convId) {
    return (select(messages)
      ..where((t) => t.conversationId.equals(convId))
      ..orderBy([(t) => OrderingTerm.desc(t.createdAt)]))
      .watch();
  }

  // 获取未读消息数
  Future<int> getUnreadCount(int convId) async {
    final count = messages.id.count();
    final query = selectOnly(messages)
      ..addColumns([count])
      ..where(messages.conversationId.equals(convId) & messages.isRead.equals(false));
    final result = await query.getSingle();
    return result.read(count) ?? 0;
  }

  // 标记消息已读
  Future<void> markAsRead(int convId, int userId) async {
    await (update(messages)
      ..where((t) => t.conversationId.equals(convId) & t.senderId.equals(userId) & t.isRead.equals(false)))
      .write(const MessagesCompanion(isRead: Value(true)));
  }
}
```

---

## 八、常见问题

### 8.1 编译报错 "Cannot find name 'Value'"

导入 drift：

```dart
import 'package:drift/drift.dart';
```

### 8.2 代码生成失败

```bash
# 清理并重新生成
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

### 8.3 Web 端不支持

```dart
// 使用 drift_flutter 包支持 Web
import 'package:drift_flutter/drift_flutter.dart';

LazyDatabase _openConnection() {
  return driftDatabase(name: 'my_database');
}
```

### 8.4 迁移失败

```dart
onUpgrade: (Migrator m, int from, int to) async {
  await customStatement('PRAGMA foreign_keys = OFF');
  // 执行迁移
  await customStatement('PRAGMA foreign_keys = ON');
}
```

---

## 九、总结

drift 是 Flutter 最推荐的 SQLite ORM：

- ✅ **全平台支持**（包括 Web）
- ✅ **类型安全**（编译时检查）
- ✅ **响应式查询**（Stream 实时更新）
- ✅ **完整迁移支持**
- ✅ **Flutter 官方推荐**

适合微信级别的大型应用，是企业级项目的首选方案。