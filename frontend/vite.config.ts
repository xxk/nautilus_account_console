import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const apiBase = process.env.NAC_API_BASE ?? "http://127.0.0.1:8765";

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      allow: [".."]
    },
    proxy: {
      "/api": apiBase,
      "/healthz": apiBase
    }
  }
});
