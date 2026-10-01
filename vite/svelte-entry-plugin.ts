import { globSync } from "glob";
import { basename, dirname } from "path";
import type { Plugin } from "vite";

const VIRTUAL_PREFIX = "\0virtual:svelte-entry:";

export function getSvelteEntries(): Record<string, string> {
  const files = globSync("src-svelte/*/index.svelte");
  const entries: Record<string, string> = {};

  for (const file of files) {
    const entryName = basename(dirname(file));
    entries[entryName] = VIRTUAL_PREFIX + entryName;
  }
  return entries;
}

export function svelteAutoMountPlugin(): Plugin {
  return {
    name: "vite-plugin-svelte-auto-mount",
    resolveId(id) {
      if (id.startsWith(VIRTUAL_PREFIX)) {
        return id;
      }
    },
    load(id) {
      if (id.startsWith(VIRTUAL_PREFIX)) {
        const entryName = id.replace(VIRTUAL_PREFIX, "");
        return `
import App from "/src-svelte/${entryName}/index.svelte";
import { mountShadowApp } from "/src-svelte/lib/mount-shadow";

const data = JSON.parse(
  document.getElementById("svelte-mount-data")?.textContent ?? "{}"
);

for (const { target, props } of data["${entryName}"] ?? []) {
  const host = document.getElementById(target);
  if (!host) { console.error(\`[svelte] [${entryName}] 找不到容器: \${target}\`); continue; }
  if (host.shadowRoot) { console.warn("[svelte] [${entryName}] 已挂载，跳过", host); continue; }
  console.log("[svelte] [${entryName}] mounted");
  mountShadowApp(App, host, props);
}
        `;
      }
    },
  };
}
