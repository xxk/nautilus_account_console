import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";
import path from "node:path";

const evidenceDir = path.resolve(
  "..",
  "docs",
  "acceptance",
  "browser-evidence",
  "p079-r1-account-console-projection"
);

const forbiddenVisibleText = new RegExp(
  [
    ["Paper", "ready"].join(" "),
    ["Live", "ready"].join(" "),
    "admit" + "ted",
    ["production", "ready"].join(" "),
    ["capital", "allocated"].join(" "),
    ["can", "trade"].join(" "),
    ["submit", "order"].join(" "),
    ["place", "order"].join(" "),
    ["cancel", "order"].join(" "),
    ["replace", "order"].join(" ")
  ].join("|"),
  "i"
);

test.describe("P079 R1 Account Console projection", () => {
  test("renders CTA-CORE-001 read-only fixtures with source refs", async ({ page }, testInfo) => {
    mkdirSync(evidenceDir, { recursive: true });

    await page.goto("/accounts/acct.demo-19053");
    await page.getByLabel("Fixture").selectOption("r1_cta_core_001");
    await expect(page.getByTestId("account-workbench-summary-panel")).toBeVisible();
    await expect(page.getByTestId("account-workbench-context-bar")).toContainText("CTA-CORE-001");
    await expect(page.getByTestId("account-workbench-context-bar")).toContainText("19053");
    await expect(page.getByText("acct.r1-cta-core-001-19053").first()).toBeVisible();
    await expect(page.getByTestId("account-summary-source-ref").first()).toBeVisible();
    await expect(page.getByTestId("account-summary-boundary-list")).toContainText("Read-only projection");
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-summary-r1.png`)
    });

    await page.goto("/accounts/acct.demo-19053/positions");
    await page.getByLabel("Fixture").selectOption("r1_cta_core_001");
    await expect(page.getByTestId("account-positions-panel")).toBeVisible();
    await expect(page.getByTestId("account-positions-table")).toContainText("IC");
    await expect(page.getByTestId("account-positions-table")).toContainText("IF");
    await expect(page.getByTestId("account-positions-source-ref").first()).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-positions-r1.png`)
    });

    await page.goto("/accounts/acct.demo-19053/reconcile");
    await page.getByLabel("Fixture").selectOption("r1_cta_core_001");
    await expect(page.getByTestId("account-reconcile-panel")).toBeVisible();
    await expect(page.getByTestId("account-reconcile-table")).toContainText("p079.target-vs-actual.ic");
    await expect(page.getByTestId("account-reconcile-table")).toContainText("p079.target-vs-actual.if");
    await expect(page.getByTestId("account-reconcile-source-ref").first()).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-reconcile-r1.png`)
    });

    await page.goto("/accounts/acct.demo-19053/evidence");
    await page.getByLabel("Fixture").selectOption("r1_cta_core_001");
    await expect(page.getByTestId("account-evidence-panel")).toBeVisible();
    await expect(page.getByTestId("account-evidence-table")).toContainText(
      "p079.phase2.signal-to-paper-position.closeout"
    );
    await expect(page.getByTestId("account-evidence-source-ref").first()).toBeVisible();
    await expect(page.getByText(forbiddenVisibleText)).toHaveCount(0);
    await page.screenshot({
      fullPage: true,
      path: path.join(evidenceDir, `${testInfo.project.name}-evidence-r1.png`)
    });
  });
});
