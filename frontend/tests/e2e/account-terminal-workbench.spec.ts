import { mkdirSync } from "node:fs";
import path from "node:path";
import { expect, test, type Page } from "@playwright/test";

const forbiddenCommandText =
  /Paper ready|Live ready|admitted|production ready|capital allocated|can trade|submit order|place order|cancel order|replace order/i;
const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p011-account-workbench-api-readback"
);

async function captureEvidence(page: Page, projectName: string, name: string) {
  mkdirSync(evidenceDir, { recursive: true });
  await page.screenshot({
    fullPage: true,
    path: path.join(evidenceDir, `${projectName}-${name}.png`),
  });
}

test.describe("T001 Account Terminal Workbench", () => {
  test("upgrades legacy acct.demo-19053 entry to Simulated 001 mirror projection", async ({
    page,
  }, testInfo) => {
    await page.goto("/accounts/acct.demo-19053");

    await expect(page.getByTestId("terminal-workbench-shell")).toBeVisible();
    await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
    await expect(page.getByTestId("terminal-top-status-bar")).toContainText("simulated-001");
    await expect(page.getByTestId("terminal-top-status-bar")).toContainText("Simulated 001");
    await expect(page.getByTestId("terminal-top-status-bar")).toContainText("sandbox-paper.simulated-001");
    await expect(page.getByTestId("account-selector")).toContainText("acct.ctp.paper.19053");
    await expect(page.getByTestId("account-selector")).toContainText("acct.nautilus.paper.demo");
    await expect(page.getByTestId("account-selector")).toContainText("simulated-001");
    await expect(page.getByTestId("account-selector")).toContainText("acct.ctp.live.025292");
    await expect(page.getByTestId("account-positions-table")).toContainText("ag2612");
    await expect(page.getByTestId("account-bottom-tape")).toContainText("simulated-001-ag2612-buy-1-001");
    await expect(page.getByText(forbiddenCommandText)).toHaveCount(0);
    await captureEvidence(page, testInfo.project.name, "legacy-acct-demo-19053-selector");
  });

  test("renders dense API-backed ready workspace for CTP paper 19053 real readback", async ({
    page,
  }, testInfo) => {
    await page.goto("/accounts/acct.ctp.paper.19053");

    await expect(page.getByTestId("terminal-workbench-shell")).toBeVisible();
    await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
    await expect(page.getByTestId("terminal-top-status-bar")).toContainText("acct.ctp.paper.19053");
    await expect(page.getByTestId("account-selector")).toContainText("19053");
    await expect(page.getByTestId("account-selector")).toContainText("acct.ctp.paper.19053");
    await expect(page.getByTestId("account-selector")).toContainText("acct.nautilus.paper.demo");
    await expect(page.getByTestId("account-capability-table")).toBeVisible();
    await expect(page.getByTestId("account-capability-row")).toHaveCount(4);
    await expect(page.getByTestId("account-capability-row").nth(0)).toContainText("F2");
    await expect(page.getByTestId("account-capability-row").nth(0)).toContainText("Observation");
    await expect(page.getByTestId("account-capability-row").nth(1)).toContainText("F4");
    await expect(page.getByTestId("account-capability-row").nth(1)).toContainText("CTP paper 19053");
    await expect(page.getByTestId("account-capability-row").nth(2)).toContainText("F3");
    await expect(page.getByTestId("account-capability-row").nth(3)).toContainText("F5");
    await expect(page.getByTestId("account-summary-metric-strip")).toContainText("Cash");
    await expect(page.getByTestId("account-summary-cash")).toContainText("CNY");
    await expect(page.getByTestId("account-positions-table")).toContainText("rb2610");
    await expect(page.getByTestId("account-bottom-tape")).toContainText("No open order rows in this mirror projection.");
    await expect(page.getByTestId("tws-fill-count")).toContainText("5");
    await expect(page.getByTestId("tws-fills-table")).toContainText("zn2610");
    await expect(page.getByTestId("account-order-execution-report")).toContainText("FillReport");
    await expect(page.getByTestId("account-source-health-panel")).toContainText("normalized_read_model");
    await expect(page.getByTestId("account-evidence-rail")).toContainText("source package");
    await expect(page.getByTestId("account-evidence-rail")).toContainText("mirror projection");
    await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
    await expect(page.getByTestId("account-command-capability-state")).toContainText("none mounted");
    await expect(page.getByText(forbiddenCommandText)).toHaveCount(0);
    await captureEvidence(page, testInfo.project.name, "ctp19053-api-readback");
  });

  test("keeps blocked 025292 live account fail-closed in UI", async ({ page }, testInfo) => {
    await page.goto("/accounts/acct.ctp.live.025292");

    await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
    await expect(page.getByTestId("terminal-top-status-bar")).toContainText("acct.ctp.live.025292");
    await expect(page.getByTestId("account-positions-table")).toContainText(
      "No position rows in this fixture projection."
    );
    await expect(page.getByTestId("account-bottom-tape")).toContainText("No open order rows in this mirror projection.");
    await expect(page.getByTestId("account-order-execution-report")).toContainText("source unavailable");
    await expect(page.getByTestId("account-order-execution-report")).toContainText(
      "output/account_capability/ctp-live-025292/source-package.json"
    );
    await expect(page.getByTestId("account-source-health-panel")).toContainText("typed_blocker");
    await expect(page.getByTestId("account-blocker-row")).toContainText("source unavailable");
    await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
    await expect(page.getByText(forbiddenCommandText)).toHaveCount(0);
    await captureEvidence(page, testInfo.project.name, "ctp025292-blocked");
  });

  test("renders R1 P079 Stage 2 simulated-001 as sandbox paper projection only", async ({ page }, testInfo) => {
    await page.goto("/accounts/simulated-001");

    await expect(page.getByTestId("account-readback-mode")).toContainText("mirror API");
    await expect(page.getByTestId("terminal-top-status-bar")).toContainText("simulated-001");
    await expect(page.getByTestId("terminal-top-status-bar")).toContainText("sandbox-paper.simulated-001");
    await expect(page.getByTestId("account-selector")).toContainText("simulated-001");
    await expect(page.getByTestId("account-source-health-panel")).toContainText(
      "CTP 025292 official market data only"
    );
    await expect(page.getByTestId("account-source-health-panel")).toContainText("Nautilus Sandbox Paper");
    await expect(page.getByTestId("account-source-health-panel")).toContainText("simulated ledger only");
    await expect(page.getByTestId("account-source-health-panel")).toContainText("Broker submission");
    await expect(page.getByTestId("account-source-health-panel")).toContainText("disabled");
    await expect(page.getByTestId("account-source-health-panel")).toContainText("simulated_sandbox_ledger");
    await expect(page.getByTestId("account-source-health-panel")).toContainText("R1/P079 Stage 2");
    await expect(page.getByTestId("account-positions-table")).toContainText("ag2612");
    await expect(page.getByTestId("account-positions-table")).toContainText("LONG");
    await expect(page.getByTestId("account-bottom-tape")).toContainText("simulated-001-ag2612-buy-1-001");
    await expect(page.getByTestId("account-bottom-tape")).toContainText("filled");
    await expect(page.getByTestId("account-command-capability-state")).toContainText("observation only");
    await expect(page.getByText(forbiddenCommandText)).toHaveCount(0);
    await captureEvidence(page, testInfo.project.name, "simulated-001-stage2");
  });
});
