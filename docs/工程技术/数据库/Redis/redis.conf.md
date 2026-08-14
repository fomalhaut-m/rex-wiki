# Redis 配置文件

> Redis 官方配置文件示例，包含所有配置项的说明和默认值。

```conf
# Redis configuration file example.
#
# Note that in order to read the configuration file, Redis must be
# started with the file path as first argument:
#
# ./redis-server /path/to/redis.conf

# Note on units: when memory size is needed, it is possible to specify
# it in the usual form of 1k 5GB 4M and so forth:
#
# 1k => 1000 bytes
# 1kb => 1024 bytes
# 1m => 1000000 bytes
# 1mb => 1024*1024 bytes
# 1g => 1000000000 bytes
# 1gb => 1024*1024*1024 bytes
#
# units are case insensitive so 1GB 1Gb 1gB are all the same.

################################## INCLUDES ###################################

# Include one or more other config files here.
# include /path/to/local.conf
# include /path/to/other.conf

################################## MODULES #####################################

# loadmodule /path/to/my_module.so
# loadmodule /path/to/other_module.so

################################## NETWORK #####################################

# bind 192.168.1.100 10.0.0.1
# bind 127.0.0.1 ::1
bind 127.0.0.1

protected-mode yes

port 6379

tcp-backlog 511

# unixsocket /tmp/redis.sock
# unixsocketperm 700

timeout 0

tcp-keepalive 300

################################# GENERAL #####################################

daemonize yes

supervised no

pidfile /var/run/redis_6379.pid

loglevel notice

logfile ""

# syslog-enabled no
# syslog-ident redis
# syslog-facility local0

databases 16

always-show-logo yes

################################ SNAPSHOTTING  ################################

save 900 1
save 300 10
save 60 10000

stop-writes-on-bgsave-error yes

rdbcompression yes

rdbchecksum yes

dbfilename dump.rdb

dir ./

################################# REPLICATION #################################

# replicaof <masterip> <masterport>
# masterauth <master-password>

replica-serve-stale-data yes

replica-read-only yes

repl-diskless-sync no

repl-diskless-sync-delay 5

# repl-ping-replica-period 10

# repl-timeout 60

repl-disable-tcp-nodelay no

# repl-backlog-size 1mb

# repl-backlog-ttl 3600

replica-priority 100

# min-replicas-to-write 3
# min-replicas-max-lag 10

# replica-announce-ip 5.5.5.5
# replica-announce-port 1234

################################## SECURITY ###################################

# requirepass foobared

# rename-command CONFIG b840fc02d524045429941cc15f59e41cb7be6c52
# rename-command CONFIG ""

################################### CLIENTS ####################################

# maxclients 10000

############################## MEMORY MANAGEMENT ################################

# maxmemory <bytes>

maxmemory-policy noeviction

maxmemory-samples 5

# replica-ignore-maxmemory yes

############################# LAZY FREEING ####################################

lazyfree-lazy-eviction no
lazyfree-lazy-expire no
lazyfree-lazy-server-del no
replica-lazy-flush no

############################## APPEND ONLY MODE ###############################

appendonly no

appendfilename "appendonly.aof"

# appendfsync always
appendfsync everysec
# appendfsync no

no-appendfsync-on-rewrite no

auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

aof-load-truncated yes

aof-use-rdb-preamble yes

################################ LUA SCRIPTING  ###############################

lua-time-limit 5000

################################ REDIS CLUSTER  ###############################

# cluster-enabled yes
# cluster-config-file nodes-6379.conf
# cluster-node-timeout 15000
# cluster-replica-validity-factor 10
# cluster-migration-barrier 1
# cluster-require-full-coverage yes
# cluster-replica-no-failover no
# cluster-announce-ip 10.1.1.5
# cluster-announce-port 6379
# cluster-announce-bus-port 6380

################################## SLOW LOG ###################################

slowlog-log-slower-than 10000

slowlog-max-len 128

################################ LATENCY MONITOR ##############################

latency-monitor-threshold 0

############################# EVENT NOTIFICATION ##############################

# 通知类型：K键空间事件、E键事件等
# g无心之失_templates键事件、l列事件、s集合事件、z有序集合事件、x过期事件
# $Stream命令、e配置事件、m键空间事件（模拟）
# notify-keyspace-events ""

############################## ADVANCED CONFIG ###############################

list-compress-depth 0

set-max-intset-entries 512

zset-max-ziplist-entries 128
zset-max-ziplist-value 64

hll-sparse-max-bytes 3000

stream-node-max-bytes 4096
stream-node-max-entries 100

activerehashing yes

client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60

# client-query-buffer-limit 1gb
# proto-max-bulk-len 512mb

hz 10

dynamic-hz yes

aof-rewrite-incremental-fsync yes

rdb-save-incremental-fsync yes

# lfu-log-factor 10
# lfu-decay-time 1

# activedefrag yes
# active-defrag-ignore-bytes 100mb
# active-defrag-threshold-lower 10
# active-defrag-threshold-upper 100
# active-defrag-cycle-min 5
# active-defrag-cycle-max 75
# active-defrag-max-scan-fields 1000
```
