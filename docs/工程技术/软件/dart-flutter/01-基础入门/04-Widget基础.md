# 03-Widget 基础

> 写个简单界面，结合 Java Swing 对比学习 Flutter Widget

---

## 1. 什么是 Widget？

**Flutter 的一切皆 Widget。**

```
Widget = 界面组件 = Java Swing 的 JButton / JLabel / JPanel
```

| Flutter | Java Swing | 说明 |
|---------|-----------|------|
| Text | JLabel | 显示文本 |
| IconButton | JButton | 按钮 |
| Container | JPanel | 容器，可放其他组件 |
| Column | BoxLayout Y | 垂直排列 |
| Row | BoxLayout X | 水平排列 |
| Scaffold | JFrame | 页面骨架 |

---

## 2. 最简单的 Widget

```dart
import 'package:flutter/material.dart';

void main() {
    runApp(
        // MaterialApp = App 根容器，类似 JFrame
        MaterialApp(
            home: Scaffold(
                // Scaffold = 页面骨架，提供 AppBar/Body/BottomNav
                appBar: AppBar(title: Text('我的App')),
                body: Center(child: Text('Hello Vexfy!')),
            ),
        ),
    );
}
```

**对应 Java Swing：**

```java
public class MyApp {
    public static void main(String[] args) {
        JFrame frame = new JFrame("我的App");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(new JLabel("Hello Vexfy!", SwingConstants.CENTER));
        frame.pack();
        frame.setVisible(true);
    }
}
```

---

## 3. Vexfy 的真实 Widget 代码

```dart
// 文件：app/lib/app/modules/player/player_page.dart

class PlayerPage extends GetView<PlayerController> {
    const PlayerPage({super.key});

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: const Text('播放器'),
                backgroundColor: Colors.black,
            ),
            
            body: Container(
                width: double.infinity,
                height: double.infinity,
                color: Colors.grey[900],
                
                child: Column(
                    children: [
                        // 封面
                        Container(
                            width: 300,
                            height: 300,
                            margin: const EdgeInsets.only(top: 50),
                            decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(20),
                            ),
                            child: ClipRRect(
                                borderRadius: BorderRadius.circular(20),
                                child: Image.network(
                                    controller.currentSong.value.coverUrl,
                                    fit: BoxFit.cover,
                                ),
                            ),
                        ),
                        
                        // 歌名 + 歌手
                        Padding(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                                children: [
                                    Text(
                                        controller.currentSong.value.title,
                                        style: const TextStyle(
                                            fontSize: 24,
                                            color: Colors.white,
                                            fontWeight: FontWeight.bold,
                                        ),
                                    ),
                                    const SizedBox(height: 8),
                                    Text(
                                        controller.currentSong.value.artist,
                                        style: TextStyle(
                                            fontSize: 16,
                                            color: Colors.grey[400],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                        
                        // 播放控制按钮
                        Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                                IconButton(
                                    icon: const Icon(Icons.skip_previous),
                                    iconSize: 50,
                                    color: Colors.white,
                                    onPressed: controller.previous,
                                ),
                                IconButton(
                                    icon: Icon(
                                        controller.isPlaying.value
                                            ? Icons.pause_circle_filled
                                            : Icons.play_circle_filled,
                                    ),
                                    iconSize: 70,
                                    color: Colors.white,
                                    onPressed: controller.playPause,
                                ),
                                IconButton(
                                    icon: const Icon(Icons.skip_next),
                                    iconSize: 50,
                                    color: Colors.white,
                                    onPressed: controller.next,
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        );
    }
}
```

---

## 4. 常用 Widget 速查

### 4.1 文本 Widget

```dart
Text(
    '歌名',
    style: TextStyle(
        fontSize: 24,
        color: Colors.white,
        fontWeight: FontWeight.bold,
    ),
)
```

### 4.2 按钮 Widget

```dart
IconButton(
    icon: Icon(Icons.play_arrow),
    iconSize: 50,
    color: Colors.white,
    onPressed: () {
        controller.play();
    },
)

ElevatedButton(
    child: Text('播放'),
    onPressed: () {},
)
```

### 4.3 容器 Widget

```dart
Container(
    width: 300,
    height: 300,
    margin: const EdgeInsets.all(10),
    padding: const EdgeInsets.all(10),
    decoration: BoxDecoration(
        color: Colors.grey[900],
        borderRadius: BorderRadius.circular(20),
    ),
    child: Text('内容'),
)
```

### 4.4 列表 Widget

```dart
ListView.builder(
    itemCount: controller.playlist.length,
    itemBuilder: (context, index) {
        final song = controller.playlist[index];
        return ListTile(
            leading: Icon(Icons.music_note),
            title: Text(song.title),
            subtitle: Text(song.artist),
            onTap: () => controller.playAt(index),
        );
    },
)
```

---

## 5. 布局 Widget（核心）

### 5.1 Column（垂直布局）

```dart
Column(
    mainAxisAlignment: MainAxisAlignment.center,
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [
        Icon(Icons.music_note),
        Text('歌名'),
        Text('歌手'),
    ],
)

// MainAxisAlignment：center / start / end / spaceBetween / spaceAround / spaceEvenly
```

