+++
date = '2026-08-28T23:33:33+08:00'
draft = false
title = 'Rust 的平台怎么跨到 Android 上'
description = '你的二进制能够到 Java World 吗?'
+++

你的二进制够不到 Java World。

最近在做一个项目 [my-remote-speaker](https://github.com/sb-child/my-remote-speaker)，我第一个准备支持的平台就是安卓。因为安卓真的是太可怕了，我还没来得及写客户端。

其实很多场景用不到你碰安卓的 JVM，比如你随便 `cargo new fuck-android` 和 [`cargo install cargo-ndk`](https://github.com/bbqsrc/cargo-ndk)，然后你就可以 `cargo ndk --platform 35 -t arm64-v8a build` 完成了。

但是如果你要碰怎么办... 像我项目里 [cpal](https://github.com/RustAudio/cpal) 要调用安卓的 AAudio，要在程序开头搞到两个指针初始化 `ndk_context::initialize_android_context(vm_ptr, activity_ptr)`。cpal 官方的例子是 [cargo-apk](https://github.com/rust-mobile/cargo-apk) 一键编译出动态库然后打包成 apk 文件所以完全不用顾虑。

---

ok 据我了解，为了拿到那两个指针，首先需要这个程序是被 Java 以 JNI 的形式跑起来的。其次不要想着给那两个参数传空指针，后面有断言。

在安卓里，有个神秘的程序 `/system/bin/app_process`，它可以凭空带着安卓的 Java 环境起一个 dex 文件。
