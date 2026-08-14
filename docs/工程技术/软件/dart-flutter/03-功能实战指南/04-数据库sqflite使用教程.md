# 07-数据库 sqflite

> sqflite 是 Flutter 中操作 SQLite 的插件，API 简洁直观。
> 本章对比 Java JDBC 讲解，并结合 Vexfy 的 Song 存储实战。

---

## 1. sqflite 是什么？

| Java | Dart |
|---|---|
| `java.sql.DriverManager` | `sqflite` 插件 |
| `Connection` | `Database` 实例 |
| `PreparedStatement` | 字符串拼接（SQL 模板） |
| `ResultSet` | `List<Map<String, dynamic>>` |
| `JDBC` 驱动（MySQL/PostgreSQL/...） | `sqflite`（仅支持 SQLite） |

**sqflite 特点：**
- 纯 Dart 实现，无需原生桥接（跨平台一致性好）
- 适合本地持久化，不适合服务端
- 数据库存在应用私有目录，Android 不需要运行时权限
- 支持事务（`batch` / `transaction`）

---

## 2. 创建数据库和表

### 2.1 Vexfy 的 DatabaseHelper

Vexfy 使用单例模式的 `DatabaseHelper` 管理数据库连接：

```dart
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';        // 路径拼接工具
import 'package:path_provider/path_provider.dart';  // 获取应用文档目录

class DatabaseHelper {
  // 单例模式
  DatabaseHelper._();
  static final DatabaseHelper instance = DatabaseHelper._();

  Database? _database;

  /// 懒加载获取数据库实例
  Future<Database> get db async {
    _database ??= await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    // 获取应用文档目录（如 Android 的 /data/data/<package>/documents/）
    final documentsDir = await getApplicationDocumentsDirectory();

    // 拼接数据库文件路径
    final dbPath = join(documentsDir.path, 'vexfy.db');

    // 打开数据库（文件不存在则自动创建，并调用 onCreate）
    return await openDatabase(
      dbPath,
      version: 1,
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,  // 未来版本升级用
    );
  }
}
```

**Java 对比：**
```java
// JDBC 连接（每次操作都重新获取连接）
public class DatabaseHelper {
    private static DataSource dataSource;

    public static Connection getConnection() throws SQLException {
        // HikariCP 连接池
        return dataSource.getConnection();
    }

    // Spring Boot: JPA / MyBatis 更常用
    @Bean
    public DataSource dataSource() {
        return DataSourceBuilder.create()
            .url("jdbc:mysql://localhost:3306/vexfy")
            .build();
    }
}
```

### 2.2 创建表

```dart
Future<void> _onCreate(Database db, int version) async {
  // songs 表：本地音乐索引
  await db.execute('''
    CREATE TABLE ${Tables.songs} (
      id          TEXT PRIMARY KEY,         -- 歌曲 ID（文件路径 MD5）
      title       TEXT NOT NULL,            -- 歌名
      artist      TEXT NOT NULL DEFAULT '',  -- 歌手
      album       TEXT,                      -- 专辑
      duration    INTEGER NOT NULL DEFAULT 0, -- 时长（毫秒）
      cover_url   TEXT,                      -- 封面 URL
      source      TEXT NOT NULL DEFAULT 'local', -- 来源 local/online
      file_path   TEXT NOT NULL,             -- 本地文件路径
      online_url  TEXT,                      -- 在线 URL
      lyrics      TEXT,                      -- 歌词
      is_favorite INTEGER NOT NULL DEFAULT 0, -- 是否收藏
      play_count  INTEGER NOT NULL DEFAULT 0, -- 播放次数
      file_size   INTEGER,                   -- 文件大小
      mime_type   TEXT,                      -- MIME 类型
      created_at  TEXT NOT NULL             -- 创建时间（ISO8601）
    )
  ''');

  // songs 表索引（加速查询）
  await db.execute(
      'CREATE INDEX idx_songs_file_path ON ${Tables.songs}(file_path)');
  await db.execute(
      'CREATE INDEX idx_songs_title ON ${Tables.songs}(title)');
}
```

**Java 对比：** 用 MyBatis XML 或 JPA `@Entity` 注解定义表结构。

---

## 3. CRUD 操作

