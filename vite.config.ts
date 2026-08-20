import { defineConfig } from "vite";
import { resolve } from "path";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import tailwindcss from "@tailwindcss/vite";
import {
  svelteAutoMountPlugin,
  getSvelteEntries,
} from "./vite/svelte-entry-plugin.ts";

export default defineConfig({
  plugins: [svelteAutoMountPlugin(), svelte(), tailwindcss()],
  server: {
    open: "/svelte-components/svelte-playground.html",
  },
  resolve: {
    alias: {
      $lib: resolve("./src-svelte/lib"),
    },
  },
  base: "/svelte-components/",
  build: {
    outDir: resolve(import.meta.dirname, "static/svelte-components"),
    emptyOutDir: true,
    manifest: true,
    copyPublicDir: false,
    rollupOptions: {
      input: getSvelteEntries(),
      output: {
        entryFileNames: "[name]-[hash].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash].[ext]",
        format: "iife",
      },
    },
  },
});
