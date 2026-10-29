---
title: "你好喵"
date: 2026-03-04T14:55:00+08:00
draft: false
description: "喜报，旧站依赖爆炸，新站遥遥无期"
tags: ["website"]
categories: ["系统信息"]
---

时隔一年我们又见面了。

## 我博客死了

为了保住我在 Google Search Console 中的优异成绩，我重开了。

- 提升 sbchild.top 在 Google 中的存在状况
- 恭喜，您的网站在 28 天内获得 5 次点击！
- 新原因导致网站 sbchild.top 上的网页无法被编入索引
- 在针对 sbchild.top 提交的网址中检测到新的网页索引编制问题
- 新原因导致网站 sbchild.top 的站点地图中的网页无法被编入索引

本站 (https://gh.sbchild.top/) 部署在 GitHub Pages。

~~放心，故居已经全部 302 重定向到本站。~~

~~为什么不是 301？我怕 GitHub Pages 也爆炸。~~

这个窟窿我终于堵上了，去看看主站: <https://sbchild.top/>。

如果你怀念我的旧站，请移步[这里]({{< relref "/about.md#你博客去哪了" >}})。

## 本站结构

在你为本站做出贡献之前，你应该先了解本站结构：

主站 **sbchild.top**:

- 源码 [sb-child/sbchild.top](https://github.com/sb-child/sbchild.top)
- 没有 CI，意味着网站是我手动部署的
- 部署到 [Cloudflare Workers](https://www.cloudflare.com/products/workers/)
- README.md 有些是 AI 帮我写的，你看看就行了不要全信
- 依赖 [sb-child/sbchild-top-wasm](https://github.com/sb-child/sbchild-top-wasm)，package 托管在 [@sb-child/sbchild-top-wasm](https://github.com/sb-child/sbchild-top-wasm/pkgs/npm/sbchild-top-wasm)

博客站 **gh.sbchild.top**:

- 源码 [sb-child/sb-child](https://github.com/sb-child/sb-child)
- 有 CI，意味着只要提交到 main 分支就会部署
- 部署到 [GitHub Pages](https://pages.github.com/)
- README.md 是 [BLOG_README.md](https://github.com/sb-child/sb-child/blob/main/BLOG_README.md)

不然你会迷路找不到我站源码在哪。
