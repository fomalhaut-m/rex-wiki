# 01-Dart 语法速通

> 基于 Vexfy 项目实战学习，适合有 Java 基础的程序员 30 分钟上手 Dart

---

## 1. Hello World

```dart
// Java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}

// Dart（更简洁）
void main() {
    print('Hello');
}
```

---

## 2. 变量和类型

```dart
// Dart 的 var 自动推断类型，等同于 Java 的 var
var name = "Luke";        // 自动推断 String
String name2 = "Luke";    // 显式类型也可以
int age = 34;
final double height = 183.0;  // final = Java 的 final
const PI = 3.14;              // const = 编译时常量，Java 没有
```

---

## 3. 空安全（Null Safety）

```java
// Java：烦人的 NPE
String name = null;
name.length();  // NullPointerException!

// Dart：空安全，默认不可为 null，编译时就报错
String name = "Luke";
// name = null;  // ❌ 编译错误！

// 真的需要 null，加 ?
String? nullableName = null;  // 加 ? 表示可以为 null
nullableName?.length;          // 安全调用，null 就返回 null
```

**Dart 从语言层面解决了 NPE，Java 14+ 的 Optional ，Dart 直接内置了。**

---

## 4. 函数

```dart
// 单行箭头函数，等同于 Java 的 -> 表达式 lambda
int add(int a, int b) => a + b;

// 完整写法
int add(int a, int b) {
    return a + b;
}

// 可选命名参数（Java 没有这个）
void greet(String name, {String? title}) {
    print('$title $name');
}
greet('Luke');                  // title 为 null，不打印
greet('Luke', title: 'Mr.');    // Mr. Luke
```

---

## 5. 类和对象

```java
// Java：需要手写 getter/setter
public class Song {
    private String title;
    public Song(String title) { this.title = title; }
    public String getTitle() { return title; }
}

// Dart：自动生成 getter/setter，直接访问属性
class Song {
    String title;       // 不用写 getter/setter
    String artist;
    
    Song(this.title, this.artist);  // 构造器简写
}

var song = Song('晴天', '周杰伦');
print(song.title);  // 直接访问，不用 getter
song.title = '七里香';  // 直接赋值，不用 setter
```

---

## 6. 继承

```java
// Java
public class PlayerController extends BaseController {
    @Override
    public void play() {
        super.play();
    }
}

// Dart（语法几乎一样）
class PlayerController extends BaseController {
    @override  // Dart 用 @override 注解
    void play() {
        super.play();
    }
}
```

---

## 7. 接口和抽象

```java
// Java
public interface PlayerService {
    void play();
    void pause();
}

// Dart（Dart 没有 interface 关键字，class 就是接口）
abstract class PlayerService {
    void play();  // 抽象方法
    void pause();
}

class PlayerImpl implements PlayerService {
    @override
    void play() { }
    @override
    void pause() { }
}
```

---

## 8. 集合（List / Map / Set）

```java
// Java
List<String> list = Arrays.asList("a", "b", "c");
Map<String, Integer> map = new HashMap<>();
map.put("key", 1);

// Dart（更简洁直观）
var list = ['a', 'b', 'c'];   // List 字面量
var map = {'key': 1};           // Map 字面量
map['key'] = 1;               // 直接访问

// 遍历
for (var item in list) {
    print(item);
}

// 函数式（类似 Java Stream）
var doubled = list.map((e) => e * 2).toList();
```

---

## 9. 异步（Future + async / await）

```java
// Java CompletableFuture
CompletableFuture<String> fetchData() {
    return CompletableFuture.supplyAsync(() -> "result");
}

// Dart（和 JavaScript 几乎一样，比 Java 简洁）
Future<String> fetchData() async {
    await Future.delayed(Duration(seconds: 1));
    return 'result';
}

// 调用
void main() async {
    var data = await fetchData();
    print(data);
}
```

---

## 10. 完整可运行示例代码

下面是包含上述所有特性的完整Dart代码示例，可以直接运行学习：

