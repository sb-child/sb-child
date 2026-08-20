import { mountShadowApp } from "./lib/mount-shadow";

import SwapApp from "./swap/index.svelte";

function mount(name: string) {
  // @ts-ignore
  window.insert_component(name);
  mountShadowApp(SwapApp, name);
}

mount("swap");
// mount("other");
