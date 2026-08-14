# 08-后台播放 audio_service

> audio_service 是 Flutter 中实现后台音频播放的标准方案。
> 本章对比 Android Service 讲解，并解析 Vexfy 的 VexfyAudioHandler 源码。

---

## 1. audio_service 是什么？

### 对比 Android Service

| Android | Flutter audio_service |
|---|---|
| `Service`（后台组件） | `AudioService`（Flutter 插件） |
| `onStartCommand` | 启动时自动调用 |
| `startForeground` + 通知栏 | 自动创建通知栏 |
| `MediaSession`（锁屏控制） | `AudioService` 内置 `BaseAudioHandler` |
| `BroadcastReceiver`（蓝牙控制） | 自动处理 |
| `onDestroy` | `onTaskRemoved` |

**audio_service 核心功能：**
- 后台播放（App 切到后台不中断）
- 通知栏显示（歌曲名 + 歌手 + 专辑封面）
- 锁屏控制（播放/暂停/上一首/下一首）
- 蓝牙/车载媒体控制
- 耳机线控（按键事件）

---

## 2. 架构概览

```
┌─────────────────────────────────────────────┐
│  PlayerPage / MiniPlayer（Flutter UI）      │
│  监听 PlayerService 的 .obs 变量            │
└──────────────┬──────────────────────────────┘
               │  Obx rebuild
┌──────────────▼──────────────────────────────┐
│  PlayerService（GetxService）              │
│  管理播放状态、队列、just_audio             │
└──────────────┬──────────────────────────────┘
               │  player 实例
┌──────────────▼──────────────────────────────┐
│  VexfyAudioHandler（BaseAudioHandler）      │
│  封装 PlayerService，实现后台播放           │
└──────────────┬──────────────────────────────┘
               │  AudioService.run()
┌──────────────▼──────────────────────────────┐
│  系统层：Android Service / iOS AVSession    │
│  通知栏 + 锁屏 + 媒体按键                   │
└─────────────────────────────────────────────┘
```

---

## 3. VexfyAudioHandler 源码解析

源码路径：`lib/services/audio_handler_service.dart`

### 3.1 类的继承关系

```dart
/// VexfyAudioHandler 继承 BaseAudioHandler
/// BaseAudioHandler 实现了通知栏、锁屏控制的核心逻辑
/// 并混入了 SeekHandler（提供 seek 方法）
class VexfyAudioHandler extends BaseAudioHandler with SeekHandler {
  final AudioPlayer _player;           // just_audio 的播放器实例
  final PlayerService _playerService;   // 业务逻辑层

  MediaItem? _currentMediaItem;        // 当前歌曲信息（通知栏显示用）
```

**Java 对比：** 类似 Spring 的 `@Component` + 实现接口约束方法。

### 3.2 初始化 — 监听 just_audio 状态

```dart
VexfyAudioHandler(this._player, this._playerService) {
  // 监听 just_audio 的播放状态 → 转换为 audio_service 格式
  _playingSubscription = _player.playerStateStream.listen((state) {
    // playbackState 是 BaseAudioHandler 提供的 BehaviorSubject
    // 通知系统：当前播放状态（playing / paused / stopped）
    playbackState.add(playbackState.value.copyWith(
      playing: state.playing,
      processingState: _mapProcessingState(state.processingState),
    ));
  });

  // 监听播放位置 → 同步给系统（锁屏界面进度条）
  _positionSubscription = _player.positionStream.listen((pos) {
    if (_player.playing) {
      seek(pos);  // 更新系统媒体的播放位置
    }
  });

  // 监听总时长变化 → 更新通知栏的时长显示
  _durationSubscription = _player.durationStream.listen((dur) {
    if (dur != null && _currentMediaItem != null) {
      // MediaItem 不可变，用 copyWith 创建新实例
      final updated = _currentMediaItem!.copyWith(duration: dur);
      _currentMediaItem = updated;
      mediaItem.add(updated);  // 通知系统更新通知栏
    }
  });

  // 监听当前歌曲变化 → 更新通知栏歌曲信息
  _currentIndexSubscription =
      _playerService.currentSong.listen((song) async {
    if (song != null) {
      await _updateMediaItem(song);
    } else {
      _currentMediaItem = null;
      mediaItem.add(MediaItem(
        id: '',
        title: '未播放',
        artist: '',
        duration: Duration.zero,
      ));
    }
  });
}
```

**Java 对比：** 相当于 Android 在 `Service.onCreate()` 中注册各种 Listener，监听媒体播放状态并更新 `Notification` 和 `MediaSession`。

### 3.3 MediaItem — 通知栏歌曲信息

```dart
/// 更新通知栏显示的歌曲信息
Future<void> _updateMediaItem(SongModel song) async {
  _currentMediaItem = MediaItem(
    id: song.id,                    // 歌曲唯一 ID
    title: song.title,              // 歌曲名（通知栏主标题）
    artist: song.artist,            // 歌手（通知栏副标题）
    album: song.album ?? '',         // 专辑名
    duration: Duration(milliseconds: song.duration),  // 总时长
    artUri: song.coverUrl != null    // 封面图 URI
        ? Uri.parse(song.coverUrl!)
        : null,
    extras: {
      // 额外数据，可用于 skipToQueueItem 等方法恢复播放
      'file_path': song.filePath ?? '',
    },
  );
  // mediaItem 是 Stream，add 新值后系统自动更新通知栏
  mediaItem.add(_currentMediaItem!);
}
```

**Java 对比：** Android `MediaSession.setMetadata(bundle)` 设置通知栏歌曲信息。

