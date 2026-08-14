# GetX 依赖管理学习（初学通俗版）

> 核心目标：不用复杂概念，不用记什么"依赖注入""控制反转"，不用手动管理实例生命周期，解决原生手动new对象的麻烦，看完就会用`put`/`find`/`lazyPut`，听完就懂、上手就会。

---

## 一、先搞懂：原生实例管理有什么麻烦？

你之前写代码创建实例的原生写法是这样的：
```dart
// 每个页面用都要new一次，重复创建浪费内存
final DioUtil dioUtil = DioUtil();
final CounterController controller = CounterController();
```

**核心痛点（初学最直观的麻烦）：**
1. 跨页面用同一个实例要到处传参，或者要自己写单例模式，容易写错
2. 实例什么时候销毁完全不管，用多了内存泄漏，运行久了APP越来越卡
3. 有些不常用的页面的控制器，APP一启动就创建了，占内存，完全没必要
4. 退出登录要清空所有状态，要手动把所有实例重新new一遍，非常麻烦

---

## 二、GetX 依赖管理核心一句话

**不用手动new实例！不用自己写单例！不用管生命周期，`Get.put()`存、`Get.find()`拿，自动缓存、自动销毁，全局任何地方都能拿到，单例多例随便控制。**

**唯一前提**：已经把`MaterialApp`换成`GetMaterialApp`（路由/状态管理已经换过的话直接用，不用改）。

---

## 三、核心概念（大白话，不用记专业术语）
不用管什么"DI容器""IOC"这些虚的，就把GetX的依赖管理当成一个全局仓库：
1. **`put`**：把你创建的实例放到仓库里存起来，默认是单例，存一次就一直有
2. **`find`**：从仓库里把你之前存的实例拿出来用，任何页面、任何控制器里都能拿
3. **`delete`**：把仓库里的某个实例删掉，下次find就要重新put

GetX会自动帮你管这个仓库：页面销毁的时候自动删掉这个页面对应的控制器，不用你手动删，完全不会内存泄漏。

---

## 四、3个最常用方法（必背，对应所有场景）
99%的场景用这三个方法就够了，其他复杂API初学不用管。

### 1. Get.put(实例) —— 立即存，马上用（最常用）
- **场景**：全局要用的实例、当前页面马上要用的控制器，比如用户控制器、网络请求工具、当前页面的控制器
- **特点**：调用的时候立即创建实例，存到仓库里，默认是单例，put一次，任何地方find都是同一个实例
- **默认规则**：页面销毁的时候自动删掉这个实例，不会内存泄漏
- **示例代码：**
```dart
// 存：把CounterController放到仓库里
Get.put(CounterController());

// 取：任何地方只要写这一句就能拿到同一个实例
final CounterController controller = Get.find();
```

---

### 2. Get.lazyPut(() => 实例) —— 懒加载，用到的时候才创建（省内存）
- **场景**：不常用页面的控制器、不是启动就必须要用的工具类，比如设置页控制器、意见反馈页控制器，用户不进这个页面就不会创建，省内存
- **特点**：调用的时候不会立即创建实例，只有第一次调用`find`拿的时候才会创建，不调用就一直不占内存
- **示例代码：**
```dart
// 启动的时候先懒加载放着，不会创建实例
Get.lazyPut<SettingController>(() => SettingController());

// 用户第一次进设置页调用find的时候，才会真正创建SettingController实例
final SettingController controller = Get.find();
```

---

### 3. Get.delete<类型>() —— 手动删除实例（特殊场景用）
- **场景**：退出登录要清空所有状态、主动释放不需要的大内存实例，默认不用手动调用
- **特点**：把仓库里对应的实例删掉，下次find的时候会提示找不到，需要重新put
- **示例代码：**
```dart
// 退出登录的时候删掉用户控制器，下次登录重新创建全新的实例，状态完全清空
Get.delete<UserController>();
```

---

## 五、2个最常用参数（进阶小技巧）
### 参数1：`permanent: true` —— 永久保存，不会被自动销毁
- **场景**：全局要用的工具类，整个APP生命周期都要用到，比如网络请求Dio工具、本地存储SP工具、全局用户控制器
- **示例代码：**
```dart
// main.dart里启动的时候就put，加permanent: true，永远不会被自动删除，整个APP都能用
Get.put(DioUtil(), permanent: true);
Get.put(SpUtil(), permanent: true);
```

