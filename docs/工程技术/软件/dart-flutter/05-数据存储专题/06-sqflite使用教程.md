# sqflite 数据库使用教程

> sqflite 是 Flutter 原生 SQLite 插件，提供直接的 SQL 操作能力，适合需要完全控制 SQL 的场景。

---

## 一、简介

### 1.1 什么是 sqflite？

sqflite 是 Flutter 官方 SQLite 插件：
- **原生 SQL**：完全控制 SQL 语句
- **最高性能**：无额外抽象层
- **跨平台**：Android/iOS/Windows/macOS/Linux
- **事务支持**：支持复杂事务操作
- **批量操作**：高效批量插入/更新

### 1.2 适用场景

- 需要完全控制 SQL 语句
- 复杂查询（联表、子查询）
- 高性能要求
- 遗留系统迁移
- 熟悉 SQL 的开发者

### 1.3 官方资源

| 资源 | 链接 |
|---|---|
| Pub 页面 | https://pub.dev/packages/sqflite |
| 官方文档 | https://github.com/tekartik/sqflite |
| 桌面支持 | https://pub.dev/packages/sqflite_common_ffi |
| sqflite_common_ffi | https://pub.dev/packages/sqflite_common_ffi |

---

## 二、安装配置

### 2.1 添加依赖

```yaml
# pubspec.yaml
dependencies:
  sqflite: ^2.3.0
  path: ^1.8.3
  path_provider: ^2.1.1

# 如果需要桌面平台支持
dependencies:
  sqflite: ^2.3.0
  sqflite_common_ffi: ^2.3.0
  path: ^1.8.3
  path_provider: ^2.1.1
```

### 2.2 安装命令

```bash
flutter pub get
```

---

## 三、基础用法

### 3.1 初始化数据库

```dart
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'my_database.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
    );
  }

  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER
      )
    ''');
  }
}
```

### 3.2 插入数据（INSERT）

```dart
Future<int> insertUser(String name, String email, int? age) async {
  final db = await database;
  return await db.insert(
    'users',
    {
      'name': name,
      'email': email,
      'age': age,
    },
  );
}

// 插入并返回新记录 ID
final id = await db.insert('users', {
  'name': 'Luke',
  'email': 'luke@example.com',
  'age': 25,
});
```

### 3.3 查询数据（SELECT）

```dart
// 查询所有
Future<List<Map<String, dynamic>>> getAllUsers() async {
  final db = await database;
  return await db.query('users');
}

// 条件查询
Future<List<Map<String, dynamic>>> getUserById(int id) async {
  final db = await database;
  return await db.query(
    'users',
    where: 'id = ?',
    whereArgs: [id],
  );
}

// 模糊查询
Future<List<Map<String, dynamic>>> searchUsers(String keyword) async {
  final db = await database;
  return await db.query(
    'users',
    where: 'name LIKE ?',
    whereArgs: ['%$keyword%'],
  );
}

// 多条件查询
Future<List<Map<String, dynamic>>> getAdultUsers() async {
  final db = await database;
  return await db.query(
    'users',
    where: 'age >= ?',
    whereArgs: [18],
    orderBy: 'created_at DESC',
  );
}

// 原生 SQL 查询
Future<List<Map<String, dynamic>>> complexQuery() async {
  final db = await database;
  return await db.rawQuery('''
    SELECT u.*, COUNT(p.id) as post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
    WHERE u.age > ?
    GROUP BY u.id
    HAVING post_count > 0
    ORDER BY post_count DESC
  ''', [18]);
}
```

### 3.4 更新数据（UPDATE）

```dart
Future<int> updateUser(int id, String name, String email) async {
  final db = await database;
  return await db.update(
    'users',
    {'name': name, 'email': email},
    where: 'id = ?',
    whereArgs: [id],
  );
}

// 返回更新的行数
final rowsAffected = await db.update(
  'users',
  {'age': 30},
  where: 'id = ?',
  whereArgs: [id],
);
```

### 3.5 删除数据（DELETE）

