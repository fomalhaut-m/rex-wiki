# Docker Compose 配置

本目录包含常用的 Docker 容器编排和启动脚本。

## 目录内容

| 脚本 | 说明 |
|------|------|
| [setup_mongo_replica.bat](setup_mongo_replica.bat) | MongoDB 副本集一键配置 |
| [setup_mq.bat](setup_mq.bat) | RabbitMQ 消息队列启动 |
| [setup_redis.bat](setup_redis.bat) | Redis 拉取脚本 |

## MongoDB 副本集配置

### docker-compose.yml

```yaml
services:
  master:
    image: mongo:5.0.13
    container_name: mongo_rs1
    hostname: mongo_rs1
    restart: unless-stopped
    ports:
      - "27017:27017"
    volumes:
      - ./data/db:/data/db
    command: mongod --replSet rs --bind_ip_all
    healthcheck:
      test: mongosh --eval "db.adminCommand('ping')"
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  default:
    name: mongo_network
    driver: bridge
```

### initReplica.js

初始化副本集的 JavaScript 脚本：

```javascript
try {
    rs.initiate({
        _id: "rs",
        members: [
            { _id: 0, host: "mongo_rs1:27017", priority: 2 }
        ]
    });
    sleep(3000);
    db.adminCommand({ setParameter: 1, transactionLifetimeLimitSeconds: 3600 });
    print("Replica set initialized successfully.");
} catch (e) {
    printjson(e);
    quit(1);
}
```

### 使用步骤

1. 执行 `setup_mongo_replica.bat` 一键配置
2. 等待脚本完成初始化
3. 使用连接字符串连接：`mongodb://admin:admin@localhost:27017/?replicaSet=rs&authSource=admin`

## RabbitMQ 配置

快速启动 RabbitMQ 容器：

```bash
docker run -d --name my-rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  -v C:\docker\rabbitmq\data:/var/lib/rabbitmq \
  --hostname my-rabbitmq-host \
  -e RABBITMQ_DEFAULT_VHOST=/ \
  -e RABBITMQ_DEFAULT_USER=guest \
  -e RABBITMQ_DEFAULT_PASS=guest \
  --restart=always \
  rabbitmq:3-management
```

- 管理界面：http://localhost:15672
- 默认账号：guest / guest

## Redis 配置

```bash
docker pull redis:latest
```
