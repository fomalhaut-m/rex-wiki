# Flutter 数据存储方案总览

> 本专题详细介绍 Flutter 中常用的数据存储方案，从入门到实战，帮你选择最适合的存储方案。

---

## 一、存储方案对比表

| 方案 | 类型 | 适用场景 | 复杂度 | 全平台支持 | 学习曲线 |
|---|---|---|---|---|---|
| **SharedPreferences** | 键值对 | 轻量配置、用户偏好设置 | ⭐ | ✅ Android/iOS/Windows/macOS/Linux/Web | 低 |
| **GetStorage** | 键值对 | 轻量数据、与GetX配合 | ⭐ | ✅ Android/iOS/Windows/macOS/Linux | 低 |
| **Hive** | NoSQL 文档数据库 | 轻量数据、离线缓存 | ⭐⭐ | ✅ Android/iOS/Windows/macOS/Linux/Web | 中 |
| **drift** | SQLite ORM | 复杂结构化数据、大型应用 | ⭐⭐⭐ | ✅ Android/iOS/Windows/macOS/Linux/Web | 中高 |
| **floor** | SQLite ORM | 复杂结构化数据（类似Android Room） | ⭐⭐⭐ | ✅ Android/iOS/Windows/macOS/Linux | 中高 |
| **sqflite** | 原生SQLite | 复杂查询、高性能要求 | ⭐⭐⭐ | ✅ Android/iOS/Windows/macOS/Linux | 高 |

---

## 二、各方案详细介绍

### 1. SharedPreferences

> Flutter 官方推荐的轻量级键值对存储。

**适用场景**：用户偏好设置、主题偏好、首次使用标识、简单开关状态。

**特点**：
- 无需初始化，直接使用
- 支持所有基础数据类型
- 同步读写，无异步回调
- 轻量级，性能优秀

**官网**：[shared_preferences - Flutter package](https://pub.dev/packages/shared_preferences)

---

### 2. GetStorage

> GetX 官方配套的轻量级键值对存储。

**适用场景**：轻量数据、与 GetX 项目无缝集成、快速原型开发。

**特点**：
- 与 GetX 生态完美结合
- 无需初始化（可异步初始化）
- 支持加密存储
- 同步 API，简单易用

**官网**：[get_storage - Pub](https://pub.dev/packages/get_storage)

---

### 3. Hive

> 高性能 NoSQL 键值对数据库，支持加密。

**适用场景**：离线缓存、复杂对象存储、需要加密的数据、离线优先应用。

**特点**：
- 高性能读写
- 支持 TypeAdapter 序列化
- 支持加密
- 可在 Web 使用
- 无需 SQL，学习成本低

**官网**：[hive - Pub](https://pub.dev/packages/hive) | [hive_flutter](https://pub.dev/packages/hive_flutter)

---

### 4. drift（原名 moor）

> 官方推荐的 SQLite ORM，功能最强大、最稳定。

**适用场景**：大型应用、结构化数据、复杂查询、多表关联、微信级别数据库。

**特点**：
- Flutter 官方推荐
- 全平台支持（包括 Web）
- 完整的类型安全查询 API
- 自动代码生成
- 支持迁移和版本管理
- 企业级项目首选

**官网**：[drift - Pub](https://pub.dev/packages/drift) | [官方文档](https://drift.simonbinder.eu/)

---

### 5. floor

> 类似 Android Room 的 SQLite ORM，易学易用。

**适用场景**：结构化数据、CRUD 操作、中小型应用、熟悉 Room 的 Android 开发者。

**特点**：
- API 设计类似 Android Room
- 注解驱动代码生成
- 支持依赖注入
- 简洁的 DAO 模式
- 稳定可靠

**官网**：[floor - Pub](https://pub.dev/packages/floor) | [GitHub](https://github.com/puszekajnik/floor)

---

### 6. sqflite

> 原生 SQLite 插件，直接执行 SQL 语句。

**适用场景**：高性能要求、复杂 SQL 查询、遗留系统迁移、需要完全控制 SQL。

**特点**：
- 完全控制 SQL 语句
- 最高性能
- 最灵活
- 学习成本高
- 需要手动管理迁移

**官网**：[sqflite - Pub](https://pub.dev/packages/sqflite) | [sqflite_common_ffi (桌面)](https://pub.dev/packages/sqflite_common_ffi)

---

## 三、选择建议

### 根据数据复杂度选择

```
简单配置/偏好设置
    ↓
SharedPreferences / GetStorage
    ↓
中等复杂度（对象、列表）
    ↓
Hive / GetStorage + 模型
    ↓
复杂结构化数据
    ↓
drift / floor / sqflite
```

### 根据项目规模选择

| 项目规模 | 推荐方案 | 原因 |
|---|---|---|
| 小型/原型 | GetStorage / Hive | 快速开发、轻量 |
| 中型 | Hive / drift | 功能丰富、性能好 |
| 大型/企业 | drift | 官方推荐、最稳定 |
| 微信级别 | drift | 完整 ORM、迁移支持 |

### 根据团队背景选择

- **熟悉 Android Room** → floor（上手最快）
- **熟悉 SQL** → sqflite（最灵活）
- **追求官方推荐** → drift（Flutter 官方）
- **快速原型** → GetStorage（最简单）

---

## 四、专题目录

本专题包含以下独立教程：

- [01-SharedPreferences使用教程](./01-SharedPreferences使用教程.md) — 官方轻量键值对存储
- [02-GetStorage使用教程](./02-GetStorage使用教程.md) — GetX官方配套存储
- [03-Hive使用教程](./03-Hive使用教程.md) — 高性能NoSQL数据库
- [04-drift使用教程](./04-drift使用教程.md) — 官方推荐的SQLite ORM
- [05-floor使用教程](./05-floor使用教程.md) — 类似Room的SQLite ORM
- [06-sqflite使用教程](./06-sqflite使用教程.md) — 原生SQLite直接操作

---

## 五、相关链接

### 官方文档
- [Flutter 数据存储官方文档](https://docs.flutter.dev/data-and-backend/storage)
- [Pub.dev 存储相关包](https://pub.dev/packages?q=storage)

### 社区资源
- [Flutter 存储方案对比文章](https://medium.com/flutter-community/comparing-flutter-persistence-options-db951170362f)
- [drift 官方示例项目](https://github.com/simonb97/drift-examples)

### 视频教程
- [Flutter 官方 Storage Codelab](https://codelabs.developers.google.com/codelabs/flutter-boring-show)

---

> 💡 **提示**：如果你是初学者，建议从 GetStorage 或 SharedPreferences 开始；如果是正式项目，建议直接学习 drift。