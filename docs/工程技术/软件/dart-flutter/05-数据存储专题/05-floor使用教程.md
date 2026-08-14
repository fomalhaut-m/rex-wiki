# floor 数据库使用教程

> floor 是类似 Android Room 的 SQLite ORM，简单易学，适合有 Android 背景的开发者。

---

## 一、floor 简介

### 1.1 什么是 floor？

floor 是 Flutter 的 SQLite ORM，API 设计灵感来自 Android Room：
- **注解驱动**：通过注解自动生成代码
- **类型安全**：编译时检查 SQL 错误
- **DAO 模式**：数据访问对象分离
- **依赖注入**：与 GetX 等状态管理完美结合

### 1.2 官方资源

| 资源 | 链接 |
|---|---|
| Pub 页面 | https://pub.dev/packages/floor |
| GitHub | https://github.com/puszekajnik/floor |
| 示例项目 | https://github.com/vincenzopalazzo/floor_tutorial |

### 1.3 floor vs drift vs sqflite

| 特性 | floor | drift | sqflite |
|---|---|---|---|
| 类型安全 | ✅ 完整 | ✅ 完整 | ❌ |
| 代码生成 | ✅ 注解 | ✅ 声明式 | ❌ |
| 流式查询 | ✅ | ✅ | ❌ |
| Web 支持 | ❌ | ✅ | ❌ |
| 学习曲线 | 中 | 中高 | 高 |
| API 风格 | 类似 Android Room | Dart 原生风格 | 原生 SQL |

---

## 二、安装配置

### 2.1 添加依赖

```yaml
# pubspec.yaml
dependencies:
  floor: ^1.4.2
  flutter:
    sdk: flutter

dev_dependencies:
  floor_generator: ^1.4.2
  build_runner: ^2.4.7
```

### 2.2 安装命令

```bash
flutter pub get
```

---

## 三、创建数据库

### 3.1 定义实体（Entity）

```dart
// lib/database/entity/user.dart
import 'package:floor/floor.dart';

@Entity(tableName: 'users')
class User {
  @PrimaryKey(autoGenerate: true)
  final int id;

  @ColumnInfo(name: 'name')
  final String name;

  @ColumnInfo(name: 'email')
  final String email;

  @ColumnInfo(name: 'age')
  final int? age;

  @ColumnInfo(name: 'created_at')
  final DateTime createdAt;

  User({
    required this.id,
    required this.name,
    required this.email,
    this.age,
    required this.createdAt,
  });
}
```

### 3.2 定义 DAO（数据访问对象）

```dart
// lib/database/dao/user_dao.dart
import 'package:floor/floor.dart';
import '../entity/user.dart';

@dao
abstract class UserDao {
  @Query('SELECT * FROM users')
  Future<List<User>> findAllUsers();

  @Query('SELECT * FROM users WHERE id = :id')
  Future<User?> findUserById(int id);

  @Query('SELECT * FROM users WHERE name LIKE :name')
  Future<List<User>> searchUsers(String name);

  @Insert(onConflict: OnConflictStrategy.replace)
  Future<void> insertUser(User user);

  @Update
  Future<void> updateUser(User user);

  @Delete
  Future<void> deleteUser(User user);

  @Query('DELETE FROM users WHERE id = :id')
  Future<void> deleteUserById(int id);
}
```

### 3.3 定义 Database 类

```dart
// lib/database/app_database.dart
import 'package:floor/floor.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart' as sqflite;

import 'entity/user.dart';
import 'dao/user_dao.dart';

part 'app_database.g.dart';

@Database(version: 1, entities: [User])
abstract class AppDatabase extends FloorDatabase {
  UserDao get userDao;
}
```

### 3.4 初始化数据库

```dart
// lib/database/database_builder.dart
import 'package:floor/floor.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import '../entity/user.dart';
import '../dao/user_dao.dart';
import 'app_database.dart';

Future<AppDatabase> getDatabase() async {
  return await $FloorAppDatabase
      .databaseBuilder('my_database.db')
      .build();
}
```

### 3.5 生成代码

```bash
dart run build_runner build
```

生成后会产生 `app_database.g.dart` 文件。

---

## 四、进阶用法

### 4.1 多表关联