### 3.1 插入（Insert）

```dart
/// 插入歌曲（ConflictAlgorithm.replace = 插入或替换）
Future<void> insertSong(SongModel song) async {
  final db = await _dbHelper.db;
  await db.insert(
    Tables.songs,
    song.toMap(),  // SongModel.toMap() 返回 Map<String, dynamic>
    conflictAlgorithm: ConflictAlgorithm.replace,  // 主键冲突时替换
  );
}
```

**Java 对比：**
```java
// JPA
songRepository.save(song);  // 自动 INSERT 或 UPDATE

// MyBatis
@Insert("INSERT INTO songs (id, title, artist, ...) VALUES (#{id}, #{title}, #{artist}, ...)")
void insertSong(Song song);
```

### 3.2 查询（Select）

```dart
/// 查询所有歌曲
Future<List<SongModel>> getAllSongs() async {
  final db = await _dbHelper.db;
  final rows = await db.query(
    Tables.songs,
    orderBy: 'title ASC',  // 按歌名升序
  );
  // rows 是 List<Map<String, dynamic>>
  return rows.map((row) => SongModel.fromMap(row)).toList();
}

/// 根据 ID 查询单条
Future<SongModel?> getSongById(String id) async {
  final db = await _dbHelper.db;
  final rows = await db.query(
    Tables.songs,
    where: 'id = ?',          // 参数化查询（防 SQL 注入）
    whereArgs: [id],
    limit: 1,
  );
  if (rows.isEmpty) return null;
  return SongModel.fromMap(rows.first);
}

/// 搜索歌曲（LIKE 查询）
Future<List<SongModel>> searchSongs(String keyword) async {
  final db = await _dbHelper.db;
  final rows = await db.query(
    Tables.songs,
    where: 'title LIKE ? OR artist LIKE ?',  // 两个条件 OR
    whereArgs: ['%$keyword%', '%$keyword%'],  // % 是通配符
    orderBy: 'title ASC',
  );
  return rows.map((row) => SongModel.fromMap(row)).toList();
}
```

**Java 对比：**
```java
// JPA
List<Song> findAllByOrderByTitleAsc();
Optional<Song> findById(String id);
List<Song> findByTitleContainingOrArtistContaining(String title, String artist);

// MyBatis
@Select("SELECT * FROM songs WHERE title LIKE #{keyword} OR artist LIKE #{keyword}")
List<Song> searchSongs(@Param("keyword") String keyword);
```

### 3.3 更新（Update）

```dart
/// 更新歌曲（根据 ID）
Future<void> updateSong(SongModel song) async {
  final db = await _dbHelper.db;
  await db.update(
    Tables.songs,
    song.toMap(),
    where: 'id = ?',
    whereArgs: [song.id],
  );
}

/// 更新收藏状态
Future<void> toggleFavorite(String songId, bool isFavorite) async {
  final db = await _dbHelper.db;
  await db.update(
    Tables.songs,
    {'is_favorite': isFavorite ? 1 : 0},
    where: 'id = ?',
    whereArgs: [songId],
  );
}
```

**Java 对比：**
```java
// JPA
@Modifying
@Query("UPDATE Song s SET s.isFavorite = :isFavorite WHERE s.id = :id")
void toggleFavorite(@Param("id") String id, @Param("isFavorite") boolean isFavorite);

// MyBatis
@Update("UPDATE songs SET is_favorite = #{isFavorite} WHERE id = #{id}")
void toggleFavorite(Song song);
```

### 3.4 删除（Delete）

```dart
/// 删除歌曲
Future<void> deleteSong(String id) async {
  final db = await _dbHelper.db;
  await db.delete(
    Tables.songs,
    where: 'id = ?',
    whereArgs: [id],
  );
}
```

**Java 对比：**
```java
// JPA
void deleteById(String id);
// 或
@Delete("DELETE FROM songs WHERE id = #{id}")
void deleteSong(String id);
```

---

## 4. Vexfy 的 Song 存储

### 4.1 SongModel 与数据库映射

