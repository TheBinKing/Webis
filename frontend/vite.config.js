import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

import Markdown from "vite-plugin-md";

// https://vitejs.dev/config/
export default defineConfig({
  base: "./",
  plugins: [
    vue({
      include: [/\.vue$/, /\.md$/],
    }),
    Markdown({
      builders: [],
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: {
    target: "esnext", // 支持顶层 await
    outDir: "dist",
    assetsDir: "assets",
  },
  esbuild: {
    // 配置 esbuild 以支持顶层 await
    supported: {
      'top-level-await': true
    }
  }
});
