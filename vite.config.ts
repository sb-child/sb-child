import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { resolve } from "path";
import { globSync } from "glob";

export default defineConfig({
  plugins: [svelte({})],
  build: {
    outDir: resolve(import.meta.dirname, "static/svelte-components"),
    emptyOutDir: true,
    manifest: true,
    copyPublicDir: false,
    rollupOptions: {
      input: globSync("src-svelte/**/main.ts").reduce(
        (acc, file) => {
          const entryName = file
            .replace(/\\/g, "/")
            .replace(/^src-svelte\//, "")
            .replace(/\/main\.ts$/, "");
          acc[entryName] = resolve(import.meta.dirname, file);
          return acc;
        },
        {} as Record<string, string>,
      ),
      output: {
        entryFileNames: "[name]-[hash].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash].[ext]",
        format: "iife",
      },
    },
  },
});