```dart
class SongModel {
  final String id;
  final String title;
  final String artist;
  final String? album;
  final int duration;
  final String? coverUrl;
  final SongSource source;
  final String? filePath;
  final String? onlineUrl;
  final String? lyrics;
  final bool isFavorite;
  final int playCount;
  final int? fileSize;
  final String? mimeType;
  final DateTime? createdAt;

  /// toMap：存入数据库
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'artist': artist,
      'album': album,
      'duration': duration,
      'cover_url': coverUrl,
      'source': source == SongSource.online ? 'online' : 'local',
      'file_path': filePath,
      'online_url': onlineUrl,
      'lyrics': lyrics,
      'is_favorite': isFavorite ? 1 : 0,
      'play_count': playCount,
      'file_size': fileSize,
      'mime_type': mimeType,
      'created_at': createdAt?.toIso8601String(),
    };
  }

  /// fromMap：从数据库读取
  factory SongModel.fromMap(Map<String, dynamic> map) {
    return SongModel(
      id: map['id'] as String,
      title: map['title'] as String,
      artist: map['artist'] as String? ?? '',
      album: map['album'] as String?,
      duration: map['duration'] as int? ?? 0,
      coverUrl: map['cover_url'] as String?,
      source: map['source'] == 'online' ? SongSource.online : SongSource.local,
      filePath: map['file_path'] as String?,
      ...
    );
  }
}
```

### 4.2 LocalMusicService 中的 CRUD

```dart
/// 扫描歌曲后，存入数据库（插入或替换）
Future<void> _upsertSong(SongModel song) async {
  final db = await _dbHelper.db;
  await db.insert(
    Tables.songs,
    song.toMap(),
    conflictAlgorithm: ConflictAlgorithm.replace,
  );
}

/// 加载所有歌曲（用于列表展示）
Future<List<SongModel>> loadAllSongs() async {
  final db = await _dbHelper.db;
  final rows = await db.query(
    Tables.songs,
    orderBy: 'title ASC',
  );
  return rows.map((row) => SongModel.fromMap(row)).toList();
}

/// 获取歌曲总数
Future<int> getSongCount() async {
  final db = await _dbHelper.db;
  final result = await db.rawQuery(
      'SELECT COUNT(*) as count FROM ${Tables.songs}');
  return Sqflite.firstIntValue(result) ?? 0;
}
```

---

## 5. 事务和批量操作

```dart
/// 批量插入（提升大量插入性能）
Future<void> batchInsert(List<SongModel> songs) async {
  final db = await _dbHelper.db;

  final batch = db.batch();  // 创建一个批量操作对象
  for (final song in songs) {
    batch.insert(Tables.songs, song.toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace);
  }

  // 一次性执行所有操作（减少数据库往返）
  await batch.commit(noResult: true);
}

/// 事务示例
Future<void> clearAndReload(List<SongModel> newSongs) async {
  final db = await _dbHelper.db;
  await db.transaction((txn) async {
    // 事务内所有操作在同一个数据库连接上执行
    await txn.delete(Tables.songs);  // 清空旧数据
    for (final song in newSongs) {
      await txn.insert(Tables.songs, song.toMap(),
          conflictAlgorithm: ConflictAlgorithm.replace);
    }
  });
}
```

**Java 对比：**
```java
// Spring 声明式事务
@Transactional
public void clearAndReload(List<Song> songs) {
    songRepository.deleteAll();
    songRepository.saveAll(songs);
}
```

---

## 6. 小结

| 操作 | sqflite | Java JDBC |
|---|---|---|
| 打开数据库 | `openDatabase(path)` | `DriverManager.getConnection(url)` |
| 插入 | `db.insert(table, map)` | `ps.executeUpdate()` |
| 查询 | `db.query(table)` → `List<Map>` | `rs = ps.executeQuery()` → `ResultSet` |
| 更新 | `db.update(table, map, where)` | `ps.executeUpdate()` |
| 删除 | `db.delete(table, where)` | `ps.executeUpdate()` |
| 批量 | `db.batch()` | `addBatch()` + `executeBatch()` |
| 事务 | `db.transaction()` | `@Transactional` |
| SQL 注入防护 | `where: 'id = ?', whereArgs: [id]` | `PreparedStatement` 参数绑定 |

---

## 下一步

→ [08-后台播放audio_service](./10-后台播放audio_service.md) — 了解 Flutter 后台播放和通知栏控制