```dart
// Dart（最简形式）
// main函数添加async修饰，才能在内部使用await
void main() async {
  print('=' * 60);
  print('🚀 Dart基础语法示例运行开始');
  print('=' * 60);

  printHello();
  useVar();
  useNullSafety();
  useFunction();
  useClass();
  useInherit();
  useInterface();
  useCollection();
  await useAsync(); // await等待异步函数执行完成


  print('\n' + '=' * 60);
  print('✅ Dart基础语法示例运行结束');
  print('=' * 60);
}

//1. Hello World
void printHello() {
  print('\n📌 [1/9] Hello World 示例:');
  print('   输出内容: Hello');
}

//2. 变量和类型
void useVar() {
  print('\n📌 [2/9] 变量和类型 示例:');
  // Dart（很像，但有var和final）
  var name = "Luke"; // 自动推断 String
  print('   var自动推断类型 name：$name (类型: ${name.runtimeType})');
  String name2 = "Luke"; // 显式类型也可以
  print('   显式声明String类型 name2：$name2 (类型: ${name2.runtimeType})');
  int age = 34;
  print('   显式声明int类型 age：$age (类型: ${age.runtimeType})');
  final double height = 183.0; // Java的final，Dart也用final、
  print('   final修饰不可变变量 height：$height (类型: ${height.runtimeType})');
  const PI = 3.14; // 编译时常量，Java没有这个、
  print('   const编译时常量 PI：$PI (类型: ${PI.runtimeType})');
}

//3. 空安全（Null Safety）
void useNullSafety() {
  print('\n📌 [3/9] 空安全（Null Safety） 示例:');
  // Java（烦人的NPE）
  //String name = null; // 编译不报错，但运行时可能炸
  // name.length(); // NullPointerException!

  // Dart（空安全，默认不可为null）
  String name = "Luke";
  print('   默认不可为null变量 name = "$name"，不可赋值为null');
  // name = null;  // ❌ 编译错误！安全

  // 如果真的需要null，加 ?
  String? nullableName = null; // 加?表示可以为null
  print('   可为null变量 nullableName = $nullableName');
  int? length = nullableName?.length; // 安全调用，null就返回null
  print('   安全调用nullableName?.length结果: $length');
}

//4. 函数
void useFunction() {
  print('\n📌 [4/9] 函数 示例:');
  // 函数（lambda）
  int add(int a, int b) => a + b;
  print('   Lambda函数 add(1, 2) = ${add(1, 2)}');

  // 函数（普通）
  int sub(int a, int b) {
    return a - b;
  }

  print('   普通函数 sub(1, 2) = ${sub(1, 2)}');

  // 可选参数
  int greet(String name, {int age = 0}) {
    return name.length + age;
  }

  print('   可选参数函数 greet("Luke") = ${greet("Luke")} (age默认值0)');
  print(
    '   可选参数函数 greet("Luke", age: 34) = ${greet("Luke", age: 34)} (age传值34)',
  );
}

//5. 类和对象
void useClass() {
  print('\n📌 [5/9] 类和对象 示例:');
  // Dart创建对象（不用new）
  var song = Song('晴天', '周杰伦');
  print('   Song实例 title: ${song.title} (类型: ${song.title.runtimeType})'); // 直接访问，不用getter/setter
  print('   Song实例 artist: ${song.artist} (类型: ${song.artist.runtimeType})');
}

// Dart（更简洁）
class Song {
  String title; // 不用写getter/setter，Flutter直接song.title访问
  String artist;
  Song(this.title, this.artist); // 构造器简写
}

//6. 继承
void useInherit() {
  print('\n📌 [6/9] 继承 示例:');
  // Dart创建对象（不用new）
  BaseController player = PlayerController();
  print('   父类引用指向子类实例 player.play() 输出:');
  player.play();

  PlayerController player2 = PlayerController();
  print('   子类实例 player2.play() 输出:');
  player2.play();
}

// Dart（更简洁）
class BaseController {
  void play() {
    print('     父类BaseController.play() 执行');
  }
}

class PlayerController extends BaseController {
  @override // Dart用@override注解，不是@Override
  void play() {
    print('     子类PlayerController.play() 调用super.play()前');
    super.play();
    print('     子类PlayerController.play() 调用super.play()后');
  }
}

//7. 接口和抽象类
void useInterface() {
  print('\n📌 [7/9] 接口和抽象类 示例:');
  // Dart创建对象（不用new）
  PlayerService player = PlayerImpl();
  print('   接口实现类实例 player.play() 输出:');
  player.play();
  print('   接口实现类实例 player.pause() 输出:');
  player.pause();
}

// Dart（Dart没有interface关键字，class就是接口）
// 用abstract class定义抽象类
abstract class PlayerService {
  void play(); // 抽象方法，不用abstract也行
  void pause();
}

class PlayerImpl implements PlayerService {
  @override
  void play() {
    print('     PlayerImpl.play() 执行: 播放');
  }

  @override
  void pause() {
    print('     PlayerImpl.pause() 执行: 暂停');
  }
}

//8. 集合（List/Map/Set）
void useCollection() {
  print('\n📌 [8/9] 集合（List/Map/Set） 示例:');
  // Java
  // List<String> list = Arrays.asList("a", "b", "c");
  // Map<String, int> map = new HashMap<>();
  // map.put("key", 1);
  // for (String item : list) { }

  // Dart（更简洁）
  var list = ['a', 'b', 'c']; // List字面量
  var map = {'key': 1}; // Map字面量
  map['key'] = 1; // 直接访问

  print('   List字面量 list: $list (类型: ${list.runtimeType})');
  print('   for-in遍历list结果:');
  // 遍历
  for (var item in list) {
    print('     $item');
  }

  print('   forEach遍历list结果:');
  // 函数式
  list.forEach((item) => print('     $item'));
  var doubled = list.map((e) => e * 2).toList();
  print('   函数式操作 list.map((e) => e * 2).toList() 结果: $doubled');
  print('   Map字面量 map: $map (类型: ${map.runtimeType})');
  print('   Map直接访问 map["key"] 结果: ${map['key']}');
}

//9. 异步（Future + async/await）
// 异步函数需要返回Future，返回值类型为Future<void>表示没有返回值
Future<void> useAsync() async {
  print('\n📌 [9/9] 异步（Future + async/await） 示例:');
  // Dart（和JavaScript很像）
  Future<String> fetchData(int requestId) async {
    await Future.delayed(Duration(seconds: 1));
    return '请求#$requestId 数据结果';
  }
  
  print('   开始调用异步函数fetchData(1)，等待1秒...');
  var result = await fetchData(1);
  print('   异步函数返回结果: $result');
}
```

