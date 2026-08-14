# Shiro 配置过程

## 1. 导入 jar 包

- spring mvc 相关
- shiro 相关

## 2. 配置

### 2.1 web.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://java.sun.com/xml/ns/javaee"
    xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd"
    id="WebApp_ID" version="2.5">

    <!-- 用于上下文加载器侦听器的配置文件 -->
    <context-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:applicationContext.xml</param-value>
    </context-param>

    <!-- 初始化监听器 -->
    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>

    <!-- 这个Spring Web应用程序的前端控制器，负责处理所有申请 -->
    <servlet>
        <servlet-name>spring</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <!-- 将所有请求映射到DispatcherServlet以进行处理 -->
    <servlet-mapping>
        <servlet-name>spring</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>

    <!-- 将所有请求映射到DispatcherServlet以进行处理 -->
    <!-- 1. 配置 Shiro 的 shiroFilter. 2. DelegatingFilterProxy 实际上是 Filter 的一个代理对象. -->
    <!-- 默认情况下, Spring 会到 IOC 容器中查找和 <filter-name> 对应的 filter bean. -->
    <!-- 也可以通过 targetBeanName 的初始化参数来配置 filter bean 的 id. -->

    <filter>
        <filter-name>shiroFilter</filter-name>
        <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
        <init-param>
            <param-name>targetFilterLifecycle</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>

    <filter-mapping>
        <filter-name>shiroFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
</web-app>
```

### 2.2 applicationContext.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
```

## 3. 配置 SecurityManager

```xml
<bean id="securityManager" class="org.apache.shiro.web.mgt.DefaultWebSecurityManager">
    <property name="cacheManager" ref="cacheManager"/>
    <property name="authenticator" ref="authenticator"></property>

    <property name="realms">
        <list>
            <ref bean="jdbcRealm"/>
            <ref bean="secondRealm"/>
        </list>
    </property>

    <property name="rememberMeManager.cookie.maxAge" value="10"></property>
</bean>
```

## 4. 配置 CacheManager

### 4.1 需要加入 ehcache 的 jar 包及配置文件

```xml
<bean id="cacheManager" class="org.apache.shiro.cache.ehcache.EhCacheManager">
    <property name="cacheManagerConfigFile" value="classpath:ehcache.xml"/>
</bean>

<bean id="authenticator"
    class="org.apache.shiro.authc.pam.ModularRealmAuthenticator">
    <property name="authenticationStrategy">
        <bean class="org.apache.shiro.authc.pam.AtLeastOneSuccessfulStrategy"></bean>
    </property>
</bean>
```

## 5. 配置 Realm

### 5.1 直接配置实现了 org.apache.shiro.realm.Realm 接口的 bean

```xml
<bean id="jdbcRealm" class="com.atguigu.shiro.realms.ShiroRealm">
    <property name="credentialsMatcher">
        <bean class="org.apache.shiro.authc.credential.HashedCredentialsMatcher">
            <property name="hashAlgorithmName" value="MD5"></property>
            <property name="hashIterations" value="1024"></property>
        </bean>
    </property>
</bean>

<bean id="secondRealm" class="com.atguigu.shiro.realms.SecondRealm">
    <property name="credentialsMatcher">
        <bean class="org.apache.shiro.authc.credential.HashedCredentialsMatcher">
            <property name="hashAlgorithmName" value="SHA1"></property>
            <property name="hashIterations" value="1024"></property>
        </bean>
    </property>
</bean>
```

## 6. 配置 LifecycleBeanPostProcessor

可以自定的来调用配置在 Spring IOC 容器中 shiro bean 的生命周期方法。

```xml
<bean id="lifecycleBeanPostProcessor" class="org.apache.shiro.spring.LifecycleBeanPostProcessor"/>

<!-- Enable Shiro Annotations for Spring-configured beans. Only run after the lifecycleBeanProcessor has run: -->
```

## 7. 启用 IOC 容器中使用 shiro 的注解

但必须在配置了 LifecycleBeanPostProcessor 之后才可以使用。

```xml
<bean class="org.springframework.aop.framework.autoproxy.DefaultAdvisorAutoProxyCreator"
      depends-on="lifecycleBeanPostProcessor"/>

<bean class="org.apache.shiro.spring.security.interceptor.AuthorizationAttributeSourceAdvisor">
    <property name="securityManager" ref="securityManager"/>
</bean>
```

## 8. 配置 ShiroFilter

- id 必须和 web.xml 文件中配置的 DelegatingFilterProxy 的 filter-name 一致
- 若不一致，则会抛出：NoSuchBeanDefinitionException
- 因为 Shiro 会来 IOC 容器中查找和 filter-name 名字对应的 filter bean

### 配置哪些页面需要受保护，以及访问这些页面需要的权限

- **anon**：可以被匿名访问
- **authc**：必须认证（即登录）后才可能访问的页面
- **logout**：登出
- **roles**：角色过滤器

```xml
<bean id="shiroFilter" class="org.apache.shiro.spring.web.ShiroFilterFactoryBean">
    <property name="securityManager" ref="securityManager"/>
    <!-- 登陆页面 -->
    <property name="loginUrl" value="/login.jsp"/>
    <!-- 登陆成功页面 -->
    <property name="successUrl" value="/list.jsp"/>
    <!-- 无权限页面 -->
    <property name="unauthorizedUrl" value="/unauthorized.jsp"/>
    <property name="filterChainDefinitionMap" ref="filterChainDefinitionMap"></property>
    <property name="filterChainDefinitions">
        <value>
            /login.jsp = anon
            /shiro/login = anon
            /shiro/logout = logout
            /user.jsp = roles[user]
            /admin.jsp = roles[admin]
            /** = authc
        </value>
    </property>
</bean>
```

## 9. 配置一个 bean

该 bean 实际上是一个 Map，通过实例工厂方法的方式。

```xml
<bean id="filterChainDefinitionMap"
    factory-bean="filterChainDefinitionMapBuilder" factory-method="buildFilterChainDefinitionMap"></bean>

<bean id="filterChainDefinitionMapBuilder"
    class="com.atguigu.shiro.factory.FilterChainDefinitionMapBuilder"></bean>

<bean id="shiroService"
    class="com.atguigu.shiro.services.ShiroService"></bean>
</beans>
```
