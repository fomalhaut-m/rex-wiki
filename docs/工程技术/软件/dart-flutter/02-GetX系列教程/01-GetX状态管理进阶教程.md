# 04-状态管理 GetX

> GetX 是 Flutter 中最流行的状态管理方案之一，类似于 Spring 的依赖注入 + 响应式编程。
> 本章结合 Vexfy 的 PlayerService 讲解。

---

## 1. GetX 是什么？

### 对比 Spring Bean

| Spring (Java) | GetX (Dart) |
|---|---|
| `@Service` 注解标记 Bean | 继承 `GetxService` 或 `GetxController` |
| `@Autowired` 注入依赖 | `Get.find<Service>()` 注入 |
| `@Bean` 返回响应式对象 | `.obs` 响应式变量 |
| ApplicationContext 容器 | `Get` 轻量容器 |

GetX 两大核心：**状态管理** + **依赖注入**（还有路由管理，本教程不展开）。

---

## 2. GetxController — 可控的状态容器

`GetxController` 是放置业务逻辑和响应式变量的地方，类似 Spring 的 `@Service`。

```dart
// Java Spring 风格
// @Service
// public class PlayerService {
//     private boolean playing = false;
//     // getter/setter + 业务逻辑
// }

/// Dart GetX 风格
/// PlayerService 继承 GetxService（服务级别单例）
class PlayerService extends GetxService {
  // 单例模式（GetX 推荐，但这里我们手动实现）
  PlayerService._();
  static final PlayerService instance = PlayerService._();

  /// 播放状态：.obs 让它变成响应式的
  /// 任何 Obx 组件监听这个变量，值变化时自动 rebuild
  final RxBool isPlaying = false.obs;

  /// 当前播放位置（毫秒）
  final RxInt position = 0.obs;

  /// 播放模式
  final Rx<PlayMode> playMode = PlayMode.listLoop.obs;

  /// 初始化（在 GetxController 创建时自动调用）
  @override
  void onInit() {
    super.onInit();
    // 监听 just_audio 的状态变化，更新响应式变量
    _player.playerStateStream.listen((state) {
      isPlaying.value = state.playing;  // 注意：.value 访问/修改值
    });
  }

  /// 播放/暂停切换
  Future<void> togglePlayPause() async {
    if (isPlaying.value) {
      await _player.pause();
    } else {
      await _player.play();
    }
  }

  @override
  void onClose() {
    _player.dispose();
    super.onClose();
  }
}
```

### 关键点

- `RxBool` / `RxInt` / `Rx<T>`：响应式包装类，加 `.obs` 后缀
- `.value`：访问或修改响应式变量的值
- `onInit()`：类似 Spring 的 `@PostConstruct`，初始化时调用
- `onClose()`：类似 Spring 的 `@PreDestroy`，销毁时调用
- `GetxService`：单例服务，永久存在，不销毁（比 `GetxController` 更像 Spring Bean）

---

## 3. .obs 响应式变量

`.obs` 是 Dart 扩展方法，给任何对象加上响应式能力：

```dart
// 普通变量（不响应）
bool isPlaying = false;

// 响应式变量（变化时，Obx 内的 UI 自动 rebuild）
final RxBool isPlaying = false.obs;

// 修改值必须用 .value
isPlaying.value = true;

// 读取值也要加 .value（或者在 Obx 里 Dart 自动解包）
print(isPlaying.value);

// RxList - 响应式列表
final RxList<SongModel> playlist = <SongModel>[].obs;
playlist.add(song);        // 自动触发 UI 更新
playlist.removeAt(0);      // 自动触发 UI 更新

// RxMap - 响应式 Map
final RxMap<String, dynamic> config = <String, dynamic>{}.obs;
config['theme'] = 'dark';  // 自动触发 UI 更新
```

### Java 对比

```java
// Java：手动观察者模式
public class PlayerService {
    private boolean playing;
    private final List<Consumer<Boolean>> listeners = new ArrayList<>();

    public void setPlaying(boolean playing) {
        this.playing = playing;
        listeners.forEach(l -> l.accept(playing));  // 手动通知
    }
}

// Dart GetX：自动响应式
// isPlaying.value = true → 自动通知所有监听者
```

---

## 4. GetView — 绑定 Controller 的 Widget

`GetView<T>` 是一个简易的 `StatelessWidget`，自动注入 `T` 类型的 Controller：

```dart
// Java：手动 findViewById / inject
// public class PlayerActivity extends AppCompatActivity {
//     @Autowired
//     PlayerService playerService;
//     @Override
//     protected void onCreate(Bundle savedInstance) {
//         super.onCreate(savedInstance);
//         playerService = SpringContext.getBean(PlayerService.class);
//     }
// }

// Dart GetView：自动注入，无需手动 Get.find
class PlayerPage extends GetView<PlayerService> {
  const PlayerPage({super.key});

  @override
  Widget build(BuildContext context) {
    // GetView 自动提供了 `controller` 字段，直接用
    final playerService = controller;  // 等价于 Get.find<PlayerService>()

    return Scaffold(
      body: Obx(() {
        // Obx：监听响应式变量，闭包内的 UI 自动 rebuild
        final isPlaying = playerService.isPlaying.value;
        return Text(isPlaying ? '播放中' : '已暂停');
      }),
    );
  }
}
```

### Obx — 响应式 UI 刷新

