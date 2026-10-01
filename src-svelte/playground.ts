import { mountShadowApp } from "./lib/mount-shadow";

import SwapApp from "./swap/index.svelte";
import OhMyLingo from "./ohmylingo/index.svelte";
import Comments from "./comments/index.svelte";

const mounts = {
  swap: SwapApp,
  ohmylingo: OhMyLingo,
  comments: Comments,
};

function mount(name: keyof typeof mounts) {
  // @ts-ignore
  const e = window.insert_component(name);
  const props = name === "comments" ? { articleId: "playground-test" } : {};
  mountShadowApp(mounts[name], e, props);
}

mount("swap");
mount("ohmylingo");
mount("comments");
// mount("other");