```dart
// 帖子表
@Entity(tableName: 'posts', foreignKeys: [
  ForeignKey(
    childColumns: ['user_id'],
    parentColumns: ['id'],
    entity: User,
  )
])
class Post {
  @PrimaryKey(autoGenerate: true)
  final int id;

  final String title;

  final String content;

  final int userId;

  final DateTime createdAt;

  Post({
    required this.id,
    required this.title,
    required this.content,
    required this.userId,
    required this.createdAt,
  });
}
```

### 4.2 自定义查询

```dart
@dao
abstract class PostDao {
  // 多条件查询
  @Query('SELECT * FROM posts WHERE user_id = :userId ORDER BY created_at DESC')
  Future<List<Post>> findPostsByUser(int userId);

  // 分页查询
  @Query('SELECT * FROM posts ORDER BY created_at DESC LIMIT :limit OFFSET :offset')
  Future<List<Post>> findPostsPaginated(int limit, int offset);

  // 聚合查询
  @Query('SELECT COUNT(*) FROM posts WHERE user_id = :userId')
  Future<int> countPostsByUser(int userId);

  // 联表查询
  @Query('''
    SELECT posts.*, users.name as author_name
    FROM posts
    INNER JOIN users ON posts.user_id = users.id
    WHERE posts.id = :postId
  ''')
  Future<PostWithAuthor?> findPostWithAuthor(int postId);
}

// 使用 @Embedded 关联对象
class PostWithAuthor {
  @Embedded()
  final Post post;

  final String authorName;

  PostWithAuthor({required this.post, required this.authorName});
}
```

### 4.3 响应式查询（Stream）

```dart
@dao
abstract class UserDao {
  // 流式查询 - 数据变化自动通知
  @Query('SELECT * FROM users')
  Stream<List<User>> watchAllUsers();

  // 条件流式查询
  @Query('SELECT * FROM users WHERE id = :id')
  Stream<User?> watchUserById(int id);
}
```

---

## 五、数据库迁移

### 5.1 版本升级

```dart
Future<AppDatabase> getDatabase() async {
  return await $FloorAppDatabase
      .databaseBuilder('my_database.db')
      .addMigrations([
        // v2 迁移
        Migration1to2(),
        // v3 迁移
        Migration2to3(),
      ])
      .build();
}

// 定义迁移
class Migration1to2 extends Migration {
  @override
  void migrate(DriftDatabase database) {
    database.execute('''
      CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
      )
    ''');
  }
}
```

### 5.2 数据迁移示例

```dart
class Migration2to3 extends Migration {
  @override
  void migrate(DriftDatabase database) async {
    // 添加新列
    await database.execute('''
      ALTER TABLE users ADD COLUMN bio TEXT
    ''');

    // 迁移旧数据
    await database.execute('''
      UPDATE users SET bio = '默认简介' WHERE bio IS NULL
    ''');
  }
}
```

---

## 六、结合 GetX 使用

### 6.1 创建 Service

```dart
// lib/services/database_service.dart
import 'package:get/get.dart';
import '../database/app_database.dart';

class DatabaseService extends GetxService {
  late final AppDatabase _database;

  AppDatabase get database => _database;

  Future<DatabaseService> init() async {
    _database = await getDatabase();
    return this;
  }

  @override
  void onClose() {
    _database.close();
    super.onClose();
  }
}
```

### 6.2 初始化

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Get.putAsync(() => DatabaseService().init());

  runApp(MyApp());
}
```

### 6.3 创建 Controller

```dart
// lib/controllers/user_controller.dart
import 'package:get/get.dart';
import '../database/entity/user.dart';
import '../services/database_service.dart';

class UserController extends GetxController {
  final _dbService = Get.find<DatabaseService>();

  final RxList<User> users = <User>[].obs;
  final RxBool isLoading = false.obs;

  @override
  void onInit() {
    super.onInit();
    loadUsers();
  }