---

## 11. Dart 独有的好东西

### 11.1 级联操作符（..）

```java
// Java 多行
song.setTitle('新歌');
song.setArtist('新歌手');
song.save();

// Dart 一行搞定，用 ..
song
    ..title = '新歌'
    ..artist = '新歌手'
    ..save();
```

### 10.2 字符串插值

```dart
var name = 'Luke';
print('Hello $name');        // Hello Luke
print('Age: ${age + 1}');   // Age: 35，支持表达式
```

### 10.3 ?? 操作符（null 合并）

```dart
var name = nullableName ?? '默认值';
// nullableName 为 null 时用默认值，等同于 Java 的 Optional.orElse()
```

### 10.4 命名构造器

```dart
class Song {
    String title;
    
    // 命名构造器 fromJson
    Song.fromJson(Map json) {
        title = json['title'];
    }
}

var song = Song.fromJson({'title': '晴天'});
```

---

## 11. 关键速查表

| Dart | Java | 说明 |
|------|------|------|
| `var` | `var` | 自动类型推断 |
| `final` | `final` | 运行时常量 |
| `const` | `static final` | 编译时常量 |
| `String?` | `Optional<String>` | 可空类型 |
| `class A extends B` | `class A extends B` | 继承 |
| `class A implements B` | `class A implements B` | 实现 |
| `=>` | `->` | 箭头函数 |
| `$name` | `%s + name` | 字符串插值 |
| `..` 级联调用 | obj.method1().method2() | 级联操作符 |
| `async / await` | `CompletableFuture` | 异步 |
| `{String? title}` | 无 | 命名可选参数 |

---

## 12. 结合 Vexfy 项目看真实代码

### 12.1 Song 模型（Dart 类）

```dart
// 文件：app/lib/data/models/song_model.dart
class Song {
    String id;         // 歌曲唯一ID（MD5）
    String title;      // 歌名
    String artist;     // 歌手
    String album;       // 专辑
    String path;        // 文件路径
    int duration;       // 时长（毫秒）

    Song({
        required this.id,
        required this.title,
        required this.artist,
        required this.album,
        required this.path,
        required this.duration,
    });

    // 命名构造器：从数据库 Map 构建
    Song.fromMap(Map<String, dynamic> map)
        : id = map['id'],
          title = map['title'],
          artist = map['artist'],
          album = map['album'],
          path = map['path'],
          duration = map['duration'];

    // 转为 Map：存入数据库
    Map<String, dynamic> toMap() => {
        'id': id,
        'title': title,
        'artist': artist,
        'album': album,
        'path': path,
        'duration': duration,
    };
}
```

**对比 Java：** 不需要手写 getter/setter，Dart 自动生成。

### 12.2 GetX Controller（Dart 类 + 状态管理）

```dart
// 文件：app/lib/services/player_service.dart
class PlayerService extends GetxController {
    // RxInt = GetX 的响应式变量，类似 Java 的 AtomicInteger
    final currentIndex = 0.obs;
    final isPlaying = false.obs;
    final playlist = <Song>[].obs;

    // 播放
    void play() {
        isPlaying.value = true;
    }

    // 暂停
    void pause() {
        isPlaying.value = false;
    }

    // 切下一首
    void next() {
        if (currentIndex.value < playlist.length - 1) {
            currentIndex.value++;
        }
    }
}
```

**对比 Java：** `.obs` 让变量变成响应式的，值变化时 UI 自动更新（类似 Spring 的事件监听，但更简洁）。

---

## 下一步

- [02-Flutter项目结构](./02-Flutter项目结构.md) — 跑起第一个页面
