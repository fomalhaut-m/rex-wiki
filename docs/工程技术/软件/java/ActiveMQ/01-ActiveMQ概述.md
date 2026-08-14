#### 系统之间直接调用实际工程落地存在的问题

微服务架构后，链式调用是我们在写程序时候的一般流程，为了完成一个整体功能会将其拆分成多个函数（或子模块），比如模块A调用模块B，模块B调用模块C，模块C调用模块D。单在大型分布式应用中，系统的RPC交互复杂。

> RPC(Remote Procedure Call Protocol)--[远程过程调用](https://baike.so.com/doc/7849156-8123251.html)协议，它是一种通过网络从远程[计算机](https://baike.so.com/doc/3435270-3615253.html)程序上请求服务，而不需要了解底层网络技术的协议。[RPC协议](https://baike.so.com/doc/1329787-1405841.html)假定某些[传输协议](https://baike.so.com/doc/4873795-5091524.html)的存在，如TCP或UDP，为通信程序之间携带信息数据。在OSI[网络通信](https://baike.so.com/doc/5715305-5928031.html)模型中，RPC跨越了传输层和应用层。RPC使得开发包括网络[分布式](https://baike.so.com/doc/6151328-6364526.html)多程序在内的[应用程序](https://baike.so.com/doc/3417785-3597266.html)更加容易。

一个功能背后要调用上百个接口并非不可能，从单机架构过渡到分布式微服务的通例。

其存在一下三大问题

1. 系统接口之间接口耦合严重
2. 面对大流量并发时，容易被冲垮
3. 等待同步存在性能问题

# MQ的产品种类

1. Kafka
2. RabbitMQ
3. RockeMQ
4. ActiveMQ

