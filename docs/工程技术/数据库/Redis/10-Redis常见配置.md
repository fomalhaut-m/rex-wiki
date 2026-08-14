# Redis 常见配置

redis.conf 配置项说明如下：

## 1. 守护进程

Redis 默认不是以守护进程的方式运行，可以通过该配置项修改，使用 yes 启用守护进程。

```conf
daemonize no
```

## 2. PID 文件

当 Redis 以守护进程方式运行时，Redis 默认会把 pid 写入 /var/run/redis.pid 文件，可以通过 pidfile 指定。

```conf
pidfile /var/run/redis.pid
```

## 3. 端口

指定 Redis 监听端口，默认端口为 6379。作者选用 6379 作为默认端口，因为 6379 在手机按键上 MERZ 对应的号码。

```conf
port 6379
```

## 4. 绑定地址

绑定的主机地址。

```conf
bind 127.0.0.1
```

## 5. 超时

当客户端闲置多长时间后关闭连接，如果指定为 0，表示关闭该功能。

```conf
timeout 300
```

## 6. 日志级别

指定日志记录级别，Redis 总共支持四个级别：debug、verbose、notice、warning，默认为 verbose。

```conf
loglevel verbose
```

## 7. 日志文件

日志记录方式，默认为标准输出。如果配置 Redis 为守护进程方式运行，而这里又配置为日志记录方式为标准输出，则日志将会发送给 /dev/null。

```conf
logfile stdout
```

## 8. 数据库数量

指定数据库的数量，默认数据库为 0，可以使用 SELECT 命令在连接上指定数据库 id。

```conf
databases 16
```

## 9. 持久化配置

指定在多长时间内，有多少次更新操作，就将数据同步到数据文件。

```conf
save <seconds> <changes>
```

Redis 默认配置文件中提供了三个条件：

```conf
save 900 1      # 900秒（15分钟）内有1个更改
save 300 10     # 300秒（5分钟）内有10个更改
save 60 10000   # 60秒内有10000个更改
```

## 10. RDB 压缩

指定存储至本地数据库时是否压缩数据，默认为 yes，Redis 采用 LZF 压缩。如果为了节省 CPU 时间，可以关闭该选项，但会导致数据库文件变的巨大。

```conf
rdbcompression yes
```

## 11. RDB 文件名

指定本地数据库文件名，默认值为 dump.rdb。

```conf
dbfilename dump.rdb
```

## 12. 数据目录

指定本地数据库存放目录。

```conf
dir ./
```

## 13. 主从复制

设置当本机为 slave 服务时，设置 master 服务的 IP 地址及端口，在 Redis 启动时，它会自动从 master 进行数据同步。

```conf
slaveof <masterip> <masterport>
```

## 14. 主从密码

当 master 服务设置了密码保护时，slave 服务连接 master 的密码。

```conf
masterauth <master-password>
```

## 15. 连接密码

设置 Redis 连接密码。如果配置了连接密码，客户端在连接 Redis 时需要通过 AUTH 命令提供密码，默认关闭。

```conf
requirepass foobared
```

## 16. 最大客户端数

设置同一时间最大客户端连接数，默认无限制。当客户端连接数到达限制时，Redis 会关闭新的连接并向客户端返回 max number of clients reached 错误信息。

```conf
maxclients 128
```

## 17. 最大内存

指定 Redis 最大内存限制。达到最大内存后，Redis 会先尝试清除已到期或即将到期的 Key。当此方法处理后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。

```conf
maxmemory <bytes>
```

## 18. AOF 持久化

指定是否在每次更新操作后进行日志记录。Redis 在默认情况下是异步的把数据写入磁盘，如果不开启，可能会在断电时导致一段时间内的数据丢失。默认为 no。

```conf
appendonly no
```

## 19. AOF 文件名

指定更新日志文件名，默认为 appendonly.aof。

```conf
appendfilename appendonly.aof
```

## 20. AOF 同步策略

指定更新日志条件，共有 3 个可选值：

- **no**：表示等操作系统进行数据缓存同步到磁盘（快）
- **always**：表示每次更新操作后手动调用 fsync() 将数据写到磁盘（慢，安全）
- **everysec**：表示每秒同步一次（折衷，默认值）

```conf
appendfsync everysec
```

## 21. 虚拟内存

指定是否启用虚拟内存机制，默认值为 no。VM 机制将数据分页存放，由 Redis 将访问量较少的页即冷数据 swap 到磁盘上，访问多的页面由磁盘自动换出到内存中。

```conf
vm-enabled no
```
