# Spring AI Examples

Spring AI 框架实践示例集合，涵盖聊天模型、MCP 协议、RAG 检索增强生成等核心功能。

## 项目概览

| 项目 | 说明 | 关键特性 |
|------|------|----------|
| `spring-ai-chat-model-examples` | 多模型聊天示例 | 多种 LLM 支持、嵌入模型、工具调用 |
| `spring-ai-advisors-examples` | 聊天记忆示例 | 多轮对话、多会话隔离、消息窗口管理 |
| `spring-ai-mcp-client-examples` | MCP 客户端示例 | 连接外部 MCP 服务器（STDIO/SSE） |
| `spring-ai-mcp-server-examples` | MCP 服务器示例 | @McpTool 注解暴露本地工具 |
| `spring-ai-rag-examples` | RAG 基础示例 | 检索增强生成核心流程 |
| `spring-ai-rag-chroma-examples` | Chroma 向量存储 | 语义搜索、元数据过滤 |
| `spring-ai-rag-redis-examples` | Redis 向量存储 | 高性能向量搜索、元数据过滤 |

---

## 1. spring-ai-chat-model-examples

### 功能特点
- 演示 Spring AI 框架对多种大语言模型的支持
- 支持云厂商模型（DeepSeek、MiniMax、OpenAI 等）
- 支持本地部署模型（Ollama）
- 嵌入模型和工具调用功能

### 核心示例

#### MiniMaxChatExample
| 示例 | 说明 |
|------|------|
| 基本对话 | 简单问答 |
| 温度参数 | 控制生成随机性 (temperature) |
| 最大令牌数 | 限制响应长度 (maxTokens) |
| TopP采样 | 核采样策略 (topP) |
| 系统消息 | 设置助手角色和风格 |
| 流式响应 | 实时流式输出 (stream) |
| 存在惩罚 | 避免重复提及 (presencePenalty) |
| 频率惩罚 | 避免重复词句 (frequencyPenalty) |
| 停止序列 | 自定义生成停止条件 |

#### MiniMaxEmbeddingExample
- 文本向量化（Embedding）
- 批量嵌入多文本
- 余弦相似度计算

#### DeepSeekChatExample
- 实体提取（Entity）
- 返回结构化数据

#### ToolExamples
- 注解式工具 `@Tool`
- 编程式工具 `MethodToolCallback`
- 函数式工具 `Function<T, R>`
- returnDirect 模式

### 支持的模型

| 模型 | 依赖 | 用途 |
|------|------|------|
| OpenAI | spring-ai-starter-model-openai | GPT-3.5/GPT-4 |
| 智谱 AI | spring-ai-starter-model-zhipuai | GLM-3/GLM-4 |
| Ollama | spring-ai-starter-model-ollama | 本地模型 |
| MiniMax | spring-ai-starter-model-minimax | abab 系列 |
| Mistral AI | spring-ai-starter-model-mistral-ai | Mistral 系列 |
| HuggingFace | spring-ai-starter-model-huggingface | HF 模型 |
| DeepSeek | spring-ai-starter-model-deepseek | DeepSeek 系列 |
| Anthropic | spring-ai-starter-model-anthropic | Claude 系列 |

---

## 2. spring-ai-advisors-examples

### 功能特点
- 使用 `InMemoryChatMemoryRepository` 作为内存存储
- 通过 `MessageWindowChatMemory` 管理消息窗口
- 自定义 `ChatMemoryWrapper` 添加日志记录

### 核心示例

| 示例 | 说明 |
|------|------|
| 单轮对话 | 无记忆的独立对话 |
| 多轮对话（带记忆） | 使用 `MessageChatMemoryAdvisor` 记住对话历史 |
| 对话摘要 | 助手能记住并总结之前讨论过的内容 |
| 多会话独立记忆 | 通过 `conversationId` 隔离不同会话的记忆 |

---

## 3. spring-ai-mcp-client-examples

### 功能特点
- 支持多种传输协议（SSE、Streamable HTTP、STDIO）
- 自动将 MCP 工具注册为 Spring AI 工具
- 与 MiniMax 大模型集成

### 演示场景

#### STDIO 传输
连接本地 MCP 服务器（如文件系统操作）

#### SSE 传输
连接远程 MCP 服务器（如高德地图）

---

## 4. spring-ai-mcp-server-examples

### 功能特点
- 注解驱动：`@McpTool` 快速创建工具
- 自动生成工具描述和参数 Schema
- 多传输协议支持（STDIO、SSE、Streamable HTTP）
- 基于 WebFlux 实现高性能

### Provider 示例

| 类名 | 功能说明 |
|------|----------|
| `ToolProvider` | 天气查询（调用 Open-Meteo API） |
| `AsyncToolProvider` | 异步工具示例 |
| `CompletionProvider` | 文本补全功能 |
| `DocumentProvider` | 文档搜索/检索 |
| `PromptProvider` | 提示模板管理 |
| `SpringAiToolProvider` | Spring AI 工具集成 |
| `UserProfileResourceProvider` | 用户资源管理 |