```dart
Future<int> deleteUser(int id) async {
  final db = await database;
  return await db.delete(
    'users',
    where: 'id = ?',
    whereArgs: [id],
  );
}

// 删除多条
Future<int> deleteUsersByAge(int maxAge) async {
  final db = await database;
  return await db.delete(
    'users',
    where: 'age < ?',
    whereArgs: [maxAge],
  );
}
```

---

## 四、进阶用法

### 4.1 批量插入

```dart
Future<void> batchInsert() async {
  final db = await database;
  final batch = db.batch();

  for (var i = 0; i < 1000; i++) {
    batch.insert('users', {
      'name': 'User $i',
      'email': 'user$i@example.com',
      'age': 20 + (i % 50),
    });
  }

  await batch.commit(noResult: true);
}

// 或使用事务
Future<void> transactionInsert() async {
  final db = await database;
  await db.transaction((txn) async {
    for (var i = 0; i < 100; i++) {
      await txn.insert('users', {
        'name': 'User $i',
        'email': 'user$i@example.com',
        'age': 25,
      });
    }
  });
}
```

### 4.2 分页查询

```dart
Future<List<Map<String, dynamic>>> getUsersPaginated(int page, int pageSize) async {
  final db = await database;
  final offset = page * pageSize;
  return await db.query(
    'users',
    limit: pageSize,
    offset: offset,
    orderBy: 'created_at DESC',
  );
}

// 使用原生 SQL
Future<List<Map<String, dynamic>>> paginatedQuery() async {
  final db = await database;
  return await db.rawQuery(
    'SELECT * FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?',
    [pageSize, offset],
  );
}
```

### 4.3 聚合查询

```dart
// 统计数量
Future<int> getUserCount() async {
  final db = await database;
  final result = await db.rawQuery('SELECT COUNT(*) as count FROM users');
  return Sqflite.firstIntValue(result) ?? 0;
}

// 计算平均值
Future<double?> getAverageAge() async {
  final db = await database;
  final result = await db.rawQuery('SELECT AVG(age) as avg FROM users');
  return result.first['avg'] as double?;
}

// 分组统计
Future<List<Map<String, dynamic>>> getAgeDistribution() async {
  final db = await database;
  return await db.rawQuery('''
    SELECT age_group, COUNT(*) as count FROM (
      SELECT
        CASE
          WHEN age < 18 THEN '未成年'
          WHEN age < 30 THEN '青年'
          WHEN age < 50 THEN '中年'
          ELSE '老年'
        END as age_group
      FROM users
      WHERE age IS NOT NULL
    )
    GROUP BY age_group
  ''');
}
```

### 4.4 事务处理

```dart
Future<void> transferMoney(int fromId, int toId, double amount) async {
  final db = await database;
  await db.transaction((txn) async {
    // 扣除转出账户
    await txn.rawUpdate(
      'UPDATE accounts SET balance = balance - ? WHERE id = ?',
      [amount, fromId],
    );

    // 增加转入账户
    await txn.rawUpdate(
      'UPDATE accounts SET balance = balance + ? WHERE id = ?',
      [amount, toId],
    );

    // 记录交易
    await txn.insert('transactions', {
      'from_id': fromId,
      'to_id': toId,
      'amount': amount,
      'created_at': DateTime.now().toIso8601String(),
    });
  });
}
```

---

## 五、数据库迁移

### 5.1 版本升级

```dart
Future<Database> _initDatabase() async {
  String path = join(await getDatabasesPath(), 'my_database.db');
  return await openDatabase(
    path,
    version: 2,
    onCreate: _onCreate,
    onUpgrade: _onUpgrade,
  );
}

Future<void> _onUpgrade(Database db, int oldVersion, int newVersion) async {
  if (oldVersion < 2) {
    // v1 -> v2: 添加新表
    await db.execute('''
      CREATE TABLE posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
      )
    ''');
  }

  if (oldVersion < 3) {
    // v2 -> v3: 添加新列
    await db.execute('ALTER TABLE users ADD COLUMN phone TEXT');
  }
}
```

