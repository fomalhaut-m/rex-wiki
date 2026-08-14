# 修改配置文件

- 复制 `conf/zoo_sample.cfg`文件  改为 `conf/zoo.cfg`

# 启动

## linux

```sh
bin/zkServer.sh start
```



## Windows

```cmd
bin\zkServer.cmd
```

> 直接运行 , 和Linux不同不需要 **start**

# 查看进程

```cmd
C:\Tools\apache-zookeeper-3.6.1-bin\apache-zookeeper-3.6.1-bin\bin>jps
33104 Jps
28164 QuorumPeerMain
24136
```



# 集群配置

```properties
# The number of milliseconds of each tick
# 每一个'tick'的毫秒数
tickTime=2000
# The number of ticks that the initial synchronization phase can take
# 初始同步阶段可以接受的节拍数
initLimit=10
# The number of ticks that can pass between sending a request and getting an acknowledgement
# 在发送请求和获得确认之间可以传递的节拍数
syncLimit=5
# the directory where the snapshot is stored. do not use /tmp for storage, /tmp here is just example sakes.
# 存储快照的目录。不要使用/tmp存储，/tmp只是一个例子。
dataDir=/c/Tools/apache-zookeeper-3.6.1-bin/apache-zookeeper-3.6.1-bin/zkData

# the port at which the clients will connect
# 客户机连接的端口
clientPort=2181
# the maximum number of client connections. increase this if you need to handle more clients
# 客户端连接的最大数目。如果你需要处理更多的客户，增加这个
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the administrator guide before turning on autopurge.
# 在开启自动督促之前，请务必阅读管理员指南中的维护部分。
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
# 要在dataDir中保留的快照数量
#autopurge.snapRetainCount=3
# Purge task interval in hours Set to "0" to disable auto purge feature
# 清除任务时间间隔设置为“0”以禁用自动清除功能
#autopurge.purgeInterval=1

# Metrics Providers
# 度量供应商
# https://prometheus.io Metrics Exporter
#metricsProvider.className=org.apache.zookeeper.metrics.prometheus.PrometheusMetricsProvider
#metricsProvider.httpPort=7000
#metricsProvider.exportJvmInfo=true

# 配置集群
# 所有的服务器 ip:通信端口号:选举端口号 (主从通过选举决定)
server.1=127.0.0.1:2887:3887
server.2=127.0.0.1:2888:3888
server.3=127.0.0.1:2889:3889

```

## 配置集群

- 所有的服务器 ip:通信端口号:选举端口号 (主从通过选举决定)
  - server.1=127.0.0.1:2887:3887
  - server.2=127.0.0.1:2888:3888
  - server.3=127.0.0.1:2889:3889