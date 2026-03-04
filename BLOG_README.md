# Hugo 博客部署指南

这是一个使用 Hugo 和 PaperMod 主题搭建的个人博客，配置了 GitHub Actions 自动部署到 GitHub Pages。

## 项目结构

```
.
├── .github/
│   └── workflows/
│       └── hugo.yml          # GitHub Actions 工作流
├── archetypes/               # 文章模板
├── content/                  # 博客内容
│   ├── archives.md          # 归档页面
│   └── posts/               # 文章目录
│       └── welcome.md       # 示例文章
├── themes/
│   └── PaperMod/            # PaperMod 主题（git submodule）
├── hugo.toml                # Hugo 配置文件
└── .gitignore               # Git 忽略文件
```

## 部署步骤

### 1. 推送代码到 GitHub

```bash
git add .
git commit -m "Initial Hugo blog setup"
git push origin main
```

### 2. 配置 GitHub Pages

1. 进入你的 GitHub 仓库 (sb-child.github.io)
2. 点击 **Settings** > **Pages**
3. 在 **Source** 部分，选择 **GitHub Actions**

### 3. 自动部署

推送代码后，GitHub Actions 会自动：

- 安装 Hugo
- 构建静态网站
- 部署到 GitHub Pages

你可以在仓库的 **Actions** 标签页查看部署进度。

## 本地预览

在本地预览博客：

```bash
hugo server -D
```

然后访问 http://localhost:1313

## 创建新文章

使用 Hugo 命令创建新文章：

```bash
hugo new posts/my-new-post.md
```

文章会在 [`content/posts/`](content/posts/) 目录下创建。

## 配置说明

主要配置在 [`hugo.toml`](hugo.toml) 文件中：

- `baseURL`: 你的网站地址
- `title`: 网站标题
- `theme`: 使用的主题
- `params`: 主题参数配置

## 主题文档

PaperMod 主题文档：https://github.com/adityatelange/hugo-PaperMod/wiki

## 常见问题

### 子模块未初始化

如果克隆仓库后主题目录为空，运行：

```bash
git submodule update --init --recursive
```

### 修改主题配置

编辑 [`hugo.toml`](hugo.toml) 文件中的 `[params]` 部分来自定义主题。

### 添加评论系统

可以在 [`hugo.toml`](hugo.toml) 中配置 Disqus、Utterances 等评论系统。

## 许可证

本博客框架基于 Hugo 和 PaperMod 主题构建。