### 5.2 数据迁移

```dart
Future<void> migrateV1ToV2(Database db) async {
  // 1. 创建临时表
  await db.execute('''
    CREATE TABLE users_temp (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT UNIQUE,
      age INTEGER,
      phone TEXT,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
  ''');

  // 2. 迁移数据
  await db.rawInsert('''
    INSERT INTO users_temp (name, email, age, phone, created_at)
    SELECT name, email, age, NULL, datetime('now') FROM users
  ''');

  // 3. 删除旧表
  await db.execute('DROP TABLE users');

  // 4. 重命名新表
  await db.execute('ALTER TABLE users_temp RENAME TO users');
}
```

---

## 六、结合 GetX 使用

### 6.1 创建 Service

```dart
// lib/services/database_service.dart
import 'package:get/get.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseService extends GetxService {
  late final Database _db;

  Database get db => _db;

  Future<DatabaseService> init() async {
    final dbPath = join(await getDatabasesPath(), 'app.db');
    _db = await openDatabase(
      dbPath,
      version: 1,
      onCreate: _onCreate,
    );
    return this;
  }

  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT,
        album TEXT,
        duration INTEGER,
        path TEXT UNIQUE,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
      )
    ''');
  }

  @override
  void onClose() {
    _db.close();
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
// lib/controllers/song_controller.dart
import 'package:get/get.dart';
import '../services/database_service.dart';

class SongController extends GetxController {
  final DatabaseService _db = Get.find();

  final RxList<Map<String, dynamic>> songs = <Map<String, dynamic>>[].obs;
  final RxBool isLoading = false.obs;

  @override
  void onInit() {
    super.onInit();
    loadSongs();
  }

  Future<void> loadSongs() async {
    isLoading.value = true;
    try {
      final result = await _db.db.query('songs', orderBy: 'created_at DESC');
      songs.value = result;
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> addSong(String title, String artist, String path, int duration) async {
    await _db.db.insert('songs', {
      'title': title,
      'artist': artist,
      'path': path,
      'duration': duration,
    });
    await loadSongs();
  }

  Future<void> deleteSong(int id) async {
    await _db.db.delete('songs', where: 'id = ?', whereArgs: [id]);
    await loadSongs();
  }

  Future<List<Map<String, dynamic>>> searchSongs(String keyword) async {
    return await _db.db.query(
      'songs',
      where: 'title LIKE ? OR artist LIKE ?',
      whereArgs: ['%$keyword%', '%$keyword%'],
    );
  }
}
```

### 6.4 页面使用

```dart
class SongListPage extends StatelessWidget {
  final SongController ctrl = Get.put(SongController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('本地音乐')),
      body: Obx(() {
        if (ctrl.isLoading.value) {
          return Center(child: CircularProgressIndicator());
        }
        if (ctrl.songs.isEmpty) {
          return Center(child: Text('暂无音乐'));
        }
        return ListView.builder(
          itemCount: ctrl.songs.length,
          itemBuilder: (context, index) {
            final song = ctrl.songs[index];
            return ListTile(
              title: Text(song['title'] ?? '未知'),
              subtitle: Text(song['artist'] ?? '未知艺术家'),
              trailing: IconButton(
                icon: Icon(Icons.delete),
                onPressed: () => ctrl.deleteSong(song['id']),
              ),
            );
          },
        );
      }),
    );
  }
}
```

---

## 七、实战示例：聊天消息存储