### 3.4 播放控制方法（系统调用）

```dart
@override
Future<void> play() async {
  await _player.play();  // 调用 just_audio 播放
}

@override
Future<void> pause() async {
  await _player.pause();  // 调用 just_audio 暂停
}

@override
Future<void> stop() async {
  await _player.stop();
  playbackState.add(PlaybackState());  // 清空播放状态
}

@override
Future<void> seek(Duration position) async {
  await _player.seek(position);  // 跳转到指定位置
}

@override
Future<void> skipToNext() async {
  await _playerService.next();  // 调用 PlayerService 的下一首
}

@override
Future<void> skipToPrevious() async {
  await _playerService.previous();  // 调用 PlayerService 的上一首
}

/// 跳转到队列中的指定歌曲
@override
Future<void> skipToQueueItem(int index) async {
  if (index >= 0 && index < _playerService.playlist.length) {
    final song = _playerService.playlist[index];
    await _playerService.playSong(song);
  }
}
```

**Java 对比：** 这些方法对应 Android `MediaSession.Callback` 的方法，由系统在用户点击通知栏按钮时调用。

### 3.5 队列管理

```dart
@override
Future<void> addQueueItem(MediaItem mediaItem) async {
  // 将系统队列中的歌曲添加到 PlayerService 播放队列
  final filePath = mediaItem.extras?['file_path'] as String? ?? '';
  final dur = mediaItem.duration ?? Duration.zero;

  final song = SongModel(
    id: mediaItem.id,
    title: mediaItem.title,
    artist: mediaItem.artist ?? '',
    album: mediaItem.album ?? '',
    duration: dur.inMilliseconds,
    coverUrl: mediaItem.artUri?.toString(),
    source: SongSource.local,
    filePath: filePath,
  );
  _playerService.addToPlaylist(song);
}

@override
Future<void> removeQueueItem(MediaItem mediaItem) async {
  _playerService.removeFromPlaylist(mediaItem.id);
}

@override
Future<void> updateQueue(List<MediaItem> queue) async {
  // 批量更新播放队列
  final songs = <SongModel>[];
  for (final item in queue) {
    final filePath = item.extras?['file_path'] as String? ?? '';
    final dur = item.duration ?? Duration.zero;

    songs.add(SongModel(
      id: item.id,
      title: item.title,
      artist: item.artist ?? '',
      album: item.album ?? '',
      duration: dur.inMilliseconds,
      coverUrl: item.artUri?.toString(),
      source: SongSource.local,
      filePath: filePath,
    ));
  }
  await _playerService.setPlaylist(songs);
}
```

### 3.6 模式设置

```dart
@override
Future<void> setShuffleMode(AudioServiceShuffleMode mode) async {
  if (mode == AudioServiceShuffleMode.all) {
    _playerService.toggleShuffle();
  }
}

@override
Future<void> setRepeatMode(AudioServiceRepeatMode mode) async {
  switch (mode) {
    case AudioServiceRepeatMode.none:
      _playerService.playMode.value = PlayMode.sequential;
      break;
    case AudioServiceRepeatMode.one:
      _playerService.playMode.value = PlayMode.singleLoop;
      break;
    case AudioServiceRepeatMode.all:
      _playerService.playMode.value = PlayMode.listLoop;
      break;
    case AudioServiceRepeatMode.group:
      break;
  }
}
```

### 3.7 启动 AudioService

```dart
/// 启动音频服务（在 main.dart 中调用）
Future<VexfyAudioHandler> startAudioService() async {
  return await AudioService.init(
    builder: () {
      final playerService = PlayerService.instance;
      return VexfyAudioHandler(
        playerService.player,   // just_audio 实例
        playerService,
      );
    },
    config: const AudioServiceConfig(
      // Android 通知栏频道 ID（Android 8.0+ 必须）
      androidNotificationChannelId: 'com.vexfy.vexfy.audio',
      // 通知栏频道名称（用户在设置中看到的）
      androidNotificationChannelName: 'Vexfy 音乐播放',
      // 正在播放时显示通知栏
      androidNotificationOngoing: true,
      // 暂停时是否关闭前台通知
      androidStopForegroundOnPause: true,
      // 通知栏主色调（专辑封面取色或品牌色）
      notificationColor: Color(0xFF1DB954),
    ),
  );
}
```

**Java 对比：** 相当于 Android `startForeground(NOTIFICATION_ID, notification)` + `mediaSession.setActive(true)`。

---

## 4. main.dart 中的初始化

```dart
// main.dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 启动音频服务（在 runApp 之前）
  // 这样 App 一启动，后台播放服务就注册到系统了
  await startAudioService();

  runApp(const VexfyApp());
}
```

---

## 5. 小结

| 概念 | Flutter audio_service | Java Android |
|---|---|---|
| 后台服务 | `AudioService.init()` | `Service` + `startForeground()` |
| 通知栏 | 自动创建 | `NotificationManager.notify()` |
| 锁屏控制 | 自动处理 | `MediaSession.setMetadata()` |
| 媒体按键 | 自动处理 | `MediaSession.Callback` |
| 播放状态流 | `playbackState.add()` | `MediaSession.setPlaybackState()` |
| 歌曲信息 | `mediaItem.add(MediaItem)` | `MediaSession.setMetadata()` |
| 播放控制 | 实现 `play/pause/stop/seek...` | `MediaButtonReceiver` |

---

## 下一步

→ [09-打包发布](./11-打包发布.md) — 学习 APK 签名、应用市场发布、CI/CD