---

## 5. spring-ai-rag-examples

### RAG 流程概述

```
文档加载 → 文本分割 → 向量化 → 存储 → 检索 → 生成
```

### 核心步骤

| 步骤 | 说明 |
|------|------|
| 1. 文档加载 | 创建 Document 对象 |
| 2. 文本分割 | 将长文档分割成块 |
| 3. 向量化 | 文本转向量（需要 EmbeddingModel） |
| 4. 存储 | 存入向量数据库 |
| 5. 检索 | 相似性搜索 |
| 6. 生成 | LLM 生成回答 |

### RAG 优势
1. **最新信息**：可接入实时更新的知识库
2. **可溯源**：答案可追溯到具体文档
3. **减少幻觉**：基于检索内容生成，降低虚构概率
4. **成本效益**：无需微调即可使用新知识

---

## 6. spring-ai-rag-chroma-examples

### 环境前置条件
```bash
docker run -p 8000:8000 ghcr.io/chroma-core/chroma:1.0.0
```

### 功能特点
- 使用 ChromaVectorStore 存储和检索文档
- 结合 MiniMax 嵌入模型进行向量化
- 支持元数据过滤和相似度阈值
- 完整的文档 CRUD 操作

### 演示场景

| 示例 | 说明 |
|------|------|
| 添加文档 | 批量添加带元数据的文档 |
| 基本相似性搜索 | 基于语义找到最相关的文档 |
| 带阈值的搜索 | 只返回相似度超过阈值的文档 |
| 元数据过滤 | 按 category、year 等字段筛选 |
| 删除文档 | 根据 ID 删除文档 |

### Chroma 特点
1. **轻量级**：易于部署和集成
2. **开源免费**：可在本地部署
3. **元数据支持**：支持丰富的过滤条件

---

## 7. spring-ai-rag-redis-examples

### 环境前置条件
```bash
docker run -p 6379:6379 redis/redis-stack
```

**注意**：必须使用 Redis Stack 版本，普通 Redis 不支持向量搜索。

### 功能特点
- 使用 RedisVectorStore 存储和检索文档
- 结合 MiniMax 嵌入模型进行向量化
- 支持元数据过滤（tag 和 numeric 字段）
- 高性能的向量相似性搜索

### 演示场景

| 示例 | 说明 |
|------|------|
| 添加文档 | 批量添加带元数据的文档到 Redis |
| 基本相似性搜索 | 基于语义找到最相关的文档 |
| 带阈值的搜索 | 只返回相似度超过阈值的文档 |
| 元数据过滤 | 按 category、year 等字段筛选 |
| 删除文档 | 根据 ID 删除文档 |

### Redis 向量存储特点
1. **高性能**：Redis 内存数据库特性，查询速度极快
2. **企业级**：成熟的数据库解决方案，适合生产环境
3. **向量索引**：支持 HNSW 和 FLAT 两种索引算法

---

## 技术栈

- Spring Boot 3.3.5
- Spring AI 1.1.4
- Java 17+
- 多种向量数据库（Chroma、Redis Stack）
- 多种大语言模型（MiniMax、DeepSeek、OpenAI 等）

## 环境配置

```properties
# MiniMax API 密钥
MINIMAX_API_KEY2=your-api-key

# DeepSeek API 密钥
DEEPSEEK_API_KEY=your-api-key
```

## 运行方式

```bash
# 编译项目
mvn compile

# 运行各个示例
cd spring-ai-chat-model-examples
java com.example.chat.minimax.MiniMaxChatExample

cd spring-ai-advisors-examples
java com.example.chatmemory.InMemoryChatMemoryRepositoryExample

# 启动需要外部服务的项目（如 RAG）
docker run -p 8000:8000 ghcr.io/chroma-core/chroma:1.0.0
docker run -p 6379:6379 redis/redis-stack
```

---

## 项目关系图

```
┌─────────────────────────────────────────────────────────┐
│                   Spring AI Examples                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────────┐    ┌─────────────────────────┐     │
│  │  Chat Model     │    │      RAG                │     │
│  │  Examples       │    │  ┌─────────────────┐    │     │
│  │  - MiniMax      │    │  │ Chroma Example  │    │     │
│  │  - DeepSeek     │    │  ├─────────────────┤    │     │
│  │  - Tool Call    │    │  │ Redis Example   │    │     │
│  └────────┬────────┘    │  └─────────────────┘    │     │
│           │              └───────────┬────────────┘     │
│           ▼                          ▼                   │
│  ┌─────────────────┐    ┌─────────────────────────┐     │
│  │  Chat Memory    │    │    Embedding Model      │     │
│  │  (Advisor)      │    │    (MiniMax embo-01)    │     │
│  └─────────────────┘    └─────────────────────────┘     │
│                                                          │
│  ┌─────────────────┐    ┌─────────────────────────┐     │
│  │  MCP Client     │◄──►│      MCP Server         │     │
│  │  (连接外部服务)  │    │  (@McpTool 暴露工具)    │     │
│  └─────────────────┘    └─────────────────────────┘     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```