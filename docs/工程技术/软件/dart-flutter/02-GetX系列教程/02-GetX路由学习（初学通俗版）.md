# GetX 路由学习文档（初学通俗版）

> 核心目标：不用复杂操作，快速掌握 GetX 路由用法，解决原生路由的麻烦，结合之前学的 Flutter 基础（欢迎页、Tab 页面），听完就懂、上手就会。

---

## 一、先搞懂：原生路由有什么麻烦？

你之前练习的原生 Flutter 页面跳转，写法是这样的：
```dart
Navigator.push(
  context, 
  MaterialPageRoute(builder: (context) => TestPage()),
);
```

**核心痛点（初学最直观的麻烦）：**
1. 必须传 `context` （上下文），少了就报错
2. 控制器（后面会学的业务逻辑类）里拿不到 `context` ，没法跳转页面
3. 代码太长，写起来麻烦，容易记混

---

## 二、GetX 路由核心一句话

**不用 context！直接用 Get.xxx() 跳转，控制器里也能随便跳！**

**唯一前提（必须做，否则用不了）：**
把 Flutter 原生的 `MaterialApp` ，换成 GetX 提供的 `GetMaterialApp` （只改这一处）。

---

## 三、4 个最常用路由（必背，对应 4 个高频场景）

记住：所有路由方法，都不用写 `context` ，直接调用 `Get.xxx()`  即可。

### 1. Get.to(页面) —— 普通打开新页面
- **场景**：点按钮进入详情页、个人页、测试页， 可以返回上一页 （最常用）
- **原生等价写法**： `Navigator.push`
- **示例代码：**
```dart
Get.to(TestPage()); // 打开TestPage，左上角返回能回到上一页
```

### 2. Get.off(页面) —— 打开新页，不能回到当前页
- **场景**：欢迎页 → 主页、登录页 → 首页（跳转后，当前页消失，回不去）
- **原理**：打开新页面的同时，把当前页面从路由栈里删掉。
- **原生等价写法**： `Navigator.pushReplacement`
- **示例代码（你之前的欢迎页跳转，直接用这个）：**
```dart
Get.off(MainTabPage()); // 从欢迎页跳转到Tab主页，再也回不去欢迎页
```

### 3. Get.offAll(页面) —— 清空所有历史，回到根页面
- **场景**：退出登录、完成订单后回到首页（清空之前所有打开的页面，只保留新页面）
- **原生等价写法**： `Navigator.pushAndRemoveUntil`
- **示例代码：**
```dart
Get.offAll(MainTabPage()); // 清空所有页面，只显示MainTabPage
```

### 4. Get.back() —— 返回上一页
- **场景**：页面里点“返回”按钮，回到上一个页面
- **原生等价写法**： `Navigator.pop(context)`
- **示例代码（最简单，不用传任何参数）：**
```dart
Get.back(); // 直接返回上一页
```

---

## 四、关键区别（最简单记忆，不用记复杂原理）
- `Get.to`：打开新页， **能回来**
- `Get.off`：打开新页， **回不来当前页**
- `Get.offAll`：打开新页， **所有历史都清掉，全回不来**
- `Get.back`： **回去** （返回上一页）

---

## 五、为什么必须换 GetMaterialApp？

GetX 路由的核心便利，全靠 `GetMaterialApp`  支撑：
它内部会帮你 **全局保存 context** ，不用你手动传递，所以不管是在页面里、控制器里，都能直接用 `Get.to()` 、 `Get.back()` ，不用管 context 在哪。

**简单说：不换 GetMaterialApp，GetX 路由就用不了！**

---

## 六、原生 vs GetX 路由对比（最直观，一眼看懂优势）

**原生路由（麻烦）**
```dart
// 必须传 context，少了就报错
Navigator.push(context, MaterialPageRoute(builder: (c)=>Page()));
```

**GetX 路由（简单）**
```dart
// 不用 context，直接写，简洁不报错
Get.to(Page());
```

---

## 七、命名路由（简单了解，后面再练）

就是给页面起一个“别名”，用别名跳转（适合页面多、路由复杂的场景，初学先了解）。

**步骤1：在 GetMaterialApp 里注册别名（给页面起名字）**
```dart
GetMaterialApp(
  home: WelcomePage(),
  getPages: [
    // 格式：GetPage(name: 别名, page: 对应页面)
    GetPage(name: '/test', page: ()=>TestPage()),
    GetPage(name: '/tab', page: ()=>MainTabPage()),
  ],
);
```

**步骤2：用别名跳转**
```dart
Get.toNamed('/test'); // 跳转到别名是“/test”的TestPage
```

---

## 八、和你之前的项目结合（一句话总结，直接套用）

结合你之前练的“欢迎页 + 底部Tab”项目，直接套用这4步：
1. `main.dart` 里，把 `MaterialApp`  换成 `GetMaterialApp`
2. 欢迎页 2秒后跳转，用 `Get.off(MainTabPage())` （回不去欢迎页）
3. 普通跳转（比如从首页跳测试页），用 `Get.to(TestPage())`
4. 返回上一页（比如从测试页回首页），用 `Get.back()`

---

## 补充说明（初学必看）
1. **前提**：必须先在 `pubspec.yaml` 里引入 GetX 依赖（之前已经教过，确保已经添加并执行 `flutter pub get`）
2. 所有路由方法，都要先导入 GetX 包： `import 'package:get/get.dart';`
3. 不用记复杂原理，先练熟 4 个核心路由方法（`Get.to`、`Get.off`、`Get.offAll`、`Get.back`），就能应对 90% 的初学场景。