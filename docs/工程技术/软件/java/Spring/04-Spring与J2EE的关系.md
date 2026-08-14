# J2EE与Spring的关系

## J2EE
### 介绍

JavaEE是一组建立在JavaSE之上的标准，解决企业级开发中的一系列问题。请特别留意，它仅仅是个标准，是对一系列接口的约定，众多厂商围绕这个标准做实现。第一个版本的JavaEE 1.2在1999年被发布，到2017年的JavaEE 8，已经经历了将近20年。

### JavaEE包括的标准

Servlet：定义了如何处理Web请求，这个相信大家最熟悉
Java Server Faces：定义了如何使编写Web界面
JAX-RS：定义了如何编写RESTFul的接口
EJB：定义了如何编写“企业Bean”
JPA：定义了如何编写ORM和数据存取
JTA：定义了如何编写事务相关的代码
JMS：定义了如何编写消息队列程序
CDI：定义了如何编写依赖注入
JAX：定义了如何编写XML程序
JAX-WS: 定义了如何编写基于XML的网络服务，即SOAP

---

## Spring

### 介绍

Spring最早可以追溯到2002～2004年，早期的Spring定位于解决J2EE在实际使用上的一系列问题，因为JavaEE的API实在是太难用了。于是总结了一套最佳实践，并总结到了一套框架里。其中最重要的，就是所谓IoC（控制反转）。

### Spring包括的组件
spring-core：Spring的Bean的管理，控制反转和程序上下文
spring-mvc: web开发中的model-view-controller
spring-data: 数据层访问和封装
spring-boot: spring全家桶自助配置和部署管理工具
spring-batch：一个简单的批处理框架
spring-cloud：支持与许多云服务接口的整合
spring-security：认证和权限管理

---

Spring中其实大量使用或者实现了JavaEE标准。比如spring-mvc是在servlet基础之上的封装。spring本身并不提供容器，而是支持使用任何支持servlet标准的容器（如tomcat，jetty等）。

归根到底Spring只是想更好的解决实际问题。JavaEE的实现做得好的就用，做得不好的用比较恰当的方式独立实现或者封装。俗称“接地气”。