```dart
class ChatDatabase {
  late Database _db;

  Future<void> init() async {
    _db = await openDatabase(
      join(await getDatabasesPath(), 'chat.db'),
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            last_message TEXT,
            last_time TEXT,
            unread_count INTEGER DEFAULT 0
          )
        ''');

        await db.execute('''
          CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            type TEXT DEFAULT 'text',
            is_read INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
          )
        ''');

        // 创建索引
        await db.execute('CREATE INDEX idx_messages_conv ON messages(conversation_id)');
        await db.execute('CREATE INDEX idx_messages_time ON messages(created_at)');
      },
    );
  }

  // 获取会话列表
  Future<List<Map<String, dynamic>>> getConversations() async {
    return await _db.query(
      'conversations',
      orderBy: 'last_time DESC',
    );
  }

  // 获取会话消息（分页）
  Future<List<Map<String, dynamic>>> getMessages(int convId, {int limit = 20, int offset = 0}) async {
    return await _db.query(
      'messages',
      where: 'conversation_id = ?',
      whereArgs: [convId],
      orderBy: 'created_at DESC',
      limit: limit,
      offset: offset,
    );
  }

  // 发送消息
  Future<int> sendMessage(int convId, int senderId, String content, {String type = 'text'}) async {
    final id = await _db.insert('messages', {
      'conversation_id': convId,
      'sender_id': senderId,
      'content': content,
      'type': type,
    });

    // 更新会话最后消息
    await _db.update(
      'conversations',
      {
        'last_message': content,
        'last_time': DateTime.now().toIso8601String(),
      },
      where: 'id = ?',
      whereArgs: [convId],
    );

    return id;
  }

  // 标记消息已读
  Future<void> markAsRead(int convId, int myId) async {
    await _db.update(
      'messages',
      {'is_read': 1},
      where: 'conversation_id = ? AND sender_id != ? AND is_read = 0',
      whereArgs: [convId, myId],
    );

    await _db.update(
      'conversations',
      {'unread_count': 0},
      where: 'id = ?',
      whereArgs: [convId],
    );
  }

  // 获取未读数
  Future<int> getUnreadCount(int convId, int myId) async {
    final result = await _db.rawQuery(
      'SELECT COUNT(*) as count FROM messages WHERE conversation_id = ? AND sender_id != ? AND is_read = 0',
      [convId, myId],
    );
    return Sqflite.firstIntValue(result) ?? 0;
  }
}
```

---

## 八、常见问题

### 8.1 数据库路径问题

```dart
// 获取正确路径
final dbPath = await getDatabasesPath();
print('数据库路径: $dbPath');

// 自定义路径
final customPath = '/data/user/0/com.example.app/databases/my.db';
```

### 8.2 并发写入冲突

```dart
// 使用事务避免冲突
await db.transaction((txn) async {
  await txn.insert('table1', data1);
  await txn.insert('table2', data2);
});
```

### 8.3 大数据量性能

```dart
// 添加索引
await db.execute('CREATE INDEX idx_column ON table(column)');

// 使用 LIMIT 限制返回
await db.query('table', limit: 100);

// 使用分页加载
await db.query('table', limit: 20, offset: page * 20);
```

### 8.4 桌面平台支持

```dart
// 在桌面平台使用 sqflite_common_ffi
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

void main() {
  // 初始化 FFI
  sqfliteFfiInit();
  databaseFactory = databaseFactoryFfi;

  runApp(MyApp());
}
```

---

## 九、与其他方案对比

| 特性 | sqflite | drift | floor |
|---|---|---|---|
| SQL 控制 | ✅ 完全 | ⚠️ 受限 | ⚠️ 受限 |
| 类型安全 | ❌ | ✅ | ✅ |
| 代码生成 | ❌ | ✅ | ✅ |
| 学习曲线 | 高 | 中高 | 中 |
| 性能 | ✅ 最高 | ✅ 高 | ✅ 高 |
| Web 支持 | ❌ | ✅ | ❌ |

---

## 十、总结

sqflite 特点：

- ✅ **最高性能**：无额外抽象层
- ✅ **完全控制**：SQL 语句完全可控
- ✅ **事务支持**：复杂事务操作
- ✅ **跨平台**：全平台支持

适用场景：
- 需要复杂 SQL 查询
- 高性能要求
- 遗留系统迁移
- 熟悉 SQL 的开发者

不适用场景：
- 需要类型安全（建议 drift/floor）
- Web 端应用（建议 drift）
- 快速开发（建议 GetStorage/Hive）

sqflite 是 Flutter 中最灵活的 SQLite 方案，适合需要完全控制数据库的场景。