### 5.2 Row（水平布局）

```dart
Row(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: [
        IconButton(icon: Icon(Icons.skip_previous)),
        IconButton(icon: Icon(Icons.play)),
        IconButton(icon: Icon(Icons.skip_next)),
    ],
)
```

### 5.3 Stack（层叠布局）

```dart
Stack(
    children: [
        Image.network(coverUrl),
        Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
                color: Colors.black54,
                child: Text('歌曲名'),
            ),
        ),
    ],
)
```

### 5.4 Expanded（占满剩余空间）

```dart
Row(
    children: [
        Text('左'),
        Expanded(child: Text('中间占满')),
        Text('右'),
    ],
)
```

---

## 6. 实战：写一个简单播放页面

```dart
import 'package:flutter/material.dart';

class SimplePlayerPage extends StatelessWidget {
    const SimplePlayerPage({super.key});

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(title: Text('播放器')),
            body: Column(
                children: [
                    // 封面
                    Container(
                        width: 250,
                        height: 250,
                        margin: const EdgeInsets.only(top: 40),
                        decoration: BoxDecoration(
                            color: Colors.grey[800],
                            borderRadius: BorderRadius.circular(20),
                        ),
                        child: const Icon(
                            Icons.music_note,
                            size: 100,
                            color: Colors.white54,
                        ),
                    ),
                    
                    const SizedBox(height: 30),
                    
                    // 歌曲信息
                    const Text(
                        '晴天',
                        style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
                    ),
                    const Text('周杰伦', style: TextStyle(fontSize: 16, color: Colors.grey)),
                    
                    const SizedBox(height: 50),
                    
                    // 进度条
                    Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 20),
                        child: Column(
                            children: [
                                Container(
                                    height: 4,
                                    decoration: BoxDecoration(
                                        color: Colors.grey[700],
                                        borderRadius: BorderRadius.circular(2),
                                    ),
                                ),
                                const SizedBox(height: 5),
                                Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                        Text('0:00', style: TextStyle(color: Colors.grey[600])),
                                        Text('4:29', style: TextStyle(color: Colors.grey[600])),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    
                    const SizedBox(height: 30),
                    
                    // 控制按钮
                    Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                            IconButton(icon: const Icon(Icons.skip_previous), iconSize: 50),
                            IconButton(icon: const Icon(Icons.play_circle_filled), iconSize: 70),
                            IconButton(icon: const Icon(Icons.skip_next), iconSize: 50),
                        ],
                    ),
                ],
            ),
        );
    }
}
```

---

## 7. Widget 嵌套树

```
Scaffold
└── body: Column
    ├── children: [
    │   ├── Container (封面)
    │   ├── Text (歌名)
    │   ├── Text (歌手)
    │   ├── Column (进度条)
    │   │   ├── Container (进度条背景)
    │   │   └── Row (时间显示)
    │   └── Row (控制按钮)
    │       ├── IconButton (上一首)
    │       ├── IconButton (播放/暂停)
    │       └── IconButton (下一首)
    ]
```

**类比 Java Swing：**
```
JFrame
└── JPanel (contentPane)
    └── BoxLayout (Y轴)
        ├── JLabel (封面)
        ├── JLabel (歌名)
        └── JButton (播放按钮)
```

---

## 8. StatelessWidget vs StatefulWidget

```dart
// StatelessWidget = 静态组件，不会变化
class StaticButton extends StatelessWidget {
    const StaticButton({super.key});

    @override
    Widget build(BuildContext context) {
        return ElevatedButton(
            child: Text('点我'),
            onPressed: () {},
        );
    }
}

// StatefulWidget = 动态组件，会变化
class CounterWidget extends StatefulWidget {
    const CounterWidget({super.key});

    @override
    State<CounterWidget> createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
    int _count = 0;

    @override
    Widget build(BuildContext context) {
        return Column(
            children: [
                Text('计数: $_count'),
                ElevatedButton(
                    child: Text('点我'),
                    onPressed: () {
                        setState(() {
                            _count++;
                        });
                    },
                ),
            ],
        );
    }
}
```

**Vexfy 用的是 GetX，不直接用 StatefulWidget（GetX 的响应式自动处理状态变化）。**

---

## 9. 速查表

| Widget | 作用 | 类比 |
|--------|------|------|
| Text | 显示文本 | JLabel |
| IconButton | 图标按钮 | JButton |
| ElevatedButton | 文字按钮 | JButton |
| Container | 通用容器 | div / JPanel |
| Column | 垂直排列 | flex column |
| Row | 水平排列 | flex row |
| Stack | 层叠布局 | FrameLayout |
| Expanded | 占满剩余 | flex: 1 |
| ListView | 滚动列表 | JList |
| Padding | 内边距 | margin/padding |
| Scaffold | 页面骨架 | Activity |
| GetView | GetX页面 | @Controller |

---

## 下一步

- [04-状态管理GetX](./04-状态管理GetX.md) — 响应式状态，和 Spring Bean 对比