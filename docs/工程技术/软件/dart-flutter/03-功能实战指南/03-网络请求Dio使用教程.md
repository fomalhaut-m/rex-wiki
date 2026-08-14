# 06-网络请求 Dio

> Dio 是 Flutter / Dart 中最流行的 HTTP 客户端库，功能完整，API 友好。
> 本章对比 Java 的 HttpClient / RestTemplate 讲解，并介绍 Vexfy 中的 OSS 上传下载用法。

---

## 1. Dio 是什么？

| Java | Dart |
|---|---|
| `HttpURLConnection`（底层） | `HttpClient`（Dart 底层） |
| `RestTemplate`（Spring 封装） | **Dio**（功能完整封装） |
| `WebClient` / `Retrofit` | Dio + 拦截器（类似 Retrofit） |
| `OkHttp` | Dio 底层默认用 `HttpClient`，也支持自定义 |

**Dio 核心功能：**
- GET / POST / PUT / DELETE / PATCH
- 文件上传 / 下载（支持进度回调）
- 拦截器（请求/响应/错误拦截）
- 请求/响应自动 JSON 转换
- 连接池、超时、代理
- 适配器模式（支持自定义 HTTP 引擎）

---

## 2. 基本用法

### 2.1 创建 Dio 实例

```dart
import 'package:dio/dio.dart';

final dio = Dio(
  BaseOptions(
    baseUrl: 'https://api.vexfy.com',  // 基础 URL
    connectTimeout: const Duration(seconds: 10),
    receiveTimeout: const Duration(seconds: 10),
    headers: {
      'Content-Type': 'application/json',
      // 全局 Header
    },
  ),
);
```

**Java 对比：**
```java
// RestTemplate（Spring）
RestTemplate restTemplate = new RestTemplate();

// 或者 OkHttp
OkHttpClient client = new OkHttpClient.Builder()
    .connectTimeout(10, TimeUnit.SECONDS)
    .build();
```

### 2.2 GET 请求

```dart
// 简单 GET
final response = await dio.get('/songs');

// 带查询参数
final response = await dio.get('/songs', queryParameters: {
  'keyword': '周杰伦',
  'page': 1,
  'size': 20,
});

// 响应体
if (response.statusCode == 200) {
  final data = response.data;  // JSON 自动解析为 dynamic
  final List songs = data['songs'];  // 类似 Java 的 Map<String, Object>
}
```

**Java 对比：**
```java
// RestTemplate GET
String url = "https://api.vexfy.com/songs?keyword=周杰伦&page=1";
Song[] songs = restTemplate.getForObject(url, Song[].class);

// 或者 URI 构建
Uri uri = Uri.parse("https://api.vexfy.com/songs")
    .replace(queryParameters: {'keyword': '周杰伦'});
Song[] songs = restTemplate.getForObject(uri, Song[].class);
```

### 2.3 POST 请求

```dart
// POST JSON
final response = await dio.post('/songs', data: {
  'title': '晴天',
  'artist': '周杰伦',
  'duration': 265000,
});

// 上传文件（FormData）
final formData = FormData.fromMap({
  'file': await MultipartFile.fromFile(
    '/path/to/song.mp3',
    filename: 'song.mp3',
  ),
  'song_id': '12345',
});

final response = await dio.post('/upload', data: formData);
```

**Java 对比：**
```java
// RestTemplate POST
HttpHeaders headers = new HttpHeaders();
headers.setContentType(MediaType.APPLICATION_JSON);

Map<String, Object> body = new HashMap<>();
body.put("title", "晴天");
body.put("artist", "周杰伦");

HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);
Song song = restTemplate.postForObject("/songs", entity, Song.class);

// 文件上传
MultiValueMap<String, Object> parts = new LinkedMultiValueMap<>();
parts.add("file", new FileSystemResource("/path/to/song.mp3"));
restTemplate.postForObject("/upload", parts, UploadResult.class);
```

---

## 3. Vexfy 中的 OSS 上传下载

Vexfy 使用阿里云 OSS（对象存储）存储音频文件和封面图。Dio 负责实际传输。

### 3.1 OSS 上传流程

```
本地音乐文件 → Vexfy → 计算文件 Hash → 请求后端获取上传凭证 → 
Dio PUT 上传到 OSS → 获得 OSS URL → 存入数据库
```

### 3.2 Dio 下载文件（带进度）

```dart
/// 下载 OSS 文件（带进度回调）
/// [url] OSS 文件 URL
/// [savePath] 本地保存路径
Future<void> downloadFile(
  String url,
  String savePath, {
  void Function(int received, int total)? onProgress,
}) async {
  final dio = Dio();

  await dio.download(
    url,
    savePath,
    onReceiveProgress: (received, total) {
      if (total != -1) {
        // 计算百分比
        final percent = received / total;
        onProgress?.call(received, total);
      }
    },
    options: Options(
      // OSS 下载可能需要响应式流
      responseType: ResponseType.stream,
    ),
  );
}
```

