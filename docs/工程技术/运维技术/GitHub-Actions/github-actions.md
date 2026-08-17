---
title: GitHub Actions 分支+路径触发
weight: 10
---

# GitHub Actions 分支+路径触发 核心写法总结

这两段是 **GitHub Actions 精准触发工作流** 的标准写法，核心是：**按分支 + 文件路径（包含/排除）过滤，避免无效构建**。

我把规则、语法、用法一次性总结清楚，直接套用即可：

---

## 一、核心触发规则（必记）
### 1. 触发事件
- `push`：代码推送到分支时触发
- `pull_request`：PR 合并/更新到目标分支时触发
- `workflow_dispatch`：**允许手动点击运行**（页面手动触发）

### 2. 分支过滤
```yaml
branches:
  - main  # 仅 main 分支触发
```

### 3. 路径过滤（最关键）
两种互斥用法：
| 语法 | 作用 | 示例 |
|------|------|------|
| `paths` | **仅当指定路径文件变化时才触发** | 只部署 Nginx |
| `paths-ignore` | **指定路径文件变化时不触发** | 排除 Nginx 配置更新 |

路径通配符：
- `nginx/**`：nginx 目录下**所有文件/子目录**都匹配
- `*.js`：根目录下所有 js 文件

---

## 二、两段配置的核心逻辑（一句话总结）
1. **Nginx 部署工作流**
   `main 分支 + 仅 nginx 目录文件改动` → 触发，支持手动运行。

2. **应用部署工作流**
   `main 分支 push/PR合并 + 排除 nginx 目录改动` → 触发。

---

## 三、标准模板（直接复制用）
### 模板1：仅指定目录改动时触发（如 Nginx）
```yaml
name: 部署 Nginx
on:
  push:
    branches: [ main ]
    paths:
      - 'nginx/**'  # 仅该目录变化才触发
  workflow_dispatch:  # 允许手动触发
```

### 模板2：排除指定目录，其他变化才触发（如应用代码）
```yaml
name: 部署应用
on:
  push:
    branches: [ main ]
    paths-ignore:
      - 'nginx/**'  # 该目录变化不触发
  pull_request:
    branches: [ main ]
    paths-ignore:
      - 'nginx/**'
```

---

## 四、关键注意事项
1. **`paths` 和 `paths-ignore` 不能同时用**（互斥）
2. 路径必须用**单引号/双引号**包裹，避免解析错误
3. 两个工作流配合使用，可实现：
   - Nginx 配置更新 → 只跑 Nginx 部署
   - 业务代码更新 → 只跑应用部署
   - 互不干扰，节省 CI 资源

---

### 总结
1. 核心：**分支 + 路径过滤** 实现精准触发
2. `paths`：白名单（只匹配我才运行）
3. `paths-ignore`：黑名单（匹配我就不运行）
4. `workflow_dispatch`：加一行就能手动触发