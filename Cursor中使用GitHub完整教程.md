# Cursor中使用GitHub完整教程

## 🎯 教程概述

本教程基于实际操作经验，详细介绍如何在Cursor编辑器中使用GitHub进行代码版本管理和协作开发。

## 📋 前置准备

### 1. 环境要求
- ✅ 已安装Cursor编辑器
- ✅ 已安装Git（通常Cursor会自动包含）
- ✅ 拥有GitHub账号
- ✅ 项目代码已准备就绪

### 2. GitHub仓库准备
- 在GitHub上创建新的空仓库
- 记录仓库URL：`https://github.com/用户名/仓库名.git`

## 🚀 完整操作流程

### 步骤1：项目初始化

在Cursor中打开终端（Ctrl+` 或 Cmd+`），执行以下命令：

```bash
# 检查是否已经初始化Git
git status

# 如果没有初始化，执行：
git init

# 设置用户信息（首次使用时）
git config --global user.name "您的用户名"
git config --global user.email "您的邮箱"
```

### 步骤2：配置.gitignore文件

**关键重要！** 在添加文件前，必须先配置`.gitignore`文件：

```gitignore
# Python项目示例
*/__pycache__
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
*.egg

# 虚拟环境
venv/
env/
ENV/
.venv/

# IDE文件
.vscode/
.idea/
*.swp
*.swo

# 系统文件
*/.DS_Store
.DS_Store
Thumbs.db

# 日志文件
*.log
logs/

# 生成的文件
dist/
build/
*.html
*.json

# 备份文件
*.zip
*.tar.gz
*.bak

# 敏感信息
.env
config/secrets.toml

# 大文件和临时文件
*.sqlite
*.db
node_modules/
```

### 步骤3：添加文件到暂存区

```bash
# 添加所有文件（会自动排除.gitignore中的文件）
git add .

# 或者添加特定文件
git add 文件名.py

# 检查暂存状态
git status
```

### 步骤4：提交更改

```bash
# 提交暂存的文件
git commit -m "🚀 Initial commit: 项目初始版本"

# 查看提交历史
git log --oneline
```

### 步骤5：连接GitHub仓库

```bash
# 添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git

# 验证远程仓库配置
git remote -v

# 如果需要修改远程仓库地址
git remote set-url origin https://github.com/新用户名/新仓库名.git
```

### 步骤6：推送到GitHub

```bash
# 首次推送（创建主分支）
git push -u origin main

# 后续推送
git push origin main
```

## 🔄 日常开发工作流

### 修改代码后的标准流程

```bash
# 1. 查看文件状态
git status

# 2. 查看具体修改内容
git diff

# 3. 添加修改的文件
git add .

# 4. 提交更改
git commit -m "✨ 添加新功能：知识图谱中文支持"

# 5. 推送到GitHub
git push origin main
```

### 提交信息规范

使用语义化的提交信息：

```bash
git commit -m "🚀 feat: 添加新功能"
git commit -m "🐛 fix: 修复已知问题"
git commit -m "📚 docs: 更新文档"
git commit -m "🎨 style: 代码格式优化"
git commit -m "♻️ refactor: 代码重构"
git commit -m "⚡ perf: 性能优化"
git commit -m "✅ test: 添加测试"
```

## 🛠️ Cursor特定技巧

### 1. 使用Cursor内置Git功能

```bash
# Cursor中可以直接使用AI助手执行Git命令
# 在聊天框中输入："帮我提交代码并推送到GitHub"
# AI会自动执行相应的Git命令
```

### 2. 代码差异查看

```bash
# 查看未暂存的修改
git diff

# 查看已暂存的修改
git diff --staged

# 查看特定文件的修改
git diff 文件名.py
```

### 3. 撤销操作

```bash
# 撤销工作区的修改
git checkout -- 文件名.py

# 撤销暂存区的修改
git reset HEAD 文件名.py

# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 完全撤销最后一次提交
git reset --hard HEAD~1
```

## ⚠️ 常见问题及解决方案

### 问题1：权限被拒绝
```bash
# 错误信息：Permission denied
# 解决方案：检查仓库URL是否正确
git remote set-url origin https://github.com/正确用户名/正确仓库名.git
```

### 问题2：网络连接失败
```bash
# 错误信息：Connection reset by peer
# 解决方案：重试推送，或检查网络连接
git push origin main
```

### 问题3：虚拟环境被误提交
```bash
# 解决方案：
# 1. 更新.gitignore文件添加venv/
# 2. 移除已跟踪的虚拟环境文件
git rm -r --cached venv/
git commit -m "🔥 移除虚拟环境文件"
```

### 问题4：大文件推送失败
```bash
# 解决方案：添加到.gitignore并移除
echo "*.zip" >> .gitignore
git rm --cached 大文件.zip
git commit -m "🔥 移除大文件"
```

## 🏆 最佳实践

### 1. .gitignore配置最佳实践
- ✅ 项目开始时就配置.gitignore
- ✅ 排除虚拟环境和依赖包
- ✅ 排除生成的文件和日志
- ✅ 排除敏感信息和配置文件

### 2. 提交频率建议
- ✅ 功能完成后立即提交
- ✅ 每天至少提交一次
- ✅ 重要里程碑单独提交
- ✅ 修复bug后立即提交

### 3. 分支管理策略
```bash
# 创建功能分支
git checkout -b feature/新功能名称

# 开发完成后合并到主分支
git checkout main
git merge feature/新功能名称

# 删除已合并的分支
git branch -d feature/新功能名称
```

### 4. 代码同步建议
```bash
# 开始工作前先拉取最新代码
git pull origin main

# 推送前检查是否有冲突
git status
git push origin main
```

## 📊 实际案例演示

基于我们刚才的AI知识图谱项目：

```bash
# 1. 项目结构检查
ls -la

# 2. 配置.gitignore（排除venv、日志、生成文件）
# 3. 添加所有源代码文件
git add .

# 4. 初始提交
git commit -m "🚀 Initial commit: AI知识图谱项目完整版本"

# 5. 设置正确的远程仓库
git remote set-url origin https://github.com/huangying-just/ai-knowledge-graph.git

# 6. 推送到GitHub
git push origin main

# 结果：成功推送351个对象，1.04MB代码
```

## 🎉 成功标志

当您看到类似输出时，说明操作成功：

```bash
Enumerating objects: 351, done.
Counting objects: 100% (351/351), done.
Delta compression using up to 16 threads
Compressing objects: 100% (150/150), done.
Writing objects: 100% (351/351), 1.04 MiB | 212.82 MiB/s, done.
Total 351 (delta 194), reused 318 (delta 186), pack-reused 0
To https://github.com/用户名/仓库名.git
 * [new branch]      main -> main
```

## 🔗 相关资源

- [Git官方文档](https://git-scm.com/doc)
- [GitHub官方指南](https://docs.github.com)
- [Cursor编辑器文档](https://cursor.sh)
- [语义化提交规范](https://www.conventionalcommits.org)

---

**💡 小贴士：** 在Cursor中，您可以直接与AI助手对话来执行Git操作，这是相比其他编辑器的独特优势！

**🚀 现在就开始您的GitHub协作之旅吧！** 