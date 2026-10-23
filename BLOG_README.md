# 关于这个博客

## 如何在 Fedora 安装 Hugo

因为 Fedora 软件源的 hugo 已经落后很多个版本了。

```sh
# 你不需要它了
sudo dnf remove hugo

# 去 https://github.com/gohugoio/hugo/releases 找到最新版
wget -O hugo.tar.gz https://github.com/gohugoio/hugo/releases/download/v0.168.0/hugo_extended_0.168.0_linux-amd64.tar.gz
tar xvzf hugo.tar.gz hugo
# install 也会替你设置 selinux context
sudo install hugo /usr/local/bin/hugo
rm hugo hugo.tar.gz
```

## 本地开发

终端1: **启动后端**(用来拉取外部资源):

```sh
cd script
# 如果你有 GitHub API Token: echo 'xxx' > .gh_api_token
uv run main.py
```

终端2:

```sh
# 安装依赖
pnpm i
# 构建svelte组件。这是一次性的，直到下次svelte那边有变动
pnpm build

# 启动 Hugo 服务器 (构建前端)
hugo server
# 或者 hugo server -D 同时构建 draft 页面
```

如果你想调试 svelte 组件，你可以打开终端3:

```sh
# 安装依赖
pnpm i
# 启动 playground
pnpm dev
# 打开 http://localhost:5173/svelte-components/svelte-playground.html
```

## 别人的东西

**Mermaid**:

```sh
cd assets/js
rm mermaid.min.js
wget https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js
cd -
```

**ECharts**:

```sh
cd assets/js
rm echarts.min.js
wget https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js
cd -
```

**PaperMod**:

```sh
git submodule update --remote themes/PaperMod
```
