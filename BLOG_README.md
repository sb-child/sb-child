# 关于这个博客

## 本地开发

终端1: **启动后端**(用来拉取外部资源):

```sh
cd script
# 如果你有 GitHub API Token: echo 'xxx' > .gh_api_token
uv run main.py
```

终端2: **启动 Hugo 服务器**(编译前端):

```sh
hugo server
```

## 别人的东西

**Mermaid**:

```sh
cd assets/js
rm mermaid.min.js
wget https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js
```

**ECharts**:

```sh
cd assets/js
rm echarts.min.js
wget https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js
```

**PaperMod**:

```sh
git submodule update --remote themes/PaperMod
```