**Java 对比：**
```java
// Java 下载（使用 Spring RestTemplate 或 Apache HttpClient）
RestTemplate restTemplate = new RestTemplate();

// 下载大文件需要流式处理
Resource resource = restTemplate.getForObject(url, Resource.class);
// 或使用 Apache HttpClient 的 FileDownload
```

### 3.3 Dio 上传文件到 OSS

```dart
/// 上传文件到 OSS
/// [filePath] 本地文件路径
/// [ossKey] OSS 上的存储路径
/// [onProgress] 进度回调
Future<String> uploadToOss(
  String filePath,
  String ossKey, {
  void Function(int sent, int total)? onProgress,
}) async {
  final dio = Dio();

  // 构造 FormData
  final formData = FormData.fromMap({
    'file': await MultipartFile.fromFile(filePath, filename: ossKey.split('/').last),
    'key': ossKey,
    // 其他 OSS 上传需要的字段（如 policy, signature 等）
  });

  // 上传到自己的后端服务器（由后端转发到 OSS，或提供预签名 URL）
  final response = await dio.post(
    'https://api.vexfy.com/oss/upload',
    data: formData,
    onSendProgress: (sent, total) {
      onProgress?.call(sent, total);
    },
  );

  // 假设返回 OSS URL
  return response.data['url'] as String;
}
```

---

## 4. 拦截器

拦截器是 Dio 最强大的功能之一，类似 Java 的 Filter / Spring AOP。

### 4.1 请求拦截器

```dart
dio.interceptors.add(
  InterceptorsWrapper(
    onRequest: (options, handler) {
      // 每个请求前自动调用
      // 可以在这里统一添加 Token
      final token = getToken();  // 获取 Token
      options.headers['Authorization'] = 'Bearer $token';

      print('🌐 ${options.method} ${options.uri}');
      handler.next(options);  // 继续处理（必须调用）
    },
  ),
);
```

**Java 对比：** 类似 Spring 的 `OncePerRequestFilter`。

### 4.2 响应拦截器

```dart
    onResponse: (response, handler) {
      // 每个响应前自动调用
      print('✅ ${response.statusCode} ${response.requestOptions.uri}');
      handler.next(response);  // 继续处理
    },
```

### 4.3 错误拦截器

```dart
    onError: (error, handler) {
      // 请求失败时调用（网络错误 / HTTP 错误状态码）
      if (error.response?.statusCode == 401) {
        // Token 过期，跳转登录
        goToLogin();
      } else if (error.response?.statusCode == 500) {
        // 服务器错误
        showToast('服务器异常，请稍后重试');
      }
      handler.next(error);  // 或 handler.resolve(response) 消费错误
    },
```

### 4.4 Log 拦截器（调试）

```dart
import 'package:dio/dio.dart';

dio.interceptors.add(LogInterceptor(
  requestBody: true,
  responseBody: true,
  error: true,
  logPrint: (obj) => print('[Dio] $obj'),
));
```

---

## 5. 错误处理

```dart
try {
  final response = await dio.get('/songs');
  if (response.statusCode == 200) {
    final songs = response.data['list'] as List;
    // 处理数据
  }
} on DioException catch (e) {
  // DioException 是 Dio 所有错误的父类
  switch (e.type) {
    case DioExceptionType.connectionTimeout:
      showToast('连接超时，请检查网络');
      break;
    case DioExceptionType.receiveTimeout:
      showToast('服务器响应超时');
      break;
    case DioExceptionType.badResponse:
      // HTTP 错误（如 404, 500）
      print('HTTP ${e.response?.statusCode}');
      break;
    case DioExceptionType.connectionError:
      showToast('网络连接失败');
      break;
    case DioExceptionType.cancel:
      // 请求被取消
      break;
    default:
      showToast('未知错误：${e.message}');
  }
}
```

**Java 对比：**
```java
try {
    ResponseEntity<Song[]> response = restTemplate.getForEntity(url, Song[].class);
} catch (HttpClientErrorException e) {
    // 4xx 错误
    if (e.getStatusCode() == HttpStatus.NOT_FOUND) { ... }
} catch (RestClientException e) {
    // 网络错误 / 超时
    e.printStackTrace();
}
```

---

## 6. 小结

| 功能 | Dart Dio | Java |
|---|---|---|
| HTTP 方法 | `dio.get/post/put/delete` | `restTemplate.getForObject/postForObject` |
| JSON | 自动解析 `response.data` | 手动或 `@JsonDeserialize` |
| 文件上传 | `FormData` + `MultipartFile` | `MultipartFile` / `Resource` |
| 进度回调 | `onSendProgress` / `onReceiveProgress` | 手动流处理 |
| 拦截器 | `InterceptorsWrapper` | `HandlerInterceptor` / `Filter` |
| 超时 | `connectTimeout` / `receiveTimeout` | `setConnectTimeout` |
| 全局配置 | `BaseOptions` | `RestTemplateBuilder` |

---

## 下一步

→ [07-数据库sqflite](./09-数据库sqflite.md) — 了解 Flutter 本地 SQLite 数据库