### 参数2：`tag: "自定义标签"` —— 同一个类存多个实例
- **场景**：同一个控制器类需要多个不同的实例，比如两个计数器页面，要用不同的CounterController实例
- **示例代码：**
```dart
// 存两个不同的CounterController，用tag区分
Get.put(CounterController(), tag: "counter1");
Get.put(CounterController(), tag: "counter2");

// 取的时候也要带对应的tag，拿到不同的实例
final controller1 = Get.find<CounterController>(tag: "counter1");
final controller2 = Get.find<CounterController>(tag: "counter2");
```

---

## 六、进阶用法：Binding（绑定）—— 跳转页面自动加载依赖（可选，非常省事）
不用手动在页面里写`Get.put()`，跳转到页面前自动把需要的控制器/工具类put好，离开页面自动delete，完全不用你管。

#### 3步直接套：
**步骤1：写Binding类**
```dart
// 首页的绑定类，存放首页需要的所有依赖
class HomeBinding extends Bindings {
  @override
  void dependencies() {
    // 跳转到首页前自动把HomeController lazyPut进去
    Get.lazyPut<HomeController>(() => HomeController());
    Get.lazyPut<PlayerController>(() => PlayerController());
  }
}
```

**步骤2：路由里配置Binding**
```dart
// 在你之前写的命名路由getPages里，给对应页面加binding参数
GetPage(
  name: '/home',
  page: () => HomePage(),
  binding: HomeBinding(), // 跳转到首页前自动执行HomeBinding的dependencies方法
)
```

**步骤3：页面里直接find用就行**
```dart
// 不用写Get.put，直接find就能拿到，跳转的时候已经自动put好了
final HomeController controller = Get.find();
```

**特点**：跳转到页面前自动加载依赖，离开页面自动删除依赖，完全不用手动写任何put/delete代码，太省事了！

---

## 七、原生 vs GetX 依赖管理对比
**原生写法（麻烦）**
```dart
// 自己写单例，容易写错，还要手动管生命周期
class DioUtil {
  static DioUtil? _instance;
  factory DioUtil() => _instance ??= DioUtil._internal();
  DioUtil._internal();
}

// 用的时候虽然是单例，但什么时候销毁完全不知道，容易内存泄漏
final dio = DioUtil();
```

**GetX写法（简单）**
```dart
// 一行搞定单例，自动管生命周期，不会内存泄漏
Get.put(DioUtil(), permanent: true);

// 任何地方直接拿，不用传参，不用手动管理
final dio = Get.find<DioUtil>();
```

---

## 八、和你之前的项目结合（直接套用）
结合你之前的Vexfy音乐播放器项目，直接套用：
1. **main.dart启动时全局永久put**：Dio网络请求工具、Sp本地存储工具、UserController用户控制器这些全APP都要用的，加`permanent: true`，永远不销毁
2. **页面级控制器用lazyPut+Binding**：首页控制器、播放页控制器、列表页控制器，每个页面对应写一个Binding，路由里配置，跳转自动加载，离开自动销毁，省内存
3. **退出登录时手动delete**：退出登录的时候调用`Get.delete<PlayerController>()`、`Get.delete<UserController>()`，所有状态清空，下次登录重新创建全新实例，不会有旧状态残留

---

## 补充说明（初学必看）
1. **默认单例**：默认put一次，find多少次都是同一个实例，不用自己写单例模式
2. **不用手动delete**：默认情况页面销毁时GetX会自动删除页面对应的控制器，99%的场景不用你手动调用delete
3. **找不到实例报错怎么办？** 肯定是你没先put就find，或者已经被delete了，先put再find就行
4. **不用记复杂API**：先练熟`put`、`find`、`lazyPut`三个方法，就能搞定99%的场景，Binding这些进阶功能慢慢学就行
5. **性能超好**：Get.find是O(1)时间复杂度，拿实例几乎不耗时，比原生传参快多了