# Elastic Agent 在 Linux 上的安装与 ELK 界面配置指南

## 一、简介
Elastic Agent 是 Elastic 官方推出的轻量级数据采集器，可替代传统的 Filebeat、Metricbeat 等组件，简化日志和指标的收集过程。本文档详细介绍如何在 Linux 服务器上安装 Elastic Agent，并通过 ELK（Elasticsearch, Logstash, Kibana）的界面进行配置。

## 二、前提条件
1. 已部署 Elasticsearch 和 Kibana（版本 8.11.0 或以上）
2. 目标 Linux 服务器可访问 Kibana（通常通过 HTTPS 端口 5601）
3. 具备服务器的 root 或 sudo 权限
4. 确认 Elasticsearch 和 Kibana 的连接信息（URL、用户名、密码）

## 三、安装 Elastic Agent

### 1. 添加 Elastic 仓库
```bash
# 适用于 Debian/Ubuntu 系统
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
sudo apt-get update

# 适用于 RHEL/CentOS 系统
sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
cat <<EOF | sudo tee /etc/yum.repos.d/elastic.repo
[elasticsearch-8.x]
name=Elasticsearch repository for 8.x packages
baseurl=https://artifacts.elastic.co/packages/8.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
EOF
```

### 2. 安装 Elastic Agent
```bash
# Debian/Ubuntu
sudo apt-get install elastic-agent

# RHEL/CentOS
sudo yum install elastic-agent
```

### 3. 验证安装
```bash
elastic-agent version
# 应输出类似：elastic-agent version 8.11.0 (amd64), libbeat 8.11.0 [a0d3b9a4d83e0c22c8b040d65d9c6c3e2c931c built 2023-10-12 19:02:43 +0000 UTC]
```

## 四、ELK 界面配置

### 1. 登录 Kibana
1. 打开浏览器，访问 Kibana（例如：`https://kibana.example.com:5601`）
2. 使用 Elasticsearch 管理员账号（默认用户名为 `elastic`，密码为初始安装时设置的密码）登录

### 2. 进入 Fleet 模块
1. 在左侧导航栏中，点击 **Fleet**
2. 如果是首次使用，系统会引导您完成初始设置，包括创建默认策略

### 3. 创建 Elastic Agent 策略
1. 点击 **Policies** 选项卡
2. 点击 **Create policy**
3. 配置基本信息：
   - **Name**：输入策略名称（例如：`linux-servers-policy`）
   - **Description**：简要描述策略用途
   - **Elasticsearch output**：选择或配置 Elasticsearch 连接信息
   - **Kibana**：选择或配置 Kibana 连接信息

### 4. 添加集成（以系统日志收集为例）
1. 在策略页面，点击 **Add integration**
2. 在搜索框中输入 **System**，选择 **System** 集成
3. 配置收集选项：
   - **Log files**：启用并配置要收集的日志文件路径（例如：`/var/log/messages`, `/var/log/syslog`）
   - **Metrics**：启用并选择要收集的系统指标（CPU、内存、磁盘等）
   - **Advanced options**：可自定义处理器、标签等

### 5. 生成注册令牌
1. 回到 **Fleet** 主页面，点击 **Agents**
2. 点击 **Add agent**
3. 选择之前创建的策略（例如：`linux-servers-policy`）
4. 点击 **Generate enrollment token**
5. 复制生成的注册命令（示例如下）：
```bash
sudo elastic-agent install \
  --fleet-server-url=https://fleet-server.example.com:8220 \
  --enrollment-token=YOUR_ENROLLMENT_TOKEN \
  --force
```

### 6. 在 Linux 服务器上执行注册命令
1. 将上一步复制的命令粘贴到目标 Linux 服务器的终端中执行
2. 若遇到 SSL 证书验证问题，可在命令末尾添加 `--insecure` 参数（仅用于测试环境）
3. 验证 Elastic Agent 服务状态：
```bash
sudo systemctl status elastic-agent
# 应显示 active (running)
```

## 五、验证配置

### 1. 查看 Agent 状态
1. 返回 Kibana 的 **Fleet > Agents** 页面
2. 确认新添加的 Agent 状态为 **Online**

### 2. 查看数据收集情况
1. 点击 Kibana 左侧导航栏中的 **Discover**
2. 在 **Index patterns** 下拉菜单中，选择与收集数据相关的索引模式（例如：`logs-system.*`）
3. 查看是否有数据流入，检查时间范围和字段

### 3. 使用预构建仪表板
1. 点击 Kibana 左侧导航栏中的 **Dashboard**
2. 搜索与收集数据相关的仪表板（例如：`System Overview`）
3. 查看系统指标和日志的可视化展示

## 六、常见问题及解决方法

### 1. Agent 显示为 Offline
- **检查网络连接**：确保服务器可访问 Fleet Server 和 Elasticsearch
- **查看日志**：检查 `/var/log/elastic-agent/elastic-agent.log` 文件
- **重启服务**：执行 `sudo systemctl restart elastic-agent`

### 2. 数据未显示在 Kibana
- **确认索引存在**：在 Kibana 的 **Dev Tools** 中执行 `GET /_cat/indices` 查看索引列表
- **检查数据流**：在 **Fleet > Data Streams** 页面查看数据流向
- **验证 Elasticsearch 连接**：检查 Agent 配置文件 `/etc/elastic-agent/elastic-agent.yml` 中的 Elasticsearch 地址和凭证

### 3. SSL 证书验证失败
- **复制 CA 证书**：将 Elasticsearch 或 Kibana 的 CA 证书复制到 `/etc/elastic-agent/certs/` 目录
- **临时禁用验证**：在注册命令中添加 `--insecure` 参数（仅用于测试）

## 七、高级配置选项

### 1. 添加自定义标签
在策略配置中，可以为收集的数据添加自定义标签，便于后续过滤和分析：
1. 编辑策略
2. 在集成配置的 **Advanced options** 中，添加 `add_tags` 处理器
3. 指定标签名称和值

### 2. 配置日志处理流水线
通过自定义流水线可以对日志进行预处理：
1. 在策略配置中，点击 **Processors**
2. 添加处理器（例如：`grok` 解析、`drop_event` 过滤、`rename` 重命名字段）
3. 保存配置并应用到 Agent

### 3. 监控 Agent 性能
Elastic Agent 自身的性能也可以被监控：
1. 在 **Fleet > Settings** 中，启用 **Agent monitoring**
2. 选择监控数据的存储位置
3. 在 Kibana 的 **Stack Monitoring** 页面查看 Agent 性能指标

## 八、卸载 Elastic Agent
若需要卸载 Elastic Agent，可执行以下命令：
```bash
# 停止并禁用服务
sudo systemctl stop elastic-agent
sudo systemctl disable elastic-agent

# 卸载软件包
# Debian/Ubuntu
sudo apt-get remove --purge elastic-agent

# RHEL/CentOS
sudo yum remove elastic-agent

# 删除配置文件和数据
sudo rm -rf /etc/elastic-agent
sudo rm -rf /var/lib/elastic-agent
```

## 九、参考文档
- [Elastic Agent 官方文档](https://www.elastic.co/guide/en/fleet/current/elastic-agent.html)
- [Fleet 模块使用指南](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html)
- [Elastic Agent 配置参考](https://www.elastic.co/guide/en/fleet/current/elastic-agent-configuration.html)

通过以上步骤，您可以成功在 Linux 服务器上安装 Elastic Agent，并通过 ELK 界面完成配置，实现日志和指标的集中收集与分析。