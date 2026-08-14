# 05-Vexfy 实战

> 以 Vexfy 音乐播放器为实战案例，整合 Widget + GetX 状态管理，理解从点击到播放的完整数据流。

---

## 1. Vexfy 项目结构回顾

```
vexfy/app/lib/
├── main.dart                    # 入口
├── app/
│   ├── routes/                  # 路由配置
│   └── modules/
│       ├── player/
│       │   ├── player_page.dart # 全屏播放页面
│       │   ├── player_tab.dart   # Tab 1：播放列表
│       │   └── player.dart       # Tab 1 Controller
│       └── ...
├── services/
│   ├── player_service.dart      # 播放器核心服务（GetxService）
│   ├── local_music_service.dart # 本地音乐扫描服务
│   └── audio_handler_service.dart # 后台播放服务
├── data/
│   ├── models/
│   │   └── song_model.dart      # 歌曲数据模型
│   └── database/
│       ├── database_helper.dart # SQLite 数据库助手
│       └── tables.dart           # 表名常量
└── widgets/
    └── mini_player.dart         # 迷你播放器（底部悬浮栏）
```

**核心关系：**
- `PlayerService`（GetxService）管理所有播放状态
- `PlayerPage` / `MiniPlayer` 通过 `Obx` 监听 `PlayerService` 的响应式变量
- `LocalMusicService` 扫描本地音乐，存入 SQLite
- `AudioHandlerService` 包装 `PlayerService`，实现后台播放

---

## 2. PlayerService 源码逐行解析

源码路径：`lib/services/player_service.dart`

### 2.1 类定义与单例

```dart
/// 播放模式枚举
enum PlayMode {
  listLoop,    // 列表循环：播完最后一首回到第一首
  singleLoop,  // 单曲循环：重复当前歌曲
  shuffle,     // 随机播放
  sequential,  // 顺序播放：播完停止
}

/// 播放器服务 - 全局单例
/// 继承 GetxService，自动纳入 GetX 依赖注入容器
/// 相当于 Spring 的 @Service，单例生命周期
class PlayerService extends GetxService {
  // 手动实现单例（也可使用 GetxService 的 permanent 模式）
  PlayerService._();
  static final PlayerService instance = PlayerService._();
```

**Java 对比：**
```java
@Service  // Spring Bean
public class PlayerService {
    private static final PlayerService INSTANCE = new PlayerService();
    public static PlayerService getInstance() { return INSTANCE; }
    private PlayerService() {}
}
```

### 2.2 响应式状态变量

```dart
  /// just_audio 的 AudioPlayer 实例
  /// late: 延迟初始化，onInit 时才赋值
  late final AudioPlayer _player;

  /// 播放队列（响应式列表）
  /// RxList<T> = 响应式的 List，任何增删改操作自动通知 Obx rebuild
  final RxList<SongModel> playlist = <SongModel>[].obs;

  /// 当前播放索引（-1 表示无歌曲）
  final RxInt currentIndex = (-1).obs;

  /// 当前播放歌曲（Rx<T?>，可为 null）
  final Rx<SongModel?> currentSong = Rx<SongModel?>(null);

  /// 播放状态
  final RxBool isPlaying = false.obs;
  final RxBool isLoading = false.obs;

  /// 播放进度（毫秒）
  final RxInt position = 0.obs;
  final RxInt duration = 0.obs;

  /// 播放模式
  final Rx<PlayMode> playMode = PlayMode.listLoop.obs;
  final RxBool isShuffle = false.obs;
```

**Java 对比：** 用 `AtomicInteger` / `AtomicBoolean` + 手动观察者模式才能实现类似效果。

### 2.3 onInit — 初始化播放器

```dart
  @override
  void onInit() {
    super.onInit();  // 父类 GetxService.onInit 必须调用
    _initPlayer();
  }

  Future<void> _initPlayer() async {
    _player = AudioPlayer();  // 创建 just_audio 播放器

    // 监听播放状态（playing / processingState）
    // Stream 是 Dart 异步编程核心，类似 RxJava 的 Flowable
    _player.playerStateStream.listen((state) {
      isPlaying.value = state.playing;  // 是否正在播放
      isLoading.value = state.processingState == ProcessingState.loading ||
          state.processingState == ProcessingState.buffering;  // 是否加载中

      // 播放完毕自动切下一首
      if (state.processingState == ProcessingState.completed) {
        _onSongComplete();
      }
    });

    // 监听播放位置（每 200ms 左右更新一次）
    _player.positionStream.listen((pos) {
      position.value = pos.inMilliseconds;  // Duration → int（毫秒）
    });

    // 监听总时长（加载新歌曲时触发）
    _player.durationStream.listen((dur) {
      if (dur != null) {
        duration.value = dur.inMilliseconds;
      }
    });
  }
```

**Java 对比：** Java 没有内置的 Stream API，需要用 RxJava / Flow / LiveData 才能实现类似效果。