  Future<void> loadUsers() async {
    isLoading.value = true;
    try {
      final result = await _dbService.database.userDao.findAllUsers();
      users.value = result;
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> addUser(String name, String email, int? age) async {
    final user = User(
      id: 0,  // autoGenerate 会忽略这个值
      name: name,
      email: email,
      age: age,
      createdAt: DateTime.now(),
    );
    await _dbService.database.userDao.insertUser(user);
    await loadUsers();
  }

  Future<void> deleteUser(int id) async {
    await _dbService.database.userDao.deleteUserById(id);
    await loadUsers();
  }
}
```

---

## 七、实战示例：任务清单应用

### 7.1 定义实体

```dart
@Entity(tableName: 'tasks')
class Task {
  @PrimaryKey(autoGenerate: true)
  final int id;

  final String title;

  final String? description;

  final bool isCompleted;

  final int priority;  // 1=低 2=中 3=高

  final DateTime dueDate;

  final DateTime createdAt;

  Task({
    required this.id,
    required this.title,
    this.description,
    required this.isCompleted,
    required this.priority,
    required this.dueDate,
    required this.createdAt,
  });
}
```

### 7.2 定义 DAO

```dart
@dao
abstract class TaskDao {
  @Query('SELECT * FROM tasks ORDER BY isCompleted ASC, priority DESC, dueDate ASC')
  Stream<List<Task>> watchAllTasks();

  @Query('SELECT * FROM tasks WHERE isCompleted = 0 ORDER BY priority DESC, dueDate ASC')
  Stream<List<Task>> watchPendingTasks();

  @Query('SELECT * FROM tasks WHERE id = :id')
  Future<Task?> findTaskById(int id);

  @Insert
  Future<void> insertTask(Task task);

  @Update
  Future<void> updateTask(Task task);

  @Delete
  Future<void> deleteTask(Task task);

  @Query('UPDATE tasks SET isCompleted = :completed WHERE id = :id')
  Future<void> updateTaskStatus(int id, bool completed);

  @Query('DELETE FROM tasks WHERE isCompleted = 1')
  Future<void> deleteCompletedTasks();
}
```

### 7.3 Controller 实现

```dart
class TaskController extends GetxController {
  final _dbService = Get.find<DatabaseService>();
  final TaskDao _taskDao => _dbService.database.taskDao;

  final RxList<Task> tasks = <Task>[].obs;
  StreamSubscription<List<Task>>? _subscription;

  @override
  void onInit() {
    super.onInit();
    _subscription = _taskDao.watchAllTasks().listen((taskList) {
      tasks.value = taskList;
    });
  }

  @override
  void onClose() {
    _subscription?.cancel();
    super.onClose();
  }

  Future<void> addTask(String title, String? description, int priority, DateTime dueDate) async {
    final task = Task(
      id: 0,
      title: title,
      description: description,
      isCompleted: false,
      priority: priority,
      dueDate: dueDate,
      createdAt: DateTime.now(),
    );
    await _taskDao.insertTask(task);
  }

  Future<void> toggleTaskStatus(Task task) async {
    await _taskDao.updateTaskStatus(task.id, !task.isCompleted);
  }

  Future<void> deleteTask(Task task) async {
    await _taskDao.deleteTask(task);
  }

  Future<void> clearCompleted() async {
    await _taskDao.deleteCompletedTasks();
  }
}
```

---

## 八、常见问题

### 8.1 编译报错 "MissingDataException"

确保在 `@Database` 注解中正确注册所有实体：

```dart
@Database(version: 1, entities: [User, Post, Comment])
abstract class AppDatabase extends FloorDatabase {
  UserDao get userDao;
  PostDao get postDao;
  CommentDao get commentDao;
}
```

### 8.2 代码生成失败

```bash
# 清理缓存
dart run build_runner clean

# 重新生成
dart run build_runner build --delete-conflicting-outputs
```

### 8.3 类型转换错误

使用 `@TypeConverter` 自定义类型转换：

```dart
class DateTimeConverter extends TypeConverter<DateTime, int> {
  @override
  DateTime decode(int databaseValue) {
    return DateTime.fromMillisecondsSinceEpoch(databaseValue);
  }

  @override
  int encode(DateTime value) {
    return value.millisecondsSinceEpoch;
  }
}

// 在实体中使用
@Entity(tableName: 'tasks', typeConverters: [DateTimeConverter])
class Task { ... }
```

### 8.4 数据库文件路径问题

```dart
// 自定义数据库路径
Future<AppDatabase> getDatabase(String dbPath) async {
  return await $FloorAppDatabase
      .databaseBuilder(dbPath)  // 传入完整路径
      .build();
}
```

---

## 九、总结

floor 是 Flutter 中学习曲线最低的 SQLite ORM：

- ✅ **类似 Android Room**（Android 开发者友好）
- ✅ **注解驱动代码生成**
- ✅ **类型安全**
- ✅ **流式查询支持**
- ✅ **DAO 模式清晰**

如果你是 Android 开发者或熟悉 Room，floor 是入门最快的选择。

如果需要 Web 支持或更强大的功能，建议使用 drift。