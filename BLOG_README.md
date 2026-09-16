# 关于这个博客

## 本地开发

终端1: **启动后端**(用来拉取外部资源):

```sh
cd script
# 如果你有 GitHub API Token: echo 'xxx' > .gh_api_token
uv run main.py
```

终端2:

```sh
# 构建svelte组件
pnpm i
pnpm build
# 启动 Hugo 服务器 (构建前端)
hugo server
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
