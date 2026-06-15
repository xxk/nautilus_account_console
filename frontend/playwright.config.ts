import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  outputDir: "../docs/acceptance/browser-evidence/frontend-test-output",
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "retain-on-failure"
  },
  webServer: {
    command: "node node_modules/vite/bin/vite.js --host 127.0.0.1 --port 5173",
    reuseExistingServer: true,
    url: "http://127.0.0.1:5173"
  },
  projects: [
    {
      name: "desktop",
      use: { viewport: { width: 1440, height: 900 } }
    },
    {
      name: "tablet",
      use: { viewport: { width: 1024, height: 768 } }
    },
    {
      name: "mobile",
      use: { ...devices["Pixel 5"], viewport: { width: 390, height: 844 } }
    }
  ]
});
