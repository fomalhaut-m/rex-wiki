# 网络诊断工具：TCPView

> Windows 系统网络连接监控利器 - Sysinternals Suite 工具集成员

## 工具简介

**TCPView** 是由 Mark Russinovich 开发的 Windows 网络诊断工具，属于 Sysinternals 工具套件的一部分。该工具能够实时显示系统上所有 TCP 和 UDP 终结点的详细列表，包括本地地址、远程地址以及连接状态，并且能够显示拥有该终结点的进程名称。

相比 Windows 自带的 Netstat 命令，TCPView 提供了更加直观和丰富的界面展示，是网络故障排查和系统监控的得力助手。

## 核心功能

### 1. 实时网络连接监控
- 显示所有活动的 TCP 和 UDP 终结点
- 展示本地和远程 IP 地址及端口
- 显示每个连接对应的进程名称（包括服务名称）
- 自动将 IP 地址解析为域名显示

### 2. 连接状态实时更新
- **每秒自动刷新**（可自定义刷新频率）
- 颜色编码区分连接状态变化：
  - **黄色**：状态发生变化的连接
  - **红色**：已删除的连接
  - **绿色**：新建的连接

### 3. 连接管理功能
- 支持手动关闭已建立的 TCP 连接
- 可将连接列表导出保存为文件

### 4. 命令行版本 Tcpvcon
TCPView 下载包中包含命令行版本 **Tcpvcon**，具有相同功能，适合脚本化使用。

## 使用方法

### 基本界面操作

1. 启动 TCPView 后，程序自动枚举所有活动的 TCP 和 UDP 终结点
2. 默认显示所有地址的域名解析版本
3. 通过工具栏按钮可切换已解析名称的显示
4. 使用 `选项 → 刷新速率` 可调整刷新频率

### 关闭连接

1. 选择 `文件 → 关闭连接`
2. 或右键点击连接，选择 `关闭连接`

### 保存输出

使用 `保存` 菜单项可将当前连接列表保存到文件

## 命令行工具 Tcpvcon

Tcpvcon 是 TCPView 的命令行版本，用法类似于 Windows 内置的 netstat 工具。

### 基本语法

```bash
tcpvcon [-a] [-c] [-n] [进程名称或 PID]
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `-a` | 显示所有终结点（默认为仅显示已建立的 TCP 连接） |
| `-c` | 将输出格式化为 CSV 格式 |
| `-n` | 不解析 IP 地址为域名 |

### 使用示例

```bash
# 显示所有活动的 TCP 和 UDP 连接
tcpvcon -a

# 以 CSV 格式显示所有连接
tcpvcon -a -c

# 显示指定进程的网络连接
tcpvcon chrome.exe

# 显示指定 PID 的网络连接
tcpvcon 1234

# 不解析域名，显示原始 IP
tcpvcon -n
```

## 下载安装

### 官方下载地址

- **下载链接**：[TCPView 下载页面](https://learn.microsoft.com/zh-cn/sysinternals/downloads/tcpview)
- **直接下载**：[TCPView.zip (1.5 MB)](https://download.sysinternals.com/files/TCPView.zip)

### 在线运行

无需安装，可直接通过 Sysinternals Live 运行：
```
https://live.sysinternals.com/Tcpview.exe
```

## 系统要求

- **客户端**：Windows 8.1 及更高版本
- **服务器**：Windows Server 2012 及更高版本

## 应用场景

### 1. 网络故障排查
- 检查是否有异常的网络连接
- 确认特定端口是否被占用
- 查看哪些进程在使用网络

### 2. 安全审计
- 检测异常的网络活动
- 发现可疑的外部连接
- 监控可疑进程的网络行为

### 3. 开发调试
- 检查 WebSocket 连接状态
- 调试 HTTP/HTTPS 请求
- 监控数据库连接
- 验证服务启动后的端口监听

### 4. 性能监控
- 查看网络连接数量
- 分析连接分布情况
- 监控网络带宽使用

## 与其他工具对比

| 工具 | 特点 | 适用场景 |
|------|------|----------|
| **TCPView** | 图形化界面，实时监控，直观易用 | 日常调试，故障排查 |
| **netstat** | 命令行工具，系统自带 | 快速查看，脚本集成 |
| **Tcpvcon** | 命令行版本，功能强大 | 批处理，自动化脚本 |
| **Wireshark** | 深度包分析，协议解析 | 流量分析，问题定位 |

## 使用技巧

1. **快速定位进程**：按进程名称排序，快速找到可疑程序
2. **过滤显示**：使用过滤器只看关心的连接
3. **配合 netstat**：命令行快速确认，GUI 详细分析
4. **定期快照**：保存连接状态进行对比分析
5. **结合 Process Explorer**：查看进程的完整信息

## 注意事项

- 关闭连接功能需谨慎，可能导致数据传输中断
- 部分系统进程拒绝关闭操作
- 需要管理员权限才能查看所有进程的网络连接
- 高频率刷新可能影响系统性能

## 相关资源

- [Sysinternals 工具套件](https://learn.microsoft.com/zh-cn/sysinternals/)
- [Process Explorer](https://learn.microsoft.com/zh-cn/sysinternals/downloads/process-explorer) - 进程管理器
- [Autoruns](https://learn.microsoft.com/zh-cn/sysinternals/downloads/autoruns) - 开机启动项管理
- [TCPView 官方文档](https://learn.microsoft.com/zh-cn/sysinternals/downloads/tcpview)
