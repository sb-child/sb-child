import { mountShadowApp } from "./lib/mount-shadow";

import SwapApp from "./swap/index.svelte";
import OhMyLingo from "./ohmylingo/index.svelte";

const mounts = {
  swap: SwapApp,
  ohmylingo: OhMyLingo,
};

function mount(name: keyof typeof mounts) {
  // @ts-ignore
  window.insert_component(name);
  mountShadowApp(mounts[name], name);
}

mount("swap");
mount("ohmylingo");
// mount("other");