### 2.4 playSong — 播放指定歌曲

```dart
  /// 播放歌曲
  /// [song] 目标歌曲
  /// [playNow] true=立即播放，false=只加入队列不播
  Future<void> playSong(SongModel song, {bool playNow = true}) async {
    // 如果歌曲不在队列中，加入队列
    int idx = playlist.indexWhere((s) => s.id == song.id);
    if (idx < 0) {
      playlist.add(song);
      idx = playlist.length - 1;
    }

    // 切换到该歌曲
    await _switchToIndex(idx, playNow: playNow);
  }

  Future<void> _switchToIndex(int index, {bool playNow = true}) async {
    if (index < 0 || index >= playlist.length) return;

    // 更新当前歌曲信息
    currentIndex.value = index;
    currentSong.value = playlist[index];

    final song = playlist[index];
    final filePath = song.filePath;
    if (filePath == null) return;

    isLoading.value = true;
    try {
      // 加载音频文件路径（just_audio 支持本地路径 / URL）
      await _player.setFilePath(filePath);
      if (playNow) {
        await _player.play();  // 开始播放
      }
    } catch (e) {
      isLoading.value = false;
      rethrow;  // 错误上抛
    }
  }
```

**Java 对比：** 相当于 Spring 的 `@Service` 方法，不需要额外注解。

### 2.5 播放控制

```dart
  /// 播放/暂停切换
  Future<void> togglePlayPause() async {
    if (isPlaying.value) {
      await _player.pause();
    } else {
      await _player.play();
    }
  }

  /// 上一首（考虑 shuffle 模式）
  Future<void> previous() async {
    if (playlist.isEmpty) return;

    int prevIndex;
    if (isShuffle.value && _shuffledIndices != null) {
      // shuffle 模式：从 shuffle 列表中找上一首
      final currentShufflePos = _shuffledIndices!.indexOf(currentIndex.value);
      prevIndex = _shuffledIndices![
          (currentShufflePos - 1 + _shuffledIndices!.length) %
              _shuffledIndices!.length];
    } else {
      // 普通模式：列表循环（最后一首的上一首是第一首）
      prevIndex = (currentIndex.value - 1 + playlist.length) % playlist.length;
    }
    await _switchToIndex(prevIndex);
  }

  /// 下一首
  Future<void> next() async {
    if (playlist.isEmpty) return;
    int nextIndex;
    if (isShuffle.value && _shuffledIndices != null) {
      final currentShufflePos = _shuffledIndices!.indexOf(currentIndex.value);
      nextIndex = _shuffledIndices![
          (currentShufflePos + 1) % _shuffledIndices!.length];
    } else {
      nextIndex = (currentIndex.value + 1) % playlist.length;
    }
    await _switchToIndex(nextIndex);
  }

  /// 跳转到指定百分比
  Future<void> seekToPercent(double percent) async {
    final total = duration.value;
    if (total <= 0) return;
    final target = (total * percent).round();
    await seekTo(target);
  }

  /// 进度百分比（供 UI 使用）
  double get progressPercent {
    if (duration.value == 0) return 0;
    return position.value / duration.value;
  }
```

### 2.6 歌曲播放完成的处理

```dart
  /// 根据播放模式决定下一首行为
  void _onSongComplete() {
    switch (playMode.value) {
      case PlayMode.singleLoop:
        // 单曲循环：回到 0 位置重新播放
        _player.seek(Duration.zero);
        _player.play();
        break;
      case PlayMode.listLoop:
        // 列表循环：下一首
        next();
        break;
      case PlayMode.shuffle:
        // shuffle 模式：下一首
        next();
        break;
      case PlayMode.sequential:
        // 顺序播放：最后一首则停止
        if (currentIndex.value < playlist.length - 1) {
          next();
        } else {
          stop();
        }
        break;
    }
  }
```

---

## 3. LocalMusicService 源码解析

源码路径：`lib/services/local_music_service.dart`

### 3.1 扫描本地音乐

```dart
class LocalMusicService {
  // 单例
  LocalMusicService._();
  static final LocalMusicService instance = LocalMusicService._();

  // on_audio_query 插件：查询设备音频文件
  final oaq.OnAudioQuery _audioQuery = oaq.OnAudioQuery();
  final DatabaseHelper _dbHelper = DatabaseHelper.instance;

  /// 全量扫描本地音乐
  /// 返回扫描到的歌曲数量
  Future<int> scanAllMusic({
    void Function(int scanned, int total)? onProgress,  // 进度回调
  }) async {
    // 请求存储权限（Android 需要）
    final hasPermission = await requestPermission();
    if (!hasPermission) throw Exception('缺少存储权限');

    // 查询所有音频文件
    final songs = await _audioQuery.querySongs(...);

    int count = 0;
    final total = songs.length;

    for (final song in songs) {
      if (!_isSupportedFormat(uri)) continue;

      final songModel = _fromAudioSongModel(song);  // 转换模型
      await _upsertSong(songModel);  // 存入 SQLite
      count++;
      onProgress?.call(count, total);  // 回调进度
    }
    return count;
  }
}
```

