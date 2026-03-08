import { defineConfig } from "vite";

export default defineConfig({
  base: "/static/core_api/frontend/",
  server: {
    port: 5173,
    host: true,
  },
  build: {
    rollupOptions: {
      output: {
        entryFileNames: "assets/app.js",
        chunkFileNames: "assets/chunk-[name].js",
        assetFileNames: (assetInfo) => {
          if (assetInfo.name?.endsWith(".css")) {
            return "assets/app.css";
          }
          return "assets/[name][extname]";
        },
      },
    },
  },
});