```dart
// Obx 包裹的代码块，监听所有 .obs 变量
Obx(() {
  // 这里用到的每个 .obs 变量变化，都会触发整个 Obx 重新 build
  final song = playerService.currentSong.value;   // 监听 currentSong
  final isPlaying = playerService.isPlaying.value; // 监听 isPlaying
  final pos = playerService.position.value;      // 监听 position

  return Column(
    children: [
      Text(song?.title ?? '无'),
      Text(isPlaying ? '播放中' : '暂停'),
      LinearProgressIndicator(value: pos / 1000),
    ],
  );
});
```

> **注意**：`Obx` 闭包内访问 `.obs` 变量必须用 `.value`，否则 Dart 不知道你在监听。

---

## 5. Bindings — 依赖注入

Bindings 用于在页面创建时注入依赖，类似 Spring 的 `@Configuration` 类：

```dart
/// Vexfy 的 PlayerBinding
/// 在进入 PlayerPage 之前，先注入 PlayerService
class PlayerBinding extends Bindings {
  @override
  void dependencies() {
    // 懒注册：第一次使用时才创建
    // Get.lazyPut<PlayerService>(() => PlayerService());

    // 立即注册：立即创建并注入（推荐用于单例服务）
    Get.put<PlayerService>(PlayerService.instance, permanent: true);
  }
}
```

### 使用 Bindings

```dart
// 在路由配置中使用
GetPage(
  name: '/player',
  page: () => const PlayerPage(),
  binding: PlayerBinding(),  // 进入页面时自动注入依赖
);

// Java 对比：Spring Boot 的 @Bean
// @Bean
// public PlayerService playerService() {
//     return new PlayerService();
// }
```

### 全局 Bindings vs 页面 Bindings

```dart
// 全局：App 启动时就注入（适合单例服务）
GetMaterialApp(
  initialBinding: GlobalBindings(),  // 全局依赖
  getPages: [...],
);

// 页面级：进入页面时才注入（按需加载）
GetPage(
  name: '/player',
  page: () => const PlayerPage(),
  binding: PlayerBinding(),
);
```

---

## 6. Vexfy 真实代码：PlayerService

完整的 PlayerService 源码在 [Vexfy 源码](https://github.com/fomalhaut-m/vexfy) `lib/services/player_service.dart`。

关键结构拆解：

```dart
class PlayerService extends GetxService {
  // ========== 响应式状态（.obs） ==========
  final RxList<SongModel> playlist  = <SongModel>[].obs;  // 播放队列
  final RxInt currentIndex           = (-1).obs;            // 当前索引
  final Rx<SongModel?> currentSong   = Rx<SongModel?>(null);// 当前歌曲
  final RxBool isPlaying            = false.obs;           // 是否播放中
  final RxBool isLoading            = false.obs;           // 是否加载中
  final RxInt position              = 0.obs;                // 当前位置（毫秒）
  final RxInt duration              = 0.obs;                // 总时长（毫秒）
  final Rx<PlayMode> playMode       = PlayMode.listLoop.obs;// 播放模式
  final RxBool isShuffle            = false.obs;           // 随机播放

  // ========== just_audio 播放器 ==========
  late final AudioPlayer _player;
  AudioPlayer get player => _player;  // 对外暴露播放器实例

  // ========== 生命周期 ==========
  @override
  void onInit() {
    super.onInit();
    _initPlayer();
  }

  Future<void> _initPlayer() async {
    _player = AudioPlayer();

    // 监听状态变化，更新响应式变量
    _player.playerStateStream.listen((state) {
      isPlaying.value = state.playing;
      isLoading.value = state.processingState == ProcessingState.loading ||
          state.processingState == ProcessingState.buffering;
    });

    // 监听播放位置
    _player.positionStream.listen((pos) {
      position.value = pos.inMilliseconds;  // Duration → int
    });

    // 监听总时长
    _player.durationStream.listen((dur) {
      if (dur != null) duration.value = dur.inMilliseconds;
    });
  }

  // ========== 播放控制 ==========
  Future<void> playSong(SongModel song, {bool playNow = true}) async { ... }
  Future<void> togglePlayPause() async { ... }
  Future<void> play() async { await _player.play(); }
  Future<void> pause() async { await _player.pause(); }
  Future<void> stop() async { await _player.stop(); }
  Future<void> previous() async { ... }
  Future<void> next() async { ... }
  Future<void> seekTo(int milliseconds) async { ... }

  @override
  void onClose() {
    _player.dispose();  // 释放资源
    super.onClose();
  }
}
```

### Java 对比：Spring Service

```java
// Java Spring Service
@Service  // 标记为 Spring Bean
public class PlayerService {
    @Autowired
    private AudioPlayer audioPlayer;  // 注入依赖

    private final AtomicBoolean playing = new AtomicBoolean(false);
    private final AtomicInteger position = new AtomicInteger(0);

    // Spring 自动管理生命周期
    @PostConstruct
    public void init() { ... }

    @PreDestroy
    public void cleanup() { audioPlayer.release(); }
}
```

GetX 的 `GetxService` 相当于 `@Service` + 自动生命周期管理，`.obs` 相当于把 `AtomicReference` 包装成响应式变量。

---

## 7. 小结

| 概念 | Dart GetX | Java Spring |
|---|---|---|
| 服务类 | `GetxService` | `@Service` |
| 响应式变量 | `.obs` (RxBool/Int/List...) | `AtomicReference` / `Flow` |
| UI 更新 | `Obx(() => ...)` | 手动 `notifyObservers()` |
| 依赖注入 | `Get.put()` / `Get.find()` | `@Autowired` |
| 初始化 | `onInit()` (@override) | `@PostConstruct` |
| 销毁 | `onClose()` (@override) | `@PreDestroy` |

---

## 下一步

→ [05-Vexfy实战](./07-Vexfy实战.md) — 结合真实项目，理解状态管理 + Widget 的配合