**Java 对比：** 相当于 Spring 的 `@Service` 扫描文件系统，解析 MP3 元数据存入数据库。

---

## 4. PlayerPage 源码解析

源码路径：`lib/app/modules/player/player_page.dart`

### 4.1 整体结构

```dart
class PlayerPage extends StatelessWidget {
  const PlayerPage({super.key});

  @override
  Widget build(BuildContext context) {
    // 获取 PlayerService 实例（GetX 依赖注入）
    final playerService = Get.find<PlayerService>();

    return Scaffold(
      backgroundColor: Colors.white,
      body: Obx(() {
        // Obx 监听 PlayerService 的所有 .obs 变量
        // 任何响应式变量变化，build 方法重新执行
        final song = playerService.currentSong.value;
        final isPlaying = playerService.isPlaying.value;
        final isLoading = playerService.isLoading.value;

        return SafeArea(
          child: Column(
            children: [
              _buildTopBar(context),      // 顶部返回按钮
              Expanded(child: _buildCoverView(song)),  // 封面
              _buildSongInfo(song),       // 歌名歌手
              _buildProgressBar(playerService),  // 进度条
              _buildControlBar(playerService, isPlaying, isLoading), // 控制栏
            ],
          ),
        );
      }),
    );
  }
}
```

### 4.2 进度条 — Obx 嵌套

```dart
  Widget _buildProgressBar(PlayerService playerService) {
    return Obx(() {
      // Obx 监听 position 和 duration
      final pos = playerService.position.value;
      final dur = playerService.duration.value;
      final percent = dur > 0 ? pos / dur : 0.0;

      return SliderTheme(
        data: SliderThemeData(trackHeight: 4, thumbShape: RoundSliderThumbShape(enabledThumbRadius: 6)),
        child: Slider(
          value: percent.clamp(0.0, 1.0),
          onChanged: (value) {
            // 拖动进度条，跳转播放位置
            playerService.seekToPercent(value);
          },
        ),
      );
    });
  }
```

### 4.3 控制栏

```dart
  Widget _buildControlBar(PlayerService playerService, bool isPlaying, bool isLoading) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        // 随机播放按钮（响应式图标颜色）
        Obx(() => IconButton(
              icon: Icon(Icons.shuffle,
                color: playerService.isShuffle.value
                    ? AppTheme.primaryGreen  // 开启：绿色
                    : AppTheme.textSecondary),  // 关闭：灰色
              onPressed: () => playerService.toggleShuffle(),
            )),

        // 上一首
        IconButton(
          icon: const Icon(Icons.skip_previous, size: 44),
          onPressed: () => playerService.previous(),
        ),

        // 播放/暂停（加载中显示转圈）
        isLoading
            ? const SizedBox(width: 64, height: 64, child: CircularProgressIndicator(...))
            : IconButton(
                icon: Icon(
                  isPlaying ? Icons.pause_circle_filled : Icons.play_circle_filled,
                  size: 64, color: AppTheme.primaryGreen,
                ),
                onPressed: () => playerService.togglePlayPause(),
              ),

        // 下一首
        IconButton(
          icon: const Icon(Icons.skip_next, size: 44),
          onPressed: () => playerService.next(),
        ),

        // 循环模式（响应式）
        Obx(() => IconButton(
              icon: Icon(_getRepeatIcon(playerService.playMode.value),
                color: playerService.playMode.value != PlayMode.sequential
                    ? AppTheme.primaryGreen : AppTheme.textSecondary),
              onPressed: () => playerService.cycleRepeatMode(),
            )),
      ],
    );
  }
```

---

## 5. 完整流程：用户点击播放

```
用户点击歌曲
    │
    ▼
PlayerPage/PlayerTab 调用 playerService.playSong(song)
    │
    ▼
playSong() 内部：
  1. playlist.add(song)  →  RxList 响应式更新，UI 自动刷新队列
  2. _switchToIndex(idx) →  currentSong.value = song（响应式）
  3. _player.setFilePath(filePath)  →  just_audio 加载音频
  4. _player.play()  →  音频播放
    │
    ▼
just_audio 触发 playerStateStream / positionStream
    │
    ▼
PlayerService 监听回调：
  isPlaying.value = true
  position.value = 当前位置（毫秒）
  duration.value = 总时长（毫秒）
    │
    ▼
PlayerPage 的 Obx 监听到响应式变量变化
    │
    ▼
Obx 闭包重新执行：
  - Text(song.title) 更新歌名
  - Text(isPlaying ? '播放中' : '暂停') 更新状态
  - Slider 更新进度条
  - Icon 更新播放/暂停图标
```

---

## 下一步

→ [06-网络请求Dio](./08-网络请求Dio.md) — 了解 Flutter 如何做网络请求
